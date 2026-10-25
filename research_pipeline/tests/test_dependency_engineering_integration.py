"""Read-only integration guards for approved main graph and identity provenance."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from research_pipeline.engine.core import PipelineError
from research_pipeline.engine.dependency_cycle_analysis import effective_references
from research_pipeline.engine.dependency_global_audit import candidate_review_bundle, load_live_snapshot
from research_pipeline.engine.dependency_graph import alias_map, missing_key


class EngineeringIdentityIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[1] / "experiments/reconstruction-v2-independent"
        self.graph = self.workspace / "dependency_graph"
        self.snapshot = load_live_snapshot(self.workspace)
        self.source = "form.22c049b8eee93897.system-of-parameters"
        self.definition = "form.b9defeff446a0526.ideal-of-definition-local-ring"
        self.canonical = "missing.b963edbe734f35266d3a"
        self.target = "meaning.b9defeff446a0526.ideal-of-definition-local-ring"

    def test_inactive_alias_is_preserved_but_not_resurrected_in_registry(self):
        event = next(a for a in self.snapshot["aliases"]
                     if a["alias_id"] == "alias.global-audit.20261023.051")
        observed = event["alias_candidate_id"]
        self.assertEqual(event["canonical_candidate_id"], self.canonical)
        registered = {c["id"]: c for c in self.snapshot["candidates"]}
        self.assertNotIn(observed, registered)
        self.assertEqual(registered[self.canonical]["resolved_target_meaning_id"], self.target)
        effective_aliases = alias_map(self.graph, set(registered), self.snapshot["aliases"])
        self.assertNotIn(observed, effective_aliases)
        self.assertEqual(len(effective_aliases), self.snapshot["state"]["summary"]["alias_candidate_records"])
        self.assertEqual(len(self.snapshot["aliases"]), len(effective_aliases) + 1)
        # Even an inactive event must retain unique append-only identity.
        with self.assertRaisesRegex(PipelineError, "Repeated/invalid"):
            alias_map(Path("."), {self.canonical}, [event, event])

    def test_observed_identity_canonical_reference_occurrence_and_seed_stay_distinct(self):
        live = self.snapshot["nodes"][self.source]
        ref = next(r for r in live["references"] if r["phrase"] == "m-primary")
        event = next(a for a in self.snapshot["aliases"]
                     if a["alias_id"] == "alias.global-audit.20261023.051")
        self.assertEqual(missing_key(ref["phrase"], ref["context"]), event["alias_candidate_id"])
        self.assertEqual(ref["missing_candidate_id"], self.canonical)
        self.assertEqual(ref["reviewed_existing_candidate_id"], self.canonical)
        projected = next(r for r in effective_references(self.snapshot)
                         if r["from_formulation"] == self.source
                         and r["occurrence_id"] == ref["occurrence_id"])
        self.assertEqual(projected["state"], "existing")
        self.assertEqual(projected["target_meaning_id"], self.target)
        self.assertEqual(projected["resolved_missing_candidate_id"], self.canonical)
        self.assertIn("candidate_resolution", projected["origin"])
        self.assertFalse(projected["occurrence_id"].startswith("seed."))
        raw = json.loads((self.graph / "nodes" / (self.source + ".json")).read_text())
        old = next(r for r in raw["references"] if r["phrase"] == "m-primary")
        self.assertEqual(old["state"], "unassigned")  # raw history was not edited
        self.assertNotEqual(old["occurrence_id"], ref["occurrence_id"])
        self.assertFalse(any(r["from_formulation"] == self.definition and
                             r.get("target_meaning_id") == self.target
                             for r in effective_references(self.snapshot)))

    def test_resolved_target_version_drift_does_not_reuse_stale_resolution(self):
        before = effective_references(self.snapshot)
        ref = next(r for r in before if r["from_formulation"] == self.source
                   and r.get("resolved_missing_candidate_id") == self.canonical)
        altered = deepcopy(self.snapshot)
        fid = altered["inventory"]["meanings"][self.target]["formulation_ids"][-1]
        altered["inventory"]["formulations"][fid]["version_sha256"] = "0" * 64
        after = next(r for r in effective_references(altered)
                     if r["from_formulation"] == self.source
                     and r["occurrence_id"] == ref["occurrence_id"])
        self.assertEqual(after["state"], "missing")
        self.assertEqual(after["missing_candidate_id"], self.canonical)
        self.assertNotIn("resolved_missing_candidate_id", after)
        # In-memory negative fixture only: physical graph was never rebuilt.
        self.assertEqual(load_live_snapshot(self.workspace), self.snapshot)

    def test_focus_excludes_resolved_candidates_and_keeps_live_indices_separate(self):
        with self.assertRaisesRegex(PipelineError, "noncanonical/resolved"):
            candidate_review_bundle(self.snapshot, candidate_ids=(self.canonical,))
        focused = candidate_review_bundle(self.snapshot, limit=8, compact_sources=True)
        self.assertNotIn(self.canonical, {c["candidate_id"] for c in focused["candidates"]})
        for fid, source in focused["source_contexts"].items():
            refs = self.snapshot["nodes"][fid]["references"]
            self.assertEqual([row["live_reference_index"] for row in source["effective_live_reference_rows"]],
                             list(range(len(refs))))
            self.assertEqual([row["expected_occurrence_id"] for row in source["effective_live_reference_rows"]],
                             [r["occurrence_id"] for r in refs])
            self.assertTrue(all(row["editable_in_live_node"] is False
                                for row in source["historical_seed_references"]))
