"""Batch 98: independently screen metric and functional-analysis meanings.

Keep source-specific mathematical conventions; do not consult production mathDef.
The metric-topology presentation explicitly fixes the induced topology.
"""
from __future__ import annotations
import argparse, hashlib, json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace, PipelineError, jsonl, canonical, digest, atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/functional_analysis_metric_source_audit_batch96_2026-10-20.jsonl"
BEFORE={"sources":14,"terms":432,"observations":872,"meanings":530,"relations":735}
AFTER=dict(BEFORE,meanings=536)
SPECS=(
 ("metric-space",0,"metric-space","Nonempty metric space, canonical metric topology","metric-space"),
 ("norm-on-vector-space",0,"norm-over-normed-division-ring","Vector norm over a normed division ring","norm-on-vector-space"),
 ("norm-on-vector-space",1,"norm-over-real-or-complex","Vector norm over the real or complex field","norm-on-vector-space"),
 ("normed-vector-space",0,"normed-vector-space","Vector space over a normed division ring equipped with a norm","normed-vector-space"),
 ("inner-product-space",0,"real-inner-product-space","Positive-definite symmetric bilinear real inner-product space","inner-product-space"),
 ("inner-product-space",1,"complex-inner-product-space","Positive-definite Hermitian complex inner-product space, first argument linear","inner-product-space"),
)
METRIC_COMPATIBLE=(
 "For a nonempty set X with a metric d, the balls B_d(x,r)={y in X:d(x,y)<r}, "
 "r>0, generate a canonical topology τ_d. The metric-space data (X,d) determine "
 "the compatible triple (X,τ_d,d), and conversely a triple (X,τ,d) with τ=τ_d "
 "determines (X,d). A metrizable topology alone does not specify a unique metric."
)

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Individual batch98 mathematical review changed")
    path.write_text(body,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Requires independent unsealed Wave 2")
    current={s:len(w.records(s)) for s in BEFORE}
    if current not in (BEFORE, AFTER):
        raise PipelineError("Source and screened-meaning count mismatch "+str(current))
    research={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if len(research)!=4 or any(r["stage_ingested"] or r["production_corpus_consulted"] for r in research.values()):
        raise PipelineError("Unreviewed or production-derived source dossier")
    terms=w.records("terms");obs=w.records("observations")
    records=[];indiv=[]
    for key,idx,suffix,context,group_key in SPECS:
        row=research[key]
        termid="term.wave2.analysis97."+key
        if termid not in terms or terms[termid]["locator"]!=row["source"]:
            raise PipelineError("Source term missing "+key)
        candidates=[(c,f) for c in row["contexts"] for f in c["formulations"]]
        if idx>=len(candidates):
            raise PipelineError("Missing variant "+suffix)
        source_context,source_form=candidates[idx]
        obsid=f"obs.wave2.analysis97.{key}.{idx+1:02d}"
        o=obs.get(obsid)
        if (not o or o["term_id"]!=termid or o["locator"]!=row["source"]
            or o["source_id"]!="src.proofwiki" or o["record_kind"]!="paraphrase"
            or o["text"]!=source_form["text"] or len(row["mathematical_review"])<280):
            raise PipelineError("Variant source-specific attribution mismatch "+suffix)
        reason=row["mathematical_review"]
        if key=="metric-space":
            reason+=(" Screening maintains one nonempty metric-space meaning with two conditionally "
                     "equivalent presentations. The compatible topology is necessarily τ_d; "
                     "metrizable does not mean any arbitrarily chosen metric induces a given topology.")
        elif key=="norm-on-vector-space":
            reason+=(" The general scalar normed-division-ring context and the real/complex "
                     "specialization are separately indexed, not equated across all scalar rings.")
        elif key=="inner-product-space":
            reason+=(" Real and complex scalar fields are distinct, with first-argument "
                     "complex linearity fixed as the source convention.")
        text=METRIC_COMPATIBLE if key=="metric-space" and idx==1 else source_form["text"]
        if key=="metric-space" and idx==1 and ("τ=τ_d" not in text or "nonempty" not in text):
            raise PipelineError("Metric topology must be specifically induced")
        form={
          "id":"form.wave2.analysis98."+suffix+(".compatible" if key=="metric-space" and idx==1 else ""),
          "text":text,"evidence_ids":[obsid],
          "review_state":"screened","human_verified":False,
          "mathematical_review_reason":reason,
          "source_screened_by":"assistant_independent_metric_functional_math_screen_2026_10_20"
        }
        if key=="metric-space" and idx==1:
            # This variant belongs to the same mathematical meaning, not a seventh meaning.
            records[0]["formulations"].append(form)
            mid=records[0]["id"]
        else:
            mid="meaning.wave2.analysis98."+suffix
            records.append({
              "id":mid,"term_group_id":"wave2.analysis98."+group_key,
              "display_term":row["term"],"context":context,"term_ids":[termid],
              "formulations":[form],"editorial_status":"source_scoped_individually_mathematically_screened",
              "editorial_screening_reason":reason,"human_verified":False
            })
        indiv.append({
          "review_id":"review.wave2.analysis98."+suffix+(".compatible" if key=="metric-space" and idx==1 else ""),
          "meaning_id":mid,"formulation_id":form["id"],
          "source_observation_id":obsid,"source_locator":row["source"],
          "mathematical_reason":reason,
          "decision":"mathematically_screened_pending_individual_dependency_review",
          "human_verified":False,"production_corpus_used":False
        })
    if len(records)!=6 or len(indiv)!=7 or sorted(len(r["formulations"]) for r in records)!=[1,1,1,1,1,2]:
        raise PipelineError("Expected six meanings and seven source-attributed formulations")
    if records[0]["formulations"][0]["id"]==records[0]["formulations"][1]["id"]:
        raise PipelineError("Distinct metric formulations lost")
    store(w.root/"wave2/analysis98_individual_mathematical_formulation_reviews.jsonl",indiv)
    input_path=store(w.root/"intake/analysis98_meanings.jsonl",records)
    old_mean=w.records("meanings")
    path=w.root/"state/wave2_formulation_reviews.jsonl"
    existing=jsonl(path)
    if len(existing) not in (554,561) or len({x["formulation_id"] for x in existing})!=len(existing):
        raise PipelineError("Historical 554 reviews absent")
    if {rid for r in existing for rid in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Previous relationship reviews incomplete")
    snapshot=w.root/"state/wave2_formulation_reviews_snapshot_554_before_analysis98.jsonl"
    if len(old_mean)==530:
        if len(existing)!=554 or any(x["meaning_catalog_digest"]!=digest(list(old_mean.values())) for x in existing):
            raise PipelineError("Previous meaning digest is not verified")
        orig=path.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=orig:
            raise PipelineError("Historical 554 review snapshot changed")
        snapshot.write_text(orig,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_554_before_analysis98.json",{
            "rows":554,"previous_links":735,
            "sha256":hashlib.sha256(orig.encode("utf-8")).hexdigest(),"human_peer_verified":False})
        w.ingest("meanings",input_path,batch_size=6)
    meanings=w.records("meanings")
    if len(meanings)!=536 or any(meanings.get(x["id"])!=x for x in records):
        raise PipelineError("Individually screened meaning admission incomplete")
    historical=jsonl(snapshot)
    if len(historical)!=554 or len({r["formulation_id"] for r in historical})!=554:
        raise PipelineError("Previous 554 individual decisions lost")
    h=digest(list(meanings.values()))
    proposed=[dict(r,meaning_catalog_digest=h) for r in historical]
    for r in indiv:
        proposed.append({
          "formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
          "meaning_catalog_digest":h,"decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,"source":"independent_metric_functional_math_screen_batch98",
          "editorial_reason":"Individually sourced mathematical meaning screened, prerequisite decision pending.",
          "reviewed_by":None,"human_verified":False
        })
    if len(existing)==561:
        if {r["formulation_id"]:r for r in existing}!={r["formulation_id"]:r for r in proposed}:
            raise PipelineError("Repeat run disagrees with earlier mathematical screening")
    else:
        atomic_jsonl(path,sorted(proposed,key=lambda r:r["formulation_id"]))
    current_reviews=jsonl(path);by={r["formulation_id"]:r for r in current_reviews}
    for prior in historical:
        now=by[prior["formulation_id"]]
        if any(now.get(k)!=v for k,v in prior.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Previously reviewed formulation changed")
    if len(by)!=561 or {i for r in current_reviews for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("New or historical formulation review coverage failed")
    check_cycles(meanings,w.records("relations"))
    counts=dict(Counter(r["decision"] for r in current_reviews))
    if counts!={"linked":548,"no_supported_target":6,"needs_review":7}:
        raise PipelineError("Unexpected full review distribution "+str(counts))
    state=w.state("meanings")
    state.update(total=536,record_digest=h,screened_new_formulations=130,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
      "batch":98,"screened_contextual_meanings":536,"reviewed_formulations":561,
      "new_meanings":6,"new_formulations":7,"prior_554_reviews_preserved":True,
      "prior_735_links_preserved":True,"metric_induced_topology_condition_explicit":True,
      "metric_nonempty_source_convention_preserved":True,
      "normed_division_ring_and_real_complex_norm_scopes_distinct":True,
      "real_complex_inner_product_conventions_distinct":True,
      "needs_individual_link_review":7,"all_stages_unsealed":True,
      "production_corpus_used":False,"human_peer_verified":False,
      "next":"Batch99 individually source-screened metric/norm/inner-product prerequisite links; do not fabricate missing scalar norm or complex-number targets."
    }
    atomic_json(w.root/"state/wave2_analysis98_meaning_screen.json",report)
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(ap.parse_args().workspace),indent=2))
if __name__=="__main__":
    main()
