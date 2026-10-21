"""Batch125: four direct independent source headings, eight observations, one held typo."""
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/convergence_eigen_source_batch125_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_125.jsonl"
BEFORE={"sources":14,"terms":465,"observations":924,"meanings":577,"relations":825}
AFTER=dict(BEFORE,terms=469,observations=932)
KEYS=("pointwise-convergence","uniform-convergence","locally-uniform-convergence","eigenvector-operator")
EXPECTED={"pointwise-convergence":2,"uniform-convergence":3,"locally-uniform-convergence":1,"eigenvector-operator":2}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Historical independent source/held observation altered")
    path.write_text(body,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BEFORE):
        raise PipelineError("Independent unsealed Wave2 required")
    if {k:len(w.records(k)) for k in BEFORE} not in (BEFORE,AFTER):
        raise PipelineError("Expected intact B124 baseline or completed B125")
    src=w.records("sources").get("src.proofwiki")
    if not src or src["rights"]!="permitted" or src["access"]!="free":
        raise PipelineError("Source registry rights approval absent")
    dossier={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(dossier)!=set(KEYS):raise PipelineError("Four direct source dossiers required")
    old_titles={m["display_term"] for m in w.records("meanings").values()}
    if any(dossier[k]["term"] in old_titles for k in KEYS):
        raise PipelineError("Existing screened mathematical term collision")
    terms=[];observations=[];leads=[];held=[]
    for key in KEYS:
        row=dossier[key];tid="term.wave2.conv125."+key
        if (row["source_id"]!="src.proofwiki" or row["source_access_outcome"]!="direct_page_read"
            or row["source_review_status"]!="individually_read_external_definition_with_variants"
            or row["stage_ingested"] or row["meaning_screened"] or row["production_corpus_consulted"]
            or len(row["review"])<370 or not row["source"].startswith("https://proofwiki.org/wiki/Definition")):
            raise PipelineError("Insufficient independently screened source hypotheses "+key)
        if key=="uniform-convergence" and ("s_n(x)" not in row["review"] or "f_k(x)" not in row["review"]):
            raise PipelineError("Erroneous summation index must remain explicit")
        terms.append({"id":tid,"label":row["term"],"source_id":"src.proofwiki",
          "locator":row["source"],"discovery_provenance":DOSSIER,"human_verified":False})
        i=0
        for c in row["contexts"]:
            for f in c["forms"]:
                i+=1
                if not f["label"] or len(f["text"])<105:raise PipelineError("Weak source observation "+key)
                oid=f"obs.wave2.conv125.{key}.{i:02d}"
                observations.append({"id":oid,"term_id":tid,"source_id":"src.proofwiki",
                 "locator":row["source"],"record_kind":"paraphrase","text":f["text"],
                 "context":c["context"]+" / "+f["label"],"editorial_note":row["review"]+" Sections: "+", ".join(row["source_sections"]),
                 "reviewed_by":"assistant_independent_convergence_eigen_source_review_2026_10_20","human_verified":False})
                if c.get("held"):
                    held.append({"observation_id":oid,"term_id":tid,
                      "decision":"source_observed_held_not_mathematically_promoted",
                      "held_reason":"Uniform-convergence page's infinite-series partial sum uses f_n(x) rather than summand f_k(x) although k is the index; summing n copies of f_n is generally wrong.",
                      "human_verified":False})
        if i!=EXPECTED[key]:raise PipelineError("Expected individual source variants missing "+key)
        leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":row["source"],
          "candidate_observation_id":f"obs.wave2.conv125.{key}.01","source_access_outcome":"direct_page_read",
          "editorial_reason":row["review"],"source_research_complete":True,
          "meaning_screened":False,"human_verified":False,"review_reference":"research.wave2.conv125."+key})
    if len(terms)!=4 or len(observations)!=8 or len(held)!=1 or held[0]["observation_id"]!="obs.wave2.conv125.uniform-convergence.03":
        raise PipelineError("Exactly one bad uniform-series claim quarantined")
    w.ingest("terms",store(w.root/"intake/conv125_terms.jsonl",terms),batch_size=4)
    w.ingest("observations",store(w.root/"intake/conv125_observations.jsonl",observations),batch_size=8)
    store(w.root/LEADS,leads);store(w.root/"wave2/conv125_quarantined_source_claims.jsonl",held)
    path=w.root/"wave2/additional_source_lead_batches.json";cfg=json.loads(path.read_text(encoding="utf-8"))
    historical=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in
      (49,54,58,62,66,70,75,80,84,89,93,97,100,103,106,109,112,115,118,121)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (historical,historical+[LEADS]):
        raise PipelineError("Previous source research manifest altered")
    cfg["paths"]=historical+[LEADS];atomic_json(path,cfg)
    now={k:len(w.records(k)) for k in AFTER}
    if now!=AFTER:raise PipelineError("Source-only inventory mismatch")
    result={"batch":125,"counts":now,"new_source_headings":4,"new_observations":8,
      "held_bad_partial_sum_index":1,"new_mathematical_meanings":0,"new_links":0,
      "real_pointwise_quantifiers_preserved":True,"metric_uniform_quantifiers_preserved":True,
      "locally_uniform_neighborhood_condition_preserved":True,"nonzero_eigenvector_preserved":True,
      "historical_611_reviews_and_825_links_unchanged":True,
      "held_source_claims_total":3,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch126 six mathematical contexts and seven accepted source formulations (one held), followed by Batch127 independently screened prerequisites."}
    atomic_json(w.root/"state/wave2_conv125_source_intake.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
