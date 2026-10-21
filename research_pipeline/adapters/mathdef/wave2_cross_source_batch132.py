"""Batch132: four directly sourced mathematical headings, eight observations.

Source-only intake. Definitions/links must be screened in later separate stages.
Generic engine remains entirely topic-neutral.
"""
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/combinatorics_convex_graph_source_batch132_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_132.jsonl"
BASE={"sources":14,"terms":473,"observations":938,"meanings":587,"relations":855}
AFTER=dict(BASE,terms=477,observations=946)
KEYS=("bell-number","stirling-second-kind","convex-hull","vertex-degree")
N={"bell-number":1,"stirling-second-kind":2,"convex-hull":3,"vertex-degree":2}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Prior independent source record changed")
    path.write_text(body,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Requires independent unsealed Wave2")
    if {k:len(w.records(k)) for k in BASE} not in (BASE,AFTER):
        raise PipelineError("Unexpected independent baseline")
    src=w.records("sources").get("src.proofwiki")
    if not src or src["rights"]!="permitted" or src["access"]!="free":
        raise PipelineError("Source rights or approval absent")
    rows={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(rows)!=set(KEYS):raise PipelineError("Four separate source dossiers required")
    names={m["display_term"] for m in w.records("meanings").values()}
    if any(rows[k]["term"] in names for k in KEYS):
        raise PipelineError("Exact title collision with existing mathematical meaning")
    terms=[];observations=[];leads=[]
    for key in KEYS:
        r=rows[key];tid="term.wave2.cross132."+key
        if (r["source_id"]!="src.proofwiki" or r["source_access_outcome"]!="direct_page_read"
          or r["source_review_status"]!="individually_read_external_definition_with_variants"
          or r["stage_ingested"] or r["meaning_screened"] or r["production_corpus_consulted"]
          or len(r["review"])<390 or not r["source"].startswith("https://proofwiki.org/wiki/Definition")):
            raise PipelineError("Insufficient directly verified mathematical source and scope "+key)
        if key=="bell-number" and "B_0=1" not in r["review"]:
            raise PipelineError("Empty partition convention not verified")
        if key=="stirling-second-kind" and "δ" not in r["review"]:
            raise PipelineError("Boundary-value definition not verified")
        if key=="convex-hull" and "conv(∅)=∅" not in r["review"]:
            raise PipelineError("Empty convex hull convention or source equivalence unverified")
        if key=="vertex-degree" and "NOT equivalent" not in r["review"]:
            raise PipelineError("Source's multigraph overgeneralization needs explicit guard")
        terms.append({"id":tid,"label":r["term"],"source_id":"src.proofwiki",
             "locator":r["source"],"discovery_provenance":DOSSIER,"human_verified":False})
        contexts=r["contexts"]
        if len(contexts)!=1 or len(contexts[0]["forms"])!=N[key]:
            raise PipelineError("Unexpected individualized source forms "+key)
        for j,f in enumerate(contexts[0]["forms"],1):
            if not f["label"] or len(f["text"])<100:
                raise PipelineError("Source paraphrase insufficient "+key)
            observations.append({"id":f"obs.wave2.cross132.{key}.{j:02d}",
              "term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
              "record_kind":"paraphrase","text":f["text"],
              "context":contexts[0]["context"]+" / "+f["label"],
              "editorial_note":r["review"]+" Source sections: "+", ".join(r["source_sections"]),
              "reviewed_by":"assistant_independent_bell_stirling_convex_degree_source_review_2026_10_20",
              "human_verified":False})
        leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
          "candidate_observation_id":f"obs.wave2.cross132.{key}.01",
          "source_access_outcome":"direct_page_read","editorial_reason":r["review"],
          "source_research_complete":True,"meaning_screened":False,"human_verified":False,
          "review_reference":"research.wave2.cross132."+key})
    if len(terms)!=4 or len(observations)!=8:raise PipelineError("Four headings and eight forms required")
    w.ingest("terms",store(w.root/"intake/cross132_terms.jsonl",terms),batch_size=4)
    w.ingest("observations",store(w.root/"intake/cross132_observations.jsonl",observations),batch_size=8)
    store(w.root/LEADS,leads)
    path=w.root/"wave2/additional_source_lead_batches.json"
    cfg=json.loads(path.read_text(encoding="utf-8"))
    historical=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in
       (49,54,58,62,66,70,75,80,84,89,93,97,100,103,106,109,112,115,118,121,125,128)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (historical,historical+[LEADS]):
        raise PipelineError("Historical source lead manifest unexpectedly modified")
    cfg["paths"]=historical+[LEADS];atomic_json(path,cfg)
    counts={k:len(w.records(k)) for k in AFTER}
    if counts!=AFTER:raise PipelineError("Source-only inventory incorrect")
    report={"batch":132,"counts":counts,"new_source_headings":4,"new_observations":8,
      "new_meanings":0,"new_links":0,"bell_number_zero_partition_case":True,
      "stirling_two_equivalent_formulations":True,"convex_hull_three_equivalent_forms":True,
      "simple_vertex_degree_context_scope_explicit":True,"multigraph_neighbor_count_not_equivalent":True,
      "previous_624_formulation_reviews_and_855_links_preserved":True,
      "prior_three_source_quarantines_untouched":True,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch133 mathematically screen four contextual meanings with eight individual forms; Batch134 separately screen exact prerequisite links."}
    atomic_json(w.root/"state/wave2_cross132_source_intake.json",report);return report
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
