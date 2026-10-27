"""Read-only existing-definition comparison screen tests."""
import unittest
from copy import deepcopy

from research_pipeline.adapters.mathdef.dedup_screen import screen


class ExistingDedupScreenTests(unittest.TestCase):
    def test_only_existing_ids_and_never_mutates_or_creates_terms(self):
        long_text = ("A complete normed vector space is a normed vector space "
                     "where every Cauchy sequence converges in its norm.")
        catalog = {"groups": [
            {"id": "ga", "title": "Banach space", "aliases": ["complete normed space"],
             "meanings": [{"id": "ma", "formulations": [{"id": "fa", "text": long_text}]}]},
            {"id": "gb", "title": "complete normed space",
             "aliases": ["Banach space"],
             "meanings": [{"id": "mb", "formulations": [{"id": "fb", "text": long_text}]}]},
            {"id": "gc", "title": "Metric space", "aliases": [],
             "meanings": [{"id": "mc", "formulations": [{"id": "fc",
               "text": "A distance on a set obeys positivity symmetry and triangle inequality."}]}]},
        ], "relations": []}
        before = deepcopy(catalog)
        report = screen(catalog, cutoff=0.7)
        self.assertEqual(catalog, before)
        self.assertEqual(report["counts"]["groups"], 3)
        self.assertEqual(report["counts"]["name_alias_collision_pairs"], 2)
        self.assertEqual(report["counts"]["cross_heading_lexical_pairs_above_cutoff"], 1)
        pair = report["cross_heading_lexical_screen"][0]
        self.assertEqual({pair["left_formulation"], pair["right_formulation"]}, {"fa", "fb"})
        self.assertEqual(report["kind"], "existing_definitions_only_no_vocabulary_discovery")
        self.assertNotIn("term_candidates", report)

    def test_same_heading_formulations_do_not_appear_as_cross_heading_pairs(self):
        body = "A topological space whose every open cover has a finite subcover."
        c = {"groups": [{"id": "g", "title": "Compact space", "aliases": [],
             "meanings": [{"id": "m1", "formulations": [{"id": "f1", "text": body},
               {"id": "f2", "text": body}]}]}], "relations": []}
        out = screen(c)
        self.assertEqual(out["counts"]["cross_heading_lexical_pairs_above_cutoff"], 0)
        self.assertEqual(out["counts"]["within_meaning_multi_formulations"], 1)


if __name__ == "__main__":
    unittest.main()
