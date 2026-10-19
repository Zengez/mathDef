"""Source-only batch 13: group kernels and categorical kernel, cokernel, exactness.

Stays within verified ProofWiki/Stacks source permissions. Does not identify
concrete subgroup kernels with abstract universal arrows, does not assert
categorical cokernels exist in all preadditive categories.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

CASES=[
("abelian-group-homomorphism-kernel","kernel of an abelian group homomorphism","src.proofwiki",
 "https://proofwiki.org/wiki/Definition%3AKernel_of_Group_Homomorphism",
 "For an abelian-group homomorphism f:A→B, ker(f)={a∈A:f(a)=0_B}, an additive subgroup of A.",
 "ProofWiki source is the general group-homomorphism kernel; specialize to abelian groups and their additive identities without identifying the subset as literally an abstract categorical universal arrow."),
("preadditive-category-kernel","kernel universal property in a preadditive category","src.stacks",
 "https://stacks.math.columbia.edu/tag/0106",
 "Given f:x→y in a preadditive category, a kernel is a morphism i:k→x satisfying f∘i=0 such that every j:z→x with f∘j=0 factors uniquely as j=i∘h.",
 "Stacks Definition 12.3.9 item 1. Kernel is a universal arrow unique up to unique isomorphism; it need not exist for all morphisms of a preadditive category."),
("preadditive-category-cokernel","cokernel universal property in a preadditive category","src.stacks",
 "https://stacks.math.columbia.edu/tag/0106",
 "For f:x→y in a preadditive category, a cokernel is a morphism p:y→c with p∘f=0 such that every q:y→z with q∘f=0 factors uniquely as q=h∘p.",
 "Stacks Definition 12.3.9 item 3. The universal arrow exists only for morphisms admitting cokernels, and in the category of abelian groups represents quotient by the image."),
("exact-sequence-abelian-category","exact sequence in an abelian category","src.stacks",
 "https://stacks.math.columbia.edu/tag/00ZX",
 "A sequence of morphisms in an abelian category is exact at its interior object Y of X→Y→Z when the image of X→Y equals the kernel of Y→Z; successive compositions are zero. A short exact sequence has the form 0→A→B→C→0.",
 "Stacks Definition 12.5.7. An additive category alone is not enough for the given image-equals-kernel formulation; abelian-group sequences form a special case.")
]
def run(root):
 w=Workspace(root)
 if json.loads((w.root/"state/baseline.json").read_text()).get("mode")!="second_wave":
  raise PipelineError("Independent fork required")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("No sealed stage editing")
 before={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
 if before not in ({"sources":9,"terms":356,"observations":779,"meanings":455,"relations":606},
                   {"sources":9,"terms":360,"observations":783,"meanings":455,"relations":606}):
  raise PipelineError("Expected exactly 606 source-screened links and 455 meanings "+str(before))
 link=w.root/"state/wave2_link_review_batch_12.json"
 if not link.exists() or json.loads(link.read_text())["total_screened_links"]!=606:
  raise PipelineError("Requires independently screened site-link batch")
 sources=w.records("sources")
 terms=[];obs=[];leads=[]
 for key,name,src,url,content,scope in CASES:
  if sources[src]["access"]!="free" or sources[src]["rights"] not in ("permitted","locator_only"):
   raise PipelineError("Source rights not permitted "+src)
  tid="term.wave2.foundation13."+key
  oid="obs.wave2.foundation13."+key
  terms.append({"id":tid,"label":name,"source_id":src,"locator":url,
    "discovery_provenance":"exact_independent_direct_source_review_2026_10_19","human_verified":False})
  obs.append({"id":oid,"term_id":tid,"source_id":src,"locator":url,
    "record_kind":"paraphrase","text":content,"context":scope,
    "editorial_note":scope,"human_verified":False,
    "reviewed_by":"assistant_independent_homological_algebra_source_review_2026_10_19"})
  leads.append({"term_id":tid,"source_id":src,"locator":url,
    "source_access_outcome":"direct_page_read","candidate_observation_id":oid,
    "editorial_reason":scope,"source_research_complete":True,
    "meaning_screened":False,"human_verified":False})
 def save(p,rows):
  p.parent.mkdir(parents=True,exist_ok=True)
  data=chr(10).join(canonical(x) for x in rows)+chr(10)
  if p.exists() and p.read_text(encoding="utf-8")!=data:
   raise PipelineError("Source evidence already exists but differs: "+str(p))
  p.write_text(data,encoding="utf-8")
  return p
 t=w.ingest("terms",save(w.root/"intake/foundations_batch_13_terms.jsonl",terms),batch_size=4)
 o=w.ingest("observations",save(w.root/"intake/foundations_batch_13_observations.jsonl",obs),batch_size=4)
 save(w.root/"wave2/foundation_source_discovery_batch_13.jsonl",leads)
 after={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
 if after!={"sources":9,"terms":360,"observations":783,"meanings":455,"relations":606}:
  raise PipelineError("Incorrect source-ledger size "+str(after))
 report={"phase":"four_homological_algebra_sources_individually_observed_not_screened",
  "counts":after,"new_source_terms":4,"new_observations":4,
  "concrete_vs_categorical_kernel_contexts_distinct":True,
  "cokernels_not_automatically_assumed_to_exist":True,
  "abelian_vs_preadditive_exactness_contexts_distinct":True,
  "screened_meanings_added":0,"screened_links_added":0,
  "term_idempotent_skips":t["already_present"],"observation_idempotent_skips":o["already_present"],
  "all_stages_unsealed":True,"human_peer_verified":False,
  "production_corpus_consulted":False}
 atomic_json(w.root/"state/wave2_foundations_batch_13.json",report)
 return report
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--workspace",type=Path,required=True)
 a=ap.parse_args();print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
