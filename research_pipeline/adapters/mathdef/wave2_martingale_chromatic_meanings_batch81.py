"""Batch 81 independently screens two martingale contexts and graph coloring.

Four individually sourced formulations, three meanings, no original
production mathematical content or reverse lookup of original definitions.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
RESEARCH="wave2/source_variant_screen_batch79_2026-10-20.jsonl"
PRE={"sources":14,"terms":417,"observations":852,"meanings":514,"relations":705}
POST=dict(PRE,meanings=517)
KEYS=("martingale-discrete","martingale-continuous-index","chromatic-proper-coloring")
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    text="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=text:
        raise PipelineError("Individual mathematical review data changed")
    path.write_text(text,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in PRE):
        raise PipelineError("Only independent unsealed Wave 2")
    if {s:len(w.records(s)) for s in PRE} not in (PRE,POST):
        raise PipelineError("Unexpected source meaning baseline")
    researched={r["key"]:r for r in jsonl(w.root/RESEARCH)}
    if set(researched)!=set(KEYS):
        raise PipelineError("Three prior independent research dossiers required")
    terms=w.records("terms");obs=w.records("observations")
    additions=[];individual=[]
    for key in KEYS:
        r=researched[key]
        tid="term.wave2.research80."+key
        mid="meaning.wave2.research81."+key
        if (tid not in terms or r["stage_ingested"] or r["production_corpus_used"]
            or not r["source_ready"] or len(r["reason"])<290):
            raise PipelineError("Mathematical source audit missing "+key)
        forms=[]
        for i,f in enumerate(r["forms"],1):
            oid=f"obs.wave2.research80.{key}.{i:02d}"
            o=obs.get(oid)
            if not o or o["term_id"]!=tid or o["locator"]!=r["url"]:
                raise PipelineError("Cannot trace mathematical formulation to source "+oid)
            fid=f"form.wave2.research81.{key}.{i:02d}"
            forms.append({
              "id":fid,"text":f["text"],"evidence_ids":[oid],
              "review_state":"screened",
              "human_verified":False,
              "mathematical_review_reason":r["reason"]+" Source section: "+f["section"],
              "source_screened_by":"assistant_independent_probability_combinatorics_screen_batch81_2026_10_20"
            })
            individual.append({
               "review_id":"review.wave2.research81."+fid,
               "meaning_id":mid,"formulation_id":fid,"source_observation_id":oid,
               "source_locator":r["url"],
               "mathematical_reason":r["reason"]+" Definition context: "+f["variant"],
               "decision":"source_screened_meaning_pending_prerequisite_review",
               "human_verified":False,"production_corpus_used":False
            })
        additions.append({
          "id":mid,
          "term_group_id":"wave2.research81.martingale" if key.startswith("martingale") else "wave2.research81.chromatic-number",
          "display_term":r["term"],"context":r["context"],
          "term_ids":[tid],"formulations":forms,
          "editorial_status":"independent_context_and_source_screened",
          "editorial_screening_reason":r["reason"],
          "human_verified":False
        })
    if len(additions)!=3 or len(individual)!=4:
        raise PipelineError("Missing one of four independently sourced formulations")
    store(w.root/"wave2/research81_individual_formulation_screening.jsonl",individual)
    intake=store(w.root/"intake/research81_meanings.jsonl",additions)
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prev=jsonl(ledger)
    meanings=w.records("meanings")
    if len(prev) not in (537,541) or len({r["formulation_id"] for r in prev})!=len(prev):
        raise PipelineError("Historical formulation review inventory incomplete")
    if {rid for r in prev for rid in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Historical source-screened relations not reviewed")
    snapshot=w.root/"state/wave2_formulation_reviews_snapshot_537_before_research81.jsonl"
    if len(meanings)==514:
        if len(prev)!=537 or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in prev):
            raise PipelineError("Previous screened meaning digest stale")
        txt=ledger.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=txt:
            raise PipelineError("Historic review snapshot mismatch")
        snapshot.write_text(txt,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_537_before_research81.json",{
           "rows":537,"screened_links":705,
           "sha256":hashlib.sha256(txt.encode("utf-8")).hexdigest(),
           "human_peer_verified":False
        })
        w.ingest("meanings",intake,batch_size=3)
    current_meanings=w.records("meanings")
    if len(current_meanings)!=517 or any(current_meanings.get(r["id"])!=r for r in additions):
        raise PipelineError("New meaning ingestion differs from individually screened records")
    historic=jsonl(snapshot)
    if len(historic)!=537 or len({r["formulation_id"] for r in historic})!=537:
        raise PipelineError("Missing 537 prior review rows")
    h=digest(list(current_meanings.values()))
    updated=[dict(r,meaning_catalog_digest=h) for r in historic]
    for r in individual:
        updated.append({
          "formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
          "meaning_catalog_digest":h,"decision":"needs_review",
          "relation_ids":[],"original_wave1_disposition":None,
          "source":"independent_probability_combinatorics_review_batch81",
          "editorial_reason":"Individually source and mathematically screened definition; exact prerequisite review pending.",
          "reviewed_by":None,"human_verified":False
        })
    if len(prev)==541:
        index={r["formulation_id"]:r for r in prev}
        if index!={r["formulation_id"]:r for r in updated}:
            raise PipelineError("Repeated batch differs from previously recorded individual reviews")
    else:
        atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
    latest=jsonl(ledger);idx={r["formulation_id"]:r for r in latest}
    if len(latest)!=541 or len(idx)!=541:
        raise PipelineError("Missing individual reviews for new formulations")
    for old in historic:
        new=idx[old["formulation_id"]]
        if any(new.get(k)!=v for k,v in old.items() if k!="meaning_catalog_digest"):
            raise PipelineError("A historical unrelated review changed")
    if {i for row in latest for i in row["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Historical definition link review changed")
    check_cycles(current_meanings,w.records("relations"))
    if dict(Counter(r["decision"] for r in latest))!={"linked":530,"no_supported_target":7,"needs_review":4}:
        raise PipelineError("Unexpected pending/historic review dispositions")
    state=w.state("meanings")
    state.update(total=517,record_digest=h,screened_new_formulations=110,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
       "batch":81,"screened_meanings":517,"reviewed_formulations":541,
       "new_contextual_meanings":3,"new_individually_screened_formulations":4,
       "two_martingale_time_contexts_one_display_group":True,
       "graph_nonempty_finite_simple_scope":True,
       "chromatic_polynomial_formulation_held_for_new_source":True,
       "old_537_review_decisions_preserved":True,"old_705_links_preserved":True,
       "four_individual_link_decisions_pending":True,
       "all_stages_unsealed":True,"human_peer_verified":False,
       "production_corpus_used":False,
       "next":"Screen contextual prerequisites only if exact independent meanings exist; no invented filtration, conditional expectation or graph-coloring links."
    }
    atomic_json(w.root/"state/wave2_research81_meanings.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
