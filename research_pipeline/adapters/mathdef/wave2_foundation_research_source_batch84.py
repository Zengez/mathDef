"""Batch 84: independently source martingale and graph-coloring prerequisites.

Topic-specific source decisions live in this mathDef adapter. Reusable
Workspace and term coverage engine remain independent of the subject.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
REVIEW="wave2/martingale_graph_foundation_research_batch83_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_84.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
FIRST={"sources":14,"terms":417,"observations":852,"meanings":517,"relations":706}
FINAL=dict(FIRST,terms=422,observations=858)
KEYS=("discrete-filtration","adapted-stochastic-process","conditional-expectation-sub-sigma","proper-vertex-coloring","stochastic-process")
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    s="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=s:
        raise PipelineError("Prior individually vetted source research changed")
    path.write_text(s,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in FIRST):
        raise PipelineError("Requires independent unsealed Wave 2")
    if {s:len(w.records(s)) for s in FIRST} not in (FIRST,FINAL):
        raise PipelineError("Unexpected source research counts")
    source=w.records("sources").get("src.proofwiki")
    if not source or source["access"]!="free" or source["rights"]!="permitted":
        raise PipelineError("ProofWiki source is not authorized for locator-based intake")
    researched={r["key"]:r for r in jsonl(w.root/REVIEW)}
    if set(researched)!=set(KEYS) or len(researched)!=5:
        raise PipelineError("Five vetted mathematical source terms required")
    existing=w.records("meanings")
    if any(r["display_term"].lower() in (
        "filtration of sigma-algebras","adapted stochastic process",
        "conditional expectation given a sigma-algebra",
        "proper vertex k-coloring","stochastic process") for r in existing.values()):
        raise PipelineError("Preexisting independent meaning collision needs manual reconciliation")
    terms=[];observations=[];leads=[]
    for key in KEYS:
        r=researched[key]
        if (r["production_corpus_used"] or not r["source_reviewed"]
            or not r["source_research_complete"] or not r["not_yet_stage_ingested"]
            or r["source_id"]!="src.proofwiki" or len(r["mathematical_review"])<220
            or len(r["forms"])!=(2 if key=="adapted-stochastic-process" else 1)):
            raise PipelineError("Individual source and mathematical scope evidence missing "+key)
        tid="term.wave2.found84."+key
        terms.append({
          "id":tid,"label":r["term"],"source_id":"src.proofwiki",
          "locator":r["url"],"discovery_provenance":REVIEW,"human_verified":False
        })
        for i,f in enumerate(r["forms"],1):
            observations.append({
              "id":f"obs.wave2.found84.{key}.{i:02d}",
              "term_id":tid,"source_id":"src.proofwiki","locator":r["url"],
              "record_kind":"paraphrase","text":f["text"],
              "context":r["context"]+" / "+f["variant"],
              "editorial_note":r["mathematical_review"],
              "reviewed_by":"assistant_independent_martingale_graph_foundation_source_screen_2026_10_20",
              "human_verified":False
            })
        leads.append({
          "term_id":tid,"source_id":"src.proofwiki","locator":r["url"],
          "candidate_observation_id":f"obs.wave2.found84.{key}.01",
          "source_access_outcome":"direct_page_read",
          "editorial_reason":r["mathematical_review"],"source_research_complete":True,
          "meaning_screened":False,"human_verified":False,
          "review_reference":"review.wave2.found84."+key
        })
    w.ingest("terms",store(w.root/"intake/found84_terms.jsonl",terms),batch_size=5)
    w.ingest("observations",store(w.root/"intake/found84_observations.jsonl",observations),batch_size=6)
    store(w.root/LEADS,leads)
    manifest=w.root/MANIFEST
    config=json.loads(manifest.read_text(encoding="utf-8"))
    earlier=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in (49,54,58,62,66,70,75,80)]
    if config.get("schema_version")!=1 or config.get("paths") not in (earlier,earlier+[LEADS]):
        raise PipelineError("Historical source-lead manifest differs")
    config["paths"]=earlier+[LEADS]
    atomic_json(manifest,config)
    counts={s:len(w.records(s)) for s in FINAL}
    if counts!=FINAL:
        raise PipelineError("Unanticipated source intake size")
    result={
      "batch":84,"counts":counts,"new_source_terms":5,"new_individual_source_observations":6,
      "new_meanings_screened":0,"new_links_screened":0,
      "previous_417_term_review_dispositions_preserved":True,
      "continuous_time_filtration_source_not_claimed":True,
      "mathworld_chromatic_polynomial_source_registration_still_pending":True,
      "human_peer_verified":False,"production_corpus_used":False,"all_stages_unsealed":True,
      "next":"Individually screen five new mathematical meanings with six formulations, then review graph-coloring source link and martingale probability foundations separately."
    }
    atomic_json(w.root/"state/wave2_found84_source_intake.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
