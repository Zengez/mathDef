"""Batch 101: screen five independently sourced division-ring mathematical contexts.

The normed-division-ring entry preserves its lower-quality bibliography
status and requires both the separately reviewed scalar norm and division ring.
Left/right vector spaces remain distinct over noncommutative scalars.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/division_ring_scalar_convention_research_batch100_2026-10-20.jsonl"
BASE={"sources":14,"terms":437,"observations":877,"meanings":536,"relations":742}
AFTER=dict(BASE,meanings=541)
KEYS=("division-ring","division-ring-multiplicative-norm","normed-division-ring",
      "left-vector-over-division-ring","right-vector-over-division-ring")

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Prior Batch101 mathematical review changed")
    path.write_text(body,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BASE):
        raise PipelineError("Independent, unsealed Wave 2 required")
    counts={s:len(w.records(s)) for s in BASE}
    if counts not in (BASE,AFTER):
        raise PipelineError("Unexpected mathematics baseline "+str(counts))
    sourcecheck=json.loads((w.root/"state/wave2_scalar100_source_intake.json").read_text())
    if sourcecheck["new_source_terms"]!=5 or sourcecheck["new_source_observations"]!=5 or sourcecheck["new_screened_meanings"]!=0:
        raise PipelineError("Prior source-only validation not verified")
    dossier={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(dossier)!=set(KEYS):
        raise PipelineError("Five source reviews missing")
    terms=w.records("terms");obs=w.records("observations")
    original=w.records("meanings")
    candidates=[];individual=[]
    for key in KEYS:
        research=dossier[key]
        tid="term.wave2.scalar100."+key
        oid="obs.wave2.scalar100."+key
        o=obs.get(oid)
        if (tid not in terms or not o or o["term_id"]!=tid or
            o["locator"]!=research["source"] or o["text"]!=research["definition"] or
            o["source_id"]!="src.proofwiki" or research["stage_ingested"] or research["production_corpus_consulted"] or
            len(research["mathematical_review"])<280):
            raise PipelineError("Unresolved source evidence for "+key)
        reason=research["mathematical_review"]
        if key=="division-ring":
            if "nonzero associative unital" not in research["definition"] or "two-sided" not in research["definition"]:
                raise PipelineError("Division ring algebraic axioms absent")
        elif key=="division-ring-multiplicative-norm":
            if "|ab|_D=|a|_D|b|_D" not in research["definition"]:
                raise PipelineError("Scalar multiplicative norm axiom absent")
        elif key=="normed-division-ring":
            if "lacking bibliographic" not in reason:
                raise PipelineError("Incomplete bibliography caveat missing")
            reason+=(" This mathematical screening validates the object as the pair of the separately "
                     "source-observed associative division ring and multiplicative norm; the direct pair page "
                     "has no bibliography, so its evidentiary status is explicitly limited.")
        elif key=="left-vector-over-division-ring":
            if "D×V→V" not in research["definition"] or "(ab)v=a(bv)" not in research["definition"]:
                raise PipelineError("Left vector action orientation incorrect")
        elif key=="right-vector-over-division-ring":
            if "V×D→V" not in research["definition"] or "(va)b=v(ab)" not in research["definition"]:
                raise PipelineError("Right vector action orientation incorrect")
        mid="meaning.wave2.scalar101."+key
        fid="form.wave2.scalar101."+key
        if key.endswith("vector-over-division-ring"):
            group="wave2.scalar101.vector-space-over-division-ring"
        else:
            group="wave2.scalar101."+key
        form={
          "id":fid,"text":research["definition"],"evidence_ids":[oid],
          "review_state":"screened","human_verified":False,
          "mathematical_review_reason":reason,
          "source_screened_by":"assistant_independent_scalar_division_ring_math_screen_2026_10_20"
        }
        candidates.append({
          "id":mid,"term_group_id":group,"display_term":research["term"],
          "context":research["context"],"term_ids":[tid],"formulations":[form],
          "editorial_status":"individually_source_and_mathematically_screened",
          "editorial_screening_reason":reason,
          "source_bibliography_warning":key=="normed-division-ring",
          "human_verified":False
        })
        individual.append({
          "review_id":"review.wave2.scalar101."+key,
          "meaning_id":mid,"formulation_id":fid,
          "source_observation_id":oid,"source_locator":research["source"],
          "mathematical_reason":reason,
          "decision":"mathematically_screened_pending_individual_link_review",
          "source_bibliography_warning":key=="normed-division-ring",
          "human_verified":False,"production_corpus_used":False
        })
    if len(candidates)!=5 or len(individual)!=5:
        raise PipelineError("Five contextual meanings must have source-specific reviews")
    if candidates[3]["term_group_id"]!=candidates[4]["term_group_id"] or candidates[3]["context"]==candidates[4]["context"]:
        raise PipelineError("Noncommutative left/right contexts must be distinct under one group")
    store(w.root/"wave2/scalar101_individual_mathematical_reviews.jsonl",individual)
    intake=store(w.root/"intake/scalar101_meanings.jsonl",candidates)
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prior=jsonl(ledger)
    if len(prior) not in (561,566) or len({r["formulation_id"] for r in prior})!=len(prior):
        raise PipelineError("Expected prior 561 individual formulation reviews")
    if {i for r in prior for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Historical screened dependency reviews incomplete")
    history=w.root/"state/wave2_formulation_reviews_snapshot_561_before_scalar101.jsonl"
    if len(original)==536:
        if len(prior)!=561 or any(r["meaning_catalog_digest"]!=digest(list(original.values())) for r in prior):
            raise PipelineError("Prior meaning catalog digest invalid")
        text=ledger.read_text(encoding="utf-8")
        if history.exists() and history.read_text(encoding="utf-8")!=text:
            raise PipelineError("Historical 561 dispositions changed")
        history.write_text(text,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_561_before_scalar101.json",{
          "rows":561,"prior_links":742,"sha256":hashlib.sha256(text.encode()).hexdigest(),
          "human_peer_verified":False
        })
        w.ingest("meanings",intake,batch_size=5)
    ms=w.records("meanings")
    if len(ms)!=541 or any(ms.get(x["id"])!=x for x in candidates):
        raise PipelineError("Source-screened contexts not ingested correctly")
    old=jsonl(history)
    if len(old)!=561 or len({x["formulation_id"] for x in old})!=561:
        raise PipelineError("Snapshot missing previous distinct reviews")
    catalog=digest(list(ms.values()))
    new=[dict(r,meaning_catalog_digest=catalog) for r in old]
    for r in individual:
        new.append({
          "formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
          "meaning_catalog_digest":catalog,"decision":"needs_review",
          "relation_ids":[],"original_wave1_disposition":None,
          "source":"independent_scalar_division_ring_mathematical_screen_batch101",
          "editorial_reason":"Source-grounded mathematical definition screened, direct prerequisite links require separate individual decisions.",
          "reviewed_by":None,"human_verified":False})
    if len(prior)==566:
        if {r["formulation_id"]:r for r in prior}!={r["formulation_id"]:r for r in new}:
            raise PipelineError("Previously committed source-screened reviews differ")
    else:
        atomic_jsonl(ledger,sorted(new,key=lambda r:r["formulation_id"]))
    reviews=jsonl(ledger);byid={r["formulation_id"]:r for r in reviews}
    if len(reviews)!=len(byid)!=566:
        raise PipelineError("Expected 566 distinct formulation reviews")
    for oldrow in old:
        updated=byid[oldrow["formulation_id"]]
        if any(updated.get(k)!=v for k,v in oldrow.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Historic individual review overwritten")
    if {i for r in reviews for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Original links lost")
    check_cycles(ms,w.records("relations"))
    if dict(Counter(r["decision"] for r in reviews))!={"linked":555,"no_supported_target":6,"needs_review":5}:
        raise PipelineError("Unexpected review outcomes")
    state=w.state("meanings")
    state.update(total=541,record_digest=catalog,screened_new_formulations=135,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    result={
      "batch":101,"screened_meanings":541,"reviewed_formulations":566,
      "new_mathematical_contexts":5,"new_formulations":5,
      "historical_561_formulation_dispositions_preserved":True,
      "historical_742_links_preserved":True,
      "scalar_division_ring_norm_is_multiplicative":True,
      "noncommutative_left_and_right_actions_distinct":True,
      "uncited_derived_pair_page_caveat_preserved":True,
      "five_prerequisite_reviews_pending":True,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch102: individually review division ring, multiplicative scalar norm, normed division ring and left/right vector space prerequisites; appropriately amend existing general norm and normed-vector-space links if sourced."
    }
    atomic_json(w.root/"state/wave2_scalar101_meaning_screen.json",result)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
