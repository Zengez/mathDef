"""Individually screen four independent homological-algebra meaning candidates.

The concrete kernel of a homomorphism of abelian groups is not identified
literally with a universal kernel arrow. Kernel and cokernel need not exist
in arbitrary preadditive categories. Exactness uses an abelian category.
Preserve all earlier 467 formulation reviews and 606 screened links.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .stage5_review_gate import atomic_jsonl
from .revisions import apply_revision
from .wave2_apply_links import check_cycles

CASES=[
 dict(slug="abelian-group-homomorphism-kernel",term="kernel",group="kernel",
   url="https://proofwiki.org/wiki/Definition%3AKernel_of_Group_Homomorphism",
   context="Concrete additive subgroup kernel of a homomorphism of abelian groups",
   text="Given a group homomorphism f:A→B of abelian groups (written additively), its kernel is ker(f)={a∈A : f(a)=0_B}, an additive subgroup of A. The canonical inclusion ker(f)→A makes this subgroup the usual kernel object in the category of abelian groups.",
   reason="ProofWiki directly defines kernels for group homomorphisms as inverse images of the group identity; additive notation gives 0_B for abelian groups. The subgroup is a concrete set of elements, while the associated categorical kernel is an inclusion arrow with a universal property. The two are related but not literally the same object data."),
 dict(slug="preadditive-category-kernel",term="kernel",group="kernel",
   url="https://stacks.math.columbia.edu/tag/0106",
   context="Universal-property kernel of a morphism in a preadditive category, existence conditional",
   text="For a morphism f:X→Y in a preadditive category, a kernel is a morphism i:K→X satisfying f∘i=0, such that for every j:Z→X with f∘j=0 there is exactly one h:Z→K with j=i∘h. A kernel is asserted only when such a universal morphism exists.",
   reason="Stacks Definition 12.3.9 item 1 gives an arrow satisfying annihilation and unique universal factorization; item 2 explicitly uses conditional 'if the kernel exists'. A preadditive category need not have all kernels. The definition is a morphism universal property, not a bare subset of a domain."),
 dict(slug="preadditive-category-cokernel",term="cokernel",group="cokernel",
   url="https://stacks.math.columbia.edu/tag/0106",
   context="Universal-property cokernel of a morphism in a preadditive category, existence conditional",
   text="For a morphism f:X→Y in a preadditive category, a cokernel is a morphism p:Y→C satisfying p∘f=0, such that for every q:Y→Z with q∘f=0 there is exactly one h:C→Z with q=h∘p. A cokernel is asserted only when such a universal morphism exists.",
   reason="Stacks Definition 12.3.9 item 3 supplies the dual universal property and item 4 explicitly qualifies notation by existence. In the category of abelian groups the corresponding morphism may be modeled by projection onto B/im(f), but the definition does not presuppose that all preadditive categories possess cokernels."),
 dict(slug="exact-sequence-abelian-category",term="exact sequence",group="exact-sequence",
   url="https://stacks.math.columbia.edu/tag/00ZX",
   context="Complex exact at interior objects of an abelian category, where images and kernels exist",
   text="A sequence of arrows in an additive category is a complex when each consecutive composite is zero. When the category is abelian, a complex X→Y→Z is exact at Y if im(X→Y)=ker(Y→Z) as subobjects of Y. An exact complex is exact at every applicable position; a short exact sequence has form 0→A→B→C→0.",
   reason="Stacks Definition 12.5.7 first defines a complex using zero composites in an additive category, then imposes image-equals-kernel exactness only after assuming an abelian category. Short exact sequences include zero objects at both ends. In arbitrary preadditive or merely additive categories the image/kernels may fail to exist, so this strong exactness claim cannot be transported there.")
]

def run(root):
 w=Workspace(root)
 if json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8")).get("mode")!="second_wave":
  raise PipelineError("Only independent Wave 2 fork supported")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("No mutation of sealed reconstruction")
 proof=w.root/"state/wave2_foundations_batch_13.json"
 if not proof.exists() or json.loads(proof.read_text(encoding="utf-8")).get("new_observations")!=4:
  raise PipelineError("Need verified source-only batch 13 before meaning screening")
 counts={s:len(w.records(s)) for s in ("sources","terms","observations","relations")}
 if counts!={"sources":9,"terms":360,"observations":783,"relations":606}:
  raise PipelineError("Unexpected intake baseline: "+str(counts))
 source_terms,observations=w.records("terms"),w.records("observations")
 original=w.records("meanings")
 if len(original) not in (455,459):
  raise PipelineError("Unexpected prior contextual meanings")
 candidates=[];math_reviews=[]
 for case in CASES:
  key=case["slug"]
  tid="term.wave2.foundation13."+key
  oid="obs.wave2.foundation13."+key
  term=source_terms.get(tid);ob=observations.get(oid)
  if not term or not ob or term["locator"]!=case["url"] or ob["locator"]!=case["url"] or ob["term_id"]!=tid or ob["record_kind"]!="paraphrase":
   raise PipelineError("Missing exact independent source attribution "+key)
  if ob["human_verified"] is not False or len(case["reason"])<180:
   raise PipelineError("Unreviewed evidence or insufficient mathematical rationale "+key)
  mid="meaning.wave2.foundation13."+key;fid="form.wave2.foundation13."+key
  candidates.append({"id":mid,"term_group_id":"wave2.foundation13."+case["group"],
    "display_term":case["term"],"context":case["context"],"term_ids":[tid],
    "editorial_status":"candidate_independent_context_screen","human_verified":False,
    "formulations":[{"id":fid,"text":case["text"],"evidence_ids":[oid],
       "review_state":"candidate","mathematical_scope_note":case["reason"],"human_verified":False}]})
  math_reviews.append({"meaning_id":mid,"formulation_id":fid,"source_url":case["url"],
    "source_observation_id":oid,"mathematical_reason":case["reason"],
    "mathematical_context":case["context"],
    "reviewed_by":"assistant_independent_mathematical_homological_screen_2026_10_19",
    "human_verified":False})
 if candidates[0]["term_group_id"]!=candidates[1]["term_group_id"]:
  raise PipelineError("Concrete and universal kernel formulations must share term heading")
 if candidates[1]["context"]==candidates[0]["context"]:
  raise PipelineError("Do not conflate distinct kernel mathematical contexts")
 def write(path,records):
  path.parent.mkdir(parents=True,exist_ok=True)
  text=chr(10).join(canonical(x) for x in records)+chr(10)
  if path.exists() and path.read_text(encoding="utf-8")!=text:
   raise PipelineError("Existing independent source/meaning evidence differs "+str(path))
  path.write_text(text,encoding="utf-8")
  return path
 intake=write(w.root/"intake/wave2_foundation_meanings_batch_14.jsonl",candidates)
 if len(original)==455:
  w.ingest("meanings",intake,batch_size=4)
 else:
  for proposed in candidates:
   got=original.get(proposed["id"])
   if not got or got["formulations"][0]["text"]!=proposed["formulations"][0]["text"]:
    raise PipelineError("Existing candidate differs from individually reviewed text")
 for case in CASES:
  mid="meaning.wave2.foundation13."+case["slug"]
  old=w.records("meanings")[mid];form=old["formulations"][0]
  if form["review_state"]=="screened":
   if old.get("editorial_screening_reason")!=case["reason"]:
    raise PipelineError("Existing mathematical screening differs")
   continue
  if form["review_state"]!="candidate":
   raise PipelineError("Expected candidate before mathematical screening")
  new=dict(old)
  new["formulations"]=[dict(form,review_state="screened",human_verified=False,
    source_screened_by="assistant_independent_mathematical_homological_screen_2026_10_19")]
  new["editorial_status"]="individually_source_mathematically_screened"
  new["editorial_screening_reason"]=case["reason"]
  apply_revision(w.root,{"event_id":"revision.wave2.homological."+case["slug"]+".screen01",
    "stage":"meanings","record_id":mid,"before_digest":digest(old),
    "editor":"assistant_independent_mathematical_homological_screen_2026_10_19",
    "reason":case["reason"],"operation":"replace","replacement":new})
 write(w.root/"wave2/foundation_meaning_review_batch_14.jsonl",math_reviews)
 meanings=w.records("meanings")
 forms={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
 if len(meanings)!=459 or len(forms)!=471 or any(f["review_state"]!="screened" for m in meanings.values() for f in m["formulations"]):
  raise PipelineError("Mathematically screened meaning catalog incorrect")
 current=w.root/"state/wave2_formulation_reviews.jsonl"
 snapshot=w.root/"state/wave2_formulation_reviews_snapshot_467_before_homological14.jsonl"
 before=jsonl(current)
 if len(before)==467:
  if len(set(r["formulation_id"] for r in before))!=467 or {rid for r in before for rid in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Historical reviewed relationship set incomplete")
  oldtext=current.read_text(encoding="utf-8")
  if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=oldtext:
   raise PipelineError("Historic review snapshot conflicts")
  snapshot.write_text(oldtext,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_467_before_homological14.json",{
    "historic_reviews":467,"screened_links":606,
    "sha256":hashlib.sha256(oldtext.encode("utf-8")).hexdigest(),
    "old_meaning_digest":before[0]["meaning_catalog_digest"],"human_peer_verified":False})
  dg=digest(list(meanings.values()))
  new=[dict(r,meaning_catalog_digest=dg) for r in before]
  for item in candidates:
   new.append({"formulation_id":item["formulations"][0]["id"],"meaning_id":item["id"],
     "meaning_catalog_digest":dg,"decision":"needs_review","relation_ids":[],
     "original_wave1_disposition":None,"source":"individual_homological_source_screen",
     "editorial_reason":"Requires an independently justified contextual prerequisite review; no keyword-only links.",
     "reviewed_by":None,"human_verified":False})
  atomic_jsonl(current,sorted(new,key=lambda r:r["formulation_id"]))
 elif len(before)==471:
  if not snapshot.exists() or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in before):
   raise PipelineError("Existing mathematical review rebase differs")
 else:
  raise PipelineError("Unexpected review ledger cardinality")
 historic=jsonl(snapshot);current_rows=jsonl(current)
 indexed={r["formulation_id"]:r for r in current_rows}
 if len(historic)!=467 or len(current_rows)!=471 or len(indexed)!=471:
  raise PipelineError("Historical reviews lost identities")
 for r in historic:
  changed=indexed.get(r["formulation_id"])
  if changed is None or any(changed.get(k)!=v for k,v in r.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Existing mathematical relationship review was altered")
 if {rid for r in current_rows for rid in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("New meaning screen disrupted screened relations")
 if dict(Counter(r["decision"] for r in current_rows))!={
     "linked":461,"no_supported_target":5,"held_ambiguity":1,"needs_review":4}:
  raise PipelineError("Unexpected new mathematical review dispositions")
 check_cycles(meanings,w.records("relations"))
 state=w.state("meanings")
 state.update(total=459,record_digest=digest(list(meanings.values())),
    screened_new_formulations=40,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 summary={"phase":"four_homological_math_contexts_source_screened",
  "contextual_meanings":459,"formulation_reviews":471,
  "screened_relations_preserved":606,"previous_review_rows_preserved":467,
  "pending_individual_link_reviews":4,
  "concrete_and_categorical_kernels_context_specific":True,
  "preadditive_kernels_cokernels_not_assumed_to_exist":True,
  "abelian_category_required_for_image_kernel_exactness":True,
  "all_stages_unsealed":True,"original_production_mathdef_consulted":False,
  "human_peer_verified":False,
  "next":"Source and screen additive/preadditive/abelian category prerequisites and precise snake-lemma dependencies before link approval."}
 atomic_json(w.root/"state/wave2_foundations_batch_14_screened.json",summary)
 return summary

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
