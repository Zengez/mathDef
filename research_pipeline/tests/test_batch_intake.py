import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research_pipeline.engine import core

from research_pipeline.engine.batch_intake import run
from research_pipeline.engine.core import Workspace, PipelineError, jsonl


class BatchTests(unittest.TestCase):
    def test_multi_page_resume_no_duplicate_and_stage3(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            w = Workspace(root / "experiment")
            w.init({"schema_version": 1, "project": "Toy", "term_kind": "name",
                    "content_kind": "definition", "adapter": "mathdef",
                    "external_reference_mode": True})
            source = {"id": "ref", "title": "Reference", "url": "https://example.org/index",
                      "authority_reviewed": True, "rights": "locator_only", "access": "free"}
            source_file = root / "source.jsonl"
            source_file.write_text(json.dumps(source) + "\n")
            w.ingest("sources", source_file)
            a = root / "a.html"
            b = root / "b.html"
            a.write_text('<h2 id="a">Closure</h2><p>Topological closure.</p>')
            b.write_text('<h2 id="b">Algebraic closure</h2><p>Field extension.</p>')
            manifest = root / "manifest.jsonl"
            lines = [
                {"id": "page.a", "source_id": "ref", "url": "https://example.org/index",
                 "profile": "headings", "html_path": str(a)},
                {"id": "page.b", "source_id": "ref", "url": "https://example.org/index",
                 "profile": "headings", "html_path": str(b)},
            ]
            manifest.write_text("".join(json.dumps(x) + "\n" for x in lines))
            out = root / "terms.jsonl"
            checkpoint = root / "terms.checkpoint.json"
            first = run(w.root, manifest, out, checkpoint, "terms", limit_pages=1)
            self.assertEqual(first["completed_pages"], 1)
            second = run(w.root, manifest, out, checkpoint, "terms")
            self.assertEqual(second["completed_pages"], 2)
            self.assertEqual(len(jsonl(out)), 2)
            again = run(w.root, manifest, out, checkpoint, "terms")
            self.assertEqual(again["new_candidate_records"], 0)
            w.ingest("terms", out)
            observations = root / "obs.jsonl"
            report = run(w.root, manifest, observations, root / "obs.checkpoint.json", "observations")
            self.assertEqual(report["records_in_output"], 2)
            self.assertTrue(all(x["record_kind"] == "locator" for x in jsonl(observations)))
            with self.assertRaisesRegex(PipelineError, "changed manifest"):
                manifest.write_text("".join(json.dumps(x) + "\n" for x in lines[:1]))
                run(w.root, manifest, out, checkpoint, "terms")


    def test_batch_reuses_registry_and_robots_but_rechecks_policy_on_resume(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            w = Workspace(root / "experiment")
            w.init({"schema_version": 1, "project": "Fixture", "term_kind": "item",
                    "content_kind": "description", "adapter": "fixture",
                    "external_reference_mode": True})
            source = {"id": "ref", "title": "Fixture", "url": "https://example.org/",
                      "authority_reviewed": True, "rights": "locator_only", "access": "free"}
            source_input = root / "source.jsonl"
            source_input.write_text(json.dumps(source) + "\n")
            w.ingest("sources", source_input)
            tasks = [{"id": f"page.{i}", "source_id": "ref",
                      "url": f"https://example.org/page{i}"} for i in range(3)]
            manifest = root / "manifest.jsonl"
            manifest.write_text("".join(json.dumps(x) + "\n" for x in tasks))
            out, checkpoint = root / "terms.jsonl", root / "checkpoint.json"
            caches = []
            def fetched(url, source, *, robots_cache):
                caches.append(robots_cache)
                return '<h2 id="item">Fixture item</h2>'
            with patch("research_pipeline.engine.batch_intake.fetch_index", side_effect=fetched), \
                    patch.object(core, "jsonl", wraps=core.jsonl) as reads:
                result = run(w.root, manifest, out, checkpoint, "terms",
                             network=True, limit_pages=2)
            self.assertEqual(result["records_in_output"], 2)
            self.assertEqual(len(caches), 2)
            self.assertIs(caches[0], caches[1])
            self.assertEqual(sum(Path(c.args[0]) == w.root / "records/sources.jsonl"
                                 for c in reads.call_args_list), 1)
            # A different invocation must reload changed source approval. The
            # first two pages remain checkpointed; the third is not admitted.
            source["authority_reviewed"] = False
            (w.root / "records/sources.jsonl").write_text(json.dumps(source) + "\n")
            with patch("research_pipeline.engine.batch_intake.fetch_index", side_effect=fetched):
                with self.assertRaisesRegex(PipelineError, "not eligible"):
                    run(w.root, manifest, out, checkpoint, "terms", network=True)
            self.assertIsNot(caches[0], caches[-1])
            self.assertEqual(len(jsonl(out)), 2)
            self.assertEqual(len(json.loads(checkpoint.read_text())["completed_ids"]), 2)

if __name__ == "__main__":
    unittest.main()
