"""Batch127: individual source-screened convergence and eigenvector prerequisites.

Preserve all 825 historical links and 611 unrelated source-formulation reviews.
A topological product target and separately screened eigenvalue remain future
coverage candidates, never fabricated dependency edges.
"""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":469,"observations":932,"meanings":583}
PW="https://proofwiki.org/wiki/Definition%3A"
POINT=PW+"Pointwise_Convergence";UNIF=PW+"Uniform_Convergence"
LOCAL=PW+"Locally_Uniform_Convergence";EIG=PW+"Eigenvector/Linear_Operator"
MAP=PW+"Mapping";TOP=PW+"Topological_Space";METRIC=PW+"Metric_Space";REAL=PW+"Real_Number"
LIN=PW+"Linear_Transformation";KERNEL=PW+"Kernel_of_Linear_Transformation"
VSPACE="https://stacks.math.columbia.edu/tag/09FM"
F="form.wave2.conv126."
M="meaning.wave2.conv126."
EDGES=(
 ("01",F+"pointwise-real","meaning.wave2.foundation.mapping-element-assignment","f_n,f:D→ℝ",POINT,MAP,
  "Pointwise convergence requires each f_n and its limit f be well-defined total maps on the same domain D. The independent mapping meaning supports this prerequisite; x-dependent thresholds are additional convergence conditions."),
 ("02",F+"pointwise-real","meaning.wave2.real45.complete-ordered-real-field","ℝ",POINT,REAL,
  "The source's real-valued pointwise ε-N inequality compares differences of real function values and finite real limits. The independently sourced complete real field supplies the scalar and absolute-value setting."),
 ("03",F+"pointwise-topological","meaning.wave2.foundation.topological-space","topological space T",POINT,TOP,
  "The topological pointwise formulation regards map values in a topological target T and the product topology of T^D. The independently reviewed topological-space definition supplies the target; the product topology itself remains a separately logged missing meaning."),
 ("04",F+"pointwise-topological","meaning.wave2.foundation.mapping-element-assignment","f_n,f:D→T",POINT,MAP,
  "A pointwise limit in function space T^D presupposes maps f_n and f with the same domain and target. The separately sourced mapping definition supplies total single-valued assignments, without imposing a topology on the domain D."),
 ("05",F+"uniform-metric","meaning.wave2.analysis98.metric-space","metric space",UNIF,METRIC,
  "Metric-target uniform convergence explicitly measures d(f_n(x),f(x)) in one metric space (M,d). The independently screened metric-space meaning supplies d and its axioms. The source domain S need not be a metric space."),
 ("06",F+"uniform-metric","meaning.wave2.foundation.mapping-element-assignment","f_n,f:S→M",UNIF,MAP,
  "The definition of uniform convergence applies to a sequence of typed mappings with shared domain S and target M. The underlying mapping definition supplies the assignment; the extra uniform ε-N quantification applies to all x at once."),
 ("07",F+"uniform-real","meaning.wave2.real45.complete-ordered-real-field","ℝ",UNIF,REAL,
  "The real-valued uniform convergence inequality uses real absolute differences |f_n(x)−f(x)| with finite real values. The independently sourced real-number system is necessary for this real specialization of metric-target uniformity."),
 ("08",F+"uniform-real","meaning.wave2.foundation.mapping-element-assignment","f_n,f:D→ℝ",UNIF,MAP,
  "The real-target formulation presupposes a sequence of real-valued mappings on the same domain D. The separately reviewed mapping definition gives that function type; one N independent of x is the convergence property."),
 ("09",F+"locally-uniform-metric","meaning.wave2.foundation.topological-space","topological space",LOCAL,TOP,
  "The locally uniform notion requires that each x of the domain X has a topological neighborhood U_x on which uniformity holds. The independent topological-space source defines the open sets giving neighborhoods, without assuming Hausdorff or local compactness."),
 ("10",F+"locally-uniform-metric","meaning.wave2.analysis98.metric-space","metric space",LOCAL,METRIC,
  "The locally uniform metric-target concept uses the metric d to compare f_n and f on each neighborhood. The separately sourced metric-space meaning supplies that codomain structure, without requiring a metric on the domain."),
 ("11",F+"locally-uniform-metric",M+"uniform-metric","uniformly",LOCAL,UNIF,
  "Locally uniform convergence is defined by uniform convergence of each restricted function sequence on some neighborhood of every domain point. The independently screened metric uniform-convergence context is therefore a direct, noncircular prerequisite."),
 ("12",F+"eigenvector-linear-operator.1","meaning.wave2.cross110.field-vector-linear","K-linear operator",EIG,LIN,
  "The eigenvector equation A(v)=λv assumes a K-linear operator A:V→V, an endomorphism rather than a transformation between unrelated vector spaces. The independently screened field-linear-map meaning supplies K-linearity; A being an endomorphism is specified additionally."),
 ("13",F+"eigenvector-linear-operator.1","meaning.b64bc15f46fe0245.vector-space-over-field","K-vector space",EIG,VSPACE,
  "Eigenvector v lies in a vector space V over field K, and λ multiplies v by the field scalar action. The independently sourced vector-space context supplies vector addition, zero and scalar multiplication; the explicit nonzero v requirement remains essential."),
 ("14",F+"eigenvector-linear-operator.2","meaning.wave2.cross110.field-vector-linear","K-linear operator",EIG,LIN,
  "For the shifted-map kernel characterization, both A and λI_V act linearly on the same field vector space V. The independently screened linear-transformation meaning supplies the field-linear condition, narrowed to domain equal to codomain."),
 ("15",F+"eigenvector-linear-operator.2","meaning.wave2.cross107.field-vector-linear-kernel","ker(A−λI_V)",EIG,KERNEL,
  "The shifted operator A−λI_V has a kernel consisting of vectors it sends to zero. The independently sourced field-vector linear-kernel meaning supplies this operator nullspace. The eigenvectors are its NONZERO elements, not the entire kernel.")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Prior exact source-specific prerequisite screen would change")
    path.write_text(body,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in (*BASE,"relations")):
        raise PipelineError("Independent unsealed Wave2 required")
    if {k:len(w.records(k)) for k in BASE}!=BASE:
        raise PipelineError("B126 screened mathematical meanings baseline missing")
    screen=json.loads((w.root/"state/wave2_conv126_meaning_screen.json").read_text())
    if screen.get("screened_meanings")!=583 or screen.get("reviewed_formulations")!=618 or not screen.get("zero_vector_not_eigenvector"):
        raise PipelineError("B126 source-specific mathematical review not verified")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=618:raise PipelineError("All 618 individual mathematical forms required")
    before_rel=w.records("relations")
    if len(before_rel) not in (825,840):raise PipelineError("Unexpected prior relationship count")
    old={id:r for id,r in before_rel.items() if not id.startswith("rel.wave2.conv127.")}
    if len(old)!=825:raise PipelineError("All 825 previous direct relationships must remain unchanged")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    before=jsonl(ledger);old_index={r["formulation_id"]:r for r in before}
    if (len(before)!=618 or len(old_index)!=618 or
      any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in before) or
      {i for r in before for i in r["relation_ids"]}!=set(before_rel)):
        raise PipelineError("Previous 618 individual review entries or digests invalid")
    checked=[]
    for n,fid,target,phrase,surl,turl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Independently sourced endpoint missing "+n)
        _,fm=forms[fid];evidence=fm.get("evidence_ids",[])
        if (fm["review_state"]!="screened" or len(evidence)!=1 or evidence[0] not in obs
          or obs[evidence[0]]["locator"]!=surl or locator(ms[target],obs)!=turl or
          phrase not in fm["text"] or len(reason)<150):
            raise PipelineError("Insufficient source-phrase target-grounded review "+n)
        checked.append({"id":"rel.wave2.conv127."+n,"from_formulation":fid,
          "target_meaning":target,"relation_type":"definition_uses",
          "review_state":"screened","source_phrase":phrase,"source_locator":surl,
          "target_locator":turl,"editorial_reason":reason,
          "reviewed_by":"assistant_independent_convergence_eigen_individual_dependency_review_2026_10_20",
          "human_verified":False})
    newids={fid for fid in forms if fid.startswith(F)}
    if len(newids)!=7 or len(checked)!=15 or {r["from_formulation"] for r in checked}!=newids:
        raise PipelineError("All seven accepted forms must have fifteen exact screened links")
    check_cycles(ms,{**old,**{r["id"]:r for r in checked}})
    archive=w.root/"state/wave2_formulation_reviews_snapshot_618_before_conv127.jsonl"
    if len(before_rel)==825:
        if any(old_index[fid]["decision"]!="needs_review" or old_index[fid]["relation_ids"] for fid in newids):
            raise PipelineError("Seven new forms cannot already have accepted mathematical relations")
        raw=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=raw:
            raise PipelineError("Prior historical review snapshot changed")
        archive.write_text(raw,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_618_before_conv127.json",{
          "rows":618,"prior_links":825,"sha256":hashlib.sha256(raw.encode()).hexdigest(),"human_peer_verified":False})
    saved=jsonl(archive);saved_by={r["formulation_id"]:r for r in saved}
    if len(saved)!=618 or len(saved_by)!=618:
        raise PipelineError("Full history of screened 618 mathematical forms absent")
    store(w.root/"wave2/conv127_individual_source_screened_links.jsonl",checked)
    intake=store(w.root/"intake/conv127_links.jsonl",checked)
    if len(before_rel)==825:w.ingest("relations",intake,batch_size=15)
    rel=w.records("relations")
    if len(rel)!=840 or any(rel.get(r["id"])!=r for r in checked):
        raise PipelineError("Fifteen specifically screened prerequisite links not admitted")
    check_cycles(ms,rel)
    revised=[]
    for p in saved:
        r=dict(p);fid=r["formulation_id"]
        if fid in newids:
            linkids=[e["id"] for e in checked if e["from_formulation"]==fid]
            if not linkids:raise PipelineError("New form lacked individual prerequisite decision")
            r["relation_ids"]=linkids;r["decision"]="linked"
            r["reviewed_by"]="assistant_independent_convergence_eigen_individual_dependency_review_2026_10_20"
            r["source"]="independent_convergence_eigen_definition_prerequisite_review_batch127"
            r["editorial_reason"]="Every source-specific mathematical prerequisite individually verified; prior decisions unchanged."
        revised.append(r)
    if len(before_rel)==840:
        if {r["formulation_id"]:r for r in before}!={r["formulation_id"]:r for r in revised}:
            raise PipelineError("Completed prior individual reviews would change on rerun")
    else:atomic_jsonl(ledger,sorted(revised,key=lambda r:r["formulation_id"]))
    reviews=jsonl(ledger);index={r["formulation_id"]:r for r in reviews}
    if len(reviews)!=618 or len(index)!=618:raise PipelineError("618 individual formulation reviews expected")
    for fid,p in saved_by.items():
        if fid not in newids and index[fid]!=p:
            raise PipelineError("Unrelated old mathematical decision altered")
    if {i for r in reviews for i in r["relation_ids"]}!=set(rel):
        raise PipelineError("Direct link not accounted for by individual formulation review")
    if dict(Counter(r["decision"] for r in reviews))!={"linked":612,"no_supported_target":6}:
        raise PipelineError("Unexpected final complete review distribution")
    for path in ("wave2/conv125_quarantined_source_claims.jsonl","wave2/quot118_quarantined_source_claims.jsonl","wave2/directional112_quarantined_source_claims.jsonl"):
        held=jsonl(w.root/path)
        if len(held)!=1 or held[0]["observation_id"] in {i for m in ms.values() for f in m["formulations"] for i in f["evidence_ids"]}:
            raise PipelineError("Known defective source claim incorrectly mathematically promoted")
    gaps=[{"topic":"pointwise convergence in arbitrary topological target",
       "missing_target":"product topology on T^D with appropriate finite-coordinate cylinder basis",
       "action":"source independently before adding dependency"},
      {"topic":"linear operator eigenvector",
       "missing_target":"field-linear operator eigenvalue as a separate mathematical meaning",
       "action":"independently source scalar eigenvalue condition; avoid circular eigenvalue/eigenvector definitions"}]
    store(w.root/"wave2/conv127_missing_prerequisite_targets.jsonl",gaps)
    report={"batch":127,"screened_meanings":583,"reviewed_formulations":618,"screened_relationships":840,
      "new_individually_source_screened_links":15,
      "all_825_prior_links_preserved":True,"all_611_old_reviews_preserved":True,
      "all_seven_new_forms_individually_reviewed":True,
      "pointwise_uniform_local_quantifiers_preserved":True,"nonzero_eigenvector_required":True,
      "three_held_source_errors_remain_unpromoted":True,
      "missing_product_topology_and_eigenvalue_targets_logged":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch128 independent breadth and selectively source missing product-topology/eigenvalue meanings without reading original mathDef corpus."}
    atomic_json(w.root/"state/wave2_conv127_link_review.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
