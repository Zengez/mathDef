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
    if state not in ("existing", "missing", "ambiguous", "external", "deferred"):
        raise PipelineError("Unknown reference state")
    if state == "existing" and ref.get("target_meaning_id") not in meanings:
        raise PipelineError("Existing dependency must target an inventory meaning")
    if state == "missing" and ref.get("missing_candidate_id") not in missing:
        raise PipelineError("Missing reference must target a registered candidate")
    if state in ("ambiguous", "deferred") and not ref.get("reason"):
        raise PipelineError("Ambiguous/deferred references need an explicit reason")
    if state == "external" and not ref.get("disposition"):
        raise PipelineError("External/primitve reference requires a justified disposition")


def missing_key(phrase, context):
    return stable_id("missing", {"phrase": norm(phrase), "context": norm(context)})


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
    for seed in inv["seed_relations"]:
        fid = seed["from_formulation"]
        if seed.get("target_query") and not seed.get("target_meaning_id"):
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
        if resolution.get("target_version_sha256") != digest(meanings[mid]):
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
            if ref["state"] == "missing" and ref["missing_candidate_id"] in resolutions:
                key = ref["missing_candidate_id"]
                reverse["missing:" + key].add(fid)  # Retain traceability.
                effective = {**ref, "state": "existing",
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
            elif state in ("ambiguous", "deferred"):
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
    state_rows = {}
    for fid in inv["formulations"]:
        scan = nodes.get(fid, {}).get("scan_status", "unscanned")
        state_rows[fid] = {
            "scan_status": scan, "encountered": scan != "unscanned",
            "completed": scan == "complete",
            "structural_status": "open" if fid in blocked else "closed",
            "direct_blockers": blockers.get(fid, []) +
                (["scan_incomplete"] if scan != "complete" else []),
            "version_sha256": inv["formulations"][fid]["version_sha256"],
        }
    occurrences.sort(key=lambda x: (x["from_formulation"], x["occurrence_id"]))
    edges.sort(key=lambda x: (x["from_formulation"], x["occurrence_id"]))
    candidates = []
    for k, c in sorted(candidate_map.items()):
        incoming = sorted(reverse.get("missing:" + k, ()))
        candidates.append({**c, "status": "resolved" if k in resolutions else "unresearched",
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
    atomic_json(graph / "reverse_index.json", {k: sorted(v) for k, v in sorted(reverse.items())})
    counts = Counter(x["scan_status"] for x in state_rows.values())
    summary = {
        "schema_version": SCHEMA, "inventory_sha256": inv["source_inventory_sha256"],
        "total_meanings": len(meanings), "total_formulations": len(state_rows),
        "screened_formulations": sum(e["origin"] == "screened" for e in inv["formulations"].values()),
        "provisional_formulations": sum(e["origin"] == "provisional" for e in inv["formulations"].values()),
        "scan_complete": counts["complete"], "scan_incomplete": counts["scan_incomplete"],
        "unscanned": counts["unscanned"], "open": len(blocked),
        "closed": len(state_rows) - len(blocked), "missing_candidates": len(candidates),
        "unresolved_missing_candidates": sum(x["status"] != "resolved" for x in candidates),
        "missing_occurrences": sum(r["state"] == "missing" for r in occurrences),
        "ambiguous_occurrences": sum(r["state"] == "ambiguous" for r in occurrences),
        "seed_relations": len(inv["seed_relations"]),
        "scan_occurrences": sum(r.get("origin") != "preexisting_relation" for r in occurrences),
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
        "next_work": "Resume unscanned/incomplete/version-invalid forms; research deduplicated missing candidates only after semantic scan review.",
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
        if ref.get("state") not in ("existing", "missing", "ambiguous", "external", "deferred"):
            raise PipelineError("Reference needs a supported state")
        if ref.get("state") == "existing" and ref.get("target_meaning_id") not in inv["meanings"]:
            raise PipelineError("Unknown existing meaning")
        if ref.get("state") == "missing":
            ref["missing_candidate_id"] = missing_key(ref["phrase"], ref.get("context", ""))
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
    graph = graph_path(workspace)
    inv = read(graph / "INVENTORY.json")
    if root not in inv["formulations"]:
        raise PipelineError("Unknown root formulation")
    nodes = live_nodes(graph, inv)
    seeds = defaultdict(list)
    for rel in inv["seed_relations"]:
        if rel.get("target_meaning_id"):
            seeds[rel["from_formulation"]].append(rel["target_meaning_id"])
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
        targets = [(mid, "preexisting_relation") for mid in seeds.get(fid, [])]
        if node:
            for ref in node["references"]:
                if ref["state"] == "existing":
                    targets.append((ref["target_meaning_id"], "scan"))
                elif ref["state"] == "missing":
                    out["children"].append({"missing_candidate_id": ref["missing_candidate_id"],
                                            "phrase": ref["phrase"], "terminal": True})
                else:
                    out["children"].append({"state": ref["state"],
                                            "phrase": ref["phrase"], "terminal": True})
        for mid, provenance in targets:
            out["children"].append({"target_meaning_id": mid, "provenance": provenance,
                "formulations": [visit(child, path | {fid}, depth + 1)
                   for child in inv["meanings"][mid]["formulation_ids"]]})
        return out
    return visit(root, set(), 0)


def research_queue(workspace, limit=20):
    graph = graph_path(workspace)
    candidates = [json.loads(x) for x in
        (graph / "missing_candidates.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    state = read(graph / "STATE.json")["summary"]
    if state["unscanned"] or state["scan_incomplete"]:
        phase = "scan_and_disambiguate_first"
    else:
        phase = "research_missing_dependencies"
    candidates = [x for x in candidates if x["status"] != "resolved"]
    candidates.sort(key=lambda x: (-x["upstream_formulation_count"],
                         -x["occurrence_count"], x["id"]))
    return {"phase": phase, "breadth_batch_143": "on_hold",
        "requires_source_research_and_explicit_review": True,
        "candidates": candidates[:limit],
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
        if row.get("target_version_sha256") != digest(inv["meanings"][mid]):
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


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--mode", choices=("inventory", "propose", "ingest", "amend", "resolve", "status", "tree", "queue"),
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
    elif args.mode == "tree":
        result = tree(args.workspace, args.root_formulation)
    elif args.mode == "queue":
        result = research_queue(args.workspace, max(0, args.limit))
    else:
        result = read(graph / "STATE.json", {}).get("summary", {})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
