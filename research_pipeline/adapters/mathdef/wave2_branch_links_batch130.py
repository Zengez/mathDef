"""Batch130: twelve individually sourced direct mathematical prerequisites.

Preserves all earlier 840 links and 618 unrelated screened formulations;
does not retroactively link old pointwise or eigenvector forms in this batch.
"""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":473,"observations":938,"meanings":587}
PW="https://proofwiki.org/wiki/Definition%3A"
PROD=PW+"Product_Topology";EIG=PW+"Eigenvalue";GRAPH=PW+"Connected_%28Graph_Theory%29/Graph";EGF=PW+"Exponential_Generating_Function"
TOP=PW+"Topological_Space";MAP=PW+"Mapping";LINEAR=PW+"Linear_Transformation"
KERNEL=PW+"Kernel_of_Linear_Transformation";SIMPLE=PW+"Simple_Graph"
VSPACE="https://stacks.math.columbia.edu/tag/09FM"
REAL=PW+"Real_Number";POWER=PW+"Power_Series/Real_Domain";CONV=PW+"Convergent_Series"
F="form.wave2.branch129.";M="meaning.wave2.branch129."
EDGES=(
 ("01",F+"indexed-product-topology.1","meaning.wave2.foundation.topological-space","topological spaces",PROD,TOP,
 "An indexed product topology begins with each topological factor (X_i,τ_i), so the independently screened topological-space definition supplies its coordinate open sets. The cylinder-preimage family is a SUBBASIS, not the topology itself."),
 ("02",F+"indexed-product-topology.1","meaning.wave2.foundation.mapping-element-assignment","projection",PROD,MAP,
 "Each product-coordinate projection π_i:X→X_i is a map taking a tuple to its ith entry. The source-specific mapping definition supplies its total single-valued behavior, used in the inverse-image cylinder subbasis."),
 ("03",F+"indexed-product-topology.2","meaning.wave2.foundation.topological-space","topological spaces",PROD,TOP,
 "The finite-support open product basis uses open sets U_i of a topological space X_i in each coordinate, with all but finitely many unrestricted. The independently reviewed topology meaning supplies precisely those factor open subsets."),
 ("04",F+"operator-eigenvalue.1","meaning.wave2.cross110.field-vector-linear","K-linear operator",EIG,LINEAR,
 "An eigenvalue of A requires a K-linear endomorphism A:V→V so the shifted map A−λI_V is linear and type-correct. The separately sourced field-linear transformation meaning supplies the K-linear structure, with equal domain and codomain specified."),
 ("05",F+"operator-eigenvalue.1","meaning.wave2.cross107.field-vector-linear-kernel","ker(A−λI_V)",EIG,KERNEL,
 "The scalar λ is an eigenvalue exactly when the K-linear shifted operator A−λI_V has a kernel containing a NONZERO vector. The independently screened linear-map kernel definition supplies that preimage-of-zero construction."),
 ("06",F+"operator-eigenvalue.2","meaning.wave2.cross110.field-vector-linear","K-linear endomorphism",EIG,LINEAR,
 "The equivalent existence of v≠0 with A(v)=λv presupposes the same field-linear map from V to itself. This source-grounded target supplies the linear assignment; nonzero eigenvectors are witnesses, not the eigenvalue itself."),
 ("07",F+"operator-eigenvalue.2","meaning.b64bc15f46fe0245.vector-space-over-field","nonzero v",EIG,VSPACE,
 "The witness v lies in the K-vector space V and must be nonzero; λ acts by field scalar multiplication. The independently sourced vector-space target supplies addition, scalar multiplication and its zero element."),
 ("08",F+"nonempty-connected-graph","meaning.wave2.graph42.simple-undirected","simple undirected graph",GRAPH,SIMPLE,
 "The connectivity predicate quantifies over pairs of vertices in a simple undirected graph with two-element unordered edges. The independently screened graph target supplies vertices and edges, while this definition explicitly restricts V to nonempty."),
 ("09",F+"real-convergent-egf","meaning.wave2.prereq122.real-centered-power-series","∑",EGF,POWER,
 "The analytic exponential generating function evaluates the power series with real coefficients b_n=a_n/n! and center zero. The independently screened centered real-power-series meaning supplies its unevaluated expression, but does not alone imply convergence."),
 ("10",F+"real-convergent-egf","meaning.wave2.prereq122.real-series-convergent","converges",EGF,CONV,
 "The domain of the exponential generating function comprises exactly real z for which the numeric series sum of b_n z^n has a finite real limit. The separately reviewed convergent-series meaning supplies convergence of partial sums."),
 ("11",F+"real-convergent-egf","meaning.wave2.foundation.mapping-element-assignment","E_A:D→ℝ",EGF,MAP,
 "Unlike a purely formal EGF, the definition here is an actual typed real-valued map E_A:D→R on the convergent locus D. The independently sourced mapping meaning supplies that input-to-unique-output assignment."),
 ("12",F+"real-convergent-egf","meaning.wave2.real45.complete-ordered-real-field","ℝ",EGF,REAL,
 "The real sequence coefficients, real argument z and finite real-valued power series sum require the real field, not merely a generic coefficient ring. The independently screened real-number meaning supplies the required scalar setting.")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Previously committed individual source/link review differs")
    path.write_text(body,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in (*BASE,"relations")):
        raise PipelineError("Requires unsealed independent Wave2")
    if {k:len(w.records(k)) for k in BASE}!=BASE:
        raise PipelineError("Screened Batch129 mathematical source meanings missing")
    outcome=json.loads((w.root/"state/wave2_branch129_meaning_screen.json").read_text())
    if outcome.get("screened_meanings")!=587 or outcome.get("reviewed_formulations")!=624 or not outcome.get("product_subbasis_finite_support_basis_equivalent"):
        raise PipelineError("Batch129 verified mathematical screen absent")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=624:raise PipelineError("624 individual mathematical formulations expected")
    earlier=w.records("relations")
    if len(earlier) not in (840,852):raise PipelineError("Unexpected existing reviewed link baseline")
    previous={i:r for i,r in earlier.items() if not i.startswith("rel.wave2.branch130.")}
    if len(previous)!=840:raise PipelineError("All prior 840 relations must stay unchanged")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl";original=jsonl(ledger)
    old={r["formulation_id"]:r for r in original}
    if (len(original)!=624 or len(old)!=624 or
      any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in original) or
      {i for r in original for i in r["relation_ids"]}!=set(earlier)):
        raise PipelineError("Previous individual formulation decisions/digests invalid")
    edges=[]
    for n,fid,target,phrase,srcurl,tgturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Missing specific independent source/target endpoint "+n)
        _,form=forms[fid];evidence=form.get("evidence_ids",[])
        if (form["review_state"]!="screened" or len(evidence)!=1 or evidence[0] not in obs
            or obs[evidence[0]]["locator"]!=srcurl or locator(ms[target],obs)!=tgturl
            or phrase not in form["text"] or len(reason)<150):
            raise PipelineError("Mathematical reason, exact source phrase or target unsupported "+n)
        edges.append({"id":"rel.wave2.branch130."+n,"from_formulation":fid,
            "target_meaning":target,"relation_type":"definition_uses",
            "review_state":"screened","source_phrase":phrase,
            "source_locator":srcurl,"target_locator":tgturl,
            "editorial_reason":reason,
            "reviewed_by":"assistant_independent_product_eigen_graph_egf_direct_dependency_screen_2026_10_20",
            "human_verified":False})
    fresh={fid for fid in forms if fid.startswith(F)}
    if len(fresh)!=6 or len(edges)!=12 or {r["from_formulation"] for r in edges}!=fresh:
        raise PipelineError("Twelve individually screened links must cover all six new forms")
    check_cycles(ms,{**previous,**{r["id"]:r for r in edges}})
    archive=w.root/"state/wave2_formulation_reviews_snapshot_624_before_branch130.jsonl"
    if len(earlier)==840:
        if any(old[fid]["decision"]!="needs_review" or old[fid]["relation_ids"] for fid in fresh):
            raise PipelineError("Fresh formulations were previously marked reviewed")
        text=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=text:
            raise PipelineError("Historic 624-row source review snapshot altered")
        archive.write_text(text,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_624_before_branch130.json",
            {"rows":624,"old_relations":840,"sha256":hashlib.sha256(text.encode()).hexdigest(),
             "human_peer_verified":False})
    saved=jsonl(archive);saved_by={r["formulation_id"]:r for r in saved}
    if len(saved)!=624 or len(saved_by)!=624:raise PipelineError("Historical 624-row review snapshot missing")
    store(w.root/"wave2/branch130_individual_source_screened_links.jsonl",edges)
    intake=store(w.root/"intake/branch130_links.jsonl",edges)
    if len(earlier)==840:w.ingest("relations",intake,batch_size=12)
    relations=w.records("relations")
    if len(relations)!=852 or any(relations.get(r["id"])!=r for r in edges):
        raise PipelineError("Twelve prerequisite links not admitted exactly")
    check_cycles(ms,relations)
    revised=[]
    for p in saved:
        row=dict(p);fid=row["formulation_id"]
        if fid in fresh:
            ids=[e["id"] for e in edges if e["from_formulation"]==fid]
            if not ids:raise PipelineError("New formulation lacks separately sourced prerequisites")
            row["relation_ids"]=ids;row["decision"]="linked"
            row["reviewed_by"]="assistant_independent_product_eigen_graph_egf_direct_dependency_screen_2026_10_20"
            row["source"]="independent_product_eigen_graph_egf_dependency_review_batch130"
            row["editorial_reason"]="Individually source-checked direct mathematical prerequisites; older decisions untouched."
        revised.append(row)
    if len(earlier)==852:
        if {r["formulation_id"]:r for r in original}!={r["formulation_id"]:r for r in revised}:
            raise PipelineError("Already reviewed individual links changed on rerun")
    else:atomic_jsonl(ledger,sorted(revised,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);index={r["formulation_id"]:r for r in final}
    if len(final)!=624 or len(index)!=624:raise PipelineError("624 individually dispositioned definitions required")
    for fid,r in saved_by.items():
        if fid not in fresh and index[fid]!=r:
            raise PipelineError("Unrelated historic formulation decision rewritten")
    if {i for r in final for i in r["relation_ids"]}!=set(relations):
        raise PipelineError("Some mathematical edge lacks a reviewed-source decision")
    if dict(Counter(r["decision"] for r in final))!={"linked":618,"no_supported_target":6}:
        raise PipelineError("Wrong individual review decision totals")
    for path in ("wave2/conv125_quarantined_source_claims.jsonl","wave2/quot118_quarantined_source_claims.jsonl","wave2/directional112_quarantined_source_claims.jsonl"):
        held=jsonl(w.root/path)
        if len(held)!=1 or held[0]["observation_id"] in {i for m in ms.values() for f in m["formulations"] for i in f["evidence_ids"]}:
            raise PipelineError("Historical mathematically erroneous source claim promoted")
    report={"batch":130,"screened_meanings":587,"reviewed_formulations":624,
      "screened_relationships":852,"new_individual_screened_links":12,
      "all_old_840_relations_preserved":True,"all_618_unrelated_formulation_decisions_preserved":True,
      "all_six_new_formulations_individually_link_reviewed":True,
      "product_topology_source_scope_retained":True,"operator_eigenvalue_noncircular_with_eigenvector":True,
      "real_EGF_not_confused_with_formal_series":True,
      "three_held_source_defects_unpromoted":True,"dependency_graph_has_cycles":False,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch131 retroactive individual prerequisite review from previously screened topological pointwise convergence to T^D product topology and both eigenvector variants to source-defined eigenvalue, avoiding any dependency cycle."}
    atomic_json(w.root/"state/wave2_branch130_link_review.json",report);return report
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
