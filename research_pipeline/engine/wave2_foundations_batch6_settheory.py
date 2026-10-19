"""Independent source intake for four missing elementary foundations.

Only after audited four-meaning/18-link expansion, add ProofWiki monoid,
binary-operation, binary-relation and Cartesian-product source observations.
This script records source-scoped mathematical paraphrases, NOT screen meanings
or infer relations; variants are preserved explicitly in observation notes.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

SPECS=[
 dict(slug="monoid",label="monoid with identity",
      url="https://proofwiki.org/wiki/Definition%3AMonoid",
      context="Algebra: nonempty semigroup with two-sided identity, no inverses required",
      text="A monoid is a nonempty set M equipped with an associative binary operation M×M→M and an element e∈M such that e⋆x=x=x⋆e for every x∈M.",
      note="Direct ProofWiki monoid axioms S0–S2 read: closure, associativity and identity. This notion does not require inverses or commutativity.",
      variants=["associative operation and identity as data","semigroup with an identity"]),
 dict(slug="binary-operation",label="binary operation (external and closed variants)",
      url="https://proofwiki.org/wiki/Definition%3AOperation/Binary_Operation",
      context="Set algebra: mapping of two inputs versus internal operation closed on a carrier",
      text="A binary operation with input sets S,T and outputs in U is a function ⋆:S×T→U. For an internal binary operation on S the type is ⋆:S×S→S, making closure on S part of the signature.",
      note="The ProofWiki source explicitly contrasts its general two-input mapping definition with the frequently used alternative where codomain equals carrier. These are not automatically the same type.",
      variants=["general two-domain S×T→U binary operation","closed internal S×S→S binary operation"]),
 dict(slug="binary-relation",label="binary relation (typed and graph-only conventions)",
      url="https://proofwiki.org/wiki/Definition%3ARelation",
      context="Set theory: relation as S,T,R triple or truth-set R⊆S×T",
      text="A binary relation from S to T may be represented by a triple (S,T,R) where R⊆S×T; in an alternative common treatment, the relation is identified with the subset R⊆S×T itself. A relation on S uses T=S.",
      note="Direct ProofWiki primary definition treats S,T as part of the relation; the separately labeled 'also defined as' treatment identifies only the subset. Two equivalent usage contexts need not represent identical objects.",
      variants=["typed triple (S,T,R) relation","subset R of Cartesian product with carrier context"]),
 dict(slug="cartesian-product",label="Cartesian product of two sets",
      url="https://proofwiki.org/wiki/Definition%3ACartesian_Product",
      context="Set theory: binary Cartesian product of sets and ordered pairs",
      text="For sets S and T, the Cartesian product S×T is the set of ordered pairs (s,t) such that s∈S and t∈T.",
      note="Direct ProofWiki binary set-product definition read. Keep finite, indexed and infinite products as distinct formulations/contexts rather than conflating them with binary S×T.",
      variants=["binary Cartesian product of sets"])
]

def run(root):
 w=Workspace(root)
 baseline=w.root/"state/baseline.json"
 if not baseline.exists() or json.loads(baseline.read_text(encoding="utf-8")).get("mode")!="second_wave":
  raise PipelineError("Only independent Wave 2 second-wave fork supported")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Refuse to mutate a sealed source or mathematical stage")
 report=w.root/"state/wave2_link_review_batch_06.json"
 if not report.exists() or json.loads(report.read_text(encoding="utf-8")).get("total_screened_links")!=563:
  raise PipelineError("Requires committed successful new-meaning and 18-relation review batch")
 old={x:len(w.records(x)) for x in ("sources","terms","observations","meanings","relations")}
 if old not in [
  {"sources":9,"terms":343,"observations":766,"meanings":435,"relations":563},
  {"sources":9,"terms":347,"observations":770,"meanings":435,"relations":563}
 ]:
  raise PipelineError("Unexpected source expansion input state: "+str(old))
 src=w.records("sources").get("src.proofwiki")
 if not src or src["access"]!="free" or src["rights"] not in ("permitted","locator_only"):
  raise PipelineError("Research source permission or access restriction")
 terms=[];observations=[];source_research=[]
 for inp in SPECS:
  tid="term.wave2.proofwiki.foundation06."+inp["slug"]
  oid="obs.wave2.proofwiki.foundation06."+inp["slug"]
  terms.append({
   "id":tid,"label":inp["label"],"source_id":"src.proofwiki",
   "locator":inp["url"],
   "discovery_provenance":"independent_direct_ProofWiki_definition_read_2026_10_19",
   "human_verified":False
  })
  observations.append({
   "id":oid,"term_id":tid,"source_id":"src.proofwiki","locator":inp["url"],
   "record_kind":"paraphrase","text":inp["text"],"context":inp["context"],
   "editorial_note":inp["note"],
   "potential_contextual_variants":inp["variants"],
   "reviewed_by":"assistant_independent_foundational_math_source_review_2026_10_19",
   "human_verified":False
  })
  source_research.append({
   "term_id":tid,"source_id":"src.proofwiki","locator":inp["url"],
   "source_access_outcome":"direct_page_read","candidate_observation_id":oid,
   "editorial_reason":inp["note"],"source_research_complete":True,
   "contextual_variant_leads":inp["variants"],"meaning_screened":False,
   "human_verified":False
  })
 def store(p,items):
  p.parent.mkdir(parents=True,exist_ok=True)
  output=chr(10).join(canonical(x) for x in items)+chr(10)
  if p.exists() and p.read_text(encoding="utf-8")!=output:
   raise PipelineError("Prior independent source research batch differs: "+str(p))
  p.write_text(output,encoding="utf-8")
  return p
 tr=w.ingest("terms",store(w.root/"intake/foundations_batch_06_terms.jsonl",terms),batch_size=4)
 or_=w.ingest("observations",store(w.root/"intake/foundations_batch_06_observations.jsonl",observations),batch_size=4)
 store(w.root/"wave2/foundation_source_discovery_batch_06.jsonl",source_research)
 actual={x:len(w.records(x)) for x in ("sources","terms","observations","meanings","relations")}
 expected={"sources":9,"terms":347,"observations":770,"meanings":435,"relations":563}
 if actual!=expected:
  raise PipelineError("Incorrect source intake counts: "+str(actual))
 result={
  "phase":"four_more_direct_proofwiki_source_observations_held_as_candidates",
  "sources_read":4,"new_source_term_records":4,"new_observations":4,
  "possible_definition_formulation_variants":7,
  "counts":actual,
  "idempotent_term_skips":tr["already_present"],"idempotent_observation_skips":or_["already_present"],
  "source_scope_cautions":["general binary operation and internally closed one not identical signatures",
    "typed relation triple and graph-only relation not identical mathematical objects",
    "set may be a primitive notion in axiomatic set theory; do not invent an informal ZFC definition"],
  "mathematically_screened_meanings_from_this_batch":0,
  "link_stage_sealed":False,"source_stage_sealed":False,
  "original_production_mathdef_consulted":False,"human_peer_verified":False,
  "next":"Archive existing 343-term source review; screen context-specific operation and relation variants only after independent mathematical cross-check."
 }
 atomic_json(w.root/"state/wave2_foundations_batch_06.json",result)
 return result

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--workspace",type=Path,required=True)
 a=ap.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
