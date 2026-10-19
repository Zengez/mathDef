"""Complete six individually reviewed no-supported-target Wave 2 analysis contexts.

No synonym-based guessed links, no Wave 1 changes. Preserve a full source and
original-formulation decision snapshot so missing foundations can later be
revisited only with exact source-screened evidence.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from collections import Counter
from .core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import locator,check_cycles

EXPECTED={
"form.wave2.analysis.antiderivative-on-interval",
"form.wave2.analysis.orthogonal-polynomials-countable",
"form.wave2.analysis.orthogonal-polynomials-finite",
"form.wave2.analysis.orthogonal-polynomials-interval",
"form.wave2.analysis.orthogonal-polynomials-measure",
"form.wave2.analysis.real-limit-punctured-epsilon-delta"
}
def run(root,batch):
 w=Workspace(root)
 if json.loads((w.root/"state/baseline.json").read_text()).get("mode")!="second_wave":
  raise PipelineError("Only independent second-wave source and review data allowed")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Cannot edit sealed research stages")
 meanings=w.records("meanings");observations=w.records("observations")
 if (len(meanings),len(w.records("relations"))) != (469,623):
  raise PipelineError("Requires verified seven-screen meaning catalog and one OpenStax prerequisite link")
 link=w.root/"state/wave2_link_review_batch_19.json"
 if not link.exists() or json.loads(link.read_text(encoding="utf-8"))["total_screened_links"]!=623:
  raise PipelineError("Audited antiderivative relationship not yet committed")
 incoming=jsonl(batch)
 if len(incoming)!=6 or {x.get("formulation_id") for x in incoming}!=EXPECTED:
  raise PipelineError("Exactly six source-specific individual no-target decisions needed")
 byform={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
 formids={f["id"] for m in meanings.values() for f in m["formulations"]}
 reviewed=w.root/"state/wave2_formulation_reviews.jsonl"
 earlier=jsonl(reviewed)
 byid={r["formulation_id"]:r for r in earlier}
 if len(earlier)!=481 or len(byid)!=481 or formids!=set(byid):
  raise PipelineError("Review ledger missing or duplicating mathematical forms")
 if any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in earlier):
  raise PipelineError("Historical meaning catalog digest is stale")
 linkset={id for row in earlier for id in row["relation_ids"]}
 if linkset!=set(w.records("relations")):
  raise PipelineError("Mathematical links are not all source-reviewed")
 # Validate every decision and exact independently observed source locator first.
 for case in incoming:
  fid=case["formulation_id"];meaning,form=byform[fid]
  review=byid[fid]
  if (meaning["id"]!=case["meaning_id"] or form["review_state"]!="screened" or
      review["relation_ids"] or
      review["decision"] not in ("needs_review","no_supported_target") or
      review.get("original_wave1_disposition") is not None):
   raise PipelineError("Cannot change an inherited or linked mathematical source review "+fid)
  if case["source_locator"]!=locator(meaning,observations):
   raise PipelineError("Unmatched source locator "+fid)
  if (case["decision"]!="no_supported_target" or len(case["mathematical_reason"])<165 or
      len(case.get("missing_foundations",[]))<3 or
      case.get("human_verified") is not False):
   raise PipelineError("Unjustified or exaggerated mathematics review "+fid)
  if review["decision"]=="no_supported_target":
   if (review.get("editorial_reason")!=case["mathematical_reason"] or
       review.get("original_wave2_pending_reason") is None):
    raise PipelineError("Previous reviewed no-target decision differs "+fid)
 # Preserve all 481 original dispositions and all 623 links.
 snapshot=w.root/"state/wave2_formulation_reviews_snapshot_481_before_analysis20_dependency_reviews.jsonl"
 snapshot_summary=w.root/"state/wave2_formulation_reviews_snapshot_481_before_analysis20_dependency_reviews.json"
 if not snapshot.exists():
  if any(byid[fid]["decision"]!="needs_review" for fid in EXPECTED):
   raise PipelineError("Original six pending review entries unavailable for snapshot")
  old=reviewed.read_text(encoding="utf-8")
  snapshot.write_text(old,encoding="utf-8")
  atomic_json(snapshot_summary,{"review_count":481,"links_preserved":623,
    "ledger_sha256":hashlib.sha256(old.encode("utf-8")).hexdigest(),
    "catalog_digest":earlier[0]["meaning_catalog_digest"],
    "human_verified":False})
 if len(jsonl(snapshot))!=481:
  raise PipelineError("Historical pending six-review snapshot invalid")
 original={r["formulation_id"]:r for r in jsonl(snapshot)}
 current={k:dict(v) for k,v in byid.items()}
 events=[]
 for case in incoming:
  fid=case["formulation_id"]
  previous=original[fid]
  review=current[fid]
  if review["decision"]=="needs_review":
   review["original_wave2_pending_reason"]=previous["editorial_reason"]
   review["decision"]="no_supported_target"
   review["editorial_reason"]=case["mathematical_reason"]
   review["reviewed_by"]=case["reviewed_by"]
   review["source"]="wave2_individual_mathematical_no_supported_target_review"
   review["human_verified"]=False
  events.append({"event_id":"wave2.analysis20.no_target."+fid,
     "formulation_id":fid,"original_review_decision":"needs_review",
     "original_pending_reason":previous["editorial_reason"],
     "decision":"no_supported_target","mathematical_reason":case["mathematical_reason"],
     "known_missing_prerequisites":case["missing_foundations"],
     "source_locator":case["source_locator"],"reviewed_by":case["reviewed_by"],
     "human_verified":False})
 for fid in current:
  if fid not in EXPECTED and current[fid]!=original[fid]:
   raise PipelineError("Unrelated mathematical review changed "+fid)
 if any(current[fid]["relation_ids"]!=original[fid]["relation_ids"] for fid in current):
  raise PipelineError("Existing screened dependency changed in a review-only process")
 eventfile=w.root/"events/wave2_analysis20_no_target_reviews.jsonl"
 payload="".join(canonical(row)+"\n" for row in sorted(events,key=lambda x:x["formulation_id"]))
 if eventfile.exists() and eventfile.read_text(encoding="utf-8")!=payload:
  raise PipelineError("Previous audit events conflict with new mathematical source review")
 eventfile.write_text(payload,encoding="utf-8")
 atomic_jsonl(reviewed,[current[k] for k in sorted(current)])
 now=jsonl(reviewed)
 counts=dict(Counter(r["decision"] for r in now))
 if len(now)!=481 or counts.get("needs_review",0)!=0 or counts.get("held_ambiguity",0)!=0:
  raise PipelineError("Some source formulations still lack an initial individual decision")
 if {id for r in now for id in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Unaccounted screened relationship")
 check_cycles(meanings,w.records("relations"))
 report={"phase":"seven_new_analysis20_dependency_reviews_completed",
   "individual_new_foundation_no_target_decisions":6,
   "one_sourced_antiderivative_relation_already_approved":True,
   "total_reviewed_formulations":481,"screened_relationships":623,
   "current_review_dispositions":counts,"pending_initial_reviews":0,
   "historical_481_review_snapshot_preserved":True,
   "unlinked_mathematical_foundations_explicitly_listed":True,
   "frozen_wave1_unmodified":True,"all_stages_unsealed":True,
   "human_peer_verified":False,"original_production_mathdef_consulted":False,
   "next":"Independently acquire mathematical definitions for derivatives, integration, measure, polynomial degree and real metrics; recheck no-target decisions after sources screen."}
 atomic_json(w.root/"state/wave2_analysis20_dependency_reviews_complete.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 p.add_argument("--batch",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace,a.batch),indent=2))
if __name__=="__main__":
 main()
