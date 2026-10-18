"""Explicit second-wave corrections with an append-only, recoverable audit log.

No silent overwrite: each edit specifies its predecessor SHA and a rationale.
An interrupted edit can be safely resumed; the original workspace remains sealed.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from .core import PipelineError, STAGES, Workspace, atomic_json, canonical, digest, jsonl, require_id, required


def _append_fsync(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(canonical(value) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def apply_revision(workspace, proposal):
    """Write-ahead event, atomic record rewrite, resumable idempotently.

    Record retirements remain in the corpus with _retired=True to preserve
    provenance. The publication gate moves such records to the held set.
    """
    w = Workspace(workspace)
    w.config()
    if not (w.root / "state" / "baseline.json").exists():
        raise PipelineError("Editing imported records requires a second-wave fork")
    for key in ("event_id", "stage", "record_id", "before_digest", "editor", "reason"):
        required(proposal, key)
    require_id(proposal["event_id"])
    stage = proposal["stage"]
    if stage not in STAGES:
        raise PipelineError("Invalid stage")
    if w.state(stage).get("sealed"):
        raise PipelineError("Cannot revise a sealed stage")
    if proposal.get("operation") not in ("replace", "retire"):
        raise PipelineError("Operation must be replace or retire")
    records = w.records(stage)
    old = records.get(proposal["record_id"])
    if not old:
        raise PipelineError("Unknown record for revision")
    new = dict(proposal.get("replacement", {})) if proposal["operation"] == "replace" else dict(old, _retired=True)
    if new.get("id") != old["id"]:
        raise PipelineError("Revisions cannot change an existing stable ID")
    w.validate(stage, new)
    if stage == "meanings":
        old_forms = {f["id"]: f for f in old["formulations"]}
        for form in new["formulations"]:
            prior = old_forms.get(form["id"])
            if prior and (prior.get("text") != form["text"] or prior.get("evidence_ids") != form["evidence_ids"]):
                if form["review_state"] != "candidate":
                    raise PipelineError("Changed formulations must return to candidate review")
    if stage == "sources" and (old.get("url") != new.get("url") or old.get("rights") != new.get("rights")):
        if new["authority_reviewed"] is True:
            raise PipelineError("Changed source rights or URL require fresh authority review")
    event = {key: proposal[key] for key in
             ("event_id", "stage", "record_id", "before_digest", "editor", "reason", "operation")}
    event["before"] = old
    event["after"] = new
    event["after_digest"] = digest(new)
    log_path = w.root / "events" / "revisions.jsonl"
    previous_events = {e["event_id"]: e for e in jsonl(log_path)}
    if event["event_id"] in previous_events:
        known = previous_events[event["event_id"]]
        # Original old may now be the successor after a crash/retry.
        if any(known.get(k) != event.get(k) for k in
               ("stage", "record_id", "before_digest", "after_digest", "editor", "reason", "operation")):
            raise PipelineError("Conflicting revision event ID")
        if canonical(old) == canonical(known["after"]):
            return {"event_id": event["event_id"], "status": "already_applied"}
        event = known
        new = known["after"]
    elif digest(old) != proposal["before_digest"]:
        raise PipelineError("Stale predecessor hash; inspect intervening revisions")
    if digest(old) not in (event["before_digest"], event["after_digest"]):
        raise PipelineError("Cannot reconcile interrupted revision")
    if digest(old) == event["after_digest"]:
        return {"event_id": event["event_id"], "status": "already_applied"}
    if event["event_id"] not in previous_events:
        _append_fsync(log_path, event)
    records[event["record_id"]] = new
    path = w.root / "records" / (stage + ".jsonl")
    temp = path.with_name(path.name + ".replacement.tmp")
    with temp.open("w", encoding="utf-8") as out:
        for row in records.values():
            out.write(canonical(row) + "\n")
        out.flush()
        os.fsync(out.fileno())
    os.replace(temp, path)
    w.checkpoint("revision", {"event_id": event["event_id"], "stage": stage,
                              "before_digest": event["before_digest"],
                              "after_digest": event["after_digest"],
                              "next_recommended_thinking": "High"})
    return {"event_id": event["event_id"], "status": "applied", "stage": stage}


def recover_pending(workspace):
    """Complete write-ahead events that survived a crash before file replacement."""
    w = Workspace(workspace)
    events = jsonl(w.root / "events" / "revisions.jsonl")
    completed = []
    for event in events:
        records = w.records(event["stage"])
        current = records[event["record_id"]]
        if digest(current) == event["after_digest"]:
            continue
        if digest(current) != event["before_digest"]:
            raise PipelineError("Revision log and record file disagree; manual intervention needed")
        # Re-apply from the original signed intent; does not append duplicate log.
        completed.append(apply_revision(w.root, {k: event[k] for k in
            ("event_id", "stage", "record_id", "before_digest", "editor", "reason", "operation")} |
            {"replacement": event["after"]}))
    return {"recovered": len(completed)}
