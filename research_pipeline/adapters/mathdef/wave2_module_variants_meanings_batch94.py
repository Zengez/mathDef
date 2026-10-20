"""Batch 94: screen three source-specific module conventions, without duplication.

The original independently sourced ordinary-left module meaning is untouched.
Three newly sourced right/unital conventions are distinct mathematical contexts.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/module_convention_variants_research_batch92_2026-10-20.jsonl"
BEFORE={"sources":14,"terms":428,"observations":865,"meanings":527,"relations":730}
AFTER=dict(BEFORE,meanings=530)
KEYS=("right-module-nonunital","unital-left-module","unital-right-module")
LEFT="meaning.wave2.foundation.left-module-nonunital"
GROUP="wave2.module94.module-over-ring"
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    data="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=data:
        raise PipelineError("Previously screened individual module review changed")
    path.write_text(data,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Requires unsealed independent Wave 2")
    if {s:len(w.records(s)) for s in BEFORE} not in (BEFORE,AFTER):
        raise PipelineError("Unexpected reviewed-source/meaning baseline")
    previous_meanings=w.records("meanings")
    left=previous_meanings.get(LEFT)
    if (not left or left["id"]!=LEFT or
        "unital action" not in left["editorial_screening_reason"].lower()):
        raise PipelineError("Original general-left source convention cannot be checked")
    dossier={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(dossier)!=set(KEYS):
        raise PipelineError("Three independently checked module sources required")
    terms=w.records("terms");obs=w.records("observations")
    additions=[];individual=[]
    for key in KEYS:
        r=dossier[key]
        tid="term.wave2.module93."+key
        oid="obs.wave2.module93."+key
        fid="form.wave2.module94."+key
        mid="meaning.wave2.module94."+key
        o=obs.get(oid)
        text=r["definition"]
        if (r["stage_ingested"] or r["production_corpus_used"] or
            r["source_id"]!="src.proofwiki" or
            r["source_review_status"]!="direct_external_page_checked" or
            len(r["mathematical_reason"])<260 or
            not o or tid not in terms or o["term_id"]!=tid or
            o["locator"]!=r["source_url"] or
            text!=o["text"] or len(text)<180):
            raise PipelineError("Individual source/provenance mismatch: "+key)
        if key=="right-module-nonunital":
            if "(mr)s=m(rs)" not in text or "m1=m" in text:
                raise PipelineError("Right module orientation/unitality wrongly described")
        elif key=="unital-left-module":
            if "(rs)m=r(sm)" not in text or "1m=m" not in text:
                raise PipelineError("Unital left ring action axioms missing")
        elif key=="unital-right-module":
            if "(mr)s=m(rs)" not in text or "m1=m" not in text:
                raise PipelineError("Unital right ring action axioms missing")
        reason=(r["mathematical_reason"]+
          " Existing general left R-module stays separate and unchanged; this is a context-specific module convention, not an equivalent characterization of all module actions.")
        form={
          "id":fid,"text":text,"evidence_ids":[oid],
          "review_state":"screened","human_verified":False,
          "mathematical_review_reason":reason,
          "source_screened_by":"assistant_independent_module_convention_mathematical_screen_2026_10_20"
        }
        additions.append({
          "id":mid,"term_group_id":GROUP,"display_term":"module over a ring",
          "context":r["context"],"term_ids":[tid],
          "formulations":[form],
          "editorial_status":"individual_mathematical_convention_screened",
          "editorial_screening_reason":reason,
          "human_verified":False
        })
        individual.append({
          "review_id":"review.wave2.module94."+key,
          "meaning_id":mid,"formulation_id":fid,
          "source_observation_id":oid,"source_locator":r["source_url"],
          "mathematical_reason":reason,
          "decision":"mathematically_screened_pending_independent_link_review",
          "human_verified":False,"production_corpus_used":False
        })
    if len(additions)!=3 or len(individual)!=3:
        raise PipelineError("All three distinct conventions must be screened")
    store(w.root/"wave2/module94_individual_formulation_reviews.jsonl",individual)
    file=store(w.root/"intake/module94_meanings.jsonl",additions)
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    old_review=jsonl(ledger)
    if len(old_review) not in (551,554) or len({r["formulation_id"] for r in old_review})!=len(old_review):
        raise PipelineError("Existing 551 mathematical review records incomplete")
    if {id for r in old_review for id in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Historical 730 screened relationships not reviewed")
    snapshot=w.root/"state/wave2_formulation_reviews_snapshot_551_before_module94.jsonl"
    if len(previous_meanings)==527:
        if len(old_review)!=551 or any(r["meaning_catalog_digest"]!=digest(list(previous_meanings.values())) for r in old_review):
            raise PipelineError("Prior meaning catalog digest is stale")
        text=ledger.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=text:
            raise PipelineError("Historical 551-formulation snapshot changed")
        snapshot.write_text(text,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_551_before_module94.json",{
          "rows":551,"screened_links":730,
          "sha256":hashlib.sha256(text.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
        w.ingest("meanings",file,batch_size=3)
    now=w.records("meanings")
    if len(now)!=530 or now.get(LEFT)!=left or any(now.get(x["id"])!=x for x in additions):
        raise PipelineError("New module context admission altered original left meaning")
    archive=jsonl(snapshot)
    if len(archive)!=551 or len({r["formulation_id"] for r in archive})!=551:
        raise PipelineError("Missing prior 551 individual reviews")
    h=digest(list(now.values()))
    new=[dict(row,meaning_catalog_digest=h) for row in archive]
    for r in individual:
        new.append({
          "formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
          "meaning_catalog_digest":h,"decision":"needs_review",
          "relation_ids":[],"original_wave1_disposition":None,
          "source":"independent_module_convention_mathematical_review_batch94",
          "editorial_reason":"Mathematical action/unit axioms source-screened; prerequisite links pending individually.",
          "reviewed_by":None,"human_verified":False
        })
    if len(old_review)==554:
        if {r["formulation_id"]:r for r in old_review}!={r["formulation_id"]:r for r in new}:
            raise PipelineError("Repeat screening differs from prior individual review history")
    else:
        atomic_jsonl(ledger,sorted(new,key=lambda r:r["formulation_id"]))
    actual=jsonl(ledger);by={r["formulation_id"]:r for r in actual}
    if len(actual)!=554 or len(by)!=554:
        raise PipelineError("Incomplete 554 reviewed formulations")
    for row in archive:
        updated=by[row["formulation_id"]]
        if any(updated.get(k)!=v for k,v in row.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Historical review decision was changed")
    if {id for r in actual for id in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Historical screened relation coverage changed")
    check_cycles(now,w.records("relations"))
    if dict(Counter(r["decision"] for r in actual))!={"linked":544,"no_supported_target":7,"needs_review":3}:
        raise PipelineError("Unexpected previous/new review statuses")
    state=w.state("meanings")
    state.update(total=530,record_digest=h,screened_new_formulations=123,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
      "batch":94,"screened_meanings":530,"reviewed_formulations":554,
      "new_distinct_module_conventions":3,
      "existing_general_left_module_untouched":True,
      "nonunital_right_and_unital_left_right_scopes_explicit":True,
      "all_551_historic_dispositions_preserved":True,
      "all_730_previous_links_preserved":True,
      "new_link_reviews_pending":3,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Screen source-specific module/abelian-group dependencies; only amend old submodule no-target if direct independently screened left module is a valid target."
    }
    atomic_json(w.root/"state/wave2_module94_meanings.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
