"""Individual mathematical screening of Stacks 10.38.1 and Stacks 10.112.5.

Require exact source evidence. Preserve 489 reviewed formulations, 643 links,
and frozen Wave 1. Never change production mathDef definitions or citations.
"""
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

DEFS=[
 dict(key="integral-over-ideal",name="element integral over an ideal",
  url="https://stacks.math.columbia.edu/tag/037E",
  context="Stacks Definition 10.38.1: integrality over an ideal along a commutative ring homomorphism",
  body="Let φ:R→S be a homomorphism of commutative rings and let I⊆R be an ideal. An element g∈S is integral over I if there are d≥1 and a monic polynomial P(T)=T^d+Σ_{j=0}^{d−1}a_jT^j, where a_j∈I^{d−j}, such that φ(P)(g)=0 in S.",
  reason="Stacks Definition 10.38.1 explicitly requires a monic annihilating polynomial with its coefficient a_j in I^(d-j). It is integrality over a chosen ideal I along φ, not merely integrality over R with arbitrary ring coefficients. The ring-map and coefficient-power hypotheses are mathematically essential."),
 dict(key="local-ring-fibre-at-prime",name="local ring of a fibre at a prime",
  url="https://stacks.math.columbia.edu/tag/00OG",
  context="Stacks Definition 10.112.5: local ring of fibre at prime q lying above prime p",
  body="Let R→S be a homomorphism of commutative rings. For a prime ideal q⊆S with contraction p=q∩R, the local ring of the fibre at q is S_q/pS_q. Equivalently, it is the localization of the fibre ring S⊗_Rκ(p) at the prime corresponding to q.",
  reason="Stacks Definition 10.112.5 identifies the local ring S_q/pS_q at a specified prime q over p. This is neither S_q alone nor the entire fibre scheme Spec(S⊗_Rκ(p)). The chosen prime, its contraction, residue field and localization are retained explicitly.")
]

def run(root):
 w=Workspace(root)
 base=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if base.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Only unsealed independent Wave 2 can be screened")
 evidence=w.root/"state/wave2_foundations_batch_33.json"
 if not evidence.exists():raise PipelineError("Missing reviewed direct-source intake")
 er=json.loads(evidence.read_text(encoding="utf-8"))
 if not er.get("coefficient_powers_I_d_minus_j_preserved") or not er.get("fibre_prime_and_contraction_hypotheses_preserved"):
  raise PipelineError("Mathematical source scope guard failed")
 if any(len(w.records(k))!=n for k,n in (("terms",376),("observations",799),("relations",643))):
  raise PipelineError("Source or link baseline unexpected")
 before=w.records("meanings")
 if len(before) not in (477,479):raise PipelineError("Unexpected preceding meanings")
 termmap=w.records("terms");observations=w.records("observations")
 items=[]
 for d in DEFS:
  k=d["key"];tid="term.wave2.foundation33."+k;oid="obs.wave2.foundation33."+k
  term,obs=termmap.get(tid),observations.get(oid)
  if not term or not obs or obs["term_id"]!=tid or term["locator"]!=d["url"] or obs["locator"]!=d["url"] or obs["record_kind"]!="paraphrase" or obs["human_verified"] is not False:
   raise PipelineError("No individually screened Stacks observation "+k)
  if len(d["reason"])<175 or len(d["body"])<175:
   raise PipelineError("Definition/math rationale too short for direct-screen gate "+k)
  items.append({"id":"meaning.wave2.foundation."+k,"display_term":d["name"],
   "term_group_id":"wave2.foundation."+k,"context":d["context"],"term_ids":[tid],
   "human_verified":False,"editorial_status":"independent_source_candidate",
   "formulations":[{"id":"form.wave2.foundation."+k,"text":d["body"],"evidence_ids":[oid],
     "review_state":"candidate","human_verified":False}]})
 def store(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  value="".join(canonical(x)+"\n" for x in rows)
  if path.exists() and path.read_text(encoding="utf-8")!=value:
   raise PipelineError("Source-specific candidate changed")
  path.write_text(value,encoding="utf-8")
  return path
 intake=store(w.root/"intake/foundations_batch_34_meaning_candidates.jsonl",items)
 if len(before)==477:
  w.ingest("meanings",intake,batch_size=2)
 else:
  if any(before.get(x["id"],{}).get("formulations",[{}])[0].get("text")!=x["formulations"][0]["text"] for x in items):
   raise PipelineError("Previously screened candidate differs")
 review=[]
 for d in DEFS:
  k=d["key"];mid="meaning.wave2.foundation."+k;m=w.records("meanings")[mid]
  f=m["formulations"][0]
  review.append({"meaning_id":mid,"formulation_id":f["id"],"source_locator":d["url"],
   "source_observation_id":"obs.wave2.foundation33."+k,"mathematical_reason":d["reason"],
   "reviewed_by":"assistant_independent_stacks_two_embedded_definitions_review_2026_10_19",
   "decision":"source_scoped_definition_screen","human_verified":False})
  if f["review_state"]=="candidate":
   revised=dict(m)
   revised["formulations"]=[dict(f,review_state="screened",
      source_screened_by="assistant_independent_stacks_two_embedded_definitions_review_2026_10_19",
      human_verified=False)]
   revised["editorial_screening_reason"]=d["reason"]
   revised["editorial_status"]="mathematically_screened_with_exact_stacks_source"
   revised["human_verified"]=False
   apply_revision(w.root,{"event_id":"revision.wave2.embedded34."+k+".screen01",
      "stage":"meanings","record_id":mid,"before_digest":digest(m),
      "editor":"assistant_independent_stacks_two_embedded_definitions_review_2026_10_19",
      "reason":d["reason"],"operation":"replace","replacement":revised})
  elif f["review_state"]!="screened" or m.get("editorial_screening_reason")!=d["reason"]:
   raise PipelineError("Previously revised mathematical meaning conflicts")
 store(w.root/"wave2/foundation_meaning_review_batch_34.jsonl",review)
 meanings=w.records("meanings")
 forms={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
 if len(meanings)!=479 or len(forms)!=491 or any(f["review_state"]!="screened" for m in meanings.values() for f in m["formulations"]):
  raise PipelineError("Expected 479 screened meanings and 491 reviewed formulations")
 ledger=w.root/"state/wave2_formulation_reviews.jsonl"
 previous=jsonl(ledger)
 snap=w.root/"state/wave2_formulation_reviews_snapshot_489_before_embedded34.jsonl"
 if len(previous)==489:
  if len({x["formulation_id"] for x in previous})!=489 or {i for x in previous for i in x["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Prior relationship review history is incomplete")
  old=ledger.read_text(encoding="utf-8")
  if snap.exists() and snap.read_text(encoding="utf-8")!=old:
   raise PipelineError("Immutable prior 489-review snapshot differs")
  snap.write_text(old,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_489_before_embedded34.json",{
   "review_count":489,"screened_links":643,"sha256":hashlib.sha256(old.encode("utf-8")).hexdigest(),
   "human_peer_verified":False})
  curr_digest=digest(list(meanings.values()))
  updated=[dict(x,meaning_catalog_digest=curr_digest) for x in previous]
  for x in items:
   updated.append({"formulation_id":x["formulations"][0]["id"],"meaning_id":x["id"],
      "meaning_catalog_digest":curr_digest,"decision":"needs_review","relation_ids":[],
      "original_wave1_disposition":None,
      "source":"independent_direct_stacks_numbered_embedded_definition",
      "editorial_reason":"New source-scoped mathematical formulation requires individual prerequisite review.",
      "reviewed_by":None,"human_verified":False})
  atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
 elif len(previous)==491:
  if not snap.exists() or any(x["meaning_catalog_digest"]!=digest(list(meanings.values())) for x in previous):
   raise PipelineError("Expanded formulation ledger no longer matches catalog")
 else:raise PipelineError("Formulation review baseline count changed")
 historical=jsonl(snap);rows=jsonl(ledger);by={x["formulation_id"]:x for x in rows}
 if len(historical)!=489 or len(rows)!=491 or len(by)!=491:
  raise PipelineError("Historical review identities were lost")
 for p in historical:
  x=by.get(p["formulation_id"])
  if x is None or any(x.get(k)!=v for k,v in p.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Historical reviewed decision rewritten")
 if {i for x in rows for i in x["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Screened mathematical dependency lost provenance")
 if sum(x["decision"]=="needs_review" for x in rows)!=2:
  raise PipelineError("Exactly two new source-specific link reviews expected")
 check_cycles(meanings,w.records("relations"))
 state=w.state("meanings")
 state.update(total=479,record_digest=digest(list(meanings.values())),
              screened_new_formulations=60,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 result={"phase":"two_individual_embedded_Stacks_definitions_screened",
  "screened_meanings":479,"formulation_reviews":491,"new_independent_meanings":2,
  "previous_489_reviews_preserved":True,"screened_links_unchanged":643,
  "ideal_coefficient_power_hypotheses_explicit":True,
  "fibre_prime_contraction_and_local_ring_explicit":True,
  "new_link_reviews_pending":2,"stages_unsealed":True,
  "human_peer_verified":False,"original_production_mathdef_consulted":False,
  "next":"Individually justify links to ideal, ring-map, prime and localization meanings without automatically treating a fibre scheme as the same object."}
 atomic_json(w.root/"state/wave2_embedded34_meaning_screen.json",result)
 return result

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--workspace",type=Path,required=True)
 a=ap.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
