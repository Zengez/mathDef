"""Batch 82: screened graph prerequisite and explicit martingale missing targets.

Avoid inventing filtered-probability-space or conditional-expectation edges.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":417,"observations":852,"meanings":517}
GRAPH="meaning.wave2.graph42.simple-undirected"
CHROM="form.wave2.research81.chromatic-proper-coloring.01"
URL_FROM="https://proofwiki.org/wiki/Definition%3AChromatic_Number"
URL_TO="https://proofwiki.org/wiki/Definition%3ASimple_Graph"
MART={
 "form.wave2.research81.martingale-discrete.01":{
   "context":"discrete time, adjacent-time conditional expectation",
   "missing":["filtered probability space","adapted stochastic process","conditional expectation","integrable random variable"]},
 "form.wave2.research81.martingale-discrete.02":{
   "context":"discrete time, all-later-times conditional expectation",
   "missing":["filtered probability space","adapted stochastic process","conditional expectation","integrable random variable"]},
 "form.wave2.research81.martingale-continuous-index.01":{
   "context":"continuous-time-indexed process, without continuity of trajectories",
   "missing":["continuous-time filtration","adapted stochastic process","conditional expectation","integrable random variable"]}
}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    text="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=text:
        raise PipelineError("Historical screening source record changed")
    path.write_text(text,encoding="utf-8")
    return path
def form_source(form,obs):
    evidence=form.get("evidence_ids",[])
    if len(evidence)!=1 or evidence[0] not in obs:
        raise PipelineError("Formulation lacks precise individual observation")
    return obs[evidence[0]]["locator"]
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BASE,"relations")):
        raise PipelineError("Independent Wave 2 must be unsealed")
    if {s:len(w.records(s)) for s in BASE}!=BASE:
        raise PipelineError("Unreviewed meanings appeared during prerequisite screening")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=541:
        raise PipelineError("Expected 541 individually mathematical formulations")
    oldlinks=w.records("relations")
    if len(oldlinks) not in (705,706):
        raise PipelineError("Unexpected screen relationship baseline")
    historic_links={i:r for i,r in oldlinks.items() if not i.startswith("rel.wave2.research82.")}
    if len(historic_links)!=705:
        raise PipelineError("705 old reviewed links not preserved")
    m,f=forms[CHROM]
    if (not ms.get(GRAPH) or form_source(f,obs)!=URL_FROM
        or locator(ms[GRAPH],obs)!=URL_TO
        or "finite simple undirected graph G" not in f["text"]):
        raise PipelineError("Graph color prerequisite has no precise source/target support")
    edge={
      "id":"rel.wave2.research82.01","from_formulation":CHROM,
      "target_meaning":GRAPH,"relation_type":"definition_uses",
      "review_state":"screened",
      "source_phrase":"finite simple undirected graph G",
      "source_locator":URL_FROM,"target_locator":URL_TO,
      "editorial_reason":"The chromatic number is defined for a finite simple undirected graph with vertex set and edge set. The existing independently sourced simple-graph meaning establishes precisely the loop-free undirected edge relation required by the proper vertex-coloring criterion; finite nonempty restrictions are additional scope choices, and graph coloring itself needs separate sourcing.",
      "reviewed_by":"assistant_independent_martingale_chromatic_dependency_review_2026_10_20",
      "human_verified":False
    }
    check_cycles(ms,{**historic_links,edge["id"]:edge})
    absent=[]
    for fid,details in MART.items():
        if fid not in forms or form_source(forms[fid][1],obs) not in (
            "https://proofwiki.org/wiki/Definition%3AMartingale",
            "https://proofwiki.org/wiki/Definition%3AMartingale/Discrete_Time"
        ):
            raise PipelineError("Individually source-scoped martingale formulation changed")
        if len(details["missing"])<3:
            raise PipelineError("Martingale prerequisite review too narrow")
        absent.append({
          "formulation_id":fid,"decision":"no_supported_target",
          "mathematical_context":details["context"],
          "missing_independently_sourced_prerequisites":details["missing"],
          "reason":"No independently screened meaning defines the filtered probability space, adapted stochastic process, conditional expectation or integrability conditions used here. A link to the martingale itself or to the other time-index context would be circular or conflate source scope. Review these foundations separately before revisiting this decision.",
          "human_verified":False
        })
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prior=jsonl(ledger);idx={r["formulation_id"]:r for r in prior}
    if (len(prior)!=541 or len(idx)!=541
        or any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in prior)
        or {id for r in prior for id in r["relation_ids"]}!=set(oldlinks)):
        raise PipelineError("Historical individual review ledger inconsistent")
    target=set(MART)|{CHROM}
    snapshot=w.root/"state/wave2_formulation_reviews_snapshot_541_before_research82.jsonl"
    if len(oldlinks)==705:
        if any(idx[id]["decision"]!="needs_review" or idx[id]["relation_ids"] for id in target):
            raise PipelineError("Four new contextual formulations not in pending status")
        oldtext=ledger.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=oldtext:
            raise PipelineError("Historical 541-review snapshot changed")
        snapshot.write_text(oldtext,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_541_before_research82.json",{
          "rows":541,"reviewed_links":705,
          "sha256":hashlib.sha256(oldtext.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
    previous=jsonl(snapshot)
    if len(previous)!=541 or len({r["formulation_id"] for r in previous})!=541:
        raise PipelineError("Missing historical complete 541-formulation snapshot")
    store(w.root/"wave2/research82_individual_no_supported_targets.jsonl",absent)
    store(w.root/"wave2/research82_individual_links.jsonl",[edge])
    input_path=store(w.root/"intake/research82_links.jsonl",[edge])
    if len(oldlinks)==705:
        w.ingest("relations",input_path,batch_size=1)
    current=w.records("relations")
    if len(current)!=706 or current.get(edge["id"])!=edge:
        raise PipelineError("Missing one independently screened graph prerequisite")
    check_cycles(ms,current)
    reviews=[]
    for r in previous:
        new=dict(r);fid=r["formulation_id"]
        if fid in target:
            new["reviewed_by"]="assistant_independent_martingale_chromatic_dependency_review_2026_10_20"
            if fid==CHROM:
                new["decision"]="linked"
                new["relation_ids"]=[edge["id"]]
                new["source"]="independent_graph_source_link_review_batch82"
                new["editorial_reason"]=edge["editorial_reason"]
            else:
                new["decision"]="no_supported_target"
                new["relation_ids"]=[]
                new["source"]="independent_martingale_missing_prerequisite_review_batch82"
                new["editorial_reason"]=next(x["reason"] for x in absent if x["formulation_id"]==fid)
        reviews.append(new)
    if len(oldlinks)==706:
        if {r["formulation_id"]:r for r in reviews}!={r["formulation_id"]:r for r in prior}:
            raise PipelineError("Repeated review disagrees with committed previous dispositions")
    else:
        atomic_jsonl(ledger,sorted(reviews,key=lambda r:r["formulation_id"]))
    actual=jsonl(ledger);current_review={r["formulation_id"]:r for r in actual}
    if len(actual)!=541 or len(current_review)!=541:
        raise PipelineError("Missing screened individual mathematical reviews")
    for r in previous:
        if r["formulation_id"] not in target and current_review[r["formulation_id"]]!=r:
            raise PipelineError("Unrelated prior disposition modified")
    if {id for r in actual for id in r["relation_ids"]}!=set(current):
        raise PipelineError("Some link not individually reviewed")
    outcome=dict(Counter(r["decision"] for r in actual))
    if outcome!={"linked":531,"no_supported_target":10}:
        raise PipelineError("Unreviewed or invalid individual outcome "+str(outcome))
    result={
      "batch":82,"meanings":517,"reviewed_formulations":541,
      "screened_relations":706,"new_screened_links":1,
      "old_705_relationships_preserved":True,
      "all_537_prior_formulation_dispositions_preserved":True,
      "three_martingale_missing_foundation_decisions":True,
      "graph_chromatic_simple_graph_link_source_screened":True,
      "all_541_formulations_individually_reviewed":True,
      "dependency_graph_has_cycles":False,
      "all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Source filtration, stochastic process and conditional expectation prerequisites individually; register and rights-review MathWorld before chromatic-polynomial alternative. Continue broad source discovery."
    }
    atomic_json(w.root/"state/wave2_research82_links.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
