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
        (data / "merged_cleanup_cross_heading_review.json").write_text(json.dumps({"schema_version": 1, "clear_duplicate_pending_group_migration": []}), encoding="utf-8")
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

    def test_transitive_semantic_and_form_redirects_preserve_original_sources(self):
        data = deepcopy(self.base)
        data["groups"][0]["meanings"].append({
            "id": "final", "label": "Preferred canonical definition",
            "formulations": [{"id": "f.final",
                "text": "A well-supported canonical condition with the same mathematics.",
                "sources": [{"title": "Third source",
                             "url": "https://example.org/third-proof"}]}],
        })
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._repo(Path(tmp))
            file = repo / "data/merged_cleanup_decisions.json"
            decisions = json.loads(file.read_text(encoding="utf-8"))
            decisions["merge_meanings"].append({
                "case_id": "second-stage-consolidation",
                "removed_meaning_id": "new",
                "kept_meaning_id": "final",
                "kept_formulation_id": "f.final",
            })
            decisions["metadata_assignments"] = {
                "final": {"subject": "Commutative Algebra",
                          "context": "Commutative rings"}
            }
            file.write_text(json.dumps(decisions), encoding="utf-8")
            cleaned, report, source_registry = prepare_curated_cleanup(data, repo)

        self.assertEqual(report["removed_duplicate_meanings"], 2)
        aliases = cleaned["consolidated_ids"]
        self.assertEqual(aliases["meaning_aliases"]["old"], "final")
        self.assertEqual(aliases["meaning_aliases"]["new"], "final")
        self.assertEqual(aliases["formulation_aliases"]["f.old"], "f.final")
        self.assertEqual(aliases["formulation_aliases"]["f.new"], "f.final")
        final = next(m for g in cleaned["groups"] for m in g["meanings"]
                     if m["id"] == "final")
        self.assertEqual(final["legacy_original_definition_ids"],
                         ["commalg.artinian-ring"])
        self.assertEqual(set(final["consolidated_from_meanings"]), {"old", "new"})
        self.assertEqual({s["url"] for s in final["formulations"][0]["sources"]}, {
            "https://example.org/third-proof",
            "https://stacks.math.columbia.edu/tag/00J4",
            "https://github.com/Zengez/mathDef/blob/main/definitions/commalg/artinian-ring.tex",
        })
        self.assertEqual(next(r for r in cleaned["relations"]
                              if r["id"] == "r.incoming")["target_meaning"], "final")
        self.assertEqual({m["id"] for g in cleaned["groups"] for m in g["meanings"]},
                         {"final", "other"})

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

    def test_cross_heading_alias_migration_is_source_preserving(self):
        data = deepcopy(self.base)
        data["groups"].append({
            "id": "g.alias", "title": "Artinian commutative ring",
            "aliases": ["ring satisfying descending-chain condition"],
            "meanings": [{"id": "m.alias", "label": "Commutative Algebra",
                          "formulations": [{
                            "id": "f.alias",
                            "text": "A commutative ring R is Artinian when descending ideal chains stabilize.",
                            "sources": [{
                                "title": "Secondary source",
                                "url": "https://example.org/another-artinian"
                            }]
                          }]}]
        })
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._repo(Path(tmp))
            (repo / "data/merged_cleanup_cross_heading_review.json").write_text(
                json.dumps({
                    "schema_version": 1,
                    "clear_duplicate_pending_group_migration": [{
                        "case_id": "alternate-artinian-heading",
                        "removed_group_id": "g.alias",
                        "retained_group_id": "g",
                        "removed_meaning_id": "m.alias",
                        "retained_meaning_id": "new",
                        "removed_title": "Artinian commutative ring",
                        "retained_title": "Artinian ring",
                        "reason": "Same descending chain condition"
                    }]
                }), encoding="utf-8"
            )
            cleaned, report, refs = prepare_curated_cleanup(data, repo)
        self.assertEqual(report["starting_groups"], 3)
        self.assertEqual(report["surviving_groups"], 2)
        self.assertEqual(report["removed_duplicate_meanings"], 2)
        self.assertEqual(report["retired_searchable_heading_aliases"], 1)
        self.assertEqual(cleaned["consolidated_ids"]["group_aliases"],
                         {"g.alias": "g"})
        self.assertEqual(cleaned["consolidated_ids"]["meaning_aliases"]["m.alias"],
                         "new")
        target = next(g for g in cleaned["groups"] if g["id"] == "g")
        self.assertIn("Artinian commutative ring", target["aliases"])
        self.assertIn("ring satisfying descending-chain condition", target["aliases"])
        sources = target["meanings"][0]["formulations"][0]["sources"]
        self.assertTrue(any(s.get("url") == "https://example.org/another-artinian"
                            for s in sources))
        self.assertEqual(len(refs["groups"]), 2)
        self.assertEqual(len(to_index(cleaned)), 2)

    def test_group_only_alias_preserves_meanings_and_distinct_sources(self):
        data = deepcopy(self.base)
        data["groups"].append({
            "id": "g.variant", "title": "Artinian commutative rings",
            "aliases": ["commutative artinian ring"],
            "meanings": [{"id": "m.variant", "label": "Commutative ring context",
                          "formulations": [{"id": "f.variant",
                              "text": "A specialized mathematical formulation with more explicit hypotheses.",
                              "sources": [{"url": "https://example.org/specialized",
                                           "title": "Separate primary work"}]}]}]
        })
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._repo(Path(tmp))
            (repo / "data/merged_cleanup_cross_heading_review.json").write_text(
                json.dumps({
                    "schema_version": 1, "clear_duplicate_pending_group_migration": [],
                    "group_only_alias_merges": [{
                        "case_id": "artinian-context-group",
                        "removed_group_id": "g.variant",
                        "retained_group_id": "g",
                        "removed_title": "Artinian commutative rings",
                        "retained_title": "Artinian ring",
                        "reason": "Distinct mathematical context survives."
                    }]
                }), encoding="utf-8"
            )
            cleaned, report, source_registry = prepare_curated_cleanup(data, repo)
        self.assertEqual(report["surviving_groups"], 2)
        self.assertEqual(report["retired_searchable_heading_aliases"], 1)
        self.assertEqual(report["removed_duplicate_meanings"], 1)
        self.assertEqual(report["group_only_alias_cases_applied"],
                         ["artinian-context-group"])
        target = next(g for g in cleaned["groups"] if g["id"] == "g")
        self.assertEqual({m["id"] for m in target["meanings"]}, {"new", "m.variant"})
        self.assertIn("Artinian commutative rings", target["aliases"])
        form = next(m for m in target["meanings"] if m["id"] == "m.variant")["formulations"][0]
        self.assertEqual(form["id"], "f.variant")
        self.assertEqual(form["sources"][0]["url"], "https://example.org/specialized")
        self.assertEqual(cleaned["consolidated_ids"]["group_aliases"],
                         {"g.variant": "g"})
        self.assertNotIn("m.variant", cleaned["consolidated_ids"]["meaning_aliases"])
        self.assertEqual(len(source_registry["groups"]), 2)

    def test_ambiguous_alias_suppressed_without_dropping_meaning(self):
        data = deepcopy(self.base)
        data["groups"].append({
            "id": "g.radical", "title": "Radical ideal",
            "aliases": ["radical of an ideal", "radical property"],
            "meanings": [{"id": "m.radical", "label": "Commutative Algebra",
                          "formulations": [{
                              "id": "f.radical", "text": "An ideal I satisfies I=sqrt(I).",
                              "sources": [{"url": "https://example.org/radical-ideal"}]
                          }]}],
        })
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._repo(Path(tmp))
            (repo / "data/merged_cleanup_cross_heading_review.json").write_text(
                json.dumps({
                    "schema_version": 1,
                    "clear_duplicate_pending_group_migration": [],
                    "remove_misleading_aliases": [{
                        "case_id": "radical-false-synonym",
                        "group_id": "g.radical", "group_title": "Radical ideal",
                        "remove_alias": "radical of an ideal",
                        "reason": "An operation is not a predicate"
                    }]
                }), encoding="utf-8")
            result, report, refs = prepare_curated_cleanup(data, repo)
        g = next(g for g in result["groups"] if g["id"] == "g.radical")
        self.assertEqual(g["title"], "Radical ideal")
        self.assertNotIn("radical of an ideal", g["aliases"])
        self.assertIn("radical property", g["aliases"])
        self.assertEqual(g["meanings"][0]["formulations"][0]["id"], "f.radical")
        self.assertEqual(report["misleading_search_aliases_removed"],
                         ["radical-false-synonym"])
        self.assertEqual(len(refs["groups"]), 3)

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
