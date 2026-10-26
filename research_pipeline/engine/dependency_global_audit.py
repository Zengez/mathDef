"""Read-only, source-free global dependency audit and reviewed batch preparation.

The scanner makes *leads*, never mathematical judgments or new definitions.
It reads the complete effective append-only graph once (including corrections),
reports contextual risks and possible missing-candidate duplicates, and can
provide a full temporary audit snapshot for carefully reviewed edits.

The preparer accepts ONLY an explicit reviewer-supplied change manifest with
exact prior-node hashes and occurrence identities. It emits <=5 complete
formulation amendments per package to an *offline* directory, validates them
with the existing read-only preflight, and never submits an inbox package.

Usage:
  python -m research_pipeline.engine.dependency_global_audit \
    --workspace research_pipeline/experiments/reconstruction-v2-independent scan \
    --limit 60 --candidate-limit 40
  python -m research_pipeline.engine.dependency_global_audit \
    --workspace research_pipeline/experiments/reconstruction-v2-independent scan \
    --snapshot-output /tmp/mathdef-effective-audit.json
  python -m research_pipeline.engine.dependency_global_audit \
    --workspace research_pipeline/experiments/reconstruction-v2-independent prepare \
    --manifest /tmp/reviewed-decisions.json --output-dir /tmp/wave2-proposed-packets
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import re

from research_pipeline.engine.core import PipelineError, digest
from research_pipeline.engine.dependency_graph import (
    KEY_RE, graph_path, live_nodes, make_snapshot, missing_key, norm, read,
)
from research_pipeline.engine.dependency_review_preflight import (
    prepare_review_context, review_preflight,
)
from research_pipeline.engine.dependency_seed_overrides import (
    read_events as read_seed_override_events, replay_seed_overrides,
    scan_missing_sources,
)
from research_pipeline.engine.dependency_audit_acceleration import (
    notation_aware_leads, rank_findings,
)


SMALL_CATEGORY = "meaning.wave2.foundation.small-category"
SMALL_GROUPOID = "meaning.wave2.foundation.small-groupoid"
FINITE_MODULE = "meaning.91ebb3796458d5bb.finite-generated-module"
SEVERITY_ORDER = {"integrity": 0, "high": 1, "review": 2}


def jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def load_live_snapshot(workspace: Path) -> dict:
    """One immutable in-memory view. No writes, original-production inputs or web."""
    graph = graph_path(workspace)
    inv = read(graph / "INVENTORY.json")
    state = read(graph / "STATE.json")
    if not inv or not isinstance(inv.get("formulations"), dict) or not state:
        raise PipelineError("Independent dependency inventory and STATE.json are required")
    nodes = live_nodes(graph, inv)  # authoritative replay of ALL amendments
    resolutions = jsonl(graph / "resolutions.jsonl")
    return {
        "inventory": inv, "state": state, "nodes": nodes,
        "candidates": jsonl(graph / "missing_candidates.jsonl"),
        "aliases": jsonl(graph / "candidate_aliases.jsonl"),
        "seed_override_events": read_seed_override_events(graph),
        "resolutions": resolutions,
        "resolved_candidate_ids": [x["missing_candidate_id"] for x in resolutions],
        "review_ledger": jsonl(graph / "audit_review_decisions.jsonl"),
    }


def candidate_review_bundle(snapshot: dict, *, candidate_ids: tuple[str, ...] = (),
                            limit: int = 8, max_formulations: int = 3,
                            contains: str = "", parent_budget: int | None = None,
                            compact_sources: bool = False) -> dict:
    """Small, impact-ordered, context-complete read-only mathematical review queue.

    Defaults to only unresolved CANONICAL candidate identities; applied
    aliases and version-bound resolutions are never reviewed a second time.
    Explicit candidate IDs must be unresolved canonical identities.
    Source text and references are the current effective append-only version.
    No similarity score is evidence of mathematical equivalence.
    """
    if limit < 0 or max_formulations < 1:
        raise PipelineError("Review limits must be nonnegative, with >=1 source per candidate")
    if parent_budget is not None and (
            not isinstance(parent_budget, int) or isinstance(parent_budget, bool)
            or parent_budget < 1):
        raise PipelineError("Parent budget must be a positive integer")
    if parent_budget is not None and candidate_ids:
        raise PipelineError("Parent budget cannot truncate explicit candidate IDs")
    inv, nodes = snapshot["inventory"], snapshot["nodes"]
    # Historical relations can appear in augmented audit evidence but do not
    # occupy live-node reference indices. Index them once for all candidates.
    seeds_by_form = defaultdict(list)
    for seed in inv.get("seed_relations", []):
        fid = seed.get("from_formulation")
        if fid in inv["formulations"]:
            seeds_by_form[fid].append({
                "relation_id": seed.get("relation_id"),
                "phrase": seed.get("phrase", ""),
                "target_meaning_id": seed.get("target_meaning_id"),
                "target_query": seed.get("target_query"),
                "relation_state": seed.get("relation_state"),
                "origin": "historical_seed_relation",
                "editable_in_live_node": False,
            })
    active = {c["id"]: c for c in snapshot.get("candidates", [])
              if c.get("status") == "unresearched"
              and not c.get("alias_of")
              and not c.get("resolved_target_meaning_id")}
    selected_ids = tuple(dict.fromkeys(candidate_ids))
    unknown = [cid for cid in selected_ids if cid not in active]
    if unknown:
        raise PipelineError("Unknown or noncanonical/resolved candidate IDs: "
                            + ", ".join(unknown))
    if selected_ids:
        chosen = [active[cid] for cid in selected_ids]
    else:
        chosen = sorted(active.values(), key=lambda c: (
            -c.get("occurrence_count", 0),
            -c.get("upstream_formulation_count", 0), c["id"]))
        if contains:
            needle = norm(contains)
            chosen = [c for c in chosen if needle in norm(
                c.get("query", "") + " " + c.get("context", ""))]
        chosen = chosen[:limit]
    omitted_by_budget = 0
    if parent_budget is not None:
        planned, visits = [], 0
        for candidate in chosen:
            cost = len(candidate.get("incoming_formulation_ids", []))
            # Keep priority order and never starve an oversized first item.
            if planned and visits + cost > parent_budget:
                break
            planned.append(candidate)
            visits += cost
            if visits >= parent_budget:
                break
        omitted_by_budget = len(chosen) - len(planned)
        chosen = planned
    shared_sources = {}
    items = []
    for candidate in chosen:
        source_ids = candidate.get("incoming_formulation_ids", [])
        # Source membership is indexed in the canonical missing registry.
        # Unknown source IDs are a visible risk, never silently fabricated.
        sources = []
        # A canonical candidate may combine context-reviewed aliases. Preserve
        # the actual source-specific phrases and original IDs in the read-only
        # bundle instead of treating the canonical query as universal wording.
        source_candidate_ids = {candidate["id"], *candidate.get("alias_ids", [])}
        for fid in source_ids[:max_formulations]:
            source = inv["formulations"].get(fid)
            node = nodes.get(fid)
            if source is None:
                sources.append({"formulation_id": fid,
                                "integrity_warning": "missing_source_formulation"})
                continue
            if fid not in shared_sources:
                shared_sources[fid] = {
                    "formulation_id": fid, "source_meaning_id": source["meaning_id"],
                    "display_term": source["display_term"],
                    "full_source_text": source["text"],
                    "source_context": source.get("context", ""),
                    "source_version_sha256": source["version_sha256"],
                    "effective_node_sha256": digest(node) if node else None,
                    "complete_scan": bool(node and node.get("scan_status") == "complete"),
                    "all_effective_references": node.get("references", []) if node else [],
                    # These positions belong EXCLUSIVELY to replayed live_nodes.
                    # Reviewer manifests should use the stable occurrence ID.
                    "effective_live_reference_rows": [
                        {"live_reference_index": i,
                         "expected_occurrence_id": ref.get("occurrence_id"),
                         "reference": ref}
                        for i, ref in enumerate(node.get("references", []) if node else [])
                    ],
                    # Never splice historical seed rows into the indexed live list.
                    "historical_seed_references": seeds_by_form.get(fid, []),
                }
            sources.append({**shared_sources[fid],
                "matching_source_references": [
                    {"reference_index": i, "phrase": ref.get("phrase", ""),
                     "context": ref.get("context", ""),
                     "observed_candidate_id": ref.get("missing_candidate_id"),
                     "occurrence_id": ref.get("occurrence_id")}
                    for i, ref in enumerate(node.get("references", []) if node else [])
                    if ref.get("state") == "missing"
                    and ref.get("missing_candidate_id") in source_candidate_ids
                ],
            })
        items.append({
            "candidate_id": candidate["id"], "query": candidate.get("query", ""),
            "mathematical_context": candidate.get("context", ""),
            "occurrence_count": candidate.get("occurrence_count", 0),
            "upstream_formulation_count": candidate.get("upstream_formulation_count", 0),
            "source_formulation_count": len(source_ids),
            "sources_truncated": max(0, len(source_ids) - len(sources)),
            "source_formulations": sources,
        })
    report = {
        "schema_version": 1, "read_only": True, "mathematics_certified": False,
        "automatic_aliases_or_edits": False,
        "inventory_sha256": inv["source_inventory_sha256"],
        "unresolved_fingerprint": snapshot["state"]["summary"].get(
            "unresolved_fingerprint"),
        "active_canonical_candidates": len(active),
        "reviewed_candidate_count": len(items),
        "candidates": items,
        "reference_view_warning": (
            "Historical seed references are distinct provenance evidence, "
            "not live-node list entries. Prepare edits against the effective "
            "node hash and exact expected_occurrence_id, not a mixed index."
        ),
        "warning": "Review entire source and effective references before "
                   "any human-authored alias or version-bound resolution; "
                   "recurrence ranks priority, never establishes equivalence.",
    }

    if parent_budget is not None or compact_sources:
        all_parents = [fid for candidate in chosen
                       for fid in candidate.get("incoming_formulation_ids", [])]
        report["workload"] = {
            "candidate_parent_visits": len(all_parents),
            "distinct_parent_formulations": len(set(all_parents)),
            "repeated_parent_visits": len(all_parents) - len(set(all_parents)),
            "parent_visit_budget": parent_budget,
            "budget_exceeded_by_first_candidate": bool(
                parent_budget is not None and len(all_parents) > parent_budget),
            "candidates_omitted_by_budget": omitted_by_budget,
            "source_contexts_emitted": len(shared_sources),
            "warning": "Counts describe context visits, not mathematical difficulty, "
                       "completed review, source certification or permission to merge.",
        }
    if compact_sources:
        report["schema_version"] = 2
        report["source_contexts"] = shared_sources
        report["source_contexts_deduplicated"] = True
        for item in items:
            item["source_formulations"] = [
                {"formulation_id": source["formulation_id"],
                 "matching_source_references": source["matching_source_references"]}
                if "matching_source_references" in source else source
                for source in item["source_formulations"]]
    if "candidate_context_reviews" in snapshot:
        from .dependency_context_reviews import validated_view
        report["candidate_context_reviews"] = validated_view(snapshot)
    return report


def strongly_connected(adjacency: dict[str, set[str]]) -> list[list[str]]:
    """Nontrivial SCCs, including self-links; deterministic sorted output."""
    order, stack, on_stack, indices, lows, cyclic = [0], [], set(), {}, {}, []

    def visit(v: str) -> None:
        indices[v] = lows[v] = order[0]
        order[0] += 1
        stack.append(v)
        on_stack.add(v)
        for w in sorted(adjacency.get(v, set())):
            if w not in indices:
                visit(w)
                lows[v] = min(lows[v], lows[w])
            elif w in on_stack:
                lows[v] = min(lows[v], indices[w])
        if lows[v] == indices[v]:
            group = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                group.append(w)
                if w == v:
                    break
            if len(group) > 1 or v in adjacency.get(v, set()):
                cyclic.append(sorted(group))

    for v in sorted(adjacency):
        if v not in indices:
            visit(v)
    return sorted(cyclic, key=lambda c: (-len(c), c))


def candidate_leads(candidates: list[dict], limit: int = 40) -> dict:
    """Compatibility adapter for notation-aware contextual review leads."""
    return notation_aware_leads(candidates, limit)


def analyze_snapshot(snapshot: dict, *, limit: int = 60,
                     candidate_limit: int = 40,
                     include_effective_snapshot: bool = False,
                     include_cycle_edges: bool = False) -> dict:
    inv, nodes = snapshot["inventory"], snapshot["nodes"]
    form = inv["formulations"]
    meanings = inv["meanings"]
    state = snapshot["state"]["summary"]
    candidates = snapshot.get("candidates", [])
    candidate_ids = {c["id"] for c in candidates}
    findings = []
    adjacency = {k: set() for k in meanings}
    edge_count = 0
    seed_edges = 0
    counts = Counter()

    def flag(severity: str, code: str, fid: str, node: dict | None,
             description: str, *, index: int | None = None,
             reference: dict | None = None) -> None:
        row = {"severity": severity, "code": code,
               "formulation_id": fid,
               "meaning_id": form[fid]["meaning_id"],
               "display_term": form[fid]["display_term"],
               "source_text": form[fid]["text"],
               "source_context": form[fid].get("context", ""),
               "version_sha256": form[fid]["version_sha256"],
               "effective_node_sha256": digest(node) if node else None,
               "description": description}
        if index is not None:
            row["reference_index"] = index
        if reference is not None:
            row["occurrence_id"] = reference.get("occurrence_id")
            row["reference"] = reference
        findings.append(row)
        counts[code] += 1

    for fid, source in sorted(form.items()):
        node = nodes.get(fid)
        if not node or node.get("scan_status") != "complete":
            flag("integrity", "incomplete_effective_node", fid, node,
                 "Missing, invalid or incomplete effective node; do not use a "
                 "stale original node in its place.")
            continue
        if node["version_sha256"] != source["version_sha256"]:
            flag("integrity", "stale_source_anchor", fid, node,
                 "Node version does not match independent source inventory.")
        # An open-preimage biconditional does not itself imply surjectivity:
        # a non-onto inclusion of discrete spaces is a counterexample.
        # This is a *scope lead*, not a finding that the full, explicitly
        # surjective submersive definition is false.
        source_words = norm(source["text"])
        if ("submersive" in source_words and "surjective" in source_words
                and "equivalently" in source_words
                and ("open exactly when" in source_words
                     or "open if and only if" in source_words)
                and ("f^{-1}" in source_words or "preimage" in source_words)):
            flag("review", "submersive_iff_surjectivity_scope", fid, node,
                 "The open-preimage biconditional alone does not imply "
                 "surjectivity. Confirm that the equivalence is asserted "
                 "only for surjective maps; this is a wording/scope lead "
                 "rather than a certified mathematical error.")
        for i, ref in enumerate(node["references"]):
            phrase = norm(ref.get("phrase", ""))
            target = ref.get("target_meaning_id")
            if ref["state"] == "existing":
                if target not in meanings:
                    flag("integrity", "unknown_existing_target", fid, node,
                         "Target meaning not found in independent inventory.",
                         index=i, reference=ref)
                    continue
                adjacency[source["meaning_id"]].add(target)
                edge_count += 1
                if target == source["meaning_id"]:
                    flag("high", "self_dependency", fid, node,
                         "Reference points back to the meaning being defined.",
                         index=i, reference=ref)
                if target == SMALL_CATEGORY:
                    if "parallel" in phrase:
                        flag("high", "parallel_arrows_linked_to_small_category",
                             fid, node, "A parallel-arrow construction is not "
                             "the small-category concept.", index=i, reference=ref)
                    elif ("category" in phrase and
                          "category c" in norm(source["text"]) and
                          not re.search(r"\b(small|finite)\s+category\s+c\b",
                                        norm(source["text"]))):
                        flag("review", "category_size_scope", fid, node,
                             "Ambient C is not explicitly assumed small in the "
                             "source. Check whether this link silently adds a "
                             "smallness hypothesis.", index=i, reference=ref)
                if target == SMALL_GROUPOID and "groupoid" in phrase:
                    # The only existing groupoid meaning requires a small
                    # category. An arbitrary hom-category or fibre groupoid
                    # need not be small. A literal Groupoids target category
                    # denotes small groupoids in this independent corpus.
                    source_text = source["text"]
                    explicitly_small = bool(re.search(
                        r"\b(small|finite)\s+groupoids?\b",
                        norm(source_text)))
                    typed_groupoids = bool(re.search(
                        r"\bGroupoids\b", source_text))
                    if not explicitly_small and not typed_groupoids:
                        flag("review", "groupoid_size_scope", fid, node,
                             "The only existing groupoid meaning explicitly "
                             "requires smallness; the source does not. Check "
                             "whether this edge adds an unsupported size "
                             "restriction. It is a review lead, not a "
                             "certified error.", index=i, reference=ref)
                if target == FINITE_MODULE and "ideal" in phrase:
                    flag("review", "ideal_vs_module_generation", fid, node,
                         "Check whether finite generation of an ideal is "
                         "correctly represented by the module target, including "
                         "the exact required number of generators.",
                         index=i, reference=ref)
            elif ref["state"] == "missing":
                cid = ref.get("missing_candidate_id")
                if cid not in candidate_ids:
                    flag("integrity", "unregistered_missing_candidate", fid, node,
                         "Missing reference does not match the saved shared "
                         "candidate registry.", index=i, reference=ref)
                # A full-node reviewer may deliberately reuse a previously
                # registered contextual candidate instead of minting an
                # otherwise redundant raw ID. The review packet must preserve
                # the original phrase and supply explicit evidence of that
                # choice. Never accept an unexplained ID/phrase mismatch.
                # The reviewer's identity is retained by the validated
                # append-only amendment event, not necessarily the reference.
                reviewed_reuse = (
                    ref.get("reviewed_existing_candidate_id") == cid
                    and len(str(ref.get(
                        "candidate_identity_review_rationale", "")).strip()) >= 40
                )
                if (missing_key(ref["phrase"], ref["context"]) != cid
                        and not reviewed_reuse):
                    flag("integrity", "stale_missing_identity", fid, node,
                         "Phrase + context do not hash to the persisted missing "
                         "candidate identity, nor is this explicitly reviewed "
                         "candidate identity reuse.", index=i, reference=ref)
            elif ref["state"] in ("unassigned", "ambiguous", "deferred"):
                flag("review", "unresolved_occurrence", fid, node,
                     "Reference still requires contextual adjudication.",
                     index=i, reference=ref)

    # Reviewed historical seed overrides hide their original restricted target
    # from effective adjacency, but never mutate immutable seed evidence.
    canonical_candidates = {
        c["id"]: c["alias_of"] for c in snapshot.get("candidates", [])
        if c.get("alias_of")}
    seed_overrides = replay_seed_overrides(
        inv, snapshot.get("seed_override_events", []),
        scan_missing_sources(nodes, canonical_candidates),
        aliased={x["alias_candidate_id"] for x in snapshot.get("aliases", [])},
        resolved=set(snapshot.get("resolved_candidate_ids", [])))
    counts["effective_seed_override_count"] = len(seed_overrides)
    # Combine authoritative seed relations with the effective append-only scan
    # graph. Never infer completeness from scan edges alone; deferred legacy
    # seed targets are missing placeholders, not asserted dependencies.
    for seed in inv.get("seed_relations", []):
        if not seed.get("target_meaning_id"):
            continue
        fid, target = seed.get("from_formulation"), seed["target_meaning_id"]
        if seed["relation_id"] in seed_overrides:
            continue  # This historical link is replaced by a reviewed missing seed.
        if fid not in form or target not in meanings:
            counts["invalid_seed_relations"] += 1
            continue
        adjacency[form[fid]["meaning_id"]].add(target)
        seed_edges += 1
        # Legacy seed edges are *independent authoritative relations*, not
        # overwritten by later contextual scan amendments. Audit their type
        # assumptions independently, rather than mistaking fixed scan links
        # for proof that all historical seed targets are appropriate.
        words = norm(form[fid]["text"])
        has_small_category = bool(re.search(
            r"\b(small|finite)\s+categor(?:y|ies)\b", words))
        has_small_groupoid = bool(re.search(
            r"\b(small|finite)\s+groupoids?\b", words))
        typed_groupoids = bool(re.search(
            r"\bGroupoids\b", form[fid]["text"]))
        reason = None
        code = None
        if target == SMALL_CATEGORY and not has_small_category:
            code = "legacy_seed_category_size_scope"
            reason = ("Pre-existing seed targets the explicitly small-category "
                      "meaning, but this source does not state that its ambient "
                      "category is small. Review the seeded prerequisite "
                      "separately from effective scan amendments.")
        elif target == SMALL_GROUPOID and not (has_small_groupoid or typed_groupoids):
            code = "legacy_seed_groupoid_size_scope"
            reason = ("Pre-existing seed targets the explicitly small-groupoid "
                      "meaning, but the source does not establish smallness. "
                      "Preserve invertibility and verify the size convention.")
        elif (target == "meaning.wave2.foundation.category-functor"
              and not has_small_category):
            code = "legacy_seed_functor_size_scope"
            reason = ("Pre-existing seed points to the small-category functor "
                      "meaning, while source functors do not explicitly have "
                      "small domain and codomain categories.")
        if code:
            flag("review", code, fid, nodes.get(fid),
                 reason + " Legacy relation ID: " + seed["relation_id"],
                 reference={
                     "phrase": seed.get("phrase", ""),
                     "state": "existing",
                     "target_meaning_id": target,
                     "origin": "preexisting_seed_relation",
                     "relation_id": seed["relation_id"],
                     "occurrence_id": "legacy-seed:" + seed["relation_id"],
                 })
    from research_pipeline.engine.dependency_cycle_analysis import analyze_cycles
    cycle_analysis = analyze_cycles(
        snapshot, include_all_edges=(include_cycle_edges or include_effective_snapshot))
    # Preserve the old restricted fields for existing CI consumers; the
    # separately scoped cycle_analysis is the full effective graph.
    cycles = strongly_connected(adjacency)
    for component in cycles:
        counts["cyclic_components"] += 1
        if len(component) > 1:
            counts["cyclic_meanings"] += len(component)
    # Priority is impact-aware, but only a *reviewer's exact anchored decision*
    # may mark a heuristic warning as accepted. Structural alerts stay visible.
    ranked = rank_findings(findings, nodes, inv, snapshot.get("review_ledger", []))
    counts["cycle_edges_review_required"] = len(cycles)
    complete = sum(n.get("scan_status") == "complete" for n in nodes.values())
    summary = {
        "inventory_sha256": inv["source_inventory_sha256"],
        "state_unresolved_fingerprint": state.get("unresolved_fingerprint"),
        "phase": state.get("phase"),
        "consolidation_gate_valid": state.get("consolidation_gate_valid"),
        "meaning_count": len(meanings),
        "formulation_count": len(form),
        "complete_effective_formulations": complete,
        "existing_dependency_edges": edge_count + seed_edges,
        "scan_dependency_edges": edge_count,
        "seed_dependency_edges": seed_edges,
        "distinct_existing_dependency_pairs": sum(map(len, adjacency.values())),
        "cycle_components": len(cycles),
        "cycle_components_scope": "legacy_direct_scan_and_unoverridden_existing_seeds",
        "effective_cycle_components": len(cycle_analysis["components"]),
        "formulation_avoidable_cycle_components": sum(
            c["classification"] == "avoidable_by_formulation_choice"
            for c in cycle_analysis["components"]),
        "unavoidable_cycle_components": sum(
            c["classification"] == "unavoidable_under_stored_formulations"
            for c in cycle_analysis["components"]),
        "undetermined_cycle_components": sum(
            c["classification"] == "undetermined_incomplete_formulations"
            for c in cycle_analysis["components"]),
        "effective_existing_dependency_edges": cycle_analysis["edge_count"],
        "unassigned_occurrences": state.get("unassigned_occurrences"),
        "ambiguous_occurrences": state.get("ambiguous_occurrences"),
        "total_flags": len(findings),
        "review_queue_count": len(ranked["needing_review"]),
        "accepted_review_count": ranked["accepted_count"],
        "stale_review_count": ranked["stale_review_count"],
        "flags_by_code": dict(sorted(counts.items())),
    }
    report = {
        "schema_version": 1, "read_only": True,
        "mathematics_certified": False,
        "external_research_performed": False,
        "automatic_aliases_or_edits": False,
        "summary": summary,
        "graph_cycle_components": cycles,
        "graph_cycle_components_scope": summary["cycle_components_scope"],
        "cycle_analysis": cycle_analysis,
        "graph_cycle_includes_seed_relations": True,
        "graph_cycle_includes_candidate_resolutions": False,
        "returned_flags": min(max(0, limit), len(ranked["needing_review"])),
        "flags": ranked["needing_review"][:max(0, limit)],
        "review_queue_by_code": ranked["review_by_code"],
        "reviewed_accepted_preview": ranked["accepted"][:10],
        "candidate_surface_review": candidate_leads(candidates, candidate_limit),
        "warning": "Potential contextual mismatches are REVIEW LEADS, not "
                   "confirmed mathematical errors. Acyclicity and passing CI "
                   "do not imply mathematical rigor or source certification.",
    }
    if include_effective_snapshot:
        report["all_review_queue"] = ranked["needing_review"]
        report["accepted_review_ledger_matches"] = ranked["accepted"]
        report["effective_formulations"] = {
            fid: {
                "source": form[fid],
                "effective_node": nodes.get(fid),
                "effective_node_sha256": digest(nodes[fid]) if fid in nodes else None,
                "reference_template": [
                    {k: v for k, v in ref.items() if k != "occurrence_id"}
                    for ref in nodes[fid]["references"]
                ] if fid in nodes else [],
            } for fid in sorted(form)
        }
    if "candidate_context_reviews" in snapshot:
        from .dependency_context_reviews import validated_view
        report["candidate_context_reviews"] = validated_view(snapshot)
    return report


def build_review_packages(snapshot: dict, manifest: dict,
                          max_per_batch: int = 5) -> list[dict]:
    """Prepare complete anchored packages from explicit decisions; NO guessing.

    Same-formulation decisions combine into one whole effective-node amendment.
    At most five DISTINCT formulations go in each packet. Duplicate edits and
    new missing-candidate identities are rejected for this audit phase.
    """
    if not 1 <= max_per_batch <= 5:
        raise PipelineError("At most five complete formulations per packet")
    inv, nodes = snapshot["inventory"], snapshot["nodes"]
    if manifest.get("schema_version") != 1:
        raise PipelineError("Reviewed manifest schema_version must equal 1")
    label = manifest.get("id")
    if not isinstance(label, str) or not KEY_RE.fullmatch(label):
        raise PipelineError("Safe, unique review manifest id required")
    if (manifest.get("inventory_sha256") != inv["source_inventory_sha256"]
            or manifest.get("unresolved_fingerprint") !=
            snapshot["state"]["summary"]["unresolved_fingerprint"]):
        raise PipelineError("Reviewed manifest is stale against live graph fingerprint")
    reviewer = manifest.get("reviewed_by")
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise PipelineError("Named contextual reviewer required")
    changes = manifest.get("changes")
    if not isinstance(changes, list) or not changes:
        raise PipelineError("At least one explicitly reviewed change required")
    existing_candidates = {c["id"] for c in snapshot.get("candidates", [])}
    by_form = defaultdict(list)
    for edit in changes:
        by_form[edit.get("formulation_id")].append(edit)
    reusable = {row["id"] for row in snapshot.get("candidates", [])
                if row.get("status") == "unresearched"
                and not row.get("alias_of")
                and not row.get("resolved_target_meaning_id")}
    packets, pending = [], []
    for fid in sorted(by_form):
        source, prior = inv["formulations"].get(fid), nodes.get(fid)
        if not source or not prior or prior.get("scan_status") != "complete":
            raise PipelineError("Unknown or incomplete effective formulation: " + str(fid))
        old_hash = digest(prior)
        refs = [{k: v for k, v in ref.items() if k != "occurrence_id"}
                for ref in prior["references"]]
        modified = set()
        reasons = []
        for edit in by_form[fid]:
            # Prefer the stable, live-node occurrence identity over an index
            # derived from a mixed scan/seed audit view. Legacy manifests that
            # include a numeric index stay valid but MUST agree with this ID.
            occurrence_id = edit.get("expected_occurrence_id")
            if not isinstance(occurrence_id, str) or not occurrence_id:
                raise PipelineError("Missing expected_occurrence_id for " + fid)
            matching = [
                i for i, ref in enumerate(prior["references"])
                if ref.get("occurrence_id") == occurrence_id
            ]
            if len(matching) != 1:
                raise PipelineError(
                    "Missing or nonunique live occurrence identity for " + fid
                    + ": " + occurrence_id
                )
            index = matching[0]
            supplied_index = edit.get("reference_index")
            if supplied_index is not None and (
                    not isinstance(supplied_index, int)
                    or isinstance(supplied_index, bool)
                    or supplied_index != index):
                raise PipelineError(
                    "reference_index conflicts with live occurrence identity for "
                    + fid + ": " + occurrence_id
                )
            original = prior["references"][index]
            if (index in modified or edit.get("expected_node_sha256") != old_hash):
                raise PipelineError("Duplicate edit or stale effective occurrence: " + fid)
            # Prefer an explicitly reviewed *delta*: leave untouched metadata
            # and unrelated context identical, instead of manually retyping
            # the entire original reference. Full replacement remains supported.
            replacement = edit.get("replacement")
            updates = edit.get("updates")
            rationale = edit.get("reason", "")
            if len(str(rationale).strip()) < 40:
                raise PipelineError("Substantive mathematical change rationale required")
            if (replacement is None) == (updates is None):
                raise PipelineError("Supply exactly one of replacement or updates")
            if updates is not None:
                if not isinstance(updates, dict) or not updates:
                    raise PipelineError("Delta updates must be a nonempty dictionary")
                removals = edit.get("remove_fields", [])
                if (not isinstance(removals, list) or
                        any(not isinstance(k, str) for k in removals)):
                    raise PipelineError("remove_fields must list reference keys")
                forbidden = {"occurrence_id", "missing_candidate_id", "span"}
                if forbidden & set(updates) or forbidden & set(removals):
                    raise PipelineError("Reviewer cannot assign generated or span metadata")
                new = dict(refs[index])
                for name in removals:
                    new.pop(name, None)
                new.update(updates)
            else:
                if not isinstance(replacement, dict):
                    raise PipelineError("Reviewed full replacement must be a dictionary")
                new = replacement
            if "occurrence_id" in new:
                raise PipelineError("Occurrence IDs are generated, not editor-assigned")
            if (new.get("state") != "existing" and "target_meaning_id" in new):
                raise PipelineError("Non-existing reference retains a stale target")
            if new.get("state") == "existing" and "missing_candidate_id" in new:
                raise PipelineError("Existing reference retains stale missing identity")
            if new.get("state") == "missing":
                if not str(new.get("context", "")).strip():
                    raise PipelineError("Missing references require mathematical context")
                reviewed = new.get("reviewed_existing_candidate_id")
                target_id = reviewed or missing_key(new.get("phrase", ""), new.get("context", ""))
                if target_id not in existing_candidates:
                    raise PipelineError("Cannot silently invent missing-candidate identities")
            if new == refs[index]:
                raise PipelineError("No-op edit: " + fid)
            refs[index] = new
            reasons.append(str(rationale).strip())
            modified.add(index)
        review_text = manifest.get("review_rationale", "")
        if len(str(review_text).strip()) < 40:
            raise PipelineError("Whole-package mathematical review rationale required")
        full_rationale = (f"{review_text} Reviewed entire source formulation "
                          f"'{source['display_term']}' and the complete effective "
                          f"predecessor reference list; {len(modified)} references changed.")
        # Validate an entire regenerated snapshot, *before writing any files*.
        make_snapshot(inv, fid, refs, "complete", full_rationale,
                      reusable_missing_candidate_ids=reusable)
        pending.append({
            "amendment_id": f"amend.{label}.{len(pending)+1:04d}",
            "formulation_id": fid, "version_sha256": source["version_sha256"],
            "expected_node_sha256": old_hash, "complete": True,
            "references": refs, "reviewed_by": reviewer,
            "reason": " ".join(reasons), "review_rationale": full_rationale,
        })
    for start in range(0, len(pending), max_per_batch):
        index = len(packets) + 1
        batch_id = f"{label}-{index:03d}"
        packets.append({
            "schema_version": 1, "id": batch_id, "mode": "amend",
            "research_scope": "Explicitly reviewed, source-free contextual "
                              "audit. No meanings added; not automatically certified.",
            "amendments": pending[start:start + max_per_batch],
        })
    return packets


def write_offline_packets(workspace: Path, manifest_path: Path,
                          output_dir: Path, max_per_batch: int = 5) -> dict:
    """Offline preparation only: validate ALL decisions, then write preflights."""
    output_dir = Path(output_dir).resolve()
    if output_dir.is_relative_to(graph_path(workspace).resolve()):
        raise PipelineError("Offline output must stay outside the dependency graph")
    snapshot = load_live_snapshot(workspace)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    packets = build_review_packages(snapshot, manifest, max_per_batch)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = [output_dir / (p["id"] + ".json") for p in packets]
    if any(p.exists() for p in paths):
        raise PipelineError("Refusing to overwrite existing reviewed batch files")
    try:
        for path, packet in zip(paths, packets):
            path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
        # The builder groups all changes to a formulation into one amendment;
        # packets are therefore disjoint. Each preflight still simulates its
        # own node dictionary, with unchanged authoritative preconditions.
        prepared = prepare_review_context(workspace)
        preflight = [review_preflight(workspace, path, prepared_context=prepared)
                     for path in paths]
    except Exception:
        for path in paths:
            path.unlink(missing_ok=True)
        raise
    return {
        "status": "offline_review_packets_prepared_not_committed",
        "read_only_graph": True, "human_certified": False,
        "packet_count": len(packets),
        "changed_formulation_count": sum(len(p["amendments"]) for p in packets),
        "files": [str(p) for p in paths], "preflight": preflight,
        "next_step": "Review ALL generated packets and submit only after "
                     "contextual mathematical approval; verify CI + receipts.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--context-review-log", type=Path)
    parser.add_argument("--context-review-checkpoint", type=Path)
    parser.add_argument("--qualification-ledger", type=Path)
    sub = parser.add_subparsers(dest="mode", required=True)
    scan = sub.add_parser("scan", help="Whole-graph diagnostic read-only review leads")
    scan.add_argument("--limit", type=int, default=60)
    scan.add_argument("--candidate-limit", type=int, default=40)
    scan.add_argument("--include-cycle-edges", action="store_true",
                      help="Include every effective existing-meaning edge in the JSON report; "
                           "normally only cyclic-component edges are returned")
    scan.add_argument("--snapshot-output", type=Path,
                      help="Optional TEMPORARY exhaustive snapshot outside the repository")
    focus = sub.add_parser("focus", help="Compact source-complete unresolved-candidate worklist")
    focus.add_argument("--candidate-id", action="append", default=[],
                       help="Exact unresolved canonical candidate; repeatable")
    focus.add_argument("--limit", type=int, default=8)
    focus.add_argument("--max-formulations", type=int, default=3)
    focus.add_argument("--contains", default="",
                       help="Filter candidate query/context when no IDs supplied")
    focus.add_argument("--parent-budget", type=int,
                       help="Bound full candidate/parent visits in priority order; "
                            "an oversized first candidate is emitted with a warning")
    focus.add_argument("--compact-sources", action="store_true",
                       help="Schema v2: emit full contexts once in source_contexts; "
                            "candidate rows keep exact occurrence matches")
    prep = sub.add_parser("prepare", help="Offline anchored full-node amendment packets")
    prep.add_argument("--manifest", type=Path, required=True)
    prep.add_argument("--output-dir", type=Path, required=True)
    prep.add_argument("--max-per-batch", type=int, default=5)
    args = parser.parse_args()
    if bool(args.context_review_log) != bool(args.context_review_checkpoint):
        parser.error("Context review log and trusted checkpoint must be supplied together")
    if args.qualification_ledger and not args.context_review_log:
        parser.error("Qualification ledger requires an explicit context review log")
    if args.mode == "prepare" and args.context_review_log:
        parser.error("Context metadata is analysis-only; graph preparation does not consume it")
    snapshot = None
    if args.mode in ("scan", "focus"):
        if args.context_review_log:
            from .dependency_context_reviews import attach_review_files, load_context_snapshot
            snapshot = attach_review_files(load_context_snapshot(args.workspace), args.context_review_log,
                args.context_review_checkpoint, qualification_ledger_path=args.qualification_ledger)
        else:
            snapshot = load_live_snapshot(args.workspace)
    if args.mode == "scan":
        report = analyze_snapshot(snapshot, limit=args.limit,
                                  candidate_limit=args.candidate_limit,
                                  include_cycle_edges=args.include_cycle_edges)
        if args.snapshot_output:
            complete_report = analyze_snapshot(
                snapshot, limit=10**9, candidate_limit=10**9,
                include_effective_snapshot=True)
            args.snapshot_output.parent.mkdir(parents=True, exist_ok=True)
            args.snapshot_output.write_text(
                json.dumps(complete_report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8")
            report["temporary_full_snapshot_path"] = str(args.snapshot_output)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.mode == "focus":
        print(json.dumps(candidate_review_bundle(
            snapshot,
            candidate_ids=tuple(args.candidate_id), limit=args.limit,
            max_formulations=args.max_formulations, contains=args.contains,
            parent_budget=args.parent_budget, compact_sources=args.compact_sources),
            ensure_ascii=False, indent=2))
    else:
        print(json.dumps(write_offline_packets(
            args.workspace, args.manifest, args.output_dir, args.max_per_batch),
            ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
