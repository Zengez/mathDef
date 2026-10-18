import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import Workspace, PipelineError
from research_pipeline.evaluation.compare import compare, original_mathdef


class CompareTests(unittest.TestCase):
    def test_baseline_only_read_after_both_waves_are_published(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            baseline = root / "old"
            (baseline / "definitions/topology").mkdir(parents=True)
            (baseline / "definitions/topology/closure.tex").write_text(
                "% id: topology.closure\n% term: Closure\n% source: https://example.org/a\n"
                "% related: topology.closure\n\nDefinition.\n")
            empty = root / "w1"
            w = Workspace(empty)
            w.init({"schema_version": 1, "project": "Toy", "term_kind": "name",
                    "content_kind": "text", "adapter": "mathdef",
                    "external_reference_mode": True})
            with self.assertRaisesRegex(PipelineError, "published"):
                compare(baseline, empty, root / "w2", root / "out.json")
            # This test only constructs frozen catalogs with valid manifests
            # via the same public path and does not depend on production files.
            data = {
                "sources": [{"id": "src", "title": "Source", "url": "https://example.org/a",
                             "authority_reviewed": True, "access": "free", "rights": "locator_only"}],
                "terms": [{"id": "term.closure", "label": "Closure",
                           "source_id": "src", "locator": "P/1"}],
                "observations": [{"id": "obs.closure", "term_id": "term.closure",
                                  "source_id": "src", "locator": "P/1", "record_kind": "locator"}],
                "meanings": [{"id": "meaning.closure", "term_group_id": "closure",
                              "display_term": "Closure", "context": "Topological closure",
                              "term_ids": ["term.closure"], "formulations": [{
                                  "id": "form.closure", "text": "Smallest closed superset",
                                  "review_state": "screened", "evidence_ids": ["obs.closure"]}]}],
                "relations": [{"id": "link.closure", "from_formulation": "form.closure",
                               "target_meaning": "meaning.closure", "relation_type": "related",
                               "review_state": "screened"}],
            }
            for stage, rows in data.items():
                file = root / "input.jsonl"
                file.write_text("".join(json.dumps(x) + "\n" for x in rows))
                w.ingest(stage, file)
                w.seal(stage)
            w.publish()
            next_workspace = root / "w2"
            w.fork_second_wave(next_workspace)
            w2 = Workspace(next_workspace)
            for stage in data:
                w2.seal(stage)
            w2.publish()
            report = compare(baseline, empty, next_workspace, root / "out.json")
            self.assertEqual(report["wave1"]["unique_name_match_candidates"], 1)
            self.assertEqual(report["wave2"]["links"]["confirmed_name_mapped_link_candidates"], 1)
            self.assertTrue(report["human_semantic_review_required"])
            self.assertTrue((root / "out.json").is_file())


if __name__ == "__main__":
    unittest.main()
