"""Batch 90: mathematical screening for four probability/measure contexts.

General and real-valued random variables are distinct meanings under the same
term heading, avoiding a false equivalence of codomain scope.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/probability_and_module_foundations_research_batch87_2026-10-20.jsonl"
BASE={"sources":14,"terms":425,"observations":862,"meanings":523,"relations":719}
AFTER=dict(BASE,meanings=527)
SPECS=(
 ("measurable-space",1,"measurable-space","A set equipped with a sigma-algebra, no measure required"),
 ("probability-space",1,"probability-space","Normalized measure space with total mass one"),
 ("random-variable",1,"random-variable-general","Random variable with values in an arbitrary measurable space"),
 ("random-variable",2,"random-variable-real","Real-valued random variable with Borel-measurable codomain")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    text="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=text:
        raise PipelineError("Historical individual review changed")
    path.write_text(text,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BASE):
        raise PipelineError("Independent unsealed Wave 2 required")
    if {s:len(w.records(s)) for s in BASE} not in (BASE,AFTER):
        raise PipelineError("Unexpected sourced independent meaning inventory")
    sources={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if len(sources)!=4 or "module" not in sources:
        raise PipelineError("Previous source research/collision audit missing")
    t=w.records("terms");obs=w.records("observations")
    additions=[];reviews=[]
    for key,i,suffix,context in SPECS:
        r=sources[key]
        tid="term.wave2.prob89."+key
        oid=f"obs.wave2.prob89.{key}.{i:02d}"
        mid="meaning.wave2.prob90."+suffix
        fid="form.wave2.prob90."+suffix
        o=obs.get(oid)
        if (tid not in t or not o or o["term_id"]!=tid or
            o["locator"]!=r["source_locator"] or
            o["source_id"]!="src.proofwiki" or
            r["stage_ingested"] or r["production_corpus_consulted"] or
            len(r["mathematical_review"])<230 or i>len(r["variants"])):
            raise PipelineError("Mathematical formulation not individually sourced "+suffix)
        text=r["variants"][i-1]["text"]
        reason=r["mathematical_review"]
        if key=="random-variable":
            reason+=" A random variable with general measurable target and a real-valued random variable have genuinely different codomain constraints; record as distinct contextual meanings in one displayed term group."
        form={
          "id":fid,"text":text,"evidence_ids":[oid],
          "review_state":"screened","human_verified":False,
          "mathematical_review_reason":reason,
          "source_screened_by":"assistant_independent_probability_meanings_batch90_2026_10_20"
        }
        group="wave2.prob90.random-variable" if key=="random-variable" else "wave2.prob90."+key
        additions.append({
          "id":mid,"term_group_id":group,"display_term":r["term"],
          "context":context,"term_ids":[tid],"formulations":[form],
          "editorial_status":"individually_source_and_mathematically_screened",
          "editorial_screening_reason":reason,"human_verified":False
        })
        reviews.append({
          "review_id":"review.wave2.prob90."+suffix,
          "meaning_id":mid,"formulation_id":fid,
          "source_observation_id":oid,"source_locator":r["source_locator"],
          "mathematical_reason":reason,
          "decision":"individually_source_screened_pending_link_review",
          "human_verified":False,"production_corpus_used":False
        })
    if len(additions)!=4 or len(reviews)!=4:
        raise PipelineError("Missing independent contextual variants")
    store(w.root/"wave2/prob90_individual_formulation_reviews.jsonl",reviews)
    intake=store(w.root/"intake/prob90_meanings.jsonl",additions)
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prev=jsonl(ledger);old=w.records("meanings")
    if len(prev) not in (547,551) or len({r["formulation_id"] for r in prev})!=len(prev):
        raise PipelineError("Historical 547 review decisions incomplete")
    if {i for r in prev for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Historical 719 screened links not all reviewed")
    snap=w.root/"state/wave2_formulation_reviews_snapshot_547_before_prob90.jsonl"
    if len(old)==523:
        if len(prev)!=547 or any(r["meaning_catalog_digest"]!=digest(list(old.values())) for r in prev):
            raise PipelineError("Prior screened meaning catalog digest differs")
        older=ledger.read_text(encoding="utf-8")
        if snap.exists() and snap.read_text(encoding="utf-8")!=older:
            raise PipelineError("Previous 547-review archive differs")
        snap.write_text(older,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_547_before_prob90.json",{
          "rows":547,"screened_relations":719,
          "sha256":hashlib.sha256(older.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
        w.ingest("meanings",intake,batch_size=4)
    ms=w.records("meanings")
    if len(ms)!=527 or any(ms.get(r["id"])!=r for r in additions):
        raise PipelineError("Screened four contextual meanings incomplete")
    historical=jsonl(snap)
    if len(historical)!=547 or len({r["formulation_id"] for r in historical})!=547:
        raise PipelineError("Complete earlier formulation review snapshot lost")
    d=digest(list(ms.values()))
    current=[dict(r,meaning_catalog_digest=d) for r in historical]
    for r in reviews:
        current.append({
          "formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
          "meaning_catalog_digest":d,"decision":"needs_review",
          "relation_ids":[],"original_wave1_disposition":None,
          "source":"independent_probability_context_math_screen_batch90",
          "editorial_reason":"Individually source-screened mathematical object definition; prerequisites separately pending.",
          "reviewed_by":None,"human_verified":False
        })
    if len(prev)==551:
        if {r["formulation_id"]:r for r in prev}!={r["formulation_id"]:r for r in current}:
            raise PipelineError("Previous Batch90 screened review changed")
    else:
        atomic_jsonl(ledger,sorted(current,key=lambda r:r["formulation_id"]))
    result=jsonl(ledger);byid={r["formulation_id"]:r for r in result}
    if len(result)!=551 or len(byid)!=551:
        raise PipelineError("551 individual mathematical dispositions incomplete")
    for prior in historical:
        updated=byid[prior["formulation_id"]]
        if any(updated.get(k)!=v for k,v in prior.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Historical reviewed formulation changed")
    if {i for r in result for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Previously reviewed screened link lost")
    check_cycles(ms,w.records("relations"))
    if dict(Counter(r["decision"] for r in result))!={"linked":539,"no_supported_target":8,"needs_review":4}:
        raise PipelineError("Unexpected formulation dispositions")
    state=w.state("meanings")
    state.update(total=527,record_digest=d,screened_new_formulations=120,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
      "batch":90,"screened_meanings":527,"reviewed_formulations":551,
      "new_meanings":4,"new_formulations":4,
      "random_variable_general_and_real_distinct_contexts":True,
      "old_547_formulation_dispositions_preserved":True,
      "old_719_screened_links_preserved":True,
      "module_existing_left_meaning_preserved":True,
      "new_prerequisite_reviews_pending":4,
      "human_peer_verified":False,"production_corpus_used":False,"all_stages_unsealed":True,
      "next":"Screen source-scoped prerequisites and explicitly amend stochastic-process missing-target decision without deleting prior evidence."
    }
    atomic_json(w.root/"state/wave2_prob90_meaning_screen.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
