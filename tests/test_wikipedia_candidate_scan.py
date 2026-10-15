import tempfile
import unittest
from pathlib import Path
from scripts.wikipedia_candidate_scan import normalize, load_terms, inventory

class FakeReader:
    def request(self, category, continuation=None):
        if category == "Category:Complex analysis":
            return {"query": {"categorymembers": [
                {"ns": 0, "title": "Bergman kernel"},
                {"ns": 0, "title": "Bloch space"},
                {"ns": 14, "title": "Category:Hardy spaces"},
                {"ns": 0, "title": "A theorem"},
            ]}}
        return {"query": {"categorymembers": [
            {"ns": 0, "title": "Szegő kernel"},
            {"ns": 0, "title": "Bergman kernel"},
        ]}}

class WikiScannerTests(unittest.TestCase):
    def test_normalized_terms_and_aliases(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / "sample.tex"
            p.write_text(
                "% id: functionspaces.bloch\n"
                "% term: Bloch space on the disk\n"
                "% aliases: Bloch space | Spaces of Bloch functions\n\nBody."
            )
            terms = load_terms(Path(folder))
            self.assertIn("bloch space", terms)
            self.assertIn("functionspaces.bloch", terms["bloch space"])
    def test_inventory_dedup_and_category_expansion(self):
        terms = {"bloch space": {"functionspaces.bloch"}}
        rows, scanned = inventory(FakeReader(), ["Category:Complex analysis"],
                                   1, 3, 100, terms)
        self.assertEqual(scanned, 2)
        self.assertEqual(len(rows), 4)
        by_title = {row["title"]: row for row in rows}
        self.assertEqual(by_title["Bloch space"]["coverage"],
                         "present_exact_title_or_alias")
        self.assertEqual(by_title["Bergman kernel"]["review_priority"],
                         "review_high")
        self.assertIn("%C5%91", by_title["Szegő kernel"]["wikipedia_url"])
        self.assertEqual(by_title["A theorem"]["review_priority"], "review_low")
    def test_normalize(self):
        self.assertEqual(normalize("Bergman kernel (several variables)"),
                         "bergman kernel")

if __name__ == "__main__":
    unittest.main()
