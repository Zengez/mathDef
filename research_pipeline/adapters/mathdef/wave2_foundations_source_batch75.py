"""Batch 75 source-only intake: four independently reviewed new foundations.

The generic Workspace/coverage engine remains reusable for other knowledge
topics. Only this mathDef adapter selects mathematical terms/source scope.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
RESEARCH="wave2/source_crosscheck_batch74_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_75.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
PRE={"sources":14,"terms":410,"observations":841,"meanings":510,"relations":698}
POST=dict(PRE,terms=414,observations=848)
KEYS=("noetherian-module","submodule","discrete-topology","continuous-topological-map")
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    text="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=text:
        raise PipelineError("Previously independently source-reviewed data changed")
    path.write_text(text,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in PRE):
        raise PipelineError("Unsealed independent Wave 2 only")
    if {s:len(w.records(s)) for s in PRE} not in (PRE,POST):
        raise PipelineError("Unexpected source baseline")
    sources=w.records("sources")
    if sources.get("src.proofwiki",{}).get("access")!="free" or sources["src.proofwiki"].get("rights")!="permitted":
        raise PipelineError("Missing vetted accessible source")
    research={r["key"]:r for r in jsonl(w.root/RESEARCH)}
    if set(research)!=set(KEYS) or len(research)!=4:
        raise PipelineError("Exactly four previously source-reviewed foundation contexts required")
    meanings=w.records("meanings")
    for key in KEYS:
        if any(key.replace("-"," ")==m["display_term"].lower() for m in meanings.values()):
            raise PipelineError("Same-concept existing meaning may be a duplicate: "+key)
    terms=[];obs=[];leads=[]
    for key in KEYS:
        r=research[key]
        if (not r["source_reviewed"] or r["stage_ingested"] or r["production_corpus_consulted"]
            or r["source_id"]!="src.proofwiki" or
            not r["url"].startswith("https://proofwiki.org/wiki/Definition") or
            len(r["reason"])<230 or len(r["forms"]) not in (1,2,3)):
            raise PipelineError("Independent source provenance incomplete: "+key)
        tid="term.wave2.foundation75."+key
        terms.append({"id":tid,"label":r["term"],"source_id":"src.proofwiki",
           "locator":r["url"],"discovery_provenance":RESEARCH,"human_verified":False})
        for i,form in enumerate(r["forms"],1):
            obs.append({"id":f"obs.wave2.foundation75.{key}.{i:02d}",
               "term_id":tid,"source_id":"src.proofwiki",
               "locator":r["url"],"record_kind":"paraphrase",
               "text":form["text"],"context":r["context"]+" / "+form["variant"],
               "editorial_note":r["reason"]+" Source section: "+form["section"],
               "reviewed_by":"assistant_independent_foundation75_source_screen_2026_10_20",
               "human_verified":False})
        leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":r["url"],
           "candidate_observation_id":f"obs.wave2.foundation75.{key}.01",
           "source_access_outcome":"direct_page_read",
           "editorial_reason":r["reason"],"source_research_complete":True,
           "meaning_screened":False,"human_verified":False,
           "review_reference":"review.wave2.foundation75."+key})
    w.ingest("terms",store(w.root/"intake/foundation75_terms.jsonl",terms),batch_size=4)
    w.ingest("observations",store(w.root/"intake/foundation75_observations.jsonl",obs),batch_size=7)
    store(w.root/LEADS,leads)
    path=w.root/MANIFEST
    cfg=json.loads(path.read_text(encoding="utf-8"))
    earlier=[f"wave2/foundation_source_discovery_batch_{i}.jsonl" for i in (49,54,58,62,66,70)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (earlier,earlier+[LEADS]):
        raise PipelineError("Prior supplemental lead manifest was modified")
    cfg["paths"]=earlier+[LEADS]
    atomic_json(path,cfg)
    counts={s:len(w.records(s)) for s in POST}
    if counts!=POST:
        raise PipelineError("New source record count not as independently researched")
    report={
       "batch":75,"counts":counts,"source_terms_added":4,"source_observations_added":7,
       "new_screened_meanings":0,"new_screened_links":0,
       "noetherian_module_variants_sourced":3,"continuous_topological_map_source_resolved":True,
       "discrete_nonempty_convention_explicit":True,
       "old_410_term_reviews_unchanged":True,"human_peer_verified":False,
       "original_mathdef_production_used":False,"all_stages_unsealed":True,
       "next":"Individually screen all four sourced meanings and seven variant formulations; then screen non-circular prerequisite links and revisit previously missing Noetherian-module link with a recorded override."
    }
    atomic_json(w.root/"state/wave2_foundations_source_batch75.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
