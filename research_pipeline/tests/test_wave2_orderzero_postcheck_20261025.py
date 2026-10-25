"""One-shot exhaustive read-only verification after applied S-linearity resolution."""
import json
import unittest
from pathlib import Path

from research_pipeline.engine.dependency_consolidation_readiness import assess, load_inputs
from research_pipeline.engine.dependency_global_audit import load_live_snapshot
from research_pipeline.engine.dependency_graph import graph_path, read

class ResolutionPostcheck(unittest.TestCase):
    def test_actual_resolved_candidate_and_full_mechanical_checks(self):
        repo = Path(__file__).resolve().parents[2]
        w = repo / "research_pipeline/experiments/reconstruction-v2-independent"
        snap = load_live_snapshot(w)
        state = snap["state"]["summary"]
        self.assertEqual(state["unresolved_missing_candidates"], 419)
        self.assertEqual(state["missing_occurrences"], 843)
        self.assertEqual(state["scan_amendment_event_count"], 773)
        self.assertFalse(state["consolidation_gate_valid"])
        self.assertEqual(state["phase"], "consolidate_occurrences")
        candidate = "missing.f9304694577e53d812c1"
        entry = next(x for x in snap["candidates"] if x["id"] == candidate)
        self.assertEqual(entry["status"], "resolved")
        self.assertEqual(entry["resolved_target_meaning_id"],
                         "meaning.wave2.cross110.module-linear")
        applied = read(graph_path(w) / "applied/resolve.wave2.orderzero-s-linear-20261025-001.json")
        self.assertEqual(applied["sha256"],
                         "d519a0c911253565dc1ea138f7cc36b107dc7767a6f91f4e9b4a508b10eaf2d9")
        res = next(x for x in snap["resolutions"] if x["missing_candidate_id"] == candidate)
        self.assertEqual(res["target_meaning_id"],
                         "meaning.wave2.cross110.module-linear")
        output = assess(load_inputs(w), exhaustive=True)
        checks = output["mechanical_checks"]
        self.assertEqual(len(checks), 19)
        self.assertTrue(all(checks.values()), checks)
        self.assertFalse(output["pass3_authorized_by_this_assessment"])
        self.assertEqual(output["status"],
                         "mechanical_checks_passed_review_decision_required")
        self.assertEqual(output["mathematical_consistency_review"]["summary"]
                         ["mechanical_integrity_count"], 0)
        after = load_live_snapshot(w)
        self.assertEqual(snap["state"], after["state"])
        self.assertEqual(snap["nodes"], after["nodes"])
        self.assertEqual(snap["inventory"], after["inventory"])
        print("ORDERZERO_POSTCHECK_ALL_19_PASSED")
        print("ORDERZERO_POSTCHECK_LEADS",
              output["mathematical_consistency_review"]["summary"]["total_review_candidates"])
        print("ORDERZERO_POSTCHECK_NEW_FINGERPRINT", state["unresolved_fingerprint"])
