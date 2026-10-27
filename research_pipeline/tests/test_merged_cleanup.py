"""Stage-only cleanup regressions: no global relinking or publish side effect."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import tempfile
import unittest

from research_pipeline.adapters.mathdef.merged_cleanup import (
    CleanupError, prepare_curated_cleanup, compile_source_registry,
)
from research_pipeline.ui.renderer import to_index


class MergedCleanupTests(unittest.TestCase):
    def setUp(self):
        self.base = {
            "groups": [{
                "id": "g", "title": "Artinian ring", "aliases": [],
                "meanings": [
                    {
                        "id": "old", "label": "Original mathDef · Commutative Algebra",
                        "source_origin": "original_mathdef",
                        "original_definition_id": "commalg.artinian-ring",
                        "formulations": [{
                            "id": "f.old",
                            "text": "Every descending chain of ideals stabilizes.",
                            "sources": [
                                {"title": "Stacks", "url": "https://stacks.math.columbia.edu/tag/00J4",
                                 "verification_status": "original_mathdef_editorial"},
                                {"title": "Original source file",
                                 "url": "https://github.com/Zengez/mathDef/blob/main/definitions/commalg/artinian-ring.tex",
                                 "role": "Definition provenance"}],
                        }],
                    },
                    {
                        "id": "new", "label": "Commutative algebra",
                        "formulations": [{
                            "id": "f.new",
                            "text": "A commutative ring R is Artinian if the descending chain condition holds.",
                            "sources": [
                                {"title": "Stacks", "url": "https://stacks.math.columbia.edu/tag/00J4",
                                 "role": "Supporting evidence (screened draft)",
                                 "source_id": "src.stacks"}],
                        }],
                    }
                ],
            }, {
                "id": "g.other", "title": "Noetherian ring", "aliases": [],
                "meanings": [{
                    "id": "other", "label": "Commutative algebra",
                    "formulations": [{"id": "f.other", "text": "Noetherian ring.",
                                      "sources": [{"url": "https://example.com/noetherian",
                                                   "title": "Reference"}]}],
                }],
            }],
            "relations": [
                {"id": "r.related", "from_formulation": "f.old",
                 "target_meaning": "other", "relation_type": "related",
                 "review_state": "screened"},
                {"id": "r.use_old_text", "from_formulation": "f.old",
                 "target_meaning": "other", "relation_type": "definition_uses",
                 "review_state": "screened", "span_start": 6, "span_end": 16,
                 "source_phrase": "descending"},
                {"id": "r.incoming", "from_formulation": "f.other",
                 "target_meaning": "old", "relation_type": "related",
                 "review_state": "screened"},
            ]
        }

    def _repo(self, location: Path) -> Path:
        data = location / "data"
        data.mkdir()
        for filename, names in (
            ("math_subjects.json", ["Commutative Algebra"]),
            ("math_contexts.json", ["Commutative rings"]),
        ):
            (data / filename).write_text(json.dumps({
                "schema_version": 1, "entries": [{"name": s} for s in names]
            }), encoding="utf-8")
        (data / "merged_cleanup_retained_variants.json").write_text(json.dumps({"schema_version": 1, "entries": []}), encoding="utf-8")
        (data / "math_subject_assignments.json").write_text(json.dumps({"schema_version": 1, "assignments": []}), encoding="utf-8")
        (data / "math_subject_routing.json").write_text(json.dumps({
            "schema_version": 1,
            "original_area_to_subject": {},
            "research_context_prefix_to_subject": {}
        }), encoding="utf-8")
        (data / "math_definition_conventions.json").write_text(json.dumps({
            "schema_version": 1, "entries": []
        }), encoding="utf-8")
        (data / "math_source_convention_assessments.json").write_text(json.dumps({
            "schema_version": 1, "assessments": []
        }), encoding="utf-8")
        (data / "merged_cleanup_decisions.json").write_text(json.dumps({
            "schema_version": 1,
            "merge_meanings": [{
                "case_id": "artinian",
                "removed_meaning_id": "old",
                "kept_meaning_id": "new",
                "kept_formulation_id": "f.new",
            }],
            "metadata_assignments": {
                "new": {"subject": "Commutative Algebra",
                        "context": "Commutative rings"}
            },
        }), encoding="utf-8")
        return location

    def test_source_evidence_provenance_aliases_and_no_fabricated_links(self):
        original = deepcopy(self.base)
        with tempfile.TemporaryDirectory() as tmp:
            cleaned, report, sources = prepare_curated_cleanup(
                self.base, self._repo(Path(tmp)))
        self.assertEqual(self.base, original, "Historical input must not change")
        self.assertEqual(report["removed_duplicate_meanings"], 1)
        self.assertEqual(report["removed_duplicate_formulations"], 1)
        self.assertEqual(report["subject_coverage"], 1)
        self.assertEqual(report["subject_missing"], 1)
        self.assertFalse(report["is_publication_ready"])
        self.assertEqual(report["deleted_source_text_edges_needing_global_relink"],
                         ["r.use_old_text"])
        self.assertEqual(cleaned["consolidated_ids"]["meaning_aliases"], {"old": "new"})
        self.assertEqual(cleaned["consolidated_ids"]["formulation_aliases"], {"f.old": "f.new"})
        self.assertEqual(len(cleaned["groups"][0]["meanings"]), 1)
        self.assertEqual(len(cleaned["relations"]), 2)
        related = next(r for r in cleaned["relations"] if r["id"] == "r.related")
        self.assertEqual(related["from_formulation"], "f.new")
        incoming = next(r for r in cleaned["relations"] if r["id"] == "r.incoming")
        self.assertEqual(incoming["target_meaning"], "new")
        surviving = cleaned["groups"][0]["meanings"][0]
        self.assertEqual(surviving["legacy_original_definition_ids"],
                         ["commalg.artinian-ring"])
        self.assertEqual(surviving["subject"], "Commutative Algebra")
        self.assertEqual(surviving["context"], "Commutative rings")
        citations = surviving["formulations"][0]["sources"]
        self.assertEqual(len(citations), 2, "Same URL is not two sources")
        self.assertEqual(len(sources["groups"][0]["source_ids"]), 2)
        artinian_sources = [s for s in sources["sources"].values()
                           if "00J4" in s["url"]]
        self.assertEqual(len(artinian_sources), 1)
        self.assertTrue(artinian_sources[0]["visible_in_future_sources_ui"])
        archival = [s for s in sources["sources"].values() if "github.com/Zengez" in s["url"]]
        self.assertEqual(len(archival), 1)
        self.assertFalse(archival[0]["visible_in_future_sources_ui"])
        self.assertEqual(sources["correction_event_history"], "not_tracked")
        self.assertEqual(len(to_index(cleaned)), 2)

    def test_strict_required_subject_gate_and_bad_primary(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._repo(Path(tmp))
            with self.assertRaisesRegex(CleanupError, "without curated mathematical subject"):
                prepare_curated_cleanup(self.base, repo, require_full_metadata=True)
            filename = repo / "data/merged_cleanup_decisions.json"
            entry = json.loads(filename.read_text())
            entry["merge_meanings"][0]["kept_formulation_id"] = "f.does.not.exist"
            filename.write_text(json.dumps(entry))
            with self.assertRaisesRegex(CleanupError, "Invalid kept formulation"):
                prepare_curated_cleanup(self.base, repo)

    def test_source_ids_distinguish_meaningful_fragments(self):
        catalog = deepcopy(self.base)
        form = catalog["groups"][0]["meanings"][0]["formulations"][0]
        form["sources"].append({"title": "Other Stacks tag",
                                "url": "https://stacks.math.columbia.edu/tag/00AB"})
        sources = compile_source_registry(catalog)
        urls = [s["url"] for s in sources["sources"].values()]
        self.assertIn("https://stacks.math.columbia.edu/tag/00J4", urls)
        self.assertIn("https://stacks.math.columbia.edu/tag/00AB", urls)
        self.assertEqual(len([u for u in urls if "stacks.math.columbia.edu" in u]), 2)


if __name__ == "__main__":
    unittest.main()
