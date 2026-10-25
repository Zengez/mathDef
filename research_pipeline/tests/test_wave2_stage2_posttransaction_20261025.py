"""One-shot read-only validation of the applied Wave 2 Stage 2 amendment."""
import unittest
from pathlib import Path

from research_pipeline.engine.dependency_consolidation_readiness import assess, load_inputs
from research_pipeline.engine.dependency_global_audit import load_live_snapshot

class Stage2AppliedVerification(unittest.TestCase):
    def test_live_edges_and_exhaustive_readiness(self):
        root = Path(__file__).resolve().parents[2]
        w = root / "research_pipeline/experiments/reconstruction-v2-independent"
        first = load_live_snapshot(w)
        s = first["state"]["summary"]
        assert s["scan_amendment_event_count"] == 773
        assert s["unresolved_missing_candidates"] == 420
        assert s["scan_complete"] == 659
        assert not s["consolidation_gate_valid"]
        assert s["phase"] == "consolidate_occurrences"

        ext = first["nodes"]["form.788671763be693df.ext-group"]
        extrefs = ext["references"]
        self.assertEqual(ext["version_sha256"],
                         "fa8adfb0f893348f71089e3e7327faa0ae57fc2e627f3e52e7be3e1218fbbd27")
        self.assertFalse(any(x.get("target_meaning_id") ==
                             "meaning.3a0545450d7a5285.internal-hom-module"
                             for x in extrefs))
        matching = [x for x in extrefs if x.get("target_meaning_id") ==
                    "meaning.wave2.cross110.module-linear"]
        self.assertEqual(len(matching), 1)
        self.assertIn("component prerequisite", matching[0]["context"])
        self.assertEqual({x["missing_candidate_id"] for x in extrefs
                          if x["state"] == "missing"},
                         {"missing.3093c306593220970d2c",
                          "missing.1bd554e6f230b14c5f9b"})

        local = first["nodes"]["form.ab260940ea9c523d.locally-connected-space"]
        localrefs = local["references"]
        self.assertEqual(local["version_sha256"],
                         "67e0cc00105f0276659d7efd0cc39e3d62cf9ba7595d895939a9ba62079f33cb")
        self.assertFalse(any(x.get("target_meaning_id") ==
                             "meaning.6a3376e5ecb82bfb.topology-basis" for x in localrefs))
        fixed = [x for x in localrefs if x["phrase"] == "neighborhood basis"]
        self.assertEqual(len(fixed), 1)
        self.assertEqual(fixed[0]["state"], "external")
        self.assertEqual({x["missing_candidate_id"] for x in localrefs
                          if x["state"] == "missing"},
                         {"missing.eb8e1a62d06acf7c487c"})

        out = assess(load_inputs(w), exhaustive=True)
        checks = out["mechanical_checks"]
        self.assertEqual(len(checks), 19)
        self.assertTrue(all(checks.values()), checks)
        self.assertEqual(out["status"], "mechanical_checks_passed_review_decision_required")
        self.assertFalse(out["pass3_authorized_by_this_assessment"])
        self.assertEqual(out["mathematical_consistency_review"]["summary"]
                         ["mechanical_integrity_count"], 0)
        after = load_live_snapshot(w)
        self.assertEqual(first["inventory"], after["inventory"])
        self.assertEqual(first["state"], after["state"])
        self.assertEqual(first["nodes"], after["nodes"])
        print("STAGE2_POSTCHECK_ALL_19_PASSED")
        print("STAGE2_POSTCHECK_LEADS",
              out["mathematical_consistency_review"]["summary"]["total_review_candidates"])
