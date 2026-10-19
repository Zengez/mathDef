"""Wave 2 independent Stacks intake of preadditive/additive/abelian category axioms.

Source-only observations. Do not automatically screen meanings/links or
assert additivity implies the abelian coimage-image isomorphism condition.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

CASES=[
("preadditive-category","preadditive category","00ZY",
 "A preadditive category C is a category whose hom-set Hom_C(x,y) is an abelian group for every pair of objects, and whose composition is bilinear in its morphism arguments.",
 "Stacks Definition 12.3.1; no zero object, finite biproduct or all-kernel existence is automatically imposed."),
("additive-category","additive category","0104",
 "An additive category is a preadditive category with finite products, including an empty product; equivalently it has a zero object and finite direct sums.",
 "Stacks Definition 12.3.8; existence of finite products is additional to bilinear hom-set composition, and does not force kernels or cokernels of all arrows."),
("abelian-category","abelian category","0109",
 "An abelian category is an additive category with a kernel and cokernel for every morphism f, such that the canonical comparison morphism Coim(f)→Im(f) is an isomorphism for every f.",
 "Stacks Definition 12.5.1; the canonical coimage-to-image isomorphism condition is essential and not a consequence of mere preadditivity or universal kernel/cokernel existence.")
]
def run(root):
 w=Workspace(root)
 if json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8")).get("mode")!="second_wave":
  raise PipelineError("Independent editable Wave 2 fork required")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("No mutation to sealed stage")
 checkpoint=w.root/"state/wave2_foundations_batch_14_screened.json"
 if not checkpoint.exists() or json.loads(checkpoint.read_text()).get("previous_review_rows_preserved")!=467:
  raise PipelineError("Prior source-reviewed homological meanings must be individually screened first")
 counts={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
 if counts not in (
  {"sources":9,"terms":360,"observations":783,"meanings":459,"relations":606},
  {"sources":9,"terms":363,"observations":786,"meanings":459,"relations":606}
 ):
  raise PipelineError("Unexpected new source baseline "+str(counts))
 src=w.records("sources")["src.stacks"]
 if src["access"]!="free" or src["rights"] not in ("permitted","locator_only"):
  raise PipelineError("Stacks source access not independently authorized")
 terms=[];obs=[];leads=[]
 for slug,label,tag,text,scope in CASES:
  url="https://stacks.math.columbia.edu/tag/"+tag
  tid="term.wave2.foundation15."+slug
  oid="obs.wave2.foundation15."+slug
  terms.append({"id":tid,"label":label,"source_id":"src.stacks","locator":url,
    "discovery_provenance":"direct_Stacks_definition_review_2026_10_19","human_verified":False})
  obs.append({"id":oid,"term_id":tid,"source_id":"src.stacks",
    "locator":url,"record_kind":"paraphrase","text":text,"context":scope,
    "editorial_note":scope,"reviewed_by":"assistant_independent_category_axioms_source_review_2026_10_19",
    "human_verified":False})
  leads.append({"term_id":tid,"source_id":"src.stacks","locator":url,
    "source_access_outcome":"direct_page_read","candidate_observation_id":oid,
    "editorial_reason":scope,"source_research_complete":True,
    "meaning_screened":False,"human_verified":False})
 def write(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  txt=chr(10).join(canonical(r) for r in rows)+chr(10)
  if path.exists() and path.read_text(encoding="utf-8")!=txt:
   raise PipelineError("Source evidence differs from previously committed independent review")
  path.write_text(txt,encoding="utf-8")
  return path
 tr=w.ingest("terms",write(w.root/"intake/foundations_batch_15_terms.jsonl",terms),batch_size=3)
 ob=w.ingest("observations",write(w.root/"intake/foundations_batch_15_observations.jsonl",obs),batch_size=3)
 write(w.root/"wave2/foundation_source_discovery_batch_15.jsonl",leads)
 after={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
 if after!={"sources":9,"terms":363,"observations":786,"meanings":459,"relations":606}:
  raise PipelineError("Source record counts wrong "+str(after))
 result={"phase":"three_distinct_category_hierarchy_definitions_independently_sourced",
   "new_term_records":3,"new_observation_records":3,"counts":after,
   "preadditive_does_not_imply_additive":True,
   "additive_does_not_imply_abelian":True,
   "coimage_image_isomorphism_not_omitted":True,
   "screened_meanings_added":0,"screened_relations_added":0,
   "idempotent_term_skips":tr["already_present"],"idempotent_observation_skips":ob["already_present"],
   "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_consulted":False}
 atomic_json(w.root/"state/wave2_foundations_batch_15.json",result)
 return result
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--workspace",required=True,type=Path)
 a=ap.parse_args();print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
