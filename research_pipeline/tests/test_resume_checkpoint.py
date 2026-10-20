"""Portable checkpoint contract tests using a synthetic, non-mathematical repo."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.resume_checkpoint import ResumeError, run


class ResumeCheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "records").mkdir()
        (self.root / "config").mkdir()
        (self.root / "state").mkdir()
        self.records = self.root / "records" / "items.jsonl"
        self.records.write_text('{"id":"item.one","decision":"screened"}\n',
                                encoding="utf-8")
        (self.root / "config" / "plan.json").write_text(json.dumps({
            "schema_version": 1,
            "next_action": "Review a source-specific astronomy catalog entry",
            "work_budget_minutes_target": 12,
            "workflow_runs_to_check_live": [{"run_id": 42, "purpose": "CI"}],
        }), encoding="utf-8")
        self.config = self.root / "config" / "resume.json"
        self.spec = {
            "schema_version": 1,
            "project_id": "astronomy-source-catalog",
            "scope": "Generic non-mathematical research",
            "plan_path": "config/plan.json",
            "output_path": "state/RESUME_STATE.json",
            "records": {
                "items": {"path": "records/items.jsonl", "id_field": "id",
                          "decision_field": "decision"}
            },
        }
        self.config.write_text(json.dumps(self.spec), encoding="utf-8")

    def test_write_and_repeat_do_not_alter_source(self):
        before = self.records.read_bytes()
        state = run(self.config, self.root, write=True)
        checkpoint = self.root / "state" / "RESUME_STATE.json"
        self.assertEqual(state["record_evidence"]["items"]["rows"], 1)
        self.assertEqual(state["record_evidence"]["items"]["decisions"],
                         {"screened": 1})
        self.assertIn("astronomy", state["project_id"])
        self.assertEqual(state["workflow_runs_to_check_live"][0]["run_id"], 42)
        self.assertEqual(self.records.read_bytes(), before)
        prior = checkpoint.read_bytes()
        again = run(self.config, self.root, write=True)
        self.assertEqual(again["changed_record_sets_since_previous_checkpoint"], [])
        self.assertEqual(checkpoint.read_bytes(), prior)
        self.assertEqual(self.records.read_bytes(), before)

    def test_changes_detected_without_rewriting_source(self):
        run(self.config, self.root, write=True)
        self.records.write_text(
            '{"id":"item.one","decision":"screened"}\n'
            '{"id":"item.two","decision":"candidate"}\n',
            encoding="utf-8")
        later = run(self.config, self.root, write=False)
        self.assertEqual(later["changed_record_sets_since_previous_checkpoint"],
                         ["items"])
        self.assertEqual(later["record_evidence"]["items"]["rows"], 2)

    def test_saved_checkpoint_freshness_requires_exact_inputs(self):
        run(self.config, self.root, write=True)
        checkpoint = self.root / "state" / "RESUME_STATE.json"
        self.assertNotIn("observed_commit", json.loads(checkpoint.read_text()))
        self.assertTrue(run(self.config, self.root, verify=True)["checkpoint_is_current"])
        self.records.write_text('{"id":"item.changed","decision":"candidate"}\n',
                                encoding="utf-8")
        self.assertFalse(run(self.config, self.root)["checkpoint_is_current"])
        with self.assertRaises(ResumeError):
            run(self.config, self.root, verify=True)
        run(self.config, self.root, write=True)
        self.assertTrue(run(self.config, self.root, verify=True)["checkpoint_is_current"])

    def test_config_and_plan_changes_invalidate_saved_snapshot(self):
        run(self.config, self.root, write=True)
        self.spec["scope"] = "Changed astronomy scope"
        self.config.write_text(json.dumps(self.spec), encoding="utf-8")
        with self.assertRaises(ResumeError):
            run(self.config, self.root, verify=True)
        run(self.config, self.root, write=True)
        plan = self.root / "config" / "plan.json"
        data = json.loads(plan.read_text(encoding="utf-8"))
        data["next_action"] = "Investigate a different catalog source"
        plan.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(ResumeError):
            run(self.config, self.root, verify=True)

    def test_supporting_group_change_invalidates_snapshot(self):
        supporting = self.root / "records" / "observations.jsonl"
        supporting.write_text('{"id":"observation.one"}\n', encoding="utf-8")
        self.spec["supporting_groups"] = {
            "supplementary_sources": ["records/observations*.jsonl"]
        }
        self.config.write_text(json.dumps(self.spec), encoding="utf-8")
        initial = run(self.config, self.root, write=True)
        self.assertEqual(initial["supporting_input_evidence"]["supplementary_sources"]["files"], 1)
        supporting.write_text('{"id":"observation.two"}\n', encoding="utf-8")
        later = run(self.config, self.root)
        self.assertEqual(later["changed_supporting_groups_since_previous_checkpoint"],
                         ["supplementary_sources"])
        with self.assertRaises(ResumeError):
            run(self.config, self.root, verify=True)

    def test_unsafe_or_empty_supporting_groups_fail_closed(self):
        self.spec["supporting_groups"] = {"bad": ["../private/*.jsonl"]}
        self.config.write_text(json.dumps(self.spec), encoding="utf-8")
        with self.assertRaises(ResumeError):
            run(self.config, self.root)
        self.spec["supporting_groups"] = {"bad": ["records/no-match*.jsonl"]}
        self.config.write_text(json.dumps(self.spec), encoding="utf-8")
        with self.assertRaises(ResumeError):
            run(self.config, self.root)

    def test_duplicate_ids_fail_closed(self):
        self.records.write_text('{"id":"x"}\n{"id":"x"}\n', encoding="utf-8")
        with self.assertRaises(ResumeError):
            run(self.config, self.root)

    def test_escape_path_rejected(self):
        self.spec["records"]["items"]["path"] = "../private.jsonl"
        self.config.write_text(json.dumps(self.spec), encoding="utf-8")
        with self.assertRaises(ResumeError):
            run(self.config, self.root)

    def test_no_subject_adapter_required(self):
        state = run(self.config, self.root, write=False)
        self.assertEqual(state["domain_validation"], {})
        self.assertFalse((self.root / "state" / "RESUME_STATE.json").exists())

    def test_unapproved_plugin_rejected(self):
        self.spec["validation_adapter"] = "os"
        self.config.write_text(json.dumps(self.spec), encoding="utf-8")
        with self.assertRaises(ResumeError):
            run(self.config, self.root)

    def test_missing_record_file_fails_closed(self):
        self.records.unlink()
        with self.assertRaises(ResumeError):
            run(self.config, self.root)


if __name__ == "__main__":
    unittest.main()
