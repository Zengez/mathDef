"""Read-only, source-context-rich dependency consolidation review bundle.

This module is intentionally subject neutral. Similar surfaces are *review
groups*, never automated assertions of semantic identity or permission to
create a missing meaning. Neither the corpus nor the graph is modified.

Usage:
    python -m research_pipeline.engine.dependency_context_worklist \
      --workspace research_pipeline/experiments/reconstruction-v2-independent \
      --contains "residue field" --limit 20
    # Or: --contains-any "ideal" --contains-any "quotient" --limit 30
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from research_pipeline.engine.core import digest
from research_pipeline.engine.dependency_graph import (
    consolidation_worklist, graph_path, live_nodes, norm, read,
)


def build_review_bundle(workspace: Path, limit: int = 20, contains: str = "",
                        contains_any: tuple[str, ...] = ()) -> dict:
    """Join grouped unresolved references to the original text and live adjacency.

    `contains` and repeatable `contains_any` select *surface phrases*, not
    mathematical synonyms. The filters are OR alternatives when both supplied.
    The complete list is inspected before filtering; `limit` applies to matching
    groups. Each source formulation is loaded only once across selected groups.
    Full current node SHA256 digests are the preconditions for any separate,
    reviewed append-only amendment. This function writes nothing.
    """
    graph = graph_path(workspace)
    inv = read(graph / "INVENTORY.json")
    if not inv:
        raise ValueError("An existing dependency graph inventory is required")
    # Reuse the generic deterministic surface grouping; request the full list
    # so a selective substring query does not silently miss later groups.
    grouped = consolidation_worklist(workspace, limit=10**9)
    needles = [norm(x) for x in (contains, *contains_any) if norm(x)]
    matches = [g for g in grouped["groups"]
               if not needles or any(n in norm(g["surface_key"]) for n in needles)]
    selected = matches[:max(0, limit)]
    nodes = live_nodes(graph, inv)
    formulations = {}
    for group in selected:
        for occurrence in group["observations"]:
            fid = occurrence["formulation_id"]
            if fid in formulations:
                continue
            source = inv["formulations"][fid]
            node = nodes.get(fid)
            formulations[fid] = {
                "source_meaning_id": source["meaning_id"],
                "source_display_term": source["display_term"],
                "source_definition": source["text"],
                "source_context": source["context"],
                "formulation_version_sha256": source["version_sha256"],
                "effective_node_sha256": digest(node) if node else None,
                "complete_scan": bool(node and node.get("scan_status") == "complete"),
                "review_rationale": node.get("review_rationale", "") if node else "",
                "reference_template": [
                    {k: v for k, v in ref.items() if k != "occurrence_id"}
                    for ref in node.get("references", [])
                ] if node else [],
                "linked_existing_meanings": [
                    {"meaning_id": ref["target_meaning_id"],
                     "display_term": inv["meanings"][ref["target_meaning_id"]]["display_term"]}
                    for ref in node.get("references", [])
                    if ref.get("state") == "existing"
                    and ref.get("target_meaning_id") in inv["meanings"]
                ] if node else [],
            }
    return {
        "schema_version": 1,
        "read_only": True,
        "phase": grouped["phase"],
        "external_definition_research_permitted":
            grouped["external_definition_research_permitted"],
        "total_unresolved_occurrences":
            grouped["total_unresolved_occurrences"],
        "distinct_surface_keys": grouped["distinct_surface_keys"],
        "surface_filter": contains,
        "surface_filters_any": list(contains_any),
        "matched_surface_groups": len(matches),
        "returned_surface_groups": len(selected),
        "groups": selected,
        "formulations": formulations,
        "warning": ("Surface similarity is NOT mathematical identity. The "
                    "reference template is only an editable draft; an amendment "
                    "still requires independent contextual mathematical review "
                    "and a version-bound append-only event."),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--contains", default="")
    parser.add_argument("--contains-any", action="append", default=[],
                        help="Repeat for OR-matched surface filters; no semantic grouping")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(build_review_bundle(
        args.workspace, limit=args.limit, contains=args.contains,
        contains_any=tuple(args.contains_any)),
        ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
