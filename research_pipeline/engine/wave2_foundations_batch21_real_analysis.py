"""Two independently read OpenStax real-analysis source observations.

Adds derivative-at-point and real absolute-value source evidence only. Does not
screen meanings, reopen blocked PlanetMath sources or invent links.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json
CASES=[
 dict(key="real-derivative-point",name="derivative of real function at interior point",
      url="https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative",
      text="For real f defined on an open interval containing a, its derivative f'(a), when it exists as a finite real number, is the limit as h→0 of [f(a+h)−f(a)]/h. Equivalently it is the limit as x→a of [f(x)−f(a)]/(x−a).",
      note="OpenStax Calculus Volume 1 §3.1: both equivalent difference quotient limits are given with a as interior point. A one-sided endpoint derivative and a generalized derivative are separate conventions.",
      variants=["increment h→0 derivative","x→a difference quotient derivative"]),
 dict(key="real-absolute-value",name="absolute value on the real line",
      url="https://openstax.org/books/calculus-volume-1/pages/1-1-review-of-functions",
      text="For each real x, |x| equals x when x≥0 and equals −x when x<0; it is nonnegative and |x−y| gives the usual distance between real x and y.",
      note="OpenStax Calculus Volume 1 §1.1: precise piecewise real absolute-value function. The induced real metric and complex modulus are mathematically related, but not the same function/type.",
      variants=["real absolute-value function","real distance d(x,y)=|x−y| as separately constructed metric"])
]
def run(root):
 w=Workspace(root)
 if json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8")).get("mode")!="second_wave":
  raise PipelineError("Independent Wave 2 required")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("No sealed stage may be modified")
 initial={"sources":9,"terms":366,"observations":789,"meanings":469,"relations":623}
 final={"sources":9,"terms":368,"observations":791,"meanings":469,"relations":623}
 current={s:len(w.records(s)) for s in initial}
 if current not in (initial,final):
  raise PipelineError("Unexpected pre-intake independent state "+str(current))
 prev=w.root/"state/wave2_analysis20_dependency_reviews_complete.json"
 if not prev.exists() or json.loads(prev.read_text(encoding="utf-8")).get("screened_relationships")!=623:
  raise PipelineError("Earlier source and mathematical review checkpoint unavailable")
 src=w.records("sources").get("src.openstax_calculus")
 if not src or src["access"]!="free" or src["rights"] not in ("locator_only","permitted"):
  raise PipelineError("OpenStax rights/access not approved")
 terms=[];observations=[];leads=[]
 for x in CASES:
  tid="term.wave2.foundation21."+x["key"]
  oid="obs.wave2.foundation21."+x["key"]
  terms.append({"id":tid,"label":x["name"],"source_id":"src.openstax_calculus",
     "locator":x["url"],"discovery_provenance":"direct_read_independent_OpenStax_definition_2026_10_19",
     "human_verified":False})
  observations.append({"id":oid,"term_id":tid,"source_id":"src.openstax_calculus",
     "locator":x["url"],"record_kind":"paraphrase","text":x["text"],"context":x["note"],
     "editorial_note":x["note"],"potential_contextual_variants":x["variants"],
     "reviewed_by":"assistant_independent_calculus_source_review_2026_10_19",
     "human_verified":False})
  leads.append({"term_id":tid,"source_id":"src.openstax_calculus","locator":x["url"],
    "source_access_outcome":"direct_page_read","candidate_observation_id":oid,
    "editorial_reason":x["note"],"source_research_complete":True,
    "meaning_screened":False,"human_verified":False})
 def store(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  data="".join(canonical(x)+"\n" for x in rows)
  if path.exists() and path.read_text(encoding="utf-8")!=data:
   raise PipelineError("Earlier independently attributed source batch differs")
  path.write_text(data,encoding="utf-8")
  return path
 tr=w.ingest("terms",store(w.root/"intake/foundations_batch_21_terms.jsonl",terms),batch_size=2)
 ob=w.ingest("observations",store(w.root/"intake/foundations_batch_21_observations.jsonl",observations),batch_size=2)
 store(w.root/"wave2/foundation_source_discovery_batch_21.jsonl",leads)
 after={s:len(w.records(s)) for s in final}
 if after!=final:
  raise PipelineError("Unanticipated source record count "+str(after))
 result={"phase":"two_independently_read_real_analysis_foundations_source_only",
   "counts":after,"direct_source_pages_read":2,
   "source_candidates_added":2,"mathematical_meanings_screened":0,"links_screened":0,
   "source_specific_scope_preserved":True,
   "old_planetmath_access_block_not_reclassified":True,
   "idempotent_term_skips":tr["already_present"],
   "idempotent_observation_skips":ob["already_present"],
   "all_stages_unsealed":True,"human_peer_verified":False,"original_production_corpus_consulted":False,
   "next":"Rebuild source coverage 368, mathematically screen point derivative and real absolute-value, then audit three newly possible prerequisites."}
 atomic_json(w.root/"state/wave2_foundations_batch_21.json",result)
 return result

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--workspace",type=Path,required=True)
 a=ap.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
