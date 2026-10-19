"""Independent Wave 2 source intake: ordered pairs, subsets, and mapping variants.

Only source-scoped authored paraphrases are added. A relation graph by itself
does not uniquely encode the mapping codomain; alternate ordered-pair set
encodings are not literally identical. No definition variants or links are
auto-approved. Run after 11 elementary links and six meanings are screened.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

ARTICLES=[
 dict(slug="ordered-pair",label="ordered pair with set-theoretic formalization",
  url="https://proofwiki.org/wiki/Definition%3AOrdered_Pair",
  context="Set theory: ordered pairs and Kuratowski encoding, not an unordered doubleton",
  text="An ordered pair (a,b) records a first coordinate a and a second coordinate b. One rigorous set-theoretic implementation is the Kuratowski pair (a,b):={{a},{a,b}}, whose equality agrees with coordinatewise equality.",
  note="Direct ProofWiki formalization and alternative Wiener/empty-set encodings read. Alternative encodings have equivalent coordinate behavior, but are not equal as sets and need separately labeled representations.",
  candidate_variants=["ordered coordinates with equality iff corresponding coordinates equal",
   "Kuratowski representation {{a},{a,b}}","other set encodings with same coordinate uniqueness"]),
 dict(slug="subset",label="subset and proper-subset distinction",
  url="https://proofwiki.org/wiki/Definition%3ASubset",
  context="Set theory: non-strict subset relation for arbitrary sets",
  text="For sets A and B, A is a subset of B, written A⊆B, precisely when every x∈A is also an element of B. Proper inclusion A⊊B additionally requires A≠B.",
  note="ProofWiki uses ⊆ for non-strict inclusion and distinguishes proper subset. Do not imply the class of all sets is itself a set or confuse ⊂ notation conventions.",
  candidate_variants=["non-strict subset","proper subset with strict inequality"]),
 dict(slug="mapping",label="mapping as total single-valued assignment and typed graph",
  url="https://proofwiki.org/wiki/Definition%3AMapping",
  context="Set theory: total single-valued map X→Y, typed graph, bare graph with ambient carriers",
  text="For sets X,Y, a mapping f:X→Y assigns each x∈X exactly one y∈Y. Equivalently, with X and Y specified, its graph G⊆X×Y satisfies: for every x∈X exactly one y∈Y has (x,y)∈G.",
  note="ProofWiki Definition 1 uses total single-valued assignment; Definitions 2–3 use a typed relation (X,Y,G) and equivalent total and uniqueness axioms. The bare graph G does not by itself determine the codomain Y. Distinguish typed mapping data from bare graph equality.",
  candidate_variants=["total single-valued assignment (educationally earlier)",
    "typed graph with totality and single-valuedness","bare graph subset under fixed ambient sets"])
]

def run(root):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
      ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Only unsealed independent Wave 2 source records can be extended")
 report=w.root/"state/wave2_link_review_batch_07.json"
 if not report.exists() or json.loads(report.read_text(encoding="utf-8")).get("total_screened_links")!=574:
  raise PipelineError("Exact prior 11-link screen must be verified and committed first")
 counts={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
 if counts not in (
  {"sources":9,"terms":347,"observations":770,"meanings":441,"relations":574},
  {"sources":9,"terms":350,"observations":773,"meanings":441,"relations":574}):
  raise PipelineError("Previous source/meaning state changed unexpectedly: "+str(counts))
 src=w.records("sources").get("src.proofwiki")
 if src is None or src["access"]!="free" or src["rights"] not in ("permitted","locator_only"):
  raise PipelineError("ProofWiki source access/rights not independently approved")
 terms=[];observations=[];leads=[]
 for a in ARTICLES:
  term_id="term.wave2.proofwiki.foundation08."+a["slug"]
  evidence_id="obs.wave2.proofwiki.foundation08."+a["slug"]
  terms.append({"id":term_id,"label":a["label"],"source_id":"src.proofwiki",
    "locator":a["url"],
    "discovery_provenance":"direct_read_independent_ProofWiki_set_mapping_definitions_2026_10_19",
    "human_verified":False})
  observations.append({"id":evidence_id,"term_id":term_id,"source_id":"src.proofwiki",
    "locator":a["url"],"record_kind":"paraphrase","text":a["text"],
    "context":a["context"],"editorial_note":a["note"],
    "potential_contextual_variants":a["candidate_variants"],
    "reviewed_by":"assistant_independent_set_foundations_source_check_2026_10_19",
    "human_verified":False})
  leads.append({"term_id":term_id,"source_id":"src.proofwiki","locator":a["url"],
    "source_access_outcome":"direct_page_read",
    "candidate_observation_id":evidence_id,
    "editorial_reason":a["note"],
    "potential_contextual_variants":a["candidate_variants"],
    "source_research_complete":True,"meaning_screened":False,"human_verified":False})
 def store(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  payload=chr(10).join(canonical(x) for x in rows)+chr(10)
  if path.exists() and path.read_text(encoding="utf-8")!=payload:
   raise PipelineError("Previous independently sourced observation intake conflicts")
  path.write_text(payload,encoding="utf-8")
  return path
 tr=w.ingest("terms",store(w.root/"intake/foundations_batch_08_terms.jsonl",terms),batch_size=3)
 ob=w.ingest("observations",store(w.root/"intake/foundations_batch_08_observations.jsonl",observations),batch_size=3)
 store(w.root/"wave2/foundation_source_discovery_batch_08.jsonl",leads)
 result={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
 if result!={"sources":9,"terms":350,"observations":773,"meanings":441,"relations":574}:
  raise PipelineError("Unexpected source intake counts "+str(result))
 report={
  "phase":"three_sourced_set_mapping_observations_pending_semantic_screen",
  "independently_sourced_terms":350,
  "source_evidence_observations":773,
  "screened_meanings_still":441,
  "screened_relations_still":574,
  "source_articles_read":3,
  "total_candidate_formulation_variants":8,
  "idempotent_term_skips":tr["already_present"],
  "idempotent_observation_skips":ob["already_present"],
  "typed_graph_and_bare_graph_equivalence_conventions_kept_distinct":True,
  "alternate_pair_encodings_not_declared_identical_sets":True,
  "meaning_reviews_automatically_approved":0,
  "link_reviews_automatically_approved":0,
  "stages_sealed":0,
  "human_peer_verified":False,
  "original_production_mathdef_consulted":False,
  "next":"Version 347-term source coverage before 350-term refresh; screen mapping and ordered-pair variants individually without conflating carrier conventions."
 }
 atomic_json(w.root/"state/wave2_foundations_batch_08.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",required=True,type=Path)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
