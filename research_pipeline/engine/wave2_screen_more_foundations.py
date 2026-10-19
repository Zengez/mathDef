"""Grow screened Wave 2 meanings with field, functor, groupoid, pseudofunctor.

Preserves 443 individually reviewed formulations and 545 screened relationships.
Only run after both Stacks presheaf corrections have been verified and committed.
No production-mathDef definitions, variants or citations are read.
"""
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
from collections import Counter
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .stage5_review_gate import atomic_jsonl
from .revisions import apply_revision
from .wave2_apply_links import check_cycles

SPECS=[
 dict(key="field-commutative-unital",term="field (nonzero commutative unital ring)",
      source="https://stacks.math.columbia.edu/tag/09FD",
      context="Stacks 9.2.1 with Stacks 10.2 commutative-unital ring convention",
      text="A field is a commutative ring k with identity 1_k, with 0≠1_k, such that for every a∈k with a≠0 there exists b∈k satisfying ab=1_k (and hence ba=1_k).",
      scope="The zero ring is excluded; no noncommutative division-ring generalization is inferred.",
      crosscheck=["https://stacks.math.columbia.edu/tag/00AQ"],
      reason="Stacks Definition 9.2.1 characterizes a field as a nonzero ring in which all nonzero elements are invertible. Section 10.2 states explicitly that ring means a commutative unital ring. The zero ring exclusion and two-sided invertibility are preserved."),
 dict(key="category-functor",term="covariant functor between small categories",
      source="https://stacks.math.columbia.edu/tag/001B",
      context="Stacks 4.2.8 ordinary strict covariant functor, not a weak pseudofunctor",
      text="A covariant functor F:A→B between small categories assigns to every object x of A an object F(x) of B and to every arrow f:x→y an arrow F(f):F(x)→F(y). For composable arrows f,g it satisfies F(g∘f)=F(g)∘F(f), and F(id_x)=id_{F(x)}.",
      scope="Covariant ordinary functor; a contravariant functor is instead covariant from A^op, and pseudofunctor comparison isomorphisms are not allowed here.",
      crosscheck=["https://stacks.math.columbia.edu/tag/0013"],
      reason="Stacks Definition 4.2.8 supplies separate object and morphism assignments with strict preservation of identity and composition. The source Section 4.2 uses sets of objects and morphisms in its category convention. This is distinct from a weak pseudofunctor."),
 dict(key="small-groupoid",term="groupoid of invertible arrows",
      source="https://stacks.math.columbia.edu/tag/0018",
      context="Stacks 4.2.5, a small category in which every arrow is an isomorphism",
      text="A groupoid is a small category G such that for every morphism f:x→y there is a morphism g:y→x with g∘f=id_x and f∘g=id_y.",
      scope="Objects need not coincide; a single-object groupoid is a group, but general groupoids need not have one object.",
      crosscheck=["https://stacks.math.columbia.edu/tag/0013"],
      reason="Stacks Definition 4.2.5 defines groupoids by requiring every morphism to be an isomorphism, and Definition 4.2.4 gives both inverse identities. General groupoids are not collapsed to one-object groups or discrete categories."),
 dict(key="pseudofunctor-to-strict-2category",source_key="pseudo-functor-strict-2category",term="pseudofunctor from category to strict 2-category",
      source="https://stacks.math.columbia.edu/tag/003N",
      context="Stacks Definition 4.29.5: ordinary source category and strict 2-category target, with invertible comparison 2-cells",
      text="A pseudofunctor P:A→C from an ordinary category A to a strict 2-category C assigns objects P(x) and 1-morphisms P(f), invertible comparison 2-cells η_x:id_{P(x)}⇒P(id_x) and κ_{g,f}:P(g∘f)⇒P(g)∘P(f), and satisfies the unit identities κ_{id_y,f}=η_y⋆id_{P(f)}, κ_{f,id_x}=id_{P(f)}⋆η_x and the associativity coherence (id_{P(h)}⋆κ_{g,f})∘κ_{h,g∘f}=(κ_{h,g}⋆id_{P(f)})∘κ_{h∘g,f} for composable f,g,h.",
      scope="Do not identify with strict functors; comparison 2-cells must be invertible and satisfy all source coherence laws; target is Stacks strict 2-category.",
      crosscheck=["https://stacks.math.columbia.edu/tag/003G"],
      reason="Stacks 4.29.5 explicitly distinguishes functors from weak or pseudo functors by supplying invertible identity/composition comparison 2-morphisms and both coherence conditions. The full unit and associativity laws are retained, with Stacks strict-target convention.")
]

def run(root):
 w=Workspace(root)
 baseline=w.root/"state/baseline.json"
 if not baseline.exists() or json.loads(baseline.read_text(encoding="utf-8")).get("mode")!="second_wave":
  raise PipelineError("Requires isolated independent Wave 2")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("No editing sealed source/meaning/relation stage")
 presheaf_report=w.root/"state/wave2_presheaf_math_corrections.json"
 if not presheaf_report.exists() or not json.loads(presheaf_report.read_text(encoding="utf-8")).get("groupoid_valued_strict_source_correction_applied"):
  raise PipelineError("Do not expand meaning catalog before source-corrected presheaves are committed")
 if len(w.records("terms"))!=343 or len(w.records("observations"))!=766 or len(w.records("relations"))!=545:
  raise PipelineError("Requires completed Stacks source batch 05 and unchanged link history")
 previous_catalog=w.records("meanings")
 if len(previous_catalog) not in (431,435):
  raise PipelineError("Unexpected historical meaning catalog length")
 candidates=[]
 for item in SPECS:
  source_key=item.get("source_key",item["key"])
  term_id="term.wave2.stacks."+source_key
  obs_id="obs.wave2.stacks."+source_key
  term=w.records("terms").get(term_id)
  obs=w.records("observations").get(obs_id)
  if not term or not obs or term["locator"]!=item["source"] or obs["locator"]!=item["source"] or obs["term_id"]!=term_id:
   raise PipelineError("No matching independent Stacks source observation: "+item["key"])
  if obs["record_kind"]!="paraphrase" or obs["human_verified"] is not False:
   raise PipelineError("Unreviewed evidence: "+item["key"])
  mid="meaning.wave2.foundation."+item["key"]
  fid="form.wave2.foundation."+item["key"]
  candidates.append({
   "id":mid,"term_group_id":"wave2.foundation."+item["key"],
   "display_term":item["term"],"context":item["context"],
   "term_ids":[term_id],
   "formulations":[{"id":fid,"text":item["text"],"evidence_ids":[obs_id],
     "review_state":"candidate","mathematical_scope_note":item["scope"],"human_verified":False}],
   "human_verified":False,"editorial_status":"candidate_requires_individual_mathematical_comparison"
  })
 def persist(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  body=chr(10).join(canonical(x) for x in rows)+chr(10)
  if path.exists() and path.read_text(encoding="utf-8")!=body:
   raise PipelineError("Conflicting prior research revision evidence")
  path.write_text(body,encoding="utf-8")
  return path
 intake=persist(w.root/"intake/wave2_foundation_meaning_candidates_batch_04.jsonl",candidates)
 if len(previous_catalog)==431:
  w.ingest("meanings",intake,batch_size=4)
 else:
  for candidate in candidates:
   m=previous_catalog.get(candidate["id"])
   if m is None or m["formulations"][0]["text"]!=candidate["formulations"][0]["text"]:
    raise PipelineError("Previously added foundation candidate differs")
 for item in SPECS:
  mid="meaning.wave2.foundation."+item["key"]
  m=w.records("meanings")[mid]
  form=m["formulations"][0]
  if form["review_state"]=="screened":
   if m.get("editorial_screening_reason")!=item["reason"]:
    raise PipelineError("Existing source-screened meaning rationale conflicts")
   continue
  if form["review_state"]!="candidate" or len(item["reason"])<140:
   raise PipelineError("Candidate not eligible for independent mathematical screen")
  updated=dict(m)
  updated["formulations"]=[dict(form,review_state="screened",human_verified=False,
   source_screened_by="assistant_independent_mathematical_stacks_review_2026_10_19")]
  updated["human_verified"]=False
  updated["editorial_screening_reason"]=item["reason"]
  updated["crosschecked_source_urls"]=[item["source"]]+item["crosscheck"]
  updated["editorial_status"]="mathematically_screened_independent_foundation"
  apply_revision(w.root,{
   "event_id":"revision.wave2.foundation."+item["key"]+".screen01",
   "stage":"meanings","record_id":mid,"before_digest":digest(m),
   "editor":"assistant_independent_mathematical_stacks_review_2026_10_19",
   "reason":item["reason"],"operation":"replace","replacement":updated
  })
 review_rows=[{
  "meaning_id":"meaning.wave2.foundation."+i["key"],
  "formulation_id":"form.wave2.foundation."+i["key"],
  "source_urls":[i["source"]]+i["crosscheck"],
  "source_evidence_ids":["obs.wave2.stacks."+i.get("source_key",i["key"])],
  "mathematical_reason":i["reason"],"reviewed_by":"assistant_independent_mathematical_stacks_review_2026_10_19",
  "decision":"screen_source_specific_formulation","human_verified":False
 } for i in SPECS]
 persist(w.root/"wave2/foundation_meaning_review_batch_03.jsonl",review_rows)
 meanings=w.records("meanings")
 all_forms={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
 if len(meanings)!=435 or len(all_forms)!=447 or any(f["review_state"]!="screened" for m in meanings.values() for f in m["formulations"]):
  raise PipelineError("New mathematical meaning count or review state invalid")
 before_path=w.root/"state/wave2_formulation_reviews.jsonl"
 reviews=jsonl(before_path)
 snapshot=w.root/"state/wave2_formulation_reviews_snapshot_443_before_new_foundations.jsonl"
 if len(reviews)==443:
  previous={r["formulation_id"]:r for r in reviews}
  if len(previous)!=443 or set(previous)!=set(all_forms)-{c["formulations"][0]["id"] for c in candidates}:
   raise PipelineError("Old individual review identities incomplete or malformed")
  if {rel for r in reviews for rel in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Unscreened historical link found")
  oldtext=before_path.read_text(encoding="utf-8")
  if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=oldtext:
   raise PipelineError("Conflicting historical 443-review snapshot")
  snapshot.write_text(oldtext,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_443_before_new_foundations.json",{
   "review_count":443,"relation_count":545,
   "review_ledger_sha256":hashlib.sha256(oldtext.encode("utf-8")).hexdigest(),
   "before_meaning_catalog_digest":reviews[0]["meaning_catalog_digest"],
   "human_peer_verified":False
  })
  new_digest=digest(list(meanings.values()))
  final=[dict(r,meaning_catalog_digest=new_digest) for r in reviews]
  for c in candidates:
   final.append({"formulation_id":c["formulations"][0]["id"],"meaning_id":c["id"],
     "meaning_catalog_digest":new_digest,"decision":"needs_review","relation_ids":[],
     "original_wave1_disposition":None,"source":"wave2_individually_screened_stacks_foundation",
     "editorial_reason":"Newly screened contextual foundation requires independent mathematical link review.",
     "reviewed_by":None,"human_verified":False})
  atomic_jsonl(before_path,sorted(final,key=lambda r:r["formulation_id"]))
 elif len(reviews)==447:
  if not snapshot.exists():
   raise PipelineError("Review migration missing original 443 snapshot")
  if any(x["meaning_catalog_digest"]!=digest(list(meanings.values())) for x in reviews):
   raise PipelineError("Existing expanded review catalog digest diverged")
 else:
  raise PipelineError("Unexpected formulation ledger before migration")
 now=jsonl(before_path)
 historical=jsonl(snapshot)
 index={r["formulation_id"]:r for r in now}
 if len(index)!=447 or len(historical)!=443:
  raise PipelineError("New and prior formulation review identities incomplete")
 for prior in historical:
  r=index.get(prior["formulation_id"])
  if r is None or any(r.get(k)!=v for k,v in prior.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Historical link disposition was rewritten")
 if {x for r in now for x in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Lost screened relationship provenance")
 check_cycles(meanings,w.records("relations"))
 summary=dict(Counter(r["decision"] for r in now))
 if summary!={"linked":419,"no_supported_target":22,"held_ambiguity":2,"needs_review":4}:
  raise PipelineError("Unexpected link review states after new meanings: "+str(summary))
 state=w.state("meanings")
 state.update(total=435,record_digest=digest(list(meanings.values())),
  screened_new_formulations=16,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 report={
  "phase":"four_screened_stacks_foundations_appended_after_presheaf_review",
  "source_terms":343,"source_observations":766,"contextual_meanings":435,
  "formulations":447,"screened_relations_retained":545,"historical_review_rows_preserved":443,
  "new_foundation_formulations_needing_link_review":4,"dispositions":summary,
  "presheaf_audit_completed_before_growth":True,
  "historical_snapshot_verified":True,"all_stages_unsealed":True,
  "original_production_mathdef_consulted":False,"human_peer_verified":False,
  "next":"Review four new source-backed foundation links, then revisit previously unsupported category, field, and pseudofunctor cases."
 }
 atomic_json(w.root/"state/wave2_new_foundations_batch_06_screened.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
