"""Source-only intake of four independently researched set-theoretic foundations.

MathDef adapter; portable operations remain in Workspace and coverage engine.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
REVIEW="wave2/foundational_set_theory_sources_batch61_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_62.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
BEFORE={"sources":14,"terms":402,"observations":826,"meanings":503,"relations":681}
AFTER=dict(BEFORE,terms=406,observations=830)
URLS={
 "natural-numbers":"https://proofwiki.org/wiki/Definition%3ANatural_Number",
 "equivalence-relation":"https://proofwiki.org/wiki/Definition%3AEquivalence_Relation",
 "equivalence-class":"https://proofwiki.org/wiki/Definition%3AEquivalence_Class",
 "quotient-set":"https://proofwiki.org/wiki/Definition%3AQuotient_Set"
}
def store(path,records):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(r)+"\n" for r in records)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Existing independently sourced Batch 62 records differ")
    path.write_text(content,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BEFORE):
        raise PipelineError("Requires unsealed independent research corpus")
    counts={k:len(w.records(k)) for k in BEFORE}
    if counts not in (BEFORE,AFTER):
        raise PipelineError("Unexpected prior independent stage count "+str(counts))
    s=w.records("sources").get("src.proofwiki")
    if not s or s["access"]!="free" or s["rights"]!="permitted":
        raise PipelineError("Independent source not vetted")
    research={r["key"]:r for r in jsonl(w.root/REVIEW)}
    if set(research)!=set(URLS) or len(research)!=4:
        raise PipelineError("Four independent source audits required")
    termrows=[];obrows=[];leads=[]
    for key,url in URLS.items():
        r=research[key]
        if (r["source"]!=url or r["source_id"]!="src.proofwiki"
            or r["source_access_outcome"]!="direct_page_read"
            or r["meaning_screened"] or r["stage_ingested"] or r["production_corpus_used"]
            or len(r["review"])<150 or len(r["definition"])<95):
            raise PipelineError("Individual mathematical source audit missing: "+key)
        term="term.wave2.set62."+key
        obs="obs.wave2.set62."+key
        termrows.append({
          "id":term,"label":r["term"],"source_id":"src.proofwiki",
          "locator":url,"discovery_provenance":REVIEW,"human_verified":False
        })
        obrows.append({
          "id":obs,"term_id":term,"source_id":"src.proofwiki",
          "locator":url,"record_kind":"paraphrase","text":r["definition"],
          "context":r["context"],"editorial_note":r["review"],
          "reviewed_by":"assistant_independent_set_fundamentals_source_review_2026_10_20",
          "human_verified":False
        })
        leads.append({
          "term_id":term,"source_id":"src.proofwiki","locator":url,
          "candidate_observation_id":obs,"source_access_outcome":"direct_page_read",
          "editorial_reason":r["review"],"source_research_complete":True,
          "meaning_screened":False,"human_verified":False,
          "review_reference":r["review_id"]
        })
    w.ingest("terms",store(w.root/"intake/set_foundations_terms_batch62.jsonl",termrows),batch_size=4)
    w.ingest("observations",store(w.root/"intake/set_foundations_observations_batch62.jsonl",obrows),batch_size=4)
    store(w.root/LEADS,leads)
    m=w.root/MANIFEST
    config=json.loads(m.read_text(encoding="utf-8"))
    paths=[
      "wave2/foundation_source_discovery_batch_49.jsonl",
      "wave2/foundation_source_discovery_batch_54.jsonl",
      "wave2/foundation_source_discovery_batch_58.jsonl"
    ]
    if config.get("schema_version")!=1 or config.get("paths") not in (paths,paths+[LEADS]):
        raise PipelineError("Supplementary source lead manifest moved without a review")
    config["paths"]=paths+[LEADS]
    atomic_json(m,config)
    final={k:len(w.records(k)) for k in AFTER}
    if final!=AFTER:
        raise PipelineError("Unexpected new mathematical source counts")
    report={
      "batch":62,"counts":final,"added_source_terms":4,"added_source_observations":4,
      "new_screened_meanings":0,"new_screened_relations":0,
      "zero_in_natural_numbers_convention_recorded":True,
      "equivalence_class_not_identified_with_quotient_set":True,
      "reviewed_proofwiki_source_only":True,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Individually screen four meanings with complete 516-formulation review history, then audit noncircular integer-construction links."
    }
    atomic_json(w.root/"state/wave2_set_source_intake_batch62.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    args=p.parse_args()
    print(json.dumps(run(args.workspace),indent=2))

if __name__=="__main__":
    main()
