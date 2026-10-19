"""Record individual no-supported-target decisions for the three remaining new Wave 2 foundations.

This does not seal relationship research or assert that missing general prerequisites
are unimportant: it records why none is available *in the screened independent corpus*.
Original Wave 1 dispositions and every existing relation remain untouched.
"""
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path
from .core import Workspace, PipelineError, canonical, digest, jsonl, atomic_json
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import locator, check_cycles

EXPECTED={
    "form.wave2.foundation.group",
    "form.wave2.foundation.small-category",
    "form.wave2.foundation.topological-space",
}

def run(root: Path, batch: Path) -> dict:
    w=Workspace(root)
    if len(w.records("relations"))!=481 or len(w.records("meanings"))!=428:
        raise PipelineError("Expected screened Wave 2 links batch 02; refuse stale review")
    if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
        raise PipelineError("Do not modify sealed Wave 2 workspace")
    meanings=w.records("meanings")
    observations=w.records("observations")
    forms={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
    if len(forms)!=440:
        raise PipelineError("Meaning/formulation count changed")
    decisions=jsonl(batch)
    if len(decisions)!=3 or {x.get("formulation_id") for x in decisions}!=EXPECTED:
        raise PipelineError("Exactly three independently reviewed new foundations are required")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    reviews=jsonl(ledger)
    byid={x["formulation_id"]:x for x in reviews}
    if len(reviews)!=440 or len(byid)!=440 or set(byid)!=set(forms):
        raise PipelineError("Incomplete/duplicate Wave 2 formulation reviews")
    if any(x.get("meaning_catalog_digest")!=digest(list(meanings.values())) for x in reviews):
        raise PipelineError("Stale review meaning catalog digest")
    before={x["formulation_id"]:canonical(x) for x in reviews if x["formulation_id"] not in EXPECTED}
    events=[]
    for decision in decisions:
        fid=decision["formulation_id"]
        m,f=forms[fid]
        r=byid[fid]
        if f.get("review_state")!="screened":
            raise PipelineError("Unscreened foundation "+fid)
        if decision.get("decision")!="no_supported_target":
            raise PipelineError("Invalid target decision "+fid)
        if decision.get("human_verified") is not False:
            raise PipelineError("Peer verification cannot be inferred")
        if decision.get("source_locator")!=locator(m,observations):
            raise PipelineError("Missing or mismatched exact source locator "+fid)
        if len(decision.get("mathematical_reason",""))<130 or len(decision.get("missing_candidates",[]))<2:
            raise PipelineError("Insufficient individual mathematical rationale "+fid)
        if r.get("original_wave1_disposition") is not None or r.get("relation_ids")!=[]:
            raise PipelineError("Attempt to change inherited or linked review "+fid)
        if r["decision"] not in ("needs_review","no_supported_target"):
            raise PipelineError("Unexpected pre-review disposition "+fid)
        orig=r.get("original_wave2_pending_reason",r["editorial_reason"])
        events.append({
            "event_id":"wave2.foundation.no_target."+fid,
            "formulation_id":fid,
            "original_wave2_disposition":"needs_review",
            "original_wave2_pending_reason":orig,
            "new_disposition":"no_supported_target",
            "mathematical_reason":decision["mathematical_reason"],
            "missing_candidates":decision["missing_candidates"],
            "source_locator":decision["source_locator"],
            "reviewed_by":decision["reviewed_by"],
            "human_verified":False,
        })
        r["original_wave2_pending_reason"]=orig
        r["decision"]="no_supported_target"
        r["editorial_reason"]=decision["mathematical_reason"]
        r["source"]="wave2_individual_mathematical_no_supported_target_review"
        r["reviewed_by"]=decision["reviewed_by"]
    if any(canonical(byid[k])!=v for k,v in before.items()):
        raise PipelineError("Attempt to rewrite earlier review dispositions")
    event_path=w.root/"events/wave2_foundation_no_target_decisions_batch01.jsonl"
    payload="".join(canonical(x)+"\n" for x in sorted(events,key=lambda e:e["formulation_id"]))
    if event_path.exists() and event_path.read_text(encoding="utf-8")!=payload:
        raise PipelineError("Existing evidence events differ")
    event_path.write_text(payload,encoding="utf-8")
    actual_relations=w.records("relations")
    if {i for row in byid.values() for i in row["relation_ids"]}!=set(actual_relations):
        raise PipelineError("A screened relationship lost its individual review")
    check_cycles(meanings,actual_relations)
    atomic_jsonl(ledger,[byid[k] for k in sorted(byid)])
    counts=dict(Counter(x["decision"] for x in byid.values()))
    assert counts.get("needs_review",0)==0
    report={
        "phase":"all_nine_new_wave2_formulations_have_individual_dependency_review_decisions",
        "new_foundations_reviewed_as_no_supported_target":3,
        "all_wave2_formulations":440,
        "screened_wave2_relations":481,
        "remaining_new_formulations_needing_review":0,
        "current_dispositions":counts,
        "historical_wave1_decisions_preserved":True,
        "stage5_wave2_sealed":False,
        "remaining_historical_ambiguities_need_source_research":counts.get("held_ambiguity",0),
        "human_peer_verified":False,
        "original_production_corpus_consulted":False,
        "next":"Continue independent source acquisitions, eight held EoM locators, two held ambiguities and explicitly uncovered foundational meanings; do not seal any stage."
    }
    atomic_json(w.root/"state/wave2_foundation_dependency_reviews_complete.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,required=True)
    p.add_argument("--batch",type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(run(a.workspace,a.batch),indent=2))
if __name__=="__main__":
    main()
