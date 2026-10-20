"""Independently screen two graph-theory foundations, preserving 497 prior reviews.

ProofWiki simple graphs (undirected, loopless, no parallel edges) differ
from undirected loopless multigraphs (parallel edges possible). General graph
source remains a context-research observation, not an automatically screened
third meaning. Only Wave 2 may be edited; original corpus remains unread.
"""
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
from collections import Counter
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

SPECS=[
 dict(key="simple-undirected",source_slug="simple-undirected-graph",
      name="simple undirected graph (loopless)",
      group="graph-theory.simple-undirected",
      ctx="Set-based undirected graph with edges as two-element vertex subsets, no loops or parallel edges, finite and infinite V allowed",
      body="A simple undirected graph is a pair G=(V,E), where V is a set of vertices and E⊆{e⊆V:|e|=2}. Thus each edge {u,v} has distinct vertices u≠v, has no direction, and occurs at most once.",
      reason="ProofWiki's formal simple-graph definition requires an irreflexive symmetric adjacency relation, equivalent to edges as unordered vertex doubletons. No multiple edges, loops or weights are allowed; finite V or nonempty V are optional restrictions, not general axioms.",
      url="https://proofwiki.org/wiki/Definition%3ASimple_Graph"),
 dict(key="loopless-undirected-multigraph",source_slug="loopless-undirected-multigraph",
      name="loopless undirected multigraph",
      group="graph-theory.loopless-undirected-multigraph",
      ctx="Multiset of unordered vertex doubletons allows parallel undirected edges but no loops; does not demand finite vertices",
      body="A loopless undirected multigraph is a pair G=(V,E), where V is a set of vertices and E is a multiset of two-element subsets of V. Two copies of {u,v} represent parallel edges joining u and v; the graph is simple exactly when each edge multiplicity is at most one.",
      reason="ProofWiki's multigraph definition explicitly makes the edge collection a multiset of unordered two-element vertex subsets, allowing multiple copies of the same edge. Unlike a graph with loops, doubleton edges have distinct endpoints. A simple graph is the multiplicity-at-most-one special case.",
      url="https://proofwiki.org/wiki/Definition%3AMultigraph")
]
def run(root):
 w=Workspace(root)
 base=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if base.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
     ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Only an unsealed independent Wave 2 fork is editable")
 source_report=w.root/"state/wave2_graph_source_batch_42.json"
 if not source_report.exists():
  raise PipelineError("Directly read graph source evidence must be committed before meaning screening")
 sr=json.loads(source_report.read_text(encoding="utf-8"))
 if (sr.get("terms_after")!=384 or sr.get("observations_after")!=807 or
     sr.get("relations_screened_preserved")!=655 or
     not sr.get("source_conventions_distinguished")):
  raise PipelineError("Graph source evidence differs from reviewed scope")
 counts={s:len(w.records(s)) for s in ("sources","terms","observations","relations")}
 if counts!={"sources":9,"terms":384,"observations":807,"relations":655}:
  raise PipelineError("Graph review source/relationship baseline drift "+str(counts))
 before=w.records("meanings")
 if len(before) not in (485,487):
  raise PipelineError("Expected 485 prior meanings or 487 already added")
 terms,observations=w.records("terms"),w.records("observations")
 proposals=[];reviewed=[]
 for item in SPECS:
  tid="term.wave2.graph42."+item["source_slug"]
  oid="obs.wave2.graph42."+item["source_slug"]
  source=terms.get(tid);evidence=observations.get(oid)
  if (not source or not evidence or source["locator"]!=item["url"]
      or evidence["locator"]!=item["url"] or evidence["term_id"]!=tid
      or evidence["record_kind"]!="paraphrase" or evidence["human_verified"] is not False):
   raise PipelineError("Missing exact source-registered individual graph evidence "+item["key"])
  if len(item["reason"])<170 or len(item["body"])<130:
   raise PipelineError("Graph definition/review rationale insufficient")
  mid="meaning.wave2.graph42."+item["key"]
  fid="form.wave2.graph42."+item["key"]
  proposals.append({"id":mid,"display_term":item["name"],"context":item["ctx"],
    "term_group_id":item["group"],"term_ids":[tid],
    "human_verified":False,"editorial_status":"candidate_independent_source_context",
    "formulations":[{"id":fid,"text":item["body"],
       "evidence_ids":[oid],"review_state":"candidate","human_verified":False}]})
  reviewed.append({"meaning_id":mid,"formulation_id":fid,
    "source_evidence_id":oid,"source_url":item["url"],
    "mathematical_reason":item["reason"],
    "reviewed_by":"assistant_independent_graph_scope_mathematical_check_2026_10_20",
    "source_convention":"simple_no_parallel" if item["key"]=="simple-undirected" else "loopless_parallel_allowed",
    "mathematically_screened":True,"human_verified":False})
 def store(path,items):
  path.parent.mkdir(parents=True,exist_ok=True)
  body="".join(canonical(x)+"\n" for x in items)
  if path.exists() and path.read_text(encoding="utf-8")!=body:
   raise PipelineError("Previously committed graph context evidence differs")
  path.write_text(body,encoding="utf-8")
  return path
 inp=store(w.root/"intake/foundations_batch_43_graph_meanings.jsonl",proposals)
 if len(before)==485:
  w.ingest("meanings",inp,batch_size=2)
 else:
  for p in proposals:
   old=before.get(p["id"])
   if not old or old["formulations"][0]["text"]!=p["formulations"][0]["text"]:
    raise PipelineError("Earlier graph meaning intake differs from precise source")
 for p,r in zip(proposals,reviewed):
  m=w.records("meanings")[p["id"]];f=m["formulations"][0]
  if f["review_state"]=="candidate":
   updated=dict(m)
   updated["formulations"]=[dict(f,review_state="screened",human_verified=False,
      source_screened_by=r["reviewed_by"])]
   updated["editorial_status"]="individual_graph_theory_scope_screened"
   updated["editorial_screening_reason"]=r["mathematical_reason"]
   updated["human_verified"]=False
   apply_revision(w.root,{
     "event_id":"revision.wave2.graph43."+p["id"].split(".")[-1]+".screen01",
     "stage":"meanings","record_id":p["id"],"before_digest":digest(m),
     "editor":r["reviewed_by"],"reason":r["mathematical_reason"],
     "operation":"replace","replacement":updated})
  elif f["review_state"]!="screened" or m.get("editorial_screening_reason")!=r["mathematical_reason"]:
   raise PipelineError("Existing screened graph formulation conflicts")
 store(w.root/"wave2/foundation_meaning_review_batch_43.jsonl",reviewed)
 meanings=w.records("meanings")
 forms={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
 if len(meanings)!=487 or len(forms)!=499 or any(f["review_state"]!="screened" for m in meanings.values() for f in m["formulations"]):
  raise PipelineError("Mathematical graph screening incomplete")
 ledger=w.root/"state/wave2_formulation_reviews.jsonl"
 prior=jsonl(ledger)
 snap=w.root/"state/wave2_formulation_reviews_snapshot_497_before_graph43.jsonl"
 if len(prior)==497:
  if len({r["formulation_id"] for r in prior})!=497 or {rid for r in prior for rid in r["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("497 prior formulations do not cover all screened relationships")
  old=ledger.read_text(encoding="utf-8")
  if snap.exists() and snap.read_text(encoding="utf-8")!=old:
   raise PipelineError("Conflicting historical graph review snapshot")
  snap.write_text(old,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_497_before_graph43.json",{
     "review_count":497,"screened_links":655,
     "sha256":hashlib.sha256(old.encode("utf-8")).hexdigest(),
     "human_peer_verified":False})
  new_digest=digest(list(meanings.values()))
  rows=[dict(r,meaning_catalog_digest=new_digest) for r in prior]
  for p in proposals:
   rows.append({"formulation_id":p["formulations"][0]["id"],"meaning_id":p["id"],
      "meaning_catalog_digest":new_digest,"decision":"needs_review","relation_ids":[],
      "original_wave1_disposition":None,"reviewed_by":None,"human_verified":False,
      "source":"independent_proofwiki_graph_definition_review",
      "editorial_reason":"New source-scoped graph meaning requires independent source-anchored prerequisite review; cannot auto-infer graph-category equivalence."})
  atomic_jsonl(ledger,sorted(rows,key=lambda r:r["formulation_id"]))
 elif len(prior)==499:
  if not snap.exists() or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in prior):
   raise PipelineError("Previously extended meaning review catalog is unverified")
 else:raise PipelineError("Unexpected number of historical individual reviews")
 history=jsonl(snap);now=jsonl(ledger);curr={r["formulation_id"]:r for r in now}
 if len(history)!=497 or len(now)!=499 or len(curr)!=499:
  raise PipelineError("Review lineage lost while screening graph concepts")
 for old in history:
  r=curr.get(old["formulation_id"])
  if not r or any(r.get(k)!=v for k,v in old.items() if k!="meaning_catalog_digest"):
   raise PipelineError("An earlier reviewed formulation changed")
 if {rid for r in now for rid in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Prior independently screened relationship not in review ledger")
 check_cycles(meanings,w.records("relations"))
 dispositions=dict(Counter(r["decision"] for r in now))
 if dispositions!={"linked":491,"no_supported_target":5,"needs_review":3}:
  raise PipelineError("Unexpected post-graph-screen review states "+str(dispositions))
 state=w.state("meanings")
 state.update(total=487,record_digest=digest(list(meanings.values())),
     screened_new_formulations=68,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 report={
   "phase":"two_independent_graph_theory_meanings_individually_screened",
   "source_terms":384,"source_observations":807,
   "contextual_meanings":487,"formulations":499,
   "previous_655_screened_links_preserved":True,
   "previous_497_review_dispositions_preserved":True,
   "simple_vs_multigraph_multiplicity_separated":True,
   "null_graph_and_finite_conventions_not_silently_imposed":True,
   "general_graph_source_still_unscreened":True,
   "new_formulations_requiring_dependency_review":2,
   "review_dispositions":dispositions,
   "wave2_stages_unsealed":True,"human_peer_verified":False,
   "original_production_mathdef_consulted":False,
   "next":"Review source-anchored adjacency matrix and bipartite graph dependencies, and explicitly disposition graph foundation reviews without inventing earlier missing source concepts."
 }
 atomic_json(w.root/"state/wave2_graph_meaning_screen_batch_43.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
