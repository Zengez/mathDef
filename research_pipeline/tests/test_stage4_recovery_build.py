"""Stage 4 recovered context grouping and stable evidence identifiers."""
import unittest

from research_pipeline.engine.core import PipelineError
from research_pipeline.engine.stage4_recovery_build import (
    EQUIVALENT, context_label, identifier_suffix)


class Stage4RecoveryBuildTests(unittest.TestCase):
    def test_context_renamed_without_loss(self):
        self.assertEqual(
            context_label({"context_hint": "Topology: irreducible component"}),
            "irreducible component")
        self.assertEqual(
            context_label({"context_hint": "Field theory: prime subfield"}),
            "prime subfield")

    def test_legacy_and_recovery_observation_ids(self):
        tid = "term.39488f3e396a1c77"
        self.assertEqual(
            identifier_suffix({"id": "obs.paraphrase.39488f3e396a1c77.algebraically_closed"}, tid),
            "algebraically-closed")
        self.assertEqual(
            identifier_suffix({"id": "obs.recovery.39488f3e396a1c77.algebraic-closure"}, tid),
            "algebraic-closure")

    def test_different_term_observation_rejected(self):
        with self.assertRaisesRegex(PipelineError, "Unrecognized source"):
            identifier_suffix({"id": "obs.recovery.aaaaaaa.example"}, "term.bbbbbbb")

    def test_equivalence_is_explicit_and_not_universal(self):
        self.assertIn("Pure ideals", EQUIVALENT)
        self.assertNotIn("Factorization", EQUIVALENT)
        self.assertEqual(len(EQUIVALENT["Pure ideals"][0]), 2)


if __name__ == "__main__":
    unittest.main()
