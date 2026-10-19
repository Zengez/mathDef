"""Individually screen OpenStax derivative and absolute-value meanings in Wave 2.

Adds two precisely scoped source-backed concepts, keeps a byte-for-byte
snapshot of the 481 prior mathematical review decisions, does not add links.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

CASES=[
dict(key="real-derivative-point",title="derivative of a real function at an interior point",
context="OpenStax calculus: finite two-sided real derivative on an open interval",
text="Let f:I→R be a function on an open real interval I containing a∈I. If the finite limit exists, the derivative of f at a is f′(a)=lim_{h→0}(f(a+h)−f(a))/h, where h≠0 and a+h∈I.",
reason="The OpenStax §3.1 derivative is the ordinary real difference-quotient limit, requiring a function defined on a neighborhood of the interior point. Its existence is not assumed for every function; one-sided endpoint and generalized weak derivatives are separate notions."),
dict(key="real-absolute-value",title="absolute value of a real number",
context="OpenStax elementary real algebra: piecewise absolute-value function",
text="For each real number x, its absolute value |x| is x if x≥0 and −x if x<0. Consequently |x|≥0 and for real a,b the quantity |a−b| is their usual distance on the real line.",
reason="OpenStax §1.1 gives the ordinary real absolute value as a piecewise function. The induced distance d(a,b)=|a−b| is an associated metric construction, not literally the same object as the unary function |·|; complex modulus and general field absolute values need distinct contexts.")
]

def run(root):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave":
  raise PipelineError("Requires independent Wave 2")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Editing a sealed stage is prohibited")
 expected={"sources":9,"terms":368,"observations":791,"relations":623}
 if any(len(w.records(s))!=n for s,n in expected.items()):
  raise PipelineError("Requires exactly source-screened OpenStax source candidate intake")
 approved=w.root/"state/wave2_foundations_batch_21.json"
 if not approved.exists() or json.loads(approved.read_text(encoding="utf-8")).get("source_candidates_added")!=2:
  raise PipelineError("Source intake for two real analysis foundations not verified")
 terms,observations=w.records("terms"),w.records("observations")
 candidates=[]
 for x in CASES:
  tid="term.wave2.foundation21."+x["key"]
  oid="obs.wave2.foundation21."+x["key"]
  t,o=terms.get(tid),observations.get(oid)
  if not t or not o or t["locator"]!=o["locator"] or o["term_id"]!=tid or o["record_kind"]!="paraphrase":
   raise PipelineError("Missing source-located OpenStax original paraphrase for "+x["key"])
  if t["source_id"]!="src.openstax_calculus" or o.get("human_verified") is not False:
   raise PipelineError("Invalid source rights or false peer verification")
  candidates.append({
    "id":"meaning.wave2.analysis."+x["key"],
    "term_group_id":"wave2.real-analysis."+x["key"],
    "display_term":x["title"],"context":x["context"],
    "term_ids":[tid],
    "formulations":[{"id":"form.wave2.analysis."+x["key"],"text":x["text"],
      "evidence_ids":[oid],"review_state":"candidate","human_verified":False}],
    "editorial_status":"candidate_requires_individual_mathematical_review",
    "human_verified":False})
 def store(p,rows):
  p.parent.mkdir(parents=True,exist_ok=True)
  content="".join(canonical(row)+"\n" for row in rows)
  if p.exists() and p.read_text(encoding="utf-8")!=content:
   raise PipelineError("Source-specific candidate or review event has changed")
  p.write_text(content,encoding="utf-8")
  return p
 batch=store(w.root/"intake/foundations_batch_22_meaning_candidates.jsonl",candidates)
 prior=w.records("meanings")
 if len(prior)==469:
  w.ingest("meanings",batch,batch_size=2)
 elif len(prior)==471:
  if any(prior.get(x["id"],{}).get("formulations",[{}])[0].get("text")!=x["formulations"][0]["text"] for x in candidates):
   raise PipelineError("Previously ingested candidate differs")
 else:
  raise PipelineError("Expected precisely 469 or 471 source meanings")
 events=[]
 for x in CASES:
  mid="meaning.wave2.analysis."+x["key"]
  current=w.records("meanings")[mid]
  f=current["formulations"][0]
  if len(x["reason"])<120 or f["id"]!="form.wave2.analysis."+x["key"]:
   raise PipelineError("Unreviewed mathematical scope")
  events.append({"meaning_id":mid,"formulation_id":f["id"],
    "source_observation_id":"obs.wave2.foundation21."+x["key"],
    "mathematical_context":x["context"],"individual_review_reason":x["reason"],
    "decision":"source_specific_meaning_screened","human_verified":False})
  if f["review_state"]=="screened":
   if current.get("editorial_screening_reason")!=x["reason"]:
    raise PipelineError("Earlier source-screened mathematical decision diverged")
   continue
  if f["review_state"]!="candidate":
   raise PipelineError("Cannot screen unknown candidate state")
  revised=dict(current)
  revised["formulations"]=[dict(f,review_state="screened",
    source_screened_by="assistant_independent_real_analysis_review_2026_10_19",human_verified=False)]
  revised["editorial_screening_reason"]=x["reason"]
  revised["editorial_status"]="individually_source_screened"
  revised["human_verified"]=False
  apply_revision(w.root,{"event_id":"revision.wave2.foundation22."+x["key"]+".screen01",
     "stage":"meanings","record_id":mid,"before_digest":digest(current),
     "editor":"assistant_independent_real_analysis_review_2026_10_19",
     "reason":x["reason"],"operation":"replace","replacement":revised})
 store(w.root/"wave2/foundation_meaning_review_batch_22.jsonl",events)
 meanings=w.records("meanings")
 forms={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
 if len(meanings)!=471 or len(forms)!=483 or any(f["review_state"]!="screened" for m in meanings.values() for f in m["formulations"]):
  raise PipelineError("Incomplete source-screened 471-meaning/483-formulation catalog")
 ledger=w.root/"state/wave2_formulation_reviews.jsonl"
 rows=jsonl(ledger)
 snapshot=w.root/"state/wave2_formulation_reviews_snapshot_481_before_analysis22.jsonl"
 if len(rows)==481:
  if len({r["formulation_id"] for r in rows})!=481 or {i for r in rows for i in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Previous 481-review ledger is incomplete")
  raw=ledger.read_text(encoding="utf-8")
  if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=raw:
   raise PipelineError("Previous 481-review history differs")
  snapshot.write_text(raw,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_481_before_analysis22.json",{
    "historical_formulations":481,"relations":623,
    "sha256":hashlib.sha256(raw.encode("utf-8")).hexdigest(),
    "before_meaning_catalog_digest":rows[0]["meaning_catalog_digest"],
    "human_verified":False})
  updated=[dict(r,meaning_catalog_digest=digest(list(meanings.values()))) for r in rows]
  for new in candidates:
   updated.append({"formulation_id":new["formulations"][0]["id"],"meaning_id":new["id"],
     "meaning_catalog_digest":digest(list(meanings.values())),
     "decision":"needs_review","relation_ids":[],"original_wave1_disposition":None,
     "source":"independent_real_analysis_foundation_meaning_screening",
     "editorial_reason":"Newly sourced real-analysis meaning requires individually reviewed prerequisite comparison.",
     "reviewed_by":None,"human_verified":False})
  atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
 elif len(rows)==483:
  if not snapshot.exists() or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in rows):
   raise PipelineError("Previously expanded review ledger stale")
 else:
  raise PipelineError("Unexpected mathematical review ledger count")
 original=jsonl(snapshot);now=jsonl(ledger)
 current={r["formulation_id"]:r for r in now}
 if len(original)!=481 or len(now)!=483 or len(current)!=483:
  raise PipelineError("Review expansion corrupt")
 for old in original:
  revised=current[old["formulation_id"]]
  if any(revised.get(k)!=v for k,v in old.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Old individual source review was rewritten")
 if {rid for r in now for rid in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Screened links not fully represented in reviews")
 check_cycles(meanings,w.records("relations"))
 if sum(r["decision"]=="needs_review" for r in now)!=2:
  raise PipelineError("Expected exactly two new mathematical dependency reviews")
 state=w.state("meanings")
 state.update(total=471,record_digest=digest(list(meanings.values())),
              screened_new_formulations=52,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 result={"phase":"two_independently_source_screened_real_analysis_foundations",
    "screened_meanings":471,"formulation_reviews":483,"screened_links_preserved":623,
    "two_new_meanings_screened":2,"prior_481_individual_reviews_preserved":True,
    "new_dependency_reviews_pending":2,
    "derivative_at_interior_point_context_preserved":True,
    "absolute_value_vs_distance_distinction_preserved":True,
    "original_planetmath_access_block_unmodified":True,
    "all_wave2_stages_unsealed":True,"human_peer_verified":False,
    "production_mathdef_corpus_consulted":False,
    "next":"Individually compare derivative to the epsilon-delta limit; antiderivative to derivative; and limit to real absolute value, preserving source scope."}
 atomic_json(w.root/"state/wave2_foundations_batch_22_screened.json",result)
 return result

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
 main()
