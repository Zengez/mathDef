"""Read-only, receipt-backed decision status for independent reference graphs.

An audit proposal is *not* an applied graph change. This report consults the
current effective graph, committed inbox packets and immutable receipts to
show which decisions are actually applied. It never accepts a decision,
writes an inbox item, opens a phase gate, or edits source/review history.

Usage:
  python -m research_pipeline.engine.dependency_reconciliation_status \\
    --workspace research_pipeline/experiments/reconstruction-v2-independent \\
    --queue research_pipeline/reviews/canonical-identity-2026-10-24/LIVE_RECONCILIATION_QUEUE.json
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

from research_pipeline.engine.core import PipelineError, digest
from research_pipeline.engine.dependency_graph import KEY_RE, graph_path, meaning_version, read
from research_pipeline.engine.dependency_global_audit import load_live_snapshot

SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


def reconciliation_status(workspace: Path, queue: dict,
                          *, snapshot: dict | None = None) -> dict:
    """Evaluate version-anchored cases without altering review or graph files.

    A receipt counts as verified ONLY when its ID, mode and digest agree with
    the actual immutable inbox packet. Review cases are anchored to effective
    *live* node occurrence IDs, not seed-augmented evidence-array positions.
    """
    if not isinstance(queue, dict) or queue.get("schema_version") != 1:
        raise PipelineError("Reconciliation queue must use schema_version 1")
    cases = queue.get("cases")
    if not isinstance(cases, list) or not cases:
        raise PipelineError("Reconciliation queue requires a nonempty cases list")
    snapshot = snapshot if snapshot is not None else load_live_snapshot(workspace)
    summary = snapshot["state"]["summary"]
    inv = snapshot["inventory"]
    graph = graph_path(workspace)
    seen_case_ids = set()
    entries = []
    packets_by_case = {}
    for case in cases:
        if not isinstance(case, dict):
            raise PipelineError("Every reconciliation case must be an object")
        case_id, kind = case.get("id"), case.get("kind")
        if (not isinstance(case_id, str) or not KEY_RE.fullmatch(case_id)
                or case_id in seen_case_ids):
            raise PipelineError("Case ID must be unique and path-safe")
        seen_case_ids.add(case_id)
        row = {"id": case_id, "kind": kind, "status": None,
               "mathematically_certified": False}
        if kind == "transaction":
            packet_id, mode, expected_sha = (
                case.get("packet_id"), case.get("mode"),
                case.get("packet_sha256"))
            if (not isinstance(packet_id, str)
                    or not KEY_RE.fullmatch(packet_id)
                    or mode not in ("alias", "amend", "resolve")
                    or not isinstance(expected_sha, str)
                    or not SHA256_RE.fullmatch(expected_sha)):
                raise PipelineError("Transaction needs safe ID, mode and SHA256")
            inbox_path = graph / "inbox" / (packet_id + ".json")
            receipt_path = graph / "applied" / (packet_id + ".json")
            packet = read(inbox_path)
            receipt = read(receipt_path)
            if packet is not None and not isinstance(packet, dict):
                raise PipelineError("Inbox packet is not an object: " + packet_id)
            if receipt is not None and not isinstance(receipt, dict):
                raise PipelineError("Applied receipt is not an object: " + packet_id)
            packet_matches = bool(
                packet is not None
                and packet.get("id") == packet_id
                and packet.get("mode") == mode
                and digest(packet) == expected_sha)
            receipt_matches = bool(
                receipt is not None
                and receipt.get("id") == packet_id
                and receipt.get("mode") == mode
                and receipt.get("sha256") == expected_sha
                and receipt.get("status") == "applied_in_independent_graph_only")
            if receipt is not None:
                row["status"] = (
                    "applied_receipt_verified" if packet_matches and receipt_matches
                    else "receipt_or_packet_conflict")
            elif packet is not None:
                row["status"] = (
                    "submitted_awaiting_receipt" if packet_matches
                    else "inbox_packet_conflict")
            else:
                row["status"] = "not_submitted"
            packets_by_case[case_id] = packet
            row.update({
                "packet_id": packet_id, "mode": mode,
                "expected_packet_sha256": expected_sha,
                "inbox_packet_present": packet is not None,
                "receipt_present": receipt is not None,
                "inbox_digest_matches": packet_matches,
                "receipt_matches": receipt_matches,
            })
            if mode == "resolve" and packet_matches:
                decisions = packet.get("resolutions")
                if not isinstance(decisions, list) or any(not isinstance(d, dict) for d in decisions):
                    raise PipelineError("Resolution packet needs a resolutions list")
                registry = {c["id"]: c for c in snapshot.get("candidates", [])}
                effects = []
                for decision in decisions:
                    cid = decision.get("missing_candidate_id")
                    mid = decision.get("target_meaning_id")
                    version = decision.get("target_version_sha256")
                    if (not isinstance(cid, str) or not KEY_RE.fullmatch(cid)
                            or not isinstance(mid, str) or not KEY_RE.fullmatch(mid)
                            or not isinstance(version, str) or not SHA256_RE.fullmatch(version)):
                        raise PipelineError("Resolution needs candidate, target and version SHA256")
                    effects.append({
                        "missing_candidate_id": cid, "target_meaning_id": mid,
                        "recorded_target_version_sha256": version,
                        "target_version_matches_current_meaning": bool(
                            mid in inv.get("meanings", {})
                            and version == meaning_version(inv, mid)),
                        "registry_target_matches": bool(
                            cid in registry and registry[cid].get("resolved_target_meaning_id") == mid),
                        "resolution_ledger_matches": any(
                            event.get("missing_candidate_id") == cid
                            and event.get("target_meaning_id") == mid
                            and event.get("target_version_sha256") == version
                            for event in snapshot.get("resolutions", [])),
                    })
                row["current_resolution_effects"] = effects
        elif kind == "review":
            fid, occurrence_id, prior_hash = (
                case.get("formulation_id"),
                case.get("expected_occurrence_id"),
                case.get("expected_node_sha256"))
            if (not isinstance(fid, str) or not KEY_RE.fullmatch(fid)
                    or not isinstance(occurrence_id, str)
                    or not occurrence_id
                    or not isinstance(prior_hash, str)
                    or not SHA256_RE.fullmatch(prior_hash)):
                raise PipelineError("Review requires version-bound live occurrence")
            if fid not in inv["formulations"]:
                row["status"] = "source_not_in_current_inventory"
            else:
                node = snapshot["nodes"].get(fid)
                if node is None or digest(node) != prior_hash:
                    row["status"] = "needs_effective_node_reanchor"
                else:
                    matches = [
                        ref for ref in node.get("references", [])
                        if ref.get("occurrence_id") == occurrence_id
                    ]
                    if len(matches) != 1:
                        row["status"] = "occurrence_changed_or_ambiguous"
                    elif (case.get("expected_state") is not None
                          and matches[0].get("state") != case["expected_state"]):
                        row["status"] = "reference_disposition_changed"
                    elif (case.get("expected_target_meaning_id") is not None
                          and matches[0].get("target_meaning_id")
                          != case["expected_target_meaning_id"]):
                        row["status"] = "reference_target_changed"
                    else:
                        row["status"] = "mathematical_review_required"
            row.update({"formulation_id": fid,
                        "expected_occurrence_id": occurrence_id,
                        "expected_node_sha256": prior_hash,
                        "current_effective_node_sha256": digest(snapshot["nodes"][fid])
                            if fid in snapshot["nodes"] else None})
        else:
            raise PipelineError("Unknown reconciliation kind: " + str(kind))
        entries.append(row)

    # Historical review anchors are retained, not silently re-anchored to a
    # newer source. Only verified amendments of the exact predecessor can
    # supersede one. Resolve after reading every case so queue order is inert.
    by_id = {row["id"]: row for row in entries}
    for case, row in zip(cases, entries):
        if "superseded_by_case_ids" not in case:
            continue
        links = case["superseded_by_case_ids"]
        if (case["kind"] != "review" or not isinstance(links, list) or not links
                or any(not isinstance(key, str) for key in links)
                or len(set(links)) != len(links)
                or any(key not in by_id or by_id[key]["kind"] != "transaction"
                       or by_id[key].get("mode") != "amend" for key in links)):
            raise PipelineError("Supersession requires unique amendment transaction case IDs")
        row["supersession_is_mathematical_certification"] = False
        row["historical_anchor_status"] = row["status"]
        row["superseded_by_case_ids"] = links
        if any(by_id[key]["status"] != "applied_receipt_verified" for key in links):
            row["status"] = "supersession_requires_receipt_verification"
            continue
        fid, prior_hash = case["formulation_id"], case["expected_node_sha256"]
        if any(not isinstance(packets_by_case[key].get("amendments"), list) for key in links):
            raise PipelineError("Superseding packet needs an amendments list")
        if not all(any(isinstance(event, dict)
                       and event.get("formulation_id") == fid
                       and event.get("expected_node_sha256") == prior_hash
                       for event in packets_by_case[key].get("amendments", []))
                   for key in links):
            row["status"] = "supersession_anchor_mismatch"
            continue
        node = snapshot["nodes"].get(fid)
        unchanged_reference = bool(node and any(
            ref.get("occurrence_id") == case["expected_occurrence_id"]
            and (case.get("expected_state") is None
                 or ref.get("state") == case["expected_state"])
            and (case.get("expected_target_meaning_id") is None
                 or ref.get("target_meaning_id") == case["expected_target_meaning_id"])
            for ref in node.get("references", [])))
        if node is None or digest(node) == prior_hash or unchanged_reference:
            row["status"] = "supersession_effect_not_visible"
        else:
            row["status"] = "superseded_by_verified_transaction"
        row["supersession_is_mathematical_certification"] = False

    return {
        "schema_version": 1,
        "read_only": True,
        "graph_changes_applied": False,
        "mathematics_certified": False,
        "authorizes_submission": False,
        "authorizes_gate_change": False,
        "historical_review_scope": queue.get("historical_review_scope"),
        "current_inventory_sha256": inv["source_inventory_sha256"],
        "current_unresolved_fingerprint": summary.get("unresolved_fingerprint"),
        "current_unresolved_canonical": summary.get("unresolved_missing_candidates"),
        "current_amendment_event_count": summary.get("scan_amendment_event_count"),
        "current_phase": summary.get("phase"),
        "current_consolidation_gate_valid": summary.get("consolidation_gate_valid"),
        "case_count": len(entries),
        "active_review_case_count": sum(row["kind"] == "review" and
            row["status"] != "superseded_by_verified_transaction" for row in entries),
        "superseded_review_case_count": sum(
            row["status"] == "superseded_by_verified_transaction" for row in entries),
        "current_registry_candidates": summary.get("missing_candidates"),
        "current_active_aliases": summary.get("alias_candidate_records"),
        "historical_alias_event_count": len(snapshot.get("aliases", [])),
        "status_counts": dict(sorted(Counter(x["status"] for x in entries).items())),
        "cases": entries,
        "warning": "Receipt verification proves a recorded graph transaction, "
                   "not semantic correctness or source certification. "
                   "Review cases never authorize automatic amendments.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--queue", required=True, type=Path)
    args = parser.parse_args()
    queue = json.loads(args.queue.read_text(encoding="utf-8"))
    print(json.dumps(reconciliation_status(args.workspace, queue),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
