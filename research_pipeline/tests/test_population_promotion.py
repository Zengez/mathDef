"""Contract tests for explicit final promotion into an independent, unsealed corpus."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import PipelineError, Workspace, jsonl
from research_pipeline.engine.population import apply, digest, snapshot
from research_pipeline.adapters.mathdef.population_promotion import prepare, run


class PromotionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        Workspace(self.root).init({
            "schema_version": 1, "project": "Standalone promotion test",
            "term_kind": "concept", "content_kind": "definition",
            "adapter": "mathdef", "external_reference_mode": True,
            "independent_second_wave": True})
        (self.root / "state/wave2_formulation_reviews.jsonl").write_text("", encoding="utf-8")
        self.inbox = self.root / "population" / "inbox"
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.form = {"id": "form.promotion", "text": "Formal independent unit test formulation",
                     "review_state": "candidate", "evidence_ids": ["obs.promotion"]}
        self.meaning = {"id": "meaning.promotion", "display_term": "Unit test concept",
                        "context": "A clearly isolated unit test context",
                        "term_group_id": "group.promotion",
                        "term_ids": ["term.promotion"], "formulations": [self.form]}
        self.batch = {
            "schema_version": 1, "id": "b-promote",
            "sources": [{"id": "src.promotion", "title": "Source",
                         "url": "https://example.org/reference", "authority_reviewed": True,
                         "rights": "permitted", "access": "free"}],
            "terms": [{"id": "term.promotion", "label": "Unit test concept",
                       "source_id": "src.promotion", "locator": "https://example.org/reference"}],
            "observations": [{"id": "obs.promotion", "term_id": "term.promotion",
                              "source_id": "src.promotion", "locator": "https://example.org/reference",
                              "record_kind": "paraphrase", "text": "Source observed concept paraphrase"}],
            "meanings": [self.meaning],
            "reviews": [{"id": "review.promotion", "formulation_id": "form.promotion",
                         "status": "provisional", "reason": "Awaiting further review"}]
        }
        self.pkg_path = self.inbox / "b-promote.json"
        self.pkg_path.write_text(json.dumps(self.batch), encoding="utf-8")

    def complete_review(self):
        apply(self.root, self.pkg_path)
        old = snapshot(self.root)[0]["reviews"]["review.promotion"]
        new = dict(old, status="screened", reviewed_by="independent_mathematical_reviewer",
                   dependency_disposition="no_supported_target",
                   reason="Reviewed source and mathematical scope; no existing independently "
                          "supported definitional prerequisite is needed here.")
        correction = {"schema_version": 1, "id": "b-reconcile",
                      "revisions": [{"id": "revision.complete-review",
                                     "kind": "reviews", "target_id": "review.promotion",
                                     "expected_sha256": digest(old),
                                     "replacement": new,
                                     "reason": "Complete source-based review with explicit no-target rationale"}]}
        path = self.inbox / "b-reconcile.json"
        path.write_text(json.dumps(correction), encoding="utf-8")
        apply(self.root, path)

    def test_unresolved_provisional_cannot_promote(self):
        apply(self.root, self.pkg_path)
        with self.assertRaises(PipelineError):
            prepare(self.root)

    def test_preflight_and_explicit_approval(self):
        self.complete_review()
        report, new_rows, previous, new_reviews = prepare(self.root)
        self.assertEqual(report["incoming_counts"]["meanings"], 1)
        self.assertEqual(report["new_review_count"], 1)
        self.assertEqual(len(previous), 0)
        self.assertEqual(new_reviews[0]["decision"], "no_supported_target")
        approval = self.root / "population" / "approval.json"
        approval.write_text(json.dumps({
            "approved_for_independent_promotion": True,
            "draft_digest": report["draft_digest"],
            "preexisting_catalog_digest": report["preexisting_catalog_digest"],
            "preexisting_review_digest": report["preexisting_review_digest"],
            "reviewer": "independent_review_for_promotion",
            "rationale": "Manually reviewed isolated mathematical source, context and"
                         " disposition after completing the entire provisional ledger."
        }), encoding="utf-8")
        result = run(self.root, approval, apply=True)
        self.assertEqual(result["status"], "promoted_into_independent_unsealed_wave2")
        self.assertEqual(len(Workspace(self.root).records("meanings")), 1)
        self.assertTrue(Workspace(self.root).state("meanings")["sealed"] is False)
        self.assertEqual(jsonl(self.root / "state/wave2_formulation_reviews.jsonl")[0]["decision"],
                         "no_supported_target")

    def test_stale_approval_rejected_before_mutation(self):
        self.complete_review()
        approval = self.root / "population" / "approval.json"
        approval.write_text(json.dumps({
            "approved_for_independent_promotion": True,
            "draft_digest": "stale",
            "preexisting_catalog_digest": "stale",
            "preexisting_review_digest": "stale",
            "reviewer": "test", "rationale": "A lengthy false approval rationale must not pass."
        }), encoding="utf-8")
        with self.assertRaises(PipelineError):
            run(self.root, approval, apply=True)
        self.assertEqual(len(Workspace(self.root).records("meanings")), 0)


if __name__ == "__main__":
    unittest.main()
