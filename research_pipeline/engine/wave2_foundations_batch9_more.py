"""Direct-source intake: reduced rings, ring maps, well-orders, subspace topology.

This adds four independently investigated source observations only. The primary
ring-map source does not require preserving unity, and the alternative unital
convention must later be a separate screened formulation. The well-order
source's displayed formula has a missing nonempty-set qualifier; use the
correct prose definition. No production corpus is consulted.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

SOURCES=[
 ("reduced-ring","reduced ring","https://proofwiki.org/wiki/Definition%3AReduced_Ring",
  "An associative ring R is reduced if every nilpotent element is zero: if r∈R and r^n=0 for some positive integer n, then r=0.",
  "General associative-ring convention; ring identity optional. Reduced does not imply integral domain.",
  ["general associative ring","commutative unital specialization"]),
 ("ring-homomorphism","ring homomorphism","https://proofwiki.org/wiki/Definition%3ARing_Homomorphism",
  "A ring homomorphism φ:R→S preserves both operations: φ(a+b)=φ(a)+φ(b), and φ(ab)=φ(a)φ(b) for every a,b∈R. A unital ring homomorphism additionally satisfies φ(1_R)=1_S.",
  "The page explicitly separates its primary identity-optional convention from identity-preserving ring homomorphisms. Record them as distinct contexts.",
  ["general ring homomorphism not necessarily unital","unital ring homomorphism"]),
 ("well-ordered-set","well-ordered set","https://proofwiki.org/wiki/Definition%3AWell-Ordered_Set",
  "A well-ordered set is a pair (S,≤) where ≤ is a total order on S and every nonempty subset A⊆S has a least element under ≤.",
  "The source's prose requires nonempty subsets but its displayed universal quantification omits this essential condition. Do not copy that formula literally.",
  ["well-order as total order with least elements of all nonempty subsets"]),
 ("topological-subspace","subspace topology","https://proofwiki.org/wiki/Definition%3ASubspace_Topology",
  "For a topological space (X,τ) and A⊆X, its subspace topology is τ_A={A∩U:U∈τ}; the induced topological space is (A,τ_A).",
  "The source redirect describes possibly empty subspaces as well as a convention requiring nonempty A. Preserve the empty-space difference explicitly.",
  ["general subspace including empty set","nonempty-subspace convention"])
]

def run(root):
 w=Workspace(root)
 b=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if b.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
     ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Requires editable independent Wave 2 workspace")
 gate=w.root/"state/wave2_foundation_dependency_no_target_batch_02.json"
 if not gate.exists() or json.loads(gate.read_text()).get("formulation_reviews_without_initial_decision")!=0:
  raise PipelineError("Complete and verify the four prior set-foundation dependency reviews first")
 counts={k:len(w.records(k)) for k in ("sources","terms","observations","meanings","relations")}
 permitted=[
  {"sources":9,"terms":350,"observations":773,"meanings":447,"relations":582},
  {"sources":9,"terms":354,"observations":777,"meanings":447,"relations":582}
 ]
 if counts not in permitted:
  raise PipelineError("Unexpected independent source baseline "+str(counts))
 s=w.records("sources").get("src.proofwiki")
 if s is None or s["access"]!="free" or s["rights"] not in ("permitted","locator_only"):
  raise PipelineError("Source access rights or license restriction")
 terms=[];observations=[];leads=[]
 for slug,label,url,words,note,variants in SOURCES:
  tid="term.wave2.proofwiki.foundation09."+slug
  oid="obs.wave2.proofwiki.foundation09."+slug
  terms.append({"id":tid,"label":label,"locator":url,"source_id":"src.proofwiki",
   "discovery_provenance":"individual_public_definition_direct_read_2026_10_19",
   "human_verified":False})
  observations.append({"id":oid,"term_id":tid,"source_id":"src.proofwiki",
   "locator":url,"record_kind":"paraphrase","text":words,
   "context":note,"potential_contextual_variants":variants,
   "editorial_note":note,
   "reviewed_by":"assistant_independent_source_convention_review_2026_10_19",
   "human_verified":False})
  leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":url,
   "source_access_outcome":"direct_page_read","candidate_observation_id":oid,
   "editorial_reason":note,"source_research_complete":True,
   "meaning_screened":False,"human_verified":False})
 def write(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  content=chr(10).join(canonical(z) for z in rows)+chr(10)
  if path.exists() and path.read_text(encoding="utf-8")!=content:
   raise PipelineError("Attempt to overwrite existing individual evidence "+str(path))
  path.write_text(content,encoding="utf-8")
  return path
 a=w.ingest("terms",write(w.root/"intake/foundations_batch_09_terms.jsonl",terms),batch_size=4)
 b=w.ingest("observations",write(w.root/"intake/foundations_batch_09_observations.jsonl",observations),batch_size=4)
 write(w.root/"wave2/foundation_source_discovery_batch_09.jsonl",leads)
 after={k:len(w.records(k)) for k in ("sources","terms","observations","meanings","relations")}
 expected={"sources":9,"terms":354,"observations":777,"meanings":447,"relations":582}
 if after!=expected:
  raise PipelineError("Source observations missing "+str(after))
 result={"phase":"four_direct_foundation_sources_intaken_as_unreviewed_meaning_candidates",
  "counts":after,"source_articles_directly_examined":4,
  "new_source_term_records":4,"new_source_observations":4,
  "candidate_contexts":["reduced ring identity optional","nonunital ring homomorphism",
    "identity-preserving ring homomorphism","well-order nonempty subset least element",
    "empty-allowed subspace topology","nonempty-subspace restricted convention"],
  "no_new_meanings_screened":True,"no_new_links_screened":True,
  "idempotent_term_skips":a["already_present"],
  "idempotent_observation_skips":b["already_present"],
  "stages_unsealed":True,"human_peer_verified":False,
  "original_production_mathdef_consulted":False,
  "next":"Reconcile 354-term source coverage before candidate mathematical screening and dependency graph changes"}
 atomic_json(w.root/"state/wave2_foundations_batch_09.json",result)
 return result

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 x=p.parse_args()
 print(json.dumps(run(x.workspace),indent=2))
if __name__=="__main__":
 main()
