"""Source-screen sigma-algebra and countably additive measure as separate Wave 2 meanings.

Preserve exactly 486 historical formulation reviews, all 634 mathematical links,
the frozen independent Wave 1, and explicit distinction from topological open
sets and Riemann integration. No production corpus used.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

DEFINITIONS=[
 dict(key="sigma-algebra",label="sigma-algebra",
  context="Measure theory: family of subsets closed under relative complements and countable unions",
  text="Let X be a set. A sigma-algebra on X is a family Σ⊆P(X) containing X, closed under taking complements X\\A for A∈Σ, and closed under countable unions ⋃_{n≥1}A_n of members A_n∈Σ.",
  reason="ProofWiki Sigma-Algebra, Definition 1, explicitly requires X to lie in Σ, closure under complements relative to X, and closure under countable unions. A sigma-algebra differs from a topology and need not contain every subset of X. The empty set follows from closure under complements."),
 dict(key="nonnegative-measure",label="nonnegative measure",
  context="Measure theory: extended nonnegative countably additive set function on a sigma-algebra",
  text="Let Σ be a sigma-algebra of subsets of X. A nonnegative measure on (X,Σ) is a function μ:Σ→[0,+∞] with μ(∅)=0 and μ(⋃_{n≥1}E_n)=∑_{n≥1}μ(E_n) for every sequence (E_n) of pairwise disjoint sets in Σ.",
  reason="ProofWiki Measure (Measure Theory), Definition 2, requires nonnegative extended-real values, zero on the empty set, and countable additivity over pairwise disjoint measurable sets. It does not require μ(X)=1, finite total measure, or a previously defined Lebesgue-Stieltjes integral.")
]
def run(root):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
       ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Only unsealed independent Wave 2 is mutable")
 proof=w.root/"state/wave2_foundations_batch_26.json"
 if not proof.exists() or not json.loads(proof.read_text()).get("countable_additivity_and_empty_set_axiom_preserved"):
  raise PipelineError("Direct mathematical source evidence not yet audited")
 expect={"sources":9,"terms":373,"observations":796,"relations":634}
 if any(len(w.records(s))!=n for s,n in expect.items()):
  raise PipelineError("Unexpected source/relationship count before meaning expansion")
 previous=w.records("meanings")
 if len(previous) not in (474,476):
  raise PipelineError("Incorrect preceding mathematical meaning count")
 terms,obs=w.records("terms"),w.records("observations")
 candidates=[]
 for item in DEFINITIONS:
  key=item["key"]
  tid="term.wave2.foundation26."+key
  oid="obs.wave2.foundation26."+key
  t,o=terms.get(tid),obs.get(oid)
  if (not t or not o or o["term_id"]!=tid or o["locator"]!=t["locator"] or
     o["record_kind"]!="paraphrase" or o.get("human_verified") is not False):
   raise PipelineError("Missing individually attributed source evidence: "+key)
  if len(item["reason"])<165 or len(item["text"])<115:
   raise PipelineError("Mathematical rationale incomplete: "+key)
  candidates.append({"id":"meaning.wave2.foundation."+key,
   "term_group_id":"wave2.foundation."+key,
   "display_term":item["label"],"context":item["context"],
   "term_ids":[tid],"human_verified":False,
   "editorial_status":"source_scoped_candidate",
   "formulations":[{"id":"form.wave2.foundation."+key,
      "text":item["text"],"evidence_ids":[oid],
      "review_state":"candidate","human_verified":False}]
  })
 def store(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  payload="".join(canonical(row)+"\n" for row in rows)
  if path.exists() and path.read_text(encoding="utf-8")!=payload:
   raise PipelineError("Immutable mathematical evidence payload differs")
  path.write_text(payload,encoding="utf-8")
  return path
 path=store(w.root/"intake/foundations_batch_27_meaning_candidates.jsonl",candidates)
 if len(previous)==474:
  w.ingest("meanings",path,batch_size=2)
 else:
  if any(previous.get(c["id"],{}).get("formulations",[{}])[0].get("text")!=c["formulations"][0]["text"] for c in candidates):
   raise PipelineError("Already screened definition text differs")
 individual=[]
 for spec in DEFINITIONS:
  key=spec["key"];mid="meaning.wave2.foundation."+key
  meaning=w.records("meanings")[mid]
  form=meaning["formulations"][0]
  individual.append({
   "meaning_id":mid,"formulation_id":form["id"],
   "source_observation_id":"obs.wave2.foundation26."+key,
   "source_locator":obs["obs.wave2.foundation26."+key]["locator"],
   "mathematical_reason":spec["reason"],"source_specific_context":spec["context"],
   "decision":"screen_independently_sourced_measure_theoretic_formulation",
   "reviewed_by":"assistant_independent_sigma_algebra_measure_context_review_2026_10_19",
   "human_verified":False})
  if form["review_state"]=="screened":
   if meaning.get("editorial_screening_reason")!=spec["reason"]:
    raise PipelineError("Previously screened meaning rationale changed")
   continue
  if form["review_state"]!="candidate":
   raise PipelineError("Unrecognized mathematical candidate review status")
  revised=dict(meaning)
  revised["formulations"]=[dict(form,review_state="screened",
    source_screened_by="assistant_independent_sigma_algebra_measure_context_review_2026_10_19",
    human_verified=False)]
  revised["editorial_screening_reason"]=spec["reason"]
  revised["editorial_status"]="source_specific_mathematical_meaning_screened"
  revised["human_verified"]=False
  apply_revision(w.root,{
   "event_id":"revision.wave2.foundation27."+key+".screen01",
   "stage":"meanings","record_id":mid,"before_digest":digest(meaning),
   "editor":"assistant_independent_sigma_algebra_measure_context_review_2026_10_19",
   "reason":spec["reason"],"operation":"replace","replacement":revised})
 store(w.root/"wave2/foundation_meaning_review_batch_27.jsonl",individual)
 meanings=w.records("meanings")
 allforms={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
 if len(meanings)!=476 or len(allforms)!=488:
  raise PipelineError("Incorrect screened sigma-algebra and measure count")
 if any(f["review_state"]!="screened" for m in meanings.values() for f in m["formulations"]):
  raise PipelineError("Candidate meaning unscreened")
 current=w.root/"state/wave2_formulation_reviews.jsonl"
 prev=jsonl(current)
 snap=w.root/"state/wave2_formulation_reviews_snapshot_486_before_measure27.jsonl"
 if len(prev)==486:
  if len({r["formulation_id"] for r in prev})!=486 or {x for r in prev for x in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Prior individual reviews or links missing")
  previous_content=current.read_text(encoding="utf-8")
  if snap.exists() and snap.read_text(encoding="utf-8")!=previous_content:
   raise PipelineError("Historical 486-review snapshot mismatch")
  snap.write_text(previous_content,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_486_before_measure27.json",{
   "review_count":486,"screened_relations":634,
   "sha256":hashlib.sha256(previous_content.encode("utf-8")).hexdigest(),
   "human_peer_verified":False})
  newdigest=digest(list(meanings.values()))
  reviewed=[dict(r,meaning_catalog_digest=newdigest) for r in prev]
  for candidate in candidates:
   reviewed.append({
     "formulation_id":candidate["formulations"][0]["id"],"meaning_id":candidate["id"],
     "meaning_catalog_digest":newdigest,"decision":"needs_review","relation_ids":[],
     "original_wave1_disposition":None,
     "source":"wave2_new_individual_measure_foundation",
     "editorial_reason":"Newly screened source-specific measure-theoretic meaning requires separate exact-prerequisite review.",
     "reviewed_by":None,"human_verified":False})
  atomic_jsonl(current,sorted(reviewed,key=lambda r:r["formulation_id"]))
 elif len(prev)==488:
  if not snap.exists() or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in prev):
   raise PipelineError("Previously expanded review catalog differs")
 else:
  raise PipelineError("Unexpected formulation review migration baseline")
 historical=jsonl(snap);rows=jsonl(current)
 by={r["formulation_id"]:r for r in rows}
 if len(historical)!=486 or len(rows)!=488 or len(by)!=488:
  raise PipelineError("Incorrect immutable review history cardinality")
 for r in historical:
  now=by.get(r["formulation_id"])
  if not now or any(now.get(k)!=v for k,v in r.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Prior mathematical review silently changed")
 if {x for r in rows for x in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Some old relation lost review lineage")
 check_cycles(meanings,w.records("relations"))
 if sum(r["decision"]=="needs_review" for r in rows)!=3:
  raise PipelineError("Expected one prior raw moment and two new measure-related link reviews")
 state=w.state("meanings")
 state.update(total=476,record_digest=digest(list(meanings.values())),
              screened_new_formulations=57,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 result={
   "phase":"screen_nonnegative_measure_and_sigma_algebra_meanings",
   "screened_contextual_meanings":476,
   "reviewed_formulations":488,
   "previous_486_review_rows_preserved":True,
   "screened_links_preserved":634,
   "new_individual_link_reviews_pending":3,
   "measure_normalization_at_empty_set_retained":True,
   "extended_nonnegative_measure_values_retained":True,
   "sigma_algebra_topology_conventions_not_equated":True,
   "riemann_vs_lebesgue_stieltjes_contexts_not_conflated":True,
   "all_wave2_stages_unsealed":True,
   "original_production_mathdef_consulted":False,"human_peer_verified":False,
   "next":"Review exactly source-anchored measure, sigma-algebra and raw-moment mathematical prerequisites, preserving all 488 individual reviews."
 }
 atomic_json(w.root/"state/wave2_foundations_batch_27_screened.json",result)
 return result

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--workspace",required=True,type=Path)
 a=ap.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
