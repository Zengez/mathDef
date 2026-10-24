"""Crash-replay-safe, domain-neutral dependency graph for independent research.

Nodes are complete, version-bound snapshots; derived indexes and checkpoints are
rebuildable and NEVER serve as evidence that unscanned contents were exhausted.
All writes remain isolated under workspace/dependency_graph.
"""
from __future__ import annotations

import argparse
import importlib
import hashlib
import json
import re
from collections import defaultdict, Counter
from pathlib import Path

from .core import PipelineError, Workspace, digest, atomic_json
from .population import snapshot, write_atomic
from .dependency_seed_overrides import (
    read_events as seed_override_events, replay_seed_overrides,
    scan_missing_sources, effective_seed_reference,
)

SCHEMA = 1
GRAPH_DIR = "dependency_graph"
KEY_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


def norm(value):
    return " ".join(str(value).casefold().split())


def graph_path(workspace):
    return Path(workspace) / GRAPH_DIR


def read(path, fallback=None):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else fallback


def read_node(path):
    try:
        return read(path)
    except json.JSONDecodeError:
        # Interrupted partial node files must never masquerade as completed scans.
        return None


def stable_id(prefix, item):
    return prefix + "." + digest(item)[:20]


def collect(workspace):
    """Read ONLY the isolated independent Wave2 and its provisional population."""
    base = Workspace(workspace)
    cfg = base.config()
    if cfg.get("independent_second_wave") is not True:
        raise PipelineError("Dependency graph requires an independent Wave2 workspace")
    draft, revisions = snapshot(workspace)
    meanings = {**base.records("meanings"), **draft["meanings"]}
    relations = {**base.records("relations"), **draft["relations"]}
    observations = {**base.records("observations"), **draft["observations"]}
    sources = {**base.records("sources"), **draft["sources"]}
    inventory = {}
    for mid, meaning in sorted(meanings.items()):
        for form in meaning.get("formulations", []):
            fid = form["id"]
            if fid in inventory:
                raise PipelineError("Repeated formulation ID: " + fid)
            evidence = [observations[x] for x in form.get("evidence_ids", []) if x in observations]
            source_ids = sorted({x.get("source_id") for x in evidence if x.get("source_id")})
            provenance = {"observations": evidence,
                          "sources": [sources[x] for x in source_ids if x in sources]}
            content = {"formulation": form, "context": meaning["context"],
                       "source_snapshot_sha256": digest(provenance)}
            inventory[fid] = {
                "formulation_id": fid, "meaning_id": mid, "display_term": meaning["display_term"],
                "context": meaning["context"],
                "origin": "provisional" if mid in draft["meanings"] else "screened",
                "version_sha256": digest(content),
                "source_snapshot_sha256": digest(provenance),
                "evidence_ids": form.get("evidence_ids", []),
                "text": form["text"],
            }
    seeds = []
    for rel in sorted(relations.values(), key=lambda x: x["id"]):
        if rel.get("relation_type") != "definition_uses":
            continue
        if rel.get("from_formulation") not in inventory:
            raise PipelineError("Relation from absent formulation: " + rel["id"])
        if rel.get("target_meaning") and rel["target_meaning"] not in meanings:
            raise PipelineError("Relation to absent meaning: " + rel["id"])
        seeds.append({
            "relation_id": rel["id"], "from_formulation": rel["from_formulation"],
            "target_meaning_id": rel.get("target_meaning"),
            "target_query": rel.get("target_query"),
            "phrase": rel.get("source_phrase") or rel.get("target_query") or "",
            "provenance": "provisional" if rel["id"] in draft["relations"] else "screened",
            "relation_state": rel.get("review_state", "candidate"),
        })
    return inventory, meanings, seeds, revisions


def inventory_sync(workspace):
    graph = graph_path(workspace)
    graph.mkdir(parents=True, exist_ok=True)
    entries, meanings, seeds, revisions = collect(workspace)
    old = read(graph / "INVENTORY.json", {})
    prior = old.get("formulations", {})
    changed = sorted(k for k in entries if k not in prior or
                     prior[k]["version_sha256"] != entries[k]["version_sha256"])
    removed = sorted(set(prior) - set(entries))
    manifest = {
        "schema_version": SCHEMA, "mode": "independent_wave2_dependency_first",
        "formulations": entries,
        "meanings": {k: {"display_term": v["display_term"], "context": v["context"],
                         "formulation_ids": [f["id"] for f in v.get("formulations", [])]}
                     for k, v in sorted(meanings.items())},
        "seed_relations": seeds, "revision_count": len(revisions),
        "source_inventory_sha256": digest(entries), "seed_relations_sha256": digest(seeds),
        "production_corpus_consulted": False,
        "breadth_expansion": "on_hold",
    }
    if old != manifest:
        atomic_json(graph / "INVENTORY.json", manifest)
    result = rebuild(workspace, manifest)
    result["changed_or_added_formulations"] = len(changed)
    result["removed_formulations"] = len(removed)
    return result


def node_file(graph, fid):
    if not KEY_RE.fullmatch(fid) or "/" in fid or fid.startswith("."):
        raise PipelineError("Unsafe formulation identifier: " + fid)
    return graph / "nodes" / (fid + ".json")


def amendment_events(graph):
    """Append-only snapshots; the node file remains immutable after correction."""
    file = graph / "amendments.jsonl"
    if not file.exists():
        return []
    return [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def live_nodes(graph, inv):
    nodes = {}
    for fid, entry in inv["formulations"].items():
        node = read_node(node_file(graph, fid))
        if node is None:
            continue
        if (node.get("formulation_id") != fid or
                node.get("version_sha256") != entry["version_sha256"] or
                node.get("schema_version") != SCHEMA):
            continue  # Old version stays visible for audit but never used as live adjacency.
        refs = node.get("references")
        if not isinstance(refs, list) or node.get("snapshot_sha256") != digest(refs):
            continue  # Part-written or corrupt node is never considered scanned.
        nodes[fid] = node
    # Apply only events for the active formulation version, strictly in
    # append order. A broken link in the correction chain invalidates the
    # entire formulation; it can NEVER be treated as safely completed.
    invalid = set()
    seen_ids = set()
    for event in amendment_events(graph):
        event_id = event.get("amendment_id")
        if not isinstance(event_id, str) or event_id in seen_ids:
            raise PipelineError("Missing or repeated graph amendment ID")
        seen_ids.add(event_id)
        fid = event.get("formulation_id")
        entry = inv["formulations"].get(fid)
        if not entry or event.get("version_sha256") != entry["version_sha256"]:
            continue  # Historical version; retained for audit, not applied.
        current = nodes.get(fid)
        replacement = event.get("replacement")
        if (fid in invalid or current is None or
                event.get("expected_node_sha256") != digest(current) or
                not isinstance(replacement, dict) or
                replacement.get("formulation_id") != fid or
                replacement.get("version_sha256") != entry["version_sha256"] or
                replacement.get("snapshot_sha256") != digest(replacement.get("references"))):
            invalid.add(fid)
            nodes.pop(fid, None)
            continue
        nodes[fid] = replacement
    return nodes


def _reference_state(ref, meanings, missing):
    state = ref.get("state")
    if state not in ("existing", "missing", "ambiguous", "external", "deferred", "unassigned"):
        raise PipelineError("Unknown reference state")
    if state == "existing" and ref.get("target_meaning_id") not in meanings:
        raise PipelineError("Existing dependency must target an inventory meaning")
    if state == "missing" and ref.get("missing_candidate_id") not in missing:
        raise PipelineError("Missing reference must target a registered candidate")
    if state in ("ambiguous", "deferred") and not ref.get("reason"):
        raise PipelineError("Ambiguous/deferred references need an explicit reason")
    if state == "unassigned" and not str(ref.get("context", "")).strip():
        raise PipelineError("Unassigned occurrence needs its local context, not a premature meaning")
    if state == "external" and not ref.get("disposition"):
        raise PipelineError("External/primitve reference requires a justified disposition")


def meaning_version(inv, mid):
    """Version-pin a meaning AND every associated formulation's full contents."""
    desc = inv["meanings"][mid]
    return digest({"meaning": desc, "formulation_versions": {
        fid: inv["formulations"][fid]["version_sha256"]
        for fid in sorted(desc["formulation_ids"])
    }})


def unresolved_fingerprint(inv, references, missing_candidates):
    """Stable phase-gate fingerprint, including evidence for all unresolved uses."""
    return digest({"inventory": inv["source_inventory_sha256"],
                   "occurrences": references,
                   "missing_candidates": missing_candidates})


def missing_key(phrase, context):
    return stable_id("missing", {"phrase": norm(phrase), "context": norm(context)})


def alias_map(graph, available, events=None):
    """Replay reviewed, flat missing-candidate aliases without losing identity."""
    path = graph / "candidate_aliases.jsonl"
    events = (events if events is not None else
              [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
               if line.strip()] if path.exists() else [])
    aliases = {}
    seen = set()
    for event in events:
        key = event.get("alias_candidate_id")
        target = event.get("canonical_candidate_id")
        eid = event.get("alias_id")
        if not eid or eid in seen:
            raise PipelineError("Repeated/invalid missing alias event ID")
        seen.add(eid)
        if key not in available or target not in available:
            continue  # Historical aliases are retained if sources are removed.
        if key == target or key in aliases or target in aliases:
            raise PipelineError("Conflicting or chained missing alias (use canonical target)")
        if not event.get("reviewed_by") or len(event.get("reason", "").strip()) < 40:
            raise PipelineError("Missing alias requires substantive contextual review")
        aliases[key] = target
    return aliases


def rebuild(workspace, inventory=None):
    """Reconstruct every derived index from committed version-valid node snapshots."""
    graph = graph_path(workspace)
    inv = inventory or read(graph / "INVENTORY.json")
    if not inv:
        raise PipelineError("First generate INVENTORY.json")
    nodes = live_nodes(graph, inv)
    meanings = inv["meanings"]
    candidate_map = {}
    refs_by_form = defaultdict(list)
    events = seed_override_events(graph)
    if events:
        alias_file = graph / "candidate_aliases.jsonl"
        resolution_file = graph / "resolutions.jsonl"
        previously_aliased = ({json.loads(line)["alias_candidate_id"]
            for line in alias_file.read_text(encoding="utf-8").splitlines()
            if line.strip()} if alias_file.exists() else set())
        previously_resolved = ({json.loads(line)["missing_candidate_id"]
            for line in resolution_file.read_text(encoding="utf-8").splitlines()
            if line.strip()} if resolution_file.exists() else set())
        overrides = replay_seed_overrides(
            inv, events, scan_missing_sources(nodes),
            aliased=previously_aliased, resolved=previously_resolved)
    else:
        overrides = {}
    for seed in inv["seed_relations"]:
        fid = seed["from_formulation"]
        if seed["relation_id"] in overrides:
            refs_by_form[fid].append(effective_seed_reference(
                seed, overrides[seed["relation_id"]],
                stable_id("seed", seed["relation_id"])))
        elif seed.get("target_query") and not seed.get("target_meaning_id"):
            k = missing_key(seed["target_query"], inv["formulations"][fid]["context"])
            candidate_map[k] = {
                "id": k, "query": seed["target_query"],
                "context": inv["formulations"][fid]["context"],
                "source": "preexisting_deferred_relation", "status": "unresearched",
            }
            refs_by_form[fid].append({
                "occurrence_id": stable_id("seed", seed["relation_id"]),
                "phrase": seed["phrase"], "state": "missing",
                "missing_candidate_id": k, "relation_id": seed["relation_id"],
                "origin": "preexisting_relation",
            })
        elif seed.get("target_meaning_id"):
            refs_by_form[fid].append({
                "occurrence_id": stable_id("seed", seed["relation_id"]),
                "phrase": seed["phrase"], "state": "existing",
                "target_meaning_id": seed["target_meaning_id"],
                "relation_id": seed["relation_id"],
                "origin": "preexisting_relation",
            })
    for fid, node in nodes.items():
        for ref in node["references"]:
            if ref["state"] == "missing":
                k = ref["missing_candidate_id"]
                candidate_map.setdefault(k, {
                    "id": k, "query": ref["phrase"], "context": ref.get("context", ""),
                    "source": "reference_scan", "status": "unresearched",
                })
            refs_by_form[fid].append(ref)
    aliases = alias_map(graph, candidate_map)
    resolutions = {}
    resolution_file = graph / "resolutions.jsonl"
    saved_resolutions = (json.loads(line) for line in
        resolution_file.read_text(encoding="utf-8").splitlines() if line.strip()
    ) if resolution_file.exists() else ()
    for resolution in saved_resolutions:
        key, mid = resolution["missing_candidate_id"], resolution["target_meaning_id"]
        if key in resolutions:
            raise PipelineError("Duplicate append-only candidate resolution " + key)
        if key not in candidate_map or mid not in meanings:
            continue  # A stale or no-longer-applicable review cannot close anything.
        if key in aliases:
            raise PipelineError("An aliased missing candidate cannot own a resolution")
        if resolution.get("target_version_sha256") != meaning_version(inv, mid):
            continue
        resolutions[key] = resolution
    reverse = defaultdict(set)
    outgoing = defaultdict(set)
    occurrences = []
    edges = []
    seen_occ = set()
    blockers = defaultdict(list)
    for fid in inv["formulations"]:
        for ref in refs_by_form[fid]:
            oid = ref["occurrence_id"]
            if oid in seen_occ:
                raise PipelineError("Duplicate occurrence: " + oid)
            seen_occ.add(oid)
            _reference_state(ref, meanings, candidate_map)
            effective = ref
            if ref["state"] == "missing" and ref["missing_candidate_id"] in aliases:
                original_key = ref["missing_candidate_id"]
                canonical_key = aliases[original_key]
                reverse["missing-alias:" + original_key].add(fid)
                effective = {**ref, "missing_candidate_id": canonical_key,
                             "observed_missing_candidate_id": original_key}
            if effective["state"] == "missing" and effective["missing_candidate_id"] in resolutions:
                key = effective["missing_candidate_id"]
                reverse["missing:" + key].add(fid)  # Retain traceability.
                effective = {**effective, "state": "existing",
                             "target_meaning_id": resolutions[key]["target_meaning_id"],
                             "resolved_missing_candidate_id": key,
                             "origin": ref.get("origin", "scan") + ":candidate_resolution"}
            occurrences.append({"from_formulation": fid, **effective})
            state = effective["state"]
            ref = effective
            if state == "existing":
                mid = ref["target_meaning_id"]
                reverse["meaning:" + mid].add(fid)
                outgoing[fid].update(meanings[mid]["formulation_ids"])
                edges.append({"from_formulation": fid, "target_meaning_id": mid,
                              "occurrence_id": oid, "origin": ref.get("origin", "scan")})
            elif state == "missing":
                reverse["missing:" + ref["missing_candidate_id"]].add(fid)
                blockers[fid].append("missing:" + ref["missing_candidate_id"])
            elif state in ("ambiguous", "deferred", "unassigned"):
                blockers[fid].append(state + ":" + oid)
    # A scanned node can be structurally closed only if no reachable node is
    # unscanned/ambiguous/missing. Propagate blockers backwards to a fixed point.
    unscanned = set(inv["formulations"]) - {fid for fid, node in nodes.items()
                  if node.get("scan_status") == "complete"}
    blocked = set(unscanned) | set(blockers)
    dependents = defaultdict(set)
    for src, targets in outgoing.items():
        for target in targets:
            dependents[target].add(src)
    todo = list(blocked)
    while todo:
        for parent in dependents[todo.pop()]:
            if parent not in blocked:
                blocked.add(parent)
                todo.append(parent)
    # Traversal completion and structural closure are different:
    # A may finish exploring every existing descendant while remaining
    # Open because a terminal missing meaning has not been researched.
    # Lexical proposals are NOT a completed semantic encounter.
    traversal_pending = set(unscanned)
    walk = list(traversal_pending)
    while walk:
        for parent in dependents[walk.pop()]:
            if parent not in traversal_pending:
                traversal_pending.add(parent)
                walk.append(parent)
    state_rows = {}
    for fid in inv["formulations"]:
        scan = nodes.get(fid, {}).get("scan_status", "unscanned")
        state_rows[fid] = {
            "scan_status": scan, "encountered": scan == "complete",
            "completed": fid not in traversal_pending,
            "structural_status": "open" if fid in blocked else "closed",
            "direct_blockers": blockers.get(fid, []) +
                (["scan_incomplete"] if scan != "complete" else []),
            "version_sha256": inv["formulations"][fid]["version_sha256"],
        }
    occurrences.sort(key=lambda x: (x["from_formulation"], x["occurrence_id"]))
    edges.sort(key=lambda x: (x["from_formulation"], x["occurrence_id"]))
    # Every occurrence survives even if it is not yet an identified missing
    # meaning. The first pass records evidence; the consolidation pass groups it.
    unresolved = [row for row in occurrences if row["state"] in
                  ("unassigned", "ambiguous", "missing", "deferred")]
    candidates = []
    for k, c in sorted(candidate_map.items()):
        incoming = sorted(reverse.get("missing:" + k, ()))
        candidate_status = ("alias" if k in aliases else
                            "resolved" if k in resolutions else "unresearched")
        candidates.append({**c, "status": candidate_status,
                           "alias_of": aliases.get(k),
                           "alias_ids": sorted(x for x, y in aliases.items() if y == k),
                           "resolved_target_meaning_id":
                               resolutions[k]["target_meaning_id"] if k in resolutions else None,
                           "incoming_formulation_ids": incoming,
                           "occurrence_count": sum(r.get("missing_candidate_id") == k
                               for r in occurrences),
                           "upstream_formulation_count": len(incoming)})
    def jsonl_output(name, rows):
        write_atomic(graph / name, "".join(json.dumps(x, sort_keys=True,
                     ensure_ascii=False) + "\n" for x in rows))
    jsonl_output("occurrences.jsonl", occurrences)
    jsonl_output("edges.jsonl", edges)
    jsonl_output("missing_candidates.jsonl", candidates)
    jsonl_output("unresolved_occurrences.jsonl", unresolved)
    atomic_json(graph / "reverse_index.json", {k: sorted(v) for k, v in sorted(reverse.items())})
    counts = Counter(x["scan_status"] for x in state_rows.values())
    incomplete = counts["unscanned"] + counts["scan_incomplete"]
    raw_unresolved = sum(row["state"] == "unassigned" for row in unresolved)
    raw_ambiguous = sum(row["state"] == "ambiguous" for row in unresolved)
    fingerprint = unresolved_fingerprint(inv, unresolved, candidates)
    gate = read(graph / "CONSOLIDATION.json", {})
    gated = (incomplete == 0 and raw_unresolved == 0 and raw_ambiguous == 0
             and gate.get("inventory_sha256") == inv["source_inventory_sha256"]
             and gate.get("unresolved_fingerprint") == fingerprint
             and isinstance(gate.get("reviewed_by"), str)
             and bool(gate["reviewed_by"].strip())
             and len(gate.get("rationale", "").strip()) >= 40)
    phase = ("scan_and_link_existing" if incomplete else
             "consolidate_occurrences" if not gated else
             "research_missing_dependencies")
    summary = {
        "schema_version": SCHEMA, "inventory_sha256": inv["source_inventory_sha256"],
        "total_meanings": len(meanings), "total_formulations": len(state_rows),
        "screened_formulations": sum(e["origin"] == "screened" for e in inv["formulations"].values()),
        "provisional_formulations": sum(e["origin"] == "provisional" for e in inv["formulations"].values()),
        "scan_complete": counts["complete"], "scan_incomplete": counts["scan_incomplete"],
        "unscanned": counts["unscanned"], "open": len(blocked),
        "closed": len(state_rows) - len(blocked), "missing_candidates": len(candidates),
        "unresolved_missing_candidates": sum(x["status"] == "unresearched" for x in candidates),
        "alias_candidate_records": len(aliases),
        "missing_occurrences": sum(r["state"] == "missing" for r in occurrences),
        "ambiguous_occurrences": sum(r["state"] == "ambiguous" for r in occurrences),
        "unassigned_occurrences": raw_unresolved,
        "unresolved_fingerprint": fingerprint,
        "phase": phase,
        "consolidation_gate_valid": gated,
        "seed_relations": len(inv["seed_relations"]),
        "scan_occurrences": sum(not r.get("origin", "").startswith("preexisting_relation")
                                for r in occurrences),
        "scan_amendment_event_count": len(amendment_events(graph)),
        "automatic_completion_is_not_certification": True,
        "breadth_expansion": "on_hold",
    }
    atomic_json(graph / "STATE.json", {"summary": summary, "formulations": state_rows})
    atomic_json(graph / "CHECKPOINT.json", {
        "schema_version": SCHEMA,
        "inventory_sha256": inv["source_inventory_sha256"],
        "state_sha256": digest(state_rows),
        "valid_node_snapshot_count": len(nodes),
        "scan_amendment_event_count": len(amendment_events(graph)),
        "next_work": ("Complete content-only semantic scans and existing-meaning links without external research"
                      if phase == "scan_and_link_existing" else
                      "Consolidate all stored unresolved occurrences before missing-definition research"
                      if phase == "consolidate_occurrences" else
                      "Research the consolidated missing-meaning candidates, then integrate new formulations"),
        "transaction": "Derived indexes written from authoritative atomic per-node snapshots; commit this directory in one Git transaction.",
    })
    return summary


def make_snapshot(inv, fid, references, status, rationale=""):
    if fid not in inv["formulations"]:
        raise PipelineError("Unknown formulation " + fid)
    if status not in ("complete", "scan_incomplete"):
        raise PipelineError("Unknown scan status")
    if status == "complete" and len(rationale.strip()) < 40:
        raise PipelineError("Completing a content scan requires explicit substantive review rationale")
    seen = set()
    output = []
    for index, item in enumerate(references):
        ref = dict(item)
        if not str(ref.get("phrase", "")).strip():
            raise PipelineError("Every reference needs a phrase")
        if ref.get("state") not in ("existing", "missing", "ambiguous", "external", "deferred", "unassigned"):
            raise PipelineError("Reference needs a supported state")
        if ref.get("state") == "existing" and ref.get("target_meaning_id") not in inv["meanings"]:
            raise PipelineError("Unknown existing meaning")
        if ref.get("state") == "missing":
            # Default to owning mathematical context; a missing object without
            # context must not be globally deduplicated across homonyms.
            ref.setdefault("context", inv["formulations"][fid]["context"])
            ref["missing_candidate_id"] = missing_key(ref["phrase"], ref["context"])
        if ref.get("state") == "unassigned":
            ref.setdefault("context", inv["formulations"][fid]["context"])
            if not str(ref.get("context", "")).strip():
                raise PipelineError("Unassigned reference requires mathematical context")
        if ref.get("state") == "ambiguous":
            ids = ref.get("candidate_meaning_ids", [])
            if not isinstance(ids, list) or any(mid not in inv["meanings"] for mid in ids):
                raise PipelineError("Ambiguity contains an unknown contextual target")
        if ref.get("state") in ("ambiguous", "deferred") and not ref.get("reason"):
            raise PipelineError("Ambiguity requires reason")
        if ref.get("state") == "external" and not ref.get("disposition"):
            raise PipelineError("External needs disposition")
        # Span is optional for seeded/editorially identified references.
        if "span" in ref:
            span = ref["span"]
            text = inv["formulations"][fid]["text"]
            if not isinstance(span, list) or len(span) != 2 or text[span[0]:span[1]].casefold() != ref["phrase"].casefold():
                raise PipelineError("Reference span must match original text")
        ref["occurrence_id"] = stable_id("occ", {"fid": fid,
            "version": inv["formulations"][fid]["version_sha256"],
            "index": index, "reference": {k: v for k, v in ref.items() if k != "occurrence_id"}})
        if ref["occurrence_id"] in seen:
            raise PipelineError("Duplicate occurrence")
        seen.add(ref["occurrence_id"])
        output.append(ref)
    return {
        "schema_version": SCHEMA, "formulation_id": fid,
        "version_sha256": inv["formulations"][fid]["version_sha256"],
        "scan_status": status, "references": output,
        "snapshot_sha256": digest(output), "review_rationale": rationale,
    }


def store(workspace, items):
    graph = graph_path(workspace)
    inv = read(graph / "INVENTORY.json")
    if not inv:
        raise PipelineError("Generate inventory first")
    staged = {}
    current = live_nodes(graph, inv)
    amended_ids = {e["formulation_id"] for e in amendment_events(graph)
                   if e.get("version_sha256") ==
                       inv["formulations"].get(e.get("formulation_id"), {}).get("version_sha256")}
    for entry in items:
        fid = entry["formulation_id"]
        if entry.get("version_sha256") != inv["formulations"].get(fid, {}).get("version_sha256"):
            raise PipelineError("Stale incoming scan for " + fid)
        status = "complete" if entry.get("complete") is True else "scan_incomplete"
        node = make_snapshot(inv, fid, entry.get("references", []),
                             status, entry.get("review_rationale", ""))
        if entry.get("proposal_fingerprint") and status == "scan_incomplete":
            node["proposal_fingerprint"] = entry["proposal_fingerprint"]
            node["scan_origin"] = "unreviewed_adapter_proposal"
        existing = current.get(fid)
        if fid in amended_ids and existing != node:
            raise PipelineError("Correct amended snapshots by append-only amendment, not store")
        if existing and existing.get("version_sha256") == node["version_sha256"]:
            if existing.get("scan_status") == "complete" and existing != node:
                raise PipelineError("Cannot overwrite completed scan without a versioned correction")
        if fid in staged:
            raise PipelineError("Duplicate scan unit in batch")
        staged[fid] = node
    for fid, node in staged.items():
        # The exact full adjacency + complete marker are one atomic node file.
        if fid not in amended_ids and read_node(node_file(graph, fid)) != node:
            atomic_json(node_file(graph, fid), node)
    return rebuild(workspace, inv)


def amend(workspace, items):
    """Atomically append reviewed same-version scan corrections.

    An amended original node is never overwritten. A crash after the
    event-ledger write but before derived-index refresh safely replays.
    """
    graph = graph_path(workspace)
    inv = read(graph / "INVENTORY.json")
    if not inv:
        raise PipelineError("Inventory required before scan amendments")
    current = live_nodes(graph, inv)
    history = amendment_events(graph)
    seen = {e["amendment_id"]: e for e in history}
    if len(seen) != len(history):
        raise PipelineError("Duplicate historical amendment")
    new_events = []
    batch_seen = set()
    for item in items:
        eid, fid = item.get("amendment_id"), item.get("formulation_id")
        if not isinstance(eid, str) or not KEY_RE.fullmatch(eid):
            raise PipelineError("Unsafe or missing amendment ID")
        if eid in batch_seen:
            raise PipelineError("Duplicate amendment in current batch")
        batch_seen.add(eid)
        if fid not in inv["formulations"]:
            raise PipelineError("Amendment references unknown formulation")
        version = inv["formulations"][fid]["version_sha256"]
        if item.get("version_sha256") != version:
            raise PipelineError("Stale formulation-version amendment")
        reason = item.get("reason", "")
        reviewer = item.get("reviewed_by", "")
        if len(reason.strip()) < 40 or not str(reviewer).strip():
            raise PipelineError("Amendment needs a substantive reason and reviewer")
        node = make_snapshot(inv, fid, item.get("references", []),
                             "complete" if item.get("complete") is True else "scan_incomplete",
                             item.get("review_rationale", ""))
        event = {
            "amendment_id": eid, "formulation_id": fid,
            "version_sha256": version,
            "expected_node_sha256": item.get("expected_node_sha256"),
            "replacement": node, "reason": reason, "reviewed_by": reviewer,
        }
        if eid in seen:
            if seen[eid] != event:
                raise PipelineError("Amendment ID reused with different contents")
            continue  # Exact replay must not append or duplicate the event.
        prior = current.get(fid)
        if prior is None or digest(prior) != item.get("expected_node_sha256"):
            raise PipelineError("Stale or missing base snapshot for amendment " + eid)
        current[fid] = node
        seen[eid] = event
        new_events.append(event)
    if new_events:
        history.extend(new_events)
        write_atomic(graph / "amendments.jsonl",
                     "".join(json.dumps(e, sort_keys=True, ensure_ascii=False) + "\n"
                             for e in history))
    return rebuild(workspace, inv)


def propose(workspace, adapter, limit=30):
    graph = graph_path(workspace)
    inv = read(graph / "INVENTORY.json")
    if not inv:
        raise PipelineError("Generate inventory first")
    nodes = live_nodes(graph, inv)
    module = importlib.import_module(adapter)
    # The source digest is an explicit adapter-version invalidation key.
    # Refresh only safe, never-reviewed lexical proposals, never completed
    # semantic reviews or manually curated incomplete work.
    source_bytes = Path(module.__file__).read_bytes()
    fingerprint = hashlib.sha256(source_bytes).hexdigest()
    def refreshable(node):
        return (node.get("scan_status") == "scan_incomplete"
                and not node.get("review_rationale")
                and node.get("proposal_fingerprint") != fingerprint
                and (node.get("scan_origin") == "unreviewed_adapter_proposal"
                     or (not node.get("scan_origin") and
                         all(r.get("origin") == "unreviewed_lexical_proposal"
                             for r in node.get("references", [])))))
    # Work fresh forms first; afterward update outdated provisional proposals.
    queue = ([fid for fid in sorted(inv["formulations"]) if fid not in nodes] +
             [fid for fid in sorted(nodes) if refreshable(nodes[fid])])
    entries = []
    for fid in queue[:limit]:
        references = module.propose(inv["formulations"][fid], inv["meanings"])
        entries.append({"formulation_id": fid,
                        "version_sha256": inv["formulations"][fid]["version_sha256"],
                        "references": references, "complete": False,
                        "proposal_fingerprint": fingerprint})
    if entries:
        result = store(workspace, entries)
    else:
        result = rebuild(workspace, inv)
    result["proposed_this_run"] = len(entries)
    return result


def tree(workspace, root, max_depth=30):
    """Render the effective stored graph, including resolved missing candidates."""
    graph = graph_path(workspace)
    inv = read(graph / "INVENTORY.json")
    if root not in inv["formulations"]:
        raise PipelineError("Unknown root formulation")
    state = read(graph / "STATE.json", {})
    if state.get("summary", {}).get("inventory_sha256") != inv["source_inventory_sha256"]:
        raise PipelineError("Rebuild stale graph indexes before tree rendering")
    nodes = live_nodes(graph, inv)
    occurrences = defaultdict(list)
    for line in (graph / "occurrences.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            ref = json.loads(line)
            occurrences[ref["from_formulation"]].append(ref)
    def visit(fid, path, depth):
        node = nodes.get(fid)
        out = {"formulation_id": fid, "status": node["scan_status"] if node else "unscanned",
               "children": []}
        if fid in path:
            out["cycle"] = True
            return out
        if depth >= max_depth:
            out["depth_limit"] = True
            return out
        for ref in occurrences[fid]:
            if ref["state"] == "existing":
                mid = ref["target_meaning_id"]
                out["children"].append({
                    "target_meaning_id": mid, "occurrence_id": ref["occurrence_id"],
                    "phrase": ref["phrase"],
                    "provenance": ref.get("origin", "scan"),
                    "formulations": [visit(child, path | {fid}, depth + 1)
                        for child in inv["meanings"][mid]["formulation_ids"]]})
            else:
                out["children"].append({
                    "state": ref["state"], "phrase": ref["phrase"],
                    "missing_candidate_id": ref.get("missing_candidate_id"),
                    "terminal": True})
        return out
    return visit(root, set(), 0)


def alias_candidates(workspace, proposed):
    """Append source-reviewed identity aliases; never rewrite original candidates."""
    graph = graph_path(workspace)
    path = graph / "candidate_aliases.jsonl"
    current = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
               if line.strip()] if path.exists() else []
    current_ids = {x.get("alias_id"): x for x in current}
    if len(current_ids) != len(current):
        raise PipelineError("Duplicate alias ID in history")
    candidate_records = [json.loads(line) for line in
        (graph / "missing_candidates.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()]
    known = {c["id"] for c in candidate_records}
    pending = list(current)
    for event in proposed:
        eid = event.get("alias_id")
        if not eid or not KEY_RE.fullmatch(eid):
            raise PipelineError("Invalid alias event ID")
        if eid in current_ids:
            if current_ids[eid] != event:
                raise PipelineError("Alias ID reused with changed content")
            continue
        if (event.get("alias_candidate_id") not in known or
                event.get("canonical_candidate_id") not in known):
            raise PipelineError("Alias must connect existing graph candidates")
        if event.get("alias_candidate_id") == event.get("canonical_candidate_id"):
            raise PipelineError("Candidate may not alias itself")
        pending.append(event)
        current_ids[eid] = event
    # Verify all events and forbid cycles/chains BEFORE writing the ledger.
    alias_map(graph, known, pending)
    if pending != current:
        write_atomic(path, "".join(json.dumps(x, sort_keys=True, ensure_ascii=False) + "\n"
                                   for x in pending))
    return rebuild(workspace)


def research_queue(workspace, limit=20):
    graph = graph_path(workspace)
    candidates = [json.loads(x) for x in
        (graph / "missing_candidates.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    state = read(graph / "STATE.json")["summary"]
    phase = state["phase"]
    candidates = [x for x in candidates if x["status"] == "unresearched"]
    candidates.sort(key=lambda x: (-x["upstream_formulation_count"],
                         -x["occurrence_count"], x["id"]))
    permitted = phase == "research_missing_dependencies"
    return {"phase": phase, "breadth_batch_143": "on_hold",
        "missing_research_permitted": permitted,
        "unassigned_occurrences": state["unassigned_occurrences"],
        "ambiguous_occurrences": state["ambiguous_occurrences"],
        "requires_source_research_and_explicit_review": permitted,
        "candidates": candidates[:limit] if permitted else [],
        "candidate_preview_only": candidates[:limit] if not permitted else [],
        "remaining": max(0, len(candidates) - limit)}


def resolve(workspace, resolutions):
    """Append-only version-bound candidate-to-meaning decisions, not certification."""
    graph = graph_path(workspace)
    inv = read(graph / "INVENTORY.json")
    if not inv:
        raise PipelineError("Inventory required before resolving candidates")
    candidate_ids = {json.loads(x)["id"] for x in
        (graph / "missing_candidates.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()}
    path = graph / "resolutions.jsonl"
    existing = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()
                if x.strip()] if path.exists() else []
    prior = {x["missing_candidate_id"]: x for x in existing}
    for row in resolutions:
        cid, mid = row.get("missing_candidate_id"), row.get("target_meaning_id")
        if cid not in candidate_ids or mid not in inv["meanings"]:
            raise PipelineError("Resolution candidate/meaning not in inventory")
        if row.get("target_version_sha256") != meaning_version(inv, mid):
            raise PipelineError("Stale target meaning version")
        if len(row.get("review_rationale", "").strip()) < 40:
            raise PipelineError("Resolution requires substantive contextual review")
        if cid in prior:
            if prior[cid] != row:
                raise PipelineError("Cannot overwrite append-only resolution")
            continue
        prior[cid] = row
        existing.append(row)
    write_atomic(path, "".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n"
                                for r in existing))
    return rebuild(workspace, inv)


def apply_seed_overrides(workspace, proposed):
    from .dependency_seed_overrides import append_seed_overrides
    return append_seed_overrides(workspace, proposed)


def apply_inbox(workspace, limit=20):
    """Replay-safe, grouped append-only ingestion with one rebuild per mode run.

    Consecutive amend, alias or resolve packets are validated as a single
    same-mode group and retain individual immutable receipts. The graph is
    rebuilt only once for that group. On a validation error, no ledger event
    or receipt for the group is committed. Crossing mode boundaries preserves
    the exact established lexical inbox order and rebuilds between modes.
    The Git transaction commits graph indexes and receipts together.
    """
    graph = graph_path(workspace)
    inbox = graph / "inbox"
    applied = graph / "applied"
    applied.mkdir(parents=True, exist_ok=True)
    valid_modes = {
        "ingest": lambda pkg: store(workspace, pkg["items"]),
        "amend": lambda pkg: amend(workspace, pkg["amendments"]),
        "resolve": lambda pkg: resolve(workspace, pkg["resolutions"]),
        "alias": lambda pkg: alias_candidates(workspace, pkg["aliases"]),
        "seed_override": lambda pkg: apply_seed_overrides(workspace, pkg["seed_overrides"]),
        "consolidate": lambda pkg: seal_consolidation(workspace, pkg["gate"]),
    }
    grouped_fields = {"amend": "amendments", "alias": "aliases",
                      "resolve": "resolutions", "seed_override": "seed_overrides"}
    result = {"applied": [], "already_applied": [], "max_packages": limit,
              "batched_rebuilds": []}
    remaining = max(0, limit)
    pending = []
    pending_mode = None

    def receipt(file, pkg, receipt_sha):
        atomic_json(applied / file.name, {
            "id": file.stem, "sha256": receipt_sha,
            "mode": pkg["mode"], "status": "applied_in_independent_graph_only",
            "human_certified": False,
        })
        result["applied"].append(file.stem)

    def flush_pending():
        nonlocal pending_mode
        if not pending:
            return
        mode = pending_mode
        combined = [item for _, pkg, _ in pending
                    for item in pkg[grouped_fields[mode]]]
        # Each append-only API validates all new events before writing its
        # ledger. Never issue a receipt if group-level validation fails.
        valid_modes[mode]({grouped_fields[mode]: combined})
        result["batched_rebuilds"].append({
            "mode": mode, "packet_count": len(pending),
            "event_count": len(combined),
        })
        for file, pkg, receipt_sha in pending:
            receipt(file, pkg, receipt_sha)
        pending.clear()
        pending_mode = None

    for file in sorted(inbox.glob("*.json")) if inbox.is_dir() else ():
        pkg = read(file)
        if (pkg.get("schema_version") != SCHEMA or
                pkg.get("id") != file.stem or
                pkg.get("mode") not in valid_modes or
                not KEY_RE.fullmatch(file.stem)):
            raise PipelineError("Invalid or unsupported dependency graph batch: " + str(file))
        receipt_sha = digest(pkg)
        prior = read(applied / file.name)
        if prior:
            if prior.get("sha256") != receipt_sha or prior.get("mode") != pkg["mode"]:
                raise PipelineError("Mutated already-applied graph batch " + file.name)
            result["already_applied"].append(file.stem)
            continue
        if remaining == 0:
            continue  # Old receipts never starve later unprocessed inbox items.
        mode = pkg["mode"]
        if mode in grouped_fields:
            if pending and mode != pending_mode:
                flush_pending()
            pending_mode = mode
            pending.append((file, pkg, receipt_sha))
        else:
            flush_pending()
            valid_modes[mode](pkg)
            receipt(file, pkg, receipt_sha)
        remaining -= 1
    flush_pending()
    return result

def scan_worklist(workspace, limit=10):
    """Deterministic, no-network first-pass input for a future Chat reviewer."""
    graph = graph_path(workspace)
    inv = read(graph / "INVENTORY.json")
    if not inv:
        raise PipelineError("Build the independent graph inventory first")
    nodes = live_nodes(graph, inv)
    seed_by_form = defaultdict(list)
    for seed in inv["seed_relations"]:
        seed_by_form[seed["from_formulation"]].append(seed)
    todo = [fid for fid in sorted(inv["formulations"])
            if nodes.get(fid, {}).get("scan_status") != "complete"]
    items = []
    for fid in todo[:max(0, limit)]:
        item = inv["formulations"][fid]
        node = nodes.get(fid, {})
        items.append({"formulation_id": fid, "version_sha256": item["version_sha256"],
                      "meaning_id": item["meaning_id"], "display_term": item["display_term"],
                      "context": item["context"], "text": item["text"],
                      "scan_status": node.get("scan_status", "unscanned"),
                      "local_lexical_proposals": node.get("references", []),
                      "historical_link_seeds": seed_by_form.get(fid, []),
                      "instruction": "Read entire formulation; link clear existing contextual meanings; "
                          "record other possible mathematical references as unassigned occurrences "
                          "with precise local context. No external source investigation or new definitions."})
    return {"phase": "scan_and_link_existing", "external_research": False,
            "total_remaining": len(todo), "items": items}


def consolidation_worklist(workspace, limit=20):
    """Read-only grouping of unresolved occurrences, NOT meaning equivalence."""
    graph = graph_path(workspace)
    inv = read(graph / "INVENTORY.json")
    if not inv:
        raise PipelineError("Build inventory before grouping unresolved occurrences")
    state = read(graph / "STATE.json", {}).get("summary", {})
    groups = defaultdict(list)
    rows = []
    source = graph / "unresolved_occurrences.jsonl"
    if source.is_file():
        rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()
                if line.strip()]
    for occurrence in rows:
        groups[norm(occurrence["phrase"])].append(occurrence)
    ordered = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    batch = []
    for phrase, occurrences in ordered[:max(0, limit)]:
        occurrences = sorted(occurrences, key=lambda r:
                             (r["from_formulation"], r["occurrence_id"]))
        batch.append({
            "surface_key": phrase, "occurrence_count": len(occurrences),
            "distinct_formulation_count": len(set(o["from_formulation"] for o in occurrences)),
            "contexts": sorted(set(o.get("context", inv["formulations"][o["from_formulation"]]["context"])
                                   for o in occurrences)),
            "observations": [{"formulation_id": o["from_formulation"],
                              "occurrence_id": o["occurrence_id"],
                              "phrase": o["phrase"], "state": o["state"],
                              "context": o.get("context", ""),
                              "candidate_meaning_ids": o.get("candidate_meaning_ids", []),
                              "missing_candidate_id": o.get("missing_candidate_id"),
                              "reason": o.get("reason", "")}
                             for o in occurrences],
            "warning": "Surface grouping only; homonyms MUST be split by mathematical context."
        })
    return {"phase": state.get("phase"), "initial_scan_complete":
                state.get("scan_complete") == state.get("total_formulations"),
            "external_definition_research_permitted": state.get("consolidation_gate_valid", False),
            "total_unresolved_occurrences": len(rows), "distinct_surface_keys": len(groups),
            "groups": batch}


def seal_consolidation(workspace, event):
    """Explicit reviewed phase barrier; stale/new occurrences invalidate it."""
    graph = graph_path(workspace)
    summary = rebuild(workspace)
    inv = read(graph / "INVENTORY.json")
    if summary["scan_complete"] != summary["total_formulations"]:
        raise PipelineError("Cannot consolidate before full first-pass semantic scans")
    if summary["unassigned_occurrences"] or summary["ambiguous_occurrences"]:
        raise PipelineError("Classify every unassigned/ambiguous occurrence or explicitly defer it")
    if event.get("inventory_sha256") != inv["source_inventory_sha256"] or (
            event.get("unresolved_fingerprint") != summary["unresolved_fingerprint"]):
        raise PipelineError("Stale consolidation scope / occurrence registry")
    if not str(event.get("reviewed_by", "")).strip() or len(str(event.get("rationale", "")).strip()) < 40:
        raise PipelineError("Global missing-occurrence consolidation needs a substantive reviewed rationale")
    if event.get("schema_version") != SCHEMA:
        raise PipelineError("Unsupported consolidation gate")
    previous = read(graph / "CONSOLIDATION.json")
    if previous and previous != event and previous.get("unresolved_fingerprint") == event["unresolved_fingerprint"]:
        raise PipelineError("Do not rewrite an existing reviewed consolidation gate")
    atomic_json(graph / "CONSOLIDATION.json", event)
    return rebuild(workspace)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--mode", choices=("inventory", "propose", "ingest", "amend", "resolve", "alias", "seed_override", "consolidate", "apply_inbox", "worklist", "consolidation_worklist", "status", "tree", "queue"),
                   required=True)
    p.add_argument("--adapter", default="research_pipeline.adapters.mathdef.dependency_scan")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--root-formulation")
    p.add_argument("--batch", type=Path)
    args = p.parse_args()
    graph = graph_path(args.workspace)
    if args.mode == "inventory":
        result = inventory_sync(args.workspace)
    elif args.mode == "propose":
        result = propose(args.workspace, args.adapter, max(0, args.limit))
    elif args.mode == "ingest":
        inbox = (graph / "inbox").resolve()
        if not args.batch or not args.batch.resolve().is_relative_to(inbox):
            raise PipelineError("Scan batches must be committed within dependency_graph/inbox")
        batch = read(args.batch)
        if batch.get("schema_version") != 1:
            raise PipelineError("Unsupported scan batch")
        result = store(args.workspace, batch["items"])
    elif args.mode == "amend":
        inbox = (graph / "inbox").resolve()
        if not args.batch or not args.batch.resolve().is_relative_to(inbox):
            raise PipelineError("Amendments must be committed within dependency_graph/inbox")
        batch = read(args.batch)
        if batch.get("schema_version") != 1:
            raise PipelineError("Unsupported graph amendment batch")
        result = amend(args.workspace, batch["amendments"])
    elif args.mode == "resolve":
        inbox = (graph / "inbox").resolve()
        if not args.batch or not args.batch.resolve().is_relative_to(inbox):
            raise PipelineError("Resolution batches must be committed within dependency_graph/inbox")
        batch = read(args.batch)
        if batch.get("schema_version") != 1:
            raise PipelineError("Unsupported resolution batch")
        result = resolve(args.workspace, batch["resolutions"])
    elif args.mode == "alias":
        inbox = (graph / "inbox").resolve()
        if not args.batch or not args.batch.resolve().is_relative_to(inbox):
            raise PipelineError("Alias packages must be committed within dependency_graph/inbox")
        batch = read(args.batch)
        if batch.get("schema_version") != SCHEMA:
            raise PipelineError("Unsupported alias batch")
        result = alias_candidates(args.workspace, batch["aliases"])
    elif args.mode == "seed_override":
        inbox = (graph / "inbox").resolve()
        if not args.batch or not args.batch.resolve().is_relative_to(inbox):
            raise PipelineError("Seed override packet must be in graph inbox")
        batch = read(args.batch)
        if batch.get("schema_version") != SCHEMA or batch.get("mode") != "seed_override":
            raise PipelineError("Unsupported historical seed override packet")
        result = apply_seed_overrides(args.workspace, batch["seed_overrides"])
    elif args.mode == "consolidate":
        inbox = (graph / "inbox").resolve()
        if not args.batch or not args.batch.resolve().is_relative_to(inbox):
            raise PipelineError("Consolidation batch must be committed under graph inbox")
        batch = read(args.batch)
        result = seal_consolidation(args.workspace, batch["gate"])
    elif args.mode == "worklist":
        result = scan_worklist(args.workspace, max(0, args.limit))
    elif args.mode == "consolidation_worklist":
        result = consolidation_worklist(args.workspace, max(0, args.limit))
    elif args.mode == "apply_inbox":
        result = apply_inbox(args.workspace, max(0, args.limit))
    elif args.mode == "tree":
        result = tree(args.workspace, args.root_formulation)
    elif args.mode == "queue":
        result = research_queue(args.workspace, max(0, args.limit))
    else:
        result = read(graph / "STATE.json", {}).get("summary", {})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
