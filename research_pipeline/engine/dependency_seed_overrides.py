"""Append-only, source-version-bound historical seed review and effective replay.

This operates only on the independent graph. The original source inventory and
its seed relations NEVER change. An old event is retained for provenance but is
inactive if its source version or original seed digest changes.
"""
from __future__ import annotations

import json
from pathlib import Path

from research_pipeline.engine.core import PipelineError, digest

EVENT_FILE = "seed_overrides.jsonl"


def read_events(graph: Path) -> list[dict]:
    path = graph / EVENT_FILE
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def scan_missing_sources(nodes: dict) -> dict[str, set[str]]:
    """Only a source-observed candidate can replace that source's seed link."""
    found: dict[str, set[str]] = {}
    for fid, node in nodes.items():
        for ref in node.get("references", []):
            if ref.get("state") == "missing":
                found.setdefault(ref["missing_candidate_id"], set()).add(fid)
    return found


def replay_seed_overrides(inv: dict, events: list[dict],
                          scan_sources: dict[str, set[str]],
                          *, aliased: set[str] | None = None,
                          resolved: set[str] | None = None) -> dict[str, dict]:
    """Validate all events BEFORE returning effective seed replacements.

    No chained overrides or silent reinterpretation of unsupported identities.
    Only one active override per historical relation/source version is allowed.
    """
    seeds = {s["relation_id"]: s for s in inv["seed_relations"]}
    active: dict[str, dict] = {}
    seen: set[str] = set()
    aliased = aliased or set()
    resolved = resolved or set()
    for event in events:
        eid = event.get("seed_override_id")
        rid = event.get("relation_id")
        if (event.get("schema_version") != 1 or not isinstance(eid, str)
                or not eid or eid in seen):
            raise PipelineError("Duplicate/invalid historical seed override identity")
        seen.add(eid)
        if not isinstance(rid, str) or rid not in seeds:
            raise PipelineError("Unknown historical seed override relation: " + str(rid))
        seed = seeds[rid]
        fid = seed["from_formulation"]
        version = inv["formulations"][fid]["version_sha256"]
        if event.get("expected_version_sha256") != version:
            continue  # Retain stale earlier-version events without applying them.
        if event.get("expected_seed_sha256") != digest(seed):
            continue  # A changed original seed also invalidates historical override.
        if rid in active:
            raise PipelineError("Repeated effective seed override: " + rid)
        if event.get("expected_old_target_meaning_id") != seed.get("target_meaning_id"):
            raise PipelineError("Seed override original target mismatch: " + rid)
        why = event.get("review_rationale")
        if (not isinstance(why, str) or len(why.strip()) < 60
                or not str(event.get("reviewed_by", "")).strip()):
            raise PipelineError("Historical seed override requires contextual review: " + rid)
        new = event.get("replacement")
        if (not isinstance(new, dict) or set(new) !=
                {"state", "missing_candidate_id"} or new.get("state") != "missing"):
            raise PipelineError("Only missing-candidate seed overrides supported: " + rid)
        cid = new["missing_candidate_id"]
        if (cid not in scan_sources or fid not in scan_sources[cid]
                or cid in aliased or cid in resolved):
            raise PipelineError("Candidate absent/noncanonical or not sourced here: " + rid)
        active[rid] = event
    return active


def effective_seed_reference(seed: dict, override: dict | None,
                             occurrence_id: str) -> dict:
    """Preserve seed relation and occurrence identity in all derived views."""
    base = {"occurrence_id": occurrence_id, "phrase": seed["phrase"],
            "relation_id": seed["relation_id"], "origin": "preexisting_relation"}
    if override is not None:
        return {**base,
                "state": "missing",
                "missing_candidate_id": override["replacement"]["missing_candidate_id"],
                "original_target_meaning_id": seed.get("target_meaning_id"),
                "seed_override_id": override["seed_override_id"],
                "origin": "preexisting_relation:seed_override"}
    if seed.get("target_meaning_id"):
        return {**base, "state": "existing",
                "target_meaning_id": seed["target_meaning_id"]}
    return base
