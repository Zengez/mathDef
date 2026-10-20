"""Batch 50: individually reviewed Dedekind lower cuts and a real-number model.

Independent source evidence only; no production definition or source index read.
Do not mistake 'supremum is the union' (a theorem) for a third definition.
All historical formulation dispositions and screened links remain unchanged.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from research_pipeline.engine.core import Workspace, PipelineError, jsonl, canonical, digest, atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

# Correct import is from the generic engine, not the domain package.

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASELINE={"sources":14,"terms":395,"observations":818,"meanings":490,"relations":664}
NEXT=dict(BASELINE,meanings=492)
REVIEW_PATH="wave2/real_constructions_independent_source_reviews_batch_48_2026-10-20.jsonl"
CASES=[
 {"n":"01","rid":"review.wave2.real48.dedekind-lower-cut",
  "mid":"meaning.wave2.real50.dedekind-rational-lower-cut",
  "fid":"form.wave2.real50.dedekind-rational-lower-cut",
  "display":"Dedekind cut of the rational numbers",
  "context":"Real construction from Q: nonempty proper lower set without greatest element",
  "group":"wave2.real50.dedekind-lower-cut",
  "text":"A (lower) Dedekind cut of the rational numbers is a subset A of Q such that A is nonempty, A is not all of Q, if a belongs to A then every rational q<a also belongs to A, and A has no largest element.",
  "reason":"PlanetMath's four conditions each have a precise logical role. Nonempty and proper exclude endpoints at negative and positive infinity; downward closure fixes the lower-set convention, while having no largest rational selects the unique lower side at each rational boundary. This is different from a Dedekind-complete abstract ordered set."},
 {"n":"02","rid":"review.wave2.real48.dedekind-real-realization",
  "mid":"meaning.wave2.real50.cut-model-reals",
  "fid":"form.wave2.real50.cut-model-reals",
  "display":"real number system (complete ordered field)",
  "context":"Concrete Dedekind-cut realization: real numbers represented by rational lower cuts",
  "group":"wave2.real45.complete-ordered-real-field",
  "text":"In the Dedekind-cut construction, the underlying set R_D consists of all lower Dedekind cuts A of Q. Define the order by A≤B if and only if A⊆B. Each rational q has the canonical representation {r∈Q:r<q}. Defining arithmetic on cuts and proving the ordered-field axioms and the least-upper-bound property then gives a concrete realization of a real-number system.",
  "reason":"PlanetMath defines real numbers in this model as the rational cuts themselves and orders distinct cuts by strict inclusion. The non-strict relation is its reflexive extension. The rational embedding via strict lower rays is injection preserving order. The claim that arithmetic and completeness hold is an additional proof obligation, not a substitution for those proofs. The new model is a contextual real-number definition, not literal equality to the abstract axiomatic complete ordered field."},
]
def store(path,items):
    path.parent.mkdir(parents=True,exist_ok=True)
    data="".join(canonical(x)+"\n" for x in items)
    if path.exists() and path.read_text(encoding="utf-8")!=data:
        raise PipelineError("Conflict with prior individually reviewed Dedekind batch")
    path.write_text(data,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave"):
        raise PipelineError("Only the independent reconstruction may be edited")
    if any(w.state(s).get("sealed") for s in BASELINE):
        raise PipelineError("An independent stage was sealed")
    counts={stage:len(w.records(stage)) for stage in BASELINE}
    if counts not in (BASELINE,NEXT):
        raise PipelineError("Unexpected source/meaning/relationship baseline: "+str(counts))
    candidates={r["id"]:r for r in jsonl(w.root/REVIEW_PATH)}
    if len(candidates)!=8:
        raise PipelineError("Batch 48 individual source reviews are incomplete")
    sources=w.records("sources"); terms=w.records("terms"); observations=w.records("observations")
    source=sources.get("src.planetmath")
    if not source or source["rights"] not in ("permitted","locator_only") or source["access"]!="free":
        raise PipelineError("Required independently reviewed PlanetMath source missing")
    expected_url="https://planetmath.org/dedekindcuts"
    prepared=[]; individual=[]
    for c in CASES:
        review=candidates.get(c["rid"])
        tid="term.wave2.real49."+c["n"]
        oid="obs.wave2.real49."+c["n"]
        t=terms.get(tid); ob=observations.get(oid)
        if (not review or review["source_primary"]["url"]!=expected_url
            or not review["candidate_formulation"] or len(review["mathematical_review"])<160
            or review["production_corpus_consulted"] or review["stage_ingested"]
            or not t or not ob or t["source_id"]!="src.planetmath"
            or ob["term_id"]!=tid or ob["source_id"]!="src.planetmath"
            or t["locator"]!=expected_url or ob["locator"]!=expected_url
            or ob["record_kind"]!="paraphrase"):
            raise PipelineError("Required independent evidence missing: "+c["n"])
        if len(c["reason"])<190:
            raise PipelineError("Mathematical rationale insufficient for a screen")
        prepared.append({
          "id":c["mid"],"term_group_id":c["group"],"display_term":c["display"],
          "context":c["context"],"term_ids":[tid],
          "editorial_status":"source_scoped_mathematical_formulation_screened",
          "editorial_screening_reason":c["reason"],
          "independent_review_id":c["rid"],"human_verified":False,
          "formulations":[{
            "id":c["fid"],"text":c["text"],"review_state":"screened",
            "evidence_ids":[oid],"human_verified":False,
            "source_screened_by":"assistant_independent_dedekind_model_mathematical_screen_2026_10_20",
          }]
        })
        individual.append({
          "review_id":"review.wave2.real50."+c["n"],
          "meaning_id":c["mid"],"formulation_id":c["fid"],"source_evidence_id":oid,
          "source_locator":expected_url,"individual_mathematical_reason":c["reason"],
          "review_disposition":"screened_definition_needs_independent_link_review",
          "reviewed_by":"assistant_independent_dedekind_model_mathematical_screen_2026_10_20",
          "human_verified":False,"production_corpus_consulted":False
        })
    store(w.root/"wave2/dedekind_individual_meaning_reviews_batch_50.jsonl",individual)
    input_file=store(w.root/"intake/real50_dedekind_meanings.jsonl",prepared)
    old=w.records("meanings")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    old_reviews=jsonl(ledger)
    old_map={x["formulation_id"]:x for x in old_reviews}
    if len(old_reviews) not in (502,504) or len(old_reviews)!=len(old_map):
        raise PipelineError("Old formulation review coverage incomplete")
    old_rel=w.records("relations")
    if {rid for r in old_reviews for rid in r["relation_ids"]}!=set(old_rel):
        raise PipelineError("Existing screened relationships lack provenance")
    if len(old)==490:
        if len(old_reviews)!=502 or any(x["meaning_catalog_digest"]!=digest(list(old.values())) for x in old_reviews):
            raise PipelineError("Prior formulation review digest mismatch")
        # Historical original decisions are preserved byte-for-byte before
        # rebuilding only the catalog-wide version digest.
        before=ledger.read_text(encoding="utf-8")
        archive=w.root/"state/wave2_formulation_reviews_snapshot_502_before_real50.jsonl"
        if archive.exists() and archive.read_text(encoding="utf-8")!=before:
            raise PipelineError("Historical 502-review snapshot conflict")
        archive.write_text(before,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_502_before_real50.json",{
          "rows":502,"screened_links":664,
          "sha256":hashlib.sha256(before.encode("utf-8")).hexdigest(),
          "source_stage":"prior_independent_mathematical_review","human_verified":False})
        w.ingest("meanings",input_file,batch_size=2)
    now=w.records("meanings")
    if len(now)!=492 or any(now.get(x["id"])!=x for x in prepared):
        raise PipelineError("Dedekind screened meaning evidence changed")
    catalog_hash=digest(list(now.values()))
    # On a re-run, the signed snapshot exists and only the catalog digest
    # may differ from historical review payloads.
    archive=w.root/"state/wave2_formulation_reviews_snapshot_502_before_real50.jsonl"
    historic=jsonl(archive)
    if len(historic)!=502:
        raise PipelineError("Missing historical formulation review snapshot")
    oldhash={x["formulation_id"]:x for x in historic}
    if len(oldhash)!=502:
        raise PipelineError("Repeated historical formulation ID")
    new_rows=[]
    for original in historic:
        amended=dict(original,meaning_catalog_digest=catalog_hash)
        new_rows.append(amended)
    for c in CASES:
        new_rows.append({
          "formulation_id":c["fid"],"meaning_id":c["mid"],
          "meaning_catalog_digest":catalog_hash,
          "decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,
          "source":"independent_PlanetMath_cut_model_source_and_math_review_batch50",
          "editorial_reason":"Source-screened definition; exact prerequisite source targets and cycles require separate individual review.",
          "reviewed_by":None,"human_verified":False
        })
    old_mapped={x["formulation_id"]:x for x in old_reviews}
    if len(old_reviews)==504 and (set(old_mapped)!={x["formulation_id"] for x in new_rows} or
           any(canonical(old_mapped[x["formulation_id"]])!=canonical(x) for x in new_rows)):
        raise PipelineError("Previously committed 504 formulation reviews differ")
    if len(old_reviews)==502:
        atomic_jsonl(ledger,sorted(new_rows,key=lambda x:x["formulation_id"]))
    resulting=jsonl(ledger)
    index={r["formulation_id"]:r for r in resulting}
    if len(resulting)!=504 or len(index)!=504:
        raise PipelineError("Incomplete updated formulation review count")
    for fid,original in oldhash.items():
        updated=index[fid]
        if any(updated.get(key)!=value for key,value in original.items() if key!="meaning_catalog_digest"):
            raise PipelineError("Previously screened formulation decision changed: "+fid)
    if {id for record in resulting for id in record["relation_ids"]} != set(old_rel):
        raise PipelineError("Definition-link review provenance changed")
    check_cycles(now,old_rel)
    if dict(Counter(x["decision"] for x in resulting))!={
          "linked":498,"no_supported_target":4,"needs_review":2}:
        raise PipelineError("Unexpected individual dependency dispositions")
    state=w.state("meanings")
    state.update(total=492,record_digest=catalog_hash,
        screened_new_formulations=73,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
      "phase":"individual_source_and_mathematical_screening_of_cut_and_real_cut_model",
      "contextual_meanings":492,"formulations":504,
      "screened_new_meanings":2,"historical_502_review_dispositions_preserved":True,
      "existing_664_links_preserved":True,
      "new_prerequisite_reviews_pending":2,"all_stages_unsealed":True,
      "rational_cauchy_candidates_still_unpromoted":4,
      "supremum_union_result_is_a_theorem_not_new_definition":True,
      "Dedekind_cut_model_distinct_from_abstract_field_underlying_set":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Independently screen remaining Cauchy candidate definitions and review precise prerequisite links; the cut supremum theorem stays in research evidence."
    }
    atomic_json(w.root/"state/wave2_dedekind_meaning_screen_batch50.json",report)
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workspace",type=Path,default=Path(ROOT))
    args=ap.parse_args()
    print(json.dumps(run(args.workspace),indent=2))

if __name__=="__main__":
    main()
