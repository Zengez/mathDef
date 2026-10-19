"""Source-only independent Wave 2 batch 19: DLMF and OpenStax definitions.

This intake adds three directly read source observations with original short
paraphrases and alternative-context notes. No meanings/relations are screened.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

CASES=[
 dict(key="orthogonal-polynomials-dlmf",name="orthogonal polynomial system (interval/discrete/measure contexts)",
      source="src.dlmf",url="https://dlmf.nist.gov/18.2.i",
      text="For polynomials p_n of exact degree n on a real interval, orthogonality with respect to a nonnegative admissible weight w means the weighted integral of p_n p_m vanishes for n≠m; the DLMF also specifies discrete weights and a Lebesgue–Stieltjes measure generalization.",
      scope="DLMF §18.2(i), equations 18.2.1–18.2.4_5: continuous, discrete and measure cases have distinct support, positivity and moment assumptions; do not silently identify the definitions or treat a finite support system as an infinite full degree sequence.",
      variant_count=3),
 dict(key="antiderivative-openstax",name="antiderivative and indefinite integral (connected-domain distinction)",
      source="src.openstax_calculus",url="https://openstax.org/books/calculus-volume-1/pages/4-10-antiderivatives",
      text="For a real-valued function f on an interval I, a differentiable F is an antiderivative of f if F'(x)=f(x) for all x∈I. The indefinite integral notation denotes the family F+C, with one constant C on a connected interval.",
      scope="OpenStax Calculus 1 §4.10: the F+C uniqueness conclusion uses connected interval I; on disconnected domains constants on different components can differ. Indefinite integral notation represents a family, not a single numerical integral.",
      variant_count=3),
 dict(key="real-limit-epsilon-delta-openstax",name="epsilon-delta limit of a real function (punctured neighborhood)",
      source="src.openstax_calculus",url="https://openstax.org/books/calculus-volume-1/pages/2-5-the-precise-definition-of-a-limit",
      text="Assume f is defined on a punctured interval around a∈R. A finite real limit L exists at a if every ε>0 admits δ>0 such that 0<|x−a|<δ implies |f(x)−L|<ε.",
      scope="OpenStax Calculus 1 §2.5 assumes a full punctured interval. Relative-domain and one-sided versions need separate quantifier domains and accumulation-point/directional hypotheses; f(a) is irrelevant.",
      variant_count=2)
]
def run(root):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave":
  raise PipelineError("Only independently forked second wave may be extended")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Do not modify sealed research stages")
 expected_before={"sources":9,"terms":363,"observations":786,"meanings":462,"relations":622}
 expected_after={"sources":9,"terms":366,"observations":789,"meanings":462,"relations":622}
 before={s:len(w.records(s)) for s in expected_before}
 if before not in (expected_before,expected_after):
  raise PipelineError("Unexpected Wave 2 research counts "+str(before))
 previous=w.root/"state/wave2_cross_source_field_theory_audit.json"
 if not previous.exists() or json.loads(previous.read_text(encoding="utf-8")).get("link_count_preserved")!=622:
  raise PipelineError("Required prior completed mathematical/source audit missing")
 source_records=w.records("sources")
 terms,observations,leads=[],[],[]
 for item in CASES:
  src=source_records.get(item["source"])
  if not src or src["access"]!="free" or src["rights"] not in ("permitted","locator_only"):
   raise PipelineError("Source not approved for traceable paraphrase")
  tid="term.wave2.foundation19."+item["key"]
  oid="obs.wave2.foundation19."+item["key"]
  terms.append({"id":tid,"label":item["name"],"source_id":item["source"],
                "locator":item["url"],"human_verified":False,
                "discovery_provenance":"individual_public_source_definition_read_2026_10_19"})
  observations.append({"id":oid,"term_id":tid,"source_id":item["source"],
        "locator":item["url"],"record_kind":"paraphrase","text":item["text"],
        "context":item["scope"],"editorial_note":item["scope"],
        "source_variant_count_to_review":item["variant_count"],
        "reviewed_by":"assistant_independent_public_mathematical_source_review_2026_10_19",
        "human_verified":False})
  leads.append({"term_id":tid,"source_id":item["source"],"locator":item["url"],
        "source_access_outcome":"direct_page_read","candidate_observation_id":oid,
        "editorial_reason":item["scope"],"source_research_complete":True,
        "meaning_screened":False,"human_verified":False})
 def store(p,rows):
  p.parent.mkdir(parents=True,exist_ok=True)
  body="".join(canonical(row)+"\n" for row in rows)
  if p.exists() and p.read_text(encoding="utf-8")!=body:
   raise PipelineError("Conflicting prior source evidence "+str(p))
  p.write_text(body,encoding="utf-8")
  return p
 t=w.ingest("terms",store(w.root/"intake/foundations_batch_19_terms.jsonl",terms),batch_size=3)
 o=w.ingest("observations",store(w.root/"intake/foundations_batch_19_observations.jsonl",observations),batch_size=3)
 store(w.root/"wave2/foundation_source_discovery_batch_19.jsonl",leads)
 after={s:len(w.records(s)) for s in expected_after}
 if after!=expected_after:
  raise PipelineError("Post-ingest source counts inconsistent "+str(after))
 result={"phase":"three_direct_dlmf_openstax_mathematical_source_observations_not_meanings",
   "counts":after,"source_sections_read":3,"context_variants_to_review":8,
   "new_term_records":3,"new_source_observations":3,
   "already_present_term_count":t["already_present"],
   "already_present_observation_count":o["already_present"],
   "new_meanings_screened":0,"new_relations_screened":0,
   "source_rights":"locator_only_with_original_short_paraphrases",
   "stages_unsealed":True,"frozen_wave1_unchanged":True,
   "human_peer_verified":False,"original_production_mathdef_consulted":False,
   "next":"Version source review ledger 363→366; then individually screen interval and integral domain hypotheses, weight/measure variants."}
 atomic_json(w.root/"state/wave2_foundations_batch_19.json",result)
 return result

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
