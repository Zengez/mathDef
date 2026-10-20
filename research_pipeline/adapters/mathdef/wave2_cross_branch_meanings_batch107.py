"""Batch107: mathematical screening of new topology, kernel and derivative contexts.

Equivalent closure/boundary presentations are one meaning each; module and
field-vector linear kernels remain separate contexts. Historical reviews
are snapshotted and preserved, with zero mathematical publication actions.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/cross_branch_source_variants_batch106_2026-10-20.jsonl"
BASE={"sources":14,"terms":445,"observations":891,"meanings":547,"relations":765}
AFTER=dict(BASE,meanings=552)
SPECS=(
 ("topological-closure",0,"topological-closure","Closure of a subset in an arbitrary topological space"),
 ("topological-boundary",0,"topological-boundary","Boundary of a subset relative to a specified topological ambient space"),
 ("linear-kernel",0,"module-linear-kernel","Kernel of a linear map between left R-modules"),
 ("linear-kernel",1,"field-vector-linear-kernel","Kernel or null space of a linear map between vector spaces over a common field"),
 ("derivative-on-interval",0,"derivative-function-open-interval","Derivative as a real-valued function on an open interval, not a single point value")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    data="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=data:
        raise PipelineError("Individual source-specific mathematical review changed")
    path.write_text(data,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Independent unsealed Wave2 required")
    current={k:len(w.records(k)) for k in BASE}
    if current not in (BASE,AFTER):
        raise PipelineError("Expected source-scoped intake counts "+str(current))
    report=json.loads((w.root/"state/wave2_cross106_source_intake.json").read_text())
    if (report.get("new_source_terms")!=4 or report.get("new_source_observations")!=7 or
        report.get("new_screened_meanings")!=0 or
        not report.get("incorrect_boundary_exterior_source_alternative_excluded")):
        raise PipelineError("Source-only audit/report absent or invalid")
    research={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    terms=w.records("terms");observations=w.records("observations")
    if len(research)!=4:
        raise PipelineError("Four original independently reviewed topics required")
    meanings=[];reviews=[]
    for key,ctxindex,suffix,scope in SPECS:
        r=research[key];tid="term.wave2.cross106."+key
        if tid not in terms or r["source"]!=terms[tid]["locator"] or r["production_corpus_consulted"]:
            raise PipelineError("Unsourced term/locator "+key)
        context=r["contexts"][ctxindex]
        reason=r["mathematical_review"]
        if len(reason)<300:
            raise PipelineError("Insufficient individual mathematical rationale")
        if key=="topological-closure":
            if len(context["formulations"])!=2 or "intersection" not in context["formulations"][0]["text"] or "smallest closed" not in context["formulations"][1]["text"]:
                raise PipelineError("Closure equivalent closed-superset variants incorrect")
            reason+=" Both presentations have the SAME mathematical context; do not generate a circular closure→boundary link."
        elif key=="topological-boundary":
            if len(context["formulations"])!=2 or "∩cl_X" not in context["formulations"][1]["text"] or "closure and exterior" not in reason:
                raise PipelineError("Boundary alternate proof or invalid exterior rejection missing")
            reason+=" Both valid boundary presentations define exactly one ambient-dependent topological boundary, not a geometric-boundary variant."
        elif key=="linear-kernel":
            if len(context["formulations"])!=1:
                raise PipelineError("Linear kernel source-specific scope unexpectedly changed")
            if ctxindex==0 and "R-linear" not in context["formulations"][0]["text"]:
                raise PipelineError("Module kernel linearity absent")
            if ctxindex==1 and "common field K" not in context["formulations"][0]["text"]:
                raise PipelineError("Field vector kernel scope missing")
            reason+=" The codomain zero element and preimage identity are explicit, unlike unrelated set-map fibers."
        elif key=="derivative-on-interval":
            if len(context["formulations"])!=1 or "f′:I→ℝ" not in context["formulations"][0]["text"]:
                raise PipelineError("Derivative function not separated from pointwise derivative")
            reason+=" The existing independently reviewed point derivative is not overwritten or collapsed into this function-valued object."
        mid="meaning.wave2.cross107."+suffix
        group=("wave2.cross107.linear-kernel" if key=="linear-kernel" else "wave2.cross107."+key)
        fs=[]
        for idx,f in enumerate(context["formulations"],1):
            oid=f"obs.wave2.cross106.{key}.{idx if ctxindex==0 else ctxindex+1:02d}"
            o=observations.get(oid)
            if (not o or o["term_id"]!=tid or o["locator"]!=r["source"] or
                o["source_id"]!="src.proofwiki" or o["text"]!=f["text"]):
                raise PipelineError("Individual formulation evidence mismatch "+suffix+"/"+str(idx))
            fid="form.wave2.cross107."+suffix+("."+str(idx) if len(context["formulations"])>1 else "")
            fs.append({
              "id":fid,"text":f["text"],"evidence_ids":[oid],"review_state":"screened",
              "human_verified":False,"mathematical_review_reason":reason,
              "source_screened_by":"assistant_independent_cross_branch_math_review_2026_10_20"})
            reviews.append({
              "review_id":"review.wave2.cross107."+suffix+("."+str(idx) if len(context["formulations"])>1 else ""),
              "meaning_id":mid,"formulation_id":fid,
              "source_observation_id":oid,"source_locator":r["source"],
              "mathematical_reason":reason,
              "decision":"mathematically_screened_pending_individual_dependency_review",
              "human_verified":False,"production_corpus_used":False})
        meanings.append({
           "id":mid,"term_group_id":group,"display_term":r["term"],
           "context":scope,"term_ids":[tid],"formulations":fs,
           "editorial_status":"individually_source_and_mathematically_screened",
           "editorial_screening_reason":reason,"human_verified":False
        })
    if len(meanings)!=5 or len(reviews)!=7 or sum(len(m["formulations"]) for m in meanings)!=7:
        raise PipelineError("Expected five meanings and seven source forms")
    store(w.root/"wave2/cross107_individual_mathematical_reviews.jsonl",reviews)
    intake=store(w.root/"intake/cross107_meanings.jsonl",meanings)
    oldms=w.records("meanings")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prev=jsonl(ledger)
    if len(prev) not in (573,580) or len({r["formulation_id"] for r in prev})!=len(prev):
        raise PipelineError("Complete prior 573 source-specific reviews absent")
    if {i for r in prev for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("All historical 765 independently screened links required")
    snap=w.root/"state/wave2_formulation_reviews_snapshot_573_before_cross107.jsonl"
    if len(oldms)==547:
        if len(prev)!=573 or any(r["meaning_catalog_digest"]!=digest(list(oldms.values())) for r in prev):
            raise PipelineError("Prior 573 meaning catalog digest mismatch")
        olddata=ledger.read_text(encoding="utf-8")
        if snap.exists() and snap.read_text(encoding="utf-8")!=olddata:
            raise PipelineError("Historical 573 review snapshot changed")
        snap.write_text(olddata,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_573_before_cross107.json",{
          "rows":573,"prior_links":765,"sha256":hashlib.sha256(olddata.encode()).hexdigest(),
          "human_peer_verified":False})
        w.ingest("meanings",intake,batch_size=5)
    nowms=w.records("meanings")
    if len(nowms)!=552 or any(nowms.get(m["id"])!=m for m in meanings):
        raise PipelineError("Approved distinct mathematical meanings missing")
    oldreviews=jsonl(snap)
    if len(oldreviews)!=573 or len({r["formulation_id"] for r in oldreviews})!=573:
        raise PipelineError("Missing historical review snapshot")
    d=digest(list(nowms.values()))
    expected=[dict(r,meaning_catalog_digest=d) for r in oldreviews]
    for r in reviews:
        expected.append({
          "formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
          "meaning_catalog_digest":d,"decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,"source":"independent_cross_branch_meaning_review_batch107",
          "editorial_reason":"Individually mathematically source-screened, direct prerequisites reviewed separately.",
          "reviewed_by":None,"human_verified":False})
    if len(prev)==580:
        if {r["formulation_id"]:r for r in prev}!={r["formulation_id"]:r for r in expected}:
            raise PipelineError("Repeat Batch107 would alter previous mathematical reviews")
    else:
        atomic_jsonl(ledger,sorted(expected,key=lambda r:r["formulation_id"]))
    currentreviews=jsonl(ledger);ix={r["formulation_id"]:r for r in currentreviews}
    if len(currentreviews)!=580 or len(ix)!=580:
        raise PipelineError("Expected 580 individual review records")
    for p in oldreviews:
        new=ix[p["formulation_id"]]
        if any(new.get(k)!=v for k,v in p.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Historic individual formulation review changed")
    if {i for r in currentreviews for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Earlier 765 links not completely reviewed")
    if dict(Counter(r["decision"] for r in currentreviews))!={"linked":567,"no_supported_target":6,"needs_review":7}:
        raise PipelineError("Unexpected new/past review decisions")
    check_cycles(nowms,w.records("relations"))
    state=w.state("meanings")
    state.update(total=552,record_digest=d,screened_new_formulations=149,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    result={"batch":107,"screened_meanings":552,"reviewed_formulations":580,
            "new_contextual_meanings":5,"new_formulations":7,
            "historical_573_individual_decisions_preserved":True,
            "historical_765_screened_links_preserved":True,
            "closure_and_boundary_equivalent_presentations_grouped":True,
            "module_and_vector_field_kernels_distinct":True,
            "interval_derivative_not_same_as_single_point_derivative":True,
            "erroneous_exterior_boundary_variant_excluded":True,
            "pending_individual_link_reviews":7,"all_stages_unsealed":True,
            "human_peer_verified":False,"production_corpus_used":False,
            "next":"Batch108 exact noncircular source→prerequisite reviews for all seven formulations, reusing verified existing topological interior and pointwise derivative meanings."}
    atomic_json(w.root/"state/wave2_cross107_meaning_screen.json",result)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__": main()
