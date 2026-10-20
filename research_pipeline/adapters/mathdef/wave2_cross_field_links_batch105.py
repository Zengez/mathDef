"""Batch 105: screen individual Lipschitz/tree/probability independence links.

Review each of seven new formulations, preserve all 754 prior edges and
566 unrelated individual formulation decisions. Never coerce pairwise
independence into mutual independence or anchored into global Lipschitz.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":441,"observations":884,"meanings":547}
PW="https://proofwiki.org/wiki/Definition%3A"
URL_LIP=PW+"Lipschitz_Continuity"
URL_TREE=PW+"Tree_%28Graph_Theory%29"
URL_INDSIG=PW+"Independent_Sigma-Algebras"
URL_INDRV=PW+"Independent_Random_Variables/General_Definition"
M="meaning.wave2.cross104."
F="form.wave2.cross104."
METRIC="meaning.wave2.analysis98.metric-space"
SIMPLE="meaning.wave2.graph42.simple-undirected"
PROB="meaning.wave2.prob90.probability-space"
SIGMA="meaning.wave2.foundation.sigma-algebra"
GENRV="meaning.wave2.prob90.random-variable-general"
EDGES=(
 ("01",F+"lipschitz-global",METRIC,"metric spaces",URL_LIP,PW+"Metric_Space",
  "A global Lipschitz inequality compares distances d_X and d_Y for every pair of points in two metric spaces. The independently screened metric-space meaning defines the source and target distances; no completeness or compactness requirement is inserted."),
 ("02",F+"lipschitz-at-point-anchored",METRIC,"f:(X,d_X)",URL_LIP,PW+"Metric_Space",
  "The source's selected-point inequality d_Y(f(x),f(a))≤L d_X(x,a) presupposes the independently defined metric spaces. This link does not identify anchored Lipschitz with two-point local Lipschitz, nor does it imply global Lipschitz on X."),
 ("03",F+"tree-unrooted.1",SIMPLE,"simple connected graph",URL_TREE,PW+"Simple_Graph",
  "This circuit-free unrooted tree is first a simple undirected graph, and then additionally connected with no nontrivial closed trails. The graph target permits finite and infinite vertex sets and forbids multiple edges and loops; no rooted structure is assumed."),
 ("04",F+"tree-unrooted.2",SIMPLE,"simple connected graph",URL_TREE,PW+"Simple_Graph",
  "This cycle-free unrooted tree is first a simple undirected graph, with the additional connectedness and acyclicity properties. It is an equivalent tree formulation to the circuit-free variant in this specific undirected simple graph context, not a new finite-tree meaning."),
 ("05",F+"independent-sigma-pair",PROB,"probability space",URL_INDSIG,PW+"Probability_Space",
  "Independence of the two sub-sigma-algebras is defined relative to one probability measure P on (Ω,F). The independently screened probability-space definition supplies a normalized countably additive measure; independence requires event intersection factorization in addition."),
 ("06",F+"independent-sigma-pair",SIGMA,"sub-σ-algebras",URL_INDSIG,PW+"Sigma_Algebra",
  "Each of the two independent families is itself a sigma-algebra of measurable subsets of the common sample space. This independently screened sigma-algebra target supplies closure operations, but is not sufficient alone to assert independence."),
 ("07",F+"independent-sigma-countable",PROB,"(Ω,F,P)",URL_INDSIG,PW+"Probability_Space",
  "Countable mutual independence of sub-sigma-algebras uses a single probability measure P and requires product factorization on every finite set of distinct indices. The probability-space target supplies the measure, not the factorization property."),
 ("08",F+"independent-sigma-countable",SIGMA,"sub-σ-algebras",URL_INDSIG,PW+"Sigma_Algebra",
  "Each indexed G_n is a sigma-algebra contained in the ambient event sigma-algebra F. Mutual independence imposes additional joint finite-event factorization; mere pairwise independence is weaker and is not silently substituted."),
 ("09",F+"independent-rv-countable",PROB,"probability space",URL_INDRV,PW+"Probability_Space",
  "A family of jointly independent random variables is defined over one probability space (Ω,F,P), making the independent measure and its shared ambient sigma-algebra a direct prerequisite. No real-valued codomain restriction is added."),
 ("10",F+"independent-rv-countable",M+"independent-sigma-countable","mutually independent sequence",URL_INDRV,URL_INDSIG,
  "The source explicitly defines mutual independence of the generated sigma-algebras σ(X_n), exactly the countable mutually independent sub-sigma-algebra meaning already separately screened. Pairwise independence of the random variables is not enough for this target."),
 ("11",F+"independent-rv-countable",GENRV,"X_n:Ω→S",URL_INDRV,PW+"Random_Variable",
  "Each source-defined X_n is a measurable map from the common probability space to a measurable target (S,Σ_S). The existing general measurable-space-valued random-variable definition supplies that underlying object, without incorrectly requiring real-valued outputs.")
)

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(row)+"\n" for row in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Historical Batch105 individual links changed")
    path.write_text(body,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in (*BASE,"relations")):
        raise PipelineError("Requires unsealed independent Wave 2")
    if {k:len(w.records(k)) for k in BASE}!=BASE:
        raise PipelineError("Expected 547 reviewed mathematical meanings")
    report=json.loads((w.root/"state/wave2_cross104_meaning_screen.json").read_text())
    if report.get("screened_meanings")!=547 or report.get("reviewed_formulations")!=573 or not report.get("pairwise_vs_mutual_independence_distinct"):
        raise PipelineError("Batch104 mathematical variant evidence unverified")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=573:
        raise PipelineError("Expected 573 source-specific formulations")
    oldrels=w.records("relations")
    if len(oldrels) not in (754,765):
        raise PipelineError("Unexpected existing independent links")
    historic={k:r for k,r in oldrels.items() if not k.startswith("rel.wave2.cross105.")}
    if len(historic)!=754:
        raise PipelineError("Historical 754 screened relationships modified")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    oldreviews=jsonl(ledger);oldidx={r["formulation_id"]:r for r in oldreviews}
    if (len(oldreviews)!=573 or len(oldidx)!=573 or
        any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in oldreviews)
        or {i for r in oldreviews for i in r["relation_ids"]}!=set(oldrels)):
        raise PipelineError("Current complete individually reviewed history invalid")
    screened=[]
    for n,fid,target,phrase,sourceurl,targeturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Missing specific math source/target endpoint "+n)
        m,f=forms[fid]
        ids=f.get("evidence_ids",[])
        if (f["review_state"]!="screened" or len(ids)!=1 or ids[0] not in obs
            or obs[ids[0]]["locator"]!=sourceurl or locator(ms[target],obs)!=targeturl
            or phrase not in f["text"] or len(reason)<155):
            raise PipelineError("No exact source phrase/meaning-specific locator "+n)
        screened.append({
          "id":"rel.wave2.cross105."+n,"from_formulation":fid,
          "target_meaning":target,"relation_type":"definition_uses",
          "review_state":"screened","source_phrase":phrase,
          "source_locator":sourceurl,"target_locator":targeturl,
          "editorial_reason":reason,
          "reviewed_by":"assistant_independent_cross_field_prerequisite_screen_2026_10_20",
          "human_verified":False
        })
    incoming={fid for fid in forms if fid.startswith(F)}
    if len(incoming)!=7 or {r["from_formulation"] for r in screened}!=incoming or len(screened)!=11:
        raise PipelineError("Every one of seven formulations requires its own reviewed prerequisites")
    check_cycles(ms,{**historic,**{r["id"]:r for r in screened}})
    archive=w.root/"state/wave2_formulation_reviews_snapshot_573_before_cross105.jsonl"
    if len(oldrels)==754:
        if any(oldidx[fid]["decision"]!="needs_review" or oldidx[fid]["relation_ids"] for fid in incoming):
            raise PipelineError("New formulations were reviewed prematurely")
        prev=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=prev:
            raise PipelineError("Historic 573-review snapshot modified")
        archive.write_text(prev,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_573_before_cross105.json",{
          "rows":573,"historical_relations":754,
          "sha256":hashlib.sha256(prev.encode("utf-8")).hexdigest(),
          "human_peer_verified":False})
    past=jsonl(archive);by={r["formulation_id"]:r for r in past}
    if len(past)!=573 or len(by)!=573:
        raise PipelineError("Missing original 573 mathematical review events")
    store(w.root/"wave2/cross105_individual_source_screened_links.jsonl",screened)
    intake=store(w.root/"intake/cross105_links.jsonl",screened)
    if len(oldrels)==754:
        w.ingest("relations",intake,batch_size=11)
    nowrel=w.records("relations")
    if len(nowrel)!=765 or any(nowrel.get(r["id"])!=r for r in screened):
        raise PipelineError("Eleven new source-screened relationships not present")
    check_cycles(ms,nowrel)
    reviews=[]
    for prior in past:
        r=dict(prior);fid=r["formulation_id"]
        if fid in incoming:
            matched=[item["id"] for item in screened if item["from_formulation"]==fid]
            if not matched:
                raise PipelineError("A source-specific formulation lacks a reviewed link")
            r["relation_ids"]=matched
            r["decision"]="linked"
            r["reviewed_by"]="assistant_independent_cross_field_prerequisite_screen_2026_10_20"
            r["source"]="independent_cross_subfield_source_prerequisites_batch105"
            r["editorial_reason"]="Each precise source phrase and independent mathematical target reviewed; unsupported variant equivalences not assumed."
        reviews.append(r)
    if len(oldrels)==765:
        if {r["formulation_id"]:r for r in oldreviews}!={r["formulation_id"]:r for r in reviews}:
            raise PipelineError("Rerun would alter already reviewed context links")
    else:
        atomic_jsonl(ledger,sorted(reviews,key=lambda x:x["formulation_id"]))
    final=jsonl(ledger);idx={r["formulation_id"]:r for r in final}
    if len(final)!=573 or len(idx)!=573:
        raise PipelineError("All 573 individual reviews required")
    for fid,p in by.items():
        if fid not in incoming and idx[fid]!=p:
            raise PipelineError("Unrelated historical mathematical review mutated")
    if {id for r in final for id in r["relation_ids"]}!=set(nowrel):
        raise PipelineError("A new screened relation has no formulation-specific disposition")
    if dict(Counter(r["decision"] for r in final))!={"linked":567,"no_supported_target":6}:
        raise PipelineError("Unexpected reviewed dependency decisions")
    result={
      "batch":105,"screened_meanings":547,"reviewed_formulations":573,
      "screened_relationships":765,"new_individual_links":11,
      "historical_754_screened_links_preserved":True,
      "historical_566_unrelated_formulation_reviews_preserved":True,
      "all_seven_new_formulations_separately_dependency_reviewed":True,
      "lipschitz_global_and_anchored_not_conflated":True,
      "binary_and_countable_independence_not_conflated":True,
      "tree_two_formulations_linked_to_same_simple_graph":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Resume broad independent source discovery including unrelated branches; preserve historical source quality caveats and exact variant contexts."
    }
    atomic_json(w.root/"state/wave2_cross105_link_review.json",result)
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(parser.parse_args().workspace),indent=2))
if __name__=="__main__":main()
