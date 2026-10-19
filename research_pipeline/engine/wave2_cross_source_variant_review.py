"""Independently audit four original Stacks field-theory cross-source variants.

Records mathematically grounded conclusions without automatically merging term
groups or changing production mathDef. The characteristic-zero addendum must
first be removed through its separately audited source-specific revision.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,jsonl,atomic_json,digest
EXPECTED={
"v2.cross_source_variant_review.ecee810777313ec5528d":"equivalent_core_with_conditional_finite_alternative",
"v2.cross_source_variant_review.04f2fc809a00e735e0b0":"equivalent_under_algebraic_extension_hypothesis",
"v2.cross_source_variant_review.99300a2cc682bb12ac04":"equivalent_in_positive_characteristic_with_unverified_characteristic_zero_addendum",
"v2.cross_source_variant_review.c0e4d3a4a1222f384da6":"equivalent_under_algebraic_extension_hypothesis"
}
def run(first, second):
 old,new=Workspace(first),Workspace(second)
 frozen=json.loads((old.root/"state/wave1_freeze.json").read_text(encoding="utf-8"))
 baseline=json.loads((new.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave" or digest(old.publication())!=frozen["published_catalog_digest"] or baseline["first_wave_digest"]!=frozen["published_catalog_digest"]:
  raise PipelineError("Invalid independent frozen research lineage")
 if any(new.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Cannot change sealed Wave 2 data")
 if len(new.records("meanings"))!=462 or len(new.records("relations"))!=622:
  raise PipelineError("Source audit is for post-correction 462-meaning/622-link checkpoint")
 scope=new.root/"state/wave2_pure_inseparable_scope_correction.json"
 if not scope.exists() or not json.loads(scope.read_text(encoding="utf-8")).get("unsupported_characteristic_zero_statement_not_silently_claimed"):
  raise PipelineError("Positive-characteristic source-scope discrepancy must be individually corrected")
 original=jsonl(new.root/"wave2/prioritized_research.jsonl")
 selected=[x for x in original if x["kind"]=="cross_source_variant_review"]
 researched=jsonl(new.root/"wave2/cross_source_field_theory_variant_reviews_2026-10-19.jsonl")
 found={x["task_id"]:x for x in researched}
 if len(selected)!=len(researched)!=len(found)!=4 or set(found)!=set(EXPECTED):
  raise PipelineError("All four original cross-source variant cases must be individually reviewed")
 meanings=new.records("meanings")
 evidence=[]
 for task in selected:
  x=found[task["id"]]
  if x["decision"]!=EXPECTED[task["id"]]:
   raise PipelineError("Source-specific decision mismatch "+task["id"])
  if len(x["meaning_ids"])!=2 or x["meaning_ids"]!=task["candidate_meaning_ids"]:
   raise PipelineError("Wrong pairing of original independent meanings "+task["id"])
  for mid,url in zip(x["meaning_ids"],x["source_urls"]):
   m=meanings.get(mid)
   if m is None or m.get("source_citation",{}).get("url")!=url or not all(f["review_state"]=="screened" for f in m["formulations"]):
    raise PipelineError("Meaning not source-screened at exact locator "+str(mid))
  if len(x["mathematical_comparison"])<250 or len(x["hypotheses_for_equivalence"])<50:
   raise PipelineError("Inadequate mathematical source comparison "+task["id"])
  if x["sourced_and_reviewed"] is not True or x["human_verified"] is not False or x["already_merged"] is not False:
   raise PipelineError("Cannot invent human approval or automatic synonymous merge")
  if x["production_corpus_consulted"] is not False:
   raise PipelineError("Production corpus comparison prohibited")
  evidence.append({
    "task_id":task["id"],"original_task_label":task["label"],
    "source_review_decision":x["decision"],
    "paired_source_urls":x["source_urls"],
    "source_bound_meaning_ids":x["meaning_ids"],
    "research_status":"individually_mathematically_reviewed",
    "definition_records_merged":False,
    "human_verified":False
  })
 if len(new.records("terms"))!=363 or len(new.records("observations"))!=786:
  raise PipelineError("Source catalog drift")
 p=new.root/"state/wave2_cross_source_field_theory_audit.json"
 report={
  "phase":"four_original_cross_source_field_theory_variants_mathematically_reviewed",
  "original_cross_source_tasks":4,
  "cross_source_tasks_with_individual_source_and_mathematics_comparison":4,
  "equivalent_core_or_matching_context_cases":3,
  "equivalent_positive_characteristic_with_separate_scope_correction":1,
  "source_scope_correction_applied_to_editable_wave2_only":True,
  "source_review_details":"wave2/cross_source_field_theory_variant_reviews_2026-10-19.jsonl",
  "source_comparison_task_ids":list(EXPECTED),
  "production_corpus_used":False,
  "automatic_synonym_merges":0,
  "other_original_source_priority_tasks_not_classified_as_reviewed":95,
  "remaining_weak_bicategory_source_variant_still_unverified":True,
  "link_count_preserved":622,
  "all_stages_unsealed":True,
  "human_peer_verified":False
 }
 atomic_json(p,report)
 return report
def main():
 a=argparse.ArgumentParser(description=__doc__)
 a.add_argument("--wave1",required=True,type=Path);a.add_argument("--wave2",required=True,type=Path)
 p=a.parse_args()
 print(json.dumps(run(p.wave1,p.wave2),indent=2))
if __name__=="__main__":main()
