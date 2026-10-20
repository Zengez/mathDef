"""Batch 86: mathematically review thirteen source-supported prerequisite links.

Historical missing-target martingale decisions are amended ONLY with archived
old review digests. A stochastic-process primitive remains explicitly
no-supported-target, with no fabricated probability-space prerequisites.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BEFORE={"sources":14,"terms":422,"observations":858,"meanings":523}
PW="https://proofwiki.org/wiki/Definition%3A"
FIL=PW+"Filtration_of_Sigma-Algebra/Discrete_Time"
AD=PW+"Adapted_Stochastic_Process"
COND=PW+"Conditional_Expectation/General_Case/Sigma-Algebra"
COL=PW+"Proper_Vertex_Coloring"
PROC=PW+"Stochastic_Process/Formal_Definition"
SIGMA=PW+"Sigma_Algebra"
SIMPLE=PW+"Simple_Graph"
MARTD=PW+"Martingale/Discrete_Time"
MARTC=PW+"Martingale"
CHROM=PW+"Chromatic_Number"
E=(
 ("01","form.wave2.found85.discrete-filtration","meaning.wave2.foundation.sigma-algebra","sub-σ-algebras",FIL,SIGMA,
  "A filtration consists of an increasing family of sub-sigma-algebras of the ambient measurable space. The independently sourced sigma-algebra meaning establishes the collection of measurable sets in each filtration layer; this does not assume a probability measure or continuous time."),
 ("02","form.wave2.found85.adapted-discrete","meaning.wave2.found85.stochastic-process","real-valued process",AD,PROC,
  "A discrete-time adapted process starts with a family of real-valued random variables indexed by nonnegative integers, a particular stochastic process. The independently screened stochastic-process meaning defines that indexed family without requiring adaptedness or a martingale identity."),
 ("03","form.wave2.found85.adapted-discrete","meaning.wave2.found85.discrete-filtration","filtration",AD,FIL,
  "The discrete adaptedness condition compares X_n with sigma-algebra F_n at each integer time. The independently sourced discrete filtration gives the correct increasing collection of information sets; this link does not assert all adapted processes are martingales."),
 ("04","form.wave2.found85.adapted-continuous","meaning.wave2.found85.stochastic-process","real-valued process",AD,PROC,
  "A real-time indexed adapted process is a stochastic process with a real time parameter. The independently screened general stochastic-process meaning permits arbitrary index sets, including nonnegative reals. No link is made to discrete filtration, whose source domain is the integers."),
 ("05","form.wave2.found85.conditional-expectation","meaning.wave2.foundation.sigma-algebra","sub-σ-algebra",COND,SIGMA,
  "Conditional expectation conditioned on G requires G to be a sub-sigma-algebra of the probability-space sigma-algebra. The independent sigma-algebra definition is precisely the structural collection of sets; uniqueness of a conditional-expectation version remains a separate theorem."),
 ("06","form.wave2.found85.proper-coloring","meaning.wave2.graph42.simple-undirected","simple graph",COL,SIMPLE,
  "The proper vertex k-coloring definition starts with the vertex and edge sets of a simple graph. The existing independent simple-graph meaning supplies a loopless undirected edge relation on distinct vertices, making adjacency and unequal endpoint colors well-defined."),
 ("07","form.wave2.research81.martingale-discrete.01","meaning.wave2.found85.adapted-discrete","adapted",MARTD,AD,
  "The adjacent-time martingale criterion explicitly assumes a discrete-time process adapted to its filtration. The separately screened discrete adapted-process meaning supplies exactly the measurability hypothesis, without itself requiring conditional expectation identities."),
 ("08","form.wave2.research81.martingale-discrete.01","meaning.wave2.found85.conditional-expectation","E[X_{n+1}|F_n]",MARTD,COND,
  "The one-step martingale identity is a conditional-expectation equality almost surely, given the current sigma-algebra. The independently defined conditional-expectation version supplies the object E[X_{n+1}|F_n], distinct from ordinary unconditional expectation."),
 ("09","form.wave2.research81.martingale-discrete.02","meaning.wave2.found85.adapted-discrete","adapted",MARTD,AD,
  "The all-later-times discrete martingale characterization assumes adaptedness to an integer-indexed filtration. This source-scoped target supplies the relevant measurability prerequisite, not the continuous-time adaptation convention."),
 ("10","form.wave2.research81.martingale-discrete.02","meaning.wave2.found85.conditional-expectation","E[X_m|F_n]",MARTD,COND,
  "The all-later-times martingale identity compares a future random variable with its conditional expectation given the earlier information sigma-algebra. The separately sourced conditional-expectation definition explains this operator, while the tower-property equivalence remains a theorem."),
 ("11","form.wave2.research81.martingale-continuous-index.01","meaning.wave2.found85.adapted-continuous","adapted",MARTC,AD,
  "The continuous-time-indexed martingale presupposes adaptedness for every real time t≥0. The independently screened continuous-index adaptedness meaning matches this index set; a discrete filtration is not substituted for the real-time one."),
 ("12","form.wave2.research81.martingale-continuous-index.01","meaning.wave2.found85.conditional-expectation","E[X_t|F_s]",MARTC,COND,
  "For any real s≤t, the martingale equation compares X_s with the conditional expectation of X_t given F_s. The general sigma-algebra-conditioned expectation definition applies regardless of whether the time indices are integers or real numbers."),
 ("13","form.wave2.research81.chromatic-proper-coloring.01","meaning.wave2.found85.proper-coloring","c:V(G)→{1,…,k}",CHROM,COL,
  "The chromatic number minimizes the palette size k over all proper vertex k-colorings of a fixed graph. The independently sourced proper-coloring meaning supplies the exact vertex-map and adjacent-endpoint inequality, and the existing graph prerequisite remains preserved.")
)
OLD=(
 "form.wave2.research81.martingale-discrete.01",
 "form.wave2.research81.martingale-discrete.02",
 "form.wave2.research81.martingale-continuous-index.01"
)
MISSING={
 "formulation_id":"form.wave2.found85.stochastic-process",
 "decision":"no_supported_target","source_locator":PROC,
 "reason":"The independently sourced general stochastic-process definition presupposes an underlying probability space and a measurable state space as well as measurable random variables. The current independent catalog has a sigma-algebra but no separately screened complete probability-space or general measurable-space object that matches either of those full prerequisite meanings. Links to adapted stochastic processes or martingales would reverse the foundations; no such link is created.",
 "missing":["probability space","measurable state space","measurable random variable"],
 "human_verified":False
}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Previous individual mathematical link screening altered")
    path.write_text(content,encoding="utf-8")
    return path
def exact_source(f,obs):
    ids=f.get("evidence_ids",[])
    if len(ids)!=1 or ids[0] not in obs:
        raise PipelineError("Source-scoped formulation evidence missing")
    return obs[ids[0]]["locator"]
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BEFORE,"relations")):
        raise PipelineError("Only independent unsealed Wave 2")
    if {s:len(w.records(s)) for s in BEFORE}!=BEFORE:
        raise PipelineError("Unexpected independent source/meaning inventory")
    meanings=w.records("meanings");obs=w.records("observations")
    byform={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
    if len(byform)!=547:
        raise PipelineError("Expected 547 mathematically screened formulations")
    original_current=w.records("relations")
    if len(original_current) not in (706,719):
        raise PipelineError("Unexpected previous relationship inventory")
    preserved={k:v for k,v in original_current.items() if not k.startswith("rel.wave2.found86.")}
    if len(preserved)!=706:
        raise PipelineError("Historical 706 links not all preserved")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    previous=jsonl(ledger)
    before={r["formulation_id"]:r for r in previous}
    if len(previous)!=547 or len(before)!=547 or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in previous):
        raise PipelineError("Historical 547-formulation review ledger stale")
    if {i for r in previous for i in r["relation_ids"]}!=set(original_current):
        raise PipelineError("Previously screened relation lacks review")
    screened=[]
    for num,fid,target,phrase,fromurl,targeturl,reason in E:
        if fid not in byform or target not in meanings:
            raise PipelineError("Independent source/target missing: "+num)
        meaning,form=byform[fid]
        if (form["review_state"]!="screened" or exact_source(form,obs)!=fromurl
            or locator(meanings[target],obs)!=targeturl or phrase not in form["text"]
            or len(reason)<175):
            raise PipelineError("Source-scoped mathematical dependency not justified: "+num)
        screened.append({
          "id":"rel.wave2.found86."+num,
          "from_formulation":fid,"target_meaning":target,
          "relation_type":"definition_uses","review_state":"screened",
          "source_phrase":phrase,"source_locator":fromurl,
          "target_locator":targeturl,"editorial_reason":reason,
          "reviewed_by":"assistant_independent_martingale_graph_foundation_links_2026_10_20",
          "human_verified":False
        })
    if len(screened)!=13:
        raise PipelineError("Expected 13 individually verified mathematics links")
    graph={**preserved,**{r["id"]:r for r in screened}}
    check_cycles(meanings,graph)
    changed={id for id in byform if id.startswith("form.wave2.found85.")}
    if len(changed)!=6 or len(OLD)!=3:
        raise PipelineError("Unexpected new foundation formulation count")
    if MISSING["formulation_id"] not in changed:
        raise PipelineError("Missing primitive no-target review subject")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_547_before_found86.jsonl"
    if len(original_current)==706:
        if any(before[f]["decision"]!="needs_review" or before[f]["relation_ids"] for f in changed):
            raise PipelineError("New mathematical forms were already reviewed")
        if any(before[f]["decision"]!="no_supported_target" or before[f]["relation_ids"] for f in OLD):
            raise PipelineError("Historic martingale missing-target decisions changed without event")
        text=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=text:
            raise PipelineError("Previous 547-review historical snapshot changed")
        archive.write_text(text,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_547_before_found86.json",{
          "rows":547,"reviewed_links":706,
          "sha256":hashlib.sha256(text.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
    historic=jsonl(archive)
    history={r["formulation_id"]:r for r in historic}
    if len(historic)!=547 or len(history)!=547 or any(history[f]["decision"]!="no_supported_target" for f in OLD):
        raise PipelineError("Historical missing-target review evidence lost")
    amendments=[]
    for f in OLD:
        amendments.append({
          "event_id":"found86.no-target-to-sourced-probability-prereqs."+f,
          "formulation_id":f,"previous_review_digest":digest(history[f]),
          "previous_decision":"no_supported_target","new_decision":"linked",
          "earlier_reason":history[f]["editorial_reason"],
          "screened_supporting_link_ids":[r["id"] for r in screened if r["from_formulation"]==f],
          "reason":"Independently source-screened time-matched adaptedness and conditional expectation now support the martingale formulation without a circular edge.",
          "human_verified":False,"production_corpus_used":False
        })
    if any(len(e["screened_supporting_link_ids"])!=2 for e in amendments):
        raise PipelineError("Each historical martingale formulation needs two newly verified sources")
    store(w.root/"events/martingale_review_amendments_batch86.jsonl",amendments)
    store(w.root/"wave2/individual_martingale_graph_links_batch86.jsonl",screened)
    store(w.root/"wave2/stochastic_process_no_target_batch86.jsonl",[MISSING])
    input=store(w.root/"intake/found86_links.jsonl",screened)
    if len(original_current)==706:
        w.ingest("relations",input,batch_size=13)
    current=w.records("relations")
    if len(current)!=719 or any(current.get(r["id"])!=r for r in screened):
        raise PipelineError("Screened source-specific graph not committed")
    check_cycles(meanings,current)
    future=[]
    for row in historic:
        r=dict(row);fid=r["formulation_id"]
        if fid in changed|set(OLD):
            attached=[item["id"] for item in screened if item["from_formulation"]==fid]
            r["relation_ids"]=attached
            r["reviewed_by"]="assistant_independent_martingale_graph_foundation_links_2026_10_20"
            if attached:
                r["decision"]="linked"
                r["source"]="independent_probability_graph_prerequisite_review_batch86"
                r["editorial_reason"]="Individually source-linked prerequisite screened, with time-index consistency and an acyclic graph."
            else:
                if fid!=MISSING["formulation_id"]:
                    raise PipelineError("Unreviewed source-screened formulation "+fid)
                r["decision"]="no_supported_target"
                r["source"]="independent_stochastic_process_missing_prob_space_review_batch86"
                r["editorial_reason"]=MISSING["reason"]
            if fid in OLD:
                r["previous_review_digest"]=digest(history[fid])
                r["previous_wave2_decision"]="no_supported_target"
                r["override_event_id"]=next(e["event_id"] for e in amendments if e["formulation_id"]==fid)
        future.append(r)
    if len(original_current)==719:
        if {r["formulation_id"]:r for r in future}!={r["formulation_id"]:r for r in previous}:
            raise PipelineError("Re-run differs from committed screened decisions")
    else:
        atomic_jsonl(ledger,sorted(future,key=lambda r:r["formulation_id"]))
    actual=jsonl(ledger);index={r["formulation_id"]:r for r in actual}
    if len(actual)!=547 or len(index)!=547:
        raise PipelineError("Incomplete individual mathematical review")
    for fid,old in history.items():
        if fid not in changed|set(OLD) and index[fid]!=old:
            raise PipelineError("Historical unrelated formulation review changed")
    if {i for r in actual for i in r["relation_ids"]}!=set(current):
        raise PipelineError("Every screened link must have an individual review")
    counts=dict(Counter(r["decision"] for r in actual))
    if counts!={"linked":539,"no_supported_target":8}:
        raise PipelineError("Unreviewed or unexpected disposition "+str(counts))
    report={
      "batch":86,"screened_meanings":523,"reviewed_formulations":547,
      "screened_relationships":719,"new_screened_relationships":13,
      "historical_706_links_preserved":True,
      "unrelated_538_formulation_reviews_preserved":True,
      "three_martingale_no_target_decisions_explicitly_amended":True,
      "new_stochastic_process_missing_prerequisite_explicit":True,
      "discrete_vs_continuous_adaptedness_respected":True,
      "all_formulations_individually_reviewed":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "production_corpus_used":False,"human_peer_verified":False,
      "next":"Independently source probability and measurable space foundations before reexamining stochastic process no-target; resume broad rotating subfield discovery."
    }
    atomic_json(w.root/"state/wave2_found86_links.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
