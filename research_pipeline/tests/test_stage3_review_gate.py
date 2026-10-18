"""Source access is not a completed mathematical definition review."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import PipelineError, Workspace, jsonl
from research_pipeline.engine.stage3_attempts import run
from research_pipeline.engine.stage3_review_gate import (
    build_review_queue, require_reviewed_term_dispositions)


class Stage3ReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.w = Workspace(self.root / "project")
        self.w.init({"schema_version": 1, "project": "Test",
                     "term_kind": "terms", "content_kind": "definitions",
                     "adapter": "mathdef", "external_reference_mode": True,
                     "require_full_definition_attempts": True,
                     "require_reviewed_term_dispositions": True})
        sources = [
            {"id": "src.stacks", "title": "Stacks",
             "url": "https://stacks.math.columbia.edu/",
             "authority_reviewed": True, "rights": "locator_only", "access": "free"},
            {"id": "src.planetmath", "title": "PlanetMath",
             "url": "https://www.planetmath.org/",
             "authority_reviewed": True, "rights": "permitted", "access": "free"},
        ]
        terms = [
            {"id": "term.a", "label": "Algebraic closure",
             "source_id": "src.stacks",
             "locator": "https://stacks.math.columbia.edu/tag/09GP"},
            {"id": "term.b", "label": "basis",
             "source_id": "src.planetmath",
             "locator": "https://planetmath.org/basis"},
        ]
        for stage, records in (("sources", sources), ("terms", terms)):
            p = self.root / (stage + ".jsonl")
            p.write_text("".join(json.dumps(r)+"\n" for r in records))
            self.w.ingest(stage, p)
            self.w.seal(stage)
        obs = {"id": "obs.form", "term_id": "term.a",
               "source_id": "src.stacks",
               "locator": "https://stacks.math.columbia.edu/tag/09GP",
               "record_kind": "paraphrase",
               "text": "An algebraic closure of a field is an algebraic extension that is itself algebraically closed."}
        path = self.root / "observations.jsonl"
        path.write_text(json.dumps(obs)+"\n")
        self.w.ingest("observations", path)
        self.ledger = self.w.root / "state/stage3_acquisition_attempts.jsonl"
        self.report = self.w.root / "state/stage3_acquisition_report.json"
        self.reviews = self.w.root / "state/stage3_term_reviews.jsonl"

        def fetch(url, source, *, delay, robots_cache):
            if source["id"] == "src.planetmath":
                raise PipelineError("Robots policy unavailable")
            return ('<title>Section 9.10 (09GP): Algebraic closure—The Stacks project</title>'
                    '<h2>9.10 Algebraic closure</h2>'
                    '<a href="/tag/09GG">Definition 9.10.1.</a>')
        run(self.w.root, self.ledger, self.report, batch_size=2, fetcher=fetch)

    def test_pending_review_does_not_allow_seal(self):
        result = build_review_queue(self.w.root, self.reviews)
        self.assertEqual(result["terms"], 2)
        self.assertEqual(result["accessible_needing_review"], 1)
        with self.assertRaisesRegex(PipelineError, "fetched terms still lack editorial review"):
            self.w.seal("observations")

    def test_reviewed_support_plus_blocked_source_can_seal(self):
        build_review_queue(self.w.root, self.reviews)
        rows = jsonl(self.reviews)
        by = {row["term_id"]: row for row in rows}
        row = by["term.a"]
        row["decision"] = "supported"
        row["reviewed_by"] = "source_reviewer"
        row["editorial_reason"] = "Inspected the cited Stacks section and independently wrote a candidate definition."
        row["evidence_ids"] = ["obs.form"]
        self.reviews.write_text("".join(json.dumps(x)+"\n" for x in rows))
        result = require_reviewed_term_dispositions(self.w.root, self.reviews)
        self.assertEqual(result["decisions"], {"supported":1, "access_blocked":1})
        self.assertTrue(self.w.seal("observations")["sealed"])

    def test_fabricated_evidence_does_not_pass(self):
        build_review_queue(self.w.root, self.reviews)
        rows = jsonl(self.reviews)
        row = next(x for x in rows if x["term_id"] == "term.a")
        row["decision"] = "supported"
        row["reviewed_by"] = "source_reviewer"
        row["editorial_reason"] = "This needs to be a real checked mathematical definition."
        row["evidence_ids"] = ["nonexistent"]
        self.reviews.write_text("".join(json.dumps(x)+"\n" for x in rows))
        with self.assertRaisesRegex(PipelineError, "lacks substantive term-matched evidence"):
            require_reviewed_term_dispositions(self.w.root, self.reviews)


if __name__ == "__main__":
    unittest.main()
