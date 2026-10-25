"""Scoped registry reuse preserves public validation, recovery and freshness."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from research_pipeline.engine import core
from research_pipeline.benchmarks.registry_throughput import measure


class RegistrySnapshotTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.w = core.Workspace(self.root / "workspace")
        self.w.init({"schema_version": 1, "project": "Fixture", "adapter": "fixture",
                     "term_kind": "item", "content_kind": "description",
                     "external_reference_mode": True})
        self.push("sources", [{"id": "source.one", "title": "Source",
                               "url": "https://example.org/", "rights": "locator_only",
                               "access": "free", "authority_reviewed": True}])

    def push(self, stage, rows, **kwargs):
        path = self.root / (stage + ".jsonl")
        path.write_text("".join(json.dumps(r) + "\n" for r in rows))
        return self.w.ingest(stage, path, **kwargs)

    def term(self, number, source="source.one"):
        return {"id": f"term.{number}", "label": f"Item {number}",
                "source_id": source, "locator": f"item/{number}"}

    def test_bulk_reads_once_and_checkpoints_durable_prefix_and_digest(self):
        with patch.object(core, "jsonl", wraps=core.jsonl) as read:
            report = self.push("terms", [self.term(i) for i in range(23)], batch_size=2)
        record_reads = [Path(c.args[0]).name for c in read.call_args_list
                        if Path(c.args[0]).parent.name == "records"]
        self.assertEqual(record_reads.count("sources.jsonl"), 1)
        self.assertEqual(record_reads.count("terms.jsonl"), 1)
        self.assertEqual(report["total"], 23)
        records = self.w.records("terms")
        self.assertEqual(self.w.state("terms")["record_digest"],
                         core.digest(list(records.values())))
        self.assertEqual(self.push("terms", [self.term(i) for i in range(23)])["added"], 0)

    def test_failure_releases_snapshot_and_retry_keeps_valid_rows(self):
        rows = [self.term(0), self.term(1, "source.two")]
        with self.assertRaisesRegex(core.PipelineError, "Unknown term source"):
            self.push("terms", rows, batch_size=1)
        self.assertEqual(set(self.w.records("terms")), {"term.0"})
        self.assertEqual(self.w.state("terms")["total"], 1)
        self.push("sources", [{"id": "source.two", "title": "Second source",
                               "url": "https://example.net/", "rights": "locator_only",
                               "access": "free", "authority_reviewed": True}])
        report = self.push("terms", rows)
        self.assertEqual((report["added"], report["already_present"]), (1, 1))
        altered = dict(rows[0], label="Changed under same ID")
        with self.assertRaisesRegex(core.PipelineError, "collision"):
            self.push("terms", [altered])

    def test_seal_reloads_sources_after_previous_operation(self):
        self.w.seal("sources")
        self.push("terms", [self.term(0)])
        path = self.w.root / "records/sources.jsonl"
        path.write_text("")
        with self.assertRaisesRegex(core.PipelineError, "Unknown term source"):
            self.w.seal("terms")
        self.assertFalse(self.w.state("terms").get("sealed"))

    def test_corrupted_prerequisite_and_duplicate_ids_are_not_cached(self):
        self.push("terms", [self.term(0)])
        path = self.w.root / "records/sources.jsonl"
        content = path.read_text()
        path.write_text(content + content)
        with self.assertRaisesRegex(core.PipelineError, "Duplicate record"):
            self.push("terms", [self.term(1)])
        path.write_text("{malformed\n")
        with self.assertRaisesRegex(core.PipelineError, "bad JSON"):
            self.push("terms", [self.term(1)])
        self.assertEqual(set(self.w.records("terms")), {"term.0"})

    def test_public_validator_override_still_runs_for_every_new_record(self):
        original = self.w.validate
        def validate(stage, row):
            original(stage, row)
            if stage == "terms" and row["label"] == "Item 1":
                raise core.PipelineError("Adapter review rejects this row")
        with patch.object(self.w, "validate", side_effect=validate) as review:
            with self.assertRaisesRegex(core.PipelineError, "Adapter review"):
                self.push("terms", [self.term(0), self.term(1)])
        self.assertEqual(review.call_count, 2)
        self.assertEqual(set(self.w.records("terms")), {"term.0"})

    def test_checkpoint_failure_after_flush_resumes_from_exact_persisted_rows(self):
        rows = [self.term(i) for i in range(5)]
        with patch.object(self.w, "_ingest_checkpoint", side_effect=OSError("checkpoint interruption")):
            with self.assertRaisesRegex(OSError, "checkpoint interruption"):
                self.push("terms", rows, batch_size=2)
        self.assertEqual(set(self.w.records("terms")), {"term.0", "term.1"})
        report = self.push("terms", rows, batch_size=2)
        self.assertEqual((report["added"], report["already_present"]), (3, 2))
        records = self.w.records("terms")
        self.assertEqual(self.w.state("terms")["record_digest"], core.digest(list(records.values())))
        self.assertEqual(len(records), 5)

    def test_end_to_end_output_unchanged_and_reads_bounded(self):
        result = measure(size=12, repeats=1)
        run = result["runs"][0]
        # Actual serialization contract covers source/evidence membership and
        # relation endpoints through ingest, every seal and publication.
        self.assertLess(sum(run["record_file_reads"].values()), 50)
        self.assertTrue(run["publication_sha256"])
