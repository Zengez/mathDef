"""Source-free prospective m-primary self-reference remediation; trial only.

Executes actual amendment-preflight and immutable receipt dispatcher on a
disposable copy of the complete independent Wave 2 workspace. No live writes.
"""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from research_pipeline.engine.core import digest
from research_pipeline.engine.dependency_global_audit import (
    load_live_snapshot, build_review_packages,
)
from research_pipeline.engine.dependency_review_preflight import review_preflight
from research_pipeline.engine.dependency_graph import (
    apply_inbox, graph_path, meaning_version, read,
)
from research_pipeline.engine.dependency_consolidation_readiness import assess, load_inputs


class MPrimaryResolutionTrial(unittest.TestCase):
    def test_version_bound_self_reference_remediation_and_resolution(self):
        repo = Path(__file__).resolve().parents[2]
        live = repo / "research_pipeline/experiments/reconstruction-v2-independent"
        snapshot = load_live_snapshot(live)
        inv = snapshot["inventory"]
        fid = "form.b9defeff446a0526.ideal-of-definition-local-ring"
        other = "form.22c049b8eee93897.system-of-parameters"
        candidate = "missing.b963edbe734f35266d3a"
        mid = "meaning.b9defeff446a0526.ideal-of-definition-local-ring"
        old = snapshot["nodes"][fid]
        self.assertEqual(snapshot["state"]["summary"]["unresolved_missing_candidates"], 419)
        self.assertEqual(snapshot["state"]["summary"]["scan_amendment_event_count"], 773)
        self.assertFalse(snapshot["state"]["summary"]["consolidation_gate_valid"])
        self.assertEqual(digest(old),
                         "da684fcc2a24f8c8ce41274f04317b7f8ffb50a44e99c2c4c9c0db47b89a22a7")
        target = inv["formulations"][fid]
        source = inv["formulations"][other]
        self.assertIn("Noetherian local ring", target["text"])
        self.assertIn("radical is the maximal ideal m", target["text"])
        self.assertIn("equivalently I is m-primary", target["text"])
        self.assertIn("whose generated ideal is m-primary", source["text"])
        self.assertEqual(inv["formulations"][fid]["version_sha256"],
                         "3fb9913ad250771266c5b4cc520056fed2ce4032b1659f4afab34ee40a408a50")
        affected = [ref for ref in old["references"]
                    if ref.get("missing_candidate_id") == candidate]
        self.assertEqual(len(affected), 1)
        self.assertEqual(affected[0]["occurrence_id"],
                         "occ.a4b38514f6ebe94712d0")
        system = snapshot["nodes"][other]
        self.assertTrue(any(ref.get("target_meaning_id") == mid for ref in system["references"]))
        self.assertTrue(any(ref.get("missing_candidate_id") == candidate
                            for ref in system["references"]))
        manifest = {
            "schema_version": 1,
            "id": "amend-mprimary-selfreference-20261025",
            "inventory_sha256": inv["source_inventory_sha256"],
            "unresolved_fingerprint": snapshot["state"]["summary"]["unresolved_fingerprint"],
            "reviewed_by": "assistant-contextual-mathematical-review",
            "review_rationale": (
                "Entire locally Noetherian definition and current effective reference "
                "list reviewed. The source itself defines ideal of definition by "
                "radical(I)=m and states an equivalent m-primary characterization; "
                "that equivalent restatement must not be a dependency of the "
                "definition on itself. The independent system-of-parameters usage "
                "retains the real missing prerequisite and direct ideal-of-definition "
                "reference. All source formulations and unrelated links unchanged."
            ),
            "changes": [{
                "formulation_id": fid,
                "expected_node_sha256": digest(old),
                "expected_occurrence_id": affected[0]["occurrence_id"],
                "reason": (
                    "Within a commutative unital local ring (R,m), an ideal "
                    "with radical m is m-primary: if ab is in I and a is not "
                    "in I, b outside m would be a unit and force a in I; hence "
                    "b is in radical I. Therefore the target's own phrase "
                    "'equivalently I is m-primary' is an equivalent "
                    "characterization already supplied in the parent source, "
                    "not a separate missing prerequisite. Retire only the "
                    "self-defining missing edge while preserving its historical "
                    "phrase and the external equivalence justification."
                ),
                "replacement": {
                    "phrase": "m-primary ideal",
                    "state": "external",
                    "disposition": (
                        "This phrase is the source definition's equivalent "
                        "m-primary characterization of radical(I)=m in a "
                        "commutative unital Noetherian local ring. Retain "
                        "as explicit provenance/explanatory equivalence, not "
                        "a self-referential missing prerequisite. The separate "
                        "system-of-parameters source still uses the candidate."
                    ),
                },
            }],
        }
        packet_list = build_review_packages(snapshot, manifest)
        self.assertEqual(len(packet_list), 1)
        amend = packet_list[0]
        self.assertEqual(amend["id"], "amend-mprimary-selfreference-20261025-001")
        self.assertEqual(len(amend["amendments"]), 1)
        resolution = {
            "schema_version": 1,
            "id": "resolve-wave2-mprimary-noetherianlocal-20261025-001",
            "mode": "resolve",
            "research_scope": (
                "Existing-meaning resolution after self-reference removal; "
                "specific commutative unital Noetherian local ring context."
            ),
            "resolutions": [{
                "missing_candidate_id": candidate,
                "target_meaning_id": mid,
                "target_version_sha256": meaning_version(inv, mid),
                "reviewed_by": "assistant-contextual-mathematical-review",
                "review_rationale": (
                    "The sole remaining m-primary candidate is the ideal "
                    "condition used by a system of parameters in a Noetherian "
                    "local ring. Its generated ideal I is m-primary exactly "
                    "when radical(I)=m. The existing ideal-of-definition "
                    "formulation defines this same predicate in that context; "
                    "the radical criterion gives a noncircular definition, "
                    "after its own redundant candidate reference has been "
                    "retired with provenance intact. Distinct concepts of "
                    "system of parameters and selecting dimension-many "
                    "generators are preserved without being identified."
                )
            }]
        }
        with tempfile.TemporaryDirectory(prefix="wave2-mprimary-trial-") as temporary:
            trial = Path(temporary) / "workspace"
            shutil.copytree(live, trial)
            graph = graph_path(trial)
            trial_amend = graph / "inbox" / (amend["id"] + ".json")
            trial_amend.write_text(json.dumps(amend, indent=2, ensure_ascii=False)+"\n")
            pre = review_preflight(trial, trial_amend)
            self.assertEqual(pre["status"], "mechanically_valid_not_applied")
            self.assertEqual(pre["checked_events"], 1)
            trial_resolve = graph / "inbox" / (resolution["id"] + ".json")
            trial_resolve.write_text(json.dumps(resolution, indent=2, ensure_ascii=False)+"\n")
            applied = apply_inbox(trial, limit=20)
            self.assertEqual(applied["applied"], [amend["id"], resolution["id"]])
            for packet in (amend, resolution):
                receipt = read(graph / "applied" / (packet["id"]+".json"))
                self.assertEqual(receipt["sha256"], digest(packet))
                self.assertEqual(receipt["status"], "applied_in_independent_graph_only")
            status = read(graph / "STATE.json")["summary"]
            self.assertEqual(status["unresolved_missing_candidates"], 418)
            self.assertEqual(status["missing_occurrences"], 841)
            self.assertEqual(status["scan_amendment_event_count"], 774)
            self.assertFalse(status["consolidation_gate_valid"])
            new_snap = load_live_snapshot(trial)
            target_refs = new_snap["nodes"][fid]["references"]
            self.assertFalse(any(r.get("target_meaning_id") == mid for r in target_refs))
            self.assertFalse(any(r.get("missing_candidate_id") == candidate for r in target_refs))
            self.assertEqual(len([r for r in target_refs if r["phrase"] == "m-primary ideal"]), 1)
            self.assertEqual(next(r for r in target_refs if r["phrase"] == "m-primary ideal")["state"],"external")
            effective = [json.loads(line) for line in
                         (graph/"occurrences.jsonl").read_text().splitlines()
                         if line.strip()]
            source_refs = [r for r in effective
                           if r["from_formulation"] == other
                           and r.get("resolved_missing_candidate_id") == candidate]
            self.assertEqual(len(source_refs), 1)
            self.assertEqual(source_refs[0]["target_meaning_id"], mid)
            # Verify on an actual complete workspace and its records.
            report = assess(load_inputs(trial), exhaustive=True)
            checks = report["mechanical_checks"]
            self.assertEqual(len(checks), 19)
            self.assertTrue(all(checks.values()), checks)
            self.assertFalse(report["pass3_authorized_by_this_assessment"])
            self.assertEqual(report["status"],
                             "mechanical_checks_passed_review_decision_required")
            print("MPRIMARY_TRIAL_19_CHECKS_PASSED")
            print("MPRIMARY_TRIAL_RESULT", status["unresolved_missing_candidates"],
                  status["missing_occurrences"], status["scan_amendment_event_count"])
        # Neither package was submitted to the real inbox.
        for packet in (amend, resolution):
            self.assertFalse((graph_path(live)/"inbox"/(packet["id"]+".json")).exists())
        again = load_live_snapshot(live)
        self.assertEqual(snapshot["nodes"], again["nodes"])
        self.assertEqual(snapshot["state"], again["state"])
        print("MPRIMARY_AMEND_PACKET="+json.dumps(amend,sort_keys=True,ensure_ascii=False))
        print("MPRIMARY_RESOLVE_PACKET="+json.dumps(resolution,sort_keys=True,ensure_ascii=False))
        print("MPRIMARY_AMEND_DIGEST="+digest(amend))
        print("MPRIMARY_RESOLVE_DIGEST="+digest(resolution))
