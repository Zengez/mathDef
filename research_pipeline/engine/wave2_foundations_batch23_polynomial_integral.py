"""Independent source-only Wave 2 evidence: polynomial degree, Riemann integral and moments.

Do not automatically assume tagged Riemann integrability for improper/open
intervals, assign degree zero to the null polynomial, or assume finite measure
moments without hypotheses. Each source is individually rights checked.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json
CASES=[
dict(key="nonzero-polynomial-degree",label="degree of a nonzero univariate formal polynomial",
 source="src.proofwiki",url="https://proofwiki.org/wiki/Definition%3ADegree_of_Polynomial",
 text="For a nonzero polynomial P=∑_{k=0}^n a_k X^k over a commutative ring R with 1, deg(P) is the largest nonnegative exponent k with a_k≠0_R. The coefficient sequence has finite support.",
 note="ProofWiki first one-variable definition, independently compared with MathWorld Polynomial Order. This is a formal polynomial, not merely its associated polynomial function; do not assign zero polynomial a finite degree, and verify the composite page's confusing degree-zero subsection separately.",
 crosscheck=["https://mathworld.wolfram.com/PolynomialOrder.html"]),
dict(key="tagged-riemann-integral",label="proper Riemann integral using all tagged partitions",
 source="src.proofwiki",url="https://proofwiki.org/wiki/Definition%3AIntegral_%28Calculus%29",
 text="For bounded real f on [a,b], the tagged Riemann sum for partition a=x_0<⋯<x_n=b and ξ_i∈[x_{i−1},x_i] is Σ_i f(ξ_i)(x_i−x_{i−1}). Its proper Riemann integral L exists if for every ε>0 there is δ>0 such that for every tagged partition with maximal subinterval length below δ, |S−L|<ε.",
 note="The ProofWiki definition quantifies over every sufficiently fine tagged subdivision on a bounded interval. Equal-spaced textbook sums under a single selection rule are not equivalent without additional conditions. Improper and Stieltjes integration are separate contexts.",
 crosscheck=["https://openstax.org/books/calculus-volume-1/pages/5-2-the-definite-integral"]),
dict(key="orthogonality-measure-moment",label="nth raw moment of an orthogonality measure",
 source="src.dlmf",url="https://dlmf.nist.gov/18.2.ix",
 text="For a measure μ on a real interval and nonnegative integer n, its nth raw moment, when the integral is defined, is μ_n=∫_a^b x^n dμ(x). In orthogonal-polynomial contexts the selected measure is required to have the necessary finite moments.",
 note="DLMF §18.2(ix), equation 18.2.26. The measure must be separately defined, moments need not exist for arbitrary measures, and raw versus central moments and probability normalization are distinct mathematical conventions.",
 crosscheck=["https://dlmf.nist.gov/18.2.i"])
]
def run(root):
 w=Workspace(root)
 if json.loads((w.root/"state/baseline.json").read_text()).get("mode")!="second_wave":
  raise PipelineError("Independent second-wave workspace required")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("No sealed source stage modifications")
 prior={"sources":9,"terms":368,"observations":791,"meanings":471,"relations":626}
 after={"sources":9,"terms":371,"observations":794,"meanings":471,"relations":626}
 current={s:len(w.records(s)) for s in prior}
 if current not in (prior,after):
  raise PipelineError("Unexpected independently reviewed source counts "+str(current))
 audit=w.root/"state/wave2_real_absolute_value_dependency_review_complete.json"
 if not audit.exists() or json.loads(audit.read_text()).get("screened_links")!=626:
  raise PipelineError("Prior 626-link mathematical review checkpoint not committed")
 sources=w.records("sources")
 terms=[];observations=[];leads=[]
 for c in CASES:
  source=sources.get(c["source"])
  if not source or source["access"]!="free" or source["rights"] not in ("permitted","locator_only"):
   raise PipelineError("Source permission does not permit independent short paraphrase")
  tid="term.wave2.foundation23."+c["key"]
  oid="obs.wave2.foundation23."+c["key"]
  terms.append({"id":tid,"label":c["label"],"locator":c["url"],
    "source_id":c["source"],
    "discovery_provenance":"independent_direct_math_source_read_2026_10_19",
    "human_verified":False})
  observations.append({"id":oid,"term_id":tid,"source_id":c["source"],
    "locator":c["url"],"record_kind":"paraphrase","text":c["text"],
    "context":c["note"],"editorial_note":c["note"],
    "source_crosscheck_urls":c["crosscheck"],
    "reviewed_by":"assistant_independent_polynomial_integral_moment_source_review_2026_10_19",
    "human_verified":False})
  leads.append({"term_id":tid,"source_id":c["source"],"locator":c["url"],
    "candidate_observation_id":oid,"source_access_outcome":"direct_page_read",
    "editorial_reason":c["note"],"source_research_complete":True,
    "meaning_screened":False,"human_verified":False})
 def store(path,items):
  path.parent.mkdir(parents=True,exist_ok=True)
  data="".join(canonical(row)+"\n" for row in items)
  if path.exists() and path.read_text(encoding="utf-8")!=data:
   raise PipelineError("Previous independently reviewed source record mismatch")
  path.write_text(data,encoding="utf-8")
  return path
 t=w.ingest("terms",store(w.root/"intake/foundations_batch_23_terms.jsonl",terms),batch_size=3)
 o=w.ingest("observations",store(w.root/"intake/foundations_batch_23_observations.jsonl",observations),batch_size=3)
 store(w.root/"wave2/foundation_source_discovery_batch_23.jsonl",leads)
 actual={s:len(w.records(s)) for s in after}
 if actual!=after:
  raise PipelineError("Unexpected source intake cardinality "+str(actual))
 report={"phase":"polynomial_riemann_integral_moment_source_observations_not_meanings",
  "counts":actual,"individually_read_source_sections":3,
  "source_meanings_screened":0,"new_relationships_screened":0,
  "zero_polynomial_degree_not_unjustifiably_assigned":True,
  "tagged_partition_vs_equal_grid_source_scope_preserved":True,
  "measure_finite_moment_hypothesis_not_dropped":True,
  "terms_already_present":t["already_present"],
  "observations_already_present":o["already_present"],
  "all_stages_unsealed":True,"human_peer_verified":False,
  "original_production_mathdef_consulted":False,
  "next":"Archive old 368 term source review history and screen exact polynomial degree, proper Riemann integral, and raw-moment hypotheses separately before any dependency links."}
 atomic_json(w.root/"state/wave2_foundations_batch_23.json",report)
 return report
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",required=True,type=Path)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
