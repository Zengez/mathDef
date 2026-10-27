"""Regression tests for dynamic source-scoped convention inheritance."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from research_pipeline.adapters.mathdef.conventions import (
    ConventionError, assessments_for_source, effective_interpretation,
    read_conventions, resolved_source_assessments,
)


class ConventionPolicyTests(unittest.TestCase):
    URL = "https://example.org/section/connected"

    def setUp(self):
        self.catalog = {
            "groups": [{
                "id": "g.connected", "title": "connected space",
                "meanings": [{
                    "id": "m.connected", "label": "topology",
                    "formulations": [{"id": "f.broad", "text": "No separation including empty."}],
                }]
            }], "relations": [],
        }
        self.record = {
            "convention_id": "topology.connected.nonempty",
            "concept_id": "topology.connected",
            "canonical_meaning_id": "m.connected",
            "note": "MathDef permits the empty space.",
        }

    def _repo(self, root, assessments):
        data = root / "data"
        data.mkdir()
        (data / "math_definition_conventions.json").write_text(
            json.dumps({"schema_version": 1, "entries": [self.record]}))
        (data / "math_source_convention_assessments.json").write_text(
            json.dumps({"schema_version": 1, "assessments": assessments}))
        return root

    def _assessment(self, status, **kwargs):
        return {
            "assessment_id": "assess." + status,
            "convention_id": "topology.connected.nonempty",
            "source_url": self.URL,
            "status": status,
            "scope": {"kind": "section", "locator": "sec.5", "name": "Section 5"},
            **kwargs,
        }

    def test_inconclusive_inherits_latest_canonical_without_claiming_evidence(self):
        checked = self._assessment("checked_inconclusive", checked_on="2026-10-27")
        with TemporaryDirectory() as tmp:
            repo = self._repo(Path(tmp), [checked])
            by_id, assessments = read_conventions(repo, self.catalog)
            initial = effective_interpretation(by_id[checked["convention_id"]],
                                                self.catalog, assessments[0])
            self.assertEqual(initial["status"], "checked_inconclusive")
            self.assertFalse(initial["author_agreement_verified"])
            self.assertEqual(initial["effective_interpretation"],
                             "inherit_current_mathdef_canonical")
            self.assertEqual(initial["current_formulation_ids"], ["f.broad"])
            # No historical stored interpretation: changing canonical data
            # changes the operational meaning in the next lookup.
            self.catalog["groups"][0]["meanings"][0]["formulations"] = [
                {"id": "f.latest", "text": "A genuinely broadened predicate."}]
            updated = effective_interpretation(by_id[checked["convention_id"]],
                                               self.catalog, assessments[0])
            self.assertEqual(updated["current_formulation_ids"], ["f.latest"])
            self.assertEqual(updated["status"], "checked_inconclusive")

    def test_verified_opposite_also_inherits_current_canonical(self):
        opposite = self._assessment(
            "verified_opposite", evidence_url=self.URL,
            evidence_locator="Sec 5: explicit absence of restriction",
        )
        with TemporaryDirectory() as tmp:
            repo = self._repo(Path(tmp), [opposite])
            resolved = resolved_source_assessments(repo, self.catalog, self.URL)
            self.assertEqual(len(resolved), 1)
            self.assertEqual(resolved[0]["status"], "verified_opposite")
            self.assertEqual(resolved[0]["effective_interpretation"],
                             "inherit_current_mathdef_canonical")
            self.assertFalse(resolved[0]["author_agreement_verified"])

    def test_positive_restriction_requires_evidence_and_stays_scoped(self):
        applies = self._assessment(
            "verified_applies", explicit_source_restriction="nonempty_required",
            evidence_url=self.URL, evidence_locator="Definition 5.1")
        with TemporaryDirectory() as tmp:
            repo = self._repo(Path(tmp), [applies])
            convention, checked = read_conventions(repo, self.catalog)
            resolved = effective_interpretation(convention[self.record["convention_id"]],
                                                self.catalog, checked[0])
            self.assertEqual(resolved["restriction"], "nonempty_required")
            self.assertEqual(resolved["effective_interpretation"],
                             "verified_source_restriction")
            self.assertEqual(assessments_for_source(
                self.URL, checked, applicable_scopes={"sec.5"}), [applies])
            self.assertEqual(assessments_for_source(
                self.URL, checked, applicable_scopes={"sec.2"}), [])

    def test_unknown_source_is_not_checked(self):
        with TemporaryDirectory() as tmp:
            repo = self._repo(Path(tmp), [])
            canonical, _ = read_conventions(repo, self.catalog)
            unknown = effective_interpretation(
                canonical[self.record["convention_id"]], self.catalog)
            self.assertEqual(unknown["status"], "not_checked")
            self.assertEqual(unknown["effective_interpretation"],
                             "inherit_current_mathdef_canonical")
            self.assertEqual(resolved_source_assessments(
                repo, self.catalog, "https://other.example.org"), [])

    def test_checked_inconclusive_cannot_contain_a_frozen_restriction(self):
        malformed = self._assessment(
            "checked_inconclusive", checked_on="2026-10-27",
            explicit_source_restriction="nonempty_required")
        with TemporaryDirectory() as tmp:
            repo = self._repo(Path(tmp), [malformed])
            with self.assertRaisesRegex(ConventionError, "cannot freeze restriction"):
                read_conventions(repo, self.catalog)


if __name__ == "__main__":
    unittest.main()
