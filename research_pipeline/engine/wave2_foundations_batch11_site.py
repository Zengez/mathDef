"""Source-only intake for exact Stacks site and indexed-morphism-family definitions."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

ITEMS=[
 ("fixed-target-morphism-family","family of morphisms with fixed target",
  "https://stacks.math.columbia.edu/tag/0396",
  "Let C be a category. A family of morphisms with a fixed target comprises an object U of C, a set I and morphisms f_i:U_i→U for each i∈I; the index set I may be empty.",
  "Stacks Definition 7.6.1; index labels and multiplicity are retained as family data, unlike the support set of arrows."),
 ("grothendieck-site-pretopology","site with designated covering families",
  "https://stacks.math.columbia.edu/tag/00VH",
  "A site in the Stacks family-based convention is a category C with a set Cov(C) of families of morphisms with common target. Cov(C) contains singleton families of isomorphisms and is closed under compositional refinement and base change of coverings along morphisms, with the needed fiber products existing.",
  "Stacks Definition 7.6.2. The family-of-arrows coverage data and set-sized condition must not be identified literally with a topology of covering sieves.")
]

def run(root):
 w=Workspace(root)
 if json.loads((w.root/"state/baseline.json").read_text()).get("mode")!="second_wave":
  raise PipelineError("Only editable independent Wave 2 research supported")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Cannot change sealed source stages")
 previous=w.root/"state/wave2_link_review_batch_10.json"
 if not previous.exists() or json.loads(previous.read_text()).get("total_screened_links")!=600:
  raise PipelineError("Requires source-screened 600-link checkpoint")
 counts={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
 if counts not in ({"sources":9,"terms":354,"observations":777,"meanings":453,"relations":600},
                   {"sources":9,"terms":356,"observations":779,"meanings":453,"relations":600}):
  raise PipelineError("Unexpected research baseline "+str(counts))
 source=w.records("sources").get("src.stacks")
 if not source or source["access"]!="free" or source["rights"] not in ("permitted","locator_only"):
  raise PipelineError("Stacks source access or rights unsupported")
 terms=[];observations=[];leads=[]
 for slug,label,url,text,reason in ITEMS:
  tid="term.wave2.stacks.foundation11."+slug
  oid="obs.wave2.stacks.foundation11."+slug
  terms.append({"id":tid,"label":label,"locator":url,"source_id":"src.stacks",
                "discovery_provenance":"independent_direct_stacks_7_6_definition_read_2026_10_19",
                "human_verified":False})
  observations.append({"id":oid,"term_id":tid,"source_id":"src.stacks","locator":url,
       "record_kind":"paraphrase","text":text,"context":reason,
       "editorial_note":reason,"reviewed_by":"assistant_independent_stacks_site_mathematical_review_2026_10_19",
       "human_verified":False})
  leads.append({"term_id":tid,"source_id":"src.stacks","locator":url,
       "source_access_outcome":"direct_page_read","candidate_observation_id":oid,
       "editorial_reason":reason,"source_research_complete":True,"meaning_screened":False,
       "human_verified":False})
 def store(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  txt=chr(10).join(canonical(x) for x in rows)+chr(10)
  if path.exists() and path.read_text(encoding="utf-8")!=txt:
   raise PipelineError("Individual source evidence differs from prior research")
  path.write_text(txt,encoding="utf-8")
  return path
 a=w.ingest("terms",store(w.root/"intake/foundations_batch_11_terms.jsonl",terms),batch_size=2)
 b=w.ingest("observations",store(w.root/"intake/foundations_batch_11_observations.jsonl",observations),batch_size=2)
 store(w.root/"wave2/foundation_source_discovery_batch_11.jsonl",leads)
 after={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
 if after!={"sources":9,"terms":356,"observations":779,"meanings":453,"relations":600}:
  raise PipelineError("Unexpected site source records "+str(after))
 report={"phase":"two_exact_Stacks_site_and_family_source_observations",
 "counts":after,"new_term_records":2,"new_observations":2,
 "source_specific_scope":"set-indexed family may be empty; site is family-based coverage satisfying three axioms",
 "screened_meanings_added":0,"screened_links_added":0,
 "term_idempotent_skips":a["already_present"],"observation_idempotent_skips":b["already_present"],
 "human_peer_verified":False,"original_production_mathdef_consulted":False,
 "stages_unsealed":True,"next":"Review two independent mathematical meaning candidates before making site/family dependency relationships"}
 atomic_json(w.root/"state/wave2_foundations_batch_11.json",report)
 return report

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--workspace",type=Path,required=True)
 a=ap.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
