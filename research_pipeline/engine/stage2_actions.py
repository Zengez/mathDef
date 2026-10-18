"""Read-only, bounded GitHub Actions term-title discovery.

Acquires only two explicitly reviewed source indexes, and writes review
artifacts, never production files or sealed stage records. Each page is
checkpointed; failures remain visible and can be retried.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .core import PipelineError, Workspace, atomic_json, canonical, digest, jsonl, required
from .source_intake import extract, fetch_index, safe_source_url

# Do not extend this set without a separate rights/robots review.
NETWORK_SOURCE_ALLOWLIST = frozenset({"src.planetmath", "src.stacks"})
MAX_PAGES = 12


def run(workspace, manifest, output_dir, *, max_pages=MAX_PAGES,
        delay=1.25):
    if not 1 <= max_pages <= MAX_PAGES:
        raise PipelineError("Page limit outside reviewed workflow cap")
    if delay < 1.25:
        raise PipelineError("The source delay may not be reduced below 1.25 seconds")

    w = Workspace(workspace)
    config = w.config()
    if config.get("external_reference_mode") is not True:
        raise PipelineError("External-reference isolation is required")
    if not w.state("sources").get("sealed"):
        raise PipelineError("Source stage must be sealed")
    if w.state("terms").get("sealed"):
        raise PipelineError("Term stage already sealed; do not acquire more")

    manifest = Path(manifest).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    tasks = jsonl(manifest)
    if len({task.get("id") for task in tasks}) != len(tasks):
        raise PipelineError("Duplicate page task IDs")
    if len(tasks) > 250:
        raise PipelineError("Manifest unexpectedly large")

    checksum = digest(tasks)
    output = output_dir / "raw_terms.jsonl"
    checkpoint_path = output_dir / "checkpoint.json"
    report_path = output_dir / "report.json"
    previous = (json.loads(checkpoint_path.read_text(encoding="utf-8"))
                if checkpoint_path.exists() else {})
    if previous and previous.get("manifest_digest") != checksum:
        raise PipelineError("Manifest changed: start with a fresh output directory")
    finished = set(previous.get("completed_ids", []))
    candidates = {r["id"]: r for r in jsonl(output)}
    results = list(previous.get("page_results", []))
    known_sources = w.records("sources")

    def persist():
        output.write_text("".join(canonical(item) + "\n"
                                  for item in sorted(candidates.values(),
                                                     key=lambda row: row["id"])),
                          encoding="utf-8")
        atomic_json(checkpoint_path, {
            "schema_version": 1, "stage": "terms",
            "manifest_digest": checksum,
            "completed_ids": sorted(finished),
            "page_results": results,
            "candidate_count": len(candidates),
            "sealed": False,
        })
        atomic_json(report_path, {
            "stage": "terms", "sealed": False,
            "manifest_pages": len(tasks),
            "allowed_network_sources": sorted(NETWORK_SOURCE_ALLOWLIST),
            "completed_pages": len(finished),
            "candidate_count": len(candidates),
            "page_results": results,
            "errors": [r for r in results if r["status"] == "error"],
            "blocked_pages": [r for r in results if r["status"] == "blocked"],
            "partial": len(finished) < len(eligible),
            "review_required": True,
            "note": "Raw title candidates only. No ingestion, human verification, or seal.",
        })

    eligible = []
    for task in tasks:
        for key in ("id", "source_id", "url"):
            required(task, key)
        source = known_sources.get(task["source_id"])
        if not source:
            raise PipelineError("Unregistered source in manifest")
        if task["source_id"] not in NETWORK_SOURCE_ALLOWLIST:
            continue
        if not source["authority_reviewed"] or source["rights"] not in (
                "permitted", "locator_only") or source["access"] != "free":
            raise PipelineError("Source is not approved for automatic index intake")
        safe_source_url(task["url"], source)
        if task.get("profile", "headings") not in ("headings", "glossary", "linked-list", "stacks-sections"):
            raise PipelineError("Unknown parser profile")
        eligible.append((task, source))

    attempted = 0
    for task, source in eligible:
        if task["id"] in finished:
            continue
        if attempted >= max_pages:
            break
        attempted += 1
        try:
            html = fetch_index(task["url"], source, delay=delay)
            discovered = extract(w.root, task["source_id"], task["url"], html,
                                 stage="terms", profile=task.get("profile", "headings"))
            if (task.get("profile") == "stacks-sections" and
                    not discovered and os.environ.get("STAGE2_DEBUG_STRUCTURE") == "1"):
                # Temporary structural probe: no article text or definitions.
                import re
                marker = html.find("Section")
                fragment = html[max(0, marker - 80):marker + 320] if marker >= 0 else ""
                print("Stacks section HTML layout probe:",
                      repr(fragment.replace("\\n", " ")[:400]))
            added = 0
            for item in discovered:
                old = candidates.get(item["id"])
                if old is not None and canonical(old) != canonical(item):
                    raise PipelineError("Conflicting discovery ID: " + item["id"])
                if old is None:
                    candidates[item["id"]] = item
                    added += 1
            finished.add(task["id"])
            results = [r for r in results if r["id"] != task["id"]]
            results.append({"id": task["id"], "source_id": task["source_id"],
                            "url": task["url"], "status": "ok",
                            "discovered": len(discovered), "added": added})
        except (OSError, ValueError, UnicodeError) as exc:
            # A failing page is NOT completed; subsequent runs can retry it.
            results = [r for r in results if r["id"] != task["id"]]
            blocked = "Robots policy unavailable" in str(exc)
            results.append({"id": task["id"], "source_id": task["source_id"],
                            "url": task["url"], "status": "blocked" if blocked else "error",
                            "error": str(exc)[:500]})
        persist()
    persist()
    return json.loads(report_path.read_text(encoding="utf-8"))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--max-pages", type=int, default=MAX_PAGES)
    args = p.parse_args(argv)
    try:
        report = run(args.workspace, args.manifest, args.output_dir,
                     max_pages=args.max_pages)
    except (PipelineError, OSError, json.JSONDecodeError) as exc:
        p.exit(2, "Stage 2 workflow error: " + str(exc) + "\n")
    print(json.dumps(report, indent=2))
    if not report["completed_pages"] or report["errors"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
