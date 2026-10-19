"""Independent Wave 2 source acquisition batch 05: four missing foundations.

Each paraphrase was authored from direct public Stacks Project definition
pages; source identity, scope and individual access evidence are preserved.
This step does NOT screen or invent any mathematical meanings or relations.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

SOURCES=[
  dict(key="field-commutative-unital",label="field (nonzero commutative unital ring)",tag="09FD",
       context="Stacks 9.2.1, commutative-unital ring convention",
       observation="A field is a nonzero commutative ring k with a multiplicative identity in which each element other than zero is a unit. Equivalently the nonzero elements form an abelian group under multiplication.",
       note="Direct Stacks Definition 9.2.1 and Stacks Section 10.2 ring convention. Exclude zero ring; invertibility requires two-sided product equal to 1.",
       crosscheck=["https://stacks.math.columbia.edu/tag/00AQ"]),
  dict(key="category-functor",label="covariant functor between categories",tag="001B",
       context="Stacks 4.2.8, ordinary strict functor of small categories",
       observation="For categories A and B, a covariant functor F:A→B assigns each object x an object F(x) and every arrow f:x→y an arrow F(f):F(x)→F(y). It preserves identities and composition: F(id_x)=id_{F(x)} and F(g∘f)=F(g)∘F(f).",
       note="Direct Stacks Definition 4.2.8. Contravariant functors reverse arrows and are separately sourced elsewhere; do not confuse functors and pseudofunctors.",
       crosscheck=["https://stacks.math.columbia.edu/tag/0013"]),
  dict(key="small-groupoid",label="groupoid (every arrow invertible)",tag="0018",
       context="Stacks 4.2.5, ordinary groupoid as small category",
       observation="A groupoid is a category in which every arrow has a two-sided inverse under composition, hence every morphism is an isomorphism. It need not have only one object, or only one arrow between objects.",
       note="Direct Stacks Definition 4.2.5, following Definitions 4.2.1 and 4.2.4. Not the same as a single-object groupoid or an abelian group.",
       crosscheck=["https://stacks.math.columbia.edu/tag/0013"]),
  dict(key="pseudo-functor-strict-2category",label="pseudofunctor into a strict 2-category",tag="003N",
       context="Stacks 4.29.5: ordinary source category and strict target 2-category; invertible coherence 2-cells",
       observation="A pseudofunctor P:A→C into a 2-category assigns objects and 1-morphisms as a functor would, but has invertible unit and composition comparison 2-morphisms instead of strict equality. The comparisons satisfy the identity compatibility laws and the associativity coherence equation for triples of composable arrows.",
       note="Direct Stacks Definition 4.29.5. Pseudofunctor is NOT the same as a strict functor; record invertible unit, composition and coherence data. Base A is an ordinary category, target C is a strict 2-category under Stacks conventions.",
       crosscheck=["https://stacks.math.columbia.edu/tag/003G"])
]
def run(root):
 w=Workspace(root)
 baseline=w.root/"state/baseline.json"
 if not baseline.exists() or json.loads(baseline.read_text())["mode"]!="second_wave":
  raise PipelineError("Only independent Wave 2 fork is writable")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Cannot ingest into sealed Wave 2")
 current={stage:len(w.records(stage)) for stage in ("sources","terms","observations","meanings","relations")}
 if current not in (
  {"sources":9,"terms":339,"observations":762,"meanings":431,"relations":545},
  {"sources":9,"terms":343,"observations":766,"meanings":431,"relations":545}):
  raise PipelineError("Source intake expected post-presheaf-correction 431/545 state, found "+str(current))
 if w.records("sources")["src.stacks"]["access"]!="free":
  raise PipelineError("Stacks source unavailable or disapproved")
 if w.records("sources")["src.stacks"]["rights"] not in ("permitted","locator_only"):
  raise PipelineError("Stacks source rights unapproved")
 terms=[];observations=[];leads=[]
 for item in SOURCES:
  locator="https://stacks.math.columbia.edu/tag/"+item["tag"]
  term_id="term.wave2.stacks."+item["key"]
  obs_id="obs.wave2.stacks."+item["key"]
  terms.append({"id":term_id,"label":item["label"],"source_id":"src.stacks",
   "locator":locator,"discovery_provenance":"individual_independent_stacks_definition_read_2026_10_19","human_verified":False})
  observations.append({"id":obs_id,"term_id":term_id,"source_id":"src.stacks",
   "locator":locator,"record_kind":"paraphrase","text":item["observation"],
   "context":item["context"],"editorial_note":item["note"],
   "source_crosscheck_urls":item["crosscheck"],
   "reviewed_by":"assistant_independent_stacks_mathematical_source_review_2026_10_19",
   "human_verified":False})
  leads.append({"term_id":term_id,"source_id":"src.stacks","locator":locator,
   "source_access_outcome":"direct_page_read","candidate_observation_id":obs_id,
   "editorial_reason":item["note"],"human_verified":False,
   "source_research_complete":True,"meaning_screened":False})
 def store(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  data=chr(10).join(canonical(row) for row in rows)+chr(10)
  if path.exists() and path.read_text(encoding="utf-8")!=data:
   raise PipelineError("Prior independently reviewed batch conflicts: "+str(path))
  path.write_text(data,encoding="utf-8")
  return path
 t=w.ingest("terms",store(w.root/"intake/foundations_batch_05_terms.jsonl",terms),batch_size=4)
 o=w.ingest("observations",store(w.root/"intake/foundations_batch_05_observations.jsonl",observations),batch_size=4)
 store(w.root/"wave2/foundation_source_discovery_batch_05.jsonl",leads)
 counts={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
 if counts!={"sources":9,"terms":343,"observations":766,"meanings":431,"relations":545}:
  raise PipelineError("Source batch counts differ: "+str(counts))
 report={"state":"four_direct_stacks_foundational_sources_read_as_unscreened_candidates",
  "term_count":343,"observation_count":766,"source_read_candidates_added":4,
  "source_conventions":[r["context"] for r in SOURCES],
  "idempotent_term_skips":t["already_present"],"idempotent_observation_skips":o["already_present"],
  "new_meanings_screened":0,"new_links_added":0,"sealed_stages":0,
  "human_peer_verified":False,"production_definitions_consulted":False,
  "next":"Expand per-term coverage to 343, then individually review four source-bound foundational meaning candidates and dependencies."}
 atomic_json(w.root/"state/wave2_foundations_batch_05.json",report)
 return report

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--workspace",type=Path,required=True)
 a=ap.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
