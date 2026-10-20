"""Batch108: nine individually justified noncircular topology/kernel/derivative links.

Preserves original 765 screened edges and all 573 unrelated formulation
dispositions. All five meanings and seven forms have exact source locators.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":445,"observations":891,"meanings":552}
PW="https://proofwiki.org/wiki/Definition%3A"
CLOS=PW+"Closure_%28Topology%29"
BOUND=PW+"Boundary_%28Topology%29"
KERNEL=PW+"Kernel_of_Linear_Transformation"
DERIV=PW+"Derivative_of_Real_Function"
TOP=PW+"Topological_Space"
INTERIOR="https://stacks.math.columbia.edu/tag/03HM"
MODULE=PW+"Module_over_Ring"
VEC="https://stacks.math.columbia.edu/tag/09FM"
POINT="https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative"
M="meaning.wave2.cross107."
F="form.wave2.cross107."
EDGES=(
 ("01",F+"topological-closure.1","meaning.wave2.foundation.topological-space","topological space",CLOS,TOP,
  "The intersection-of-all-closed-supersets closure is defined relative to a topology τ on an ambient set X. The independently screened open-set-axioms topology supplies the meaning of τ and of the closed complements; no separation axioms are assumed."),
 ("02",F+"topological-closure.2","meaning.wave2.foundation.topological-space","topological space",CLOS,TOP,
  "The smallest-closed-containing-set formulation is meaningful only in a specified ambient topological space, whose closed sets are complements of its open sets. The underlying topological-space target is independently source-screened and applies even to empty ambient spaces."),
 ("03",F+"topological-boundary.1",M+"topological-closure","cl_X(A)",BOUND,CLOS,
  "The formula ∂_X A=cl_X(A)\\int_X(A) directly uses the independently defined closure of A in the same ambient topological space X. Closure is screened through closed supersets, not by reference to boundary, so no circular mathematical dependency is introduced."),
 ("04",F+"topological-boundary.1","meaning.c15e2b26c207d87e.interior-subset-topological","int_X(A)",BOUND,INTERIOR,
  "The formula ∂_X A=cl_X(A)\\int_X(A) directly uses the interior of A relative to X. The existing independently sourced topology-interior meaning gives the union of all open subsets lying inside A, avoiding any geometric versus topological interior ambiguity."),
 ("05",F+"topological-boundary.2",M+"topological-closure","cl_X(A)",BOUND,CLOS,
  "The alternative boundary formula cl_X(A)∩cl_X(X\\A) applies closure to A and to its complement in the exact ambient X. It depends on topological closure but not on a falsely included complement-exterior formula; relative subspace boundaries may differ."),
 ("06",F+"module-linear-kernel","meaning.wave2.foundation.left-module-nonunital","left R-modules",KERNEL,MODULE,
  "The kernel of an R-linear homomorphism presupposes additive left R-modules M and N. Their independently screened module meaning defines scalar action and additive group structure; the kernel preimage uses zero in the CODOMAIN N, not in M."),
 ("07",F+"field-vector-linear-kernel","meaning.b64bc15f46fe0245.vector-space-over-field","vector spaces",KERNEL,VEC,
  "A kernel of a K-linear map V→W between vector spaces over a common field uses vector addition, scalar compatibility and the zero vector of W. The independently reviewed field-vector-space definition supplies exactly those structures and is narrower than arbitrary modules."),
 ("08",F+"field-vector-linear-kernel",M+"module-linear-kernel","kernel",KERNEL,KERNEL,
  "A linear transformation over a field is also a homomorphism between its underlying modules, so its zero-vector preimage is the specific field-vector-space instance of the earlier R-linear module-kernel definition. This specialization link does not claim all module kernels are vector-space kernels."),
 ("09",F+"derivative-function-open-interval","meaning.wave2.analysis.real-derivative-point","f′(x)",DERIV,POINT,
  "The derivative function f′:I→ℝ assigns to each interior x the previously independently screened finite two-sided derivative f′(x). This is an assembly of pointwise derivative values across the open interval I, not the definition of a single derivative number at a fixed point.")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Historical exact Batch108 link screening changed")
    path.write_text(body,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in (*BASE,"relations")):
        raise PipelineError("Independent unsealed Wave2 required")
    if {s:len(w.records(s)) for s in BASE}!=BASE:
        raise PipelineError("Source-screened Batch107 meanings absent")
    screen=json.loads((w.root/"state/wave2_cross107_meaning_screen.json").read_text())
    if screen.get("screened_meanings")!=552 or screen.get("reviewed_formulations")!=580 or not screen.get("erroneous_exterior_boundary_variant_excluded"):
        raise PipelineError("Batch107 mathematical screen invalid")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=580:
        raise PipelineError("Expected 580 individually mathematical formulations")
    previous=w.records("relations")
    if len(previous) not in (765,774):
        raise PipelineError("Unexpected relationship baseline")
    oldrel={i:r for i,r in previous.items() if not i.startswith("rel.wave2.cross108.")}
    if len(oldrel)!=765:
        raise PipelineError("All 765 historic links must survive unchanged")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    last=jsonl(ledger);lastindex={r["formulation_id"]:r for r in last}
    if (len(last)!=580 or len(lastindex)!=580 or
        any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in last) or
        {i for r in last for i in r["relation_ids"]}!=set(previous)):
        raise PipelineError("Current 580-formulation reviewed ledger not complete")
    prepared=[]
    for n,fid,target,phrase,sourceurl,targeturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Missing screened prerequisite endpoint "+n)
        meaning,form=forms[fid];ids=form.get("evidence_ids",[])
        if (form["review_state"]!="screened" or len(ids)!=1 or ids[0] not in obs or
            obs[ids[0]]["locator"]!=sourceurl or
            locator(ms[target],obs)!=targeturl or phrase not in form["text"] or
            len(reason)<160):
            raise PipelineError("Exact individual source/target evidence invalid "+n)
        prepared.append({
           "id":"rel.wave2.cross108."+n,
           "from_formulation":fid,"target_meaning":target,
           "relation_type":"definition_uses","review_state":"screened",
           "source_phrase":phrase,"source_locator":sourceurl,
           "target_locator":targeturl,"editorial_reason":reason,
           "reviewed_by":"assistant_independent_topology_linear_calculus_link_review_2026_10_20",
           "human_verified":False})
    newforms={fid for fid in forms if fid.startswith(F)}
    if len(prepared)!=9 or len(newforms)!=7 or {e["from_formulation"] for e in prepared}!=newforms:
        raise PipelineError("Every new formulation needs individually screened edges")
    check_cycles(ms,{**oldrel,**{e["id"]:e for e in prepared}})
    snap=w.root/"state/wave2_formulation_reviews_snapshot_580_before_cross108.jsonl"
    if len(previous)==765:
        if any(lastindex[fid]["decision"]!="needs_review" or lastindex[fid]["relation_ids"] for fid in newforms):
            raise PipelineError("Batch107 new formulations already link-reviewed")
        oldtext=ledger.read_text(encoding="utf-8")
        if snap.exists() and snap.read_text(encoding="utf-8")!=oldtext:
            raise PipelineError("Historical 580 review archive differs")
        snap.write_text(oldtext,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_580_before_cross108.json",{
          "rows":580,"prior_links":765,"sha256":hashlib.sha256(oldtext.encode("utf-8")).hexdigest(),
          "human_peer_verified":False})
    past=jsonl(snap);oldidx={r["formulation_id"]:r for r in past}
    if len(past)!=580 or len(oldidx)!=580:
        raise PipelineError("Historical 580 review decisions absent")
    store(w.root/"wave2/cross108_individually_screened_links.jsonl",prepared)
    intake=store(w.root/"intake/cross108_links.jsonl",prepared)
    if len(previous)==765:
        w.ingest("relations",intake,batch_size=9)
    rel=w.records("relations")
    if len(rel)!=774 or any(rel.get(r["id"])!=r for r in prepared):
        raise PipelineError("Nine source-screened relationships not admitted")
    check_cycles(ms,rel)
    revised=[]
    for original in past:
        r=dict(original);fid=r["formulation_id"]
        if fid in newforms:
            added=[e["id"] for e in prepared if e["from_formulation"]==fid]
            if not added: raise PipelineError("Unreviewed new form "+fid)
            r["relation_ids"]=added
            r["decision"]="linked"
            r["reviewed_by"]="assistant_independent_topology_linear_calculus_link_review_2026_10_20"
            r["source"]="independent_topological_and_linear_derivative_prerequisites_batch108"
            r["editorial_reason"]="Exact individually source-screened prerequisite, existing historic graph untouched and acyclic."
        revised.append(r)
    if len(previous)==774:
        if {r["formulation_id"]:r for r in last}!={r["formulation_id"]:r for r in revised}:
            raise PipelineError("Rerunning would modify previously reviewed source relations")
    else:
        atomic_jsonl(ledger,sorted(revised,key=lambda r:r["formulation_id"]))
    current=jsonl(ledger);idx={r["formulation_id"]:r for r in current}
    if len(current)!=580 or len(idx)!=580:
        raise PipelineError("All 580 separate reviewed forms required")
    for fid,p in oldidx.items():
        if fid not in newforms and idx[fid]!=p:
            raise PipelineError("Unrelated historical individual review changed")
    if {i for r in current for i in r["relation_ids"]}!=set(rel):
        raise PipelineError("Any missing individual relationship review invalidates batch")
    if dict(Counter(r["decision"] for r in current))!={"linked":574,"no_supported_target":6}:
        raise PipelineError("Unexpected review status distribution")
    report={"batch":108,"screened_meanings":552,"reviewed_formulations":580,
      "screened_relationships":774,"new_individual_links":9,
      "historic_765_links_preserved":True,
      "historic_573_unrelated_formulation_reviews_preserved":True,
      "all_seven_new_formulations_separately_link_reviewed":True,
      "closure_not_circularly_defined_using_boundary":True,
      "invalid_boundary_exterior_source_variant_excluded":True,
      "module_and_vector_kernel_scope_separated":True,
      "derivative_function_to_point_derivative_linked":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch109 independent cross-field breadth discovery, including direct source quality checks and contextual closure variants; avoid reseeding already reviewed contexts."}
    atomic_json(w.root/"state/wave2_cross108_link_review.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
