"""Review six context-specific meaning candidates from four independently read ProofWiki pages.

Never conflate typed relations with graph-only relations or external binary
operations with internal ones. Run only after the earlier 18-link Stacks batch,
all four source observations, and the 347-term source-review ledger are committed.
Preserve every earlier formulation review and every screened dependency link.
"""
from __future__ import annotations
import argparse,json,hashlib
from collections import Counter
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

def run(root):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
   ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Requires an unsealed independent Wave 2 workspace")
 expected={"sources":9,"terms":347,"observations":770,"relations":563}
 if any(len(w.records(s))!=n for s,n in expected.items()):
  raise PipelineError("Previous source intake and dependency screening not committed")
 first=w.root/"state/wave2_foundations_batch_06.json"
 previous=w.root/"state/wave2_link_review_batch_06.json"
 if not first.exists() or not previous.exists():
  raise PipelineError("Missing verified prior source/relationship reports")
 if json.loads(previous.read_text(encoding="utf-8")).get("total_screened_links")!=563:
  raise PipelineError("Incorrect preceding relationship batch")
 proposals=jsonl(w.root/"wave2/foundational_meaning_proposals_batch_07.jsonl")
 if len(proposals)!=6 or len({p["intended_formulation_id"] for p in proposals})!=6:
  raise PipelineError("Exactly six unique individually reviewed contexts expected")
 terms,obs=w.records("terms"),w.records("observations")
 outcomes=[]
 for p in proposals:
  t=terms.get(p["source_term_id"]);o=obs.get(p["source_observation_id"])
  if not t or not o or t["locator"]!=p["source_url"] or o["locator"]!=p["source_url"]:
   raise PipelineError("Missing direct approved source evidence "+p["proposal_id"])
  if o["term_id"]!=t["id"] or o["record_kind"]!="paraphrase" or
      p["source_reference_verified_directly"] is not True or
      p["formulation_screened"] is not False or p["editorial_peer_verified"] is not False:
   raise PipelineError("Unscreened source convention falsely promoted")
  if len(p["mathematical_review_note"])<85 or len(p["text"])<120:
   raise PipelineError("Insufficient mathematical rationale or definition")
  if p["intended_meaning_id"]!=p["intended_formulation_id"].replace("form.","meaning.",1):
   raise PipelineError("Meaning/formulation identity mismatch")
  outcomes.append({
   "id":p["intended_meaning_id"],"term_group_id":p["term_group_id"],
   "display_term":p["display_term"],"context":p["context"],
   "term_ids":[t["id"]], "human_verified":False,
   "editorial_status":"candidate_to_be_source_screened",
   "formulations":[{
     "id":p["intended_formulation_id"],"text":p["text"],
     "evidence_ids":[o["id"]],"review_state":"candidate",
     "mathematical_scope_note":p["mathematical_review_note"],"human_verified":False
   }]
  })
 bykey={x["id"]:x for x in outcomes}
 assert len(bykey)==6
 # Distinct mathematical objects: do not merge alternatives as literal equality.
 expectedcontexts={
   "meaning.wave2.foundation.binary-operation-general",
   "meaning.wave2.foundation.binary-operation-internal",
   "meaning.wave2.foundation.binary-relation-typed",
   "meaning.wave2.foundation.binary-relation-subset"}
 if not expectedcontexts.issubset(bykey):
  raise PipelineError("Lost an important distinct source convention")
 if (bykey["meaning.wave2.foundation.binary-operation-general"]["term_group_id"] !=
     bykey["meaning.wave2.foundation.binary-operation-internal"]["term_group_id"]):
  raise PipelineError("Two operation variants must remain grouped")
 if (bykey["meaning.wave2.foundation.binary-relation-typed"]["term_group_id"] !=
     bykey["meaning.wave2.foundation.binary-relation-subset"]["term_group_id"]):
  raise PipelineError("Two relation variants must remain grouped")
 def store(path,records):
  path.parent.mkdir(parents=True,exist_ok=True)
  payload=chr(10).join(canonical(x) for x in records)+chr(10)
  if path.exists() and path.read_text(encoding="utf-8")!=payload:
   raise PipelineError("Attempted to rewrite immutable source research batch")
  path.write_text(payload,encoding="utf-8")
  return path
 candidate_path=store(w.root/"intake/wave2_foundational_meanings_batch_07.jsonl",outcomes)
 original=w.records("meanings")
 if len(original)==435:
  w.ingest("meanings",candidate_path,batch_size=6)
 elif len(original)==441:
  for c in outcomes:
   m=original.get(c["id"])
   if not m or m["formulations"][0]["text"]!=c["formulations"][0]["text"]:
    raise PipelineError("Existing context candidate differs from initial screened content")
 else:
  raise PipelineError("Unexpected source-scoped meaning count")
 review_events=[]
 for p in proposals:
  mid=p["intended_meaning_id"]
  meaning=w.records("meanings")[mid]
  form=meaning["formulations"][0]
  reason=p["mathematical_review_note"]
  record={
   "formulation_id":form["id"],"meaning_id":mid,
   "source_url":p["source_url"],"source_observation_id":p["source_observation_id"],
   "distinct_context":p["context"],"mathematical_reason":reason,
   "decision":"source_specific_context_screened_not_asserted_identical_to_alternate_convention",
   "human_verified":False,
   "reviewed_by":"assistant_independent_source_mathematical_screen_2026_10_19"}
  review_events.append(record)
  if form["review_state"]=="screened":
   if meaning.get("editorial_screening_reason")!=reason:
    raise PipelineError("Previously screened rationale differs")
   continue
  if form["review_state"]!="candidate":
   raise PipelineError("Only candidates may be independently screened")
  revised=dict(meaning)
  revised["formulations"]=[dict(form,review_state="screened",
      source_screened_by=record["reviewed_by"],human_verified=False)]
  revised["editorial_status"]="source_scoped_mathematical_formulation_screened"
  revised["editorial_screening_reason"]=reason
  revised["human_verified"]=False
  apply_revision(w.root,{
    "event_id":"revision.wave2.foundation07."+p["scope_kind"]+".screen01",
    "stage":"meanings","record_id":mid,
    "before_digest":digest(meaning),
    "editor":record["reviewed_by"],"reason":reason,
    "operation":"replace","replacement":revised})
 store(w.root/"wave2/foundation_meaning_review_batch_04.jsonl",review_events)
 meanings=w.records("meanings")
 forms={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
 if len(meanings)!=441 or len(forms)!=453 or any(f["review_state"]!="screened" for
     m in meanings.values() for f in m["formulations"]):
  raise PipelineError("Inconsistent six-context source screen")
 current=w.root/"state/wave2_formulation_reviews.jsonl"
 prior=jsonl(current)
 oldsnapshot=w.root/"state/wave2_formulation_reviews_snapshot_447_before_foundations07.jsonl"
 if len(prior)==447:
  oldmap={p["formulation_id"]:p for p in prior}
  if len(oldmap)!=447 or {x for r in prior for x in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Historical 447 independent reviews incomplete")
  src=current.read_text(encoding="utf-8")
  if oldsnapshot.exists() and oldsnapshot.read_text(encoding="utf-8")!=src:
   raise PipelineError("Conflicting preserved 447-review ledger")
  oldsnapshot.write_text(src,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_447_before_foundations07.json",{
    "review_count":447,"screened_links":563,
    "sha256":hashlib.sha256(src.encode("utf-8")).hexdigest(),
    "previous_meaning_digest":prior[0]["meaning_catalog_digest"],
    "human_peer_verified":False})
  new_digest=digest(list(meanings.values()))
  nextrows=[dict(r,meaning_catalog_digest=new_digest) for r in prior]
  for m in outcomes:
   nextrows.append({
     "formulation_id":m["formulations"][0]["id"],"meaning_id":m["id"],
     "meaning_catalog_digest":new_digest,"decision":"needs_review","relation_ids":[],
     "original_wave1_disposition":None,"source":"individually_screened_proofwiki_foundation07",
     "editorial_reason":"This newly added context-specific formulation awaits separately justified source-anchored prerequisites.",
     "reviewed_by":None,"human_verified":False})
  atomic_jsonl(current,sorted(nextrows,key=lambda r:r["formulation_id"]))
 elif len(prior)==453:
  if not oldsnapshot.exists() or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in prior):
   raise PipelineError("Unrecoverable previously migrated review catalog")
 else:
  raise PipelineError("Missing baseline of 447 formulation reviews")
 old=jsonl(oldsnapshot)
 fresh=jsonl(current)
 newmap={r["formulation_id"]:r for r in fresh}
 if len(old)!=447 or len(fresh)!=453 or len(newmap)!=453:
  raise PipelineError("Review-history count inconsistent")
 for r in old:
  new=newmap.get(r["formulation_id"])
  if not new or any(new.get(k)!=v for k,v in r.items() if k!="meaning_catalog_digest"):
   raise PipelineError("An inherited formulation review was changed")
 if {rid for r in fresh for rid in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Link source review coverage lost")
 check_cycles(meanings,w.records("relations"))
 dispositions=dict(Counter(r["decision"] for r in fresh))
 if dispositions!={"linked":431,"no_supported_target":20,"held_ambiguity":2,"needs_review":6}:
  # The exact count may be revised after independently verified Stage 6;
  # require no inconsistency, rather than silently normalize history.
  if sum(dispositions.values())!=453 or dispositions.get("needs_review")!=6:
   raise PipelineError("Inconsistent new candidate link-review state "+str(dispositions))
 state=w.state("meanings")
 state.update(total=441,record_digest=digest(list(meanings.values())),
     screened_new_formulations=22,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 report={
  "phase":"six_source_scoped_elementary_foundations_screened",
  "independently_screened_meanings":441,
  "total_formulations":453,
  "new_contextual_meanings":6,
  "historical_review_rows_preserved":447,
  "screened_links_unchanged":563,
  "new_unlinked_formulations_awaiting_dependency_review":6,
  "review_dispositions":dispositions,
  "binary_operation_and_relation_variants_kept_separate":True,
  "zero_automatically_accepted_links":True,
  "source_stages_remain_unsealed":True,
  "human_peer_verified":False,
  "original_production_mathdef_consulted":False,
  "next":"Research exact source anchors for group and monoid operations, preorders and binary relations, and cross-definition terms before further individual link screening."
 }
 atomic_json(w.root/"state/wave2_foundations_batch_07_screened.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
