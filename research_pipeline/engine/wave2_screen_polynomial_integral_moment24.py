"""Screen three independently sourced polynomial, Riemann and measure-moment meanings.

Preserves formal polynomial object identity, all-tags Riemann quantification and
measure moment existence hypotheses. Protect 483 prior reviews and 626 links.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .stage5_review_gate import atomic_jsonl
from .revisions import apply_revision
from .wave2_apply_links import check_cycles
SPECS=[
dict(key="nonzero-polynomial-degree",title="degree of a nonzero univariate polynomial",
 context="Formal algebra: nonzero polynomial in R[X] over a commutative unital ring",
 text="Let R be a commutative ring with multiplicative identity and let P=∑_{k=0}^n a_kX^k∈R[X] be nonzero. Its degree deg(P) is the greatest integer k≥0 for which a_k≠0_R. This definition does not assign a finite degree to the zero polynomial.",
 reason="ProofWiki Degree of Polynomial, primary one-variable definition, independently crosschecked against MathWorld Polynomial Order. Use a formal coefficient polynomial, not an arbitrary associated polynomial function; the zero polynomial has no nonnegative leading exponent and its degree requires a separate convention."),
dict(key="tagged-riemann-integral",title="proper Riemann integral on a compact interval",
 context="Classical real analysis: universal sufficiently fine tagged partition integral",
 text="Let f:[a,b]→R be bounded with a<b. For a finite partition a=x_0<⋯<x_n=b and arbitrary tags ξ_i∈[x_{i−1},x_i], let S=Σ_{i=1}^n f(ξ_i)(x_i−x_{i−1}) and mesh=max_i(x_i−x_{i−1}). The function f is Riemann integrable on [a,b] with integral L∈R if for every ε>0 there exists δ>0 such that |S−L|<ε for every tagged partition with mesh<δ.",
 reason="ProofWiki Integral (Calculus) gives a universal epsilon–delta criterion over all tagged subdivisions. Explicitly require compact bounded [a,b] and bounded f, rather than OpenStax's pedagogical sequence of equally spaced sums; no improper, infinite interval or Lebesgue–Stieltjes integration is inferred."),
dict(key="orthogonality-measure-raw-moment",source_key="orthogonality-measure-moment",title="nth raw moment of an orthogonality measure",
 context="DLMF orthogonal-polynomial analysis: raw power moment with respect to a positive measure",
 text="Let μ be a nonnegative Borel or Lebesgue–Stieltjes measure on a real interval (a,b) and let n be a nonnegative integer such that x↦x^n is μ-integrable. The nth raw moment of μ is μ_n=∫_a^b x^n dμ(x). It is finite only when the integral is finite.",
 reason="DLMF 18.2(ix), Equation 18.2.26 defines the power moment of an orthogonality measure. The existence of the integral and positive-measure context are hypotheses; a raw moment differs from a centered moment, and no probability normalization is assumed.")
]

def run(root):
 w=Workspace(root)
 if json.loads((w.root/"state/baseline.json").read_text()).get("mode")!="second_wave":
  raise PipelineError("Independent second wave required")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Cannot edit sealed stages")
 req={"sources":9,"terms":371,"observations":794,"relations":626}
 if any(len(w.records(s))!=n for s,n in req.items()):
  raise PipelineError("Requires 371 individually reviewed source terms and 626 existing links")
 intro=w.root/"state/wave2_foundations_batch_23.json"
 if not intro.exists() or json.loads(intro.read_text()).get("individually_read_source_sections")!=3:
  raise PipelineError("Three independently read source sections not registered")
 terms,obs=w.records("terms"),w.records("observations")
 candidates=[]
 for s in SPECS:
  evidence_key=s.get("source_key",s["key"])
  tid="term.wave2.foundation23."+evidence_key;oid="obs.wave2.foundation23."+evidence_key
  t,o=terms.get(tid),obs.get(oid)
  if not t or not o or o["term_id"]!=tid or o["locator"]!=t["locator"] or o["record_kind"]!="paraphrase":
   raise PipelineError("Source evidence missing "+s["key"])
  if len(s["reason"])<170 or len(s["text"])<155:
   raise PipelineError("Incomplete independent mathematical scope review "+s["key"])
  candidates.append({"id":"meaning.wave2.foundation."+s["key"],
   "display_term":s["title"],"term_group_id":"wave2.foundation."+s["key"],
   "context":s["context"],"term_ids":[tid],
   "formulations":[{"id":"form.wave2.foundation."+s["key"],
     "text":s["text"],"evidence_ids":[oid],
     "review_state":"candidate","human_verified":False}],
   "human_verified":False,"editorial_status":"source_specific_candidate"})
 def store(path,items):
  path.parent.mkdir(parents=True,exist_ok=True)
  data="".join(canonical(x)+"\n" for x in items)
  if path.exists() and path.read_text(encoding="utf-8")!=data:
   raise PipelineError("Historical reviewed source evidence conflicts")
  path.write_text(data,encoding="utf-8")
  return path
 path=store(w.root/"intake/foundations_batch_24_meaning_candidates.jsonl",candidates)
 prev=w.records("meanings")
 if len(prev)==471:
  w.ingest("meanings",path,batch_size=3)
 elif len(prev)==474:
  if any(prev.get(c["id"],{}).get("formulations",[{}])[0].get("text")!=c["formulations"][0]["text"] for c in candidates):
   raise PipelineError("Previous candidate text inconsistent")
 else:
  raise PipelineError("Unexpected prior meaning count")
 audits=[]
 for s in SPECS:
  mid="meaning.wave2.foundation."+s["key"]
  m=w.records("meanings")[mid]
  f=m["formulations"][0]
  audits.append({"meaning_id":mid,"formulation_id":f["id"],
    "source_observation_id":"obs.wave2.foundation23."+s.get("source_key",s["key"]),
    "source_specific_context":s["context"],"mathematical_reason":s["reason"],
    "reviewed_by":"assistant_independent_polynomial_integral_moment_review_2026_10_19",
    "decision":"screen_mathematically_source_scoped_formulation",
    "human_verified":False})
  if f["review_state"]=="screened":
   if m.get("editorial_screening_reason")!=s["reason"]:
    raise PipelineError("Previously screened source scope altered")
   continue
  if f["review_state"]!="candidate":
   raise PipelineError("Only candidate mathematical formulations may be screened")
  revised=dict(m)
  revised["formulations"]=[dict(f,review_state="screened",
     source_screened_by="assistant_independent_polynomial_integral_moment_review_2026_10_19",
     human_verified=False)]
  revised["editorial_status"]="individually_source_screened"
  revised["editorial_screening_reason"]=s["reason"]
  revised["human_verified"]=False
  apply_revision(w.root,{"event_id":"revision.wave2.foundation24."+s["key"]+".screen01",
      "stage":"meanings","record_id":mid,"before_digest":digest(m),
      "editor":"assistant_independent_polynomial_integral_moment_review_2026_10_19",
      "reason":s["reason"],"operation":"replace","replacement":revised})
 store(w.root/"wave2/foundation_meaning_review_batch_24.jsonl",audits)
 m=w.records("meanings")
 forms={f["id"]:p["id"] for p in m.values() for f in p["formulations"]}
 if len(m)!=474 or len(forms)!=486 or any(f["review_state"]!="screened" for p in m.values() for f in p["formulations"]):
  raise PipelineError("Incomplete three-source meaning screening")
 ledger=w.root/"state/wave2_formulation_reviews.jsonl"
 rows=jsonl(ledger)
 snap=w.root/"state/wave2_formulation_reviews_snapshot_483_before_foundations24.jsonl"
 if len(rows)==483:
  if len({r["formulation_id"] for r in rows})!=483 or {id for r in rows for id in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Historical review ledger incomplete or source links missing")
  original=ledger.read_text(encoding="utf-8")
  if snap.exists() and snap.read_text(encoding="utf-8")!=original:
   raise PipelineError("Existing 483-review snapshot conflicts")
  snap.write_text(original,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_483_before_foundations24.json",{
   "previous_formulation_reviews":483,"previous_screened_links":626,
   "sha256":hashlib.sha256(original.encode("utf-8")).hexdigest(),
   "human_peer_verified":False})
  newdigest=digest(list(m.values()))
  nextrows=[dict(r,meaning_catalog_digest=newdigest) for r in rows]
  for p in candidates:
   nextrows.append({"formulation_id":p["formulations"][0]["id"],
    "meaning_id":p["id"],"meaning_catalog_digest":newdigest,
    "decision":"needs_review","relation_ids":[],"original_wave1_disposition":None,
    "source":"source_scoped_independent_polynomial_integral_moment_meaning_review",
    "editorial_reason":"Independent context-specific meaning has not yet received a separate exact-prerequisite review.",
    "reviewed_by":None,"human_verified":False})
  atomic_jsonl(ledger,sorted(nextrows,key=lambda r:r["formulation_id"]))
 elif len(rows)==486:
  if not snap.exists() or any(r["meaning_catalog_digest"]!=digest(list(m.values())) for r in rows):
   raise PipelineError("Existing review ledger stale")
 else:
  raise PipelineError("Unknown formulation-review history count")
 historical=jsonl(snap);now=jsonl(ledger)
 ix={r["formulation_id"]:r for r in now}
 if len(historical)!=483 or len(now)!=486 or len(ix)!=486:
  raise PipelineError("Invalid reviewed formulation identities")
 for old in historical:
  x=ix[old["formulation_id"]]
  if any(x.get(k)!=v for k,v in old.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Historical screened mathematical decision changed")
 if {rid for r in now for rid in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Unreviewed prior mathematical link")
 check_cycles(m,w.records("relations"))
 if sum(x["decision"]=="needs_review" for x in now)!=3:
  raise PipelineError("Exactly three new links await independent analysis")
 state=w.state("meanings")
 state.update(total=474,record_digest=digest(list(m.values())),
              screened_new_formulations=55,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 report={"phase":"three_screened_foundational_polynomial_integral_and_moment_meanings",
  "screened_contextual_meanings":474,"formulations":486,
  "historical_483_reviews_preserved":True,
  "previous_screened_links_preserved":626,
  "new_individual_dependency_reviews_pending":3,
  "zero_polynomial_degree_context_separated":True,
  "tagged_riemann_vs_improper_integrals_not_conflated":True,
  "moment_finiteness_hypotheses_retained":True,
  "all_stages_unsealed":True,"human_peer_verified":False,
  "original_production_corpus_consulted":False,
  "next":"Individually review orthogonal polynomial dependencies on formal polynomial degree and finite moment definition; only accept correct source-scoped matches."}
 atomic_json(w.root/"state/wave2_foundations_batch_24_screened.json",report)
 return report
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
