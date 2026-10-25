"""One-shot independent postapplication verification of m-primary resolution."""
import json
from pathlib import Path
import unittest

from research_pipeline.engine.core import digest
from research_pipeline.engine.dependency_consolidation_readiness import assess, load_inputs
from research_pipeline.engine.dependency_global_audit import load_live_snapshot
from research_pipeline.engine.dependency_graph import graph_path, read

class AppliedMPrimaryVerification(unittest.TestCase):
    def test_receipts_active_graph_provenance_and_all_nineteen_checks(self):
        root = Path(__file__).resolve().parents[2]
        workspace = root / "research_pipeline/experiments/reconstruction-v2-independent"
        snap = load_live_snapshot(workspace)
        summary = snap["state"]["summary"]
        self.assertEqual(summary["scan_complete"], 659)
        self.assertEqual(summary["unresolved_missing_candidates"], 418)
        self.assertEqual(summary["missing_occurrences"], 841)
        self.assertEqual(summary["missing_candidates"], 727)
        self.assertEqual(summary["alias_candidate_records"], 300)
        self.assertEqual(summary["scan_amendment_event_count"], 775)
        self.assertEqual(summary["unresolved_fingerprint"],
                         "7b69e2fdcb30a4536883df44308d386219b7621533886d65276b8992959f4773")
        self.assertFalse(summary["consolidation_gate_valid"])
        self.assertEqual(summary["phase"], "consolidate_occurrences")
        graph = graph_path(workspace)
        digests = {
            "amend-mprimary-selfreference-20261025-001":
                "8c9ba8c6e6b67c397c08c6950c5a0b998106ea892643b87a4e052bf80d677da4",
            "resolve-wave2-mprimary-noetherianlocal-20261025-001":
                "a6e41ea7f038971cdb00fa40487da2054820f864b3ddf963658f7e435e258eef",
        }
        for packet_id, expected_sha in digests.items():
            receipt = read(graph / "applied" / (packet_id+".json"))
            packet = read(graph / "inbox" / (packet_id+".json"))
            self.assertEqual(receipt["sha256"], expected_sha)
            self.assertEqual(receipt["status"], "applied_in_independent_graph_only")
            self.assertEqual(digest(packet), expected_sha)
        mid = "meaning.b9defeff446a0526.ideal-of-definition-local-ring"
        candidate = "missing.b963edbe734f35266d3a"
        defid = "form.b9defeff446a0526.ideal-of-definition-local-ring"
        systemid = "form.22c049b8eee93897.system-of-parameters"
        own_refs = snap["nodes"][defid]["references"]
        self.assertFalse(any(x.get("target_meaning_id") == mid for x in own_refs))
        self.assertFalse(any(x.get("missing_candidate_id") == candidate for x in own_refs))
        own = [x for x in own_refs if x.get("phrase") == "m-primary ideal"]
        self.assertEqual(len(own), 1)
        self.assertEqual(own[0]["state"], "external")
        self.assertIn("equivalent", own[0]["disposition"])
        original = read(graph / "nodes" / (defid+".json"))
        self.assertEqual(original["references"][4]["phrase"], "m-primary ideal")
        self.assertEqual(original["references"][4]["state"], "unassigned")
        entries = snap["nodes"][systemid]["references"]
        marked = [r for r in entries if r.get("missing_candidate_id") == candidate]
        self.assertEqual(len(marked), 1)
        self.assertEqual(marked[0]["reviewed_existing_candidate_id"], candidate)
        current_candidate = next(c for c in snap["candidates"] if c["id"] == candidate)
        self.assertEqual(current_candidate["status"], "resolved")
        self.assertEqual(current_candidate["resolved_target_meaning_id"], mid)
        self.assertEqual(current_candidate["incoming_formulation_ids"], [systemid])
        self.assertTrue(any(x.get("alias_candidate_id") == "missing.2a4c23153be5ee32b75f"
                            and x.get("canonical_candidate_id") == candidate
                            for x in snap["aliases"]))
        rows = [json.loads(line) for line in
                (graph/"occurrences.jsonl").read_text().splitlines() if line.strip()]
        linked = [r for r in rows if r["from_formulation"] == systemid
                  and r.get("resolved_missing_candidate_id") == candidate]
        self.assertEqual(len(linked), 1)
        self.assertEqual(linked[0]["state"], "existing")
        self.assertEqual(linked[0]["target_meaning_id"], mid)
        report = assess(load_inputs(workspace), exhaustive=True)
        checks = report["mechanical_checks"]
        self.assertEqual(len(checks), 19)
        self.assertTrue(all(checks.values()), checks)
        self.assertEqual(report["status"],
                         "mechanical_checks_passed_review_decision_required")
        self.assertFalse(report["pass3_authorized_by_this_assessment"])
        self.assertFalse(report["gate_contract"]["existing_record_present"])
        self.assertEqual(report["mathematical_consistency_review"]["summary"]
                         ["mechanical_integrity_count"], 0)
        after = load_live_snapshot(workspace)
        self.assertEqual(snap["state"], after["state"])
        self.assertEqual(snap["nodes"], after["nodes"])
        print("MPRIMARY_LIVE_POSTCHECK_19_OF_19_PASS")
        print("MPRIMARY_LIVE_POSTCHECK_CONSISTENCY_LEADS",
              report["mathematical_consistency_review"]["summary"]
              ["total_review_candidates"])
        print("MPRIMARY_LIVE_POSTCHECK_UNRESOLVED", summary["unresolved_missing_candidates"])
