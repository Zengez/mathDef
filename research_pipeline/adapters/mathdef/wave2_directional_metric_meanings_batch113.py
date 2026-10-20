"""Batch113 screen six contexts with seven source-backed formulations.

Gradient existence alone is held at observation level and explicitly excluded.
The two homeomorphism descriptions share one mathematical meaning.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/directional_metric_topology_source_audit_batch112_2026-10-20.jsonl"
BASE={"sources":14,"terms":453,"observations":906,"meanings":558,"relations":784}
AFTER=dict(BASE,meanings=564)
SPECS=(
 ("open-ball",0,"open-metric","Open ball in a metric space with positive radius"),
 ("open-ball",1,"open-norm","Open ball in a normed vector space with positive radius"),
 ("closed-ball",0,"closed-metric","Closed ball in a metric space with positive radius"),
 ("closed-ball",1,"closed-norm","Closed ball in a normed vector space with positive radius"),
 ("homeomorphism",0,"homeomorphism-topological","Homeomorphism of arbitrary topological spaces"),
 ("directional-derivative",0,"directional-differentiable","Directional derivative of a differentiable function in Euclidean space")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    data="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=data:
        raise PipelineError("Historical individual screened mathematical source record altered")
    path.write_text(data,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Independent unsealed Wave 2 required")
    now={k:len(w.records(k)) for k in BASE}
    if now not in (BASE,AFTER):
        raise PipelineError("Unexpected source-screened mathematical inventory "+str(now))
    source_report=json.loads((w.root/"state/wave2_directional112_source_intake.json").read_text())
    if source_report.get("new_source_observations")!=8 or source_report.get("held_gradient_claims")!=1 or not source_report.get("gradient_exists_not_sufficient_for_directional_formula"):
        raise PipelineError("Batch112 source-only held audit not verified")
    held=jsonl(w.root/"wave2/directional112_quarantined_source_claims.jsonl")
    if len(held)!=1 or held[0]["observation_id"]!="obs.wave2.directional112.directional-derivative.02":
        raise PipelineError("Gradient claim quarantine absent or changed")
    dossier={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if len(dossier)!=4:
        raise PipelineError("Four prior approved source topics required")
    termdb=w.records("terms");observations=w.records("observations")
    meanings=[];individual=[]
    for key,cidx,suffix,context_name in SPECS:
        r=dossier[key]
        tid="term.wave2.directional112."+key
        if tid not in termdb or r["source"]!=termdb[tid]["locator"] or r["production_corpus_consulted"]:
            raise PipelineError("Source lineage invalid "+key)
        context=r["contexts"][cidx]
        if context.get("held"):raise PipelineError("Held gradient-only source must not be promoted")
        reason=r["review"]
        if len(reason)<300:raise PipelineError("Lack of source-specific mathematical rationale")
        if key=="homeomorphism":
            if len(context["forms"])!=2 or "inverse map" not in context["forms"][0]["text"] or "exactly when" not in context["forms"][1]["text"]:
                raise PipelineError("Homeomorphism equivalence source forms not evidenced")
            reason+=" Both equivalent topological definitions share one mathematical meaning; no Hausdorff property is added."
        elif key=="directional-derivative":
            if len(context["forms"])!=1 or "differentiable at a" not in context["forms"][0]["text"]:
                raise PipelineError("Differentiability assumption missing from accepted directional form")
            reason+=" Only source Definition 2 with total differentiability is admitted, and the suspect gradient-only observation is source-preserved but not a screened meaning."
        else:
            if len(context["forms"])!=1:
                raise PipelineError("Ball context must be individually source-backed")
            formtext=context["forms"][0]["text"]
            if ("closed" in key and "≤r" not in formtext) or ("open" in key and "<r" not in formtext):
                raise PipelineError("Strict/non-strict ball-radius inequality not preserved")
            reason+=" Positive radius is required. A closed metric ball need not equal closure of the corresponding open ball."
        mid="meaning.wave2.directional113."+suffix
        forms=[]
        for i,form in enumerate(context["forms"],start=1):
            obs_index=(i if key=="homeomorphism" else cidx+1)
            oid=f"obs.wave2.directional112.{key}.{obs_index:02d}"
            o=observations.get(oid)
            if not o or o["term_id"]!=tid or o["locator"]!=r["source"] or o["text"]!=form["text"]:
                raise PipelineError("Exact mathematical source observation unavailable "+suffix)
            if oid==held[0]["observation_id"]:
                raise PipelineError("Held gradient source incorrectly admitted")
            fid="form.wave2.directional113."+suffix+("."+str(i) if len(context["forms"])>1 else "")
            forms.append({"id":fid,"text":form["text"],"evidence_ids":[oid],
              "review_state":"screened","human_verified":False,
              "mathematical_review_reason":reason,
              "source_screened_by":"assistant_independent_directional_metric_math_screen_2026_10_20"})
            individual.append({"review_id":"review.wave2.directional113."+suffix+("."+str(i) if len(context["forms"])>1 else ""),
              "meaning_id":mid,"formulation_id":fid,"source_observation_id":oid,
              "source_locator":r["source"],"mathematical_reason":reason,
              "decision":"mathematically_screened_pending_individual_dependency_review",
              "human_verified":False,"production_corpus_used":False})
        meanings.append({"id":mid,"term_group_id":"wave2.directional113."+key,
          "display_term":r["term"],"context":context_name,
          "term_ids":[tid],"formulations":forms,
          "editorial_status":"source_scoped_individually_mathematically_screened",
          "editorial_screening_reason":reason,"human_verified":False})
    if len(meanings)!=6 or len(individual)!=7:
        raise PipelineError("Six contexts and seven source formulations expected")
    if any(r["source_observation_id"]==held[0]["observation_id"] for r in individual):
        raise PipelineError("Unsafe directional gradient source was promoted")
    store(w.root/"wave2/directional113_individual_mathematical_reviews.jsonl",individual)
    intake=store(w.root/"intake/directional113_meanings.jsonl",meanings)
    current=w.records("meanings")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    previous=jsonl(ledger)
    if len(previous) not in (587,594) or len({r["formulation_id"] for r in previous})!=len(previous):
        raise PipelineError("587 historical individually dispositioned forms required")
    if {i for r in previous for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Prior 784 links not individually covered")
    snapshot=w.root/"state/wave2_formulation_reviews_snapshot_587_before_directional113.jsonl"
    if len(current)==558:
        if len(previous)!=587 or any(r["meaning_catalog_digest"]!=digest(list(current.values())) for r in previous):
            raise PipelineError("Prior meaning digest mismatch")
        old=ledger.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=old:
            raise PipelineError("Historical 587 review snapshot differs")
        snapshot.write_text(old,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_587_before_directional113.json",{
           "rows":587,"old_links":784,"sha256":hashlib.sha256(old.encode("utf-8")).hexdigest(),
           "human_peer_verified":False})
        w.ingest("meanings",intake,batch_size=6)
    ms=w.records("meanings")
    if len(ms)!=564 or any(ms.get(m["id"])!=m for m in meanings):
        raise PipelineError("Independently screened meaning records missing")
    historical=jsonl(snapshot)
    if len(historical)!=587 or len({r["formulation_id"] for r in historical})!=587:
        raise PipelineError("Historical individual review snapshot absent")
    d=digest(list(ms.values()))
    expected=[dict(r,meaning_catalog_digest=d) for r in historical]
    for r in individual:
        expected.append({"formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
          "meaning_catalog_digest":d,"decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,"source":"independent_directional_metric_math_screen_batch113",
          "editorial_reason":"Source-specific mathematical statement screened, individual dependencies await separate review.",
          "reviewed_by":None,"human_verified":False})
    if len(previous)==594:
        if {r["formulation_id"]:r for r in previous}!={r["formulation_id"]:r for r in expected}:
            raise PipelineError("Already completed math screen changed on rerun")
    else:
        atomic_jsonl(ledger,sorted(expected,key=lambda r:r["formulation_id"]))
    actual=jsonl(ledger);idx={r["formulation_id"]:r for r in actual}
    if len(actual)!=594 or len(idx)!=594:
        raise PipelineError("594 individual formulation reviews required")
    for old in historical:
        current_review=idx[old["formulation_id"]]
        if any(current_review.get(k)!=v for k,v in old.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Unrelated historical review altered")
    if dict(Counter(r["decision"] for r in actual))!={"linked":581,"no_supported_target":6,"needs_review":7}:
        raise PipelineError("Unexpected 7 newly screened versus historical disposition")
    check_cycles(ms,w.records("relations"))
    state=w.state("meanings")
    state.update(total=564,record_digest=d,screened_new_formulations=163,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={"batch":113,"screened_meanings":564,"reviewed_formulations":594,
      "new_contextual_meanings":6,"new_individual_formulations":7,
      "historical_587_formulation_reviews_preserved":True,
      "historical_784_links_preserved":True,
      "held_gradient_claim_remains_excluded":True,
      "homeomorphism_equivalent_forms_one_meaning":True,
      "closed_metric_ball_not_assumed_open_ball_closure":True,
      "all_seven_new_forms_pending_link_review":True,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch114: individually source-screen seven new ball/homeomorphism/directional formulations against existing metric, normed vector, topological and continuity concepts."}
    atomic_json(w.root/"state/wave2_directional113_meaning_screen.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
