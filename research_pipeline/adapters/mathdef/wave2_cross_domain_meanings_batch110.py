"""Batch110: six distinct mathematical meanings from seven independent source forms.

Module vs vector linearity and set vs sequence accumulation are context-
specific; the two mapping-image presentations are equivalent in one meaning.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/cross_domain_source_variants_batch109_2026-10-20.jsonl"
BASE={"sources":14,"terms":449,"observations":898,"meanings":552,"relations":774}
AFTER=dict(BASE,meanings=558)
SPECS=(
 ("linear-transformation",0,"module-linear","Left R-module linear transformation"),
 ("linear-transformation",1,"field-vector-linear","Linear transformation of vector spaces over one field"),
 ("image-mapping",0,"image-of-mapping","Set-theoretic full image of a total mapping"),
 ("rank-linear",0,"finite-image-rank","Finite rank of field-vector-space linear transformation"),
 ("accumulation-point",0,"sequence-accumulation","Accumulation point of an indexed topological sequence"),
 ("accumulation-point",1,"set-accumulation","Derived-set accumulation point of a subset in a topological space")
)

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Previously screened individual source/formulation data differs")
    path.write_text(content,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Independent unsealed Wave2 required")
    current={k:len(w.records(k)) for k in BASE}
    if current not in (BASE,AFTER):
        raise PipelineError("Source-only baseline mismatch "+str(current))
    source_report=json.loads((w.root/"state/wave2_cross109_source_intake.json").read_text())
    if (source_report.get("new_source_terms")!=4 or source_report.get("new_source_observations")!=7 or
        source_report.get("new_screened_meanings")!=0 or not source_report.get("rank_finite_image_condition_retained")):
        raise PipelineError("Committed source-specific intake audit missing")
    research={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    terms=w.records("terms");obs=w.records("observations")
    if len(research)!=4:
        raise PipelineError("Four independently screened sources required")
    meanings=[];individual=[]
    for key,cidx,suffix,scope in SPECS:
        r=research[key];tid="term.wave2.cross109."+key
        if tid not in terms or terms[tid]["locator"]!=r["source"] or r["production_corpus_consulted"]:
            raise PipelineError("Source/term citation mismatch "+key)
        ctx=r["contexts"][cidx]
        reason=r["mathematical_review"]
        if len(reason)<320: raise PipelineError("Mathematical rationale insufficient")
        if key=="linear-transformation":
            if cidx==0 and ("R-linear" not in ctx["context"] and "R-module" not in ctx["context"]):
                raise PipelineError("General module linearity not scoped correctly")
            if cidx==1 and "field K" not in ctx["formulations"][0]["text"]:
                raise PipelineError("Field vector-space homomorphism not scoped correctly")
        elif key=="image-mapping":
            if len(ctx["formulations"])!=2 or "f[S]" not in ctx["formulations"][1]["text"]:
                raise PipelineError("Two equivalent mapping-image formulations required")
            reason+=" Both forms share the same source/target object and are equivalent, not two mathematical meanings."
        elif key=="rank-linear":
            if "finite-dimensional" not in ctx["formulations"][0]["text"] or "FINITE-DIMENSIONAL" not in reason:
                raise PipelineError("Finite image condition must remain")
        elif key=="accumulation-point":
            if cidx==0 and ("index set" not in ctx["formulations"][0]["text"] or "infinite" not in ctx["formulations"][0]["text"]):
                raise PipelineError("Sequence accumulation quantifies over indices")
            if cidx==1 and "A\\{x}" not in ctx["formulations"][0]["text"]:
                raise PipelineError("Set accumulation must remove the queried point")
            reason+=" Sequence accumulation by infinitely many indices and derived-set accumulation of a SET remain different conditions."
        mid="meaning.wave2.cross110."+suffix
        group="wave2.cross110."+key
        forms=[]
        for idx,f in enumerate(ctx["formulations"],1):
            obs_index=idx if key=="image-mapping" else cidx+1
            oid=f"obs.wave2.cross109.{key}.{obs_index:02d}"
            o=obs.get(oid)
            if not o or o["term_id"]!=tid or o["locator"]!=r["source"] or o["text"]!=f["text"]:
                raise PipelineError("Source-specific observation mismatch "+suffix+"/"+str(idx))
            fid="form.wave2.cross110."+suffix+("."+str(idx) if len(ctx["formulations"])>1 else "")
            forms.append({"id":fid,"text":f["text"],"evidence_ids":[oid],
                  "review_state":"screened","human_verified":False,
                  "mathematical_review_reason":reason,
                  "source_screened_by":"assistant_independent_linear_image_rank_accumulation_math_screen_2026_10_20"})
            individual.append({
              "review_id":"review.wave2.cross110."+suffix+("."+str(idx) if len(ctx["formulations"])>1 else ""),
              "meaning_id":mid,"formulation_id":fid,"source_observation_id":oid,
              "source_locator":r["source"],"mathematical_reason":reason,
              "decision":"mathematically_screened_pending_link_review",
              "human_verified":False,"production_corpus_used":False})
        meanings.append({"id":mid,"term_group_id":group,"display_term":r["term"],
             "context":scope,"term_ids":[tid],"formulations":forms,
             "editorial_status":"individually_source_and_mathematically_screened",
             "editorial_screening_reason":reason,"human_verified":False})
    if len(meanings)!=6 or len(individual)!=7 or sum(len(m["formulations"]) for m in meanings)!=7:
        raise PipelineError("Six distinct meanings with seven source formulations required")
    store(w.root/"wave2/cross110_individual_mathematical_reviews.jsonl",individual)
    intake=store(w.root/"intake/cross110_meanings.jsonl",meanings)
    oldms=w.records("meanings")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prev=jsonl(ledger)
    if len(prev) not in (580,587) or len({r["formulation_id"] for r in prev})!=len(prev):
        raise PipelineError("Expected 580 historical individually reviewed forms")
    if {i for r in prev for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Previously screened 774 relationships not all dispositioned")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_580_before_cross110.jsonl"
    if len(oldms)==552:
        if len(prev)!=580 or any(r["meaning_catalog_digest"]!=digest(list(oldms.values())) for r in prev):
            raise PipelineError("Historical meaning digest invalid")
        data=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=data:
            raise PipelineError("Historical snapshot changed")
        archive.write_text(data,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_580_before_cross110.json",{
            "rows":580,"historical_links":774,
            "sha256":hashlib.sha256(data.encode("utf-8")).hexdigest(),
            "human_peer_verified":False})
        w.ingest("meanings",intake,batch_size=6)
    ms=w.records("meanings")
    if len(ms)!=558 or any(ms.get(m["id"])!=m for m in meanings):
        raise PipelineError("Six new meaning records missing")
    old=jsonl(archive)
    if len(old)!=580 or len({r["formulation_id"] for r in old})!=580:
        raise PipelineError("Historical formulation review snapshot absent")
    d=digest(list(ms.values()))
    upcoming=[dict(r,meaning_catalog_digest=d) for r in old]
    for r in individual:
        upcoming.append({"formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
           "meaning_catalog_digest":d,"decision":"needs_review","relation_ids":[],
           "original_wave1_disposition":None,"source":"independent_cross_domain_context_screen_batch110",
           "editorial_reason":"Source-scoped mathematical definition screened, individual mathematical dependencies pending.",
           "reviewed_by":None,"human_verified":False})
    if len(prev)==587:
        if {r["formulation_id"]:r for r in prev}!={r["formulation_id"]:r for r in upcoming}:
            raise PipelineError("Existing Batch110 review would be changed")
    else:
        atomic_jsonl(ledger,sorted(upcoming,key=lambda r:r["formulation_id"]))
    now=jsonl(ledger);ix={r["formulation_id"]:r for r in now}
    if len(now)!=587 or len(ix)!=587:raise PipelineError("Expected 587 distinct individual formulation reviews")
    for r in old:
        cur=ix[r["formulation_id"]]
        if any(cur.get(k)!=v for k,v in r.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Unrelated historic disposition altered")
    if dict(Counter(r["decision"] for r in now))!={"linked":574,"no_supported_target":6,"needs_review":7}:
        raise PipelineError("Invalid pending/old formulation disposition split")
    check_cycles(ms,w.records("relations"))
    state=w.state("meanings")
    state.update(total=558,record_digest=d,screened_new_formulations=156,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
      "batch":110,"screened_meanings":558,"reviewed_formulations":587,
      "new_contextual_meanings":6,"new_individual_formulations":7,
      "historical_580_dispositions_preserved":True,"historical_774_links_preserved":True,
      "image_equivalent_source_formulations_grouped":True,
      "linear_module_vs_field_vector_scope_separated":True,
      "rank_finite_dimensional_image_preserved":True,
      "accumulation_sequence_vs_set_separated":True,
      "pending_individual_link_reviews":7,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch111: individually review direct module/vector/mapping/image/rank/closure/topology prerequisites for all seven source-screened forms."}
    atomic_json(w.root/"state/wave2_cross110_meaning_screen.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
