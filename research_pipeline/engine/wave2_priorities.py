"""Generate *prioritized* independent second-wave research tasks from frozen Wave 1.

Only reads the Wave 1 research workspace and the Wave 2 fork: never read
production mathDef definitions, variants, citation records or comparison output.
Tasks are unsolved leads, not inferred definitions or automatically approved links.
"""
from __future__ import annotations
import argparse
import json
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

from .core import Workspace, PipelineError, atomic_json, canonical, digest, jsonl


def task_id(kind, key):
    return "v2." + kind + "." + hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]


def build(first_wave, second_wave):
    first_wave, second_wave = Workspace(first_wave), Workspace(second_wave)
    freeze_path = first_wave.root / "state/wave1_freeze.json"
    baseline_path = second_wave.root / "state/baseline.json"
    if not freeze_path.exists() or not baseline_path.exists():
        raise PipelineError("Expected frozen Wave 1 and independently forked Wave 2")
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    if freeze.get("state") != "FROZEN" or baseline.get("mode") != "second_wave":
        raise PipelineError("Incorrect research lineage for Wave 2")
    if baseline.get("first_wave_digest") != freeze.get("published_catalog_digest"):
        raise PipelineError("Wave 2 fork does not derive from the frozen Wave 1 catalog")
    if digest(first_wave.publication()) != freeze["published_catalog_digest"]:
        raise PipelineError("Wave 1 no longer matches its frozen catalog")
    for stage in ("sources", "terms", "observations", "meanings", "relations"):
        inherited = first_wave.records(stage)
        mutable = second_wave.records(stage)
        for key, value in inherited.items():
            if mutable.get(key) != value:
                raise PipelineError("Inherited Wave 1 record was changed: " + stage + " " + key)

    term_reviews = jsonl(first_wave.root / "state/stage3_term_reviews.jsonl")
    formulation_reviews = jsonl(first_wave.root / "state/stage5_formulation_reviews.jsonl")
    meanings = first_wave.records("meanings")
    sources = first_wave.records("sources")
    terms = first_wave.records("terms")
    assert len(term_reviews) == len(terms) == 318
    assert len(formulation_reviews) == 431

    tasks = []
    def add(kind, priority, key, **fields):
        tasks.append({
            "id": task_id(kind, key), "kind": kind,
            "priority": priority, "status": "unresearched",
            "origin": "frozen_independent_wave1", **fields
        })

    for review in formulation_reviews:
        state = review["decision"]
        if state not in ("held_ambiguity", "no_supported_target"):
            continue
        fm = review["formulation_id"]
        matching = [(m, f) for m in meanings.values()
                    for f in m["formulations"] if f["id"] == fm]
        if len(matching) != 1:
            raise PipelineError("Missing/non-unique formulation identity: " + fm)
        meaning, form = matching[0]
        add("held_link_research" if state == "held_ambiguity" else "missing_foundation",
            0 if state == "held_ambiguity" else 1, fm,
            formulation_id=fm, meaning_id=meaning["id"], label=meaning["display_term"],
            context=meaning["context"], source_formulation=form["text"],
            source_review_reason=review["editorial_reason"],
            action=("Research additional accessible definitions for the ambiguous source "
                    "concept; distinguish mathematical contexts before linking"
                    if state == "held_ambiguity"
                    else "Find a separately defined missing mathematical prerequisite "
                         "in an independently approved and accessible source; then review its context"))
    for review in term_reviews:
        state = review["decision"]
        if state not in ("access_blocked", "no_suitable_definition"):
            continue
        tid = review["term_id"]
        term = terms[tid]
        add("blocked_source_recovery" if state == "access_blocked" else "unproductive_section_retry",
            2 if state == "access_blocked" else 3, tid,
            term_id=tid, label=term["label"], initial_source=term["source_id"],
            source_locator=term["locator"], original_disposition=state,
            source_review_reason=review["editorial_reason"],
            action="Look for the mathematical definition using independent accessible references; never retry a policy-blocked fetch")
    by_title = defaultdict(list)
    for meaning in meanings.values():
        by_title[" ".join(meaning["display_term"].casefold().split())].append(meaning)
    for title, found in sorted(by_title.items()):
        if len(found) <= 1:
            continue
        add("cross_source_variant_review", 2, title,
            label=found[0]["display_term"], candidate_meaning_ids=[m["id"] for m in found],
            contexts=[m["context"] for m in found],
            action="Compare hypotheses, mathematical objects and equivalence versus context-specific variants; no automatic merge")
    for source in sources.values():
        add("source_collection_resurvey", 4, source["id"],
            source_id=source["id"], label=source["title"],
            original_url=source["url"], rights=source["rights"], access=source["access"],
            action="Reassess authoritative definition coverage and permitted access; check new index routes; do not bypass robots or restrictions")

    tasks.sort(key=lambda x: (x["priority"], x["kind"], x["label"].casefold(), x["id"]))
    ids = [x["id"] for x in tasks]
    if len(ids) != len(set(ids)):
        raise PipelineError("Priority task identity collision")
    kind_counts = dict(sorted(Counter(x["kind"] for x in tasks).items()))
    expected = {"held_link_research": 4, "missing_foundation": 89,
                "blocked_source_recovery": 27, "unproductive_section_retry": 59,
                "cross_source_variant_review": 4, "source_collection_resurvey": 9}
    if kind_counts != expected:
        raise PipelineError("Unexpected Wave 1 gaps; audit scope rather than silently discard any: " + str(kind_counts))
    out = second_wave.root / "wave2/prioritized_research.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(canonical(x) + "\n" for x in tasks)
    if out.exists() and out.read_text(encoding="utf-8") != payload:
        raise PipelineError("Priority queue differs from existing file; version the proposed revision")
    out.write_text(payload, encoding="utf-8")
    result = {
        "phase": "source_discovery_and_context_research",
        "source": "frozen independent Wave 1 review ledgers",
        "ready": True, "total_tasks": len(tasks),
        "priority_counts": kind_counts,
        "first_wave_catalog_digest": freeze["published_catalog_digest"],
        "priority_queue_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "work_queue": str(out),
        "original_mathdef_corpus_used": False,
        "coverage_note": "All inherited missing links, held cases, blocked/no-content headings, cross-source duplicate names and source collections are individually represented.",
        "next": "Individually research foundation/ambiguity leads and source licenses; do not automatically accept candidate definitions or repeat blocked source retrieval."
    }
    atomic_json(second_wave.root / "state/wave2_priorities.json", result)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--first-wave", required=True, type=Path)
    p.add_argument("--second-wave", required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(build(args.first_wave, args.second_wave), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
