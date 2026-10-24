"""Independent regression tests for source-free historical seed preview."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from research_pipeline.engine.core import PipelineError, digest
from research_pipeline.engine.dependency_seed_retarget_preview import (
    preview_seed_retargets,
)
from research_pipeline.engine.dependency_global_audit import load_live_snapshot


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

    def test_live_round175_proposals_are_valid_at_original_snapshot(self):
        root = Path(__file__).resolve().parents[1]
        workspace = root / "experiments" / "reconstruction-v2-independent"
        manifest_path = root / "review_proposals" / "WAVE2_SEED_SCOPE_ROUND175_READONLY.json"
        if not manifest_path.is_file() or not (workspace / "dependency_graph" / "STATE.json").is_file():
            self.skipTest("Full independent Wave2 graph not part of this installation")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        snapshot = load_live_snapshot(workspace)
        # Historical proposals become stale when the underlying graph advances.
        # A new graph version should not silently reactivate old decisions.
        current = snapshot["state"]["summary"]["unresolved_fingerprint"]
        if current != manifest["unresolved_fingerprint"]:
            self.skipTest("Round 175 manifest is intentionally stale for the current graph")
        if snapshot["inventory"]["seed_relations_sha256"] != manifest["seed_relations_sha256"]:
            self.skipTest("Seed input changed; historical preview needs independent re-review")
        result = preview_seed_retargets(snapshot, manifest)
        self.assertEqual(result["proposal_count"], 18)
        self.assertFalse(result["applied"])
        self.assertEqual(
            sum(x["proposed_candidate_id"] == "missing.fcb5ab865c6d9dbb3d79"
                for x in result["proposals"]), 16)
        self.assertEqual(
            sum(x["proposed_candidate_id"] == "missing.c5104821c3c70afa1f63"
                for x in result["proposals"]), 2)

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

    def test_complete_seed_record_can_anchor_a_portable_proposal(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["changes"][0].pop("expected_seed_sha256")
        manifest["changes"][0]["expected_seed_record"] = copy.deepcopy(self.seed)
        out = preview_seed_retargets(self.snapshot, manifest)
        self.assertEqual(out["proposal_count"], 1)
        manifest["changes"][0]["expected_seed_record"]["phrase"] = "wrong context"
        with self.assertRaises(PipelineError):
            preview_seed_retargets(self.snapshot, manifest)

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
