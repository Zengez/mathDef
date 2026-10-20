"""Batch 52: independently screened quotient-model and positive-real-class definitions.

This source-adapter verifies CSUSM chapter 9 mathematical source evidence.
It preserves all 506 previous formulation review decisions, 664 links,
and the independent frozen Wave 1, without consulting production mathDef.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from collections import Counter
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
RESEARCH="wave2/real_constructions_independent_source_reviews_batch_48_2026-10-20.jsonl"
URL="https://public.csusm.edu/aitken_html/m378_S2016/Ch9RealNumbers.pdf"
STAGES=("sources","terms","observations","meanings","relations")
BEFORE={"sources":14,"terms":395,"observations":818,"meanings":494,"relations":664}
AFTER=dict(BEFORE,meanings=496)
CASES=(
 {
  "index":"06","review":"review.wave2.real48.cauchy-class-real",
  "meaning":"meaning.wave2.real52.cauchy-quotient-reals",
  "form":"form.wave2.real52.cauchy-quotient-reals",
  "label":"real number system (complete ordered field)",
  "group":"wave2.real45.complete-ordered-real-field",
  "context":"Concrete quotient model of the reals: rational Cauchy sequences modulo zero difference",
  "text":"Let C_Q be the set of all rational Cauchy sequences and let a∼b mean that a_n−b_n tends to rational zero. The Cauchy-sequence model of the real numbers has underlying set R_C=C_Q/∼, whose elements are equivalence classes [a_n]. On classes one defines [a_n]+[b_n]=[a_n+b_n] and [a_n]·[b_n]=[a_n b_n], and embeds each rational q as the class of the constant sequence q.",
  "reason":"CSUSM Chapter 9 Definitions 1–3 explicitly define the real-number model as equivalence classes of rational Cauchy sequences and define arithmetic classwise. This construction does not identify sequences with their rational limits; representatives may not converge in Q. Independence of representatives, field laws, an order and the least-upper-bound property are mathematical proof obligations and must not be regarded as part of the bare quotient definition."
 },
 {
  "index":"07","review":"review.wave2.real48.cauchy-positive",
  "meaning":"meaning.wave2.real52.positive-cauchy-class",
  "form":"form.wave2.real52.positive-cauchy-class",
  "label":"positive Cauchy-equivalence real class",
  "group":"wave2.real52.positive-cauchy-class",
  "context":"Positive cone of rational-Cauchy quotient field, with an eventual uniform rational margin",
  "text":"A Cauchy-equivalence class [a_n] is called positive when there is a positive rational δ and an index N such that a_n≥δ for all n≥N. This condition is independent of the representative: if b_n−a_n tends to zero, then b_n is eventually bounded below by δ/2.",
  "reason":"CSUSM Chapter 9 Section 5 and the rational-Cauchy model distinguish strict positivity from mere eventual positivity of sequence terms. The null sequence 1/n has every term positive yet represents zero, so only an eventual uniform bound by a positive rational number defines a positive class. Representative independence follows by an epsilon comparison and is necessary before defining the ordered-field relation."
 },
)

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Changed previously reviewed Cauchy model batch")
    path.write_text(body,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in STAGES):
        raise PipelineError("Unsealed independent second wave required")
    counts={s:len(w.records(s)) for s in STAGES}
    if counts not in (BEFORE,AFTER):
        raise PipelineError("Invalid independent Cauchy-model baseline: "+str(counts))
    current=w.records("meanings"); terms=w.records("terms")
    observations=w.records("observations"); sources=w.records("sources")
    if sources["src.csusm_aitken378"]["rights"]!="locator_only":
        raise PipelineError("Unexpected source reuse rights")
    research={r["id"]:r for r in jsonl(w.root/RESEARCH)}
    if len(research)!=8:
        raise PipelineError("Missing independently authored source reviews")
    proposals=[]; individual=[]
    for c in CASES:
        rid=c["review"];r=research.get(rid)
        tid="term.wave2.real49."+c["index"];oid="obs.wave2.real49."+c["index"]
        if (not r or r["stage_ingested"] or r["production_corpus_consulted"]
            or r["source_primary"]["url"]!=URL or
            not terms.get(tid) or terms[tid]["source_id"]!="src.csusm_aitken378"
            or not observations.get(oid) or observations[oid]["term_id"]!=tid
            or observations[oid]["source_id"]!="src.csusm_aitken378"
            or observations[oid]["locator"]!=URL):
            raise PipelineError("Unscreened or mismatched CSUSM source claim "+c["index"])
        if len(c["reason"])<220:
            raise PipelineError("Insufficient individual mathematical review")
        proposals.append({
          "id":c["meaning"],"term_group_id":c["group"],
          "display_term":c["label"],"context":c["context"],"term_ids":[tid],
          "editorial_status":"source_scoped_mathematical_formulation_screened",
          "editorial_screening_reason":c["reason"],
          "independent_review_id":rid,"human_verified":False,
          "formulations":[{
            "id":c["form"],"text":c["text"],"evidence_ids":[oid],
            "review_state":"screened","human_verified":False,
            "source_screened_by":"assistant_independent_cauchy_models_review_2026_10_20"
          }]
        })
        individual.append({
          "review_id":"review.wave2.real52."+c["index"],
          "meaning_id":c["meaning"],"formulation_id":c["form"],
          "source_evidence_id":oid,"source_locator":URL,
          "mathematical_reason":c["reason"],
          "decision":"source_scoped_definition_screened_with_separate_proofs_required",
          "reviewed_by":"assistant_independent_cauchy_models_review_2026_10_20",
          "human_verified":False,"production_corpus_consulted":False
        })
    store(w.root/"wave2/cauchy_model_and_positive_class_reviews_batch_52.jsonl",individual)
    input_path=store(w.root/"intake/real52_cauchy_models_meanings.jsonl",proposals)
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    earlier=jsonl(ledger)
    if len(earlier) not in (506,508) or len({r["formulation_id"] for r in earlier})!=len(earlier):
        raise PipelineError("Stale historical formulation review ledger")
    old_rel=w.records("relations")
    if {id for record in earlier for id in record["relation_ids"]}!=set(old_rel):
        raise PipelineError("Historical links not individually documented")
    snapshot=w.root/"state/wave2_formulation_reviews_snapshot_506_before_real52.jsonl"
    if len(current)==494:
        if len(earlier)!=506 or any(r["meaning_catalog_digest"]!=digest(list(current.values())) for r in earlier):
            raise PipelineError("Stale 506-formulation meaning version")
        before=ledger.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=before:
            raise PipelineError("Old history snapshot changed")
        snapshot.write_text(before,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_506_before_real52.json",{
            "rows":506,"screened_links":664,"sha256":hashlib.sha256(before.encode("utf-8")).hexdigest(),
            "human_peer_verified":False})
        w.ingest("meanings",input_path,batch_size=2)
    now=w.records("meanings")
    if len(now)!=496 or any(now.get(p["id"])!=p for p in proposals):
        raise PipelineError("Cauchy model formulations changed or missing")
    historic=jsonl(snapshot)
    if len(historic)!=506 or len({r["formulation_id"] for r in historic})!=506:
        raise PipelineError("Historical 506-formulation archive lost")
    newhash=digest(list(now.values()))
    updated=[dict(record,meaning_catalog_digest=newhash) for record in historic]
    for c in CASES:
        updated.append({
          "formulation_id":c["form"],"meaning_id":c["meaning"],
          "meaning_catalog_digest":newhash,"decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,
          "source":"independent_Cauchy_quotient_and_positive_class_math_review_batch52",
          "editorial_reason":"Source-supported model definition; verify individually each circularity-free foundational link and exact source target.",
          "reviewed_by":None,"human_verified":False
        })
    if len(earlier)==508:
        idx={r["formulation_id"]:r for r in earlier}
        if len(idx)!=508 or any(idx.get(r["formulation_id"])!=r for r in updated):
            raise PipelineError("Previously screened Cauchy-model review ledger conflicts")
    else:
        atomic_jsonl(ledger,sorted(updated,key=lambda x:x["formulation_id"]))
    result=jsonl(ledger)
    index={r["formulation_id"]:r for r in result}
    if len(result)!=508 or len(index)!=508:
        raise PipelineError("Missing screened review row")
    for prior in historic:
        restored=index[prior["formulation_id"]]
        if any(restored.get(k)!=v for k,v in prior.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Old formulation decision was altered")
    if {id for record in result for id in record["relation_ids"]}!=set(old_rel):
        raise PipelineError("Historical relationship link changed")
    check_cycles(now,old_rel)
    if dict(Counter(r["decision"] for r in result))!={
        "linked":498,"no_supported_target":4,"needs_review":6}:
        raise PipelineError("Incorrect pending source/meaning review disposition")
    state=w.state("meanings")
    state.update(total=496,record_digest=newhash,screened_new_formulations=77,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
      "phase":"Cauchy_sequence_equivalence_class_and_positive_cone_source_screened",
      "screened_meanings":496,"reviewed_formulations":508,"new_meanings":2,
      "old_506_review_decisions_preserved":True,
      "old_664_dependency_links_preserved":True,
      "all_six_new_formulations_still_need_individual_dependency_reviews":True,
      "positive_class_requires_uniform_positive_margin":True,
      "class_arithmetic_requires_well_definedness_proof":True,
      "cut_and_Cauchy_models_not_claimed_equal_as_sets":True,
      "theorem_model_isomorphism_kept_out_of_definition_counts":True,
      "source_prose_reproduced":False,"production_corpus_used":False,"human_peer_verified":False,
      "all_stages_unsealed":True,
      "next":"Independently screen prerequisite relationships for all six new mathematical formulations; ensure no cycles, avoid separate-field models as definition dependencies when only model isomorphism is meant."
    }
    atomic_json(w.root/"state/wave2_cauchy_model_meaning_screen_batch52.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    args=p.parse_args()
    print(json.dumps(run(args.workspace),indent=2))

if __name__=="__main__":main()
