"""Screen six source-specific algebra, order and topology foundation meanings.

Preserve 459 prior individual link reviews and 582 screened links. The six
contexts include unital versus general ring maps, and general versus nonempty
topological subspaces. The source well-ordering formula is corrected to require
least elements only for nonempty subsets.
"""
from __future__ import annotations
import argparse,json,hashlib
from collections import Counter
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

ITEMS=[
 dict(slug="reduced-ring",source_slug="reduced-ring",title="reduced ring",group="ring-reduced",
  context="Algebra: associative ring, not necessarily unital, with no nonzero nilpotent elements",
  text="An associative ring R is reduced if for every r∈R and every positive integer n, the equality r^n=0 implies r=0. Equivalently, its only nilpotent element is zero.",
  reason="ProofWiki's reduced-ring definition excludes nonzero nilpotents. The independently sourced general ring convention does not force 1 or commutativity. A reduced ring need not be a domain (products of domains give examples)."),
 dict(slug="ring-map-general",source_slug="ring-homomorphism",title="ring homomorphism",group="ring-homomorphism",
  context="Additive/multiplicative homomorphism between associative rings; no required preservation of unity",
  text="A ring homomorphism φ:R→S between associative rings is a mapping satisfying φ(a+b)=φ(a)+φ(b) and φ(ab)=φ(a)φ(b) for all a,b∈R. If both rings carry identity elements, this definition alone does not require φ(1_R)=1_S.",
  reason="ProofWiki's primary ring-homomorphism definition requires preserving addition and multiplication but does not require preservation of multiplicative identities. Separate the more restrictive unital convention rather than silently adding that axiom."),
 dict(slug="ring-map-unital",source_slug="ring-homomorphism",title="ring homomorphism",group="ring-homomorphism",
  context="Unital ring homomorphism, with preservation of multiplicative identities",
  text="For rings R and S with specified identities, a unital ring homomorphism φ:R→S is an additive and multiplicative homomorphism additionally satisfying φ(1_R)=1_S.",
  reason="ProofWiki's 'also defined as' explicitly documents authors who use 'ring homomorphism' to mean a unital homomorphism. This stronger convention requires preserving one, unlike the page's primary nonunital convention."),
 dict(slug="well-ordered-set",source_slug="well-ordered-set",title="well-ordered set",group="well-order",
  context="Order theory: total order with a least element in every nonempty subset",
  text="A well-ordered set is a pair (S,≤) in which ≤ is a total order and every nonempty subset A⊆S has a least element: there exists a∈A such that a≤x for all x∈A.",
  reason="ProofWiki correctly states the nonempty-subset condition in prose, although one displayed formula accidentally leaves it out. The revised independent wording includes the restriction explicitly; the empty ordered set is well-ordered vacuously."),
 dict(slug="subspace-topology-general",source_slug="topological-subspace",title="subspace topology",group="subspace-topology",
  context="General topological subspace including the empty subset when allowed",
  text="For a topological space (X,τ) and any subset A⊆X, the subspace topology on A is τ_A={A∩U:U∈τ}; the pair (A,τ_A) is the resulting topological subspace. This includes A=∅.",
  reason="ProofWiki's topological-subspace source provides the intersections-with-opens construction and a convention permitting the empty topological subspace. The independent general topology already admits the empty space."),
 dict(slug="subspace-topology-nonempty",source_slug="topological-subspace",title="subspace topology",group="subspace-topology",
  context="Restricted nonempty topological subspace convention",
  text="If a topological-space convention requires nonempty spaces, a topological subspace of (X,τ) is a nonempty subset A⊆X equipped with τ_A={A∩U:U∈τ}. Empty A is excluded only by this source convention.",
  reason="The ProofWiki source discusses authors who exclude empty topological spaces and thereby restrict topological subspaces to nonempty carriers. Keep this stronger convention separate from the empty-allowed formulation.")
]
SOURCE={
 "reduced-ring":"https://proofwiki.org/wiki/Definition%3AReduced_Ring",
 "ring-homomorphism":"https://proofwiki.org/wiki/Definition%3ARing_Homomorphism",
 "well-ordered-set":"https://proofwiki.org/wiki/Definition%3AWell-Ordered_Set",
 "topological-subspace":"https://proofwiki.org/wiki/Definition%3ASubspace_Topology"
}

def run(root):
 w=Workspace(root)
 if json.loads((w.root/"state/baseline.json").read_text()).get("mode")!="second_wave":
  raise PipelineError("Independent editable Wave 2 lineage required")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Sealed stages cannot be mutated")
 if (len(w.records("terms")),len(w.records("observations")),len(w.records("relations")))!=(354,777,582):
  raise PipelineError("Four-source intake and all 582 links must be committed before screening")
 proof=w.root/"state/wave2_foundations_batch_09.json"
 if not proof.exists() or not json.loads(proof.read_text()).get("no_new_meanings_screened"):
  raise PipelineError("Source evidence intake report absent")
 existing=w.records("meanings")
 if len(existing) not in (447,453):
  raise PipelineError("Unexpected existing independently screened meanings")
 termrecords=w.records("terms"); observations=w.records("observations")
 candidates=[]
 for item in ITEMS:
  key=item["source_slug"]
  tid="term.wave2.proofwiki.foundation09."+key
  oid="obs.wave2.proofwiki.foundation09."+key
  t=termrecords.get(tid);o=observations.get(oid)
  if not t or not o or t["locator"]!=SOURCE[key] or o["locator"]!=SOURCE[key] or o["term_id"]!=tid:
   raise PipelineError("Misidentified source or observation: "+key)
  if o["record_kind"]!="paraphrase" or o["human_verified"] is not False or len(item["reason"])<140:
   raise PipelineError("Insufficient separately audited source rationale: "+key)
  mid="meaning.wave2.foundation."+item["slug"]
  fid="form.wave2.foundation."+item["slug"]
  candidates.append({"id":mid,"term_group_id":"wave2.foundation."+item["group"],
    "display_term":item["title"],"context":item["context"],"term_ids":[tid],
    "formulations":[{"id":fid,"text":item["text"],"evidence_ids":[oid],
       "review_state":"candidate","human_verified":False,
       "mathematical_scope_note":item["reason"]}],
    "editorial_status":"candidate_awaiting_specific_mathematical_review","human_verified":False})
 def store(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  txt=chr(10).join(canonical(x) for x in rows)+chr(10)
  if path.exists() and path.read_text(encoding="utf-8")!=txt:
   raise PipelineError("Existing independent research evidence differs: "+str(path))
  path.write_text(txt,encoding="utf-8")
  return path
 incoming=store(w.root/"intake/wave2_foundation_meanings_batch_10.jsonl",candidates)
 if len(existing)==447:
  w.ingest("meanings",incoming,batch_size=6)
 else:
  for c in candidates:
   current=existing.get(c["id"])
   if not current or current["formulations"][0]["text"]!=c["formulations"][0]["text"]:
    raise PipelineError("Existing meaning formulation differs")
 reviews=[]
 for item in ITEMS:
  mid="meaning.wave2.foundation."+item["slug"]
  m=w.records("meanings")[mid]; f=m["formulations"][0]
  reviews.append({"meaning_id":mid,"formulation_id":f["id"],
      "source_url":SOURCE[item["source_slug"]],
      "source_observation_id":"obs.wave2.proofwiki.foundation09."+item["source_slug"],
      "mathematical_reason":item["reason"],
      "mathematical_context":item["context"],
      "source_screened_by":"assistant_independent_source_scope_review_2026_10_19",
      "human_verified":False})
  if f["review_state"]=="screened":
   if m.get("editorial_screening_reason")!=item["reason"]:
    raise PipelineError("Previously screened context rationale changed")
   continue
  if f["review_state"]!="candidate":raise PipelineError("Expected pending candidate")
  updated=dict(m)
  updated["formulations"]=[dict(f,review_state="screened",
    source_screened_by="assistant_independent_source_scope_review_2026_10_19",human_verified=False)]
  updated["editorial_status"]="individual_source_math_scope_screened"
  updated["editorial_screening_reason"]=item["reason"]
  apply_revision(w.root,{"event_id":"revision.wave2.foundation10."+item["slug"]+".screen01",
      "stage":"meanings","record_id":mid,"before_digest":digest(m),
      "editor":"assistant_independent_source_scope_review_2026_10_19",
      "reason":item["reason"],"operation":"replace","replacement":updated})
 store(w.root/"wave2/foundation_meaning_review_batch_10.jsonl",reviews)
 meanings=w.records("meanings")
 forms={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
 if len(meanings)!=453 or len(forms)!=465 or any(f["review_state"]!="screened" for m in meanings.values() for f in m["formulations"]):
  raise PipelineError("Six mathematical foundations not individually screened")
 current=w.root/"state/wave2_formulation_reviews.jsonl"
 historical=w.root/"state/wave2_formulation_reviews_snapshot_459_before_foundations10.jsonl"
 prior=jsonl(current)
 if len(prior)==459:
  if len(set(r["formulation_id"] for r in prior))!=459 or {rid for r in prior for rid in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Incomplete 459 review history before context expansion")
  original=current.read_text(encoding="utf-8")
  if historical.exists() and historical.read_text(encoding="utf-8")!=original:
   raise PipelineError("Immutable 459-review historical snapshot differs")
  historical.write_text(original,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_459_before_foundations10.json",{
    "review_count":459,"link_count":582,"sha256":hashlib.sha256(original.encode("utf-8")).hexdigest(),
    "human_peer_verified":False})
  newdigest=digest(list(meanings.values()))
  newer=[dict(r,meaning_catalog_digest=newdigest) for r in prior]
  for m in candidates:
   newer.append({"formulation_id":m["formulations"][0]["id"],"meaning_id":m["id"],
     "meaning_catalog_digest":newdigest,"decision":"needs_review","relation_ids":[],
     "original_wave1_disposition":None,"source":"new_individual_source_review_foundation10",
     "editorial_reason":"Newly source-screened formulation; independently investigate exact prerequisite relationships.",
     "reviewed_by":None,"human_verified":False})
  atomic_jsonl(current,sorted(newer,key=lambda x:x["formulation_id"]))
 elif len(prior)==465:
  if not historical.exists() or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in prior):
   raise PipelineError("Previously expanded reviews not source synchronized")
 else:raise PipelineError("Unexpected relation review cardinality")
 older=jsonl(historical); current_reviews=jsonl(current)
 index={r["formulation_id"]:r for r in current_reviews}
 if len(older)!=459 or len(index)!=465:
  raise PipelineError("Lost mathematical review identities")
 for r in older:
  p=index.get(r["formulation_id"])
  if p is None or any(p.get(k)!=value for k,value in r.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Original reviewed disposition changed without audit")
 if {rid for r in current_reviews for rid in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Screened links lost relationship ledger coverage")
 count=dict(Counter(x["decision"] for x in current_reviews))
 if count!={"linked":444,"no_supported_target":14,"held_ambiguity":1,"needs_review":6}:
  raise PipelineError("Earlier reviewed mathematical meaning dispositions changed unexpectedly "+str(count))
 check_cycles(meanings,w.records("relations"))
 state=w.state("meanings")
 state.update(total=453,record_digest=digest(list(meanings.values())),
       screened_new_formulations=34,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 report={"phase":"six_new_algebra_order_topology_contexts_individually_screened",
   "source_term_count":354,"source_observations":777,
   "contextual_meanings":453,"formulation_reviews":465,
   "screened_links_preserved":582,"historical_review_rows_preserved":459,
   "new_formulation_reviews_pending":6,
   "unital_and_nonunital_ring_maps_distinct":True,
   "wellorder_nonempty_subset_requirement_checked":True,
   "subspace_empty_carrier_conventions_separate":True,
   "review_dispositions":count,"human_peer_verified":False,
   "stages_unsealed":True,"original_production_mathdef_consulted":False,
   "next":"Source-screen individual relations and no-target decisions for these six formulations; do not invent links from name similarity."}
 atomic_json(w.root/"state/wave2_foundations_batch_10_screened.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",required=True,type=Path)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
