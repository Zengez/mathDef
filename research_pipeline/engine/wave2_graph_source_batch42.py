"""Acquire three independent graph-theory foundations from directly read ProofWiki pages.

Distinguish abstract graphs, finite-or-infinite simple loopless graphs, and
multigraphs that admit parallel undirected edges. These are authored
paraphrases with exact source evidence, not approved meanings or links.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

ARTICLES=[
  dict(slug="graph-theory",label="graph with vertex and edge sets",
       locator="https://proofwiki.org/wiki/Definition%3AGraph_%28Graph_Theory%29",
       context="General graph terminology: pair of vertices and edges with endpoints; conventions for directed, loops, empty graphs and multiple edges vary",
       text="A graph G has a set V of vertices and a collection E of edges, each edge carrying two incident endpoints in V. How an edge is represented depends on the graph convention: unordered pairs, directed ordered pairs, or individually identifiable edges.",
       note="ProofWiki defines a graph intuitively through vertices and edges, then distinguishes directed, multigraph and loop conventions. This source is not itself a sufficiently specific standalone formal graph type to justify equivalence with every graph convention.",
       variants=["simple undirected","directed arcs","multigraph with parallel edges","loops and null-vertex convention"]),
  dict(slug="simple-undirected-graph",label="simple undirected graph with no loops",
       locator="https://proofwiki.org/wiki/Definition%3ASimple_Graph",
       context="Set-based simple loopless undirected graph; no weights or parallel edges; no mandatory finiteness",
       text="A simple undirected graph is a pair (V,E), where V is a set of vertices and E is a set of two-element subsets of V. An edge is an unordered pair {u,v} with u≠v, so self-loops and multiple edges between the same pair cannot occur.",
       note="ProofWiki formal simple-graph definition specifies antireflexive symmetric adjacency and equivalent unordered doubleton edges. The same page notes that some authors require V to be finite or nonempty, but these restrictions are not imposed in the general version.",
       variants=["finite simple graph adds finite V","nonempty simple graph adds V not empty","simple graph including possible empty V"]),
  dict(slug="loopless-undirected-multigraph",label="undirected multigraph without loops, parallel edges allowed",
       locator="https://proofwiki.org/wiki/Definition%3AMultigraph",
       context="Undirected multigraph with edge multiplicity from unordered pairs of distinct vertices, no required finiteness",
       text="An undirected loopless multigraph consists of a vertex set V and a multiset E of unordered two-element subsets {u,v} of V. Repeated occurrences of the same unordered pair represent distinct parallel edges; a simple graph is the special case with multiplicities at most one.",
       note="ProofWiki's multigraph definition explicitly allows multiple copies of an unordered pair of vertices and represents E as a multiset of doubletons. This convention has no loops. Different sources allow loops and use edge identities plus incidence maps; those must be separate variants.",
       variants=["edge multiplicity for loopless graphs","simple graph as multiplicity 0-or-1 case","pseudograph or loop-multigraph requires explicit loop conventions"])
]
def run(root):
 w=Workspace(root)
 b=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if b.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
      ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Only unsealed independent Wave 2 supports new research")
 after=w.root/"state/wave2_link_review_batch_41.json"
 if not after.exists() or json.loads(after.read_text(encoding="utf-8")).get("total_screened_links")!=655:
  raise PipelineError("Guarded graph source intake requires verified five-link batch 41")
 counts={stage:len(w.records(stage)) for stage in ("sources","terms","observations","meanings","relations")}
 expected={"sources":9,"terms":381,"observations":804,"meanings":485,"relations":655}
 completed={"sources":9,"terms":384,"observations":807,"meanings":485,"relations":655}
 if counts not in (expected,completed):
  raise PipelineError("Unexpected independent graph source baseline "+str(counts))
 source=w.records("sources").get("src.proofwiki")
 if source is None or source["access"]!="free" or source["rights"] not in ("permitted","locator_only"):
  raise PipelineError("ProofWiki source license/access not approved")
 terms=[];evidence=[];leads=[]
 for a in ARTICLES:
  tid="term.wave2.graph42."+a["slug"]
  oid="obs.wave2.graph42."+a["slug"]
  terms.append({"id":tid,"label":a["label"],"source_id":"src.proofwiki",
       "locator":a["locator"],
       "discovery_provenance":"direct_independent_mathematical_source_review_2026_10_20",
       "human_verified":False})
  evidence.append({"id":oid,"term_id":tid,"source_id":"src.proofwiki",
      "locator":a["locator"],"record_kind":"paraphrase","text":a["text"],
      "context":a["context"],"editorial_note":a["note"],
      "potential_contextual_variants":a["variants"],
      "reviewed_by":"assistant_independent_graph_foundation_sources_2026_10_20",
      "human_verified":False})
  leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":a["locator"],
      "source_access_outcome":"direct_page_read","candidate_observation_id":oid,
      "editorial_reason":a["note"],"contextual_variant_leads":a["variants"],
      "source_research_complete":True,"meaning_screened":False,
      "original_production_corpus_consulted":False,"human_verified":False})
 def store(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  payload="".join(canonical(r)+"\n" for r in rows)
  if path.exists() and path.read_text(encoding="utf-8")!=payload:
   raise PipelineError("Original graph source evidence conflicts with new batch")
  path.write_text(payload,encoding="utf-8")
  return path
 result1=w.ingest("terms",store(w.root/"intake/foundations_batch_42_terms.jsonl",terms),batch_size=3)
 result2=w.ingest("observations",store(w.root/"intake/foundations_batch_42_observations.jsonl",evidence),batch_size=3)
 store(w.root/"wave2/foundation_source_discovery_batch_42.jsonl",leads)
 got={stage:len(w.records(stage)) for stage in expected}
 if got!=completed: raise PipelineError("Graph source intake count drift "+str(got))
 report={
  "phase":"three_approved_proofwiki_graph_foundations_source_acquired",
  "terms_after":384,"observations_after":807,"meanings_screened_preserved":485,
  "relations_screened_preserved":655,
  "new_directly_read_articles":3,"new_meanings_screened":0,
  "source_conventions_distinguished":True,
  "general_graph_source_not_asserted_equivalent_to_simple_graph":True,
  "finite_graph_not_inferred_from_simple_graph":True,
  "multi_edges_not_conflated_with_simple_edges":True,
  "idempotent_term_skips":result1["already_present"],
  "idempotent_observation_skips":result2["already_present"],
  "stage_sealed":False,"human_peer_verified":False,
  "production_corpus_consulted":False,
  "next":"Expand source review ledger to 384; independently screen graph meanings before graph-based adjacency links."
 }
 atomic_json(w.root/"state/wave2_graph_source_batch_42.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
