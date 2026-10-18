"""Non-bypassable per-term editorial review gate for repaired Stage 3.

Every document acquisition outcome must receive an explicit disposition.
A source fetch or a definition anchor alone NEVER becomes a vetted definition.
Inaccessible pages can be held by their objectively recorded failure reason.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from .core import PipelineError, Workspace, canonical, jsonl
from .stage3_attempts import CONTENT_VISITED, require_full_attempt_coverage, catalog_digest

TERMINAL_REVIEW = {"supported", "no_suitable_definition", "access_blocked"}
ACCESS_FAILURES = {"policy_blocked", "fetch_failed_after_retries"}


def build_review_queue(workspace, out):
    w = Workspace(workspace)
    attempts_file = w.root / "state" / "stage3_acquisition_attempts.jsonl"
    require_full_attempt_coverage(w.root, attempts_file)
    attempts = {x["term_id"]: x for x in jsonl(attempts_file)}
    existing = w.records("observations")
    evidence = {}
    for obs in existing.values():
        if obs["record_kind"] == "paraphrase":
            evidence.setdefault(obs["term_id"], []).append(obs["id"])
    rows = []
    for tid, term in sorted(w.records("terms").items()):
        source_attempt = attempts[tid]
        failure = source_attempt["outcome"] in ACCESS_FAILURES
        rows.append({
            "term_id": tid, "label": term["label"],
            "source_id": term["source_id"], "locator": term["locator"],
            "term_catalog_digest": catalog_digest(w),
            "attempt_outcome": source_attempt["outcome"],
            "page_fetched": source_attempt["page_fetched"],
            "definition_candidates": source_attempt.get("definition_candidates", []),
            "known_substantive_observation_ids": evidence.get(tid, []),
            "decision": "access_blocked" if failure else "needs_review",
            "editorial_reason": (
                "Fetch prohibited by source policy or exhausted retrieval retries; "
                "no mathematical text has been read from this page."
                if failure else "Requires actual reading and mathematical review of the source page."),
            "reviewed_by": "automatic_access_check" if failure else None,
            "research_retry_required": source_attempt["outcome"] == "fetch_failed_after_retries",
            "human_verified": False,
        })
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(canonical(x)+"\n" for x in rows), encoding="utf-8")
    return {"terms": len(rows), "accessible_needing_review": sum(
        r["decision"] == "needs_review" for r in rows),
        "blocked_with_recorded_reason": sum(r["decision"] == "access_blocked" for r in rows)}


def require_reviewed_term_dispositions(workspace, reviews_path):
    w = Workspace(workspace)
    attempts_file = w.root / "state" / "stage3_acquisition_attempts.jsonl"
    require_full_attempt_coverage(w.root, attempts_file)
    attempts = {x["term_id"]: x for x in jsonl(attempts_file)}
    terms = w.records("terms")
    substantive = {}
    for x in w.records("observations").values():
        if x["record_kind"] in ("paraphrase", "licensed_excerpt"):
            substantive[x["id"]] = x
    rows = jsonl(reviews_path)
    by_id = {}
    tally = Counter()
    for row in rows:
        tid = row.get("term_id")
        if tid not in terms or tid in by_id:
            raise PipelineError("Missing or duplicate term review identity: " + str(tid))
        by_id[tid] = row
        term, attempt = terms[tid], attempts[tid]
        if (row.get("source_id"), row.get("locator"), row.get("label")) != (
                term["source_id"], term["locator"], term["label"]):
            raise PipelineError("Term review does not refer to sealed term")
        if row.get("term_catalog_digest") != catalog_digest(w):
            raise PipelineError("Stale term review catalog digest")
        if row.get("attempt_outcome") != attempt["outcome"]:
            raise PipelineError("Term review stale after attempt retry")
        decision = row.get("decision")
        if decision not in TERMINAL_REVIEW | {"needs_review"}:
            raise PipelineError("Unknown editorial disposition for " + tid)
        if row.get("human_verified") is not False:
            raise PipelineError("Stage 3 cannot claim independent human verification")
        reason = row.get("editorial_reason", "")
        if not isinstance(reason, str) or len(reason.strip()) < 25:
            raise PipelineError("Editorial decision lacks meaningful reason: " + tid)
        if decision == "access_blocked":
            if attempt["outcome"] not in ACCESS_FAILURES:
                raise PipelineError("Cannot mark a fetched page as access blocked")
            if row.get("reviewed_by") != "automatic_access_check":
                raise PipelineError("Access status must follow source policy evidence")
        elif decision == "supported":
            if attempt["outcome"] not in CONTENT_VISITED:
                raise PipelineError("Cannot support definition from an unfetched page")
            if not row.get("reviewed_by") or row["reviewed_by"] == "automatic_access_check":
                raise PipelineError("Source page needs mathematical reviewer attribution")
            ids = row.get("evidence_ids", [])
            if not ids or any(eid not in substantive or
                              substantive[eid]["term_id"] != tid for eid in ids):
                raise PipelineError("Supported definition lacks substantive term-matched evidence")
        elif decision == "no_suitable_definition":
            if attempt["outcome"] not in CONTENT_VISITED:
                raise PipelineError("Unfetched page cannot be judged no-definition")
            if not row.get("reviewed_by") or row["reviewed_by"] == "automatic_access_check":
                raise PipelineError("No-definition verdict needs actual source review")
            if len(reason.strip()) < 50:
                raise PipelineError("No-definition verdict needs detailed evidence")
        tally[decision] += 1

    if len(by_id) != len(terms):
        raise PipelineError("Stage 3 cannot seal: %s of %s term reviews accounted for" %
                            (len(by_id), len(terms)))
    if tally["needs_review"]:
        raise PipelineError("Stage 3 cannot seal: %s fetched terms still lack editorial review" %
                            tally["needs_review"])
    return {
        "term_count": len(terms), "decisions": dict(tally),
        "reviewed_or_source_blocked_all": True,
        "caveat": "Access-blocked outcomes remain unresolved, not substantive definitions.",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", required=True, type=Path)
    p.add_argument("--reviews", required=True, type=Path)
    p.add_argument("--prepare", action="store_true")
    args = p.parse_args()
    result = (build_review_queue(args.workspace, args.reviews) if args.prepare
              else require_reviewed_term_dispositions(args.workspace, args.reviews))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
