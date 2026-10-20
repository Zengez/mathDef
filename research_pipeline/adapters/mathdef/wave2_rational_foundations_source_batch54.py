"""Batch 54: source-only intake of independently researched rational foundations.

Generic Workspace handles ingestion; topic-specific choices stay here.
Does not read original production mathDef definitions, site, or citations.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json

WORK="research_pipeline/experiments/reconstruction-v2-independent"
RESEARCH="wave2/rational_foundations_source_review_batch54_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_54.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
START={"sources":14,"terms":395,"observations":818,"meanings":496,"relations":670}
DONE=dict(START,terms=399,observations=822)
EXPECTED={
 "rational-number":"https://proofwiki.org/wiki/Definition%3ARational_Number",
 "rational-sequence":"https://proofwiki.org/wiki/Definition%3ARational_Sequence",
 "rational-absolute-value":"https://proofwiki.org/wiki/Definition%3AAbsolute_Value/Ordered_Integral_Domain",
 "strictly-positive-rational":"https://proofwiki.org/wiki/Definition%3AStrictly_Positive_Rational_Number"
}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Changed prior individually source-reviewed batch: "+str(path))
    path.write_text(body,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in START):
        raise PipelineError("Independent unsealed Wave 2 required")
    current={s:len(w.records(s)) for s in START}
    if current not in (START,DONE):
        raise PipelineError("Unexpected rational source stage counts: "+str(current))
    existing_sources=w.records("sources")
    if (existing_sources.get("src.proofwiki",{}).get("rights")!="permitted"
         or existing_sources["src.proofwiki"]["access"]!="free"):
        raise PipelineError("Expected vetted public reference missing")
    data=jsonl(w.root/RESEARCH)
    keyed={r["id"]:r for r in data}
    if len(data)!=4 or set(keyed)!=set(EXPECTED):
        raise PipelineError("Exactly four individually researched rational foundations required")
    terms=[]; observations=[]; leads=[]
    for name,url in EXPECTED.items():
        x=keyed[name]
        if (x["source_url"]!=url or x["source_id"]!="src.proofwiki"
            or x["stage_ingested"] or x["meaning_screened"]
            or x["production_corpus_consulted"] or not x["source_review_complete"]
            or x["source_access_outcome"]!="direct_page_read"
            or len(x["reason"])<170):
            raise PipelineError("Source/rights/mathematical review not complete: "+name)
        tid="term.wave2.rational54."+name
        oid="obs.wave2.rational54."+name
        terms.append({
            "id":tid,"label":x["term"],"locator":url,
            "source_id":"src.proofwiki","discovery_provenance":RESEARCH,
            "human_verified":False})
        observations.append({
            "id":oid,"term_id":tid,"source_id":"src.proofwiki",
            "locator":url,"record_kind":"paraphrase","text":x["text"],
            "context":x["context"],"editorial_note":x["reason"],
            "source_crosscheck_urls":[x["secondary_url"]] if x.get("secondary_url") else [],
            "reviewed_by":x["reviewed_by"],"human_verified":False})
        leads.append({
            "term_id":tid,"source_id":"src.proofwiki","locator":url,
            "candidate_observation_id":oid,"source_access_outcome":"direct_page_read",
            "editorial_reason":x["reason"],"source_research_complete":True,
            "meaning_screened":False,"human_verified":False,
            "review_reference":x["review_id"]})
    t=w.ingest("terms",store(w.root/"intake/foundations_batch54_terms.jsonl",terms),batch_size=4)
    o=w.ingest("observations",store(w.root/"intake/foundations_batch54_observations.jsonl",observations),batch_size=4)
    store(w.root/LEADS,leads)
    manifest=w.root/MANIFEST
    prev=json.loads(manifest.read_text(encoding="utf-8"))
    if prev.get("schema_version")!=1 or prev.get("paths") not in (
        ["wave2/foundation_source_discovery_batch_49.jsonl"],
        ["wave2/foundation_source_discovery_batch_49.jsonl",LEADS]):
        raise PipelineError("Unexpected prior source-lead manifest")
    prev["paths"]=["wave2/foundation_source_discovery_batch_49.jsonl",LEADS]
    atomic_json(manifest,prev)
    final={s:len(w.records(s)) for s in DONE}
    if final!=DONE:
        raise PipelineError("Source intake changed expected research inventories")
    report={
      "phase":"four_independent_rational_source_observations_not_meanings",
      "counts":final,"new_source_terms":4,"new_source_observations":4,
      "existing_14_sources_reused":True,"new_meanings_screened":0,
      "new_relations_screened":0,"term_intake":t,"observation_intake":o,
      "strict_positive_not_conflated_with_nonnegative":True,
      "reals_not_assumed_to_exist":True,"all_stages_unsealed":True,
      "human_peer_verified":False,"original_production_mathdef_consulted":False,
      "next":"Individually screen four mathematical meanings and migrate complete 508-formulation review ledger; then revisit formerly unsupported Cauchy prerequisites."}
    atomic_json(w.root/"state/wave2_rational_source_intake_batch54.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(WORK))
    a=p.parse_args()
    print(json.dumps(run(a.workspace),indent=2))

if __name__=="__main__":
    main()
