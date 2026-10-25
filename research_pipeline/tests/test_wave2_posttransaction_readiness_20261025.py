"""Ephemeral, read-only post-transaction verification (remove after archived).
Runs the actual exhaustive gate readiness against the current main workspace.
"""
from pathlib import Path
import json
import unittest

from research_pipeline.engine.dependency_global_audit import load_live_snapshot, analyze_snapshot
from research_pipeline.engine.dependency_consolidation_readiness import load_inputs, assess
from research_pipeline.engine.dependency_consistency_worklist import build_worklist

ROOT = Path(__file__).resolve().parents[2]
W = ROOT / "research_pipeline/experiments/reconstruction-v2-independent"

class ReconciliationReadinessTest(unittest.TestCase):
    def test_two_reviewed_transactions_and_full_readiness(self):
        graph = W / "dependency_graph"
        snap = load_live_snapshot(W)
        state = snap["state"]["summary"]
        self.assertEqual(state["unresolved_missing_candidates"], 420)
        self.assertEqual(state["alias_candidate_records"], 301)
        self.assertEqual(state["scan_amendment_event_count"], 771)
        self.assertFalse(state["consolidation_gate_valid"])
        self.assertEqual(state["phase"], "consolidate_occurrences")
        node = snap["nodes"]["form.wave2.found85.adapted-continuous"]
        refs = node["references"]
        self.assertEqual(len(refs), 6)
        self.assertEqual(refs[1]["state"], "external")
        self.assertNotIn("target_meaning_id", refs[1])
        self.assertEqual(refs[3]["state"], "missing")
        self.assertEqual(refs[3]["missing_candidate_id"], "missing.65d334caa51c845ea335")
        for ident, mode in [
            ("alias.chat-postcoverage.20261025.shifted-operator", "alias"),
            ("chat-postcoverage-realtime-filtration-edge-20261025-001", "amend"),
        ]:
            receipt = json.loads((graph / "applied" / (ident + ".json")).read_text())
            self.assertEqual(receipt["status"], "applied_in_independent_graph_only")
            self.assertEqual(receipt["mode"], mode)
        audit = analyze_snapshot(snap)
        self.assertEqual(audit["summary"]["cycle_components"], 0)
        self.assertFalse(any(f["severity"]=="integrity" for f in audit["flags"]))
        self.assertFalse(any(
            e.get("from_formulation")=="form.wave2.found85.adapted-continuous"
            and e.get("target_meaning_id")=="meaning.wave2.found85.discrete-filtration"
            for e in audit.get("effective_existing_edges", [])
        ))
        readiness = assess(load_inputs(W), exhaustive=True)
        self.assertEqual(readiness["status"], "mechanical_checks_passed_review_decision_required")
        self.assertEqual(len(readiness["mechanical_checks"]), 19)
        self.assertTrue(all(readiness["mechanical_checks"].values()))
        self.assertFalse(readiness["pass3_authorized_by_this_assessment"])
        consistent = build_worklist(snap, exhaustive=True)
        self.assertFalse(consistent["mathematics_certified"])
        self.assertEqual(consistent["summary"]["mechanical_integrity_count"], 0)
        print("POSTTRANSACTION_RECONCILIATION_READINESS_JSON=" + json.dumps({
            "status": readiness["status"],
            "mechanical_checks_passed": sum(readiness["mechanical_checks"].values()),
            "canonical_unresolved": state["unresolved_missing_candidates"],
            "aliases": state["alias_candidate_records"],
            "amendments": state["scan_amendment_event_count"],
            "global_review_leads": audit["summary"]["total_flags"],
            "consistency_review_leads": consistent["summary"]["total_review_candidates"],
            "gate_open": state["consolidation_gate_valid"],
        }, sort_keys=True))
