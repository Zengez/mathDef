"""Display-only UI adapter tests with an unrelated, synthetic astronomy corpus."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.ui.renderer import ViewError, render, to_index


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
                      "formulations": [
                          {"id": "form.orbit.one", "text": "A gravitational trajectory.",
                           "sources": [{"title": "Scientific catalog",
                                        "url": "https://example.org/catalog",
                                        "locator": "https://example.org/catalog/orbit"}]}]},
                     {"id": "meaning.orbit.two", "label": "Dynamical systems",
                      "formulations": [
                          {"id": "form.orbit.two", "text": "Iterates of a transformation.",
                           "sources": [{"title": "Scientific handbook",
                                        "url": "https://example.org/handbook",
                                        "locator": "https://example.org/handbook/orbit"}]}]}
                 ]},
                {"id": "concept.planet", "title": "Planet", "aliases": ["world"],
                 "meanings": [{"id": "meaning.planet", "label": "Planetary science",
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
        self.assertEqual(by_name["Planet"]["path"], "")
        self.assertTrue((out / "styles.css").exists())
        self.assertTrue((out / "app.js").exists())
        self.assertTrue((out / "feedback.js").exists())
        self.assertFalse((self.root / "definitions-index.json").exists())

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
