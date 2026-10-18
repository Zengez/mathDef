import json
import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
