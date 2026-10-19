"""Individually screen preadditive, additive and abelian category axioms.

Preserve precisely 471 existing review entries, 606 links and frozen Wave 1.
Do not infer that preadditive categories have zero objects, or that additive
categories admit kernels/cokernels or are automatically abelian.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

SPECS=[
 {"slug":"preadditive-category","title":"preadditive category","tag":"00ZY",
 "context":"Stacks Definition 12.3.1: abelian-group hom-sets and bilinear composition",
 "text":"A preadditive category C is a category such that for every pair of objects X,Y the morphism set Hom_C(X,Y) is an abelian group, and composition Hom_C(Y,Z)×Hom_C(X,Y)→Hom_C(X,Z) is bilinear in its two morphism variables.",
 "reason":"Stacks 12.3.1 requires abelian group structure on every hom-set and additivity in each argument of composition. These axioms alone do not guarantee existence of a zero object, finite direct sums, kernels or cokernels, so the independently screened formulation does not silently impose any of those stronger conditions."},
 {"slug":"additive-category","title":"additive category","tag":"0104",
 "context":"Stacks Definition 12.3.8: preadditive category with all finite products",
 "text":"An additive category C is a preadditive category in which all finite products exist, including an empty product. Equivalently in a preadditive category, it has a zero object and finite direct sums.",
 "reason":"Stacks 12.3.8 adds finite-product existence to preadditivity and explicitly gives zero object and direct sums as an equivalent characterization. The empty finite product is essential for the zero object. Merely bilinear composition is insufficient, and additivity does not imply all kernels or cokernels exist."},
 {"slug":"abelian-category","title":"abelian category","tag":"0109",
 "context":"Stacks Definition 12.5.1: additive category with kernels, cokernels, and coimage-image isomorphisms",
 "text":"An abelian category C is an additive category in which every morphism f has a kernel and a cokernel and, for every such f, the canonical comparison morphism Coim(f)→Im(f) is an isomorphism.",
 "reason":"Stacks 12.5.1 imposes three independent requirements: additivity, existence of all kernels and cokernels, and invertibility of the canonical coimage-to-image comparison. The last condition cannot be dropped, since an additive category may have (co)kernels but fail that isomorphism. This definition is not interchangeable with preadditivity."}
]

def run(root):
 w=Workspace(root)
 if json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8")).get("mode")!="second_wave":
  raise PipelineError("Editable independent Wave 2 fork required")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Cannot change a sealed stage")
 intake=w.root/"state/wave2_foundations_batch_15.json"
 if not intake.exists() or json.loads(intake.read_text(encoding="utf-8")).get("new_observation_records")!=3:
  raise PipelineError("Three individually approved source observations must be committed before meaning screening")
 counts={s:len(w.records(s)) for s in ("sources","terms","observations","relations")}
 if counts!={"sources":9,"terms":363,"observations":786,"relations":606}:
  raise PipelineError("Unexpected source/relationship baseline "+str(counts))
 initial=w.records("meanings")
 if len(initial) not in (459,462):
  raise PipelineError("Unexpected meaning catalog before 3-context screen")
 terms,obs=w.records("terms"),w.records("observations")
 candidates=[];decisions=[]
 for case in SPECS:
  slug=case["slug"];url="https://stacks.math.columbia.edu/tag/"+case["tag"]
  tid="term.wave2.foundation15."+slug
  oid="obs.wave2.foundation15."+slug
  t,o=terms.get(tid),obs.get(oid)
  if not t or not o or t["locator"]!=url or o["locator"]!=url or o["term_id"]!=tid or o["record_kind"]!="paraphrase" or o["human_verified"] is not False:
   raise PipelineError("Missing exact source candidate "+slug)
  if len(case["reason"])<160 or len(case["text"])<150:
   raise PipelineError("Individual mathematical meaning review too short "+slug)
  mid="meaning.wave2.foundation15."+slug;fid="form.wave2.foundation15."+slug
  candidates.append({"id":mid,"term_group_id":"wave2.foundation15."+slug,
    "display_term":case["title"],"context":case["context"],"term_ids":[tid],
    "editorial_status":"candidate_requires_individual_stacks_source_comparison","human_verified":False,
    "formulations":[{"id":fid,"text":case["text"],"evidence_ids":[oid],
      "review_state":"candidate","mathematical_scope_note":case["reason"],"human_verified":False}]})
  decisions.append({"meaning_id":mid,"formulation_id":fid,"source_url":url,
    "source_observation_id":oid,"mathematical_reason":case["reason"],
    "reviewed_by":"assistant_independent_stacks_category_axioms_review_2026_10_19",
    "human_verified":False})
 def write(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  payload=chr(10).join(canonical(x) for x in rows)+chr(10)
  if path.exists() and path.read_text(encoding="utf-8")!=payload:
   raise PipelineError("Previously reviewed source material conflicts "+str(path))
  path.write_text(payload,encoding="utf-8")
  return path
 stored=write(w.root/"intake/wave2_foundation_meanings_batch_16.jsonl",candidates)
 if len(initial)==459:
  w.ingest("meanings",stored,batch_size=3)
 else:
  for c in candidates:
   m=initial.get(c["id"])
   if not m or m["formulations"][0]["text"]!=c["formulations"][0]["text"]:
    raise PipelineError("Existing candidate formulation differs")
 for case in SPECS:
  mid="meaning.wave2.foundation15."+case["slug"]
  m=w.records("meanings")[mid];f=m["formulations"][0]
  if f["review_state"]=="screened":
   if m.get("editorial_screening_reason")!=case["reason"]:
    raise PipelineError("Existing mathematical screening reason differs")
   continue
  if f["review_state"]!="candidate":raise PipelineError("Unexpected prior review state")
  screened=dict(m)
  screened["formulations"]=[dict(f,review_state="screened",
    source_screened_by="assistant_independent_stacks_category_axioms_review_2026_10_19",
    human_verified=False)]
  screened["editorial_status"]="individually_mathematically_source_screened"
  screened["editorial_screening_reason"]=case["reason"]
  apply_revision(w.root,{"event_id":"revision.wave2.category_axioms."+case["slug"]+".screen01",
    "stage":"meanings","record_id":mid,"before_digest":digest(m),
    "editor":"assistant_independent_stacks_category_axioms_review_2026_10_19",
    "reason":case["reason"],"operation":"replace","replacement":screened})
 write(w.root/"wave2/foundation_meaning_review_batch_16.jsonl",decisions)
 meanings=w.records("meanings")
 forms={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
 if len(meanings)!=462 or len(forms)!=474 or any(f["review_state"]!="screened" for m in meanings.values() for f in m["formulations"]):
  raise PipelineError("Missing new mathematical meaning reviews")
 current=w.root/"state/wave2_formulation_reviews.jsonl"
 snapshot=w.root/"state/wave2_formulation_reviews_snapshot_471_before_category16.jsonl"
 old=jsonl(current)
 if len(old)==471:
  if len(set(r["formulation_id"] for r in old))!=471 or {i for r in old for i in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Current source-reviewed relationship ledger incomplete")
  content=current.read_text(encoding="utf-8")
  if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=content:
   raise PipelineError("Immutable 471-review source snapshot conflicts")
  snapshot.write_text(content,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_471_before_category16.json",{
    "formulation_review_count":471,"screened_relations":606,
    "prior_sha256":hashlib.sha256(content.encode("utf-8")).hexdigest(),"human_peer_verified":False})
  dg=digest(list(meanings.values()))
  revised=[dict(row,meaning_catalog_digest=dg) for row in old]
  for meaning in candidates:
   revised.append({"formulation_id":meaning["formulations"][0]["id"],"meaning_id":meaning["id"],
     "meaning_catalog_digest":dg,"decision":"needs_review","relation_ids":[],
     "original_wave1_disposition":None,"source":"individually_source_screened_category_axioms16",
     "editorial_reason":"New mathematical foundation requires separately justified screened prerequisite links.",
     "reviewed_by":None,"human_verified":False})
  atomic_jsonl(current,sorted(revised,key=lambda row:row["formulation_id"]))
 elif len(old)==474:
  if not snapshot.exists() or any(r.get("meaning_catalog_digest")!=digest(list(meanings.values())) for r in old):
   raise PipelineError("Previously expanded mathematical reviews are stale")
 else:raise PipelineError("Unexpected number of prior individual reviews")
 before=jsonl(snapshot);after=jsonl(current);by={r["formulation_id"]:r for r in after}
 if len(before)!=471 or len(after)!=474 or len(by)!=474:
  raise PipelineError("Existing review identity was lost")
 for r in before:
  now=by.get(r["formulation_id"])
  if now is None or any(now.get(k)!=v for k,v in r.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Historical mathematics disposition changed")
 if {i for r in after for i in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Existing screened links lost review provenance")
 dispositions=dict(Counter(r["decision"] for r in after))
 if dispositions!={"linked":461,"no_supported_target":5,"held_ambiguity":1,"needs_review":7}:
  raise PipelineError("Unexpected old/new disposition counts "+str(dispositions))
 check_cycles(meanings,w.records("relations"))
 state=w.state("meanings")
 state.update(total=462,record_digest=digest(list(meanings.values())),
   screened_new_formulations=43,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 result={"phase":"preadditive_additive_abelian_category_axioms_mathematically_screened",
  "screened_contextual_meanings":462,"reviewed_formulations":474,
  "previous_review_rows_preserved":471,"screened_links_preserved":606,
  "new_link_reviews_pending":3,"total_pending_formulation_review":7,
  "preadditive_additive_abelian_hierarchy_not_conflated":True,
  "coimage_image_comparison_axiom_preserved":True,
  "all_stages_unsealed":True,"original_production_mathdef_consulted":False,
  "human_peer_verified":False}
 atomic_json(w.root/"state/wave2_foundations_batch_16_screened.json",result)
 return result
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--workspace",required=True,type=Path)
 a=ap.parse_args();print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
