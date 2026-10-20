"""Batch 93: source-only intake of independently verified module conventions.

Do not duplicate already screened general left module; retain right/unital
variations as independently reviewed source evidence pending mathematical review.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
RESEARCH="wave2/module_convention_variants_research_batch92_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_93.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
BEFORE={"sources":14,"terms":425,"observations":862,"meanings":527,"relations":730}
AFTER=dict(BEFORE,terms=428,observations=865)
KEYS=("right-module-nonunital","unital-left-module","unital-right-module")
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    data="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=data:
        raise PipelineError("Historical vetted source evidence changed")
    path.write_text(data,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Independent unsealed Wave 2 required")
    if {s:len(w.records(s)) for s in BEFORE} not in (BEFORE,AFTER):
        raise PipelineError("Independent stage has moved unexpectedly")
    pw=w.records("sources").get("src.proofwiki")
    if not pw or pw["rights"]!="permitted" or pw["access"]!="free":
        raise PipelineError("ProofWiki locator reuse not permitted")
    existing=w.records("meanings")
    if ("meaning.wave2.foundation.left-module-nonunital" not in existing or
        any(m["display_term"].lower() in (
           "right module over a ring","unitary left module over a ring",
           "unitary right module over a ring") for m in existing.values())):
        raise PipelineError("Potential duplicate module variant/collision")
    research={r["key"]:r for r in jsonl(w.root/RESEARCH)}
    if set(research)!=set(KEYS) or len(research)!=3:
        raise PipelineError("Three individually source-reviewed module contexts required")
    terms=[];obs=[];leads=[]
    for key in KEYS:
        r=research[key]
        if (r["stage_ingested"] or r["production_corpus_used"]
            or r["source_id"]!="src.proofwiki"
            or r["source_review_status"]!="direct_external_page_checked"
            or r["existing_left_module_reference"]!="meaning.wave2.foundation.left-module-nonunital"
            or len(r["mathematical_reason"])<260
            or len(r["definition"])<200
            or not r["source_url"].startswith("https://proofwiki.org/wiki/Definition")):
            raise PipelineError("Individual module convention source proof missing "+key)
        tid="term.wave2.module93."+key;oid="obs.wave2.module93."+key
        terms.append({"id":tid,"label":r["term"],
            "source_id":"src.proofwiki","locator":r["source_url"],
            "discovery_provenance":RESEARCH,"human_verified":False})
        obs.append({"id":oid,"term_id":tid,"source_id":"src.proofwiki",
            "locator":r["source_url"],"record_kind":"paraphrase",
            "text":r["definition"],"context":r["context"],
            "editorial_note":r["mathematical_reason"]+" Source section: "+r["section"],
            "reviewed_by":"assistant_independent_module_convention_source_review_2026_10_20",
            "human_verified":False})
        leads.append({"term_id":tid,"source_id":"src.proofwiki",
            "locator":r["source_url"],"candidate_observation_id":oid,
            "source_access_outcome":"direct_page_read",
            "editorial_reason":r["mathematical_reason"],
            "source_research_complete":True,"meaning_screened":False,
            "human_verified":False,"review_reference":"review.wave2.module93."+key})
    w.ingest("terms",store(w.root/"intake/module93_terms.jsonl",terms),batch_size=3)
    w.ingest("observations",store(w.root/"intake/module93_observations.jsonl",obs),batch_size=3)
    store(w.root/LEADS,leads)
    manifest=w.root/MANIFEST
    content=json.loads(manifest.read_text(encoding="utf-8"))
    old=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in (49,54,58,62,66,70,75,80,84,89)]
    if content.get("schema_version")!=1 or content.get("paths") not in (old,old+[LEADS]):
        raise PipelineError("Historical reviewed-source manifest changed")
    content["paths"]=old+[LEADS]
    atomic_json(manifest,content)
    counts={s:len(w.records(s)) for s in AFTER}
    if counts!=AFTER:
        raise PipelineError("Unexpected module source count")
    report={"batch":93,"counts":counts,"new_terms":3,"new_observations":3,
      "existing_general_left_module_preserved":True,
      "right_module_and_unital_conventions_separated":True,
      "mathematical_meanings_added":0,"links_added":0,
      "all_425_previous_term_dispositions_preserved":True,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Screen three module contexts separately after confirming precise additive action and unity axioms; preserve existing independent general-left meaning."
    }
    atomic_json(w.root/"state/wave2_module93_source_intake.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
