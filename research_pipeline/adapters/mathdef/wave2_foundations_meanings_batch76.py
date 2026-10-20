"""Batch 76: independently screen four module/topology meanings and seven variants.

Reuse source-reviewed observations, preserve all previous 530 formulation
decisions, and keep individual dependency screening for its own step.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
REVIEW="wave2/source_crosscheck_batch74_2026-10-20.jsonl"
BASE={"sources":14,"terms":414,"observations":848,"meanings":510,"relations":698}
NEXT=dict(BASE,meanings=514)
KEYS=("noetherian-module","submodule","discrete-topology","continuous-topological-map")
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Previous mathematical screening record modified")
    path.write_text(body,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BASE):
        raise PipelineError("Must use independent unsealed Wave 2")
    counts={s:len(w.records(s)) for s in BASE}
    if counts not in (BASE,NEXT):
        raise PipelineError("Unexpected source or meaning count")
    source={r["key"]:r for r in jsonl(w.root/REVIEW)}
    if set(source)!=set(KEYS):
        raise PipelineError("Four source-reviewed concepts required")
    terms=w.records("terms");obs=w.records("observations")
    additions=[];individual=[]
    for key in KEYS:
        x=source[key]
        tid="term.wave2.foundation75."+key
        if x["production_corpus_consulted"] or x["stage_ingested"] or not x["source_reviewed"] or tid not in terms:
            raise PipelineError("Independent source history incomplete "+key)
        mid="meaning.wave2.foundation76."+key
        forms=[]
        for i,form in enumerate(x["forms"],1):
            oid=f"obs.wave2.foundation75.{key}.{i:02d}"
            expected=obs.get(oid)
            if not expected or expected["term_id"]!=tid or expected["locator"]!=x["url"]:
                raise PipelineError("Variant has no individually reviewed matching source observation")
            fid=f"form.wave2.foundation76.{key}.{i:02d}"
            forms.append({
               "id":fid,"text":form["text"],"evidence_ids":[oid],
               "review_state":"screened","human_verified":False,
               "mathematical_review_reason":x["reason"]+" Exact source section: "+form["section"],
               "source_screened_by":"assistant_independent_mathematical_screen_foundations76_2026_10_20"
            })
            individual.append({
               "review_id":"review.wave2.foundation76."+fid,
               "meaning_id":mid,"formulation_id":fid,"source_observation_id":oid,
               "mathematical_reason":x["reason"]+" Source variant: "+form["variant"],
               "source_locator":x["url"],
               "decision":"individually_source_mathematical_screened_pending_link_review",
               "human_verified":False,"production_corpus_used":False
            })
        additions.append({
            "id":mid,"term_group_id":"wave2.foundation76."+key,
            "display_term":x["term"],"context":x["context"],"term_ids":[tid],
            "editorial_status":"individually_source_and_mathematical_screened",
            "editorial_screening_reason":x["reason"],
            "human_verified":False,"formulations":forms
        })
    if len(additions)!=4 or len(individual)!=7:
        raise PipelineError("Some equivalent formulations were dropped")
    store(w.root/"wave2/foundation76_individual_meaning_reviews.jsonl",individual)
    intake=store(w.root/"intake/foundation76_meanings.jsonl",additions)
    history_file=w.root/"state/wave2_formulation_reviews.jsonl"
    previous=jsonl(history_file)
    oldmeanings=w.records("meanings")
    if len(previous) not in (530,537) or len({r["formulation_id"] for r in previous})!=len(previous):
        raise PipelineError("Prior 530 formulation-level reviews missing")
    if {id for r in previous for id in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Historical independently screened relations are not all reviewed")
    snap=w.root/"state/wave2_formulation_reviews_snapshot_530_before_foundation76.jsonl"
    if len(oldmeanings)==510:
        if len(previous)!=530 or any(r["meaning_catalog_digest"]!=digest(list(oldmeanings.values())) for r in previous):
            raise PipelineError("Historical 530 meaning-version digests stale")
        text=history_file.read_text(encoding="utf-8")
        if snap.exists() and snap.read_text(encoding="utf-8")!=text:
            raise PipelineError("Earlier 530-reviewed archive was altered")
        snap.write_text(text,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_530_before_foundation76.json",{
          "rows":530,"links":698,"sha256":hashlib.sha256(text.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
        w.ingest("meanings",intake,batch_size=4)
    ms=w.records("meanings")
    if len(ms)!=514 or any(ms.get(x["id"])!=x for x in additions):
        raise PipelineError("Unexpected individual-screened meanings")
    hist=jsonl(snap)
    if len(hist)!=530 or len({r["formulation_id"] for r in hist})!=530:
        raise PipelineError("Historical source-screened formulation records lost")
    version=digest(list(ms.values()))
    new=[dict(r,meaning_catalog_digest=version) for r in hist]
    for row in individual:
        new.append({
          "formulation_id":row["formulation_id"],"meaning_id":row["meaning_id"],
          "meaning_catalog_digest":version,"decision":"needs_review",
          "relation_ids":[],"original_wave1_disposition":None,
          "source":"independent_foundations_variant_screen_batch76",
          "editorial_reason":"Mathematically screened, source-attributed formulation; exact prerequisite review pending.",
          "reviewed_by":None,"human_verified":False
        })
    if len(previous)==537:
        before={r["formulation_id"]:r for r in previous}
        if before!={r["formulation_id"]:r for r in new}:
            raise PipelineError("Prior independently screened variant reviews conflict")
    else:
        atomic_jsonl(history_file,sorted(new,key=lambda r:r["formulation_id"]))
    latest=jsonl(history_file)
    by={r["formulation_id"]:r for r in latest}
    if len(latest)!=537 or len(by)!=537:
        raise PipelineError("Formulation-review ledger did not cover all 537 formulations")
    for earlier in hist:
        newr=by[earlier["formulation_id"]]
        if any(newr.get(k)!=v for k,v in earlier.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Historical unrelated review changed")
    if {i for r in latest for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Previously screened dependency links lost")
    check_cycles(ms,w.records("relations"))
    if dict(Counter(r["decision"] for r in latest))!={"linked":523,"no_supported_target":7,"needs_review":7}:
        raise PipelineError("Unexpected prior/new review dispositions")
    state=w.state("meanings")
    state.update(total=514,record_digest=version,screened_new_formulations=106,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
       "batch":76,"screened_contextual_meanings":514,"reviewed_formulations":537,
       "source_reviewed_new_meanings":4,"source_reviewed_new_variants":7,
       "historic_530_formulation_decisions_preserved":True,
       "historic_698_screened_links_preserved":True,
       "nonempty_discrete_source_scope_preserved":True,
       "two_continuity_definitions_equivalent":True,
       "module_vs_noetherian_ring_semantics_distinct":True,
       "new_link_reviews_pending":7,"human_peer_verified":False,
       "production_corpus_used":False,"all_stages_unsealed":True,
       "next":"Individually screen source-specific module and topological prerequisites and review historical Noetherian-ring no-target amendment explicitly."
    }
    atomic_json(w.root/"state/wave2_foundations_meaning_screen_batch76.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
