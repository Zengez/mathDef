"""Regression checks for explicitly reviewed reuse of known missing candidates."""
import unittest
from research_pipeline.engine.core import PipelineError
from research_pipeline.engine.dependency_graph import make_snapshot, missing_key

class ReviewedCandidateReuseTests(unittest.TestCase):
    def setUp(self):
        self.fid = "form.review"
        self.inv = {"formulations": {
            self.fid: {"version_sha256": "fixture-version",
                       "context": "General topology",
                       "text": "A source referring to a closed subset."}},
            "meanings": {}}
        self.candidate = missing_key(
            "closed subset of a topological space",
            "Topology: subset with open complement")
        self.ref = {
            "phrase": "closed subset in the fixed space",
            "state": "missing",
            "context": "Topology: same closedness predicate",
            "reviewed_existing_candidate_id": self.candidate,
            "candidate_identity_review_rationale":
                "Both expressions assert that a subset of the same "
                "topological space has open complement; no additional "
                "separation, scheme or closed-map hypotheses are imposed.",
        }

    def snapshot(self, ref, known=None):
        return make_snapshot(
            self.inv, self.fid, [ref], "complete",
            "Reviewed the complete source definition and all prerequisites.",
            reusable_missing_candidate_ids=known)

    def test_explicit_reuse_preserves_context_without_new_identity(self):
        node = self.snapshot(self.ref, {self.candidate})
        actual = node["references"][0]
        self.assertEqual(actual["missing_candidate_id"], self.candidate)
        self.assertEqual(actual["phrase"], self.ref["phrase"])
        self.assertEqual(actual["context"], self.ref["context"])
        self.assertEqual(actual["candidate_identity_review_rationale"],
                         self.ref["candidate_identity_review_rationale"])

    def test_unreviewed_mode_remains_phrase_context_based(self):
        row = {k: v for k, v in self.ref.items()
               if k not in ("reviewed_existing_candidate_id",
                            "candidate_identity_review_rationale")}
        node = self.snapshot(row)
        self.assertEqual(node["references"][0]["missing_candidate_id"],
                         missing_key(row["phrase"], row["context"]))
        self.assertNotEqual(node["references"][0]["missing_candidate_id"],
                            self.candidate)

    def test_missing_registry_or_short_identity_rationale_rejected(self):
        with self.assertRaises(PipelineError):
            self.snapshot(self.ref)
        with self.assertRaises(PipelineError):
            self.snapshot(self.ref, {"missing.some-other-id"})
        with self.assertRaises(PipelineError):
            self.snapshot({**self.ref, "candidate_identity_review_rationale": "same"},
                          {self.candidate})


    def test_full_amendment_reuses_registered_candidate_and_preflight_agrees(self):
        import json
        import tempfile
        from pathlib import Path
        from research_pipeline.engine.core import Workspace, digest
        from research_pipeline.engine.dependency_graph import (
            amend, graph_path, inventory_sync, live_nodes, read, store)
        from research_pipeline.engine.dependency_review_preflight import review_preflight
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            Workspace(root).init({
                "schema_version": 1, "project": "Regression fixture",
                "term_kind": "term", "content_kind": "definition",
                "adapter": "mathdef", "external_reference_mode": True,
                "independent_second_wave": True,
            })
            rec = root / "records"
            rec.mkdir(exist_ok=True)
            meanings = [
                {"id": "meaning.alpha", "display_term": "Alpha",
                 "context": "Topology", "formulations": [
                     {"id": "form.alpha", "text": "A closed subset is used."}]},
                {"id": "meaning.beta", "display_term": "Beta",
                 "context": "Topology", "formulations": [
                     {"id": "form.beta", "text": "Closed subsets are required."}]},
            ]
            (rec / "meanings.jsonl").write_text(
                "".join(json.dumps(m) + "\n" for m in meanings))
            (rec / "relations.jsonl").write_text("")
            inventory_sync(root)
            graph = graph_path(root)
            inv = read(graph / "INVENTORY.json")
            context = "Topology: closed subset in a fixed ambient space"
            canonical = missing_key("closed subset of topological space", context)
            def scan(fid, refs):
                return {"formulation_id": fid,
                        "version_sha256": inv["formulations"][fid]["version_sha256"],
                        "references": refs, "complete": True,
                        "review_rationale":
                            "Reviewed the full mathematical statement and all its references."}
            store(root, [
                scan("form.alpha", [{"phrase": "closed subset of topological space",
                                     "state": "missing", "context": context}]),
                scan("form.beta", []),
            ])
            prior = live_nodes(graph, inv)["form.beta"]
            ref = dict(self.ref, reviewed_existing_candidate_id=canonical)
            event = {**scan("form.beta", [ref]),
                     "amendment_id": "amend.fixture-reuse",
                     "expected_node_sha256": digest(prior),
                     "reviewed_by": "source-context-reviewer",
                     "reason": "Compared both source definitions and verified "
                               "their closed-subset prerequisites have the same typing."}
            offline = graph / "review-fixture.json"
            offline.write_text(json.dumps({
                "schema_version": 1, "id": "review-fixture",
                "mode": "amend", "amendments": [event]}))
            preview = review_preflight(root, offline)
            self.assertTrue(preview["new_candidate_preview"][0]["explicit_reviewed_reuse"])
            self.assertFalse(preview["new_candidate_preview"][0]["new_candidate_identity"])
            outcome = amend(root, [event])
            self.assertEqual(outcome["missing_candidates"], 1)
            self.assertEqual(outcome["unresolved_missing_candidates"], 1)
            actual = live_nodes(graph, inv)["form.beta"]["references"][0]
            self.assertEqual(actual["missing_candidate_id"], canonical)

if __name__ == "__main__":
    unittest.main()
