"""Resume a source-index discovery batch across many vetted HTML index pages.

Manifest is JSONL with {id, source_id, url, profile, html_path} rows.
Offline HTML fixtures/caches are the default; remote fetching is explicit.
Records are checkpointed every page and de-duplicated on resume.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .core import PipelineError, Workspace, atomic_json, canonical, digest, jsonl, require_id, required
from .source_intake import extract, fetch_index


def run(workspace, manifest, output, checkpoint, stage, *, network=False,
        batch_pages=5, limit_pages=None, licensed_excerpts=False):
    w = Workspace(workspace)
    w.config()
    if stage not in ("terms", "observations") or batch_pages < 1:
        raise PipelineError("Unsupported batch stage or batch size")
    manifest = Path(manifest).resolve()
    output = Path(output).resolve()
    checkpoint = Path(checkpoint).resolve()
    rows = jsonl(manifest)
    checksum = digest(rows)
    if len({r["id"] for r in rows}) != len(rows):
        raise PipelineError("Manifest task IDs must be unique")
    for r in rows:
        for field in ("id", "source_id", "url"):
            required(r, field)
        require_id(r["id"])
        if r.get("html_path") is None and not network:
            raise PipelineError("Network mode disabled and task has no local HTML")
    previous = json.loads(checkpoint.read_text(encoding="utf-8")) if checkpoint.exists() else {}
    if previous and (previous["manifest_digest"] != checksum or previous["stage"] != stage):
        raise PipelineError("Cannot resume using a changed manifest or different stage")
    processed_ids = set(previous.get("completed_ids", []))
    output.parent.mkdir(parents=True, exist_ok=True)
    existing = {r["id"]: r for r in jsonl(output)}
    completed_this_run, written = 0, 0
    stop_after = limit_pages if limit_pages is not None else batch_pages
    if stop_after < 1:
        raise PipelineError("limit_pages must be positive")
    for task in rows:
        if task["id"] in processed_ids:
            continue
        source = w.records("sources").get(task["source_id"])
        if not source:
            raise PipelineError("Unregistered source: " + task["source_id"])
        if task.get("html_path"):
            local = Path(task["html_path"])
            if not local.is_absolute():
                local = manifest.parent / local
            data = local.read_bytes()
            if len(data) > 2_000_000:
                raise PipelineError("Offline HTML exceeds size limit")
            page = data.decode("utf-8")
        else:
            page = fetch_index(task["url"], source)
        findings = extract(w.root, task["source_id"], task["url"], page,
                           stage=stage, profile=task.get("profile", "headings"),
                           allow_excerpts=licensed_excerpts)
        new = []
        for row in findings:
            if row["id"] in existing:
                if canonical(existing[row["id"]]) != canonical(row):
                    raise PipelineError("Conflicting record with same ID " + row["id"])
                continue
            new.append(row)
            existing[row["id"]] = row
        if new:
            with output.open("a", encoding="utf-8") as out:
                for row in new:
                    out.write(canonical(row) + "\n")
                out.flush()
                os.fsync(out.fileno())
        written += len(new)
        processed_ids.add(task["id"])
        completed_this_run += 1
        # Commit page-level completion atomically. Safe even if interrupted
        # after writing data but before updating the checkpoint.
        atomic_json(checkpoint, {
            "schema_version": 1, "stage": stage, "manifest_digest": checksum,
            "completed_ids": sorted(processed_ids), "records_written_total": len(existing),
            "recommended_thinking": "Instant" if stage == "terms" else "Medium",
            "next_action": "Continue this manifest, then inspect and ingest the result JSONL."
        })
        if completed_this_run >= stop_after:
            break
    return {"stage": stage, "pages_this_run": completed_this_run,
            "completed_pages": len(processed_ids), "total_pages": len(rows),
            "new_candidate_records": written, "records_in_output": len(existing),
            "output": str(output), "checkpoint": str(checkpoint)}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--stage", choices=("terms", "observations"), required=True)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--checkpoint", required=True, type=Path)
    p.add_argument("--network", action="store_true", help="Explicitly permit eligible HTTPS fetches")
    p.add_argument("--licensed-excerpts", action="store_true")
    p.add_argument("--batch-pages", type=int, default=5)
    p.add_argument("--limit-pages", type=int)
    args = p.parse_args(argv)
    result = run(args.workspace, args.manifest, args.output, args.checkpoint, args.stage,
                 network=args.network, batch_pages=args.batch_pages,
                 limit_pages=args.limit_pages, licensed_excerpts=args.licensed_excerpts)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
