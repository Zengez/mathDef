"""Read-only preflight checks for context-reviewed dependency graph packages.

Run after an editor has reviewed mathematical/other domain meaning, and BEFORE
committing a proposed graph inbox package. This module checks mechanics only:
version anchors, live effective-node hashes, package shape, candidate aliases,
and source-preserving snapshot validation. It never asserts semantic equivalence,
certifies mathematics, writes files, or admits new meanings.

Usage:
    python -m research_pipeline.engine.dependency_review_preflight \\
      --workspace research_pipeline/experiments/reconstruction-v2-independent \\
      --batch research_pipeline/experiments/reconstruction-v2-independent/dependency_graph/inbox/REVIEW.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from research_pipeline.engine.core import PipelineError, digest
from research_pipeline.engine.dependency_graph import (
    SCHEMA, KEY_RE, alias_map, amendment_events, graph_path, live_nodes,
    make_snapshot, missing_key, read,
)


def review_preflight(workspace: Path, batch_path: Path) -> dict:
    """Mechanically validate an already human/assistant-reviewed batch, no writes.

    Same-version amendment preconditions are checked against the *effective*
    snapshot, including prior append-only amendments. Repeated amendments to
    one formulation in the same package are checked sequentially, like ingest.
    Candidate identity remains phrase + context; possible aliases are NOT
    inferred by this function.
    """
    graph = graph_path(workspace)
    inv = read(graph / "INVENTORY.json")
    if not isinstance(inv, dict) or not inv.get("formulations"):
        raise PipelineError("Preflight requires an existing graph inventory")
    package = read(batch_path)
    if not isinstance(package, dict):
        raise PipelineError("Review batch must be a JSON object")
    batch_id = package.get("id")
    mode = package.get("mode")
    if (package.get("schema_version") != SCHEMA
            or not isinstance(batch_id, str)
            or not KEY_RE.fullmatch(batch_id)
            or Path(batch_path).stem != batch_id
            or mode not in ("amend", "alias")):
        raise PipelineError("Preflight supports correctly named amend/alias packages only")

    receipt = read(graph / "applied" / (batch_id + ".json"))
    package_hash = digest(package)
    if receipt is not None:
        if receipt.get("sha256") != package_hash or receipt.get("mode") != mode:
            raise PipelineError("Previously applied package differs from its immutable receipt")
        return {"schema_version": SCHEMA, "read_only": True,
                "mathematical_certification": False, "batch_id": batch_id,
                "mode": mode, "status": "already_applied", "package_sha256": package_hash,
                "checked_events": 0, "new_candidate_preview": []}

    nodes = live_nodes(graph, inv)
    candidates_path = graph / "missing_candidates.jsonl"
    known_reusable = {
        row["id"] for line in candidates_path.read_text(encoding="utf-8").splitlines()
        if line.strip() for row in [json.loads(line)]
        if row.get("status") == "unresearched" and not row.get("alias_of")
        and not row.get("resolved_target_meaning_id")
    } if candidates_path.is_file() else set()
    preview = []
    seen_events = set()
    if mode == "amend":
        historical = {event["amendment_id"] for event in amendment_events(graph)}
        proposed = package.get("amendments")
        if not isinstance(proposed, list) or not proposed:
            raise PipelineError("Amend package needs a nonempty amendments list")
        for item in proposed:
            eid = item.get("amendment_id")
            fid = item.get("formulation_id")
            if (not isinstance(eid, str) or not KEY_RE.fullmatch(eid)
                    or eid in seen_events or eid in historical):
                raise PipelineError("Missing, invalid or reused append-only amendment ID")
            seen_events.add(eid)
            entry = inv["formulations"].get(fid)
            if not entry or item.get("version_sha256") != entry["version_sha256"]:
                raise PipelineError("Unknown or stale formulation version: " + str(fid))
            if (not isinstance(item.get("reason"), str)
                    or len(item["reason"].strip()) < 40
                    or not str(item.get("reviewed_by", "")).strip()):
                raise PipelineError("Amendment needs substantive rationale and reviewer")
            prior = nodes.get(fid)
            if prior is None or item.get("expected_node_sha256") != digest(prior):
                raise PipelineError("Stale effective node hash: " + str(fid))
            next_node = make_snapshot(
                inv, fid, item.get("references", []),
                "complete" if item.get("complete") is True else "scan_incomplete",
                item.get("review_rationale", ""),
                reusable_missing_candidate_ids=known_reusable,
            )
            if prior.get("scan_status") == "complete" and next_node["scan_status"] != "complete":
                raise PipelineError("Cannot silently demote a reviewed complete scan")
            nodes[fid] = next_node
            for ref in next_node["references"]:
                if ref["state"] == "missing":
                    preview.append({
                        "formulation_id": fid, "phrase": ref["phrase"],
                        "candidate_id": ref["missing_candidate_id"],
                        "explicit_reviewed_reuse": bool(ref.get("reviewed_existing_candidate_id")),
                        "new_candidate_identity": ref["missing_candidate_id"] not in known_reusable,
                    })
        checked = len(proposed)
    else:
        proposed = package.get("aliases")
        if not isinstance(proposed, list) or not proposed:
            raise PipelineError("Alias package needs a nonempty aliases list")
        known = {json.loads(line)["id"] for line in
                 (graph / "missing_candidates.jsonl").read_text(encoding="utf-8").splitlines()
                 if line.strip()}
        old_file = graph / "candidate_aliases.jsonl"
        historical = ([json.loads(line) for line in
                       old_file.read_text(encoding="utf-8").splitlines()
                       if line.strip()] if old_file.exists() else [])
        existing_ids = {event["alias_id"] for event in historical}
        for item in proposed:
            eid = item.get("alias_id")
            if (not isinstance(eid, str) or not KEY_RE.fullmatch(eid)
                    or eid in existing_ids or eid in seen_events):
                raise PipelineError("Invalid or reused alias event identity")
            seen_events.add(eid)
            if (item.get("alias_candidate_id") not in known
                    or item.get("canonical_candidate_id") not in known):
                raise PipelineError("Candidate alias must reference two existing candidates")
            if (not str(item.get("reviewed_by", "")).strip()
                    or len(str(item.get("reason", "")).strip()) < 40):
                raise PipelineError("Alias requires an explicit contextual reviewer and reason")
        # Also checks chains, cycles, repeats and already aliased canonical targets.
        alias_map(graph, known, historical + proposed)
        checked = len(proposed)

    return {"schema_version": SCHEMA, "read_only": True,
            "mathematical_certification": False, "batch_id": batch_id,
            "mode": mode, "status": "mechanically_valid_not_applied",
            "package_sha256": package_hash, "checked_events": checked,
            "new_candidate_preview": preview,
            "warning": "Mechanical validation is not contextual equivalence review, "
                       "external-source verification, independent freeze or approval."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--batch", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(review_preflight(args.workspace, args.batch),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
