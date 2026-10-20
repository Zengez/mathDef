"""Individually screen strongly transcendental element over a subring, Stacks 10.123.7.

Requires separately committed direct source observation and explicit historical
491-formulation review snapshot. Does not automatically accept any dependency.
"""
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

KEY="strongly-transcendental-subring-element"
SOURCE="https://stacks.math.columbia.edu/tag/00PZ"
TERM="term.wave2.foundation36."+KEY
OBS="obs.wave2.foundation36."+KEY
MID="meaning.wave2.foundation."+KEY
FID="form.wave2.foundation."+KEY
BODY="Let R⊆S be an inclusion of commutative rings with identity, and let x∈S. The element x is strongly transcendental over R if for every integer n≥0, coefficients a_0,…,a_n∈R, and u∈S, the equation u(a_0+a_1x+⋯+a_nx^n)=0 implies ua_i=0 for every i=0,…,n."
REASON=("Stacks Definition 10.123.7 defines strong transcendence via all finite R-polynomial relations after multiplication by an arbitrary element u of S. "
 "The conclusion is that each coefficient a_i is annihilated by the same u. This is strictly context-sensitive over rings with zero divisors: "
 "one may not silently replace the condition by ordinary polynomial algebraic independence. The cited note relates the notions in integral domains using fields of fractions.")
def run(root):
 w=Workspace(root)
 base=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if base.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
    ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Independent unsealed Wave 2 meaning review required")
 source=w.root/"state/wave2_foundations_batch_36.json"
 if not source.exists() or not json.loads(source.read_text(encoding="utf-8")).get("zero_divisor_sensitive_coefficient_condition_preserved"):
  raise PipelineError("Missing exact Stacks direct-source observation")
 if any(len(w.records(stage))!=count for stage,count in
    (("sources",9),("terms",377),("observations",800),("relations",648))):
  raise PipelineError("Source and relationship baselines changed")
 old=w.records("meanings")
 if len(old) not in (479,480):
  raise PipelineError("Unexpected mathematical meaning baseline")
 term=w.records("terms").get(TERM)
 obs=w.records("observations").get(OBS)
 if not term or not obs or term["locator"]!=SOURCE or obs["locator"]!=SOURCE or obs["term_id"]!=TERM or obs["record_kind"]!="paraphrase" or obs["human_verified"] is not False:
  raise PipelineError("Exact Stacks 10.123.7 evidence missing")
 if len(REASON)<185 or len(BODY)<185:
  raise PipelineError("Definition or mathematical justification too short")
 record={"id":MID,"display_term":"strongly transcendental element over a subring",
  "term_group_id":"wave2.foundation."+KEY,"context":"Stacks 10.123.7: strong transcendence under a commutative ring inclusion, with annihilators and potential zero divisors",
  "term_ids":[TERM],"human_verified":False,
  "editorial_status":"candidate_individual_mathematical_screen",
  "formulations":[{"id":FID,"text":BODY,"evidence_ids":[OBS],"review_state":"candidate","human_verified":False}]}
 candidate=w.root/"intake/foundations_batch_37_meaning_candidates.jsonl"
 candidate.parent.mkdir(parents=True,exist_ok=True)
 data=canonical(record)+"\n"
 if candidate.exists() and candidate.read_text(encoding="utf-8")!=data:
  raise PipelineError("Previously supplied contextual meaning changed")
 candidate.write_text(data,encoding="utf-8")
 if len(old)==479:
  w.ingest("meanings",candidate,batch_size=1)
 elif old.get(MID,{}).get("formulations",[{}])[0].get("text")!=BODY:
  raise PipelineError("Previously screened meaning text differs")
 m=w.records("meanings")[MID];f=m["formulations"][0]
 if f["review_state"]=="candidate":
  revised=dict(m)
  revised["formulations"]=[dict(f,review_state="screened",
     source_screened_by="assistant_independent_stacks_strong_transcendence_review_2026_10_20",
     human_verified=False)]
  revised["editorial_screening_reason"]=REASON
  revised["editorial_status"]="source_scoped_meaning_individually_screened"
  revised["human_verified"]=False
  apply_revision(w.root,{
   "event_id":"revision.wave2.strong_transcendence37.screen01",
   "stage":"meanings","record_id":MID,"before_digest":digest(m),
   "editor":"assistant_independent_stacks_strong_transcendence_review_2026_10_20",
   "reason":REASON,"operation":"replace","replacement":revised})
 elif f["review_state"]!="screened" or m.get("editorial_screening_reason")!=REASON:
  raise PipelineError("Existing screened meaning review differs")
 meaning=w.records("meanings")
 forms={f["id"]:m["id"] for m in meaning.values() for f in m["formulations"]}
 if len(meaning)!=480 or len(forms)!=492 or any(f["review_state"]!="screened" for m in meaning.values() for f in m["formulations"]):
  raise PipelineError("Incorrect new mathematical catalog cardinality or state")
 ledger=w.root/"state/wave2_formulation_reviews.jsonl"
 oldreviews=jsonl(ledger)
 snap=w.root/"state/wave2_formulation_reviews_snapshot_491_before_strong_transcendence37.jsonl"
 if len(oldreviews)==491:
  if len({r["formulation_id"] for r in oldreviews})!=491 or {rid for r in oldreviews for rid in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Prior 491 per-formulation reviewed links incomplete")
  oldtext=ledger.read_text(encoding="utf-8")
  if snap.exists() and snap.read_text(encoding="utf-8")!=oldtext:
   raise PipelineError("Immutable source ledger snapshot mismatch")
  snap.write_text(oldtext,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_491_before_strong_transcendence37.json",{
   "review_count":491,"prior_links":648,
   "sha256":hashlib.sha256(oldtext.encode("utf-8")).hexdigest(),"human_peer_verified":False})
  updated=[dict(r,meaning_catalog_digest=digest(list(meaning.values()))) for r in oldreviews]
  updated.append({"formulation_id":FID,"meaning_id":MID,
   "meaning_catalog_digest":digest(list(meaning.values())),"decision":"needs_review",
   "relation_ids":[],"original_wave1_disposition":None,
   "source":"independent_stacks_numbered_definition_source_review",
   "editorial_reason":"Definition source-screened; independently justify each prerequisite without assuming ordinary algebraic transcendence or a domain.",
   "reviewed_by":None,"human_verified":False})
  atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
 elif len(oldreviews)==492:
  if not snap.exists() or any(r["meaning_catalog_digest"]!=digest(list(meaning.values())) for r in oldreviews):
   raise PipelineError("Existing screened meaning review catalog inconsistent")
 else:raise PipelineError("Unexpected formulation review baseline")
 oldrows=jsonl(snap);newrows=jsonl(ledger);now={r["formulation_id"]:r for r in newrows}
 if len(oldrows)!=491 or len(newrows)!=492 or len(now)!=492:raise PipelineError("Missing historical review")
 for r in oldrows:
  curr=now.get(r["formulation_id"])
  if not curr or any(curr.get(k)!=v for k,v in r.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Prior independently screened review decision mutated")
 if {rid for r in newrows for rid in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Historical mathematical dependency lost source formulation provenance")
 if sum(r["decision"]=="needs_review" for r in newrows)!=1:
  raise PipelineError("Expected exactly one new prerequisite review")
 check_cycles(meaning,w.records("relations"))
 state=w.state("meanings")
 state.update(total=480,record_digest=digest(list(meaning.values())),
   screened_new_formulations=61,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 result={"phase":"stacks_strongly_transcendental_element_source_screened",
  "screened_meanings":480,"individually_reviewed_formulations":492,
  "new_stacks_meaning_screened":1,"previous_491_formulation_reviews_preserved":True,
  "previous_648_links_preserved":True,"new_relationship_reviews_pending":1,
  "source_scoped_zero_divisor_condition_unchanged":True,"stages_unsealed":True,
  "human_peer_verified":False,"production_corpus_consulted":False,
  "next":"Individually justify ring inclusion and algebraic ring prerequisites without forcing integral-domain hypotheses; preserve original review history."}
 atomic_json(w.root/"state/wave2_strong_transcendence37_meaning_screen.json",result)
 return result

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--workspace",required=True,type=Path)
 a=ap.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
