"""Regression checks for read-only, overlay-aware provenance metadata audit."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import Workspace
from research_pipeline.engine.dependency_graph import inventory_sync
from research_pipeline.engine.dependency_provenance_audit import (
    audit_workspace, summarize_provenance,
)


class ProvenanceAuditTests(unittest.TestCase):
    def test_structural_links_and_unverified_status_are_separate(self):
        inventory = {
            "source_inventory_sha256": "frozen-inventory-test",
            "formulations": {
                "form.a": {"origin": "screened", "evidence_ids": ["obs.a"]},
                "form.b": {"origin": "provisional", "evidence_ids": ["obs.b"]},
            },
            "meanings": {
                "meaning.a": {"display_term": "Same", "formulation_ids": ["form.a"]},
                "meaning.b": {"display_term": "Same", "formulation_ids": ["form.b"]},
            },
        }
        observations = {
            "obs.a": {"record_kind": "paraphrase", "source_id": "src.a",
                      "locator": "https://example.org/a"},
            "obs.b": {"record_kind": "paraphrase", "source_id": "src.b",
                      "locator": "https://example.org/b",
                      "verification_state": "index_locator_only"},
        }
        result = summarize_provenance(
            inventory, observations, {"src.a": {}, "src.b": {}}
        )
        self.assertTrue(result["structural_provenance_complete"])
        self.assertFalse(result["external_content_verified_by_this_command"])
        self.assertEqual(result["evidence_links"], 2)
        self.assertEqual(result["explicit_verification_state_counts"], {
            "index_locator_only": 1, "unspecified": 1
        })
        self.assertEqual(result["duplicate_display_name_groups"], 1)

    def test_detects_all_three_broken_evidence_steps(self):
        inventory = {
            "source_inventory_sha256": "test",
            "formulations": {
                "form.empty": {"origin": "screened", "evidence_ids": []},
                "form.missing": {"origin": "screened", "evidence_ids": ["not-there"]},
                "form.bad-source": {"origin": "provisional", "evidence_ids": ["obs.bad"]},
            },
            "meanings": {},
        }
        obs = {"obs.bad": {"record_kind": "paraphrase", "source_id": "no-source",
                           "locator": ""}}
        r = summarize_provenance(inventory, obs, {}, example_limit=3)
        self.assertFalse(r["structural_provenance_complete"])
        self.assertEqual(r["zero_evidence_formulations"], 1)
        self.assertEqual(r["missing_evidence_records"], 1)
        self.assertEqual(r["missing_source_records"], 1)
        self.assertEqual(r["missing_locator_fields"], 1)

    def test_reads_population_overlay_without_modifying_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            Workspace(root).init({
                "schema_version": 1, "project": "Test", "term_kind": "term",
                "content_kind": "definition", "adapter": "mathdef",
                "external_reference_mode": True, "independent_second_wave": True,
            })
            records = root / "records"
            records.joinpath("meanings.jsonl").write_text(
                json.dumps({
                    "id": "meaning.a", "display_term": "A", "context": "testing",
                    "formulations": [{"id": "form.a", "text": "A test.",
                                     "evidence_ids": ["obs.draft"]}],
                }) + "\n", encoding="utf-8"
            )
            population = root / "population" / "records"
            population.mkdir(parents=True)
            population.joinpath("observations.jsonl").write_text(
                json.dumps({"id": "obs.draft", "term_id": "term.draft",
                            "source_id": "src.draft", "record_kind": "paraphrase",
                            "locator": "https://example.org/draft",
                            "text": "Independent note"}) + "\n", encoding="utf-8"
            )
            population.joinpath("sources.jsonl").write_text(
                json.dumps({"id": "src.draft", "title": "Draft source",
                            "url": "https://example.org/draft",
                            "rights": "locator_only", "access": "free",
                            "authority_reviewed": True}) + "\n", encoding="utf-8"
            )
            inventory_sync(root)
            inv_file = root / "dependency_graph" / "INVENTORY.json"
            before = inv_file.read_bytes()
            result = audit_workspace(root)
            self.assertEqual(result["formulations"], 1)
            self.assertEqual(result["missing_evidence_records"], 0)
            self.assertEqual(result["missing_source_records"], 0)
            self.assertTrue(result["structural_provenance_complete"])
            self.assertEqual(before, inv_file.read_bytes())


if __name__ == "__main__":
    unittest.main()
