"""Topic-neutral research queue: group deferred targets and propose breadth tasks.

Never treats heuristic labels as mathematical equivalence. All output is a
planning aid for source-based reasoning in Chat, not verified new content.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

from .core import PipelineError
from .population import audit, read_json, write_atomic


def normalized(text):
    return " ".join(re.findall(r"[a-z0-9]+", text.casefold()))


def plan(workspace, profile):
    root = Path(workspace).resolve()
    config = read_json(profile)
    if config.get("schema_version") != 1 or not isinstance(config.get("breadth_topics"), list):
        raise PipelineError("Planning profile needs schema version and breadth_topics")
    pending = audit(root)
    graph_status_file = root / "dependency_graph" / "STATE.json"
    if graph_status_file.is_file():
        graph_status = read_json(graph_status_file)["summary"]
        # Generic handshake: when a graph-driven project explicitly holds
        # unrelated breadth, this legacy breadth planner must not override it.
        if graph_status.get("breadth_expansion") == "on_hold":
            from .dependency_graph import research_queue
            queue = research_queue(root, limit=1000)
            clusters = [
                {"missing_candidate_id": candidate["id"],
                 "target_query_normalized": normalized(candidate["query"]),
                 "context": candidate.get("context", ""),
                 "awaiting_formulation_ids": candidate["incoming_formulation_ids"],
                 "number_of_affected_formulations": candidate["upstream_formulation_count"],
                 "priority": "high" if candidate["upstream_formulation_count"] > 1 else "normal"}
                for candidate in queue["candidates"]
            ]
            return {
                "schema_version": 1,
                "strategy": "dependency_first_until_structural_stabilization",
                "breadth_candidates": [], "completed_breadth_topics": [],
                "breadth_batch_143": "on_hold",
                "deferred_target_clusters": clusters,
                "suggested_next_package": {
                    "breadth_topic_candidates": [],
                    "maximum_deferred_target_inclusions": len(clusters),
                    "rule": ("Finish unscanned/contextual formulation scans before "
                             "deduplicated missing-meaning research; no unrelated breadth.")
                },
                "graph_checkpoint": {
                    "phase": queue["phase"],
                    "inventory_sha256": graph_status["inventory_sha256"],
                    "open": graph_status["open"], "closed": graph_status["closed"],
                    "scan_complete": graph_status["scan_complete"],
                    "unscanned": graph_status["unscanned"],
                    "scan_incomplete": graph_status["scan_incomplete"],
                },
                "reconciliation_findings": pending["finding_summary"],
                "note": "Graph-derived scheduling only. Does not certify or promote records.",
            }
    grouped = defaultdict(list)
    for finding in pending["findings"]:
        if finding["kind"] == "unresolved_target":
            grouped[normalized(finding["reason"])].append(finding["record_id"])
    targets = [
        {"target_query_normalized": key, "awaiting_relation_ids": sorted(ids),
         "number_of_affected_relations": len(ids),
         "priority": "high" if len(ids) > 1 else "normal"}
        for key, ids in grouped.items() if key
    ]
    targets.sort(key=lambda x: (-x["number_of_affected_relations"],
                                x["target_query_normalized"]))
    visited = set()
    completed = set(config.get("completed_topic_ids", []))
    # Future package metadata can supply covered topic IDs without
    # repeatedly editing the project adapter. Only APPLIED packages count.
    applied = root / "population" / "applied"
    inbox = root / "population" / "inbox"
    if applied.is_dir():
        for receipt in applied.glob("*.json"):
            record = read_json(receipt)
            pkg = inbox / (record.get("id", "") + ".json")
            if pkg.is_file():
                committed = read_json(pkg)
                completed.update(committed.get("research_topic_ids", []))
    breadth = []
    for item in config["breadth_topics"]:
        key = item.get("id")
        if not isinstance(key, str) or not key or key in visited or not item.get("research_prompt"):
            raise PipelineError("Each breadth topic needs a unique id and research_prompt")
        visited.add(key)
        if key in completed:
            continue
        breadth.append({"id": key, "research_prompt": item["research_prompt"],
                        "priority": item.get("priority", "normal"),
                        "source_review_required": True})
    output = {
        "schema_version": 1,
        "strategy": "balanced independent breadth with bounded prerequisite lookahead",
        "breadth_candidates": breadth,
        "completed_breadth_topics": sorted(completed),
        "deferred_target_clusters": targets,
        "suggested_next_package": {
            "breadth_topic_candidates": [r["id"] for r in breadth[:max(
                1, config.get("breadth_topics_per_package", 3))]],
            "maximum_deferred_target_inclusions": max(
                0, config.get("prerequisite_lookahead_limit", 2)),
            "rule": "Independently inspect sources and collisions; never mechanically certify candidate labels.",
        },
        "reconciliation_findings": pending["finding_summary"],
        "coverage_and_stop_policy": config.get("completion_policy", {}),
        "note": "Candidate queue only; no automatic mathematical research, admission, publication or freeze.",
    }
    return output


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--profile", type=Path, required=True)
    p.add_argument("--write", action="store_true")
    args = p.parse_args()
    result = plan(args.workspace, args.profile)
    if args.write:
        write_atomic(Path(args.workspace) / "population" / "QUEUE.json",
                     json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
