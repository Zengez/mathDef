"""Ingest only directly researched ordered-real source observations in Wave 2.

The circular opening of ProofWiki's real-number article is expressly excluded.
Different meanings (complete ordered field, totally ordered field, supremum
property and modulus) remain candidate evidence, never auto-screened meanings.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

PAGES=[
 ("axiomatic-complete-ordered-reals","complete ordered field as a real-number system","https://proofwiki.org/wiki/Definition%3AReal_Number",
  "A real-number system is a totally ordered field R in which every nonempty subset of R that is bounded above has a supremum in R. Different complete ordered-field realizations are equivalent up to an order-preserving field isomorphism.",
  "ProofWiki Axiomatic Definition only. Its initial 'rationals plus irrationals' characterization is explicitly circular and excluded from this definition. Cauchy-class and Dedekind-cut constructions need separate source review."),
 ("totally-ordered-field","totally ordered field compatible with arithmetic","https://proofwiki.org/wiki/Definition%3AOrdered_Field",
  "A totally ordered field F is a field with a total order ≤ for which x<y implies x+z<y+z for every z, and x<y with z>0 implies xz<yz. Such a field is not necessarily Dedekind complete.",
  "ProofWiki Totally Ordered Field subsection; the article distinguishes a more general partially ordered field whose conventions vary."),
 ("dedekind-supremum-property","Dedekind completeness of ordered sets","https://proofwiki.org/wiki/Definition%3ADedekind_Complete",
  "An ordered set S has the Dedekind completeness property if every nonempty subset A⊆S bounded above in S has a least upper bound in S.",
  "Source specifies the order-theoretic supremum property, not arbitrary metric completeness. The empty subset is expressly excluded; upper bound is taken in S."),
 ("real-absolute-value-variants","real-number absolute value by sign and square root","https://proofwiki.org/wiki/Definition%3AAbsolute_Value_of_Real_Number",
  "For a real number x the absolute value |x| equals x if x≥0 and −x if x<0; equivalently, |x|=√(x²) where √ denotes the nonnegative real square root.",
  "The piecewise and square-root formulations are equivalent over the reals, but the latter invokes an independently defined nonnegative square-root function. This evidence must not silently overwrite the previously screened real-absolute-value meaning.")
]

def run(root):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
   ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Only unsealed independent Wave 2 may be edited")
 state={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
 if state not in (
  {"sources":9,"terms":384,"observations":807,"meanings":487,"relations":659},
  {"sources":9,"terms":388,"observations":811,"meanings":487,"relations":659}
 ):
  raise PipelineError("Unexpected source/meaning/relation state "+str(state))
 src=w.records("sources").get("src.proofwiki")
 if not src or src["access"]!="free" or src["rights"] not in ("permitted","locator_only"):
  raise PipelineError("Source rights/access not approved")
 terms=[];observations=[];leads=[]
 for slug,label,url,text,note in PAGES:
  tid="term.wave2.real45."+slug
  oid="obs.wave2.real45."+slug
  terms.append({"id":tid,"label":label,"source_id":"src.proofwiki","locator":url,
    "discovery_provenance":"direct_independent_proofwiki_exact_definition_section_review_2026_10_20",
    "human_verified":False})
  observations.append({"id":oid,"term_id":tid,"source_id":"src.proofwiki","locator":url,
    "record_kind":"paraphrase","text":text,"context":"Real analysis and field/order foundations",
    "editorial_note":note,"reviewed_by":"assistant_independent_complete_ordered_field_review_2026_10_20",
    "human_verified":False})
  leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":url,
    "source_access_outcome":"direct_page_read","candidate_observation_id":oid,
    "source_research_complete":True,"meaning_screened":False,
    "editorial_reason":note,"human_verified":False})
 def store(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  body="".join(canonical(x)+"\n" for x in rows)
  if path.exists() and path.read_text(encoding="utf-8")!=body:
   raise PipelineError("Conflicting preexisting independent source evidence")
  path.write_text(body,encoding="utf-8")
  return path
 t=w.ingest("terms",store(w.root/"intake/foundations_batch_45_terms.jsonl",terms),batch_size=4)
 o=w.ingest("observations",store(w.root/"intake/foundations_batch_45_observations.jsonl",observations),batch_size=4)
 store(w.root/"wave2/foundation_source_discovery_batch_45.jsonl",leads)
 after={s:len(w.records(s)) for s in state}
 if after!={"sources":9,"terms":388,"observations":811,"meanings":487,"relations":659}:
  raise PipelineError("Source evidence cardinality inconsistent "+str(after))
 result={"phase":"real_ordered_field_and_modulus_candidate_source_acquisition",
  "direct_source_articles_read":4,"terms_after":388,"observations_after":811,
  "meanings_preserved":487,"links_preserved":659,
  "real_definition_circular_original_lead_rejected":True,
  "complete_ordered_field_requires_supremum_axiom":True,
  "ordered_field_distinct_from_complete_ordered_field":True,
  "modulus_sqrt_variant_requires_nonnegative_sqrt":True,
  "new_meanings_screened":0,"new_links_screened":0,
  "term_idempotent_skips":t["already_present"],
  "observation_idempotent_skips":o["already_present"],
  "human_peer_verified":False,"production_mathdef_corpus_consulted":False,
  "all_stages_unsealed":True,
  "next":"Refresh 388-term individual source-review ledger and screen order-related mathematical meanings without imposing unproved equivalences."}
 atomic_json(w.root/"state/wave2_real_source_batch_45.json",result)
 return result

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
