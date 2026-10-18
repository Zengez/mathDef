import tempfile
import json
import unittest
from pathlib import Path

from research_pipeline.engine.core import Workspace
from research_pipeline.engine.stage3_locators import collect


class Stage3LocatorTests(unittest.TestCase):
    def test_sealed_term_index_produces_only_safe_locator_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            w = Workspace(root / "isolated")
            w.init({"schema_version": 1, "project": "Test",
                    "term_kind": "name", "content_kind": "definitions",
                    "adapter": "mathdef", "external_reference_mode": True})
            src = [
                {"id": "src.stacks", "title": "Stacks", "url": "https://stacks.math.columbia.edu/",
                 "authority_reviewed": True, "access": "free", "rights": "locator_only"},
                {"id": "src.planetmath", "title": "PlanetMath", "url": "https://www.planetmath.org/",
                 "authority_reviewed": True, "access": "free", "rights": "locator_only"},
            ]
            srcfile = root / "sources.jsonl"
            srcfile.write_text("".join(json.dumps(x)+"\n" for x in src))
            w.ingest("sources", srcfile)
            w.seal("sources")
            terms = [
                {"id": "term.stacks001", "label": "Algebraic closure",
                 "source_id": "src.stacks",
                 "locator": "https://stacks.math.columbia.edu/tag/09GP"},
                {"id": "term.planet001", "label": "basis",
                 "source_id": "src.planetmath",
                 "locator": "https://planetmath.org/basis"},
            ]
            tfile = root / "terms.jsonl"
            tfile.write_text("".join(json.dumps(x)+"\n" for x in terms))
            w.ingest("terms", tfile)
            w.seal("terms")
            output = root / "obs-in.jsonl"
            result = collect(w.root, output, ingest=True)
            self.assertEqual(result["added"], 2)
            rows = list(w.records("observations").values())
            self.assertEqual(len(rows), 2)
            self.assertTrue(all(row["record_kind"] == "locator" for row in rows))
            self.assertTrue(all("text" not in row for row in rows))\n            self.assertEqual({r["verification_state"] for r in rows},\n                             {"index_locator_only", "unverified_source_locator"})
            self.assertFalse(w.state("observations")["sealed"])
            again = collect(w.root, output, ingest=True)
            self.assertEqual(again["new_locator_candidates"], 0)


if __name__ == "__main__":
    unittest.main()
