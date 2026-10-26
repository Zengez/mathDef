"""Nonrecursive, source-backed first-generation staging for an independent corpus.

One gate seals one ORIGINAL candidate snapshot. Research submissions live only
in generation_staging, never in the active population, inventory, or graph.
Staging does not itself promote/certify definitions, resolve candidates,
trigger new dependency scans, or import production material.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .core import PipelineError
from .dependency_graph import graph_path, read, digest
from .population import write_atomic


def _hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _staging(workspace):
    return Path(workspace) / "generation_staging"


def _snapshot_path(workspace):
    return _staging(workspace) / "MANIFEST.json"


def _record_dir(workspace):
    return _staging(workspace) / "records"


def _active(workspace):
    manifest = read(_snapshot_path(workspace))
    if not manifest:
        raise PipelineError("No sealed first-generation staging manifest")
    if manifest.get("schema_version") != 1:
        raise PipelineError("Unsupported generation staging manifest")
    return manifest


def create(workspace):
    """Freeze the original candidate IDs; do not load unresearched offspring."""
    root = Path(workspace)
    graph = graph_path(root)
    state = read(graph / "STATE.json", {}).get("summary", {})
    manifest_file = _snapshot_path(root)
    if manifest_file.exists():
        current = _active(root)
        if current.get("unresolved_fingerprint") == state.get("unresolved_fingerprint"):
            return {"status": "already_exists", "count": current["candidate_count"],
                    "manifest": str(manifest_file)}
        raise PipelineError("A generation already exists; archive/integrate it before opening another")
    if not state.get("consolidation_gate_valid") or state.get("phase") != "research_missing_dependencies":
        raise PipelineError("First-generation external research requires valid phase gate")
    if state.get("scan_complete") != state.get("total_formulations"):
        raise PipelineError("Source inventory has unscanned formulations")
    candidates_file = graph / "missing_candidates.jsonl"
    candidates = [json.loads(line) for line in candidates_file.read_text(encoding="utf-8").splitlines()
                  if line.strip()]
    todo = [dict(id=c["id"], query=c["query"], context=c.get("context", ""),
                 occurrence_count=c["occurrence_count"],
                 upstream_formulation_count=c["upstream_formulation_count"],
                 incoming_formulation_ids=c.get("incoming_formulation_ids", []))
            for c in candidates if c.get("status") == "unresearched"]
    todo.sort(key=lambda c: (-c["upstream_formulation_count"],
                             -c["occurrence_count"], c["id"]))
    if not todo:
        raise PipelineError("No unresolved original candidates to research")
    snapshot = {
        "schema_version": 1,
        "policy": "one_bounded_generation_no_recursive_dependencies",
        "inventory_sha256": state["inventory_sha256"],
        "unresolved_fingerprint": state["unresolved_fingerprint"],
        "candidate_registry_sha256": _hash_file(candidates_file),
        "accepted_meanings_file_sha256": _hash_file(root / "records" / "meanings.jsonl"),
        "candidate_count": len(todo),
        "original_incoming_occurrences": sum(x["occurrence_count"] for x in todo),
        "candidates": todo,
        "research_status": "source_backed_provisional_staging_only",
        "certified": False, "published": False, "recursive_research": False,
    }
    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    write_atomic(manifest_file, json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    return {"status": "created", "count": len(todo),
            "manifest": str(manifest_file),
            "original_incoming_occurrences": snapshot["original_incoming_occurrences"]}


def status(workspace):
    manifest = _active(workspace)
    directory = _record_dir(workspace)
    ids = {x["id"] for x in manifest["candidates"]}
    recorded = set()
    outcomes = {}
    for path in sorted(directory.glob("*.json")) if directory.is_dir() else ():
        data = read(path)
        cid = data.get("candidate_id")
        if cid not in ids or path.stem != cid or cid in recorded:
            raise PipelineError("Unexpected, duplicate or invalid staged candidate " + path.name)
        recorded.add(cid)
        outcomes[data["disposition"]] = outcomes.get(data["disposition"], 0) + 1
    return {
        "phase": "bounded_first_generation",
        "original_candidate_count": len(ids),
        "completed_provisional_dispositions": len(recorded),
        "remaining": len(ids - recorded),
        "ready_for_reviewed_integration": len(ids) == len(recorded),
        "disposition_counts": outcomes,
        "graph_changed": False, "production_accessed": False,
        "publication_certified": False,
    }


def stage(workspace, submission_file):
    """One versioned research record; original candidates stay untouched."""
    root = Path(workspace)
    manifest = _active(root)
    graph_state = read(graph_path(root) / "STATE.json", {}).get("summary", {})
    if (not graph_state.get("consolidation_gate_valid")
            or graph_state.get("inventory_sha256") != manifest["inventory_sha256"]
            or graph_state.get("unresolved_fingerprint") != manifest["unresolved_fingerprint"]):
        raise PipelineError("Stale generation: initial inventory changed during staging")
    sub = read(Path(submission_file))
    if sub.get("schema_version") != 1:
        raise PipelineError("Unsupported staged research version")
    cid = sub.get("candidate_id")
    source = {x["id"]: x for x in manifest["candidates"]}.get(cid)
    if not source or sub.get("original_query") != source["query"]:
        raise PipelineError("Unrecognized or mutated original candidate identity")
    dispositions = {"new_meaning", "equivalent_to_existing", "contextual_variant",
                    "specialization", "nondefinitional", "deferred", "unresolved"}
    if sub.get("disposition") not in dispositions:
        raise PipelineError("Unknown mathematical research disposition")
    if len(sub.get("reasoning", "").strip()) < 50:
        raise PipelineError("Missing substantive mathematical reasoning")
    if sub["disposition"] not in {"deferred", "unresolved"}:
        if len(sub.get("definition", "").strip()) < 25:
            raise PipelineError("Research record requires preliminary definition")
        if not isinstance(sub.get("sources"), list) or not sub["sources"]:
            raise PipelineError("First generation requires external mathematical sources")
        for entry in sub["sources"]:
            if not isinstance(entry, dict) or not str(entry.get("url", "")).startswith("https://"):
                raise PipelineError("Every cited source needs an https locator")
            if not entry.get("section") or not entry.get("relevance"):
                raise PipelineError("Source missing section or mathematical relevance note")

    comparison = sub.get("comparison") or {}
    if (comparison.get("accepted_meanings_sha256") != manifest["accepted_meanings_file_sha256"]
            or not comparison.get("reviewed_accepted_independent_corpus")
            or not comparison.get("reviewed_provisional_independent_corpus")
            or len(comparison.get("rationale", "").strip()) < 40):
        raise PipelineError("Explicit accepted and provisional corpus comparisons required")
    from .population import snapshot
    preliminary, _ = snapshot(root)
    provisional_version = digest(preliminary["meanings"])
    if comparison.get("provisional_meanings_sha256") != provisional_version:
        raise PipelineError("Stale provisional comparison snapshot")
    records = _record_dir(root)
    previous_ids = sorted(path.stem for path in records.glob("*.json")) if records.exists() else []
    target = records / (cid + ".json")
    if target.exists():
        if read(target) == sub:
            return {"status": "unchanged", "candidate_id": cid}
        raise PipelineError("Staged decision already exists; preserve it as immutable evidence")
    if comparison.get("earlier_staged_candidate_ids") != previous_ids:
        raise PipelineError("Must compare against every earlier first-generation provisional draft")
    if sub.get("new_missing_dependencies") and not sub.get("defer_new_missing_dependencies"):
        raise PipelineError("New dependencies belong to the next generation, not recursive research")
    records.mkdir(parents=True, exist_ok=True)
    write_atomic(target, json.dumps(sub, indent=2, ensure_ascii=False) + "\n")
    return {"status": "staged", "candidate_id": cid,
            "completed": len(previous_ids) + 1, "original_count": manifest["candidate_count"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--mode", required=True, choices=("create", "stage", "status"))
    parser.add_argument("--submission", type=Path)
    args = parser.parse_args()
    if args.mode == "create":
        outcome = create(args.workspace)
    elif args.mode == "status":
        outcome = status(args.workspace)
    else:
        if not args.submission:
            raise PipelineError("--submission is required for stage")
        outcome = stage(args.workspace, args.submission)
    print(json.dumps(outcome, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
