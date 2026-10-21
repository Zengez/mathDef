"""Tests for the topic-neutral research population ledger."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import Workspace, PipelineError
from research_pipeline.engine.population import apply, audit, digest, snapshot, canonical
from research_pipeline.engine.population_queue import plan


class PopulationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        Workspace(self.root).init({
            "schema_version": 1, "project": "Unit test",
            "term_kind": "item", "content_kind": "statement",
            "adapter": "test", "external_reference_mode": True})
        self.inbox = self.root / "population" / "inbox"
        self.inbox.mkdir(parents=True)
        self.form = {"id": "form.sample", "text": "A sample statement derived from observed material.",
                     "evidence_ids": ["obs.sample"], "review_state": "candidate"}
        self.meaning = {"id": "meaning.sample", "display_term": "Sample",
                        "term_group_id": "group.sample", "context": "Test context",
                        "term_ids": ["term.sample"], "formulations": [self.form]}
        self.package = {
            "schema_version": 1, "id": "batch-1",
            "sources": [{"id": "src.sample", "title": "Test text",
                         "url": "https://example.org/source",
                         "authority_reviewed": True, "rights": "permitted",
                         "access": "free"}],
            "terms": [{"id": "term.sample", "label": "Sample",
                       "source_id": "src.sample", "locator": "https://example.org/source"}],
            "observations": [{"id": "obs.sample", "term_id": "term.sample",
                              "source_id": "src.sample", "locator": "https://example.org/source",
                              "record_kind": "paraphrase", "text": "Observed example paraphrase"}],
            "meanings": [self.meaning],
            "relations": [{"id": "rel.sample", "from_formulation": "form.sample",
                           "target_query": "Not yet researched",
                           "relation_type": "definition_uses",
                           "editorial_reason": "A missing prerequisite is deliberately recorded",
                           "review_state": "candidate"}],
            "reviews": [{"id": "review.sample", "formulation_id": "form.sample",
                         "status": "provisional",
                         "reason": "Deferred consistency audit",
                         "formulation_sha256": digest({
                             "formulation": self.form, "context": "Test context"})}]}

    def write(self, pkg, name="batch-1.json"):
        p = self.inbox / name
        p.write_text(json.dumps(pkg), encoding="utf-8")
        return p

    def test_append_and_replay_and_unchanged_parent(self):
        path = self.write(self.package)
        self.assertTrue(apply(self.root, path, dry_run=True)["dry_run"])
        self.assertEqual(apply(self.root, path)["status"], "committed")
        self.assertEqual(apply(self.root, path)["status"], "unchanged")
        self.assertEqual(len(snapshot(self.root)[0]["meanings"]), 1)
        self.assertEqual(len(Workspace(self.root).records("meanings")), 0)
        issues = audit(self.root)["finding_summary"]
        self.assertEqual(issues["pending_review"], 1)
        self.assertEqual(issues["unresolved_target"], 1)
        self.assertEqual(issues["pending_link_review"], 1)
        with self.assertRaises(PipelineError):
            audit(self.root, certify=True)

    def test_auto_stamp_review_hash_in_immutable_draft(self):
        del self.package["reviews"][0]["formulation_sha256"]
        path = self.write(self.package)
        self.assertEqual(apply(self.root, path)["status"], "committed")
        records = snapshot(self.root)[0]
        review = records["reviews"]["review.sample"]
        self.assertEqual(review["formulation_sha256"],
                         digest({"formulation": self.form, "context": "Test context"}))

    def test_reject_overwriting_or_bad_evidence(self):
        self.package["observations"][0]["source_id"] = "src.unseen"
        with self.assertRaises(PipelineError):
            apply(self.root, self.write(self.package))
        self.assertFalse((self.root / "population" / "applied" / "batch-1.json").exists())

    def test_reject_screened_without_reason_and_author(self):
        self.package["reviews"][0]["status"] = "screened"
        with self.assertRaises(PipelineError):
            apply(self.root, self.write(self.package))

    def test_draft_revision_is_auditable_and_version_anchored(self):
        apply(self.root, self.write(self.package))
        old = snapshot(self.root)[0]["meanings"]["meaning.sample"]
        replacement = dict(old, context="Improved context")
        correction = {"schema_version": 1, "id": "batch-2",
                      "revisions": [{"id": "rev.sample", "kind": "meanings",
                                     "target_id": "meaning.sample",
                                     "expected_sha256": digest(old),
                                     "replacement": replacement,
                                     "reason": "Correct the scope of the draft meaning"}]}
        path = self.write(correction, name="batch-2.json")
        result = apply(self.root, path)
        self.assertEqual(result["status"], "committed")
        data, changes = snapshot(self.root)
        self.assertEqual(data["meanings"]["meaning.sample"]["context"], "Improved context")
        self.assertEqual(len(changes), 1)
        self.assertEqual(data["meanings"]["meaning.sample"]["formulations"][0]["id"], "form.sample")

    def test_revision_interruption_replay_and_conflicting_event_rejected(self):
        apply(self.root, self.write(self.package))
        old = snapshot(self.root)[0]["meanings"]["meaning.sample"]
        fixed = dict(old, context="More precise independently checked context")
        patch = {"schema_version": 1, "id": "revision-recovery",
                 "revisions": [{"id": "rev.recovery", "kind": "meanings",
                                "target_id": "meaning.sample",
                                "expected_sha256": digest(old),
                                "replacement": fixed,
                                "reason": "Reviewed isolated context correction"}]}
        path = self.write(patch, "revision-recovery.json")
        self.assertEqual(apply(self.root, path)["status"], "committed")
        (self.root / "population" / "applied" / "revision-recovery.json").unlink()
        # Simulate an interruption after the versioned event write but before
        # its package receipt. An exact replay must not duplicate that event.
        self.assertEqual(apply(self.root, path)["status"], "committed")
        self.assertEqual(len(snapshot(self.root)[1]), 1)
        (self.root / "population" / "applied" / "revision-recovery.json").unlink()
        tampered = dict(patch, revisions=[dict(patch["revisions"][0],
                       reason="Unexpected rewritten review rationale")])
        with self.assertRaises(PipelineError):
            apply(self.root, self.write(tampered, "revision-recovery.json"))

    def test_partial_interruption_replays_exact_prior_rows(self):
        path = self.write(self.package)
        partial = self.root / "population" / "records" / "sources.jsonl"
        partial.parent.mkdir(parents=True, exist_ok=True)
        partial.write_text(canonical(self.package["sources"][0]) + "\n", encoding="utf-8")
        result = apply(self.root, path)
        self.assertEqual(result["status"], "committed")
        self.assertEqual(len(snapshot(self.root)[0]["sources"]), 1)
        self.assertTrue((self.root / "population" / "STATUS.json").is_file())

    def test_queue_clusters_missing_targets(self):
        apply(self.root, self.write(self.package))
        cfg = self.root / "topics.json"
        cfg.write_text(json.dumps({"schema_version": 1,
            "breadth_topics": [{"id": "topic-a", "research_prompt": "Research a new branch"}],
            "prerequisite_lookahead_limit": 1}), encoding="utf-8")
        result = plan(self.root, cfg)
        self.assertEqual(result["deferred_target_clusters"][0]["number_of_affected_relations"], 1)
        self.assertEqual(result["suggested_next_package"]["maximum_deferred_target_inclusions"], 1)

    def test_source_rights_gate(self):
        self.package["sources"][0]["rights"] = "disallowed"
        with self.assertRaises(PipelineError):
            apply(self.root, self.write(self.package))


if __name__ == "__main__":
    unittest.main()
