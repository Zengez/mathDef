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
from research_pipeline.engine.dependency_review_preflight import review_preflight
from research_pipeline.engine.dependency_audit_acceleration import (
    notation_aware_leads, rank_findings,
)


SMALL_CATEGORY = "meaning.wave2.foundation.small-category"
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
    return {
        "inventory": inv, "state": state, "nodes": nodes,
        "candidates": jsonl(graph / "missing_candidates.jsonl"),
        "aliases": jsonl(graph / "candidate_aliases.jsonl"),
        "review_ledger": jsonl(graph / "audit_review_decisions.jsonl"),
    }


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
                     include_effective_snapshot: bool = False) -> dict:
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
                if missing_key(ref["phrase"], ref["context"]) != cid:
                    flag("integrity", "stale_missing_identity", fid, node,
                         "Phrase + context do not hash to the persisted missing "
                         "candidate identity.", index=i, reference=ref)
            elif ref["state"] in ("unassigned", "ambiguous", "deferred"):
                flag("review", "unresolved_occurrence", fid, node,
                     "Reference still requires contextual adjudication.",
                     index=i, reference=ref)

    # Combine authoritative seed relations with the effective append-only scan
    # graph. Never infer completeness from scan edges alone; deferred legacy
    # seed targets are missing placeholders, not asserted dependencies.
    for seed in inv.get("seed_relations", []):
        if not seed.get("target_meaning_id"):
            continue
        fid, target = seed.get("from_formulation"), seed["target_meaning_id"]
        if fid not in form or target not in meanings:
            counts["invalid_seed_relations"] += 1
            continue
        adjacency[form[fid]["meaning_id"]].add(target)
        seed_edges += 1
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
        "graph_cycle_includes_seed_relations": True,
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
            index = edit.get("reference_index")
            if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < len(refs):
                raise PipelineError("Invalid reference_index for " + fid)
            original = prior["references"][index]
            if (index in modified or edit.get("expected_node_sha256") != old_hash
                    or edit.get("expected_occurrence_id") != original.get("occurrence_id")):
                raise PipelineError("Duplicate edit or stale effective occurrence: " + fid)
            new = edit.get("replacement")
            rationale = edit.get("reason", "")
            if not isinstance(new, dict) or len(str(rationale).strip()) < 40:
                raise PipelineError("Reviewed full replacement and 40-character reason required")
            if "occurrence_id" in new:
                raise PipelineError("Occurrence IDs are generated, not editor-assigned")
            if new.get("state") == "missing":
                if missing_key(new.get("phrase", ""), new.get("context", "")) not in existing_candidates:
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
        make_snapshot(inv, fid, refs, "complete", full_rationale)
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
        preflight = [review_preflight(workspace, path) for path in paths]
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
    sub = parser.add_subparsers(dest="mode", required=True)
    scan = sub.add_parser("scan", help="Whole-graph diagnostic read-only review leads")
    scan.add_argument("--limit", type=int, default=60)
    scan.add_argument("--candidate-limit", type=int, default=40)
    scan.add_argument("--snapshot-output", type=Path,
                      help="Optional TEMPORARY exhaustive snapshot outside the repository")
    prep = sub.add_parser("prepare", help="Offline anchored full-node amendment packets")
    prep.add_argument("--manifest", type=Path, required=True)
    prep.add_argument("--output-dir", type=Path, required=True)
    prep.add_argument("--max-per-batch", type=int, default=5)
    args = parser.parse_args()
    if args.mode == "scan":
        snapshot = load_live_snapshot(args.workspace)
        report = analyze_snapshot(snapshot, limit=args.limit,
                                  candidate_limit=args.candidate_limit)
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
    else:
        print(json.dumps(write_offline_packets(
            args.workspace, args.manifest, args.output_dir, args.max_per_batch),
            ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
