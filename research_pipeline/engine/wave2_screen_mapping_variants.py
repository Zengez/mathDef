"""Individually review six mathematically distinct set/mapping source formulations.

Previous 453 reviews and 574 links are preserved. Alternative mapping/graph
representations remain distinct contexts under one display heading and the
element-assignment formulation has the preferred earlier educational order.
Do not read production mathDef definitions or compare its corpus.
"""
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
from collections import Counter
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

def run(root):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
   ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Only unsealed independent Wave 2 may be reviewed")
 report=w.root/"state/wave2_foundations_batch_08.json"
 if not report.exists() or json.loads(report.read_text(encoding="utf-8")).get("independently_sourced_terms")!=350:
  raise PipelineError("Mapping/set source acquisition must be committed first")
 if {k:len(w.records(k)) for k in ("terms","observations","relations")}!={"terms":350,"observations":773,"relations":574}:
  raise PipelineError("Unexpected source or reviewed relation counts")
 props=jsonl(w.root/"wave2/foundational_meaning_proposals_batch_09.jsonl")
 if len(props)!=6 or len({p["intended_formulation_id"] for p in props})!=6:
  raise PipelineError("Six independent source-context proposals are required")
 expected_ids={
  "meaning.wave2.foundation.ordered-pair-kuratowski",
  "meaning.wave2.foundation.subset-nonstrict",
  "meaning.wave2.foundation.subset-proper",
  "meaning.wave2.foundation.mapping-element-assignment",
  "meaning.wave2.foundation.mapping-typed-graph",
  "meaning.wave2.foundation.mapping-bare-graph"}
 if {p["intended_meaning_id"] for p in props}!=expected_ids:
  raise PipelineError("Missing a contextual variant or introducing unexpected mathematical claim")
 obs=w.records("observations");terms=w.records("terms")
 incoming=[]
 for p in props:
  t=terms.get(p["source_term_id"]);o=obs.get(p["source_observation_id"])
  if not t or not o or t["locator"]!=p["source_locator"] or o["locator"]!=p["source_locator"]:
   raise PipelineError("Wrong independent source evidence "+p["proposal_id"])
  if o["term_id"]!=t["id"] or o["record_kind"]!="paraphrase" or p.get("formulation_screened") is not False or p.get("human_verified") is not False:
   raise PipelineError("Candidate not sufficiently source-screened")
  if p.get("source_read_directly") is not True or p.get("original_production_consulted") is not False:
   raise PipelineError("Unacceptable source lineage")
  if len(p["mathematical_review_note"])<130 or len(p["text"])<120:
   raise PipelineError("Insufficient independent mathematical justification")
  if p["intended_meaning_id"]!=p["intended_formulation_id"].replace("form.","meaning.",1):
   raise PipelineError("Meaning/formulation identity mismatch")
  incoming.append({
   "id":p["intended_meaning_id"],"term_group_id":p["term_group_id"],
   "display_term":p["display_term"],"context":p["context"],"term_ids":[t["id"]],
   "formulations":[{"id":p["intended_formulation_id"],"text":p["text"],
     "evidence_ids":[o["id"]],"review_state":"candidate",
     "educational_order_hint":p["educational_order_hint"],
     "variant_label":p["variant_label"],
     "mathematical_scope_note":p["mathematical_review_note"],
     "human_verified":False}],
   "human_verified":False,"editorial_status":"individual_review_required"
  })
 by={x["id"]:x for x in incoming}
 assignments=["mapping-element-assignment","mapping-typed-graph","mapping-bare-graph"]
 if not (by["meaning.wave2.foundation."+assignments[0]]["term_group_id"]==
         by["meaning.wave2.foundation."+assignments[1]]["term_group_id"]==
         by["meaning.wave2.foundation."+assignments[2]]["term_group_id"]):
  raise PipelineError("Function variants were split under different display terms")
 if sorted(by["meaning.wave2.foundation."+n]["formulations"][0]["educational_order_hint"]
            for n in assignments)!=[1,2,3]:
  raise PipelineError("Pedagogical mapping representation order is inconsistent")
 def store(p,rows):
  p.parent.mkdir(parents=True,exist_ok=True)
  payload=chr(10).join(canonical(x) for x in rows)+chr(10)
  if p.exists() and p.read_text(encoding="utf-8")!=payload:
   raise PipelineError("Conflicting source-specific intake/review history")
  p.write_text(payload,encoding="utf-8")
  return p
 src=store(w.root/"intake/wave2_foundational_meanings_batch_09.jsonl",incoming)
 old_meanings=w.records("meanings")
 if len(old_meanings)==441:
  w.ingest("meanings",src,batch_size=6)
 elif len(old_meanings)==447:
  for c in incoming:
   m=old_meanings.get(c["id"])
   if not m or m["formulations"][0]["text"]!=c["formulations"][0]["text"]:
    raise PipelineError("Resumed mathematical formulation differs")
 else:
  raise PipelineError("Unexpected prior contextual meaning count")
 events=[]
 for p in props:
  mid=p["intended_meaning_id"]
  m=w.records("meanings")[mid]
  f=m["formulations"][0]
  ev={
   "meaning_id":mid,"formulation_id":f["id"],"source_url":p["source_locator"],
   "observation_id":p["source_observation_id"],
   "educational_order_hint":p["educational_order_hint"],
   "distinct_convention_note":p["mathematical_review_note"],
   "decision":"screen_exact_source_scoped_mathematical_formulation",
   "human_verified":False,"reviewed_by":"assistant_independent_set_mapping_mathematical_review_2026_10_19"
  }
  events.append(ev)
  if f["review_state"]=="screened":
   if m.get("editorial_screening_reason")!=p["mathematical_review_note"]:
    raise PipelineError("Re-review reason differs from previously screened meaning")
   continue
  if f["review_state"]!="candidate":
   raise PipelineError("Formulation not eligible for screening")
  corrected=dict(m)
  corrected["formulations"]=[dict(f,review_state="screened",
      source_screened_by=ev["reviewed_by"],human_verified=False)]
  corrected["editorial_screening_reason"]=p["mathematical_review_note"]
  corrected["editorial_status"]="independent_mathematical_source_context_screened"
  corrected["human_verified"]=False
  apply_revision(w.root,{
    "event_id":"revision.wave2.foundation09."+p["intended_meaning_id"].split(".")[-1]+".screen01",
    "stage":"meanings","record_id":mid,
    "before_digest":digest(m),"editor":ev["reviewed_by"],
    "reason":p["mathematical_review_note"],"operation":"replace","replacement":corrected})
 store(w.root/"wave2/foundation_meaning_review_batch_05.jsonl",events)
 meaning=w.records("meanings")
 allforms={f["id"]:m["id"] for m in meaning.values() for f in m["formulations"]}
 if len(meaning)!=447 or len(allforms)!=459 or any(f["review_state"]!="screened" for m in meaning.values() for f in m["formulations"]):
  raise PipelineError("Incomplete new mapping/set source review")
 current=w.root/"state/wave2_formulation_reviews.jsonl"
 prior=jsonl(current)
 snapshot=w.root/"state/wave2_formulation_reviews_snapshot_453_before_foundations09.jsonl"
 if len(prior)==453:
  oldmap={x["formulation_id"]:x for x in prior}
  if len(oldmap)!=453 or {id for r in prior for id in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Original 453 relation reviews or 574 links incomplete")
  oldtext=current.read_text(encoding="utf-8")
  if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=oldtext:
   raise PipelineError("Prior immutable review snapshot differs")
  snapshot.write_text(oldtext,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_453_before_foundations09.json",{
    "formulation_count":453,"screened_relation_count":574,
    "sha256":hashlib.sha256(oldtext.encode("utf-8")).hexdigest(),
    "prior_meaning_catalog_digest":prior[0]["meaning_catalog_digest"],
    "human_verified":False})
  target_digest=digest(list(meaning.values()))
  nextrows=[dict(r,meaning_catalog_digest=target_digest) for r in prior]
  for m in incoming:
   nextrows.append({
    "meaning_id":m["id"],"formulation_id":m["formulations"][0]["id"],
    "meaning_catalog_digest":target_digest,"decision":"needs_review",
    "relation_ids":[],"original_wave1_disposition":None,
    "source":"new_independent_source_screened_foundation09",
    "editorial_reason":"New source-specific elementary definition requires individual screened mathematical prerequisite review.",
    "reviewed_by":None,"human_verified":False})
  atomic_jsonl(current,sorted(nextrows,key=lambda x:x["formulation_id"]))
 elif len(prior)==459:
  if not snapshot.exists() or any(x["meaning_catalog_digest"]!=digest(list(meaning.values())) for x in prior):
   raise PipelineError("Cannot rebase previously expanded mathematical review ledger")
 else:
  raise PipelineError("Unexpected historical formulation review count")
 old=jsonl(snapshot);now=jsonl(current);newmap={x["formulation_id"]:x for x in now}
 if len(old)!=453 or len(now)!=459 or len(newmap)!=459:
  raise PipelineError("Source review identity lost")
 for x in old:
  item=newmap.get(x["formulation_id"])
  if not item or any(item.get(k)!=v for k,v in x.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Previously reviewed source and dependency decision altered")
 if {id for x in now for id in x["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Screened link missing supporting review")
 check_cycles(meaning,w.records("relations"))
 summary=dict(Counter(x["decision"] for x in now))
 if summary!={"linked":440,"no_supported_target":11,"held_ambiguity":1,"needs_review":7}:
  raise PipelineError("Unexpected review disposition changes "+str(summary))
 s=w.state("meanings")
 s.update(total=447,record_digest=digest(list(meaning.values())),
   screened_new_formulations=28,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",s)
 report={
  "phase":"six_new_mapping_subset_and_ordered_pair_contexts_screened",
  "independently_screened_meanings":447,"individually_reviewed_formulations":459,
  "prior_review_entries_preserved":453,
  "screened_relations_preserved":574,
  "new_meanings":6,"new_prerequisite_reviews_pending":6,
  "all_pending_review_count":summary["needs_review"],
  "review_dispositions":summary,
  "mapping_assigned_first_educational_order":True,
  "typed_graph_and_bare_graph_separate_conventions":True,
  "ordered_pair_encoding_preserved_as_kuratowski_variant":True,
  "no_automatic_dependency_links_created":True,
  "human_peer_verified":False,
  "all_wave2_stages_unsealed":True,
  "original_production_mathdef_consulted":False,
  "next":"Individually review source-anchored mapping, Cartesian-product and subset relations; do not conflate equivalent graphs with equal typed functions."
 }
 atomic_json(w.root/"state/wave2_foundations_batch_09_screened.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
