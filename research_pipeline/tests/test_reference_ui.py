"""Display-only UI adapter tests with an unrelated, synthetic astronomy corpus."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.ui.renderer import ViewError, render, to_index, to_sources_index


class ReferenceUITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.catalog = {
            "groups": [
                {"id": "concept.orbit", "title": "Orbit", "aliases": [],
                 "meanings": [
                     {"id": "meaning.orbit.one", "label": "Celestial mechanics",
                      "subject": "Astronomy",
                      "formulations": [
                          {"id": "form.orbit.one", "text": "A gravitational trajectory.",
                           "sources": [{"title": "Scientific catalog",
                                        "url": "https://example.org/catalog",
                                        "locator": "https://example.org/catalog/orbit"}]}]},
                     {"id": "meaning.orbit.two", "label": "Dynamical systems",
                      "subject": "Mathematical Dynamics",
                      "formulations": [
                          {"id": "form.orbit.two", "text": "Iterates of a transformation.",
                           "sources": [{"title": "Scientific handbook",
                                        "url": "https://example.org/handbook",
                                        "locator": "https://example.org/handbook/orbit"}]}]}
                 ]},
                {"id": "concept.planet", "title": "Planet", "aliases": ["world"],
                 "meanings": [{"id": "meaning.planet", "label": "Planetary science",
                               "subject": "Astronomy",
                               "formulations": [
                                   {"id": "form.planet", "text": "A celestial body.",
                                    "sources": [{"title": "Scientific catalog",
                                                 "url": "https://example.org/catalog",
                                                 "locator": "https://example.org/catalog/planet"}]}]}]}
            ],
            "relations": [
                {"id": "rel.planet-orbit", "from_formulation": "form.planet",
                 "target_meaning": "meaning.orbit.one",
                 "relation_type": "definition_uses", "review_state": "screened"}
            ]
        }
        self.brand = {
            "schema_version": 1, "project_name": "AstroRef",
            "logo": "✦", "eyebrow": "SCIENCE REFERENCE",
            "subtitle": "An independent astronomy glossary",
            "repository_url": "https://github.com/example/astroref",
            "noun": "definition", "noun_plural": "definitions",
            "search_term_label": "terms", "search_content_label": "definitions"
        }
        (self.root / "catalog.json").write_text(json.dumps(self.catalog), encoding="utf-8")
        (self.root / "brand.json").write_text(json.dumps(self.brand), encoding="utf-8")

    def test_unrelated_brand_and_contexts_are_independent(self):
        out = self.root / "viewer"
        result = render(self.root / "catalog.json", self.root / "brand.json",
                        out, "Initial stage", "Synthetic research draft")
        self.assertEqual((result["terms"], result["formulations"], result["relations"]), (2, 3, 1))
        markup = (out / "index.html").read_text(encoding="utf-8")
        self.assertIn("AstroRef", markup)
        self.assertIn("SCIENCE REFERENCE", markup)
        self.assertIn("Synthetic research draft", markup)
        self.assertIn("term-pane", markup)
        self.assertIn("definition-pane", markup)
        self.assertNotIn("Original mathDef site", markup)
        entries = json.loads((out / "definitions-index.json").read_text(encoding="utf-8"))
        by_name = {e["term"]: e for e in entries}
        self.assertEqual(len(by_name["Orbit"]["formulations"]), 2)
        self.assertEqual(by_name["Planet"]["aliases"], ["world"])
        self.assertEqual(by_name["Planet"]["dependencies"][0]["id"], by_name["Orbit"]["id"])
        self.assertEqual(by_name["Orbit"]["formulations"][0]["sources"][0]["title"],
                         "Scientific catalog")
        self.assertEqual([f["subject"] for f in by_name["Orbit"]["formulations"]],
                         ["Astronomy", "Mathematical Dynamics"])
        self.assertEqual(by_name["Planet"]["formulations"][0]["subject"], "Astronomy")
        self.assertEqual(by_name["Planet"]["path"], "")
        self.assertTrue((out / "styles.css").exists())
        self.assertTrue((out / "app.js").exists())
        self.assertTrue((out / "subject_priority.js").exists())
        self.assertTrue((out / "sources_ui.js").exists())
        self.assertIn('src="./subject_priority.js"', markup)
        self.assertTrue((out / "feedback.js").exists())
        self.assertFalse((self.root / "definitions-index.json").exists())

    def _approved_override(self, **updates):
        item = {
            "id": "accepted-example",
            "status": "approved",
            "source_formulation_id": "form.planet",
            "target_group_id": "concept.orbit",
            "preferred_formulation_id": "form.orbit.two",
            "approval_reference": "https://github.com/example/astroref/issues/12",
            "reason": "Editor accepted the narrower mathematical context",
        }
        item.update(updates)
        return {"schema_version": 1, "overrides": [item]}

    def test_approved_priority_override_attaches_to_original_link_not_catalog(self):
        approved = self._approved_override()
        index = to_index(self.catalog, expansion_overrides=approved)
        planet = next(x for x in index if x["term"] == "Planet")
        dep = planet["formulations"][0]["dependencies"][0]
        self.assertEqual(dep["preferred_formulation"], "form.orbit.two")
        self.assertEqual(dep["priority_override_id"], "accepted-example")
        self.assertEqual(planet["dependencies"][0]["preferred_formulation"], "form.orbit.two")
        self.assertNotIn("preferred_formulation", self.catalog["relations"][0])
        (self.root / "approved.json").write_text(json.dumps(approved), encoding="utf-8")
        out = self.root / "approved-viewer"
        render(self.root / "catalog.json", self.root / "brand.json",
               out, "Draft", "Synthetic", expansion_overrides_file=self.root / "approved.json")
        published = json.loads((out / "definitions-index.json").read_text())
        self.assertEqual(next(x for x in published if x["term"] == "Planet")
                         ["formulations"][0]["dependencies"][0]["preferred_formulation"],
                         "form.orbit.two")

    def test_occurrence_specific_override_supersedes_general_and_bad_rules_fail(self):
        second = dict(self.catalog["relations"][0])
        self.catalog["relations"][0].update({"span_start": 2, "span_end": 8})
        second.update({"id": "rel.other", "span_start": 12, "span_end": 18})
        self.catalog["relations"].append(second)
        broad = self._approved_override()["overrides"][0]
        specific = dict(broad, id="exact-other", preferred_formulation_id="form.orbit.one",
                        source_span={"start": 12, "end": 18})
        overrides = {"schema_version": 1, "overrides": [broad, specific]}
        first, second_dep = next(x for x in to_index(
            self.catalog, expansion_overrides=overrides) if x["term"] == "Planet"
        )["formulations"][0]["dependencies"]
        self.assertEqual(first["preferred_formulation"], "form.orbit.two")
        self.assertEqual(second_dep["preferred_formulation"], "form.orbit.one")
        for bad in (
            self._approved_override(preferred_formulation_id="form.planet"),
            self._approved_override(status="pending"),
            self._approved_override(source_formulation_id="does-not-exist"),
            self._approved_override(target_group_id="other-group"),
            self._approved_override(source_span={"start": 70, "end": 80}),
            {"schema_version": 1, "overrides": [broad, broad]},
        ):
            with self.subTest(bad=bad), self.assertRaises(ViewError):
                to_index(self.catalog, expansion_overrides=bad)

    def test_nested_priority_follows_approved_later_source_formulation(self):
        other = {"id": "form.planet.two", "text": "Another discussion of orbits.",
                 "sources": [{"title": "Reference", "url": "https://example.org/ref"}]}
        self.catalog["groups"][1]["meanings"][0]["formulations"].append(other)
        relation = {"id": "later", "from_formulation": "form.planet.two",
                    "target_meaning": "meaning.orbit.two",
                    "relation_type": "definition_uses", "review_state": "screened"}
        self.catalog["relations"].append(relation)
        rule = self._approved_override(source_formulation_id="form.planet.two")
        index = to_index(self.catalog, expansion_overrides=rule)
        planet = next(x for x in index if x["term"] == "Planet")
        self.assertEqual(planet["dependencies"][0]["formulation"], "form.planet.two")
        self.assertEqual(planet["dependencies"][0]["preferred_formulation"], "form.orbit.two")


    def _source_registry(self):
        # A domain-produced registry, not a source rank invented by the UI.
        return {
            "schema_version": 1, "scope": "example_sources",
            "sources": {
                "s.catalog": {
                    "id": "s.catalog", "url": "https://example.org/catalog/orbit",
                    "titles": ["Scientific catalog"],
                    "occurrences": [{
                        "group_id": "concept.orbit", "meaning_id": "meaning.orbit.one",
                        "formulation_id": "form.orbit.one",
                        "locator": "https://example.org/catalog/orbit",
                        "role": "supporting definition",
                        "verification_status": "direct_source_passage_checked",
                        "provenance_only": False,
                    }],
                    "source_convention_assessments": [],
                },
                "s.handbook": {
                    "id": "s.handbook", "url": "https://example.org/handbook/orbit",
                    "titles": ["Scientific handbook"],
                    "occurrences": [{
                        "group_id": "concept.orbit", "meaning_id": "meaning.orbit.two",
                        "formulation_id": "form.orbit.two",
                        "locator": "https://example.org/handbook/orbit",
                        "role": "supporting definition",
                        "verification_status": "untracked",
                        "provenance_only": False,
                    }],
                },
                "s.planet": {
                    "id": "s.planet", "url": "https://example.org/catalog/planet",
                    "titles": ["Scientific catalog — planets"],
                    "occurrences": [{
                        "group_id": "concept.planet", "meaning_id": "meaning.planet",
                        "formulation_id": "form.planet",
                        "role": "source-file provenance",
                        "verification_status": "untracked",
                        "provenance_only": True,
                    }],
                },
            },
            "groups": [
                {"group_id": "concept.orbit", "term": "Orbit",
                 "source_ids": ["s.catalog", "s.handbook"],
                 "meanings": [
                     {"meaning_id": "meaning.orbit.one", "subject": "Astronomy",
                      "context": None,
                      "source_ids": ["s.catalog"],
                      "primary_source_by_formulation": {"form.orbit.one": "s.catalog"},
                      "convention_notes": []},
                     {"meaning_id": "meaning.orbit.two", "subject": "Mathematical Dynamics",
                      "context": None,
                      "source_ids": ["s.handbook"],
                      "primary_source_by_formulation": {"form.orbit.two": "s.handbook"},
                      "convention_notes": []}
                 ]},
                {"group_id": "concept.planet", "term": "Planet",
                 "source_ids": ["s.planet"],
                 "meanings": [
                     {"meaning_id": "meaning.planet", "subject": "Astronomy",
                      "context": None,
                      "source_ids": ["s.planet"],
                      "primary_source_by_formulation": {},
                      "convention_notes": []}
                 ]}
            ]
        }

    def test_sources_index_preserves_metadata_without_claiming_verification(self):
        sources = self._source_registry()
        validated = to_sources_index(self.catalog, sources)
        self.assertIs(validated, sources)
        self.assertEqual(validated["sources"]["s.catalog"]["occurrences"][0]
                         ["verification_status"], "direct_source_passage_checked")
        self.assertEqual(validated["sources"]["s.planet"]["occurrences"][0]
                         ["provenance_only"], True)
        self.assertEqual(validated["groups"][0]["meanings"][0]
                         ["primary_source_by_formulation"]["form.orbit.one"], "s.catalog")
        out = self.root / "sources-viewer"
        render(self.root / "catalog.json", self.root / "brand.json", out,
               "Draft", "Synthetic", source_registry=sources)
        page = (out / "index.html").read_text()
        self.assertIn("sources-dialog", page)
        self.assertTrue((out / "sources-index.json").exists())
        self.assertTrue((out / "sources_ui.js").exists())
        self.assertIn('src="./sources_ui.js"', page)
        self.assertEqual(json.loads((out / "sources-index.json").read_text()), sources)
        self.assertIn('"sources_file": "sources-index.json"', page)
        # A generic independent stage without an explicit source registry
        # should not fabricate primary-source selections.
        out2 = self.root / "no-sources"
        render(self.root / "catalog.json", self.root / "brand.json",
               out2, "Draft", "Synthetic")
        self.assertFalse((out2 / "sources-index.json").exists())

    def test_sources_index_rejects_stale_primary_and_missing_occurrence(self):
        import copy
        base = self._source_registry()
        for edited in ("stale_form", "unknown_source", "false_primary",
                       "wrong_owner", "missing_group"):
            registry = copy.deepcopy(base)
            if edited == "stale_form":
                registry["groups"][0]["meanings"][0]["primary_source_by_formulation"] = {
                    "form.not-present": "s.catalog"
                }
            elif edited == "unknown_source":
                registry["groups"][0]["meanings"][0]["primary_source_by_formulation"] = {
                    "form.orbit.one": "s.not-present"
                }
            elif edited == "false_primary":
                registry["groups"][1]["meanings"][0]["primary_source_by_formulation"] = {
                    "form.planet": "s.planet"
                }
            elif edited == "wrong_owner":
                registry["sources"]["s.catalog"]["occurrences"][0]["group_id"] = "concept.planet"
            elif edited == "missing_group":
                registry["groups"].pop()
            with self.subTest(edited=edited), self.assertRaises(ViewError):
                to_sources_index(self.catalog, registry)

    def test_reject_bad_source_and_relation(self):
        self.catalog["groups"][0]["meanings"][0]["formulations"][0]["sources"] = []
        with self.assertRaisesRegex(ViewError, "source evidence"):
            to_index(self.catalog)
        self.catalog["groups"][0]["meanings"][0]["formulations"][0]["sources"] = [
            {"title": "Scientific catalog", "url": "https://example.org"}
        ]
        self.catalog["relations"][0]["target_meaning"] = "meaning.missing"
        with self.assertRaisesRegex(ViewError, "endpoint"):
            to_index(self.catalog)

    def test_branding_values_are_escaped(self):
        self.brand["subtitle"] = "<script>alert('XSS')</script>"
        (self.root / "brand.json").write_text(json.dumps(self.brand), encoding="utf-8")
        render(self.root / "catalog.json", self.root / "brand.json",
               self.root / "viewer", "Draft", "Stage")
        page = (self.root / "viewer/index.html").read_text()
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn("<script>alert('XSS')</script>", page)


if __name__ == "__main__":
    unittest.main()
