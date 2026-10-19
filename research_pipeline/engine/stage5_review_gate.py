"""Audited formulation-level Stage 5 links for independent reconstruction.

No production mathDef data is read. The Stage 5 seal MUST account for every
Stage 4 formulation, including explicit no-link and held-ambiguity outcomes.
Text-matching alone never changes a review's pending state.
"""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

from .core import PipelineError, Workspace, atomic_json, canonical, digest, jsonl
from .queues import make_queue

DECISIONS = {"needs_review", "linked", "no_supported_target", "held_ambiguity"}
REVIEW_PATH = Path("state/stage5_formulation_reviews.jsonl")


def atomic_jsonl(path, rows):
    """Write a review ledger atomically so an interruption cannot truncate it."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    try:
        with temp.open("w", encoding="utf-8") as out:
            out.write("".join(canonical(row) + "\n" for row in rows))
            out.flush()
            os.fsync(out.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def validate_screened_edge(row, meanings, forms, w):
    """Validate independently screened edge against both sealed endpoints."""
    fid, target = row.get("from_formulation"), row.get("target_meaning")
    if fid not in forms or target not in meanings:
        raise PipelineError("Unresolved relation endpoint: " + str(row.get("id")))
    parent, form = forms[fid]
    if parent["id"] == target:
        raise PipelineError("Self-link is not a definitional dependency")
    if row.get("relation_type") not in ("definition_uses", "logical_implication", "equivalent_characterization") or row.get("review_state") != "screened":
        raise PipelineError("Unknown or unscreened mathematical relationship type")
    if row.get("human_verified") is not False:
        raise PipelineError("Assistant editorial research cannot claim formal human verification")
    phrase = row.get("source_phrase", "")
    if not isinstance(phrase, str) or not phrase.strip() or phrase.casefold() not in form["text"].casefold():
        raise PipelineError("Dependency anchor missing from source formulation: " + str(row.get("id")))
    if row.get("source_locator") != parent["source_citation"]["url"]:
        raise PipelineError("Source provenance mismatch: " + str(row.get("id")))
    if row.get("target_locator") != meanings[target]["source_citation"]["url"]:
        raise PipelineError("Target provenance mismatch: " + str(row.get("id")))
    reason = row.get("editorial_reason")
    if not isinstance(reason, str) or len(reason.strip()) < 50:
        raise PipelineError("Every screened edge needs individual mathematical rationale")
    if not isinstance(row.get("reviewed_by"), str) or not row["reviewed_by"].strip():
        raise PipelineError("Screened edges need editorial attribution")
    w.validate("relations", row)


def inventory(w):
    if not w.state("meanings").get("sealed"):
        raise PipelineError("Seal Stage 4 before preparing Stage 5")
    meanings = w.records("meanings")
    if w.state("meanings").get("record_digest") != digest(list(meanings.values())):
        raise PipelineError("Stage 4 meanings changed after sealing")
    forms = {}
    for meaning in meanings.values():
        for form in meaning["formulations"]:
            if form["id"] in forms:
                raise PipelineError("Stage 5: repeated formulation identity")
            if form["review_state"] != "screened":
                raise PipelineError("Stage 5: unscreened upstream formulation")
            forms[form["id"]] = (meaning, form)
    return meanings, forms


def prepare(workspace):
    w = Workspace(workspace)
    meanings, forms = inventory(w)
    out = w.root / REVIEW_PATH
    if out.exists():
        raise PipelineError("Existing Stage 5 ledger: preserve reviews; do not reset")
    make_queue(w.root, "relations", batch_size=10)
    lines = []
    for form_id, (meaning, form) in sorted(forms.items()):
        lines.append({
            "formulation_id": form_id, "meaning_id": meaning["id"],
            "meaning_catalog_digest": w.state("meanings")["record_digest"],
            "decision": "needs_review", "relation_ids": [],
            "editorial_reason": "Pending individual cross-definition research; no link or no-link judgment has been made.",
            "reviewed_by": None, "human_verified": False,
        })
    out.parent.mkdir(parents=True, exist_ok=True)
    atomic_jsonl(out, lines)
    w.checkpoint("relations", {"sealed": False, "reviewed_formulations": 0,
                               "formulations": len(forms), "meanings": len(meanings),
                               "next": "Apply source-checked relation batches, review each remaining formulation"})
    return {"meaning_tasks": len(meanings), "formulation_reviews_prepared": len(lines),
            "reviewed": 0, "pending": len(lines)}


def apply_batch(workspace, batch):
    w = Workspace(workspace)
    meanings, forms = inventory(w)
    if w.state("relations").get("sealed"):
        raise PipelineError("Cannot update sealed Stage 5")
    ledger = w.root / REVIEW_PATH
    if not ledger.is_file():
        raise PipelineError("Run --prepare before applying relation batches")
    reviews = {x["formulation_id"]: x for x in jsonl(ledger)}
    if set(reviews) != set(forms):
        raise PipelineError("Review ledger must cover the exact sealed Stage 4 formulations")
    batch_rows = jsonl(batch)
    if not batch_rows:
        raise PipelineError("No reviewed relations in batch")
    by_form = defaultdict(list)
    seen = set()
    existing_edges = w.records("relations")
    for row in batch_rows:
        rid, fid = row.get("id"), row.get("from_formulation")
        if rid in seen:
            raise PipelineError("Duplicate reviewed link in batch")
        seen.add(rid)
        validate_screened_edge(row, meanings, forms, w)
        prior = reviews[fid]
        # Important: check review conflicts and record collisions BEFORE any writes.
        if prior["decision"] not in ("needs_review", "linked"):
            raise PipelineError("Cannot overwrite a no-link/ambiguity disposition: " + fid)
        if rid in existing_edges and canonical(existing_edges[rid]) != canonical(row):
            raise PipelineError("Record ID collision with changed content: " + rid)
        by_form[fid].append(row)
    # A replay of a partially interrupted batch is safe: record and ledger updates
    # are individually restartable, and both must be valid before committing.
    ingest_result = w.ingest("relations", batch, batch_size=10)
    for fid, links in by_form.items():
        review = reviews[fid]
        if review["decision"] not in ("needs_review", "linked"):
            raise PipelineError("Cannot overwrite a no-link/ambiguity disposition: " + fid)
        previous = set(review.get("relation_ids", []))
        previous.update(r["id"] for r in links)
        review["decision"] = "linked"
        review["relation_ids"] = sorted(previous)
        review["reviewed_by"] = "assistant_source_comparison_2026-10-18"
        review["editorial_reason"] = (
            "Manually screened source formulation against exact reconstructed target meanings; "
            "individual mathematical reasons and both source locators are attached to each relation.")
    atomic_jsonl(ledger, [reviews[k] for k in sorted(reviews)])
    result = audit(workspace)
    w.checkpoint("relations", {"sealed": False,
                               "reviewed_formulations": result["reviewed"],
                               "formulations": result["formulations"],
                               "links": result["screened_relations"],
                               "next": "Continue all remaining formulation reviews; do not seal early"})
    return {"ingestion": ingest_result, "review": result}



def apply_dispositions(workspace, batch):
    """Save individually reasoned no-link or held-ambiguity reviews; never infer them."""
    w = Workspace(workspace)
    _, forms = inventory(w)
    if w.state("relations").get("sealed"):
        raise PipelineError("Cannot change sealed Stage 5 dispositions")
    ledger = w.root / REVIEW_PATH
    if not ledger.is_file():
        raise PipelineError("Prepare Stage 5 reviews first")
    existing = {r["formulation_id"]: r for r in jsonl(ledger)}
    if set(existing) != set(forms):
        raise PipelineError("Stale or incomplete Stage 5 ledger")
    rows = jsonl(batch)
    if not rows:
        raise PipelineError("No individually reviewed dispositions")
    seen = set()
    for item in rows:
        fid = item.get("formulation_id")
        if fid not in forms or fid in seen:
            raise PipelineError("Unknown or repeated disposition formulation")
        seen.add(fid)
        if item.get("decision") not in ("no_supported_target", "held_ambiguity"):
            raise PipelineError("A disposition batch may not fabricate links or clear pending reviews")
        if item.get("human_verified") is not False:
            raise PipelineError("Human verification cannot be implied")
        if not item.get("reviewed_by") or not isinstance(item["reviewed_by"], str):
            raise PipelineError("No-link/ambiguity decisions need editorial attribution")
        if len(str(item.get("editorial_reason", "")).strip()) < 50:
            raise PipelineError("No-link/ambiguity decisions need detailed mathematical rationale")
        if (item.get("source_text_digest") != digest(forms[fid][1]["text"]) and
                item.get("source_text") != forms[fid][1]["text"]):
            raise PipelineError("Disposition based on stale or wrong formulation")
        prior = existing[fid]
        if prior["decision"] not in ("needs_review", item["decision"]):
            raise PipelineError("Cannot silently replace a prior screened disposition")
        if prior["relation_ids"]:
            raise PipelineError("Cannot discard existing links via no-link disposition")
        if prior["decision"] != "needs_review" and (
                prior["editorial_reason"] != item["editorial_reason"] or
                prior["reviewed_by"] != item["reviewed_by"]):
            raise PipelineError("Conflicting disposition revision requires audited next wave")
        prior["decision"] = item["decision"]
        prior["editorial_reason"] = item["editorial_reason"]
        prior["reviewed_by"] = item["reviewed_by"]
    atomic_jsonl(ledger, [existing[k] for k in sorted(existing)])
    report = audit(workspace)
    w.checkpoint("relations", {"sealed": False,
                               "reviewed_formulations": report["reviewed"],
                               "formulations": report["formulations"],
                               "links": report["screened_relations"],
                               "next": "Review all pending formulations before sealing"})
    return report

def audit(workspace, require_complete=False):
    w = Workspace(workspace)
    meanings, forms = inventory(w)
    path = w.root / REVIEW_PATH
    if not path.exists():
        raise PipelineError("No Stage 5 formulation-level ledger")
    entries = jsonl(path)
    if len(entries) != len(forms):
        raise PipelineError("Stage 5 missing formulation reviews: %s of %s" %
                            (len(entries), len(forms)))
    relations = w.records("relations")
    by_id = {}
    tally = Counter()
    accounted_relations = set()
    for row in entries:
        fid = row.get("formulation_id")
        if fid not in forms or fid in by_id:
            raise PipelineError("Unknown or duplicate Stage 5 formulation review")
        by_id[fid] = row
        meaning = forms[fid][0]
        if row.get("meaning_id") != meaning["id"]:
            raise PipelineError("Stage 5 review attached to wrong meaning")
        if row.get("meaning_catalog_digest") != w.state("meanings")["record_digest"]:
            raise PipelineError("Stale Stage 5 review against meaning registry")
        if row.get("human_verified") is not False:
            raise PipelineError("No automatic human verification claims")
        decision = row.get("decision")
        if decision not in DECISIONS:
            raise PipelineError("Unsupported Stage 5 decision")
        ids = row.get("relation_ids")
        if not isinstance(ids, list) or len(ids) != len(set(ids)):
            raise PipelineError("Relation IDs must be a unique list")
        if decision == "needs_review":
            if ids or row.get("reviewed_by"):
                raise PipelineError("Pending item contains editorial claims")
        else:
            if not isinstance(row.get("reviewed_by"), str) or not row["reviewed_by"]:
                raise PipelineError("Terminal Stage 5 disposition needs an editor")
            if len(row.get("editorial_reason", "").strip()) < 50:
                raise PipelineError("Terminal Stage 5 disposition lacks substantive explanation")
            if decision == "linked" and not ids:
                raise PipelineError("Linked decision has no supported relation")
            if decision != "linked" and ids:
                raise PipelineError("Held/no-link decision cannot cite published relations")
        for rid in ids:
            rel = relations.get(rid)
            if not rel or rel["from_formulation"] != fid or rel["review_state"] != "screened":
                raise PipelineError("Stage 5 review points at missing/unscreened relation")
            validate_screened_edge(rel, meanings, forms, w)
            if rel["target_meaning"] == meaning["id"]:
                raise PipelineError("Unwanted recursive self dependency")
            accounted_relations.add(rid)
        tally[decision] += 1
    if set(by_id) != set(forms):
        raise PipelineError("Stage 5 did not account for every formulation")
    unreviewed_relations = set(relations) - accounted_relations
    if unreviewed_relations:
        raise PipelineError("Relations have no matching editorial review: " +
                            str(sorted(unreviewed_relations)[:5]))
    if require_complete and tally["needs_review"]:
        raise PipelineError("Stage 5 cannot seal: %s of %s formulations not reviewed" %
                            (tally["needs_review"], len(forms)))
    return {"formulations": len(forms), "meanings": len(meanings),
            "reviewed": len(forms) - tally["needs_review"],
            "needs_review": tally["needs_review"],
            "decisions": dict(tally),
            "screened_relations": len(relations),
            "complete": tally["needs_review"] == 0,
            "human_verified": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("--prepare", action="store_true")
    operation.add_argument("--apply-batch", type=Path)
    operation.add_argument("--apply-dispositions", type=Path)
    operation.add_argument("--audit", action="store_true")
    operation.add_argument("--seal", action="store_true")
    args = parser.parse_args(argv)
    if args.prepare:
        result = prepare(args.workspace)
    elif args.apply_batch:
        result = apply_batch(args.workspace, args.apply_batch)
    elif args.apply_dispositions:
        result = apply_dispositions(args.workspace, args.apply_dispositions)
    elif args.seal:
        result = audit(args.workspace, require_complete=True)
        Workspace(args.workspace).seal("relations")
        result["sealed"] = True
        atomic_json(args.workspace / "state/stage5_review.json", result)
    else:
        result = audit(args.workspace)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
