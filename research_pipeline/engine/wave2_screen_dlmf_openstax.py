"""Screen seven independent real-analysis and orthogonal-polynomial meaning contexts.

Preserve 474 existing formulation reviews and all 622 independently screened
links. New candidates are reviewed individually, never treated as synonyms
merely because they share a mathematical topic or source.
"""
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
from .core import Workspace,PipelineError,canonical,jsonl,digest,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

SPECS=[
dict(key="orthogonal-polynomials-interval",source_key="orthogonal-polynomials-dlmf",
     term="orthogonal polynomial system",group="wave2.orthogonal-polynomial-system",
     context="DLMF continuous real interval with admissible nonnegative weight",
     text="Let (a,b) be a real interval and w≥0 an integrable weight with 0<∫_a^b w(x)dx<∞ and ∫_a^b |x|^k w(x)dx<∞ for every positive integer k. A polynomial system (p_n)_{n≥0}, with deg(p_n)=n, is orthogonal relative to w when ∫_a^b p_n(x)p_m(x)w(x)dx=0 whenever n≠m.",
     reason="DLMF 18.2(i), equations 18.2.1 and 18.2.1_5: preserve polynomial exact degree n, nonnegative weight with positive finite total mass, and all finite moments. Interval-density context is not literally identical to discrete sums."),
dict(key="orthogonal-polynomials-countable",source_key="orthogonal-polynomials-dlmf",
     term="orthogonal polynomial system",group="wave2.orthogonal-polynomial-system",
     context="DLMF countably infinite discrete support with positive summable weights",
     text="Let X⊆R be a countably infinite set of distinct points and assign each x∈X a weight w_x>0 with Σ_{x∈X}|x|^k w_x<∞ for every integer k≥0. A system (p_n)_{n≥0} with deg(p_n)=n is orthogonal on X when Σ_{x∈X}p_n(x)p_m(x)w_x=0 for n≠m.",
     reason="DLMF 18.2(i) distinguishes countably infinite weighted sums from integrals and explicitly imposes finite moments. A finite-support system needs a finite sequence of degrees; do not extend the infinite system formula blindly."),
dict(key="orthogonal-polynomials-finite",source_key="orthogonal-polynomials-dlmf",
     term="orthogonal polynomial system",group="wave2.orthogonal-polynomial-system",
     context="DLMF finite set of N+1 distinct points with strictly positive weights",
     text="Let X⊆R consist of N+1 distinct points with weights w_x>0. Polynomials p_0,…,p_N, with deg(p_n)=n, form a finite orthogonal polynomial system on X if Σ_{x∈X}p_n(x)p_m(x)w_x=0 for all distinct n,m in {0,…,N}.",
     reason="DLMF 18.2(i), equation 18.2.3, limits the degree index to 0,…,N for N+1 support points. An infinite sequence of nonzero mutually orthogonal functions cannot be supported on a finite N+1 dimensional function space."),
dict(key="orthogonal-polynomials-measure",source_key="orthogonal-polynomials-dlmf",
     term="orthogonal polynomial system",group="wave2.orthogonal-polynomial-system",
     context="DLMF Lebesgue–Stieltjes measure with infinitely many points of increase",
     text="Let μ be a nonnegative Lebesgue–Stieltjes measure arising from an admissible bounded nondecreasing function with infinitely many points of increase and finite moments ∫|x|^k dμ(x)<∞ for all integers k≥0. A polynomial family p_n of degree n is orthogonal with respect to μ when ∫p_n(x)p_m(x)dμ(x)=0 for n≠m.",
     reason="DLMF 18.2(i), equation 18.2.4_5, explicitly extends orthogonality to admissible Lebesgue–Stieltjes measures. Infinite support and finite moments prevent unintended degeneracy; the measure framework is broader than a density formula."),
dict(key="antiderivative-on-interval",source_key="antiderivative-openstax",
     term="antiderivative",group="wave2.antiderivative-and-indefinite-integral",
     context="Elementary real calculus: differentiable real function on an interval",
     text="Let I⊆R be an open interval and f:I→R. A function F:I→R is an antiderivative of f on I if F is differentiable at every x∈I and F′(x)=f(x) for all x∈I.",
     reason="OpenStax Calculus Volume 1 §4.10 defines an antiderivative through the derivative identity. The open-interval hypothesis avoids endpoint derivative conventions; the result does not assert that a particular f must possess an antiderivative."),
dict(key="indefinite-integral-on-interval",source_key="antiderivative-openstax",
     term="indefinite integral",group="wave2.antiderivative-and-indefinite-integral",
     context="Elementary real calculus: full antiderivative family on a connected interval",
     text="If f:I→R has an antiderivative F on an interval I, its indefinite integral, written ∫f(x)dx, denotes the family of functions {F+C:C∈R} on I. This is not a single numerical definite integral.",
     reason="OpenStax Calculus Volume 1 §4.10 defines the indefinite integral as the general antiderivative F+C. Equality of derivatives entails difference by one constant on an interval; arbitrary disconnected domains need componentwise constants."),
dict(key="real-limit-punctured-epsilon-delta",source_key="real-limit-epsilon-delta-openstax",
     term="finite limit of a real function",group="wave2.real-function-limit",
     context="Real functions defined on a full punctured neighborhood of the approach point",
     text="Suppose a,L∈R and f is defined for every x≠a in some open interval containing a. Then lim_{x→a}f(x)=L if for every ε>0 there exists δ>0 such that for all x with 0<|x−a|<δ in that interval, one has |f(x)−L|<ε.",
     reason="OpenStax Calculus Volume 1 §2.5 gives this punctured-neighborhood epsilon–delta definition for finite real limits. No assumption on f(a) is needed; relative-domain and one-sided limits require separate domain hypotheses and separate source review.")
]
def run(root):
 w=Workspace(root)
 if json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8")).get("mode")!="second_wave":
  raise PipelineError("Independent second-wave fork required")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Cannot mutate sealed stages")
 expected={"sources":9,"terms":366,"observations":789,"relations":622}
 if any(len(w.records(s))!=n for s,n in expected.items()):
  raise PipelineError("Requires committed source-only DLMF/OpenStax evidence with 622 links")
 prior=w.root/"state/wave2_foundations_batch_19.json"
 if not prior.exists() or json.loads(prior.read_text(encoding="utf-8")).get("new_meanings_screened")!=0:
  raise PipelineError("Source-only batch 19 is not verified")
 terms,observations=w.records("terms"),w.records("observations")
 prepared=[]
 for item in SPECS:
  tid="term.wave2.foundation19."+item["source_key"]
  oid="obs.wave2.foundation19."+item["source_key"]
  term,ob=terms.get(tid),observations.get(oid)
  if not term or not ob or ob["term_id"]!=tid or term["locator"]!=ob["locator"] or ob["record_kind"]!="paraphrase":
   raise PipelineError("No matching independently reviewed mathematical source "+item["key"])
  if item["key"].startswith("orthogonal-polynomials") and term["source_id"]!="src.dlmf":
   raise PipelineError("DLMF source convention mismatch")
  if len(item["reason"])<135 or len(item["text"])<150:
   raise PipelineError("Individual mathematical source review is inadequate")
  prepared.append({"id":"meaning.wave2.analysis."+item["key"],"term_group_id":item["group"],
   "display_term":item["term"],"context":item["context"],"term_ids":[tid],
   "formulations":[{"id":"form.wave2.analysis."+item["key"],"text":item["text"],
       "evidence_ids":[oid],"review_state":"candidate","human_verified":False}],
   "editorial_status":"candidate_independently_source_reviewed",
   "human_verified":False})
 def save(p,rows):
  p.parent.mkdir(parents=True,exist_ok=True)
  data="".join(canonical(x)+"\n" for x in rows)
  if p.exists() and p.read_text(encoding="utf-8")!=data:
   raise PipelineError("Previously committed source candidate differs")
  p.write_text(data,encoding="utf-8")
  return p
 batch=save(w.root/"intake/foundations_batch_20_meaning_candidates.jsonl",prepared)
 meanings=w.records("meanings")
 if len(meanings)==462:
  w.ingest("meanings",batch,batch_size=7)
 elif len(meanings)==469:
  if any(meanings.get(x["id"],{}).get("formulations",[{}])[0].get("text")!=x["formulations"][0]["text"] for x in prepared):
   raise PipelineError("Previously screened candidate text diverged")
 else:
  raise PipelineError("Expected precisely 462 or 469 screened meanings")
 audits=[]
 for item in SPECS:
  mid="meaning.wave2.analysis."+item["key"]
  curr=w.records("meanings")[mid]
  f=curr["formulations"][0]
  evidence={"meaning_id":mid,"formulation_id":f["id"],
    "source_evidence_id":"obs.wave2.foundation19."+item["source_key"],
    "mathematical_scope":item["context"],"reason":item["reason"],
    "reviewed_by":"assistant_independent_mathematical_source_review_2026_10_19",
    "human_verified":False,"decision":"accept_context_specific_formulation_without_equating_other_variants"}
  audits.append(evidence)
  if f["review_state"]=="screened":
   if curr.get("editorial_screening_reason")!=item["reason"]:
    raise PipelineError("Existing screened rationale conflicts with previous audit")
   continue
  if f["review_state"]!="candidate":
   raise PipelineError("Must screen only source-backed candidates")
  updated=dict(curr)
  updated["formulations"]=[dict(f,review_state="screened",
    source_screened_by=evidence["reviewed_by"],human_verified=False)]
  updated["editorial_status"]="source_mathematics_individually_screened"
  updated["editorial_screening_reason"]=item["reason"]
  updated["human_verified"]=False
  apply_revision(w.root,{
   "event_id":"revision.wave2.analysis."+item["key"]+".screen01",
   "stage":"meanings","record_id":mid,"before_digest":digest(curr),
   "editor":evidence["reviewed_by"],"reason":item["reason"],
   "operation":"replace","replacement":updated})
 save(w.root/"wave2/foundation_meaning_review_batch_20.jsonl",audits)
 meanings=w.records("meanings")
 forms={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
 if len(meanings)!=469 or len(forms)!=481 or any(f["review_state"]!="screened" for m in meanings.values() for f in m["formulations"]):
  raise PipelineError("Missing or unscreened context-specific candidate")
 ledger=w.root/"state/wave2_formulation_reviews.jsonl"
 previous=jsonl(ledger)
 snapshot=w.root/"state/wave2_formulation_reviews_snapshot_474_before_analysis20.jsonl"
 if len(previous)==474:
  if len({r["formulation_id"] for r in previous})!=474 or {x for r in previous for x in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Historical 474 relationship reviews do not cover all 622 links")
  original=ledger.read_text(encoding="utf-8")
  if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=original:
   raise PipelineError("Historical audit snapshot already exists but differs")
  snapshot.write_text(original,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_474_before_analysis20.json",{
    "review_count":474,"relations_preserved":622,
    "history_sha256":hashlib.sha256(original.encode("utf-8")).hexdigest(),
    "previous_catalog_digest":previous[0]["meaning_catalog_digest"],"human_verified":False})
  catalog_digest=digest(list(meanings.values()))
  next_rows=[dict(r,meaning_catalog_digest=catalog_digest) for r in previous]
  for item in prepared:
   next_rows.append({"formulation_id":item["formulations"][0]["id"],
      "meaning_id":item["id"],"meaning_catalog_digest":catalog_digest,
      "decision":"needs_review","relation_ids":[],"original_wave1_disposition":None,
      "source":"independent_dlmf_openstax_context_specific_screening",
      "editorial_reason":"Fresh source-screened contextual meaning requires individual mathematical prerequisite review; do not infer links from common terminology.",
      "reviewed_by":None,"human_verified":False})
  atomic_jsonl(ledger,sorted(next_rows,key=lambda x:x["formulation_id"]))
 elif len(previous)==481:
  if not snapshot.exists() or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in previous):
   raise PipelineError("Incomplete existing expanded review ledger")
 else:
  raise PipelineError("Unexpected mathematical review ledger size")
 previous=jsonl(snapshot);updated=jsonl(ledger)
 new_by={r["formulation_id"]:r for r in updated}
 if len(previous)!=474 or len(updated)!=481 or len(new_by)!=481:
  raise PipelineError("Snapshot or expanded mathematical review cardinality invalid")
 for row in previous:
  revised=new_by.get(row["formulation_id"])
  if not revised or any(revised.get(k)!=v for k,v in row.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Historical mathematical source review was overwritten")
 if {x for r in updated for x in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Screened link record lost individual mathematical review")
 check_cycles(meanings,w.records("relations"))
 if sum(r["decision"]=="needs_review" for r in updated)!=7:
  raise PipelineError("Expected seven new dependency reviews awaiting individual decisions")
 state=w.state("meanings")
 state.update(total=469,record_digest=digest(list(meanings.values())),
              screened_new_formulations=50,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 report={"phase":"seven_context_specific_dlmf_openstax_formulations_individually_screened",
  "meanings_total":469,"formulations_total":481,"new_meanings_screened":7,
  "historical_474_formulation_reviews_preserved":True,
  "prior_screened_links_preserved":622,
  "new_relation_decisions_pending":7,
  "distinct_orthogonal_polynomial_contexts":4,
  "disconnected_antiderivative_constant_scope_retained":True,
  "domain_relative_limit_not_falsely_ascribed_to_textbook":True,
  "all_stages_unsealed":True,"human_peer_verified":False,
  "original_production_mathdef_consulted":False,
  "next":"Individually examine seven mathematical prerequisite reviews, preserve zero unsupported links, and separately research generalized-domain limit variants."}
 atomic_json(w.root/"state/wave2_analysis20_meaning_screen.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",required=True,type=Path)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
