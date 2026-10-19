"""Independent source-only Wave 2 intake: sigma-algebras and nonnegative measures.

These direct ProofWiki paraphrases establish mathematical source evidence,
without asserting that a Lebesgue–Stieltjes integral is a proper Riemann
integral or auto-screening any new definition or dependency.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

CASES=[
 dict(key="sigma-algebra",label="sigma-algebra of subsets of a set",
      url="https://proofwiki.org/wiki/Definition%3ASigma_Algebra",
      text="For a set X, a sigma-algebra Σ on X is a family Σ⊆P(X) such that X∈Σ; if A∈Σ then X\\A∈Σ; and for every countable sequence (A_n) with each A_n∈Σ, the union ⋃_{n≥1}A_n belongs to Σ.",
      note="Direct ProofWiki Definition 1. Countable-union and relative-complement conditions are not interchangeable with arbitrary-union topological axioms; X may be empty. Do not equate sigma-algebra with topology.",
      corroboration=["https://proofwiki.org/wiki/Definition%3ASigma_Algebra"]),
 dict(key="nonnegative-measure",label="nonnegative countably additive measure",
      url="https://proofwiki.org/wiki/Definition%3AMeasure_%28Measure_Theory%29",
      text="Let Σ be a sigma-algebra on a set X. A (nonnegative) measure is a function μ:Σ→[0,+∞] such that μ(∅)=0 and μ(⋃_{n=1}^∞ E_n)=∑_{n=1}^∞ μ(E_n) whenever (E_n) is a sequence of pairwise disjoint sets in Σ.",
      note="Direct ProofWiki Definition 2. Values may be +infinity; zero on the empty set and countable additivity for pairwise disjoint measurable sets are explicit. Do not infer probability normalization μ(X)=1 or finite total mass.",
      corroboration=["https://proofwiki.org/wiki/Definition%3ACountably_Additive_Function"])
]

def run(root):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
      ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Only unsealed independent Wave 2 research can be modified")
 completed=w.root/"state/wave2_link_review_batch_25.json"
 if not completed.exists() or json.loads(completed.read_text()).get("total_screened_links")!=634:
  raise PipelineError("Requires verified 634-link polynomial and Riemann screen")
 before={"sources":9,"terms":371,"observations":794,"meanings":474,"relations":634}
 after={"sources":9,"terms":373,"observations":796,"meanings":474,"relations":634}
 actual={s:len(w.records(s)) for s in before}
 if actual not in (before,after):
  raise PipelineError("Unexpected current Wave 2 source counts "+str(actual))
 source=w.records("sources").get("src.proofwiki")
 if not source or source["access"]!="free" or source["rights"] not in ("permitted","locator_only"):
  raise PipelineError("Research source rights do not authorize short independent paraphrase")
 terms=[];observations=[];leads=[]
 for x in CASES:
  tid="term.wave2.foundation26."+x["key"]; oid="obs.wave2.foundation26."+x["key"]
  terms.append({"id":tid,"label":x["label"],"source_id":"src.proofwiki",
     "locator":x["url"],"discovery_provenance":"independent_direct_ProofWiki_definition_read_2026_10_19",
     "human_verified":False})
  observations.append({"id":oid,"term_id":tid,"source_id":"src.proofwiki",
     "locator":x["url"],"record_kind":"paraphrase","text":x["text"],
     "context":x["note"],"editorial_note":x["note"],
     "source_crosscheck_urls":x["corroboration"],
     "reviewed_by":"assistant_independent_sigma_algebra_measure_source_review_2026_10_19",
     "human_verified":False})
  leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":x["url"],
     "candidate_observation_id":oid,"source_access_outcome":"direct_page_read",
     "editorial_reason":x["note"],"source_research_complete":True,
     "meaning_screened":False,"human_verified":False})
 def store(path,records):
  path.parent.mkdir(parents=True,exist_ok=True)
  content="".join(canonical(r)+"\n" for r in records)
  if path.exists() and path.read_text(encoding="utf-8")!=content:
   raise PipelineError("Previously reviewed source intake unexpectedly differs")
  path.write_text(content,encoding="utf-8")
  return path
 tr=w.ingest("terms",store(w.root/"intake/foundations_batch_26_terms.jsonl",terms),batch_size=2)
 ob=w.ingest("observations",store(w.root/"intake/foundations_batch_26_observations.jsonl",observations),batch_size=2)
 store(w.root/"wave2/foundation_source_discovery_batch_26.jsonl",leads)
 current={s:len(w.records(s)) for s in after}
 if current!=after:
  raise PipelineError("Source count mismatch "+str(current))
 report={"phase":"source_only_sigma_algebra_and_nonnegative_measure_foundations",
   "counts":current,"new_direct_source_pages_read":2,
   "source_meanings_screened":0,"new_relationships_screened":0,
   "infinite_measure_values_explicit":True,
   "countable_additivity_and_empty_set_axiom_preserved":True,
   "sigma_algebra_not_conflated_with_topology":True,
   "riemann_and_lebesgue_stieltjes_integral_not_conflated":True,
   "idempotent_term_skips":tr["already_present"],
   "idempotent_observation_skips":ob["already_present"],
   "all_stages_unsealed":True,"human_peer_verified":False,
   "original_production_mathdef_consulted":False,
   "next":"Archive 371-term review coverage then individually source-screen measure and sigma-algebra definitions before linking raw moments."}
 atomic_json(w.root/"state/wave2_foundations_batch_26.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",required=True,type=Path)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
