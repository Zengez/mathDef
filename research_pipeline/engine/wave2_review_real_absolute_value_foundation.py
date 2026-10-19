"""Individually classify the real absolute-value foundation without inventing links.

Preserves the exact 483-review source snapshot and 626 existing links.
No source changes, no new definition, no Wave 1 or production access.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from collections import Counter
from .core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import locator,check_cycles

FORM_ID="form.wave2.analysis.real-absolute-value"
def run(root,batch):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave":
  raise PipelineError("Independent Wave 2 only")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("All five research stages must be editable")
 meanings=w.records("meanings");relationships=w.records("relations")
 if len(meanings)!=471 or len(relationships)!=626:
  raise PipelineError("Requires proven real calculus three-link screen")
 previous=w.root/"state/wave2_link_review_batch_22.json"
 if not previous.exists() or json.loads(previous.read_text(encoding="utf-8")).get("total_screened_links")!=626:
  raise PipelineError("Three exact-source real-analysis links not committed")
 rows=jsonl(batch)
 if len(rows)!=1 or rows[0]["formulation_id"]!=FORM_ID:
  raise PipelineError("Exactly one individually reviewed absolute-value foundation required")
 case=rows[0]
 m=meanings.get(case["meaning_id"])
 if not m or m["formulations"][0]["id"]!=FORM_ID:
  raise PipelineError("Reviewed meaning/formulation identity is inconsistent")
 if (case.get("source_locator")!=locator(m,w.records("observations")) or
     m["formulations"][0]["review_state"]!="screened" or
     case.get("decision")!="no_supported_target" or
     len(case.get("mathematical_reason",""))<200 or
     len(case.get("missing_foundations",[]))<3 or
     case.get("human_verified") is not False):
  raise PipelineError("No independent source-specific justified real absolute-value decision")
 p=w.root/"state/wave2_formulation_reviews.jsonl"
 reviews=jsonl(p)
 byid={r["formulation_id"]:r for r in reviews}
 if len(reviews)!=483 or len(byid)!=483 or FORM_ID not in byid:
  raise PipelineError("Incomplete existing mathematical review ledger")
 if any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in reviews):
  raise PipelineError("Stale catalog digest")
 if {rid for r in reviews for rid in r["relation_ids"]}!=set(relationships):
  raise PipelineError("Original 626 links not covered by reviews")
 old=byid[FORM_ID]
 if old["relation_ids"] or old.get("original_wave1_disposition") is not None or old["decision"] not in ("needs_review","no_supported_target"):
  raise PipelineError("Would overwrite a historical or linked mathematical disposition")
 snapshot=w.root/"state/wave2_formulation_reviews_snapshot_483_before_absolute_value_review.jsonl"
 previous_text=p.read_text(encoding="utf-8")
 if not snapshot.exists():
  if old["decision"]!="needs_review":
   raise PipelineError("First review already applied without historical snapshot")
  snapshot.write_text(previous_text,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_483_before_absolute_value_review.json",{
    "original_reviews":483,"original_links":626,
    "review_sha256":hashlib.sha256(previous_text.encode("utf-8")).hexdigest(),
    "original_catalog_digest":old["meaning_catalog_digest"],"human_verified":False})
 before=jsonl(snapshot)
 if len(before)!=483 or {r["formulation_id"] for r in before}!=set(byid):
  raise PipelineError("Historical 483-formulation review snapshot invalid")
 prior={r["formulation_id"]:r for r in before}
 if prior[FORM_ID]["decision"]!="needs_review" or prior[FORM_ID]["relation_ids"]:
  raise PipelineError("Missing original pending review")
 revised={key:dict(row) for key,row in byid.items()}
 new=revised[FORM_ID]
 if new["decision"]=="needs_review":
  new["original_wave2_pending_reason"]=prior[FORM_ID]["editorial_reason"]
  new["decision"]="no_supported_target"
  new["editorial_reason"]=case["mathematical_reason"]
  new["source"]="wave2_individual_mathematical_no_supported_target_review"
  new["reviewed_by"]=case["reviewed_by"]
  new["human_verified"]=False
 if new["editorial_reason"]!=case["mathematical_reason"]:
  raise PipelineError("Existing source review conflicts with documented mathematics")
 for key in revised:
  if key!=FORM_ID and revised[key]!=prior[key]:
   raise PipelineError("Unrelated historical source review changed")
 events=[{"event_id":"wave2.absolutevalue.no_target."+FORM_ID,
    "formulation_id":FORM_ID,"old_decision":"needs_review",
    "old_mathematical_review_reason":prior[FORM_ID]["editorial_reason"],
    "new_decision":"no_supported_target",
    "mathematical_reason":case["mathematical_reason"],
    "source_locator":case["source_locator"],
    "missing_foundations":case["missing_foundations"],
    "human_verified":False}]
 events_path=w.root/"events/wave2_real_absolute_value_no_target_review.jsonl"
 event_text="".join(canonical(e)+"\n" for e in events)
 if events_path.exists() and events_path.read_text(encoding="utf-8")!=event_text:
  raise PipelineError("Historic review events conflict")
 events_path.write_text(event_text,encoding="utf-8")
 atomic_jsonl(p,[revised[k] for k in sorted(revised)])
 now=jsonl(p)
 counts=dict(Counter(r["decision"] for r in now))
 if counts!={"linked":474,"no_supported_target":9}:
  raise PipelineError("Incorrect post-review mathematical dispositions "+str(counts))
 if {rid for r in now for rid in r["relation_ids"]}!=set(relationships):
  raise PipelineError("Historical source-screened links lost")
 check_cycles(meanings,relationships)
 report={"phase":"single_real_absolute_value_mathematical_foundation_individually_reviewed",
   "screened_meanings":471,"reviewed_formulations":483,"screened_links":626,
   "review_dispositions":counts,"remaining_unreviewed":0,
   "original_483_formulation_review_snapshot_preserved":True,
   "future_real_ordered_field_foundation_research_needed":True,
   "original_planetmath_access_block_unchanged":True,
   "stages_sealed":0,"human_peer_verified":False,
   "original_production_corpus_consulted":False,
   "next":"Independently source real ordered fields, weighted polynomial/integration and measure foundations; never invent links to fill a statistic."}
 atomic_json(w.root/"state/wave2_real_absolute_value_dependency_review_complete.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 p.add_argument("--batch",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace,a.batch),indent=2))
if __name__=="__main__":
 main()
