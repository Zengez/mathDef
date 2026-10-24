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

if __name__ == "__main__":
    unittest.main()
