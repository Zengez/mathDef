import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import Workspace, PipelineError, digest, jsonl
from research_pipeline.engine.revisions import apply_revision, recover_pending


class RevisionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.w = Workspace(root / "original")
        self.w.init({"schema_version": 1, "project": "Fixture", "term_kind": "label",
                     "content_kind": "definition", "adapter": "mathdef",
                     "external_reference_mode": True})
        self.data = root / "src.jsonl"
        stages = {
            "sources": [{"id": "ref", "title": "Reference", "url": "https://example.org/reference",
                         "rights": "locator_only", "access": "free", "authority_reviewed": True}],
            "terms": [{"id": "term.a", "label": "A", "source_id": "ref", "locator": "A"}],
            "observations": [{"id": "obs.a", "term_id": "term.a", "source_id": "ref",
                              "locator": "A", "record_kind": "locator"}],
            "meanings": [{"id": "meaning.a", "term_group_id": "a", "display_term": "A",
                          "context": "Context of A", "term_ids": ["term.a"],
                          "formulations": [{"id": "form.a", "text": "Initial content",
                                            "review_state": "screened", "evidence_ids": ["obs.a"]}]}],
            "relations": [{"id": "link.a", "from_formulation": "form.a",
                           "target_meaning": "meaning.a", "relation_type": "related",
                           "review_state": "screened"}],
        }
        for stage, rows in stages.items():
            self.data.write_text("".join(json.dumps(x) + "\n" for x in rows))
            self.w.ingest(stage, self.data)
            self.w.seal(stage)
        self.w.publish()
        self.second = Workspace(root / "second")
        self.w.fork_second_wave(self.second.root)

    def test_change_preserves_history_and_requires_rescreen(self):
        old = self.second.records("meanings")["meaning.a"]
        replacement = json.loads(json.dumps(old))
        replacement["formulations"][0]["text"] = "Better content"
        with self.assertRaisesRegex(PipelineError, "candidate review"):
            apply_revision(self.second.root, {
                "event_id": "edit.a", "stage": "meanings", "record_id": "meaning.a",
                "before_digest": digest(old), "editor": "authorized-maintainer",
                "reason": "Clarify context", "operation": "replace",
                "replacement": replacement})
        replacement["formulations"][0]["review_state"] = "candidate"
        event = {"event_id": "edit.a", "stage": "meanings", "record_id": "meaning.a",
                 "before_digest": digest(old), "editor": "authorized-maintainer",
                 "reason": "Clarify context", "operation": "replace",
                 "replacement": replacement}
        self.assertEqual(apply_revision(self.second.root, event)["status"], "applied")
        self.assertEqual(apply_revision(self.second.root, event)["status"], "already_applied")
        self.assertEqual(len(jsonl(self.second.root / "events/revisions.jsonl")), 1)
        self.assertEqual(self.w.records("meanings")["meaning.a"], old)
        self.assertEqual(recover_pending(self.second.root)["recovered"], 0)

    def test_stale_edit_fails(self):
        old = self.second.records("meanings")["meaning.a"]
        bad = {"event_id": "edit.b", "stage": "meanings", "record_id": "meaning.a",
               "before_digest": "0" * 64, "editor": "reviewer", "reason": "change",
               "operation": "replace", "replacement": old}
        with self.assertRaisesRegex(PipelineError, "Stale predecessor"):
            apply_revision(self.second.root, bad)

    def test_retirement_preserves_evidence(self):
        old = self.second.records("meanings")["meaning.a"]
        e = {"event_id": "retire.a", "stage": "meanings", "record_id": "meaning.a",
             "before_digest": digest(old), "editor": "reviewer", "reason": "Merged",
             "operation": "retire"}
        result = apply_revision(self.second.root, e)
        self.assertEqual(result["status"], "applied")
        # Frozen first-wave records are unchanged and the successor remains auditable.
        self.assertTrue(self.second.records("meanings")["meaning.a"]["_retired"])
        self.assertEqual(len(self.w.records("meanings")), 1)


if __name__ == "__main__":
    unittest.main()
