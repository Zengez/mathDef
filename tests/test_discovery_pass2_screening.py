"""Conservative automatic exclusions must never discard named mathematical terms."""
import unittest
from scripts.discovery_pass2_triage import classify, confident_false_positive

class ScreeningTests(unittest.TestCase):
    def test_unambiguously_non_terms_removed(self):
        cases = ["a compact group", "the finite dimensional vector space",
                 "abelian group is a subgroup", "action its isomorphism group",
                 "vector space and", "we construct a group"]
        for phrase in cases:
            with self.subTest(phrase=phrase):
                self.assertIsNotNone(confident_false_positive(phrase))

    def test_plausible_math_stays(self):
        cases = ["group of units", "space of functions", "ring with identity",
                 "if and only if", "category of sets", "fundamental group",
                 "abelian category", "space of bounded linear operators"]
        for phrase in cases:
            with self.subTest(phrase=phrase):
                self.assertIsNone(confident_false_positive(phrase))

    def test_existing_weak_flags_do_not_remove(self):
        phrase = "inner product space"
        self.assertIsNone(confident_false_positive(phrase))
        self.assertIn(classify(phrase)[0], {"plausible_term_review","higher_thinking_review"})

if __name__=="__main__":
    unittest.main()
