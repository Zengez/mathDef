"""Repaired Wave 1 Stage 4 audit, with dynamic term/evidence coverage.

The historical 31-meaning count is not a target for recovered research.
Every term judged definition-supported must be represented, all other terms
must have an explicit Stage 3 disposition, and locator-only records cannot
justify screened formulations.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from .core import PipelineError, Workspace, atomic_json, jsonl
from .stage3_attempts import require_full_attempt_coverage
from .stage3_review_gate import require_reviewed_term_dispositions


def audit_corrected(workspace, *, seal=False):
    w = Workspace(workspace)
    if not w.state("observations").get("sealed"):
        raise PipelineError("Complete corrected Stage 3 before Stage 4")
    attempts = require_full_attempt_coverage(
        w.root, w.root / "state/stage3_acquisition_attempts.jsonl")
    disposition_summary = require_reviewed_term_dispositions(
        w.root, w.root / "state/stage3_term_reviews.jsonl")
    reviews = {row["term_id"]:row for row in
               jsonl(w.root / "state/stage3_term_reviews.jsonl")}
    supported = {tid for tid, row in reviews.items()
                 if row["decision"] == "supported"}
    observations = w.records("observations")
    substantive = {eid:row for eid,row in observations.items()
                   if row["record_kind"] in ("paraphrase", "licensed_excerpt")}
    meanings = w.records("meanings")
    terms = w.records("terms")
    represented = set()
    classified_evidence = set()
    global_form_ids = set()
    context_counts = Counter()
    for meaning in meanings.values():
        w.validate("meanings", meaning)
        if meaning.get("human_verified") is not False:
            raise PipelineError("Automatic Stage 4 cannot claim independent human verification")
        if meaning.get("review_stage") != "source_cross_checked":
            raise PipelineError("Missing mathematical editorial screening")
        source = meaning.get("source_citation")
        if not isinstance(source, dict) or not source.get("section") or not source.get("url"):
            raise PipelineError("Meaning missing precise source reference")
        for tid in meaning["term_ids"]:
            if tid not in supported:
                raise PipelineError("Meaning has no reviewed substantive term: " + tid)
            represented.add(tid)
            context_counts[tid] += 1
        for form in meaning["formulations"]:
            if form["id"] in global_form_ids:
                raise PipelineError("Duplicate formulation ID: " + form["id"])
            global_form_ids.add(form["id"])
            if form["review_state"] != "screened" or len(form["text"].strip()) < 30:
                raise PipelineError("Meaning contains unscreened or empty formulation")
            if not form.get("editorial_note") and not form.get("equivalence_note"):
                raise PipelineError("Missing formulation source/equivalence rationale")
            for eid in form["evidence_ids"]:
                observation = substantive.get(eid)
                if not observation:
                    raise PipelineError("Locator-only evidence cannot support a formulation")
                if observation["term_id"] not in meaning["term_ids"]:
                    raise PipelineError("Evidence pertains to a different mathematical term")
                if (observation["source_id"] != source.get("source_id") or
                        observation["locator"] != source["url"]):
                    raise PipelineError("Meaning source citation does not match evidence")
                classified_evidence.add(eid)
    if represented != supported:
        raise PipelineError("Stage 4 incomplete: %s supported terms lack meanings" %
                            len(supported - represented))
    if set(substantive) != classified_evidence:
        raise PipelineError("Stage 4 incomplete: %s substantive records still unclassified" %
                            len(set(substantive) - classified_evidence))
    held = sorted(set(terms) - supported)
    report = {
        "schema_version": 2, "stage": "meanings",
        "source_terms_total": len(terms),
        "attempts_accounted_for": attempts["attempts_accounted_for"],
        "reviewed_term_dispositions": disposition_summary["decisions"],
        "supported_term_count": len(supported),
        "term_meanings_count": len(meanings),
        "screened_formulation_count": len(global_form_ids),
        "held_term_count": len(held),
        "held_term_ids": held,
        "terms_with_multiple_mathematical_meanings":
            sorted(tid for tid, count in context_counts.items() if count > 1),
        "human_verified": False,
        "note": "All terms accounted for; only mathematically reviewed substantive evidence is promoted.",
    }
    if seal:
        atomic_json(w.root / "state/stage4_review.json", report)
        return {"sealed": True, **w.seal("meanings"), "review": report}
    return {"sealed": False, "review": report}
