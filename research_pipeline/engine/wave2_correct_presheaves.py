"""Mathematically correct two Stacks presheaf formulations in independent Wave 2.

Two-step audited revisions: change text -> candidate, re-review -> screened.
Snapshot the 443-formulation relation review ledger before rebasing its catalog
digest; protect all 545 screened relationships and prior relation dispositions.
Do not alter the frozen independent Wave 1 or production mathDef definitions.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from .core import Workspace, PipelineError, canonical, digest, jsonl, atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

CASES = [
 dict(
  slug="category-valued-presheaf",
  mid="meaning.f7206eb9332b9389.category-valued-presheaf",
  fid="form.f7206eb9332b9389.category-valued-presheaf",
  source="https://stacks.math.columbia.edu/tag/02XU",
  old="A category-valued presheaf on C is a contravariant functor C^op→Cat, assigning a category to each object and compatible pullback functors to arrows in the base.",
  new="A (strict) category-valued presheaf on a category C is a functor F:C^op→Cat (equivalently, a contravariant functor from C to Cat). It assigns a category F(U) to each object U and a pullback functor f*:F(U)→F(V) to every arrow f:V→U, with (f∘g)*=g*∘f* and (id_U)* the identity functor.",
  context="Strict category-valued presheaf in Stacks Section 4.36, Example 4.36.1: functor from the opposite category, not a second contravariant functor from C^op",
  reason="Stacks Example 4.36.1 explicitly uses an ordinary functor C^op→Cat with strict composition of pullback functors. Saying 'contravariant functor C^op→Cat' incorrectly reverses variance twice. The revised formulation preserves the valid contravariant-functor prerequisite by saying contravariant FROM C. All previously screened source links remain mathematically applicable.",
  decision="linked",
 ),
 dict(
  slug="groupoid-valued-presheaf",
  mid="meaning.f0d993a60533fc99.groupoid-valued-presheaf",
  fid="form.f0d993a60533fc99.groupoid-valued-presheaf",
  source="https://stacks.math.columbia.edu/tag/0048",
  old="A groupoid-valued presheaf on a category C is a contravariant pseudofunctor assigning a groupoid F(U) to each object U of C and compatible pullback functors F(U)→F(V) to arrows V→U.",
  new="A (strict) groupoid-valued presheaf on a category C is a functor F:C^op→Groupoids, assigning a groupoid F(U) to every object U and a pullback functor f*:F(U)→F(V) to each arrow f:V→U. Pullbacks preserve identities and compose strictly: (f∘g)*=g*∘f*.",
  context="Strict functor-valued presheaf in Stacks Section 4.37, Example 4.37.1; pseudofunctors with nontrivial coherence data are a separate context not established by this source",
  reason="Stacks Example 4.37.1 explicitly assumes a functor C^op→Groupoids and strict equality of pullback compositions. The inherited citation does not support an unrestricted contravariant pseudofunctor; the revised formulation is deliberately strict, and any weak/coherent pseudofunctor variant requires an independent source. Retain the historical held-link decision until its new strict prerequisite is reviewed.",
  decision="held_ambiguity",
 )
]

def run(root):
 w=Workspace(root)
 baseline=w.root/"state/baseline.json"
 if not baseline.exists() or json.loads(baseline.read_text(encoding="utf-8")).get("mode")!="second_wave":
  raise PipelineError("Requires independent Wave 2 fork")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Cannot correct sealed Wave 2")
 if len(w.records("relations"))!=545 or len(w.records("meanings"))!=431:
  raise PipelineError("Unexpected pre-correction meaning or relationship count")
 prior_reviews_path=w.root/"state/wave2_formulation_reviews.jsonl"
 prior_reviews=jsonl(prior_reviews_path)
 byid={r["formulation_id"]:r for r in prior_reviews}
 if len(prior_reviews)!=443 or len(byid)!=443:
  raise PipelineError("Need all 443 existing independent formulation dispositions")
 for case in CASES:
  review=byid.get(case["fid"])
  if not review or review["decision"]!=case["decision"]:
   raise PipelineError("Inherited decision changed for "+case["slug"])
  if (case["slug"]=="category-valued-presheaf" and
      review["relation_ids"]!=["rel.stage5.category-valued-presheaf.to.contravariant-functor"]):
   raise PipelineError("Unexpected existing category-valued link")
  m=w.records("meanings")[case["mid"]]
  if m["source_citation"]["url"]!=case["source"] or len(m["formulations"])!=1:
   raise PipelineError("Unexpected sourced meaning "+case["slug"])
  form=m["formulations"][0]
  if form["id"]!=case["fid"] or form["text"] not in (case["old"],case["new"]):
   raise PipelineError("Incompatible original formulation "+case["slug"])
  if len(case["reason"])<170:
   raise PipelineError("Insufficient mathematical review rationale")
  if form["text"]==case["old"]:
   cand=dict(m)
   cand["formulations"]=[dict(form,text=case["new"],review_state="candidate",human_verified=False)]
   cand["context"]=case["context"]
   cand["editorial_status"]="under_wave2_source_reexamination"
   apply_revision(w.root,{
     "event_id":"revision.wave2.mathcorrection."+case["slug"]+".candidate01",
     "stage":"meanings","record_id":case["mid"],"before_digest":digest(m),
     "editor":"assistant_independent_stacks_mathematical_review_2026_10_19",
     "reason":case["reason"],"operation":"replace","replacement":cand
   })
  current=w.records("meanings")[case["mid"]]
  cf=current["formulations"][0]
  if cf["text"]!=case["new"]:
   raise PipelineError("Candidate text mismatch after audited revision")
  if cf["review_state"]=="candidate":
   reviewed=dict(current)
   reviewed["formulations"]=[dict(cf,review_state="screened",
       source_screened_by="assistant_independent_stacks_mathematical_review_2026_10_19",
       human_verified=False)]
   reviewed["editorial_status"]="wave2_formulation_source_corrected_and_individually_rescreened"
   reviewed["editorial_screening_reason"]=case["reason"]
   reviewed["context"]=case["context"]
   reviewed["human_verified"]=False
   apply_revision(w.root,{
     "event_id":"revision.wave2.mathcorrection."+case["slug"]+".screen01",
     "stage":"meanings","record_id":case["mid"],"before_digest":digest(current),
     "editor":"assistant_independent_stacks_mathematical_review_2026_10_19",
     "reason":case["reason"],"operation":"replace","replacement":reviewed
   })
  if w.records("meanings")[case["mid"]]["formulations"][0]["review_state"]!="screened":
   raise PipelineError("Re-reviewed meaning was not screened")

 meanings=w.records("meanings")
 if len(meanings)!=431 or sum(len(m["formulations"]) for m in meanings.values())!=443:
  raise PipelineError("Meaning catalog cardinality unexpectedly altered")
 revised_catalog=digest(list(meanings.values()))
 relations=w.records("relations")
 if len(relations)!=545:
  raise PipelineError("Existing source-reviewed relationships changed")
 # Preserve the original 443-entry reviewed decisions as an immutable snapshot.
 snap=w.root/"state/wave2_formulation_reviews_snapshot_443_before_presheaf_correction.jsonl"
 old_content=prior_reviews_path.read_text(encoding="utf-8")
 current_reviews=jsonl(prior_reviews_path)
 if not snap.exists():
  if current_reviews!=prior_reviews:
   raise PipelineError("Unable to snapshot original review decisions")
  snap.write_text(old_content,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_443_before_presheaf_correction.json",{
   "formulations":443,"relationships":545,
   "review_ledger_sha256":hashlib.sha256(old_content.encode("utf-8")).hexdigest(),
   "old_meaning_catalog_digest":prior_reviews[0]["meaning_catalog_digest"],
   "human_peer_verified":False
  })
 historical=jsonl(snap)
 if len(historical)!=443:
  raise PipelineError("Incomplete 443 historical snapshot")
 old_map={r["formulation_id"]:r for r in historical}
 if set(old_map)!=set(byid):
  raise PipelineError("Original 443 formulation ID set differs")

 # Rebase a per-formulation source-recheck decision with separately retained history.
 updated=[]
 for row in historical:
  new=dict(row,meaning_catalog_digest=revised_catalog)
  case=next((x for x in CASES if x["fid"]==row["formulation_id"]),None)
  if case:
   new["original_presheaf_review_reason"]=row["editorial_reason"]
   new["editorial_reason"]=case["reason"]
   new["source"]="wave2_source_mathematical_correction_and_re-review"
   new["reviewed_by"]="assistant_independent_stacks_mathematical_review_2026_10_19"
   new["human_verified"]=False
  updated.append(new)
 corrected_m={r["formulation_id"]:r for r in updated}
 if any(corrected_m[fid]["relation_ids"]!=old_map[fid]["relation_ids"] or
        corrected_m[fid]["decision"]!=old_map[fid]["decision"] or
        corrected_m[fid]["original_wave1_disposition"]!=old_map[fid]["original_wave1_disposition"]
        for fid in old_map):
  raise PipelineError("Review disposition or link lineage altered unexpectedly")
 if {rid for r in updated for rid in r["relation_ids"]}!=set(relations):
  raise PipelineError("Screened relationship lost its reviewed source formulation")
 cat=meanings[CASES[0]["mid"]]["formulations"][0]
 for x in relations.values():
  if x["from_formulation"]==cat["id"] and
     x["source_phrase"].casefold() not in cat["text"].casefold():
   raise PipelineError("Prior category-valued source link lost its exact source anchor")
 check_cycles(meanings,relations)
 if current_reviews!=updated:
  if current_reviews!=historical:
   raise PipelineError("Existing revised review ledger differs from expected corrections")
  atomic_jsonl(prior_reviews_path,sorted(updated,key=lambda r:r["formulation_id"]))
 audit=[{
   "record_id":x["mid"],"formulation_id":x["fid"],"source_url":x["source"],
   "old_text":x["old"],"new_text":x["new"],"new_context":x["context"],
   "mathematical_recheck":x["reason"],"source_reviewed_directly":True,
   "old_review_disposition":old_map[x["fid"]]["decision"],
   "new_review_disposition":corrected_m[x["fid"]]["decision"],
   "previous_source_link_ids":old_map[x["fid"]]["relation_ids"],
   "replacement_source_link_ids":corrected_m[x["fid"]]["relation_ids"],
   "human_verified":False
  } for x in CASES]
 event_file=w.root/"events/wave2_presheaf_mathematical_corrections_2026-10-19.jsonl"
 evidence=chr(10).join(canonical(x) for x in audit)+chr(10)
 if event_file.exists() and event_file.read_text(encoding="utf-8")!=evidence:
  raise PipelineError("Presheaf mathematical review evidence conflicts with earlier event")
 event_file.write_text(evidence,encoding="utf-8")
 state=w.state("meanings")
 state.update(total=431,record_digest=revised_catalog,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 report={
  "phase":"two_source_corrected_stacks_presheaves_audited_and_rescreened",
  "corrected_formulations":2,"meaning_count":431,"formulation_count":443,
  "relations_preserved":545,"prior_formulation_reviews_preserved":443,
  "review_snapshotted_before_catalog_rebase":True,
  "historical_wave1_dispositions_preserved":True,
  "category_valued_variance_correction_applied":True,
  "groupoid_valued_strict_source_correction_applied":True,
  "groupoid_valued_dependency_held_for_fresh_individual_review":True,
  "all_meanings_screened":True,"all_stages_unsealed":True,
  "human_peer_verified":False,"production_corpus_consulted":False,
  "next":"Individually screen and append strict groupoid-valued presheaf -> category-valued presheaf link; preserve previous held reason in override event."
 }
 atomic_json(w.root/"state/wave2_presheaf_math_corrections.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",required=True,type=Path)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
