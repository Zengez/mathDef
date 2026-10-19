"""Finish four initial foundation dependency reviews WITHOUT inventing links.

Preserve 459 previously screened formulation-review rows by immutable snapshot,
then update only four evidence-documented needs_review cases as no-supported-
target. Do not close Wave 2 or imply a set-theoretic primitive has a definition.
"""
from __future__ import annotations
import argparse,json,hashlib
from collections import Counter
from pathlib import Path
from .core import Workspace,PipelineError,canonical,jsonl,atomic_json,digest
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import locator,check_cycles

EXPECTED={
 "form.wave2.foundation.cartesian-product-binary",
 "form.wave2.foundation.ordered-pair-kuratowski",
 "form.wave2.foundation.subset-nonstrict",
 "form.wave2.foundation.mapping-element-assignment"
}
def run(root):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
      ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Requires unsealed independently sourced Wave 2")
 report=w.root/"state/wave2_link_review_batch_08.json"
 if not report.exists() or json.loads(report.read_text(encoding="utf-8")).get("total_screened_links")!=582:
  raise PipelineError("Cannot review before exact eight new mapping relation links are committed")
 meanings=w.records("meanings")
 relations=w.records("relations")
 observations=w.records("observations")
 forms={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
 if len(meanings)!=447 or len(forms)!=459 or len(relations)!=582:
  raise PipelineError("Unexpected meaning/formulation/link count")
 decisions=jsonl(w.root/"wave2/foundation_no_supported_target_reviews_batch_02.jsonl")
 if len(decisions)!=4 or {d["formulation_id"] for d in decisions}!=EXPECTED:
  raise PipelineError("Exactly four independent foundation decisions required")
 review_path=w.root/"state/wave2_formulation_reviews.jsonl"
 previous=jsonl(review_path)
 index={r["formulation_id"]:r for r in previous}
 if len(previous)!=459 or len(index)!=459 or set(index)!=set(forms):
  raise PipelineError("Incomplete or duplicated 459 individual reviews")
 expected_digest=digest(list(meanings.values()))
 if any(x["meaning_catalog_digest"]!=expected_digest for x in previous):
  raise PipelineError("Historical meaning source digest no longer matches reviews")
 if {rid for r in previous for rid in r["relation_ids"]}!=set(relations):
  raise PipelineError("Earlier 582 source links missing review attribution")
 snapshot=w.root/"state/wave2_formulation_reviews_snapshot_459_before_no_target_batch02.jsonl"
 if not snapshot.exists():
  if any(index[fid]["decision"]!="needs_review" for fid in EXPECTED):
   raise PipelineError("Missing initial pending disposition for first no-target review")
  source=review_path.read_text(encoding="utf-8")
  snapshot.write_text(source,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_459_before_no_target_batch02.json",{
    "formulation_count":459,"screened_relation_count":582,
    "review_ledger_sha256":hashlib.sha256(source.encode("utf-8")).hexdigest(),
    "human_peer_verified":False})
 historical=jsonl(snapshot)
 old={r["formulation_id"]:r for r in historical}
 if len(old)!=459 or len(old)!=len(set(old)):
  raise PipelineError("459 original individual reviews were not preserved")
 for row in historical:
  if row["formulation_id"] not in EXPECTED and canonical(index[row["formulation_id"]])!=canonical(row):
   raise PipelineError("Unrelated prior mathematical review was changed")
 events=[]
 for item in decisions:
  fid=item["formulation_id"]
  record=index[fid]
  meaning,form=forms[fid]
  if item["meaning_id"]!=meaning["id"] or form["review_state"]!="screened":
   raise PipelineError("Missing mathematical source or incorrect formulation "+fid)
  if item.get("human_verified") is not False or item.get("original_production_mathdef_consulted") is not False:
   raise PipelineError("Unsupported peer verification or production source provenance")
  if item["decision"]!="no_supported_target" or len(item["mathematical_reason"])<240 or len(item.get("missing_candidates",[]))<2:
   raise PipelineError("Insufficient independent no-target mathematical rationale "+fid)
  if record["relation_ids"] or old[fid]["decision"]!="needs_review":
   raise PipelineError("Cannot erase an existing link or change a previously decided case "+fid)
  original_reason=old[fid]["editorial_reason"]
  if record["decision"] not in ("needs_review","no_supported_target"):
   raise PipelineError("Unexpected current formulation review state "+fid)
  if record["decision"]=="no_supported_target" and record["editorial_reason"]!=item["mathematical_reason"]:
   raise PipelineError("An already-finalized no-target reason was altered "+fid)
  if record["decision"]=="needs_review":
   record["original_wave2_pending_reason"]=original_reason
   record["decision"]="no_supported_target"
   record["editorial_reason"]=item["mathematical_reason"]
   record["source"]="wave2_individual_mathematical_no_supported_target_review"
   record["reviewed_by"]=item["reviewed_by"]
   record["human_verified"]=False
  events.append({
   "event_id":"wave2.source_no_target_review02."+fid,
   "formulation_id":fid,"meaning_id":meaning["id"],
   "source_locator":locator(meaning,observations),
   "historical_decision":"needs_review","current_decision":"no_supported_target",
   "initial_reason":original_reason,
   "new_mathematical_reason":item["mathematical_reason"],
   "missing_foundation_candidates":item["missing_candidates"],
   "future_research_action":item["future_research_action"],
   "source_specific_review":True,
   "human_verified":False
  })
 audited=w.root/"events/wave2_source_no_target_reviews_batch02.jsonl"
 payload=chr(10).join(canonical(x) for x in sorted(events,key=lambda r:r["formulation_id"]))+chr(10)
 if audited.exists() and audited.read_text(encoding="utf-8")!=payload:
  raise PipelineError("Existing mathematical review event payload differs")
 audited.write_text(payload,encoding="utf-8")
 if {r for x in index.values() for r in x["relation_ids"]}!=set(relations):
  raise PipelineError("Source-reviewed relations lost after mathematical decision")
 counts=dict(Counter(x["decision"] for x in index.values()))
 if counts!={"linked":444,"no_supported_target":14,"held_ambiguity":1}:
  raise PipelineError("Unexpected disposition counts "+str(counts))
 check_cycles(meanings,relations)
 atomic_jsonl(review_path,[index[k] for k in sorted(index)])
 report={
  "phase":"four_context_specific_set_and_mapping_formulations_reviewed_no_supported_target",
  "meaning_count":447,"formulation_count":459,
  "screened_relations_retained":582,
  "individual_new_no_target_reviews":4,
  "prior_review_rows_archived":459,
  "review_dispositions":counts,
  "formulation_reviews_without_initial_decision":0,
  "original_wave1_dispositions_preserved":True,
  "primitive_membership_not_fabricated_as_definition":True,
  "bare_graph_not_conflated_with_typed_function":True,
  "representation_choice_not_misrepresented_as_universal_dependency":True,
  "stages_unsealed":True,
  "original_production_mathdef_consulted":False,
  "human_peer_verified":False,
  "next":"Continue to research abstract ordered pairs, primitive membership and full map/graph equivalence; source-review still-unresolved mathematical gaps without forcing links."
 }
 atomic_json(w.root/"state/wave2_foundation_dependency_no_target_batch_02.json",report)
 return report

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--workspace",required=True,type=Path)
 a=ap.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
