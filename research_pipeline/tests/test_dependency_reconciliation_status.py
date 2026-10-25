"""Read-only reconciliation status is grounded in receipts and live IDs."""
import json
from copy import deepcopy
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import PipelineError, digest
from research_pipeline.engine.dependency_graph import meaning_version
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
        self.assertEqual(report["case_count"], len(queue["cases"]))
        self.assertEqual(report["status_counts"], {
            "applied_receipt_verified": 6, "superseded_by_verified_transaction": 2})
        self.assertEqual(report["active_review_case_count"], 0)
        self.assertEqual(report["current_active_aliases"], 300)
        self.assertEqual(report["historical_alias_event_count"], 301)
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
                self.assertEqual(case["status"], "superseded_by_verified_transaction")
                self.assertEqual(case["superseded_by_case_ids"],
                                 ["ext-hom-local-connectedness-amendment"])
        # Independently verify actual packet hashes rather than trusting the
        # status labels. Resolve is a distinct transaction mode, not an alias.
        for case in queue["cases"]:
            if case["kind"] != "transaction":
                continue
            graph = workspace / "dependency_graph"
            packet = json.loads((graph / "inbox" / (case["packet_id"] + ".json")).read_text())
            receipt = json.loads((graph / "applied" / (case["packet_id"] + ".json")).read_text())
            self.assertEqual(digest(packet), case["packet_sha256"])
            self.assertEqual(receipt["sha256"], digest(packet))
            self.assertEqual(receipt["id"], packet["id"])
            self.assertEqual(receipt["mode"], packet["mode"])
        for case in report["cases"]:
            for effect in case.get("current_resolution_effects", []):
                self.assertTrue(effect["target_version_matches_current_meaning"])
                self.assertTrue(effect["registry_target_matches"])
                self.assertTrue(effect["resolution_ledger_matches"])

    def set_superseding_amendment(self):
        self.historical_node = deepcopy(self.node)
        review = self.queue["cases"][1]
        review["superseded_by_case_ids"] = ["operator-alias"]
        self.packet = {"schema_version": 1, "id": "alias.proposal", "mode": "amend",
                       "amendments": [{"formulation_id": "form.example",
                                       "expected_node_sha256": digest(self.node)}]}
        transaction = self.queue["cases"][0]
        transaction.update(mode="amend", packet_sha256=digest(self.packet))
        self.write("inbox", self.packet)
        self.write("applied", {"id": self.packet["id"], "mode": "amend",
                               "sha256": digest(self.packet),
                               "status": "applied_in_independent_graph_only"})
        self.node["references"] = [{"occurrence_id": "occ.new", "state": "external"}]

    def test_exact_receipt_backed_supersession_preserves_historical_anchor(self):
        self.set_superseding_amendment()
        original = deepcopy(self.queue)
        report = self.report()
        review = report["cases"][1]
        self.assertEqual(review["status"], "superseded_by_verified_transaction")
        self.assertEqual(review["historical_anchor_status"], "needs_effective_node_reanchor")
        self.assertEqual(review["expected_occurrence_id"], "occ.one")
        self.assertEqual(report["active_review_case_count"], 0)
        self.assertEqual(report["superseded_review_case_count"], 1)
        self.assertEqual(self.queue, original)
        self.queue["cases"].reverse()
        reordered = self.report()
        self.assertEqual({r["id"]: r["status"] for r in report["cases"]},
                         {r["id"]: r["status"] for r in reordered["cases"]})

    def test_supersession_without_verified_receipt_remains_actionable(self):
        self.set_superseding_amendment()
        (self.graph / "applied/alias.proposal.json").unlink()
        report = self.report()
        self.assertEqual(report["cases"][1]["status"], "supersession_requires_receipt_verification")
        self.assertEqual(report["active_review_case_count"], 1)
        self.write("applied", {"id": "alias.proposal", "mode": "amend", "sha256": "0" * 64,
                               "status": "applied_in_independent_graph_only"})
        self.assertEqual(self.report()["cases"][1]["status"],
                         "supersession_requires_receipt_verification")

    def test_unrelated_or_wrong_predecessor_packet_cannot_retire_review(self):
        self.set_superseding_amendment()
        for field, value in [("formulation_id", "form.other"), ("expected_node_sha256", "0" * 64)]:
            packet = deepcopy(self.packet)
            packet["amendments"][0][field] = value
            self.queue["cases"][0]["packet_sha256"] = digest(packet)
            self.write("inbox", packet)
            self.write("applied", {"id": "alias.proposal", "mode": "amend", "sha256": digest(packet),
                                   "status": "applied_in_independent_graph_only"})
            self.assertEqual(self.report()["cases"][1]["status"], "supersession_anchor_mismatch")

    def test_unreplayed_or_unchanged_review_reference_cannot_be_superseded(self):
        self.set_superseding_amendment()
        self.snapshot["nodes"]["form.example"] = deepcopy(self.historical_node)
        self.assertEqual(self.report()["cases"][1]["status"], "supersession_effect_not_visible")
        self.snapshot["nodes"]["form.example"]["review_rationale"] = "An unrelated change"
        self.assertEqual(self.report()["cases"][1]["status"], "supersession_effect_not_visible")

    def test_invalid_supersession_links_fail_closed(self):
        self.set_superseding_amendment()
        for links in [[], "operator-alias", [42], ["unknown"], ["remaining-edge-review"],
                      ["operator-alias", "operator-alias"]]:
            self.queue["cases"][1]["superseded_by_case_ids"] = links
            with self.assertRaisesRegex(PipelineError, "Supersession requires"):
                self.report()

    def test_resolution_status_pins_all_meaning_variants_and_registry_effect(self):
        inv = self.snapshot["inventory"]
        inv["meanings"] = {"meaning.target": {"formulation_ids": ["form.v1", "form.v2"]}}
        inv["formulations"].update({"form.v1": {"version_sha256": "a" * 64},
                                    "form.v2": {"version_sha256": "b" * 64}})
        decision = {"missing_candidate_id": "missing.example", "target_meaning_id": "meaning.target",
                    "target_version_sha256": meaning_version(inv, "meaning.target")}
        self.packet = {"schema_version": 1, "id": "alias.proposal", "mode": "resolve",
                       "resolutions": [decision]}
        self.queue["cases"][0].update(mode="resolve", packet_sha256=digest(self.packet))
        self.snapshot["resolutions"] = [decision]
        self.snapshot["candidates"] = [{"id": "missing.example", "resolved_target_meaning_id": "meaning.target"}]
        self.write("inbox", self.packet)
        self.write("applied", {"id": "alias.proposal", "mode": "resolve", "sha256": digest(self.packet),
                               "status": "applied_in_independent_graph_only"})
        row = self.report()["cases"][0]
        self.assertEqual(row["status"], "applied_receipt_verified")
        self.assertTrue(all(row["current_resolution_effects"][0][key] for key in [
            "target_version_matches_current_meaning", "registry_target_matches", "resolution_ledger_matches"]))
        inv["formulations"]["form.v2"]["version_sha256"] = "c" * 64
        row = self.report()["cases"][0]
        self.assertEqual(row["status"], "applied_receipt_verified")  # historical receipt remains true
        self.assertFalse(row["current_resolution_effects"][0]["target_version_matches_current_meaning"])
        self.snapshot["candidates"] = []
        self.snapshot["resolutions"] = []
        effect = self.report()["cases"][0]["current_resolution_effects"][0]
        self.assertFalse(effect["registry_target_matches"])
        self.assertFalse(effect["resolution_ledger_matches"])

    def test_no_file_write(self):
        self.write("inbox", self.packet)
        files = [p for p in self.graph.rglob("*") if p.is_file()]
        before = {str(p): p.read_bytes() for p in files}
        self.report()
        self.assertEqual(before,
                         {str(p): p.read_bytes() for p in files})


if __name__ == "__main__":
    unittest.main()
