"""Batch 80: append individually vetted probability and combinatorics sources.

The MathWorld chromatic polynomial formulation is HELD pending distinct source
registration/rights review. No original mathDef definitions are consulted.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
REVIEW="wave2/source_variant_screen_batch79_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_80.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
PRE={"sources":14,"terms":414,"observations":848,"meanings":514,"relations":705}
POST=dict(PRE,terms=417,observations=852)
KEYS=("martingale-discrete","martingale-continuous-index","chromatic-proper-coloring")
URLS={
 "martingale-discrete":"https://proofwiki.org/wiki/Definition%3AMartingale/Discrete_Time",
 "martingale-continuous-index":"https://proofwiki.org/wiki/Definition%3AMartingale",
 "chromatic-proper-coloring":"https://proofwiki.org/wiki/Definition%3AChromatic_Number"
}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Previously vetted source batch differs")
    path.write_text(body,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in PRE):
        raise PipelineError("Independent unsealed Wave 2 only")
    if {s:len(w.records(s)) for s in PRE} not in (PRE,POST):
        raise PipelineError("Unexpected source record counts")
    pw=w.records("sources").get("src.proofwiki")
    if not pw or pw["rights"]!="permitted" or pw["access"]!="free":
        raise PipelineError("Approved independent ProofWiki source not available")
    ms=w.records("meanings")
    if any(m["display_term"].lower() in ("martingale","chromatic number") for m in ms.values()):
        raise PipelineError("Potential duplicate mathematical meaning in independent catalog")
    approved={r["key"]:r for r in jsonl(w.root/REVIEW)}
    if len(approved)!=3 or set(approved)!=set(KEYS):
        raise PipelineError("Three individually screened mathematical source dossiers required")
    terms=[];observations=[];leads=[]
    for key in KEYS:
        r=approved[key]
        if (not r["source_ready"] or r["source_id"]!="src.proofwiki"
            or r["url"]!=URLS[key] or r["stage_ingested"] or r["meaning_screened"]
            or r["production_corpus_used"] or len(r["reason"])<290
            or len(r["forms"])!=(2 if key=="martingale-discrete" else 1)):
            raise PipelineError("Source/variant research incomplete: "+key)
        tid="term.wave2.research80."+key
        terms.append({"id":tid,"label":r["term"],"source_id":"src.proofwiki",
           "locator":r["url"],"discovery_provenance":REVIEW,"human_verified":False})
        for idx,f in enumerate(r["forms"],1):
            observations.append({
                "id":f"obs.wave2.research80.{key}.{idx:02d}",
                "term_id":tid,"source_id":"src.proofwiki","locator":r["url"],
                "record_kind":"paraphrase","text":f["text"],
                "context":r["context"]+" / "+f["variant"],
                "editorial_note":r["reason"]+" Source section: "+f["section"],
                "reviewed_by":"assistant_independent_martingale_chromatic_source_review_2026_10_20",
                "human_verified":False
            })
        leads.append({
          "term_id":tid,"source_id":"src.proofwiki","locator":r["url"],
          "candidate_observation_id":f"obs.wave2.research80.{key}.01",
          "source_access_outcome":"direct_page_read",
          "editorial_reason":r["reason"],"source_research_complete":True,
          "meaning_screened":False,"human_verified":False,
          "review_reference":r["id"]
        })
    w.ingest("terms",store(w.root/"intake/research80_terms.jsonl",terms),batch_size=3)
    w.ingest("observations",store(w.root/"intake/research80_observations.jsonl",observations),batch_size=4)
    store(w.root/LEADS,leads)
    manifest=w.root/MANIFEST
    cfg=json.loads(manifest.read_text(encoding="utf-8"))
    previous=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in (49,54,58,62,66,70,75)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (previous,previous+[LEADS]):
        raise PipelineError("Existing source-lead manifest changed")
    cfg["paths"]=previous+[LEADS]
    atomic_json(manifest,cfg)
    result={s:len(w.records(s)) for s in POST}
    if result!=POST:
        raise PipelineError("Unexpected new source counts")
    report={
      "batch":80,"counts":result,"new_source_terms":3,"new_observations":4,
      "screened_meanings_added":0,"screened_links_added":0,
      "martingale_discrete_vs_continuous_time_distinct_source_contexts":True,
      "chromatic_polynomial_alt_held_for_source_registration":True,
      "prior_414_term_dispositions_preserved":True,
      "all_stages_unsealed":True,"human_peer_verified":False,
      "production_corpus_used":False,
      "next":"Screen three contextual meanings with four formulations. Retain real-valued adapted integrability and graph-coloring scope. Link review separate."
    }
    atomic_json(w.root/"state/wave2_martingale_chromatic_source_batch80.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
