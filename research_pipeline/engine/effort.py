"""Optional, evidence-based cost and effort log for the reconstruction benchmark.

Never infer thinking level, human effort, API expenditure, or web calls.
Store ONLY numbers explicitly supplied for a completed batch.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .core import PipelineError, Workspace, canonical, jsonl, require_id


def log_effort(workspace, event):
    w = Workspace(workspace)
    w.config()
    require_id(event.get("id"))
    if event.get("thinking") not in ("Instant", "Medium", "High", "none"):
        raise PipelineError("Thinking effort must be Instant/Medium/High/none")
    for name in ("minutes", "research_calls", "records_examined"):
        number = event.get(name)
        if not isinstance(number, (int, float)) or isinstance(number, bool) or number < 0:
            raise PipelineError("Missing/nonnegative numeric effort field: " + name)
    if not isinstance(event.get("stage"), str) or not event["stage"]:
        raise PipelineError("Missing stage")
    event = dict(event)
    event.setdefault("logged_utc", datetime.now(timezone.utc).isoformat())
    path = w.root / "state" / "effort.jsonl"
    existing = {row["id"]: row for row in jsonl(path)}
    if event["id"] in existing:
        old = dict(existing[event["id"]])
        new = dict(event)
        old.pop("logged_utc", None)
        new.pop("logged_utc", None)
        if canonical(old) != canonical(new):
            raise PipelineError("Conflicting effort event ID")
        return {"id": event["id"], "already_logged": True}
    with path.open("a", encoding="utf-8") as out:
        out.write(canonical(event) + "\n")
        out.flush()
    return {"id": event["id"], "already_logged": False}


def summarize(workspace):
    w = Workspace(workspace)
    totals = {"minutes": 0.0, "research_calls": 0, "records_examined": 0,
              "events": 0, "effort_by_stage": {}}
    for event in jsonl(w.root / "state" / "effort.jsonl"):
        totals["events"] += 1
        stage = totals["effort_by_stage"].setdefault(event["stage"],
             {"minutes": 0.0, "research_calls": 0, "records_examined": 0})
        for key in ("minutes", "research_calls", "records_examined"):
            totals[key] += event[key]
            stage[key] += event[key]
    return totals


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--event-file", type=Path, help="A reviewed batch-effort record JSON")
    args = p.parse_args()
    if args.event_file:
        report = log_effort(args.workspace, json.loads(args.event_file.read_text(encoding="utf-8")))
    else:
        report = summarize(args.workspace)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
