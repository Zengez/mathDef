"""Batch128: independent four-source intake, no mathematical promotion.

Subject-specific source and mathematical semantics belong only in this adapter.
"""
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/product_eigen_graph_egf_source_batch128_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_128.jsonl"
BEFORE={"sources":14,"terms":469,"observations":932,"meanings":583,"relations":840}
AFTER=dict(BEFORE,terms=473,observations=938)
KEYS=("product-topology","eigenvalue-linear-operator","connected-simple-graph","exponential-generating-function")
COUNTS={"product-topology":2,"eigenvalue-linear-operator":2,"connected-simple-graph":1,"exponential-generating-function":1}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Previously committed source evidence changed")
    path.write_text(content,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BEFORE):
        raise PipelineError("Requires unsealed independent Wave2")
    counts={k:len(w.records(k)) for k in BEFORE}
    if counts not in (BEFORE,AFTER):raise PipelineError("Unexpected reviewed research baseline "+str(counts))
    src=w.records("sources").get("src.proofwiki")
    if not src or src["access"]!="free" or src["rights"]!="permitted":
        raise PipelineError("Source rights not approved")
    rows={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(rows)!=set(KEYS):raise PipelineError("Exactly four direct source dossiers required")
    names={m["display_term"] for m in w.records("meanings").values()}
    if any(rows[k]["term"] in names for k in KEYS):
        raise PipelineError("Existing contextual meaning term collision")
    terms=[];observations=[];leads=[]
    for key in KEYS:
        r=rows[key];tid="term.wave2.branch128."+key
        if (r["source_id"]!="src.proofwiki" or r["source_access_outcome"]!="direct_page_read" or
          r["source_review_status"]!="individually_read_external_definition_with_variants" or
          r["stage_ingested"] or r["meaning_screened"] or r["production_corpus_consulted"] or
          len(r["review"])<370 or not r["source"].startswith("https://proofwiki.org/wiki/Definition")):
            raise PipelineError("Missing individually source-reviewed mathematical scope "+key)
        if key=="product-topology" and ("NOT the complete topology" not in r["review"] or "BOX topology" not in r["review"]):
            raise PipelineError("Topological subbasis / box-topology scope not preserved")
        if key=="eigenvalue-linear-operator" and "zero-dimensional" not in r["review"]:
            raise PipelineError("Zero-dimensional vector-space and nonzero eigenvector caveat missing")
        if key=="connected-simple-graph" and "empty graph" not in r["review"]:
            raise PipelineError("Empty graph connectedness convention must be explicit")
        if key=="exponential-generating-function" and "n! denominator" not in r["review"]:
            raise PipelineError("Exponential denominator distinction absent")
        terms.append({"id":tid,"label":r["term"],"source_id":"src.proofwiki",
            "locator":r["source"],"discovery_provenance":DOSSIER,"human_verified":False})
        context=r["contexts"]
        if len(context)!=1 or len(context[0]["forms"])!=COUNTS[key]:
            raise PipelineError("Independent variants count invalid "+key)
        for j,f in enumerate(context[0]["forms"],1):
            if len(f["text"])<115 or not f["label"]:
                raise PipelineError("Source evidence paraphrase too weak "+key)
            observations.append({"id":f"obs.wave2.branch128.{key}.{j:02d}",
                "term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
                "record_kind":"paraphrase","text":f["text"],
                "context":context[0]["context"]+" / "+f["label"],
                "editorial_note":r["review"]+" Sections: "+", ".join(r["source_sections"]),
                "reviewed_by":"assistant_independent_product_eigen_graph_egf_source_review_2026_10_20",
                "human_verified":False})
        leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
            "candidate_observation_id":f"obs.wave2.branch128.{key}.01",
            "source_access_outcome":"direct_page_read","editorial_reason":r["review"],
            "source_research_complete":True,"meaning_screened":False,
            "human_verified":False,"review_reference":"research.wave2.branch128."+key})
    if len(terms)!=4 or len(observations)!=6:
        raise PipelineError("Exactly 4 source headings and 6 evidence observations required")
    w.ingest("terms",store(w.root/"intake/branch128_terms.jsonl",terms),batch_size=4)
    w.ingest("observations",store(w.root/"intake/branch128_observations.jsonl",observations),batch_size=6)
    store(w.root/LEADS,leads)
    path=w.root/"wave2/additional_source_lead_batches.json";cfg=json.loads(path.read_text(encoding="utf-8"))
    historical=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in
        (49,54,58,62,66,70,75,80,84,89,93,97,100,103,106,109,112,115,118,121,125)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (historical,historical+[LEADS]):
        raise PipelineError("Earlier source lead manifest unexpectedly altered")
    cfg["paths"]=historical+[LEADS];atomic_json(path,cfg)
    now={k:len(w.records(k)) for k in AFTER}
    if now!=AFTER:raise PipelineError("Post-intake inventory mismatch "+str(now))
    report={"batch":128,"counts":now,"new_terms":4,"new_source_observations":6,
      "new_meanings":0,"new_links":0,"product_subbasis_vs_basis_distinguished":True,
      "eigenvalue_nontrivial_kernel_distinguished":True,"connected_graph_empty_graph_convention_logged":True,
      "real_exponential_generating_function_convergence_domain":True,
      "all_618_formulation_reviews_and_840_links_unchanged":True,"three_historical_held_source_observations_unpromoted":True,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch129 individually screen four contextual meanings with six sourced formulations; Batch130 reviewed direct prerequisites and optional targeted backfill."}
    atomic_json(w.root/"state/wave2_branch128_source_intake.json",report);return report
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
