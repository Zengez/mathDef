"""Add only independently found embedded Stacks 10.38.1 and 10.112.5 source evidence.

The originally unproductive section *titles* stay unmodified. This creates two
new source terms and two authored mathematical paraphrases, not screened meanings.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,jsonl,atomic_json

SOURCES=[
 dict(key="integral-over-ideal",tag="037E",
  label="element integral over an ideal under a ring map",
  text="Given a ring map φ:R→S, ideal I⊆R, and g∈S, one says g is integral over I if a monic polynomial T^d+Σ_{j<d}a_j T^j∈R[T] annihilates g after applying φ, with every coefficient a_j∈I^{d-j}.",
  context="Stacks Definition 10.38.1: integral over an ideal along a ring map, requiring coefficient powers I^(d-j)",
  note="Do not identify with ordinary integrality of g over R; imposing a_j∈I^(d-j) for all j is the key additional condition."),
 dict(key="local-ring-fibre-at-prime",tag="00OG",
  label="local ring of the fibre of a ring map at a prime",
  text="For a ring map R→S and a prime ideal q⊆S with contraction p=q∩R, the local ring of the fibre at q is S_q/pS_q. Equivalently it is the localization of S⊗_R κ(p) at the prime induced by q.",
  context="Stacks Definition 10.112.5: local ring at a prime of an algebraic fibre over p; not the whole scheme-theoretic fibre",
  note="Keep the chosen prime q and contraction p as part of the context. Distinguish the fibre ring from the total-space local ring S_q.")
]

def run(root):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Only unsealed independent Wave 2 source acquisition permitted")
 before={"sources":9,"terms":374,"observations":797,"meanings":477,"relations":643}
 after={"sources":9,"terms":376,"observations":799,"meanings":477,"relations":643}
 now={s:len(w.records(s)) for s in before}
 if now not in (before,after):raise PipelineError("Unexpected source/meaning state "+str(now))
 evidence=jsonl(w.root/"wave2/original_unproductive_sections_independent_reinspection_batch06_2026-10-19.jsonl")
 for s in SOURCES:
  item=[r for r in evidence if r["review_id"]=="wave2.original-unproductive-reinspection."+s["tag"]]
  if len(item)!=1 or item[0].get("mathematical_result")!="embedded_formal_individual_mathematical_definition_discovered" or item[0].get("source_observation_ingested") is not False:
   raise PipelineError("Missing original embedded-definition source audit "+s["tag"])
 stacks=w.records("sources").get("src.stacks")
 if not stacks or stacks["access"]!="free" or stacks["rights"] not in ("permitted","locator_only"):
  raise PipelineError("Approved direct Stacks source access or rights missing")
 terms=[];observations=[];leads=[]
 for s in SOURCES:
  locator="https://stacks.math.columbia.edu/tag/"+s["tag"]
  tid="term.wave2.foundation33."+s["key"]
  oid="obs.wave2.foundation33."+s["key"]
  terms.append({"id":tid,"label":s["label"],"source_id":"src.stacks",
       "locator":locator,"discovery_provenance":"independent_stacks_embedded_numbered_definition_reinspection_2026_10_19",
       "human_verified":False})
  observations.append({"id":oid,"term_id":tid,"source_id":"src.stacks",
       "locator":locator,"record_kind":"paraphrase","text":s["text"],
       "context":s["context"],"editorial_note":s["note"],
       "source_crosscheck_urls":[locator],
       "reviewed_by":"assistant_independent_stacks_embedded_definitions_review_2026_10_19",
       "human_verified":False})
  leads.append({"term_id":tid,"source_id":"src.stacks","locator":locator,
      "source_access_outcome":"direct_page_read","candidate_observation_id":oid,
      "source_section":"Stacks Definition "+("10.38.1" if s["tag"]=="037E" else "10.112.5"),
      "original_source_heading_research_disposition":"no_suitable_definition_preserved",
      "editorial_reason":s["note"],
      "source_research_complete":True,"meaning_screened":False,"human_verified":False})
 def store(p,items):
  p.parent.mkdir(parents=True,exist_ok=True)
  body="".join(canonical(x)+"\n" for x in items)
  if p.exists() and p.read_text(encoding="utf-8")!=body:
   raise PipelineError("Individual source evidence prior version changed")
  p.write_text(body,encoding="utf-8")
  return p
 t=w.ingest("terms",store(w.root/"intake/foundations_batch_33_terms.jsonl",terms),batch_size=2)
 o=w.ingest("observations",store(w.root/"intake/foundations_batch_33_observations.jsonl",observations),batch_size=2)
 store(w.root/"wave2/foundation_source_discovery_batch_33.jsonl",leads)
 actual={s:len(w.records(s)) for s in after}
 if actual!=after:raise PipelineError("Two Stacks sources not fully ingested "+str(actual))
 report={
  "phase":"two_numbered_definition_observations_recovered_from_nondefinitional_section_headings",
  "source_term_records":376,"source_observations":799,
  "new_mathematical_meanings_screened":0,"new_dependency_links_screened":0,
  "source_sections":["Stacks 10.38.1 integral over an ideal","Stacks 10.112.5 local ring of fibre at a prime"],
  "coefficient_powers_I_d_minus_j_preserved":True,
  "fibre_prime_and_contraction_hypotheses_preserved":True,
  "original_heading_source_review_not_overridden":True,
  "term_idempotent_skips":t["already_present"],"observation_idempotent_skips":o["already_present"],
  "all_stages_unsealed":True,"human_peer_verified":False,
  "original_production_mathdef_consulted":False,
  "next":"Archive 374-term coverage and screen the two independently sourced context-specific mathematical meanings with a 489-review historical snapshot."
 }
 atomic_json(w.root/"state/wave2_foundations_batch_33.json",report)
 return report

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--workspace",required=True,type=Path)
 args=ap.parse_args()
 print(json.dumps(run(args.workspace),indent=2))
if __name__=="__main__":main()
