"""Stage 5 review coverage: no silent promotion of a subset to a completed graph."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import PipelineError, Workspace, canonical, digest, jsonl
from research_pipeline.engine.stage5_review_gate import prepare, apply_batch, apply_dispositions, audit, REVIEW_PATH


class Stage5ReviewGateTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.w = Workspace(self.root / "isolated")
        self.w.init({
            "schema_version": 1, "project": "Artificial trial",
            "term_kind": "term", "content_kind": "mathematical formulation",
            "adapter": "mathdef", "external_reference_mode": True,
        })
        self._push("sources", [{
            "id": "src.demo", "title": "Fixture", "url": "https://example.org/math",
            "rights": "locator_only", "access": "free", "authority_reviewed": True,
        }])
        self._push("terms", [
            {"id": "term.group", "label": "Group", "source_id": "src.demo",
             "locator": "https://example.org/math"},
            {"id": "term.topgroup", "label": "Topological group", "source_id": "src.demo",
             "locator": "https://example.org/math"},
        ])
        self._push("observations", [
            {"id": "obs.group", "term_id": "term.group", "source_id": "src.demo",
             "locator": "https://example.org/math", "record_kind": "paraphrase",
             "text": "A group with an associative binary operation."},
            {"id": "obs.topgroup", "term_id": "term.topgroup", "source_id": "src.demo",
             "locator": "https://example.org/math", "record_kind": "paraphrase",
             "text": "A topological group is a group with continuous operations."},
        ])
        self._push("meanings", [
            {"id": "meaning.group", "term_group_id": "group.group", "display_term": "Group",
             "context": "Groups", "term_ids": ["term.group"],
             "source_citation": {"url": "https://example.org/math"},
             "formulations": [{"id": "form.group", "text": "A group has an associative product.",
                               "review_state": "screened", "evidence_ids": ["obs.group"]}]},
            {"id": "meaning.topgroup", "term_group_id": "group.topgroup",
             "display_term": "Topological group", "context": "Topological groups",
             "term_ids": ["term.topgroup"],
             "source_citation": {"url": "https://example.org/math"},
             "formulations": [{"id": "form.topgroup", "text": "A topological group is a group with continuous operations.",
                               "review_state": "screened", "evidence_ids": ["obs.topgroup"]}]},
        ])
        self.batch = self.root / "batch.jsonl"
        self.edge = {
            "id": "rel.topgroup-to-group", "from_formulation": "form.topgroup",
            "target_meaning": "meaning.group", "relation_type": "definition_uses",
            "review_state": "screened", "source_phrase": "group",
            "source_locator": "https://example.org/math",
            "target_locator": "https://example.org/math",
            "editorial_reason": "The topological group definition explicitly requires the base group structure, which the target defines.",
            "reviewed_by": "editorial_source_comparison", "human_verified": False,
        }

    def _push(self, stage, rows):
        path = self.root / (stage + ".jsonl")
        path.write_text("".join(canonical(r) + "\n" for r in rows), encoding="utf-8")
        self.w.ingest(stage, path)
        self.w.seal(stage)

    def test_prepare_requires_coverage_and_does_not_overwrite(self):
        result = prepare(self.w.root)
        self.assertEqual((result["meaning_tasks"], result["formulation_reviews_prepared"]), (2, 2))
        self.assertEqual(len(jsonl(self.w.root / REVIEW_PATH)), 2)
        with self.assertRaisesRegex(PipelineError, "preserve"):
            prepare(self.w.root)
        with self.assertRaisesRegex(PipelineError, "cannot seal"):
            audit(self.w.root, require_complete=True)

    def test_screened_batch_does_not_inflate_coverage(self):
        prepare(self.w.root)
        self.batch.write_text(canonical(self.edge) + "\n", encoding="utf-8")
        result = apply_batch(self.w.root, self.batch)
        self.assertEqual(result["review"]["screened_relations"], 1)
        self.assertEqual(result["review"]["reviewed"], 1)
        self.assertEqual(result["review"]["needs_review"], 1)
        # Re-ingestion of an identical batch is idempotent.
        again = apply_batch(self.w.root, self.batch)
        self.assertEqual(again["ingestion"]["already_present"], 1)
        self.assertEqual(again["review"]["reviewed"], 1)
        # One specific independent no-link decision is required for the other form.
        reviews = jsonl(self.w.root / REVIEW_PATH)
        pending = next(x for x in reviews if x["formulation_id"] == "form.group")
        pending["decision"] = "no_supported_target"
        pending["reviewed_by"] = "assistant_source_comparison"
        pending["editorial_reason"] = ("Reviewed the fixture's reconstructed target inventory: the basic "
                                      "group axiom formulation does not depend on another available meaning.")
        (self.w.root / REVIEW_PATH).write_text(
            "".join(canonical(x) + "\n" for x in reviews), encoding="utf-8")
        self.assertTrue(audit(self.w.root, require_complete=True)["complete"])


    def test_no_link_needs_specific_source_review_and_current_digest(self):
        prepare(self.w.root)
        form_text = self.w.records("meanings")["meaning.group"]["formulations"][0]["text"]
        disposition = {
            "formulation_id": "form.group", "decision": "no_supported_target",
            "editorial_reason": ("Compared this basic group formulation with the other reconstructed "
                                 "group meanings and found no distinct available prerequisite target."),
            "reviewed_by": "assistant_mathematical_review", "human_verified": False,
            "source_text_digest": digest(form_text),
        }
        self.batch.write_text(canonical(disposition) + "\n", encoding="utf-8")
        result = apply_dispositions(self.w.root, self.batch)
        self.assertEqual(result["reviewed"], 1)
        self.assertEqual(result["needs_review"], 1)
        self.assertEqual(result["screened_relations"], 0)
        # A later identical replay is safe, while a fabricated stale review is not.
        self.assertEqual(apply_dispositions(self.w.root, self.batch)["reviewed"], 1)
        stale = dict(disposition, source_text_digest="0" * 64)
        self.batch.write_text(canonical(stale) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(PipelineError, "stale"):
            apply_dispositions(self.w.root, self.batch)


    def test_anchor_and_target_guard(self):
        prepare(self.w.root)
        bad = dict(self.edge, source_phrase="unmentioned phrase")
        self.batch.write_text(canonical(bad) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(PipelineError, "anchor"):
            apply_batch(self.w.root, self.batch)
        bad = dict(self.edge, target_meaning="meaning.topgroup")
        self.batch.write_text(canonical(bad) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(PipelineError, "Self-link"):
            apply_batch(self.w.root, self.batch)
        self.assertEqual(audit(self.w.root)["screened_relations"], 0)


if __name__ == "__main__":
    unittest.main()
