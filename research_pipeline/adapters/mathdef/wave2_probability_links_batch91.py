"""Batch 91: independently source-screen probability-space and random-variable prerequisites.

The stochastic process previously had an explicit no-supported-target review;
it is amended only with archived review evidence. Conditional expectation's
existing sigma-algebra prerequisite remains, with additive source-scoped links.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
PRE={"sources":14,"terms":425,"observations":862,"meanings":527}
PW="https://proofwiki.org/wiki/Definition%3A"
URLS={
 "measurable":PW+"Measurable_Space",
 "probability":PW+"Probability_Space",
 "variable":PW+"Random_Variable",
 "sigma":PW+"Sigma_Algebra",
 "process":PW+"Stochastic_Process/Formal_Definition",
 "expectation":PW+"Conditional_Expectation/General_Case/Sigma-Algebra"
}
STOCH="form.wave2.found85.stochastic-process"
COND="form.wave2.found85.conditional-expectation"
RELS=(
 ("01","form.wave2.prob90.measurable-space","meaning.wave2.foundation.sigma-algebra",
  "σ-algebra",URLS["measurable"],URLS["sigma"],
  "A measurable space consists of a set with a specified sigma-algebra on that set; the previously screened sigma-algebra meaning supplies precisely the collection of subsets required here, without presupposing a probability measure."),
 ("02","form.wave2.prob90.probability-space","meaning.wave2.prob90.measurable-space",
  "measurable space",URLS["probability"],URLS["measurable"],
  "A probability space is a measurable space equipped with a normalized countably additive measure. The independent measurable-space definition supplies the underlying pair of sample points and events without imposing normalization."),
 ("03","form.wave2.prob90.random-variable-general","meaning.wave2.prob90.probability-space",
  "probability space",URLS["variable"],URLS["probability"],
  "A measurable-space-valued random variable is defined on a probability space (Ω,F,P); the independent normalized probability triple is its exact domain probability structure, not itself a random variable."),
 ("04","form.wave2.prob90.random-variable-general","meaning.wave2.prob90.measurable-space",
  "measurable space",URLS["variable"],URLS["measurable"],
  "General random variables take values in a separately specified measurable codomain (S,SigmaS). Its sigma-algebra provides the target-measurability test. This is not necessarily a real-valued random variable."),
 ("05","form.wave2.prob90.random-variable-real","meaning.wave2.prob90.probability-space",
  "(Ω,F,P)",URLS["variable"],URLS["probability"],
  "A real-valued random variable on the triple (Ω,F,P) presupposes a probability-space domain; the independent probability-space meaning provides the normalized probability measure and event sigma-algebra."),
 ("06","form.wave2.prob90.random-variable-real","meaning.wave2.foundation.sigma-algebra",
  "Borel σ-algebra",URLS["variable"],URLS["sigma"],
  "A real random variable is measurable with respect to the Borel sigma-algebra of real numbers. The existing independent sigma-algebra meaning explains the ambient set system, while the specialized Borel construction remains a separately sourceable context."),
 ("07",STOCH,"meaning.wave2.prob90.probability-space",
  "probability space",URLS["process"],URLS["probability"],
  "An indexed family of measurable random variables is a stochastic process on a probability space. The newly independent probability-space definition supplies the ambient probability triple and does not depend on stochastic processes."),
 ("08",STOCH,"meaning.wave2.prob90.measurable-space",
  "measurable state space",URLS["process"],URLS["measurable"],
  "A stochastic process valued in (E,Ecal) requires a measurable state space, which is independently defined as a set equipped with a sigma-algebra. It is not necessarily real valued or continuous."),
 ("09",STOCH,"meaning.wave2.prob90.random-variable-general",
  "random variables",URLS["process"],URLS["variable"],
  "A stochastic process is an indexed family of random variables, not a single random variable or a martingale. The general measurable-codomain variable definition is the correct source-backed element concept."),
 ("10",COND,"meaning.wave2.prob90.probability-space",
  "(Ω,F,P)",URLS["expectation"],URLS["probability"],
  "Conditional expectation is defined for an integrable random variable on a probability-space triple. The independent probability-space meaning supplies that normalized measurable probability structure, independent of conditional expectation."),
 ("11",COND,"meaning.wave2.prob90.random-variable-real",
  "real random variable",URLS["expectation"],URLS["variable"],
  "A sigma-algebra-conditioned expectation is defined for an integrable real random variable X and produces another measurable integrable random variable Z. This is a noncircular prerequisite and does not claim the uniqueness theorem as part of the definition.")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    data="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=data:
        raise PipelineError("Previously source-reviewed relation audit differs")
    path.write_text(data,encoding="utf-8")
    return path
def form_url(f,obs):
    ids=f.get("evidence_ids",[])
    if len(ids)!=1 or ids[0] not in obs:
        raise PipelineError("Ambiguous or missing particular variant source")
    return obs[ids[0]]["locator"]
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*PRE,"relations")):
        raise PipelineError("Independent unsealed Wave 2 required")
    if {s:len(w.records(s)) for s in PRE}!=PRE:
        raise PipelineError("Historical source/meaning counts changed")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=551:
        raise PipelineError("Expected 551 source-screened mathematical formulations")
    oldlinks=w.records("relations")
    if len(oldlinks) not in (719,730):
        raise PipelineError("Concurrent relationship changes found")
    olderlinks={id:r for id,r in oldlinks.items() if not id.startswith("rel.wave2.prob91.")}
    if len(olderlinks)!=719:
        raise PipelineError("Historical 719 links changed")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prior=jsonl(ledger);oldreview={r["formulation_id"]:r for r in prior}
    if (len(prior)!=551 or len(oldreview)!=551
        or any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in prior)
        or {id for row in prior for id in row["relation_ids"]}!=set(oldlinks)):
        raise PipelineError("Historical individual meaning review ledger not complete")
    prepared=[]
    for number,fid,target,phrase,fromurl,targeturl,reason in RELS:
        if fid not in forms or target not in ms:
            raise PipelineError("Source or independent target missing for "+number)
        _,f=forms[fid]
        if (f["review_state"]!="screened" or form_url(f,obs)!=fromurl
            or locator(ms[target],obs)!=targeturl or phrase not in f["text"]
            or len(reason)<155):
            raise PipelineError("Mathematically unsupported exact-source prerequisite "+number)
        prepared.append({
          "id":"rel.wave2.prob91."+number,
          "from_formulation":fid,"target_meaning":target,
          "relation_type":"definition_uses","review_state":"screened",
          "source_phrase":phrase,"source_locator":fromurl,
          "target_locator":targeturl,"editorial_reason":reason,
          "reviewed_by":"assistant_independent_probability_prerequisite_screen_2026_10_20",
          "human_verified":False
        })
    projected={**olderlinks,**{r["id"]:r for r in prepared}}
    check_cycles(ms,projected)
    if len(prepared)!=11:
        raise PipelineError("Missing individually justified relationship")
    new={fid for fid in forms if fid.startswith("form.wave2.prob90.")}
    if len(new)!=4:
        raise PipelineError("Exactly four new individual mathematical forms required")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_551_before_prob91.jsonl"
    if len(oldlinks)==719:
        if any(oldreview[fid]["decision"]!="needs_review" or oldreview[fid]["relation_ids"] for fid in new):
            raise PipelineError("New mathematical definition has an unsnapshotted review")
        if (oldreview[STOCH]["decision"]!="no_supported_target" or oldreview[STOCH]["relation_ids"]
            or oldreview[COND]["decision"]!="linked"
            or oldreview[COND]["relation_ids"]!=["rel.wave2.found86.05"]):
            raise PipelineError("Existing stochastic or conditional-expectation reviewed links changed")
        original=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=original:
            raise PipelineError("Historical 551-review snapshot differs")
        archive.write_text(original,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_551_before_prob91.json",{
          "rows":551,"previous_screened_links":719,
          "sha256":hashlib.sha256(original.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
    past=jsonl(archive);past_by={r["formulation_id"]:r for r in past}
    if len(past)!=551 or len(past_by)!=551 or past_by[STOCH]["decision"]!="no_supported_target":
        raise PipelineError("Historical source review proof incomplete")
    amendment={
      "event_id":"prob91.stochastic-process-no-target-to-probability-random-variable-foundations",
      "formulation_id":STOCH,"earlier_review_digest":digest(past_by[STOCH]),
      "earlier_decision":"no_supported_target","new_decision":"linked",
      "previous_review_reason":past_by[STOCH]["editorial_reason"],
      "new_screened_link_ids":[r["id"] for r in prepared if r["from_formulation"]==STOCH],
      "reason":"Probability space, measurable state space and general random variables are now independent source-screened prerequisite meanings, making the previous missing-foundations disposition revisable without circular dependence.",
      "human_verified":False,"production_corpus_used":False
    }
    additive={
      "event_id":"prob91.conditional-expectation-append-probability-random-variable-links",
      "formulation_id":COND,"previous_review_digest":digest(past_by[COND]),
      "preserved_original_link_ids":past_by[COND]["relation_ids"],
      "additional_link_ids":[r["id"] for r in prepared if r["from_formulation"]==COND],
      "reason":"Retain the old sigma-algebra prerequisite and add independently sourced probability-space and real-valued-random-variable targets as source-specific additional links.",
      "human_verified":False,"production_corpus_used":False
    }
    if len(amendment["new_screened_link_ids"])!=3 or additive["preserved_original_link_ids"]!=["rel.wave2.found86.05"] or len(additive["additional_link_ids"])!=2:
        raise PipelineError("Amended review missing original or new independently sourced links")
    store(w.root/"events/stochastic_process_no_target_amendment_batch91.jsonl",[amendment])
    store(w.root/"events/conditional_expectation_link_extension_batch91.jsonl",[additive])
    store(w.root/"wave2/prob91_individual_screened_links.jsonl",prepared)
    file=store(w.root/"intake/prob91_links.jsonl",prepared)
    if len(oldlinks)==719:
        w.ingest("relations",file,batch_size=11)
    links=w.records("relations")
    if len(links)!=730 or any(links.get(r["id"])!=r for r in prepared):
        raise PipelineError("New precise sourced relationship records missing")
    check_cycles(ms,links)
    nextreviews=[]
    for row in past:
        r=dict(row);fid=r["formulation_id"]
        if fid in new|{STOCH,COND}:
            found=[edge["id"] for edge in prepared if edge["from_formulation"]==fid]
            if fid==COND:
                found=past_by[COND]["relation_ids"]+found
                r["link_extension_event_id"]=additive["event_id"]
                r["previous_review_digest"]=digest(past_by[COND])
            r["relation_ids"]=found
            if not found:
                raise PipelineError("No individual prerequisite coverage for "+fid)
            r["decision"]="linked"
            r["reviewed_by"]="assistant_independent_probability_prerequisite_screen_2026_10_20"
            r["source"]="independent_probability_and_measurable_space_links_batch91"
            r["editorial_reason"]="Exact individual source/target mathematical prerequisites screened and dependency graph acyclic; prior source links retained."
            if fid==STOCH:
                r["previous_review_digest"]=digest(past_by[STOCH])
                r["previous_wave2_decision"]="no_supported_target"
                r["override_event_id"]=amendment["event_id"]
        nextreviews.append(r)
    if len(oldlinks)==730:
        if {r["formulation_id"]:r for r in prior}!={r["formulation_id"]:r for r in nextreviews}:
            raise PipelineError("Repeated source-screened individual reviews differ")
    else:
        atomic_jsonl(ledger,sorted(nextreviews,key=lambda r:r["formulation_id"]))
    current=jsonl(ledger);idx={r["formulation_id"]:r for r in current}
    if len(current)!=551 or len(idx)!=551:
        raise PipelineError("Individual formulation review inventory incomplete")
    modified=new|{STOCH,COND}
    for fid,old in past_by.items():
        if fid not in modified and idx[fid]!=old:
            raise PipelineError("Historical unrelated formulation review changed")
    if {i for r in current for i in r["relation_ids"]}!=set(links):
        raise PipelineError("One or more source-reviewed links lack individual review")
    count=dict(Counter(r["decision"] for r in current))
    if count!={"linked":544,"no_supported_target":7}:
        raise PipelineError("Unexpected individual review dispositions "+str(count))
    report={
      "batch":91,"screened_meanings":527,"reviewed_formulations":551,
      "screened_relationships":730,"new_links":11,
      "historical_719_links_preserved":True,
      "previous_545_unrelated_formulation_reviews_preserved":True,
      "stochastic_process_previous_no_target_amended_explicitly":True,
      "conditional_expectation_old_sigma_link_retained_and_extended":True,
      "all_551_formulations_reviewed":True,"graph_acyclic":True,
      "human_peer_verified":False,"production_corpus_used":False,"all_stages_unsealed":True,
      "next":"Review right and unitary module variants and continue breadth-first independently sourced discovery; no duplicate left module."
    }
    atomic_json(w.root/"state/wave2_prob91_links.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path(ROOT))
    p.add_argument("--workspace-path",type=Path,default=None)
    a=p.parse_args()
    print(json.dumps(run(a.workspace_path or a.workspace),indent=2))
if __name__=="__main__":main()
