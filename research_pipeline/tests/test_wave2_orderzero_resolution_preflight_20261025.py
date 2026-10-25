"""One-shot source-anchored resolution trial. Never submits to live inbox."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from research_pipeline.engine.core import digest
from research_pipeline.engine.dependency_graph import (
    apply_inbox, graph_path, meaning_version, read,
)

class SLinearOrderZeroResolution(unittest.TestCase):
    def test_disposable_real_graph_replay(self):
        repo = Path(__file__).resolve().parents[2]
        workspace = repo / "research_pipeline/experiments/reconstruction-v2-independent"
        live_graph = graph_path(workspace)
        inventory = read(live_graph / "INVENTORY.json")
        state = read(live_graph / "STATE.json")["summary"]
        self.assertEqual(state["unresolved_missing_candidates"], 420)
        self.assertEqual(state["scan_amendment_event_count"], 773)
        self.assertFalse(state["consolidation_gate_valid"])
        target = "meaning.wave2.cross110.module-linear"
        candidate = "missing.f9304694577e53d812c1"
        source = inventory["formulations"]["form.a81a0fbec29f2186.finite-order-differential-operator"]
        self.assertEqual(source["version_sha256"],
                         "ee0ba0c53bc6f2a9a0b4b138ef37f6ae28530ccd1a66c12d473aae9864f781c1")
        self.assertIn("D is S-linear", source["text"])
        target_form = inventory["formulations"]["form.wave2.cross110.module-linear"]
        self.assertIn("Let R be an associative ring", target_form["text"])
        candidates = [json.loads(s) for s in
                      (live_graph / "missing_candidates.jsonl").read_text().splitlines()
                      if s.strip()]
        found = [row for row in candidates if row["id"] == candidate]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["status"], "unresearched")
        self.assertEqual(found[0]["incoming_formulation_ids"],
                         ["form.a81a0fbec29f2186.finite-order-differential-operator"])
        packet = {
            "schema_version": 1,
            "id": "resolve.wave2.orderzero-s-linear-20261025-001",
            "mode": "resolve",
            "research_scope": "Source-free reviewed prerequisite identification, independent graph only; no source changes or gate transition.",
            "resolutions": [{
                "missing_candidate_id": candidate,
                "target_meaning_id": target,
                "target_version_sha256": meaning_version(inventory, target),
                "reviewed_by": "assistant-source-free-contextual-mathematics-review",
                "review_rationale": (
                    "The order-at-most-zero clause in the full independent differential-operator "
                    "source specifies that D:M to N is S-linear for the S-modules M and N "
                    "over the ring map R to S. The independent generic module-linear map "
                    "definition over an associative ring states additive preservation and "
                    "scalar compatibility; instantiate its ring variable as S. This "
                    "identifies only the order-zero component predicate, not the "
                    "recursive commutator clause for k>0, and does not equate "
                    "R-linearity with S-linearity. Preserve the source's other "
                    "dependencies and all ring/module unit and action conventions."
                )
            }]
        }
        with tempfile.TemporaryDirectory(prefix="wave2-resolve-trial-") as tmp:
            simulated = Path(tmp) / "workspace"
            target_graph = graph_path(simulated)
            shutil.copytree(live_graph, target_graph)
            f = target_graph / "inbox" / (packet["id"] + ".json")
            self.assertFalse(f.exists())
            f.write_text(json.dumps(packet, ensure_ascii=False, indent=2)+"\n")
            outcome = apply_inbox(simulated, limit=20)
            self.assertEqual(outcome["applied"], [packet["id"]])
            receipt = read(target_graph / "applied" / f.name)
            self.assertEqual(receipt["sha256"], digest(packet))
            self.assertEqual(receipt["mode"], "resolve")
            after = read(target_graph / "STATE.json")["summary"]
            self.assertEqual(after["unresolved_missing_candidates"], 419)
            self.assertEqual(after["scan_amendment_event_count"], 773)
            self.assertFalse(after["consolidation_gate_valid"])
            self.assertEqual(after["phase"], "consolidate_occurrences")
            occurrences = [json.loads(s) for s in
                           (target_graph / "occurrences.jsonl").read_text().splitlines()
                           if s.strip()]
            linked = [r for r in occurrences
                      if r.get("resolved_missing_candidate_id") == candidate]
            self.assertEqual(len(linked), 1)
            self.assertEqual(linked[0]["target_meaning_id"], target)
            self.assertEqual(linked[0]["state"], "existing")
        self.assertEqual(read(live_graph / "STATE.json")["summary"], state)
        self.assertFalse((live_graph / "applied" / (packet["id"]+".json")).exists())
        print("WAVE2_RESOLUTION_PACKET="+json.dumps(packet,sort_keys=True,ensure_ascii=False))
        print("WAVE2_RESOLUTION_SHA256="+digest(packet))
        print("WAVE2_RESOLUTION_TRIAL=applied_only_in_temp_graph")
