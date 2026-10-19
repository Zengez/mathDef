"""Reconcile the original 192 prioritized Wave 2 tasks with verified current state.

Never erase/rewrite the original immutable, mostly 'unresearched' priority queue.
A screened relation is evidence of some progress on the relevant formulation,
NOT proof every prerequisite is present or a source-research task is complete.
The current overlay can be regenerated idempotently after each new link batch.
"""
from __future__ import annotations
import argparse
import json
from collections import Counter,defaultdict
from pathlib import Path
from .core import Workspace,PipelineError,jsonl,digest,canonical,atomic_json
from .stage5_review_gate import atomic_jsonl

LINK_GAP_KINDS={"missing_foundation","held_link_research"}
OTHER_KINDS={"blocked_source_recovery","cross_source_variant_review",
             "unproductive_section_retry","source_collection_resurvey"}

def run(first, second):
 a,b=Workspace(first),Workspace(second)
 freeze=json.loads((a.root/"state/wave1_freeze.json").read_text(encoding="utf-8"))
 baseline=json.loads((b.root/"state/baseline.json").read_text(encoding="utf-8"))
 if (freeze.get("state")!="FROZEN" or baseline.get("mode")!="second_wave" or
    digest(a.publication())!=freeze["published_catalog_digest"] or
    baseline["first_wave_digest"]!=freeze["published_catalog_digest"]):
  raise PipelineError("Independent frozen lineage is invalid")
 tasks=jsonl(b.root/"wave2/prioritized_research.jsonl")
 broad=jsonl(b.root/"wave2/tasks.jsonl")
 if len(tasks)!=192 or len(broad)!=3599 or len({t["id"] for t in tasks})!=192:
  raise PipelineError("Original 192/3599 research queues unexpectedly changed")
 links=b.records("relations")
 reviews=jsonl(b.root/"state/wave2_formulation_reviews.jsonl")
 meaning=b.records("meanings")
 forms={f["id"]:m["id"] for m in meaning.values() for f in m["formulations"]}
 reviewmap={r["formulation_id"]:r for r in reviews}
 if len(reviewmap)!=len(reviews) or set(reviewmap)!=set(forms):
  raise PipelineError("Current formulation review catalog incomplete or duplicated")
 if any(r.get("meaning_catalog_digest")!=digest(list(meaning.values())) for r in reviews):
  raise PipelineError("Stale relation review catalog versus mathematical meanings")
 if {rid for r in reviews for rid in r["relation_ids"]}!=set(links):
  raise PipelineError("Relationships missing individual formulation review")
 if any(x["review_state"]!="screened" for x in links.values()):
  raise PipelineError("Unsafe to count unscreened relationship as progress")
 counts=defaultdict(lambda:{"original":0,"with_at_least_one_link":0,
                             "not_demonstrated_complete":0})
 overlay=[]
 for task in tasks:
  kind=task["kind"]
  if kind not in LINK_GAP_KINDS|OTHER_KINDS:
   raise PipelineError("Unknown priority task kind "+kind)
  fid=task.get("formulation_id")
  review=reviewmap.get(fid) if fid else None
  if kind in LINK_GAP_KINDS and review is None:
   raise PipelineError("Missing source formulation for priority relationship gap "+task["id"])
  has_link=(kind in LINK_GAP_KINDS and review is not None and
            review["decision"]=="linked" and len(review["relation_ids"])>0)
  if has_link and not all(rid in links for rid in review["relation_ids"]):
   raise PipelineError("Priority progress points to missing link")
  counts[kind]["original"]+=1
  if has_link:
   counts[kind]["with_at_least_one_link"]+=1
  else:
   counts[kind]["not_demonstrated_complete"]+=1
  overlay.append({
   "task_id":task["id"],
   "kind":kind,
   "initial_status":task.get("status","unresearched"),
   "formulation_id":fid,
   "current_relation_review_decision":review["decision"] if review else None,
   "screened_relation_ids":list(review["relation_ids"]) if review else [],
   "current_evidence_class":"at_least_one_screened_relation" if has_link else
       "not_demonstrated_complete_by_relation_evidence",
   "complete_for_all_mathematical_prerequisites":False,
   "human_verified":False
  })
 total_link_tasks=sum(counts[x]["original"] for x in LINK_GAP_KINDS)
 with_links=sum(counts[x]["with_at_least_one_link"] for x in LINK_GAP_KINDS)
 non_link_tasks=sum(counts[x]["original"] for x in OTHER_KINDS)
 if total_link_tasks!=93 or non_link_tasks!=99:
  raise PipelineError("Original fixed priority-category baseline changed")
 report={
  "phase":"reproducible_fixed_baseline_reconciliation",
  "original_priority_tasks":192,
  "original_relationship_gap_tasks":total_link_tasks,
  "original_relationship_gaps_with_at_least_one_screened_link":with_links,
  "original_relationship_gaps_without_a_screened_link":total_link_tasks-with_links,
  "other_source_variant_collection_tasks_not_proven_complete_by_this_metric":non_link_tasks,
  "total_original_priority_tasks_not_demonstrated_complete":192-with_links,
  "priority_kind_details":dict(counts),
  "original_generic_research_leads":len(broad),
  "screened_links_now":len(links),
  "reviewed_formulations_now":len(reviews),
  "source_coverage_not_inferred_from_link_counts":True,
  "a_link_is_not_proof_of_exhaustive_prerequisites":True,
  "source_task_research_not_automatically_closed":True,
  "original_priority_queue_not_mutated":True,
  "frozen_wave1_digest_verified":True,
  "original_production_mathdef_consulted":False,
  "human_peer_verified":False,
  "wave2_stages_unsealed":not any(b.state(x).get("sealed") for x in
       ("sources","terms","observations","meanings","relations"))
 }
 state=b.root/"state"
 atomic_jsonl(state/"wave2_priority_progress_current.jsonl",overlay)
 atomic_json(state/"wave2_priority_progress_current.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--wave1",type=Path,required=True)
 p.add_argument("--wave2",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.wave1,a.wave2),indent=2))
if __name__=="__main__":
 main()
