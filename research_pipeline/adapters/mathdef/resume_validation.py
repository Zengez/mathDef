"""mathDef-specific policy plugin for the generic research checkpoint engine.

Only the *independent reconstruction experiment* is consulted. The original
production mathDef corpus, definitions and citations are never read here.
An educational-terminology or theorem repository may use a different plugin.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from research_pipeline.engine.core import Workspace, digest, jsonl
from research_pipeline.engine.resume_checkpoint import ResumeError, inside
from research_pipeline.engine.wave2_apply_links import check_cycles


def inspect(repo: Path, config: dict) -> dict:
    domain = config["domain"]
    original = Workspace(inside(repo, domain["frozen_workspace"]))
    current = Workspace(inside(repo, domain["editable_workspace"]))
    frozen_marker = original.root / "state" / "wave1_freeze.json"
    baseline_marker = current.root / "state" / "baseline.json"
    frozen = json.loads(frozen_marker.read_text(encoding="utf-8"))
    baseline = json.loads(baseline_marker.read_text(encoding="utf-8"))
    expected = domain["expected_frozen_publication_digest"]
    if (frozen["state"] != "FROZEN" or
            frozen["published_catalog_digest"] != expected or
            baseline["first_wave_digest"] != expected or
            baseline.get("mode") != "second_wave"):
        raise ResumeError("Frozen independent lineage attestation mismatch")
    if digest(original.publication()) != expected:
        raise ResumeError("Frozen independent Wave 1 publication digest changed")
    stages = ("sources", "terms", "observations", "meanings", "relations")
    counts = {}
    for stage in stages:
        if current.state(stage).get("sealed"):
            raise ResumeError("Wave 2 stage sealed unexpectedly: " + stage)
        inherited = original.records(stage)
        live = current.records(stage)
        if len(live) < len(inherited):
            raise ResumeError("Missing inherited records in " + stage)
        counts[stage] = len(live)
        # Meanings can have explicitly source-reviewed independent Wave 2
        # revisions. Their histories are versioned separately, so the live
        # meaning payload itself need not match frozen Wave 1 byte-for-byte.
        if stage not in ("meanings",):
            if any(live.get(key) != row for key, row in inherited.items()):
                raise ResumeError("Frozen inherited " + stage + " changed in Wave 2")
        elif any(key not in live for key in inherited):
            raise ResumeError("Frozen meaning IDs missing in Wave 2")
    meanings = current.records("meanings")
    relations = current.records("relations")
    forms = {f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
    if len(forms) != sum(len(m["formulations"]) for m in meanings.values()):
        raise ResumeError("Duplicate formulation IDs")
    if any(f["review_state"] != "screened" for m in meanings.values()
           for f in m["formulations"]):
        raise ResumeError("Unscreened meaning in screened mathematical corpus")
    reviews = jsonl(current.root / "state" / "wave2_formulation_reviews.jsonl")
    reviewed = {r["formulation_id"]:r for r in reviews}
    if len(reviews) != len(forms) or set(reviewed) != set(forms):
        raise ResumeError("Incomplete or repeated individual formulation decisions")
    catalog_digest = digest(list(meanings.values()))
    if any(r["meaning_id"] != forms[r["formulation_id"]] or
           r.get("meaning_catalog_digest") != catalog_digest for r in reviews):
        raise ResumeError("Stale formulation meaning context or catalog digest")
    link_ids = [link for r in reviews for link in r["relation_ids"]]
    if len(set(link_ids)) != len(link_ids) or set(link_ids) != set(relations):
        raise ResumeError("Screened links and review coverage differ")
    if any(r["review_state"] != "screened" for r in relations.values()):
        raise ResumeError("An unscreened relationship was included in totals")
    check_cycles(meanings, relations)
    firstpass_path = current.root / "state" / domain["firstpass_relative_path"]
    firstpass = jsonl(firstpass_path)
    initial = jsonl(current.root / "wave2" / "prioritized_research.jsonl")
    original_ids = [task.get("id") for task in initial]
    firstpass_ids = [record.get("task_id") for record in firstpass]
    if (len(initial) != domain["original_priority_items"] or
            len(firstpass) != len(initial) or
            len(set(original_ids)) != len(original_ids) or
            len(set(firstpass_ids)) != len(firstpass_ids) or
            set(original_ids) != set(firstpass_ids)):
        raise ResumeError("Original priority IDs and first-pass review evidence differ")
    return {
        "independent_frozen_wave1_digest": expected,
        "frozen_wave1_digest_recomputed_and_matched": True,
        "editable_wave2_unsealed": True,
        "production_corpus_used": False,
        "sources": counts["sources"],
        "terms": counts["terms"],
        "source_observations": counts["observations"],
        "screened_contextual_meanings": counts["meanings"],
        "reviewed_formulations": len(reviews),
        "screened_relationships": counts["relations"],
        "review_dispositions": dict(sorted(Counter(r["decision"] for r in reviews).items())),
        "original_priority_firstpass_records": len(firstpass),
        "original_priorities_are_not_exhaustive_coverage": True,
        "dependency_graph_has_cycles": False,
        "human_peer_verified": False,
    }
