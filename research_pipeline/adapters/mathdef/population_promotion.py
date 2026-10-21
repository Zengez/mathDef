"""mathDef reconciliation promotion: preflight, manifest, explicit guarded apply.

Not a mathematical proof. Never draws from the production mathDef corpus.
This moves source-reviewed independent provisional records to the independently
screened Wave 2 registry only after separately recorded review decisions.
Normal population never calls this entry point.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from research_pipeline.engine.core import Workspace, PipelineError, canonical, digest as catalog_digest, jsonl, atomic_json
from research_pipeline.engine.population import audit, snapshot, digest, write_atomic
from research_pipeline.engine.wave2_apply_links import check_cycles


STAGES = ("sources", "terms", "observations", "meanings", "relations")


def prepare(workspace):
    w = Workspace(workspace)
    conf = w.config()
    if not conf.get("independent_second_wave"):
        raise PipelineError("Promotion requires the independent editable Wave 2 workspace")
    if any(w.state(stage).get("sealed") for stage in STAGES):
        raise PipelineError("Cannot promote to a sealed independent wave")
    old = {stage: w.records(stage) for stage in STAGES}
    draft, revisions = snapshot(w.root)
    if not draft["meanings"]:
        raise PipelineError("No provisional meanings to promote")
    findings = audit(w.root)["findings"]
    # Missing source evidence and pending reviews are blocking conditions.
    if findings:
        raise PipelineError("Unresolved reconciliation findings: " +
                            json.dumps(Counter(f["kind"] for f in findings), sort_keys=True))
    for stage in STAGES:
        duplicates = set(old[stage]).intersection(draft[stage])
        if duplicates:
            raise PipelineError("Unreviewed collision with screened " + stage +
                                ": " + next(iter(duplicates)))
    sources = {**old["sources"], **draft["sources"]}
    terms = {**old["terms"], **draft["terms"]}
    obs = {**old["observations"], **draft["observations"]}
    meanings = {**old["meanings"], **draft["meanings"]}
    forms = {}
    for m in meanings.values():
        for f in m["formulations"]:
            if f["id"] in forms:
                raise PipelineError("Duplicate formulation ID")
            forms[f["id"]] = (m, f)
    form_reviews = defaultdict(list)
    for r in draft["reviews"].values():
        form_reviews[r.get("formulation_id")].append(r)
    incoming = {key: [] for key in STAGES}
    for stage in ("sources", "terms", "observations"):
        incoming[stage] = list(draft[stage].values())
    for item in draft["observations"].values():
        source = sources.get(item.get("source_id"))
        term = terms.get(item.get("term_id"))
        if (source is None or term is None or term["source_id"] != item["source_id"]
                or source.get("authority_reviewed") is not True
                or source.get("rights") not in ("permitted", "locator_only")
                or source.get("access") != "free"
                or not item.get("locator")):
            raise PipelineError("Unverified observation provenance: " + item.get("id", "?"))
    links = {**old["relations"], **draft["relations"]}
    check_cycles(meanings, links)
    new_reviews = []
    for m in draft["meanings"].values():
        new_forms = []
        for f in m["formulations"]:
            if f.get("review_state") not in ("candidate", "screened"):
                raise PipelineError("Held formulation cannot be promoted: " + f["id"])
            reviews = [r for r in form_reviews.get(f["id"], [])
                       if r.get("formulation_sha256") ==
                          digest({"formulation": f, "context": m["context"]})
                       and r.get("status") == "screened"]
            if len(reviews) != 1:
                raise PipelineError("Exactly one current mathematical screen required: " + f["id"])
            r = reviews[0]
            if not r.get("reviewed_by") or len(r.get("reason", "")) < 30:
                raise PipelineError("Mathematical review needs attributable rationale")
            for eid in f.get("evidence_ids", []):
                if eid not in obs or obs[eid].get("term_id") not in m["term_ids"]:
                    raise PipelineError("Unverified formulation source observation: " + f["id"])
            related = [x["id"] for x in draft["relations"].values()
                       if x.get("from_formulation") == f["id"]]
            if not related and r.get("dependency_disposition") != "no_supported_target":
                raise PipelineError("No prerequisite links; explicitly justify no-supported-target: " + f["id"])
            new_forms.append({**f, "review_state": "screened", "human_verified": False,
                              "mathematical_review_reason": r["reason"]})
            new_reviews.append({"formulation_id": f["id"], "meaning_id": m["id"],
                                "decision": "linked" if related else "no_supported_target",
                                "relation_ids": sorted(related),
                                "reviewed_by": r["reviewed_by"],
                                "editorial_reason": r["reason"],
                                "source": "approved_independent_population_reconciliation",
                                "original_wave1_disposition": None, "human_verified": False})
        incoming["meanings"].append({**m, "formulations": new_forms,
                                    "editorial_status": "individually_reconciled",
                                    "human_verified": False})
    # A link is not promotable merely because a candidate target exists.
    for edge in draft["relations"].values():
        src = forms.get(edge.get("from_formulation"))
        target = meanings.get(edge.get("target_meaning"))
        if (edge.get("review_state") != "screened" or not edge.get("reviewed_by")
                or len(edge.get("editorial_reason", "")) < 80
                or edge.get("relation_type") != "definition_uses"
                or src is None or target is None):
            raise PipelineError("Incomplete individualized prerequisite screen: " + edge["id"])
        cited = {obs[eid]["locator"] for eid in src[1]["evidence_ids"]}
        cited_target = {obs[eid]["locator"] for f in target["formulations"]
                        for eid in f.get("evidence_ids", [])}
        if (edge.get("source_locator") not in cited
                or edge.get("target_locator") not in cited_target
                or not edge.get("source_phrase")):
            raise PipelineError("Link lacks checked source-form and target provenance: " + edge["id"])
        incoming["relations"].append(edge)
    provisional_digest = digest({stage: draft[stage] for stage in (*STAGES, "reviews", "issues")})
    previous = jsonl(w.root / "state/wave2_formulation_reviews.jsonl")
    previous_forms = {f["id"]:m["id"] for m in old["meanings"].values()
                      for f in m["formulations"]}
    if (len(previous) != len(previous_forms) or
            {r["formulation_id"] for r in previous} != set(previous_forms)):
        raise PipelineError("Historical individually screened review ledger incomplete")
    historical_links = {rid for r in previous for rid in r["relation_ids"]}
    if historical_links != set(old["relations"]):
        raise PipelineError("Historical source-reviewed links cannot be silently changed")
    current_digest = catalog_digest(list(old["meanings"].values()))
    if any(r.get("meaning_catalog_digest") != current_digest for r in previous):
        raise PipelineError("Historical formulation review references stale catalog")
    report = {
        "schema_version": 1,
        "independent_workspace": str(w.root),
        "draft_digest": provisional_digest,
        "preexisting_catalog_digest": current_digest,
        "preexisting_review_digest": digest(previous),
        "preexisting_counts": {stage: len(old[stage]) for stage in STAGES},
        "incoming_counts": {stage: len(incoming[stage]) for stage in STAGES},
        "new_review_count": len(new_reviews),
        "versioned_revision_events": len(revisions),
        "reviewed_math_not_human_peer_verified": True,
        "certification_and_freeze_outstanding": True,
        "no_production_mathdef_data_consulted": True,
    }
    return report, incoming, previous, new_reviews


def run(workspace, approval_path=None, apply=False):
    report, incoming, previous, new_reviews = prepare(workspace)
    w = Workspace(workspace)
    if not apply:
        return {"promotion_ready": True, **report}
    if approval_path is None:
        raise PipelineError("Explicit approval manifest required for promotion")
    approval = json.loads(Path(approval_path).read_text(encoding="utf-8"))
    if (approval.get("approved_for_independent_promotion") is not True
            or approval.get("draft_digest") != report["draft_digest"]
            or approval.get("preexisting_catalog_digest") != report["preexisting_catalog_digest"]
            or approval.get("preexisting_review_digest") != report["preexisting_review_digest"]
            or not approval.get("reviewer") or len(approval.get("rationale", "")) < 60):
        raise PipelineError("Promotion approval invalid, missing or stale")
    if not Path(approval_path).resolve().is_relative_to((w.root / "population").resolve()):
        raise PipelineError("Approval record must stay within independent population ledger")
    # Revalidate all incoming records before any change to existing reviewed data.
    original = w.root / "population" / "PROMOTION_PRECHECK.json"
    atomic_json(original, report)
    for stage in STAGES:
        if incoming[stage]:
            intake = w.root / "population" / "promotion_intake" / (stage + ".jsonl")
            write_atomic(intake, "".join(canonical(row) + "\n" for row in incoming[stage]))
            w.ingest(stage, intake, batch_size=max(1, len(incoming[stage])))
    meanings = w.records("meanings")
    updated_digest = catalog_digest(list(meanings.values()))
    reviewed = [dict(row, meaning_catalog_digest=updated_digest) for row in previous]
    reviewed.extend(dict(row, meaning_catalog_digest=updated_digest) for row in new_reviews)
    reviewed.sort(key=lambda r: r["formulation_id"])
    led = w.root / "state/wave2_formulation_reviews.jsonl"
    archive = w.root / "population" / "promotion_history" / "previous_reviews.jsonl"
    write_atomic(archive, "".join(canonical(row) + "\n" for row in previous))
    write_atomic(led, "".join(canonical(row) + "\n" for row in reviewed))
    check_cycles(meanings, w.records("relations"))
    result = {"status": "promoted_into_independent_unsealed_wave2",
              **report, "new_catalog_digest": updated_digest,
              "new_review_count": len(reviewed), "human_peer_verified": False}
    atomic_json(w.root / "population" / "PROMOTION_RESULT.json", result)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--approval", type=Path)
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    print(json.dumps(run(args.workspace, args.approval, args.apply),
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
