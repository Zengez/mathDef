"""Batch 66: independent source observations for measure/topology variants.

This adapter does not read original mathDef mathematical content. Existing
independent meanings are inspected for identity collisions before admission.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
REVIEW="wave2/broad_source_variant_reviews_batch65_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_66.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
BEFORE={"sources":14,"terms":406,"observations":830,"meanings":508,"relations":691}
AFTER=dict(BEFORE,terms=408,observations=834)
TOPICS={
 "sigma-algebra":("wave2.batch65.sigma-algebra","https://proofwiki.org/wiki/Definition%3ASigma_Algebra"),
 "compact-space":("wave2.batch65.compact-space","https://proofwiki.org/wiki/Definition%3ACompact_Topological_Space")
}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    payload="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=payload:
        raise PipelineError("Previously reviewed independent source evidence differs")
    path.write_text(payload,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Independent unsealed Wave 2 required")
    if {s:len(w.records(s)) for s in BEFORE} not in (BEFORE,AFTER):
        raise PipelineError("Unexpected source-stage baseline")
    source=w.records("sources").get("src.proofwiki")
    if not source or source["rights"]!="permitted" or source["access"]!="free":
        raise PipelineError("Independent source not approved")
    meanings=w.records("meanings")
    sigma=meanings.get("meaning.wave2.foundation.sigma-algebra")
    quasi=meanings.get("meaning.27eb121021fd989d.quasicompact-space")
    if (not sigma or sigma["term_group_id"]!="wave2.foundation.sigma-algebra"
        or not quasi or quasi["display_term"]!="quasicompact space"):
        raise PipelineError("Existing screened collision contexts were not resolved")
    review={x["id"]:x for x in jsonl(w.root/REVIEW)}
    if len(review)!=2:
        raise PipelineError("Two individual cross-field variant review dossiers required")
    terms=[];observations=[];leads=[]
    for key,(rid,url) in TOPICS.items():
        rec=review.get(rid)
        if (not rec or rec["source_locator"]!=url or rec["source_id"]!="src.proofwiki"
            or rec["production_corpus_consulted"] or rec["stage_ingested"]
            or rec["source_access_outcome"]!="direct_page_read"
            or len(rec["mathematical_review"])<260 or len(rec["formulations"])!=2):
            raise PipelineError("Source-scoped alternative formulations not verified: "+key)
        term="term.wave2.broad66."+key
        terms.append({"id":term,"label":rec["term"],"source_id":"src.proofwiki",
                      "locator":url,"discovery_provenance":REVIEW,"human_verified":False})
        for i,form in enumerate(rec["formulations"],1):
            observations.append({
              "id":f"obs.wave2.broad66.{key}.{i:02d}","term_id":term,
              "source_id":"src.proofwiki","locator":url,"record_kind":"paraphrase",
              "text":form["text"],"context":rec["domain"]+" / "+form["variant"],
              "editorial_note":rec["mathematical_review"]+" Source section: "+form["source_section"],
              "reviewed_by":"assistant_independent_cross_domain_variant_review_2026_10_20",
              "human_verified":False
            })
        leads.append({
           "term_id":term,"source_id":"src.proofwiki","locator":url,
           "candidate_observation_id":f"obs.wave2.broad66.{key}.01",
           "source_access_outcome":"direct_page_read",
           "editorial_reason":rec["mathematical_review"],
           "source_research_complete":True,"meaning_screened":False,
           "human_verified":False,"review_reference":rid
        })
    w.ingest("terms",store(w.root/"intake/broad_variants_terms_batch66.jsonl",terms),batch_size=2)
    w.ingest("observations",store(w.root/"intake/broad_variants_observations_batch66.jsonl",observations),batch_size=4)
    store(w.root/LEADS,leads)
    path=w.root/MANIFEST
    cfg=json.loads(path.read_text(encoding="utf-8"))
    existing=["wave2/foundation_source_discovery_batch_"+str(i)+".jsonl" for i in (49,54,58,62)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (existing,existing+[LEADS]):
        raise PipelineError("Supplemental reviewed-lead manifest changed")
    cfg["paths"]=existing+[LEADS]
    atomic_json(path,cfg)
    final={s:len(w.records(s)) for s in AFTER}
    if final!=AFTER:
        raise PipelineError("Unexpected source evidence totals")
    report={
       "batch":66,"counts":final,"terms_added":2,"formulation_observations_added":4,
       "screened_meanings_added":0,"links_added":0,
       "sigma_algebra_existing_meaning_detected":True,
       "quasi_compact_existing_context_detected":True,
       "explicit_formulation_level_source_provenance":True,
       "original_production_mathdef_used":False,"human_peer_verified":False,
       "all_stages_unsealed":True,
       "next":"Amend existing sigma-algebra meaning with a mathematically equivalent new formulation, separately screen named compact topological space with two formulations, preserving all old 521 reviewed formulation dispositions."
    }
    atomic_json(w.root/"state/wave2_broad_source_batch66.json",report)
    return report
def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(a.parse_args().workspace),indent=2))
if __name__=="__main__":main()
