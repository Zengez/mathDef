"""Screen two independently sourced Stacks site/family meanings; preserve 465 reviews."""
from __future__ import annotations
import argparse,json,hashlib
from collections import Counter
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

ITEMS=[
 {"slug":"fixed-target-morphism-family","term":"indexed family of morphisms with fixed target",
  "context":"Stacks Definition 7.6.1, set-indexed arrows with a common target and possible empty indexing set",
  "text":"Let C be a small category and U an object of C. An indexed family of morphisms with fixed target U consists of a set I and, for every i∈I, an object U_i and a morphism f_i:U_i→U. The indexing set I may be empty; repeated arrows with different indices are still different family occurrences.",
  "reason":"Stacks 7.6.1 specifies one target U, set-indexed source arrows and allows the empty index set. Index multiplicities belong to the indexed family data; collapsing to the support set of arrows changes that data. This formulation uses the Stacks small-category convention, without imposing coverage axioms.",
  "url":"https://stacks.math.columbia.edu/tag/0396"},
 {"slug":"grothendieck-site-pretopology","term":"site with covering families",
  "context":"Stacks Definition 7.6.2, category with distinguished covering families and base-change/refinement axioms",
  "text":"A site in the Stacks covering-family convention is a small category C together with a set Cov(C) of indexed families of morphisms with fixed target, called covering families. Singleton families of isomorphisms are coverings; compositions/refinements of covering families are coverings; and coverings pull back along arrows with the necessary fiber products existing.",
  "reason":"Stacks 7.6.2 expresses its coverage through families of arrows satisfying isomorphism, transitivity/refinement and base-change axioms. This formulation records actual covering-family data rather than identifying it literally with the associated sieve-based Grothendieck topology. The Stacks category convention supplies the underlying objects and arrows.",
  "url":"https://stacks.math.columbia.edu/tag/00VH"}
]
def run(root):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Independent unsealed Wave 2 required")
 prior=w.root/"state/wave2_foundations_batch_11.json"
 if not prior.exists() or json.loads(prior.read_text(encoding="utf-8")).get("new_observations")!=2:
  raise PipelineError("Both Stacks source observations must be individually verified first")
 expected={"sources":9,"terms":356,"observations":779,"relations":600}
 if any(len(w.records(k))!=n for k,n in expected.items()):raise PipelineError("Source baseline changed")
 initial=w.records("meanings")
 if len(initial) not in (453,455):raise PipelineError("Unexpected meaning catalog")
 terms,obs=w.records("terms"),w.records("observations")
 candidates=[];reviews=[]
 for i in ITEMS:
  slug=i["slug"];mid="meaning.wave2.foundation."+slug;fid="form.wave2.foundation."+slug
  tid="term.wave2.stacks.foundation11."+slug;oid="obs.wave2.stacks.foundation11."+slug
  t,o=terms.get(tid),obs.get(oid)
  if not t or not o or t["locator"]!=i["url"] or o["locator"]!=i["url"] or o["term_id"]!=tid or o["record_kind"]!="paraphrase":
   raise PipelineError("Missing exact independent source attribution "+slug)
  if len(i["reason"])<140 or len(i["text"])<140:raise PipelineError("Insufficient review rationale "+slug)
  candidates.append({"id":mid,"term_group_id":"wave2.foundation."+slug,"display_term":i["term"],"context":i["context"],
    "term_ids":[tid],"human_verified":False,"editorial_status":"individual_source_screen_pending",
    "formulations":[{"id":fid,"text":i["text"],"evidence_ids":[oid],"review_state":"candidate",
      "human_verified":False,"mathematical_scope_note":i["reason"]}]})
  reviews.append({"meaning_id":mid,"formulation_id":fid,"source_url":i["url"],
    "source_observation_id":oid,"mathematical_reason":i["reason"],
    "source_screened_by":"assistant_independent_stacks_site_mathematical_comparison_2026_10_19","human_verified":False})
 def write(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  data=chr(10).join(canonical(r) for r in rows)+chr(10)
  if path.exists() and path.read_text(encoding="utf-8")!=data:
   raise PipelineError("Existing individual research evidence differs "+str(path))
  path.write_text(data,encoding="utf-8")
  return path
 if len(initial)==453:
  w.ingest("meanings",write(w.root/"intake/wave2_foundation_meanings_batch_12.jsonl",candidates),batch_size=2)
 else:
  for item in candidates:
   old=initial.get(item["id"])
   if old is None or old["formulations"][0]["text"]!=item["formulations"][0]["text"]:
    raise PipelineError("Previously added meaning differs")
 for item in ITEMS:
  mid="meaning.wave2.foundation."+item["slug"]
  m=w.records("meanings")[mid];f=m["formulations"][0]
  if f["review_state"]=="screened":
   if m.get("editorial_screening_reason")!=item["reason"]:raise PipelineError("Earlier screening differs")
   continue
  if f["review_state"]!="candidate":raise PipelineError("Wrong source-review state")
  upd=dict(m)
  upd["formulations"]=[dict(f,review_state="screened",human_verified=False,
    source_screened_by="assistant_independent_stacks_site_mathematical_comparison_2026_10_19")]
  upd["editorial_status"]="source_scope_mathematically_screened"
  upd["editorial_screening_reason"]=item["reason"]
  apply_revision(w.root,{"event_id":"revision.wave2.foundation12."+item["slug"]+".screen01",
    "stage":"meanings","record_id":mid,"before_digest":digest(m),
    "editor":"assistant_independent_stacks_site_mathematical_comparison_2026_10_19",
    "reason":item["reason"],"operation":"replace","replacement":upd})
 write(w.root/"wave2/foundation_meaning_review_batch_12.jsonl",reviews)
 meanings=w.records("meanings")
 forms={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
 if len(meanings)!=455 or len(forms)!=467 or any(f["review_state"]!="screened" for m in meanings.values() for f in m["formulations"]):
  raise PipelineError("New source-screened catalog invalid")
 current=w.root/"state/wave2_formulation_reviews.jsonl"
 older=jsonl(current)
 snapshot=w.root/"state/wave2_formulation_reviews_snapshot_465_before_foundations12.jsonl"
 if len(older)==465:
  ids={r["formulation_id"] for r in older}
  if len(ids)!=465 or {rid for r in older for rid in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Prior individual review coverage incomplete")
  oldtext=current.read_text(encoding="utf-8")
  if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=oldtext:raise PipelineError("Historical snapshot conflicts")
  snapshot.write_text(oldtext,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_465_before_foundations12.json",{
    "prior_reviews":465,"screened_links":600,"sha256":hashlib.sha256(oldtext.encode("utf-8")).hexdigest(),"human_peer_verified":False})
  dg=digest(list(meanings.values()))
  updated=[dict(r,meaning_catalog_digest=dg) for r in older]
  for item in candidates:
   updated.append({"formulation_id":item["formulations"][0]["id"],"meaning_id":item["id"],
     "meaning_catalog_digest":dg,"decision":"needs_review","relation_ids":[],
     "original_wave1_disposition":None,"source":"individually_screened_stacks_site12",
     "editorial_reason":"New source-specific Stacks site/family definition requires separate prerequisite research.",
     "reviewed_by":None,"human_verified":False})
  atomic_jsonl(current,sorted(updated,key=lambda r:r["formulation_id"]))
 elif len(older)==467:
  if not snapshot.exists() or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in older):
   raise PipelineError("Earlier ledger migration inconsistent")
 else:raise PipelineError("Review count unexpected")
 hist=jsonl(snapshot);new=jsonl(current);by={r["formulation_id"]:r for r in new}
 if len(hist)!=465 or len(new)!=467 or len(by)!=467:raise PipelineError("Lost individual review IDs")
 for old in hist:
  curr=by.get(old["formulation_id"])
  if not curr or any(curr.get(k)!=v for k,v in old.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Historical review disposition changed")
 if {rid for r in new for rid in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Old mathematical relationships no longer reviewed")
 dispositions=dict(Counter(r["decision"] for r in new))
 if dispositions!={"linked":457,"no_supported_target":7,"held_ambiguity":1,"needs_review":2}:
  raise PipelineError("Unexpected new review states "+str(dispositions))
 check_cycles(meanings,w.records("relations"))
 state=w.state("meanings")
 state.update(total=455,record_digest=digest(list(meanings.values())),
              screened_new_formulations=36,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 report={"phase":"two_stacks_site_and_family_meanings_individually_screened",
   "source_terms":356,"source_observations":779,"contextual_meanings":455,"formulations":467,
   "screened_links_preserved":600,"historical_review_rows_preserved":465,
   "new_formulation_reviews_pending":2,"review_dispositions":dispositions,
   "indexed_family_empty_index_set_allowed":True,
   "site_family_coverage_not_equated_to_sieve_topology":True,
   "human_peer_verified":False,"all_stages_unsealed":True,"original_production_mathdef_consulted":False}
 atomic_json(w.root/"state/wave2_foundations_batch_12_screened.json",report)
 return report
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--workspace",type=Path,required=True)
 a=ap.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
