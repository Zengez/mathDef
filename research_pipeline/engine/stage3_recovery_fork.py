"""Safely reopen Wave 1 Stage 3 without rewriting any historical sealed stage.

After EVERY sealed term has an acquisition outcome, create a new isolated
workspace from ONLY the original experiment's sealed Stage 1/2 records.
Carry forward Stage 3 observations as candidates, not as a sealed stage.
Never carry forward the prematurely sealed Stage 4 meanings.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from .core import PipelineError, Workspace, atomic_json
from .stage3_attempts import require_full_attempt_coverage
from .stage3_review_gate import build_review_queue


def fork(original, destination):
    original = Workspace(original)
    original.config()
    destpath = Path(destination).resolve()
    if destpath.exists() or destpath == original.root:
        raise PipelineError("Recovery destination must be a fresh, absent directory")
    if not original.state("sources").get("sealed") or not original.state("terms").get("sealed"):
        raise PipelineError("Cannot fork without sealed Stage 1/2 records")
    ledger = original.root / "state/stage3_acquisition_attempts.jsonl"
    audit = require_full_attempt_coverage(original.root, ledger)
    config = dict(original.config())
    config.update({
        "project": "mathDef independent reconstruction — corrected Wave 1",
        "require_full_definition_attempts": True,
        "require_reviewed_term_dispositions": True,
        "repaired_from": "research_pipeline/experiments/reconstruction-v1",
        "correction_reason": (
            "Stage 3 previously sealed using URL coverage without attempting "
            "substantive source acquisition for most Stage 2 terms."),
    })
    dest = Workspace(destpath)
    dest.init(config)
    for stage in ("sources", "terms"):
        source = original.root / "records" / (stage + ".jsonl")
        target = dest.root / "records" / (stage + ".jsonl")
        shutil.copy2(source, target)
        info = dest.seal(stage)
        previous = original.state(stage)
        if info["record_digest"] != previous.get("record_digest"):
            raise PipelineError("Frozen source/term registry changed during recovery fork")
    # Prior Stage 3 has useful, but incomplete, observations. Preserve each
    # existing ID and source attribution; import as editable candidates.
    old_obs = original.root / "records/observations.jsonl"
    if old_obs.exists():
        dest.ingest("observations", old_obs, batch_size=25)
        # CI runners have ephemeral absolute directories; keep lineage portable.
        state = dest.state("observations")
        state["last_input"] = "research_pipeline/experiments/" + original.root.name + "/records/observations.jsonl"
        atomic_json(dest.root / "state/observations.json", state)
        dest.checkpoint("observations", state)
    shutil.copy2(ledger, dest.root / "state/stage3_acquisition_attempts.jsonl")
    summary = original.root / "state/stage3_acquisition_report.json"
    if summary.exists():
        shutil.copy2(summary, dest.root / "state/stage3_acquisition_report.json")
    reviews = dest.root / "state/stage3_term_reviews.jsonl"
    prepared = build_review_queue(dest.root, reviews)
    lineage = {
        "schema_version": 1, "mode": "corrected_wave1_stage3",
        "original_workspace": "research_pipeline/experiments/" + original.root.name,
        "source_registry_digest": original.state("sources")["record_digest"],
        "term_registry_digest": original.state("terms")["record_digest"],
        "original_observation_digest": original.state("observations").get("record_digest"),
        "archived_meanings_digest": original.state("meanings").get("record_digest"),
        "original_observation_count": len(original.records("observations")),
        "original_meanings_carried_forward": False,
        "per_term_attempts_accounted": audit["attempts_accounted_for"],
        "page_fetches": audit["source_documents_fetched"],
        "source_access_blocked": audit["policy_blocked"],
        "source_fetch_failed": audit["fetch_failed_after_retries"],
        "editorial_queue": prepared,
        "reason": "Historically sealed Stage 3/4 preserved, never overwritten; recovery requires review before re-sealing.",
        "next_stage": "unsealed Stage 3 review and independently authored mathematical evidence",
    }
    atomic_json(dest.root / "state/stage3_recovery_lineage.json", lineage)
    return {"workspace": str(dest.root), **lineage}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--original", type=Path, required=True)
    p.add_argument("--destination", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(fork(args.original, args.destination), indent=2))


if __name__ == "__main__":
    main()
