"""Independent regression tests for source-free historical seed preview."""
from __future__ import annotations

import copy
import unittest

from research_pipeline.engine.core import PipelineError, digest
from research_pipeline.engine.dependency_seed_retarget_preview import (
    preview_seed_retargets,
)


class SeedRetargetPreviewTests(unittest.TestCase):
    def setUp(self):
        self.form = {
            "meaning_id": "meaning.source",
            "display_term": "terminal object",
            "text": "In a category C, an object T is terminal when all objects map uniquely to T.",
            "context": "Category theory",
            "version_sha256": "source-version-0",
        }
        self.seed = {
            "relation_id": "rel.old.001",
            "from_formulation": "form.source",
            "target_meaning_id": "meaning.small-category",
            "target_query": None,
            "phrase": "category C",
            "provenance": "screened",
            "relation_state": "screened",
        }
        self.snapshot = {
            "inventory": {
                "source_inventory_sha256": "inv-1",
                "seed_relations_sha256": "seeds-1",
                "formulations": {"form.source": self.form},
                "meanings": {
                    "meaning.small-category": {"display_term": "small category"},
                    "meaning.source": {"display_term": "terminal object"},
                },
                "seed_relations": [self.seed],
            },
            "state": {"summary": {"unresolved_fingerprint": "unresolved-1"}},
            "candidates": [{
                "id": "missing.unrestricted-category",
                "query": "category (unrestricted)",
                "context": "Any category, small or large",
                "status": "unresearched",
                "alias_of": None,
                "resolved_target_meaning_id": None,
                "incoming_formulation_ids": ["form.source"],
            }],
            "aliases": [],
        }
        self.manifest = {
            "schema_version": 1,
            "inventory_sha256": "inv-1",
            "seed_relations_sha256": "seeds-1",
            "unresolved_fingerprint": "unresolved-1",
            "reviewed_by": "source-free mathematical reviewer",
            "changes": [{
                "relation_id": "rel.old.001",
                "expected_seed_sha256": digest(self.seed),
                "expected_from_formulation": "form.source",
                "expected_version_sha256": "source-version-0",
                "expected_seed_target_meaning_id": "meaning.small-category",
                "replacement": {
                    "state": "missing",
                    "missing_candidate_id": "missing.unrestricted-category",
                },
                "review_rationale": (
                    "Terminal objects are meaningful in large locally small "
                    "categories, and the source does not require that its "
                    "entire ambient category have a set of objects."
                ),
            }],
        }

    def test_valid_seed_preview_never_modifies_snapshot_or_manifest(self):
        before = copy.deepcopy(self.snapshot)
        manifest_before = copy.deepcopy(self.manifest)
        out = preview_seed_retargets(self.snapshot, self.manifest)
        self.assertTrue(out["read_only"])
        self.assertFalse(out["applied"])
        self.assertTrue(out["no_graph_or_seed_writes"])
        self.assertFalse(out["mathematics_certified"])
        self.assertEqual(out["proposal_count"], 1)
        self.assertEqual(out["proposals"][0]["previous_target_term"], "small category")
        self.assertEqual(out["proposals"][0]["proposed_candidate_query"],
                         "category (unrestricted)")
        self.assertEqual(out["proposals"][0]["expected_seed_sha256"], digest(self.seed))
        self.assertEqual(self.snapshot, before)
        self.assertEqual(self.manifest, manifest_before)

    def test_stale_inventory_or_seed_fingerprint_rejected(self):
        for field in ("inventory_sha256", "seed_relations_sha256",
                      "unresolved_fingerprint"):
            manifest = copy.deepcopy(self.manifest)
            manifest[field] = "stale"
            with self.subTest(field=field), self.assertRaises(PipelineError):
                preview_seed_retargets(self.snapshot, manifest)

    def test_stale_source_or_seed_target_rejected(self):
        for field in ("expected_seed_sha256", "expected_from_formulation",
                      "expected_version_sha256",
                      "expected_seed_target_meaning_id"):
            manifest = copy.deepcopy(self.manifest)
            manifest["changes"][0][field] = "bad-value"
            with self.subTest(field=field), self.assertRaises(PipelineError):
                preview_seed_retargets(self.snapshot, manifest)

    def test_alias_resolved_and_unregistered_candidate_rejected(self):
        for condition in ("alias", "resolved", "noncanonical", "unregistered"):
            snap = copy.deepcopy(self.snapshot)
            candidate = snap["candidates"][0]
            if condition == "alias":
                snap["aliases"] = [{
                    "alias_candidate_id": candidate["id"],
                    "canonical_candidate_id": "missing.other",
                }]
            if condition == "resolved":
                candidate["resolved_target_meaning_id"] = "meaning.small-category"
            if condition == "noncanonical":
                candidate["alias_of"] = "missing.other"
            if condition == "unregistered":
                candidate["incoming_formulation_ids"] = []
            with self.subTest(condition=condition), self.assertRaises(PipelineError):
                preview_seed_retargets(snap, self.manifest)

    def test_duplicate_relation_and_unknown_relation_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["changes"].append(copy.deepcopy(manifest["changes"][0]))
        with self.assertRaises(PipelineError):
            preview_seed_retargets(self.snapshot, manifest)
        manifest = copy.deepcopy(self.manifest)
        manifest["changes"][0]["relation_id"] = "rel.other"
        with self.assertRaises(PipelineError):
            preview_seed_retargets(self.snapshot, manifest)

    def test_unsupported_replacement_or_weak_review_rejected(self):
        for replacement in (
            {"state": "existing", "target_meaning_id": "meaning.small-category"},
            {"state": "missing", "missing_candidate_id": "missing.unknown"},
            {"state": "missing", "missing_candidate_id":
             "missing.unrestricted-category", "extra": True},
        ):
            manifest = copy.deepcopy(self.manifest)
            manifest["changes"][0]["replacement"] = replacement
            with self.subTest(replacement=replacement), self.assertRaises(PipelineError):
                preview_seed_retargets(self.snapshot, manifest)
        manifest = copy.deepcopy(self.manifest)
        manifest["changes"][0]["review_rationale"] = "generic category"
        with self.assertRaises(PipelineError):
            preview_seed_retargets(self.snapshot, manifest)


if __name__ == "__main__":
    unittest.main()
