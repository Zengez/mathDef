"""Temporary read-only CI preflights for the two staged Wave 2 proposals.

This file executes only the offline graph preparer and preflight. It neither
places a packet in the active graph inbox nor mutates the protected workspace.
Remove this temporary CI probe after archiving its result in the audit record.
"""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from research_pipeline.engine.dependency_global_audit import (
    load_live_snapshot,
    write_offline_packets,
)
from research_pipeline.engine.dependency_review_preflight import review_preflight


REPO = Path(__file__).resolve().parents[2]
WORKSPACE = REPO / "research_pipeline/experiments/reconstruction-v2-independent"
AUDIT = REPO / "research_pipeline/reviews/canonical-identity-2026-10-24"
STAGE = AUDIT / "staged-not-applied"
FILTRATION_ID = "form.wave2.found85.adapted-continuous"
BAD_REF = "occ.4dc2044654482ca4b966"
GOOD_REF = "occ.3cee100f060f105c219b"


class TestStagedWave2OfflinePreflight(unittest.TestCase):
    def test_filtration_replacement_prepares_and_passes_engine_preflight(self):
        manifest_path = STAGE / "filtration_prepare_manifest.json"
        before = load_live_snapshot(WORKSPACE)
        node = before["nodes"][FILTRATION_ID]
        original_refs = node["references"]
        original_text = before["inventory"]["formulations"][FILTRATION_ID]["text"]
        self.assertEqual(len(original_refs), 7)
        self.assertTrue(any(
            x["occurrence_id"] == GOOD_REF
            and x["state"] == "missing"
            and x["missing_candidate_id"] == "missing.65d334caa51c845ea335"
            for x in original_refs
        ))
        self.assertTrue(any(
            x["occurrence_id"] == BAD_REF
            and x["state"] == "existing"
            and x["target_meaning_id"] == "meaning.wave2.found85.discrete-filtration"
            for x in original_refs
        ))

        with tempfile.TemporaryDirectory(prefix="mathdef-stage1-offline-") as folder:
            result = write_offline_packets(
                WORKSPACE, manifest_path, Path(folder), max_per_batch=5
            )
            self.assertEqual(result["status"], "offline_review_packets_prepared_not_committed")
            self.assertTrue(result["read_only_graph"])
            self.assertEqual(result["packet_count"], 1)
            self.assertEqual(result["changed_formulation_count"], 1)
            self.assertEqual(len(result["preflight"]), 1)
            self.assertEqual(result["preflight"][0]["status"], "mechanically_valid_not_applied")

            generated = json.loads(Path(result["files"][0]).read_text())
            self.assertEqual(generated["mode"], "amend")
            self.assertEqual(len(generated["amendments"]), 1)
            amendment = generated["amendments"][0]
            self.assertEqual(amendment["formulation_id"], FILTRATION_ID)
            self.assertEqual(len(amendment["references"]), len(original_refs))
            for index, (old, new) in enumerate(zip(original_refs, amendment["references"])):
                if old["occurrence_id"] == BAD_REF:
                    self.assertEqual(new["state"], "external")
                    self.assertNotIn("target_meaning_id", new)
                    self.assertIn("discrete-filtration", new["disposition"])
                else:
                    self.assertEqual(
                        new,
                        {k: v for k, v in old.items() if k != "occurrence_id"},
                        f"Unchanged reference {index} lost metadata",
                    )

            print("STAGE1 FILTRATION ENGINE PREPARE AND PREFLIGHT PASSED:", json.dumps({
                "status": result["status"],
                "batch_id": result["preflight"][0]["batch_id"],
                "checked_events": result["preflight"][0]["checked_events"],
                "changed_formulation": FILTRATION_ID,
                "references_preserved": len(original_refs) - 1,
                "real_time_missing_preserved": GOOD_REF,
            }, sort_keys=True))

        after = load_live_snapshot(WORKSPACE)
        self.assertEqual(
            after["inventory"]["formulations"][FILTRATION_ID]["text"], original_text
        )
        self.assertEqual(after["nodes"][FILTRATION_ID], node)
        self.assertEqual(
            after["state"]["summary"]["unresolved_fingerprint"],
            before["state"]["summary"]["unresolved_fingerprint"],
        )

    def test_shifted_operator_alias_packet_passes_engine_preflight(self):
        path = STAGE / "alias.chat-postcoverage.20261025.shifted-operator.json"
        result = review_preflight(WORKSPACE, path)
        self.assertEqual(result["status"], "mechanically_valid_not_applied")
        self.assertTrue(result["read_only"])
        self.assertFalse(result["mathematical_certification"])
        self.assertEqual(result["checked_events"], 1)
        self.assertEqual(result["mode"], "alias")
        self.assertFalse(result["new_candidate_preview"])
        print("STAGE1 SHIFTED OPERATOR ALIAS ENGINE PREFLIGHT PASSED:", json.dumps({
            "status": result["status"],
            "batch_id": result["batch_id"],
            "checked_events": result["checked_events"],
            "package_sha256": result["package_sha256"],
        }, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
