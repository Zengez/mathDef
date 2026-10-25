"""One-off review-only full amendment packet export for independent Wave2.

Generate the reviewed amendment through the real package builder in the CI
checkout, engine-preflight it, then display its exact JSON for GitHub review.
No graph inbox writes, no permanent artifacts or source modifications.
"""
import json
import tempfile
import unittest
from pathlib import Path
from research_pipeline.engine.dependency_global_audit import write_offline_packets

HERE = Path(__file__).resolve().parents[2]
W = HERE / "research_pipeline/experiments/reconstruction-v2-independent"
P = (HERE / "research_pipeline/reviews/canonical-identity-2026-10-24"
     / "staged-not-applied/filtration_prepare_manifest.json")

class TestEmitReviewedAmendment(unittest.TestCase):
    def test_emit_preflighted_packet_once(self):
        with tempfile.TemporaryDirectory(prefix="mathdef-reviewed-offline-") as d:
            report = write_offline_packets(W, P, Path(d))
            self.assertEqual(report["packet_count"], 1)
            self.assertEqual(report["preflight"][0]["status"], "mechanically_valid_not_applied")
            batch = json.loads(Path(report["files"][0]).read_text())
            self.assertEqual(batch["mode"], "amend")
            self.assertEqual(len(batch["amendments"]), 1)
            amend = batch["amendments"][0]
            self.assertEqual(amend["formulation_id"], "form.wave2.found85.adapted-continuous")
            self.assertEqual(len(amend["references"]), 6)
            self.assertEqual(amend["references"][1]["state"], "external")
            self.assertNotIn("target_meaning_id", amend["references"][1])
            self.assertEqual(
                amend["references"][3]["missing_candidate_id"],
                "missing.65d334caa51c845ea335",
            )
            print("REVIEWED_PACKET_JSON="+json.dumps(batch, ensure_ascii=False, separators=(",",":")))
            print("REVIEWED_PACKET_PREFLIGHT="+json.dumps(report["preflight"][0], sort_keys=True))

if __name__=="__main__":
    unittest.main()
