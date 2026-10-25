"""Mechanical and read-only preflight regression tests, no semantic automation."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import PipelineError, Workspace, digest
from research_pipeline.engine.dependency_graph import (
    graph_path, inventory_sync, live_nodes, missing_key, read, store,
)
from research_pipeline.engine.dependency_review_preflight import review_preflight


class DependencyReviewPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        Workspace(self.root).init({
            "schema_version": 1, "project": "Portable fixture", "term_kind": "term",
            "content_kind": "definition", "adapter": "mathdef",
            "external_reference_mode": True, "independent_second_wave": True,
        })
        records = self.root / "records"
        meanings = [
            {"id": "meaning.alpha", "display_term": "Alpha", "context": "Set theory",
             "formulations": [{"id": "form.alpha", "text": "Alpha references two concepts."}]},
            {"id": "meaning.beta", "display_term": "Beta", "context": "Set theory",
             "formulations": [{"id": "form.beta", "text": "Beta is primitive."}]},
        ]
        (records / "meanings.jsonl").write_text(
            "".join(json.dumps(x) + "\n" for x in meanings), encoding="utf-8")
        (records / "relations.jsonl").write_text("", encoding="utf-8")
        inventory_sync(self.root)
        self.graph = graph_path(self.root)
        self.inv = read(self.graph / "INVENTORY.json")
        store(self.root, [
            {"formulation_id": "form.alpha",
             "version_sha256": self.inv["formulations"]["form.alpha"]["version_sha256"],
             "complete": True,
             "review_rationale": "The entire illustrative mathematical statement was carefully scanned.",
             "references": [
                 {"phrase": "concept one", "state": "missing",
                  "context": "Illustrative unknown contextual concept"},
                 {"phrase": "concept two", "state": "missing",
                  "context": "Illustrative unknown contextual concept"},
             ]},
            {"formulation_id": "form.beta",
             "version_sha256": self.inv["formulations"]["form.beta"]["version_sha256"],
             "complete": True,
             "review_rationale": "Reviewed the complete primitive definition of Beta.",
             "references": []},
        ])
        self.inbox = self.graph / "inbox"
        self.inbox.mkdir(exist_ok=True)

    def write_batch(self, name, mode, items):
        data = {"schema_version": 1, "id": name, "mode": mode,
                "amendments" if mode == "amend" else "aliases": items}
        path = self.inbox / (name + ".json")
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def candidate(self, phrase):
        return missing_key(phrase, "Illustrative unknown contextual concept")

    def amendment(self):
        prior = live_nodes(self.graph, self.inv)["form.alpha"]
        refs = [{k: v for k, v in r.items()
                 if k not in ("occurrence_id", "missing_candidate_id")}
                for r in prior["references"]]
        refs[0]["state"] = "existing"
        refs[0].pop("context")
        refs[0]["target_meaning_id"] = "meaning.beta"
        return {
            "amendment_id": "amend.preflight-alpha",
            "formulation_id": "form.alpha",
            "version_sha256": self.inv["formulations"]["form.alpha"]["version_sha256"],
            "expected_node_sha256": digest(prior),
            "complete": True,
            "reviewed_by": "fixture-editor",
            "review_rationale": "Reconsidered every occurrence and justified one additional existing link.",
            "reason": "An editor has reviewed concept one in its actual source context and found a valid existing target.",
            "references": refs,
        }

    def test_valid_amendment_read_only_and_hash_staleness(self):
        event = self.amendment()
        path = self.write_batch("reviewed-amend", "amend", [event])
        before = {p.name: p.read_bytes()
                  for p in self.graph.iterdir() if p.is_file()}
        result = review_preflight(self.root, path)
        self.assertEqual(result["status"], "mechanically_valid_not_applied")
        self.assertEqual(result["checked_events"], 1)
        self.assertFalse(result["mathematical_certification"])
        self.assertEqual(len(result["new_candidate_preview"]), 1)
        self.assertEqual(before, {p.name: p.read_bytes()
                                  for p in self.graph.iterdir() if p.is_file()})
        event["expected_node_sha256"] = "0" * 64
        stale = self.write_batch("reviewed-amend", "amend", [event])
        with self.assertRaisesRegex(PipelineError, "Stale effective node hash"):
            review_preflight(self.root, stale)

    def test_alias_checks_existing_candidate_ids_and_invalid_chains(self):
        canonical = self.candidate("concept one")
        second = self.candidate("concept two")
        event = {
            "alias_id": "alias.preflight",
            "alias_candidate_id": second,
            "canonical_candidate_id": canonical,
            "reason": "Two different surface phrases have been manually established to represent the same contextual prerequisite in this illustrative case.",
            "reviewed_by": "fixture-editor",
        }
        path = self.write_batch("reviewed-alias", "alias", [event])
        before = {p.name: p.read_bytes()
                  for p in self.graph.iterdir() if p.is_file()}
        result = review_preflight(self.root, path)
        self.assertEqual(result["checked_events"], 1)
        self.assertEqual(result["new_candidate_preview"], [])
        self.assertEqual(before, {p.name: p.read_bytes()
                                  for p in self.graph.iterdir() if p.is_file()})
        invalid = dict(event, alias_id="alias.next", alias_candidate_id=canonical,
                       canonical_candidate_id=second)
        path = self.write_batch("reviewed-chain", "alias", [event, invalid])
        with self.assertRaises(PipelineError):
            review_preflight(self.root, path)

    def test_receipt_replay_and_bad_name(self):
        path = self.write_batch("reviewed-amend", "amend", [self.amendment()])
        data = json.loads(path.read_text(encoding="utf-8"))
        applied = self.graph / "applied"
        applied.mkdir(exist_ok=True)
        (applied / path.name).write_text(json.dumps({
            "id": "reviewed-amend", "sha256": digest(data), "mode": "amend",
            "status": "applied_in_independent_graph_only",
        }), encoding="utf-8")
        result = review_preflight(self.root, path)
        self.assertEqual(result["status"], "already_applied")
        different = self.write_batch("misnamed", "amend", [self.amendment()])
        wrong_path = different.with_name("different-name.json")
        wrong_path.write_bytes(different.read_bytes())
        with self.assertRaises(PipelineError):
            review_preflight(self.root, wrong_path)


    def test_partial_wrong_identity_and_nonobject_receipts_fail_closed(self):
        path = self.write_batch("receipt-fixture", "amend", [self.amendment()])
        data = json.loads(path.read_text())
        applied = self.graph / "applied"
        applied.mkdir(exist_ok=True)
        valid = {"id": "receipt-fixture", "mode": "amend", "sha256": digest(data),
                 "status": "applied_in_independent_graph_only"}
        invalid = [[], {k: v for k, v in valid.items() if k != "id"},
                   {**valid, "id": "another-packet"}, {**valid, "status": "pending"}]
        for receipt in invalid:
            (applied / path.name).write_text(json.dumps(receipt))
            with self.assertRaisesRegex(PipelineError, "immutable receipt"):
                review_preflight(self.root, path)
        (applied / path.name).write_text(json.dumps(valid))
        self.assertEqual(review_preflight(self.root, path)["status"], "already_applied")

if __name__ == "__main__":
    unittest.main()
