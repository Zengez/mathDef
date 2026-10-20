"""Independent real-construction Batch 49: vetted locators and source observations.

This is a mathDef adapter, not generic pipeline logic. The generic Workspace
validates and idempotently ingests reviewed records. No production definitions,
variants, production generated indices, or reconstructed Wave 1 contents are
queried for candidate mathematical knowledge.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from research_pipeline.engine.core import Workspace, PipelineError, canonical, atomic_json, jsonl, digest

WORK = "research_pipeline/experiments/reconstruction-v2-independent"
REVIEW = "wave2/real_constructions_independent_source_reviews_batch_48_2026-10-20.jsonl"
RIGHTS = "wave2/external_source_rights_authority_review_batch49_2026-10-20.jsonl"
LEADS = "wave2/foundation_source_discovery_batch_49.jsonl"
MANIFEST = "wave2/additional_source_lead_batches.json"

# Explicit evidence choices: a theorem about model isomorphism is NOT
# silently converted to another definition. The already screened abstract
# real-number field meaning is NOT overwritten by these set-theoretic models.
CASES = (
 ("review.wave2.real48.dedekind-lower-cut","src.planetmath","https://planetmath.org/dedekindcuts"),
 ("review.wave2.real48.dedekind-real-realization","src.planetmath","https://planetmath.org/dedekindcuts"),
 ("review.wave2.real48.cut-supremum","src.planetmath","https://planetmath.org/dedekindcuts"),
 ("review.wave2.real48.rational-cauchy","src.cornell_math304","https://pi.math.cornell.edu/~web304/reals.pdf"),
 ("review.wave2.real48.cauchy-equivalence","src.libretexts_sloughter","https://math.libretexts.org/Bookshelves/Analysis/A_Primer_of_Real_Analysis_%28Sloughter%29/01%3A_Fundamentals/1.04%3A_Real_Numbers"),
 ("review.wave2.real48.cauchy-class-real","src.csusm_aitken378","https://public.csusm.edu/aitken_html/m378_S2016/Ch9RealNumbers.pdf"),
 ("review.wave2.real48.cauchy-positive","src.csusm_aitken378","https://public.csusm.edu/aitken_html/m378_S2016/Ch9RealNumbers.pdf"),
)

def store(path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8") != content:
        raise PipelineError("Changed previously reviewed batch: "+str(path))
    path.write_text(content,encoding="utf-8")
    return path

def run(workspace=WORK):
    w=Workspace(workspace)
    if not w.config().get("independent_second_wave"):
        raise PipelineError("Requires independent second-wave workspace")
    if any(w.state(x).get("sealed") for x in ("sources","terms","observations","meanings","relations")):
        raise PipelineError("No stage may be sealed")
    prior={"sources":9,"terms":388,"observations":811,"meanings":490,"relations":664}
    after={"sources":14,"terms":395,"observations":818,"meanings":490,"relations":664}
    counts={x:len(w.records(x)) for x in prior}
    if counts not in (prior,after):
        raise PipelineError("Unexpected prior research-stage cardinalities: "+str(counts))
    decisions={r["source_id"]:r for r in jsonl(w.root/RIGHTS)}
    candidates={r["id"]:r for r in jsonl(w.root/REVIEW)}
    if len(decisions)!=5 or len(candidates)!=8:
        raise PipelineError("Batch 48/49 review inventories incomplete")
    for rec in decisions.values():
        if (not rec["authority_reviewed"] or rec["rights_decision"]!="locator_only"
            or rec["source_admission_status"]!="ready_for_independent_locator_only_manifest"
            or rec["access_class"]!="free"):
            raise PipelineError("New-source authority/rights review not ready")
    sources=[]
    for id_,rec in sorted(decisions.items()):
        sources.append({
            "id":id_,"title":rec["title"],"url":rec["url"],
            "authority_reviewed":True,"rights":"locator_only","access":"free",
            "authority_rationale":rec["authority_basis"],"rights_note":rec["publication_license_evidence"],
            "acquisition_policy":rec["allowed"],"rights_review_provenance":RIGHTS,
            "human_verified":False
        })
    termrows=[]; observations=[]; leads=[]
    for n,(rid,sid,url) in enumerate(CASES,1):
        review=candidates[rid]
        if (review["source_primary"]["source_id_existing"] not in (None,sid)
            or review["stage_ingested"] or review["production_corpus_consulted"]):
            raise PipelineError("Mismatched reviewed mathematical evidence: "+rid)
        if review["source_primary"]["url"]!=url:
            raise PipelineError("Reviewed primary locator differs from intake: "+rid)
        tag=f"real49.{n:02d}"
        tid="term.wave2."+tag
        oid="obs.wave2."+tag
        termrows.append({"id":tid,"label":review["candidate_display_term"],
            "locator":url,"source_id":sid,
            "discovery_provenance":REVIEW,"human_verified":False})
        observations.append({"id":oid,"term_id":tid,"source_id":sid,"locator":url,
            "record_kind":"paraphrase","text":review["candidate_formulation"],
            "context":review["candidate_context"],"editorial_note":review["mathematical_review"],
            "reviewed_by":review["reviewed_by"],"human_verified":False,
            "copyright_policy":"Independently formulated mathematics, locator citations only"})
        leads.append({"term_id":tid,"source_id":sid,"locator":url,
            "candidate_observation_id":oid,"source_access_outcome":"direct_page_read",
            "editorial_reason":review["mathematical_review"],
            "source_research_complete":True,"meaning_screened":False,"human_verified":False,
            "review_reference":rid})
    # Validate all IDs and record shapes against a hypothetical in-memory
    # workspace sequence via generic ingest, preserving strict identity.
    source_result=w.ingest("sources",store(w.root/"intake/real49_sources.jsonl",sources),batch_size=5)
    term_result=w.ingest("terms",store(w.root/"intake/real49_terms.jsonl",termrows),batch_size=7)
    obs_result=w.ingest("observations",store(w.root/"intake/real49_observations.jsonl",observations),batch_size=7)
    store(w.root/LEADS,leads)
    path=w.root/MANIFEST
    meta={"schema_version":1,"paths":[LEADS],"purpose":"Future reviewed Wave 2 source-lead batches: append paths, never alter historical batch lists."}
    if path.exists() and json.loads(path.read_text(encoding="utf-8"))!=meta:
        raise PipelineError("Existing supplemental lead manifest differs from reviewed batch")
    atomic_json(path,meta)
    final={x:len(w.records(x)) for x in after}
    if final!=after:
        raise PipelineError("Post-ingest cardinality mismatch: "+str(final))
    report={
       "status":"source_scoped_candidates_only",
       "counts":final,
       "sources_locator_only_added":5,
       "new_source_terms":7,
       "individual_source_observations_added":7,
       "meaning_formulations_screened":0,
       "new_links_screened":0,
       "deferred_theorem": "review.wave2.real48.models-isomorphic",
       "right_to_reproduce_source_text_granted":False,
       "independent_research_only":True,
       "human_peer_verified":False,
       "rights_review_manifest":RIGHTS,
       "batch48_source_reviews":REVIEW,
       "intake_totals":{"sources":source_result,"terms":term_result,"observations":obs_result},
       "all_wave2_stages_unsealed":True,
       "next":"Reconcile 395 individually reviewed term coverage and screen each definition only after source/meaning review, then decide prerequisite links."
    }
    atomic_json(w.root/"state/wave2_real_source_intake_batch49.json",report)
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace",type=Path,default=Path(WORK))
    args=parser.parse_args()
    print(json.dumps(run(args.workspace),indent=2))

if __name__=="__main__":
    main()
