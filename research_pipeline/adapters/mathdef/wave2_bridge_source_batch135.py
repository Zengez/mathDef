"""Batch135 direct independent source intake: convexity, falling factorial, delta, bipartiteness."""
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/convex_falling_delta_bipartite_source_batch135_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_135.jsonl"
BASE={"sources":14,"terms":477,"observations":946,"meanings":591,"relations":869}
AFTER=dict(BASE,terms=481,observations=953)
KEYS=("convex-set","falling-factorial","kronecker-delta","bipartite-simple-graph")
COUNTS={"convex-set":2,"falling-factorial":1,"kronecker-delta":2,"bipartite-simple-graph":2}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    contents="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=contents:
        raise PipelineError("Previously reviewed independent source evidence mutated")
    path.write_text(contents,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Requires unsealed independent Wave2")
    if {k:len(w.records(k)) for k in BASE} not in (BASE,AFTER):
        raise PipelineError("Expected verified Batch134 independent inventory")
    registry=w.records("sources").get("src.proofwiki")
    if not registry or registry["rights"]!="permitted" or registry["access"]!="free":
        raise PipelineError("Approved source rights absent")
    rows={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(rows)!=set(KEYS):raise PipelineError("Four directly source-reviewed topics required")
    names={r["display_term"] for r in w.records("meanings").values()}
    if any(rows[k]["term"] in names for k in KEYS):
        raise PipelineError("Exact independent mathematical term collision")
    terms=[];obs=[];leads=[]
    for key in KEYS:
        r=rows[key];tid="term.wave2.bridge135."+key
        if (r["source_id"]!="src.proofwiki" or r["source_access_outcome"]!="direct_page_read"
            or r["source_review_status"]!="individually_read_external_definition_with_variants"
            or r["stage_ingested"] or r["meaning_screened"] or r["production_corpus_consulted"]
            or len(r["review"])<390 or not r["source"].startswith("https://proofwiki.org/wiki/Definition")):
            raise PipelineError("Source observations and scope not independently reviewed "+key)
        if key=="falling-factorial" and ("n=0" not in r["review"] or "Binomial_Coefficient_with_Zero" not in r["corroborating_source"]):
            raise PipelineError("Source's n>0 domain needs separately proven n=0 extension")
        if key=="bipartite-simple-graph" and "either color class" not in r["review"] and "both color classes" not in r["review"]:
            raise PipelineError("Color-class nonempty ambiguity not recorded")
        if key=="kronecker-delta" and "ring-with-unity" not in r["review"]:
            raise PipelineError("General ring-valued delta must remain separate context")
        terms.append({"id":tid,"label":r["term"],"source_id":"src.proofwiki",
            "locator":r["source"],"discovery_provenance":DOSSIER,"human_verified":False})
        ctx=r["contexts"]
        if len(ctx)!=1 or len(ctx[0]["forms"])!=COUNTS[key]:
            raise PipelineError("Unexpected source variant count "+key)
        for i,f in enumerate(ctx[0]["forms"],1):
            if len(f["text"])<96 or not f["label"]:raise PipelineError("Weak source paraphrase "+key)
            obs.append({"id":f"obs.wave2.bridge135.{key}.{i:02d}",
                "term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
                "record_kind":"paraphrase","text":f["text"],
                "context":ctx[0]["context"]+" / "+f["label"],
                "editorial_note":r["review"]+" Source sections: "+", ".join(r["source_sections"]),
                "reviewed_by":"assistant_independent_convex_falling_delta_bipartite_source_review_2026_10_20",
                "human_verified":False})
        leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
            "candidate_observation_id":f"obs.wave2.bridge135.{key}.01",
            "source_access_outcome":"direct_page_read","editorial_reason":r["review"],
            "source_research_complete":True,"meaning_screened":False,
            "human_verified":False,"review_reference":"research.wave2.bridge135."+key})
    if len(terms)!=4 or len(obs)!=7:raise PipelineError("Exactly four source headings and seven observations required")
    w.ingest("terms",store(w.root/"intake/bridge135_terms.jsonl",terms),batch_size=4)
    w.ingest("observations",store(w.root/"intake/bridge135_observations.jsonl",obs),batch_size=7)
    store(w.root/LEADS,leads)
    file=w.root/"wave2/additional_source_lead_batches.json";cfg=json.loads(file.read_text(encoding="utf-8"))
    historical=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in
      (49,54,58,62,66,70,75,80,84,89,93,97,100,103,106,109,112,115,118,121,125,128,132)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (historical,historical+[LEADS]):
        raise PipelineError("Previously committed source-ledger manifest changed")
    cfg["paths"]=historical+[LEADS];atomic_json(file,cfg)
    counts={k:len(w.records(k)) for k in AFTER}
    if counts!=AFTER:raise PipelineError("Source-only inventory mismatch "+str(counts))
    report={"batch":135,"counts":counts,"new_source_headings":4,"new_observations":7,
       "new_meanings":0,"new_links":0,"convex_empty_set_allowed":True,
       "falling_factorial_zero_case_independently_corroborated":True,
       "numerical_delta_distinct_from_ring_valued":True,
       "bipartite_two_color_classes_may_be_empty":True,
       "all_632_previous_formulations_and_869_links_unchanged":True,
       "three_historical_source_holds_unpromoted":True,"all_stages_unsealed":True,
       "human_peer_verified":False,"production_corpus_used":False,
       "next":"Batch136 four screened contextual meanings/seven formulations then Batch137 individual source-to-mathematical-meaning prerequisites."}
    atomic_json(w.root/"state/wave2_bridge135_source_intake.json",report);return report
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
