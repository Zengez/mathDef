"""One-time read-only preflight of the exact Stage 2 contextual corrections.

This test MUST remain on the isolated preparation branch only. Never leave a
stale, fixed-hash manifest test in recurring main tests after graph application.
"""
import json
import unittest
from pathlib import Path

from research_pipeline.engine.core import digest
from research_pipeline.engine.dependency_global_audit import (
    build_review_packages, load_live_snapshot,
)
from research_pipeline.engine.dependency_review_preflight import review_preflight
from research_pipeline.engine.dependency_graph import make_snapshot


class ReviewedStage2EdgePreflight(unittest.TestCase):
    def test_real_engine_manifest_with_complete_nodes_and_unmodified_other_references(self):
        root = Path(__file__).resolve().parents[2]
        w = root / "research_pipeline/experiments/reconstruction-v2-independent"
        manifest_path = (root / "research_pipeline/reviews/canonical-identity-2026-10-24/"
                         "stage2-preflight/reviewed-ext-hom-local-connectedness.json")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        snapshot = load_live_snapshot(w)
        before = snapshot["nodes"]
        pre_hash = {fid: digest(node) for fid, node in before.items()}
        packages = build_review_packages(snapshot, manifest)
        self.assertEqual(len(packages), 1)
        self.assertEqual(len(packages[0]["amendments"]), 2)
        adjustments = {a["formulation_id"]: a for a in packages[0]["amendments"]}
        self.assertEqual(set(adjustments), {
            "form.788671763be693df.ext-group",
            "form.ab260940ea9c523d.locally-connected-space",
        })
        change = {x["formulation_id"]: x for x in manifest["changes"]}
        expected = {
            "form.788671763be693df.ext-group": (
                "occ.321952d7b781466d1856",
                "meaning.wave2.cross110.module-linear"),
            "form.ab260940ea9c523d.locally-connected-space": (
                "occ.cdc96f16a3e31332ec7d", None),
        }
        for fid, (oid, target) in expected.items():
            prior = before[fid]
            prior_i = next(i for i, ref in enumerate(prior["references"])
                           if ref["occurrence_id"] == oid)
            # Before/after compare normalized complete original references.
            orig = [{k: v for k, v in r.items() if k != "occurrence_id"}
                    for r in prior["references"]]
            amend = adjustments[fid]
            updated = amend["references"]
            self.assertEqual(len(updated), len(orig))
            self.assertEqual(updated[:prior_i], orig[:prior_i])
            self.assertEqual(updated[prior_i+1:], orig[prior_i+1:])
            self.assertEqual(updated[prior_i]["target_meaning_id"]
                             if target else updated[prior_i].get("target_meaning_id"), target)
            self.assertEqual(amend["expected_node_sha256"], pre_hash[fid])
            self.assertEqual(amend["version_sha256"],
                             snapshot["inventory"]["formulations"][fid]["version_sha256"])
            missing_before = {r["missing_candidate_id"] for r in orig
                              if r["state"] == "missing"}
            missing_after = {r["missing_candidate_id"] for r in updated
                             if r["state"] == "missing"}
            self.assertEqual(missing_before, missing_after)
        self.assertEqual(adjustments["form.788671763be693df.ext-group"]["references"][2]["state"],
                         "existing")
        # End-to-end preflight, against live graph via the real repo engine.
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / (packages[0]["id"] + ".json")
            path.write_text(json.dumps(packages[0], ensure_ascii=False), encoding="utf-8")
            report = review_preflight(w, path)
            self.assertEqual(report["status"], "mechanically_valid_not_applied")
            self.assertEqual(report["checked_events"], 2)
            self.assertEqual(report["mode"], "amend")
            print("STAGE2_REVIEWED_PACKET_JSON="+json.dumps(packages[0],sort_keys=True,ensure_ascii=False))
            print("STAGE2_PREFLIGHT_REPORT="+json.dumps(report,sort_keys=True))
        after = load_live_snapshot(w)
        self.assertEqual(after["nodes"], before)
        self.assertEqual(after["state"], snapshot["state"])
        self.assertEqual(after["inventory"], snapshot["inventory"])
