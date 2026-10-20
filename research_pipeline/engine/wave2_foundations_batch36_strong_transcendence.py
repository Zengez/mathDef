"""Recover exact Stacks Definition 10.123.7 without treating Zariski's Main Theorem as a definition.

Independent, authored source paraphrase only. No new mathematical meaning or
dependency is automatically accepted. Frozen Wave 1 and production mathDef
content are never opened or modified.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,jsonl,atomic_json

SOURCE_URL="https://stacks.math.columbia.edu/tag/00PZ"
TERM_ID="term.wave2.foundation36.strongly-transcendental-subring-element"
OBS_ID="obs.wave2.foundation36.strongly-transcendental-subring-element"

def run(root):
 w=Workspace(root)
 base=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if base.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
  ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Only editable independent Wave 2 source records may be extended")
 before={"sources":9,"terms":376,"observations":799,"meanings":479,"relations":648}
 after={"sources":9,"terms":377,"observations":800,"meanings":479,"relations":648}
 now={s:len(w.records(s)) for s in before}
 if now not in (before,after):
  raise PipelineError("Unexpected baseline for one independently recovered definition "+str(now))
 reports=w.root/"state/wave2_original_59_unproductive_section_reinspection_complete_2026-10-20.json"
 audits=w.root/"wave2/original_unproductive_sections_independent_reinspection_batch10_2026-10-20.jsonl"
 if not reports.exists() or not audits.exists():
  raise PipelineError("Original section and source-rights research not independently audited")
 summary=json.loads(reports.read_text(encoding="utf-8"))
 if summary.get("individual_source_pages_reinspected")!=59:
  raise PipelineError("Original 59-source reinspection report missing")
 found=[x for x in jsonl(audits) if x["review_id"]=="wave2.original-unproductive-reinspection.00PI"]
 if len(found)!=1 or found[0].get("embedded_definition_source_url")!=SOURCE_URL:
  raise PipelineError("Strong transcendence not independently identified in exact Stacks section")
 src=w.records("sources").get("src.stacks")
 if not src or src["access"]!="free" or src["rights"] not in ("permitted","locator_only"):
  raise PipelineError("Source access/rights not approved")
 term={"id":TERM_ID,"label":"strongly transcendental element over a subring",
  "source_id":"src.stacks","locator":SOURCE_URL,
  "discovery_provenance":"independent_Stacks_10_123_7_embedded_definition_audit_2026_10_20",
  "human_verified":False}
 obs={"id":OBS_ID,"term_id":TERM_ID,"source_id":"src.stacks","locator":SOURCE_URL,
  "record_kind":"paraphrase",
  "text":"Given an inclusion R⊆S of commutative rings and x∈S, x is strongly transcendental over R if for every u∈S and finite coefficients a_0,...,a_n∈R, the equation u(a_0+a_1x+...+a_nx^n)=0 implies ua_i=0 for each i.",
  "context":"Stacks Definition 10.123.7: strong transcendence relative to ring inclusion, preserving all zero-divisor-sensitive scalar multiples u",
  "editorial_note":"Do not replace this by ordinary algebraic transcendence in an arbitrary ring with zerodivisors. In the integral-domain setting, Stacks explains equivalence with transcendence over corresponding fields of fractions.",
  "source_crosscheck_urls":["https://stacks.math.columbia.edu/tag/00PI",SOURCE_URL],
  "reviewed_by":"assistant_independent_stacks_source_review_2026_10_20",
  "human_verified":False}
 lead={"term_id":TERM_ID,"source_id":"src.stacks","locator":SOURCE_URL,
  "source_access_outcome":"direct_page_read","candidate_observation_id":OBS_ID,
  "source_section":"Stacks Definition 10.123.7",
  "original_source_heading_research_disposition":"no_suitable_definition_preserved_for_Zariski_Main_Theorem_title",
  "editorial_reason":"Genuine separately numbered definition inside a formerly unproductive theorem section. Strong transcendence uses all u∈S and annihilation of each coefficient under the same u.",
  "source_research_complete":True,"meaning_screened":False,"human_verified":False}
 def store(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  data="".join(canonical(x)+"\n" for x in rows)
  if path.exists() and path.read_text(encoding="utf-8")!=data:
   raise PipelineError("Prior direct-source audit batch differs")
  path.write_text(data,encoding="utf-8")
  return path
 t=w.ingest("terms",store(w.root/"intake/foundations_batch_36_terms.jsonl",[term]),batch_size=1)
 o=w.ingest("observations",store(w.root/"intake/foundations_batch_36_observations.jsonl",[obs]),batch_size=1)
 store(w.root/"wave2/foundation_source_discovery_batch_36.jsonl",[lead])
 actual={s:len(w.records(s)) for s in after}
 if actual!=after:
  raise PipelineError("Strongly transcendental independent source acquisition incomplete "+str(actual))
 report={"phase":"stacks_strongly_transcendental_embedded_definition_observation_acquired",
  "original_section_tag":"00PI","direct_definition_tag":"00PZ",
  "source_term_records":377,"source_observations":800,
  "previous_meanings_preserved":479,"previous_links_preserved":648,
  "new_mathematical_meanings_screened":0,"new_links_screened":0,
  "zero_divisor_sensitive_coefficient_condition_preserved":True,
  "original_theorem_heading_disposition_unchanged":True,
  "idempotent_term_skips":t["already_present"],"idempotent_observation_skips":o["already_present"],
  "all_stages_unsealed":True,"human_peer_verified":False,
  "original_production_mathdef_consulted":False,
  "next":"Version 376-term per-source coverage, then independently screen this one mathematical meaning while preserving all 491 previous formulation reviews and 648 screened dependency links."}
 atomic_json(w.root/"state/wave2_foundations_batch_36.json",report)
 return report

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--workspace",type=Path,required=True)
 a=ap.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
