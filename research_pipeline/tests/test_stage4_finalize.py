"""Regressions: Stage 4 must not promote locator-only evidence."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research_pipeline.engine.core import Workspace, PipelineError
from research_pipeline.engine.stage4_finalize import audit


class MeaningGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.w = Workspace(self.root / "isolated")
        self.w.init({"schema_version": 1, "project": "Test",
                     "term_kind": "terms", "content_kind": "definitions",
                     "adapter": "mathdef", "external_reference_mode": True})
        self.source = {"id": "src.stacks", "title": "Independent Stacks source",
                       "url": "https://stacks.math.columbia.edu/",
                       "rights": "locator_only", "access": "free",
                       "authority_reviewed": True}
        self.term = {"id": "term.x1", "label": "test",
                     "locator": "https://stacks.math.columbia.edu/tag/09GP",
                     "source_id": "src.stacks"}
        self.obs = {"id": "obs.independent.x1", "term_id": "term.x1",
                    "source_id": "src.stacks", "locator": self.term["locator"],
                    "record_kind": "paraphrase", "review_state": "candidate",
                    "confidence": "source_checked",
                    "text": "A field is algebraically closed if it admits no nontrivial algebraic field extension."}
        for stage, rows in (("sources", [self.source]), ("terms", [self.term]),
                            ("observations", [self.obs])):
            f = self.root / (stage + ".jsonl")
            f.write_text("".join(json.dumps(x) + "\n" for x in rows), encoding="utf-8")
            self.w.ingest(stage, f)
            self.w.seal(stage)
        self.meaning = {
            "id": "meaning.x1.test",
            "term_group_id": "group.x1",
            "display_term": "Algebraically closed field",
            "context": "Field theory: algebraic closure",
            "term_ids": ["term.x1"],
            "formulations": [
                {"id": "form.x1.a", "text": self.obs["text"],
                 "evidence_ids": [self.obs["id"]], "review_state": "screened",
                 "editorial_note": "Source checked, not verified by a human."},
                {"id": "form.x1.b", "text": "Every nonconstant polynomial over the field has a root in that field.",
                 "evidence_ids": [self.obs["id"]], "review_state": "screened",
                 "equivalence_note": "Equivalent root criterion."},
            ],
            "source_citation": {"source_id": "src.stacks",
                                "url": self.term["locator"], "section": "9.10"},
            "human_verified": False, "review_stage": "source_cross_checked",
        }

    def run_audit(self, **kwargs):
        with patch.multiple("research_pipeline.engine.stage4_finalize",
                            EXPECTED_TERMS=1,
                            EXPECTED_AUTHORED_OBSERVATIONS=1,
                            EXPECTED_SUPPORTED_TERMS=1,
                            EXPECTED_MEANINGS=1,
                            EXPECTED_FORMULATIONS=2):
            return audit(self.w.root, **kwargs)

    def add_meaning(self, row):
        f = self.root / "meaning.jsonl"
        f.write_text(json.dumps(row) + "\n", encoding="utf-8")
        self.w.ingest("meanings", f)

    def test_valid_meaning_and_two_equivalent_formulations(self):
        self.add_meaning(self.meaning)
        result = self.run_audit(seal=True)
        self.assertTrue(result["sealed"])
        self.assertEqual(result["screened_formulations"], 2)
        self.assertTrue((self.w.root / "state/stage4_review.json").exists())

    def test_locator_only_not_accepted_as_mathematical_evidence(self):
        original = self.meaning["formulations"][0]["evidence_ids"]
        self.meaning["formulations"][0]["evidence_ids"] = ["obs.locator.x1"]
        loc = {"id": "obs.locator.x1", "term_id": "term.x1",
               "source_id": "src.stacks", "locator": self.term["locator"],
               "record_kind": "locator"}
        # The pipeline's inherited Stage 3 registry cannot be revised in place;
        # construct the malicious condition on disk to test the gate itself.
        with (self.w.root / "records/observations.jsonl").open("a") as f:
            f.write(json.dumps(loc) + "\n")
        self.add_meaning(self.meaning)
        with self.assertRaisesRegex(PipelineError, "Locator-only evidence"):
            self.run_audit()
        self.meaning["formulations"][0]["evidence_ids"] = original


if __name__ == "__main__":
    unittest.main()
