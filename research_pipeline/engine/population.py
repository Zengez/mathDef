"""Reusable, append-only population ledger for isolated research workspaces.

Populate intentionally DOES NOT certify old/new mathematics or publish records.
The active reviewed workspace is never written by this module. Individual
evidence and revisions are hashed; exhaustive review is deferred to audit.
"""
from __future__ import annotations

import argparse
import importlib
import hashlib
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

from .core import PipelineError, Workspace, canonical

KINDS = ("sources", "terms", "observations", "meanings", "relations", "reviews", "issues")
STATUSES = ("pending", "provisional", "screened", "held", "rejected")


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as output:
        output.write(text)
        output.flush()
        os.fsync(output.fileno())
    os.replace(tmp, path)


def parent_records(workspace):
    parent = Workspace(workspace)
    parent.config()
    return {kind: parent.records(kind) for kind in KINDS[:5]}


def snapshot(workspace):
    """Materialize current draft records, replaying versioned draft-only revisions."""
    root = Path(workspace) / "population"
    data = {}
    for kind in KINDS:
        rows = read_jsonl(root / "records" / (kind + ".jsonl"))
        found = {}
        for item in rows:
            key = item.get("id")
            if not isinstance(key, str) or not key or key in found:
                raise PipelineError("Missing/duplicate population ID: " + str(key))
            found[key] = item
        data[kind] = found
    changes = read_jsonl(root / "revisions.jsonl")
    seen = set()
    impacts = []
    for event in changes:
        event_id = event.get("id")
        kind, key = event.get("kind"), event.get("target_id")
        if not event_id or event_id in seen or kind not in KINDS or key not in data[kind]:
            raise PipelineError("Invalid or duplicate revision event")
        seen.add(event_id)
        old = data[kind][key]
        if digest(old) != event.get("expected_sha256"):
            raise PipelineError("Stale revision precondition: " + str(key))
        replacement = event.get("replacement")
        if not isinstance(replacement, dict) or replacement.get("id") != key or not event.get("reason"):
            raise PipelineError("Invalid replacement or revision rationale")
        data[kind][key] = replacement
        impacts.append({"kind": kind, "id": key, "revision": event_id})
    return data, impacts


def validate_package(package, current, parent):
    if package.get("schema_version") != 1 or not isinstance(package.get("id"), str):
        raise PipelineError("Batch needs schema_version=1 and id")
    batch_id = package["id"]
    if not batch_id or not all(c.isascii() and (c.isalnum() or c in "-_.") for c in batch_id):
        raise PipelineError("Unsafe batch ID")
    if not any(package.get(k) for k in (*KINDS, "revisions")):
        raise PipelineError("Empty research batch")
    draft = {k: dict(current[k]) for k in KINDS}
    for kind in KINDS:
        rows = package.get(kind, [])
        seen_in_batch = set()
        if not isinstance(rows, list):
            raise PipelineError(kind + " must be an array")
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
                raise PipelineError("Missing " + kind + " stable ID")
            key = row["id"]
            if key in seen_in_batch:
                raise PipelineError("Repeated ID within the same batch: " + key)
            seen_in_batch.add(key)
            if kind in parent and key in parent[kind]:
                raise PipelineError("Previously screened record cannot be overwritten: " + key)
            if key in draft[kind] and canonical(draft[kind][key]) != canonical(row):
                raise PipelineError("Conflicting already ingested provisional record: " + key)
            if not all(c.isascii() and (c.isalnum() or c in "-_.") for c in key):
                raise PipelineError("Unsafe record ID: " + key)
            draft[kind][key] = dict(row)

    def require(condition, message):
        if not condition:
            raise PipelineError(message)

    sources = {**parent["sources"], **draft["sources"]}
    terms = {**parent["terms"], **draft["terms"]}
    observations = {**parent["observations"], **draft["observations"]}
    meanings = {**parent["meanings"], **draft["meanings"]}
    forms = {}
    for m in meanings.values():
        for f in m.get("formulations", []):
            if f.get("id") in forms:
                raise PipelineError("Repeated formulation ID " + str(f.get("id")))
            forms[f["id"]] = (m, f)
    for s in package.get("sources", []):
        require(s.get("url", "").startswith("https://") and s.get("authority_reviewed") is True
                and s.get("access") in ("free", "paid", "unknown")
                and s.get("rights") in ("permitted", "locator_only", "unknown", "disallowed"),
                "Unreviewed source provenance or rights")
    for t in package.get("terms", []):
        require(t.get("source_id") in sources and bool(t.get("label"))
                and bool(t.get("locator")), "Term lacks source/locator")
    for o in package.get("observations", []):
        s = sources.get(o.get("source_id"))
        require(s is not None and o.get("term_id") in terms
                and o.get("record_kind") in ("locator", "paraphrase", "licensed_excerpt")
                and bool(o.get("locator")), "Observation lacks source/term provenance")
        if o.get("record_kind") != "locator":
            require(bool(o.get("text")) and s.get("access") == "free"
                    and s.get("rights") in ("permitted", "locator_only"),
                    "Unpermitted or missing observed text")
        if o.get("record_kind") == "licensed_excerpt":
            require(s.get("rights") == "permitted", "Excerpt rights unapproved")
    for m in package.get("meanings", []):
        require(bool(m.get("display_term")) and bool(m.get("context"))
                and bool(m.get("term_ids")) and bool(m.get("formulations")),
                "Meaning missing context or formulations")
        require(all(t in terms for t in m["term_ids"]), "Meaning lacks term provenance")
        for f in m["formulations"]:
            require(bool(f.get("id")) and bool(f.get("text")) and bool(f.get("evidence_ids")),
                    "Formulation needs evidence and text")
            require(f.get("review_state", "candidate") == "candidate",
                    "Population cannot confer screened mathematical status")
            require(all(e in observations and observations[e]["term_id"] in m["term_ids"]
                        for e in f["evidence_ids"]), "Formulation evidence mismatch")
    for r in package.get("relations", []):
        require(r.get("from_formulation") in forms and r.get("relation_type") in
                ("definition_uses", "equivalent", "implies", "related"),
                "Relation lacks source formulation or relation type")
        require(r.get("review_state", "candidate") == "candidate",
                "Populate cannot certify dependency links")
        require(r.get("target_meaning") in meanings or bool(r.get("target_query")),
                "Unresolved target requires explicit target_query")
        require(bool(r.get("editorial_reason")), "Relation needs rationale")
    for review in package.get("reviews", []):
        fid = review.get("formulation_id")
        require(fid in forms, "Review references unknown formulation")
        require(review.get("status") in STATUSES, "Unknown review status")
        require(review.get("status") != "screened" or
                (len(review.get("reason", "")) >= 30 and bool(review.get("reviewed_by"))),
                "Screened review needs substantive reasoning and attribution")
        require(review.get("formulation_sha256") ==
                digest({"formulation": forms[fid][1], "context": forms[fid][0]["context"]}),
                "Stale or missing local formulation/context hash")
    for issue in package.get("issues", []):
        require(bool(issue.get("reason")) and issue.get("status", "open") == "open",
                "Issues require reason and open state")
    for event in package.get("revisions", []):
        kind, key = event.get("kind"), event.get("target_id")
        require(kind in KINDS and key in current[kind] and key not in parent.get(kind, {}),
                "Revisions may update only prior provisional records")
        require(event.get("expected_sha256") == digest(current[kind][key])
                and event.get("replacement", {}).get("id") == key
                and bool(event.get("reason")), "Revision must be version-anchored and justified")
    # Every new form gets an explicit local review state, even if only pending.
    reviewed = {r["formulation_id"] for r in package.get("reviews", [])}
    for m in package.get("meanings", []):
        for f in m["formulations"]:
            require(f["id"] in reviewed, "New form requires a version-anchored review: " + f["id"])
    return draft


def apply(workspace, package_path, dry_run=False, policy=None):
    root = Path(workspace).resolve()
    package_path = Path(package_path).resolve()
    # Only committed packages inside this isolated experiment may be run remotely.
    inbox = (root / "population" / "inbox").resolve()
    if not package_path.is_relative_to(inbox) or package_path.suffix != ".json":
        raise PipelineError("Research package must be a JSON file in population/inbox")
    package = read_json(package_path)
    name = package.get("id", "")
    current, _ = snapshot(root)
    parent = parent_records(root)
    record_path = root / "population" / "applied" / (name + ".json")
    incoming = digest(package)
    if record_path.exists():
        previous = read_json(record_path)
        if previous.get("sha256") != incoming:
            raise PipelineError("Previously applied batch changed")
        return {"batch": name, "replayed": True, "status": "unchanged"}
    validate_package(package, current, parent)
    if policy:
        if not policy.startswith('research_pipeline.adapters.'):
            raise PipelineError('External policy modules are not allowed')
        plugin = importlib.import_module(policy)
        plugin.validate_package(package, root)
    if dry_run:
        return {"batch": name, "dry_run": True, "added": {k: len(package.get(k, [])) for k in KINDS}}
    # Write independent draft records; historical screened corpora stay untouched.
    for kind in KINDS:
        rows = [r for r in package.get(kind, []) if r["id"] not in current[kind]]
        if rows:
            path = root / "population" / "records" / (kind + ".jsonl")
            body = path.read_text(encoding="utf-8") if path.exists() else ""
            body += "".join(canonical(r) + "\n" for r in rows)
            write_atomic(path, body)
    revisions = package.get("revisions", [])
    if revisions:
        path = root / "population" / "revisions.jsonl"
        body = path.read_text(encoding="utf-8") if path.exists() else ""
        body += "".join(canonical(r) + "\n" for r in revisions)
        write_atomic(path, body)
    write_atomic(record_path, json.dumps({"id": name, "sha256": incoming,
                "chat_exchange_id": package.get("chat_exchange_id"),
                "research_minutes_reported": package.get("research_minutes_reported"),
                "counts": {k: len(package.get(k, [])) for k in KINDS}}, indent=2) + "\n")
    post = audit(root)
    write_atomic(root / "population" / "STATUS.json", json.dumps({
        "latest_package": name, "draft_counts": post["draft_counts"],
        "reconciliation_backlog": post["finding_summary"],
        "revision_count": post["revision_count"], "review_mode": "provisional_population",
        "main_screened_corpus_untouched": True,
        "next_action": "Continue independent breadth; defer cross-batch mathematical reconciliation."
    }, indent=2, ensure_ascii=False) + "\n")
    return {"batch": name, "replayed": False, "status": "committed",
            "added": {k: len(package.get(k, [])) for k in KINDS}}


def audit(workspace, write=False, certify=False):
    root = Path(workspace).resolve()
    draft, revisions = snapshot(root)
    base = parent_records(root)
    meanings = {**base["meanings"], **draft["meanings"]}
    forms = {f["id"]: (m, f) for m in meanings.values() for f in m["formulations"]}
    review_by_form = defaultdict(list)
    for r in draft["reviews"].values():
        review_by_form[r["formulation_id"]].append(r)
    findings = []
    def flag(kind, key, reason):
        findings.append({"kind": kind, "record_id": key, "reason": reason})
    for m in draft["meanings"].values():
        for f in m["formulations"]:
            history = review_by_form.get(f["id"], [])
            matched = [r for r in history if r.get("formulation_sha256") ==
                digest({"formulation": f, "context": m["context"]})]
            if not matched or all(r.get("status") != "screened" for r in matched):
                flag("pending_review", f["id"], "No current version-anchored completed review")
    for r in draft["relations"].values():
        if r.get("target_meaning") not in meanings:
            flag("unresolved_target", r["id"], r.get("target_query", "missing target"))
        if r.get("review_state", "candidate") != "screened":
            flag("pending_link_review", r["id"], "Candidate link not individually screened")
    for item in draft["issues"].values():
        if item.get("status", "open") == "open":
            flag("open_issue", item["id"], item.get("reason", "Unresolved issue"))
    titles = defaultdict(list)
    for m in meanings.values():
        titles[" ".join(m["display_term"].casefold().split())].append(m)
    for m in draft["meanings"].values():
        others = [x["id"] for x in titles[" ".join(m["display_term"].casefold().split())]
                  if x["id"] != m["id"] and x.get("context") == m.get("context")]
        if others:
            flag("potential_duplicate_context", m["id"], ", ".join(others[:10]))
    # Flag new dependency cycles. All candidate edges remain unpromoted.
    graph = defaultdict(set)
    for r in list(base["relations"].values()) + list(draft["relations"].values()):
        if r.get("relation_type") == "definition_uses" and r.get("target_meaning") in meanings:
            frm = forms.get(r.get("from_formulation"))
            if frm:
                graph[frm[0]["id"]].add(r["target_meaning"])
    visited, active = set(), set()
    def visit(node):
        if node in active:
            flag("cycle", node, "Candidate dependency cycle; resolve before certification")
            return
        if node in visited:
            return
        active.add(node)
        for target in graph.get(node, set()):
            visit(target)
        active.remove(node)
        visited.add(node)
    for node in list(graph):
        visit(node)
    for event in revisions:
        if event["kind"] == "meanings":
            changed = draft["meanings"][event["id"]]
            affected = [r["id"] for r in list(base["relations"].values()) + list(draft["relations"].values())
                        if r.get("target_meaning") == changed["id"] or
                        any(f["id"] == r.get("from_formulation") for f in changed["formulations"])]
            if affected:
                flag("downstream_review", changed["id"], "Affected edges: " + ", ".join(affected[:25]))
    result = {"status": "ready_for_final_review" if not findings else "reconciliation_required",
              "draft_counts": {k: len(v) for k, v in draft.items()},
              "revision_count": len(revisions), "findings": findings,
              "finding_summary": dict(Counter(x["kind"] for x in findings)),
              "note": "Readiness audit only. Never seals or publishes the working corpus."}
    if write:
        write_atomic(root / "population" / "AUDIT_REPORT.json",
                     json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    if certify and findings:
        raise PipelineError("Certification readiness failed: " +
                            json.dumps(result["finding_summary"], sort_keys=True))
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--mode", choices=("populate", "reconcile", "certify", "status"), default="status")
    p.add_argument("--batch", type=Path)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--policy", help="Reviewed project policy module for populate")
    args = p.parse_args()
    if args.mode == "populate":
        if not args.batch:
            p.error("--batch required for populate")
        result = apply(args.workspace, args.batch, dry_run=args.dry_run, policy=args.policy)
    else:
        result = audit(args.workspace, write=args.mode == "reconcile", certify=args.mode == "certify")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
