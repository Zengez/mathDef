"""Read-only, version-pinned review of historical Wave2 seed re-target proposals.

A successful preview does NOT alter authoritative seed relations, graphs, or gate
status. There is intentionally no submission or application code here.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from research_pipeline.engine.core import PipelineError, digest
from research_pipeline.engine.dependency_global_audit import load_live_snapshot


def preview_seed_retargets(snapshot: dict, manifest: dict) -> dict:
    """Validate every proposed decision against immutable seed/source evidence.

    Replacement only permits a REGISTERED unresolved canonical candidate, not
    a new meaning or an unrecorded missing identity. This is validation of
    provenance and state, *not* certification of mathematical correctness.
    """
    inv = snapshot["inventory"]
    summary = snapshot["state"]["summary"]
    if manifest.get("schema_version") != 1:
        raise PipelineError("Seed preview requires schema_version=1")
    if (manifest.get("inventory_sha256") != inv["source_inventory_sha256"]
            or manifest.get("seed_relations_sha256") != inv["seed_relations_sha256"]
            or manifest.get("unresolved_fingerprint") != summary["unresolved_fingerprint"]):
        raise PipelineError("Seed review anchors are stale")
    reviewer = manifest.get("reviewed_by")
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise PipelineError("Named reviewer required for historical seed proposal")
    changes = manifest.get("changes")
    if not isinstance(changes, list) or not changes:
        raise PipelineError("An explicit nonempty list of seed proposals is required")
    seeds = {s["relation_id"]: s for s in inv["seed_relations"]}
    candidates = {c["id"]: c for c in snapshot.get("candidates", [])}
    aliases = {a["alias_candidate_id"] for a in snapshot.get("aliases", [])}
    seen = set()
    previews = []
    for edit in changes:
        rid = edit.get("relation_id")
        if not isinstance(rid, str) or rid in seen or rid not in seeds:
            raise PipelineError("Unknown or duplicate historical seed relation: " + str(rid))
        seen.add(rid)
        seed = seeds[rid]
        fid = seed["from_formulation"]
        source = inv["formulations"][fid]
        if (edit.get("expected_seed_sha256") != digest(seed)
                or edit.get("expected_from_formulation") != fid
                or edit.get("expected_version_sha256") != source["version_sha256"]
                or edit.get("expected_seed_target_meaning_id") != seed["target_meaning_id"]):
            raise PipelineError("Stale historical seed or formulation: " + rid)
        if seed["target_meaning_id"] not in inv["meanings"]:
            raise PipelineError("Seed does not point to an existing meaning: " + rid)
        why = edit.get("review_rationale")
        if not isinstance(why, str) or len(why.strip()) < 60:
            raise PipelineError("Substantive mathematical justification required: " + rid)
        replacement = edit.get("replacement")
        if not isinstance(replacement, dict) or set(replacement) != {
                "state", "missing_candidate_id"} or replacement["state"] != "missing":
            raise PipelineError("Only registered missing-candidate previews permitted: " + rid)
        cid = replacement["missing_candidate_id"]
        candidate = candidates.get(cid)
        if (not candidate or candidate.get("status") != "unresearched"
                or candidate.get("alias_of") or candidate.get("resolved_target_meaning_id")
                or cid in aliases):
            raise PipelineError("Missing target must be an unresolved canonical candidate: " + rid)
        # A source without an observed candidate occurrence is not automatically
        # presumed semantically equivalent just from a candidate's general name.
        if fid not in candidate.get("incoming_formulation_ids", []):
            raise PipelineError("Candidate lacks reviewed occurrence from this formulation: " + rid)
        previews.append({
            "relation_id": rid,
            "from_formulation": fid,
            "source_term": source["display_term"],
            "source_text": source["text"],
            "source_context": source["context"],
            "source_version_sha256": source["version_sha256"],
            "expected_seed_sha256": digest(seed),
            "previous_target_meaning_id": seed["target_meaning_id"],
            "previous_target_term": inv["meanings"][seed["target_meaning_id"]]["display_term"],
            "proposed_state": "missing",
            "proposed_candidate_id": cid,
            "proposed_candidate_query": candidate["query"],
            "source_occurrence_registered": True,
            "review_rationale": why,
        })
    return {
        "schema_version": 1,
        "read_only": True,
        "applied": False,
        "no_graph_or_seed_writes": True,
        "mathematics_certified": False,
        "inventory_sha256": inv["source_inventory_sha256"],
        "seed_relations_sha256": inv["seed_relations_sha256"],
        "unresolved_fingerprint": summary["unresolved_fingerprint"],
        "reviewed_by": reviewer,
        "proposal_count": len(previews),
        "proposals": previews,
        "warning": ("Preflight checks exact provenance and canonical identity only. "
                    "No engine support for applying seed overrides is implemented; "
                    "these remain mathematical review proposals."),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = preview_seed_retargets(load_live_snapshot(args.workspace), manifest)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
