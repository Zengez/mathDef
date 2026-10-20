"""Batch 85: screen six source-scoped contextual meanings from five terms.

Discrete/continuous adapted processes are separate contexts sharing one term
group. Existence and uniqueness of conditional expectation are theorems,
not part of its defining integral criterion. No original corpus is read.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
RESEARCH="wave2/martingale_graph_foundation_research_batch83_2026-10-20.jsonl"
BEFORE={"sources":14,"terms":422,"observations":858,"meanings":517,"relations":706}
AFTER=dict(BEFORE,meanings=523)
SPECS=(
 ("discrete-filtration",1,"discrete-filtration","Discrete time: increasing sub-sigma-algebras indexed by n≥0"),
 ("adapted-stochastic-process",1,"adapted-discrete","Discrete-time stochastic process adapted to a filtration indexed by n≥0"),
 ("adapted-stochastic-process",2,"adapted-continuous","Real-time indexed stochastic process adapted to a filtration indexed by t≥0"),
 ("conditional-expectation-sub-sigma",1,"conditional-expectation","Conditional expectation with respect to a sub-sigma-algebra"),
 ("proper-vertex-coloring",1,"proper-coloring","Proper vertex coloring of a simple undirected graph"),
 ("stochastic-process",1,"stochastic-process","General measurable-state-valued stochastic process indexed by a set")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Previously individually screened candidate differs")
    path.write_text(body,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Unsealed independent Wave 2 required")
    if {s:len(w.records(s)) for s in BEFORE} not in (BEFORE,AFTER):
        raise PipelineError("Unexpected source or mathematical meaning counts")
    source={r["key"]:r for r in jsonl(w.root/RESEARCH)}
    if len(source)!=5 or {key for key,_,_,_ in SPECS}!=set(source):
        raise PipelineError("Five mathematically source-reviewed terms required")
    terms=w.records("terms");observations=w.records("observations")
    additions=[];individual=[]
    for key,index,suffix,context in SPECS:
        r=source[key]
        tid="term.wave2.found84."+key
        oid=f"obs.wave2.found84.{key}.{index:02d}"
        m_id="meaning.wave2.found85."+suffix
        f_id="form.wave2.found85."+suffix
        o=observations.get(oid)
        if (r["production_corpus_used"] or not r["source_reviewed"] or
            not r["source_research_complete"] or not r["not_yet_meaning_screened"]
            or tid not in terms or o is None
            or o["term_id"]!=tid or o["locator"]!=r["url"]
            or o["source_id"]!="src.proofwiki"
            or index>len(r["forms"]) or len(r["mathematical_review"])<210):
            raise PipelineError("Independent source screening missing for "+suffix)
        raw=r["forms"][index-1]["text"]
        if key=="conditional-expectation-sub-sigma":
            suffix_theorem=" It is unique up to almost-sure equality."
            if not raw.endswith(suffix_theorem):
                raise PipelineError("Expected to separate conditional-expectation theorem statement from definition")
            raw=raw[:-len(suffix_theorem)]
        justification=r["mathematical_review"]
        if key=="conditional-expectation-sub-sigma":
            justification+=" The essential uniqueness statement is separately a theorem, intentionally omitted from the displayed definition."
        if key=="adapted-stochastic-process":
            justification+=" Discrete and real-time indexing are independently labeled contextual meanings under one shared term group."
        form={
          "id":f_id,"text":raw,"evidence_ids":[oid],
          "review_state":"screened","human_verified":False,
          "mathematical_review_reason":justification,
          "source_screened_by":"assistant_independent_martingale_foundations_batch85_2026_10_20"
        }
        grp="wave2.found85.adapted-stochastic-process" if key=="adapted-stochastic-process" else "wave2.found85."+key
        additions.append({
          "id":m_id,"term_group_id":grp,"display_term":r["term"],
          "context":context,"term_ids":[tid],"formulations":[form],
          "editorial_status":"individually_source_and_mathematically_screened",
          "editorial_screening_reason":justification,"human_verified":False
        })
        individual.append({
          "review_id":"review.wave2.found85."+suffix,
          "meaning_id":m_id,"formulation_id":f_id,
          "source_observation_id":oid,"source_locator":r["url"],
          "mathematical_reason":justification,
          "decision":"mathematically_screened_pending_independent_link_review",
          "human_verified":False,"production_corpus_used":False
        })
    if len(additions)!=6 or len(individual)!=6 or len({r["id"] for r in additions})!=6:
        raise PipelineError("Six individual time/context variants required")
    store(w.root/"wave2/found85_individual_meaning_reviews.jsonl",individual)
    file=store(w.root/"intake/found85_meanings.jsonl",additions)
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prev=jsonl(ledger)
    before=w.records("meanings")
    if len(prev) not in (541,547) or len({r["formulation_id"] for r in prev})!=len(prev):
        raise PipelineError("Historical 541 formulation-review inventory missing")
    if {id for r in prev for id in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Historical link reviews do not cover the graph")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_541_before_found85.jsonl"
    if len(before)==517:
        if len(prev)!=541 or any(r["meaning_catalog_digest"]!=digest(list(before.values())) for r in prev):
            raise PipelineError("Historic meaning catalog digest mismatch")
        old=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=old:
            raise PipelineError("Previously archived 541-review lineage changed")
        archive.write_text(old,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_541_before_found85.json",{
          "rows":541,"reviewed_links":706,
          "sha256":hashlib.sha256(old.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
        w.ingest("meanings",file,batch_size=6)
    ms=w.records("meanings")
    if len(ms)!=523 or any(ms.get(r["id"])!=r for r in additions):
        raise PipelineError("Individually screened new meaning batch missing or changed")
    history=jsonl(archive)
    if len(history)!=541 or len({r["formulation_id"] for r in history})!=541:
        raise PipelineError("Historical review archive not complete")
    current_digest=digest(list(ms.values()))
    next_rows=[dict(r,meaning_catalog_digest=current_digest) for r in history]
    for x in individual:
        next_rows.append({
          "formulation_id":x["formulation_id"],"meaning_id":x["meaning_id"],
          "meaning_catalog_digest":current_digest,"decision":"needs_review",
          "relation_ids":[],"original_wave1_disposition":None,
          "source":"independent_martingale_and_graph_foundations_screen_batch85",
          "editorial_reason":"Individually source-screened meaning; exact noncircular prerequisites pending separate review.",
          "reviewed_by":None,"human_verified":False
        })
    if len(prev)==547:
        if {r["formulation_id"]:r for r in prev}!={r["formulation_id"]:r for r in next_rows}:
            raise PipelineError("Previously run Batch 85 differs from historical reviews")
    else:
        atomic_jsonl(ledger,sorted(next_rows,key=lambda r:r["formulation_id"]))
    reviewed=jsonl(ledger);by={r["formulation_id"]:r for r in reviewed}
    if len(reviewed)!=547 or len(by)!=547:
        raise PipelineError("Not all 547 formulations represented")
    for r in history:
        current=by[r["formulation_id"]]
        if any(current.get(k)!=v for k,v in r.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Historical individual reviewed formulation disposition changed")
    if {id for r in reviewed for id in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Historical 706 relations not all reviewed")
    check_cycles(ms,w.records("relations"))
    if dict(Counter(r["decision"] for r in reviewed))!={"linked":531,"no_supported_target":10,"needs_review":6}:
        raise PipelineError("Expected six pending prerequisite reviews")
    state=w.state("meanings")
    state.update(total=523,record_digest=current_digest,screened_new_formulations=116,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    result={
      "batch":85,"screened_meanings":523,"reviewed_formulations":547,
      "new_contextual_meanings":6,"new_formulations":6,
      "adapted_discrete_and_continuous_separate_contexts":True,
      "conditional_expectation_uniqueness_separated_as_theorem":True,
      "prior_541_formulation_decisions_preserved":True,
      "prior_706_screened_relations_preserved":True,
      "pending_prerequisite_reviews":6,
      "original_production_mathdef_content_used":False,"human_peer_verified":False,
      "all_stages_unsealed":True,
      "next":"Screen links to existing σ-algebra and graph, and explicitly amend historically justified martingale/coloring no-targets only after exact source/target verification."
    }
    atomic_json(w.root/"state/wave2_found85_meaning_screen.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    args=p.parse_args()
    print(json.dumps(run(args.workspace),indent=2))
if __name__=="__main__":main()
