"""Guarded independent Wave2 consolidation transitions.

This module is an operational phase control, NOT mathematical certification.
It may seal the isolated dependency graph only for a configured, explicitly
owner-approved review policy and a mechanically clean, version-pinned state.
Never imports production or frozen reconstruction materials.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import PipelineError
from .dependency_graph import graph_path, read, seal_consolidation, digest

MIN_RATIONALE = 40


def _pending_inbox(graph: Path):
    """A gate must not be sealed ahead of unapplied classification events."""
    pending = []
    for packet in sorted((graph / "inbox").glob("*.json")):
        entry = read(packet)
        receipt = read(graph / "applied" / packet.name)
        if (not receipt or receipt.get("sha256") != digest(entry)
                or receipt.get("mode") != entry.get("mode")):
            pending.append(packet.name)
    return pending


def evaluate(workspace: Path, policy_file: Path):
    """Check eligibility without writing or rebuilding anything."""
    root = Path(workspace)
    graph = graph_path(root)
    policy = read(policy_file)
    state = read(graph / "STATE.json", {}).get("summary", {})
    inventory = read(graph / "INVENTORY.json", {})
    if policy.get("schema_version") != 1 or policy.get("enabled") is not True:
        raise PipelineError("Missing or disabled owner-approved gate policy")
    if not policy.get("owner_approved_standing_routine"):
        raise PipelineError("Routine gate transitions lack owner approval")
    if not state or not inventory:
        raise PipelineError("Missing independent graph state/inventory")
    if state.get("inventory_sha256") != inventory.get("source_inventory_sha256"):
        raise PipelineError("Stale graph state relative to inventory")
    if state.get("consolidation_gate_valid"):
        return {"status": "already_valid", "gate_valid": True, "event": None,
                "phase": state.get("phase"), "pending_inbox": []}
    pending = _pending_inbox(graph)
    if (state.get("scan_complete") != state.get("total_formulations")
            or state.get("scan_incomplete") or state.get("unscanned")
            or state.get("ambiguous_occurrences") or state.get("unassigned_occurrences")
            or pending):
        return {"status": "waiting_for_complete_classification",
                "gate_valid": False, "phase": state.get("phase"),
                "pending_inbox": pending, "event": None}

    # A human reviewer can place a blocking flag here for a substantive issue.
    holds = read(root / "generation_staging" / "GATE_HOLDS.json", {})
    if holds.get("block_gate") is True:
        return {"status": "review_hold", "gate_valid": False,
                "phase": state.get("phase"), "event": None,
                "reason": holds.get("reason", "")}

    first = policy.get("initial_reviewed_gate", {})
    initial_match = (
        first.get("inventory_sha256") == state["inventory_sha256"]
        and first.get("unresolved_fingerprint") == state["unresolved_fingerprint"]
    )
    if initial_match:
        event = dict(first)
        provenance = "explicitly_reviewed_initial_gate"
    else:
        prior = read(graph / "CONSOLIDATION.json", {})
        # Never use the standing rule as a substitute for the first reviewed gate.
        if not prior or not policy.get("subsequent_routine_gates_enabled", False):
            return {"status": "requires_reviewed_initial_gate",
                    "gate_valid": False, "event": None}
        completed = read(root / "generation_staging" / "INTEGRATION_RECEIPT.json", {})
        if (completed.get("status") != "integration_complete"
                or completed.get("prior_gate_inventory_sha256") !=
                prior.get("inventory_sha256")
                or completed.get("prior_gate_unresolved_fingerprint") !=
                prior.get("unresolved_fingerprint")
                or completed.get("global_mathematical_audit") != "completed"
                or completed.get("source_verification_review") != "completed"
                or not str(completed.get("reviewed_by", "")).strip()
                or len(str(completed.get("review_rationale", "")).strip()) < 40):
            return {"status": "prior_generation_not_integrated",
                    "gate_valid": False, "event": None}
        from .dependency_generation import status as generation_status
        try:
            previous_generation = generation_status(root)
        except (PipelineError, KeyError, ValueError):
            return {"status": "prior_generation_not_integrated",
                    "gate_valid": False, "event": None}
        if not previous_generation["ready_for_reviewed_integration"]:
            return {"status": "prior_generation_not_integrated",
                    "gate_valid": False, "event": None}
        event = {
            "schema_version": 1,
            "inventory_sha256": state["inventory_sha256"],
            "unresolved_fingerprint": state["unresolved_fingerprint"],
            "reviewed_by": "owner-approved standing routine gate policy (not source certification)",
            "rationale": (
                "Following completed first-generation staging and separately "
                "attested integration, all newly inventoried independent "
                "formulations have full classified scans, with zero ambiguous "
                "or unassigned occurrences and no pending graph inbox packets. "
                "This is a mechanical research-phase transition under the "
                "standing owner policy, not a mathematical equivalence finding, "
                "source certificate, release approval or production import."
            ),
        }
        provenance = "owner_approved_subsequent_routine_gate"
    if (event.get("schema_version") != 1 or
            not str(event.get("reviewed_by", "")).strip() or
            len(str(event.get("rationale", "")).strip()) < MIN_RATIONALE):
        raise PipelineError("Insufficient gate review metadata")
    return {"status": "ready", "gate_valid": False, "event": event,
            "provenance": provenance, "phase": state.get("phase"),
            "pending_inbox": []}


def run(workspace: Path, policy_file: Path, apply=False):
    result = evaluate(workspace, policy_file)
    if not apply or result["status"] != "ready":
        return result
    state = seal_consolidation(workspace, result["event"])
    if not state["consolidation_gate_valid"]:
        raise PipelineError("Graph did not acknowledge reviewed consolidation gate")
    return {"status": "sealed", "gate_valid": True,
            "phase": state["phase"], "provenance": result["provenance"],
            "inventory_sha256": state["inventory_sha256"],
            "unresolved_fingerprint": state["unresolved_fingerprint"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--apply", action="store_true",
                        help="Seal only if the reviewed phase checks pass")
    args = parser.parse_args()
    print(json.dumps(run(args.workspace, args.policy, args.apply), indent=2))


if __name__ == "__main__":
    main()
