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


def _validate_meaning_catalog_review_bridge(meanings: dict, reviews: list, workspace: Path) -> dict:
    """Recognize one explicitly approved, text-only source revision without
    rewriting old individual review evidence as though it were reviewed anew.

    Fail closed if any other mathematical meaning content changes. The
    predecessor catalog is reconstructed by reversing only the recorded text
    edit; its digest MUST exactly match all historical review anchors.
    """
    historical_digests = {r.get("meaning_catalog_digest") for r in reviews}
    if len(historical_digests) != 1 or None in historical_digests:
        raise ResumeError("Individual meaning reviews lack one coherent catalog anchor")
    previous_digest = next(iter(historical_digests))
    current_digest = digest(list(meanings.values()))
    event_path = workspace / "events" / "meaning_text_revision_attestations.jsonl"
    events = jsonl(event_path) if event_path.is_file() else []
    if current_digest == previous_digest:
        if events:
            raise ResumeError("Unexpected source revision event for unchanged reviewed catalog")
        return {"historical_catalog_digest_matched": True, "authorized_text_revisions": 0}
    if len(events) != 1:
        raise ResumeError("Changed meaning catalog requires exactly one reviewed, source-only bridge")
    event = events[0]
    expected = {
        "schema_version": 1,
        "event_id": "wave2.fip-compactness-nonempty-family.2026-10-24",
        "stage": "meanings",
        "meaning_id": "meaning.wave2.broad67.compact-topological-space",
        "formulation_id": "form.wave2.broad67.compact-closed-fip",
        "before_text": (
            "Equivalently, X is compact if every family of closed subsets of X "
            "that has the finite intersection property has nonempty total intersection."
        ),
        "after_text": (
            "Equivalently, X is compact if every nonempty family of closed subsets "
            "of X that has the finite intersection property has nonempty total intersection."
        ),
    }
    if any(event.get(key) != value for key, value in expected.items()):
        raise ResumeError("Attested source correction does not match approved FIP edit")
    if event.get("prior_reviewed_meaning_catalog_digest") != previous_digest:
        raise ResumeError("Source correction is not anchored to the original reviews")
    if (len(str(event.get("reason", "")).strip()) < 40 or
            not str(event.get("reviewed_by", "")).strip() or
            not str(event.get("authorization", "")).startswith("User explicitly approved")):
        raise ResumeError("Source revision lacks substantive review and approval scope")
    old_catalog = []
    replacement_count = 0
    for mid, live in meanings.items():
        if mid != expected["meaning_id"]:
            old_catalog.append(live)
            continue
        restored = dict(live)
        restored_forms = []
        for form in live["formulations"]:
            if form["id"] == expected["formulation_id"]:
                if form["text"] != expected["after_text"]:
                    raise ResumeError("Current FIP wording differs from reviewed revision")
                restored_forms.append({**form, "text": expected["before_text"]})
                replacement_count += 1
            else:
                restored_forms.append(form)
        restored["formulations"] = restored_forms
        old_catalog.append(restored)
    if replacement_count != 1 or digest(old_catalog) != previous_digest:
        raise ResumeError("Unreviewed mathematical source changes beyond approved FIP correction")
    return {
        "historical_catalog_digest_matched_after_exact_reversal": True,
        "authorized_text_revisions": 1,
        "revised_formulation": expected["formulation_id"],
        "original_individual_reviews_preserved": True,
        "external_source_certification": False,
    }




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
    if any(r["meaning_id"] != forms[r["formulation_id"]] for r in reviews):
        raise ResumeError("Stale formulation to meaning assignment")
    catalog_review = _validate_meaning_catalog_review_bridge(meanings, reviews, current.root)
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
        "review_catalog_version_evidence": catalog_review,
        "screened_relationships": counts["relations"],
        "review_dispositions": dict(sorted(Counter(r["decision"] for r in reviews).items())),
        "original_priority_firstpass_records": len(firstpass),
        "original_priorities_are_not_exhaustive_coverage": True,
        "dependency_graph_has_cycles": False,
        "human_peer_verified": False,
    }
