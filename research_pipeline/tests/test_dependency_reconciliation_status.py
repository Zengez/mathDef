"""Read-only reconciliation status is grounded in receipts and live IDs."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import PipelineError, digest
from research_pipeline.engine.dependency_reconciliation_status import (
    reconciliation_status,
)


class ReconciliationStatusTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.graph = self.root / "dependency_graph"
        (self.graph / "inbox").mkdir(parents=True)
        (self.graph / "applied").mkdir()
        self.node = {"formulation_id": "form.example",
                     "references": [{"occurrence_id": "occ.one",
                                    "state": "existing",
                                    "target_meaning_id": "meaning.old"}]}
        self.snapshot = {
            "state": {"summary": {
                "unresolved_missing_candidates": 420,
                "unresolved_fingerprint": "fingerprint-live",
                "scan_amendment_event_count": 771,
                "phase": "consolidate_occurrences",
                "consolidation_gate_valid": False}},
            "inventory": {"source_inventory_sha256": "inventory-live",
                          "formulations": {"form.example": {"id": "form.example"}}},
            "nodes": {"form.example": self.node},
        }
        self.packet = {"schema_version": 1, "id": "alias.proposal",
                       "mode": "alias", "aliases": []}
        self.queue = {"schema_version": 1, "cases": [
            {"id": "operator-alias", "kind": "transaction",
             "packet_id": "alias.proposal", "mode": "alias",
             "packet_sha256": digest(self.packet)},
            {"id": "remaining-edge-review", "kind": "review",
             "formulation_id": "form.example", "expected_occurrence_id": "occ.one",
             "expected_node_sha256": digest(self.node),
             "expected_state": "existing",
             "expected_target_meaning_id": "meaning.old"},
        ]}

    def report(self):
        return reconciliation_status(self.root, self.queue,
                                     snapshot=self.snapshot)

    def write(self, kind, contents):
        p = self.graph / kind / "alias.proposal.json"
        p.write_text(json.dumps(contents), encoding="utf-8")

    def test_missing_transaction_and_anchored_review(self):
        report = self.report()
        self.assertEqual([x["status"] for x in report["cases"]],
                         ["not_submitted", "mathematical_review_required"])
        self.assertFalse(report["authorizes_gate_change"])
        self.assertFalse(report["authorizes_submission"])
        self.assertEqual(report["current_unresolved_canonical"], 420)

    def test_actual_packet_and_receipt_both_required(self):
        self.write("inbox", self.packet)
        self.assertEqual(self.report()["cases"][0]["status"],
                         "submitted_awaiting_receipt")
        receipt = {
            "id": self.packet["id"], "mode": "alias",
            "sha256": digest(self.packet),
            "status": "applied_in_independent_graph_only",
            "human_certified": False,
        }
        self.write("applied", receipt)
        applied = self.report()["cases"][0]
        self.assertEqual(applied["status"], "applied_receipt_verified")
        self.assertTrue(applied["receipt_matches"])
        self.assertFalse(applied["mathematically_certified"])

    def test_orphan_receipt_and_bad_hash_fail_closed(self):
        receipt = {"id": "alias.proposal", "mode": "alias",
                   "sha256": digest(self.packet),
                   "status": "applied_in_independent_graph_only"}
        self.write("applied", receipt)
        self.assertEqual(self.report()["cases"][0]["status"],
                         "receipt_or_packet_conflict")
        self.write("inbox", {**self.packet, "aliases": [{"not": "original"}]})
        self.assertEqual(self.report()["cases"][0]["status"],
                         "receipt_or_packet_conflict")
        self.write("inbox", self.packet)
        self.write("applied", {**receipt, "sha256": "0" * 64})
        self.assertEqual(self.report()["cases"][0]["status"],
                         "receipt_or_packet_conflict")

    def test_stale_review_and_changed_reference(self):
        case = self.queue["cases"][1]
        self.node["references"][0]["target_meaning_id"] = "meaning.new"
        self.assertEqual(self.report()["cases"][1]["status"],
                         "needs_effective_node_reanchor")
        case["expected_node_sha256"] = digest(self.node)
        self.assertEqual(self.report()["cases"][1]["status"],
                         "reference_target_changed")
        self.node["references"][0]["occurrence_id"] = "occ.two"
        case["expected_node_sha256"] = digest(self.node)
        self.assertEqual(self.report()["cases"][1]["status"],
                         "occurrence_changed_or_ambiguous")

    def test_invalid_or_repeated_case_rejected(self):
        self.queue["cases"].append(dict(self.queue["cases"][0]))
        with self.assertRaisesRegex(PipelineError, "unique"):
            self.report()
        self.queue["cases"][-1]["id"] = "../unsafe"
        with self.assertRaisesRegex(PipelineError, "path-safe"):
            self.report()
        self.queue["cases"].pop()
        self.queue["cases"][0]["packet_sha256"] = "wrong"
        with self.assertRaisesRegex(PipelineError, "SHA256"):
            self.report()


    def test_repository_queue_matches_current_graph_receipts(self):
        """The current checkout, not an audit narrative, determines application."""
        repo = Path(__file__).resolve().parents[2]
        workspace = repo / "research_pipeline/experiments/reconstruction-v2-independent"
        queue_path = (repo / "research_pipeline/reviews/"
                      "canonical-identity-2026-10-24/LIVE_RECONCILIATION_QUEUE.json")
        queue = json.loads(queue_path.read_text(encoding="utf-8"))
        report = reconciliation_status(workspace, queue)
        self.assertEqual(report["case_count"], 4)
        self.assertFalse(report["graph_changes_applied"])
        self.assertFalse(report["current_consolidation_gate_valid"])
        self.assertEqual(report["current_phase"], "consolidate_occurrences")
        self.assertTrue(report["historical_review_scope"]
                        ["canonical_reviews_complete"] == 421)
        for case in report["cases"]:
            self.assertFalse(case["mathematically_certified"])
            if case["kind"] == "transaction":
                receipt = (workspace / "dependency_graph/applied"
                           / (case["packet_id"] + ".json"))
                expected = ("applied_receipt_verified" if receipt.exists()
                            else "not_submitted")
                self.assertEqual(case["status"], expected)
            else:
                self.assertIn(case["status"], (
                    "mathematical_review_required", "needs_effective_node_reanchor",
                    "reference_target_changed", "reference_disposition_changed",
                    "occurrence_changed_or_ambiguous"))

    def test_no_file_write(self):
        self.write("inbox", self.packet)
        files = [p for p in self.graph.rglob("*") if p.is_file()]
        before = {str(p): p.read_bytes() for p in files}
        self.report()
        self.assertEqual(before,
                         {str(p): p.read_bytes() for p in files})


if __name__ == "__main__":
    unittest.main()
