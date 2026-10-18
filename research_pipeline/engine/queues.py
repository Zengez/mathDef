"""Generate deterministic work queues for research to be performed in chat.

This module NEVER searches the original mathDef corpus or directly calls an AI
model. Its jobs describe the inputs that a human/assistant should investigate.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from .core import EFFORT, PipelineError, Workspace, canonical


def normalized(label):
    return " ".join(re.findall(r"[a-z0-9]+", label.casefold()))


def make_queue(workspace, stage, batch_size=10):
    w = Workspace(workspace)
    w.config()
    if batch_size < 1:
        raise PipelineError("batch_size must be positive")
    if stage == "sources":
        records = [{
            "id": "discover.sources",
            "task": "Find authoritative source collections for the configured project; evaluate access, rights, scope, and reliability. Do not collect terminology.",
            "project": w.config()["project"],
        }]
    elif stage == "terms":
        records = [{
            "id": "discover.terms." + s["id"], "source_id": s["id"],
            "url": s["url"],
            "task": "Review permitted index/glossary/TOC pages to record candidate term names and exact source locators. Do not collect full definitions.",
        } for s in w.records("sources").values()
            if s["authority_reviewed"] and s["access"] == "free"
            and s["rights"] in ("permitted", "locator_only")]
    elif stage == "observations":
        records = [{
            "id": "discover.content." + t["id"], "term_id": t["id"],
            "label": t["label"], "source_id": t["source_id"],
            "locator": t["locator"],
            "task": "Find candidate content at this permitted source locator. Record exact provenance, reuse category, and independently authored paraphrases. Preserve variant observations separately.",
        } for t in w.records("terms").values()
            if w.records("sources")[t["source_id"]]["access"] == "free"
            and w.records("sources")[t["source_id"]]["rights"] in ("permitted", "locator_only")]
    elif stage == "meanings":
        terms = list(w.records("terms").values())
        observations = w.records("observations")
        terms.sort(key=lambda t: (normalized(t["label"]), t["id"]))
        records = []
        for start in range(0, len(terms), batch_size):
            group = terms[start:start + batch_size]
            records.append({
                "id": "classify." + str(start // batch_size + 1),
                "term_ids": [t["id"] for t in group],
                "observations": [o["id"] for o in observations.values()
                                 if o["term_id"] in {t["id"] for t in group}],
                "task": "Group synonymous terms and contextual meanings; identify equivalent/restricted formulations, retain all evidence, and identify uncertain classifications. Neighboring batches may later require reconciliation.",
            })
    elif stage == "relations":
        records = [{
            "id": "link." + m["id"], "meaning_id": m["id"],
            "formulations": [f["id"] for f in m["formulations"]],
            "context": m["context"],
            "task": "Research relationship types, plausible targets, dependencies, and ambiguity. Propose contextual priorities without pretending they are confirmed.",
        } for m in w.records("meanings").values()]
    else:
        raise PipelineError("Unsupported queue stage")
    target = w.root / "tasks" / (stage + ".jsonl")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as output:
        for record in records:
            output.write(canonical(record) + "\n")
    handoff = {
        "stage": stage, "tasks": len(records), "queue_file": str(target),
        "batch_size": batch_size, "recommended_thinking": EFFORT[stage],
        "completed_stage_records": len(w.records(stage)),
        "next_action": "Work through the next unprocessed queue item; ingest resulting records in small batches and commit checkpoint files."
    }
    # Do not overwrite a stage's ingestion checkpoint, which tracks durable actual data.
    from .core import atomic_json
    atomic_json(w.root / "tasks" / (stage + ".summary.json"), handoff)
    return handoff
