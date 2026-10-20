"""Independent Batch118 source-only intake and explicit graph-isomorphism source hold."""
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/quotient_graph_generating_source_batch118_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_118.jsonl"
BASE={"sources":14,"terms":457,"observations":912,"meanings":568,"relations":803}
AFTER=dict(BASE,terms=461,observations=919)
KEYS=("normal-subgroup","quotient-group","graph-isomorphism","ordinary-generating-function")
N={"normal-subgroup":3,"quotient-group":1,"graph-isomorphism":2,"ordinary-generating-function":1}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    data="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=data:
        raise PipelineError("Historical source or held mathematical claim differs")
    path.write_text(data,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BASE):
        raise PipelineError("Requires independent unsealed Wave2")
    if {s:len(w.records(s)) for s in BASE} not in (BASE,AFTER):
        raise PipelineError("Reviewed baseline mismatch")
    src=w.records("sources").get("src.proofwiki")
    if not src or src["access"]!="free" or src["rights"]!="permitted":
        raise PipelineError("Approved direct independent ProofWiki source unavailable")
    data={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(data)!=set(KEYS):raise PipelineError("Four exact source dossiers absent")
    existing={m["display_term"] for m in w.records("meanings").values()}
    if any(data[k]["term"] in existing for k in KEYS):
        raise PipelineError("Exact term collision with existing screened meaning")
    terms=[];obs=[];leads=[];held=[]
    for key in KEYS:
        r=data[key];tid="term.wave2.quot118."+key
        if (r["source_id"]!="src.proofwiki" or r["source_access_outcome"]!="direct_page_read"
            or r["stage_ingested"] or r["meaning_screened"] or r["production_corpus_consulted"]
            or not r["source"].startswith("https://proofwiki.org/wiki/Definition")
            or len(r["review"])<340):
            raise PipelineError("Incomplete independently source-reviewed claim "+key)
        if key=="graph-isomorphism" and ("Counterexample" not in r["review"] or not r["contexts"][1].get("held")):
            raise PipelineError("Invalid forward-only graph source clause must be quarantined")
        if key=="ordinary-generating-function" and "CONVERGES" not in r["review"]:
            raise PipelineError("Analytic generating function convergence scope omitted")
        terms.append({"id":tid,"label":r["term"],"source_id":"src.proofwiki",
            "locator":r["source"],"discovery_provenance":DOSSIER,"human_verified":False})
        i=0
        for c in r["contexts"]:
            for f in c["forms"]:
                i+=1
                if not f["label"] or len(f["text"])<100:
                    raise PipelineError("Incomplete individual mathematical observation "+key)
                oid=f"obs.wave2.quot118.{key}.{i:02d}"
                obs.append({"id":oid,"term_id":tid,"source_id":"src.proofwiki",
                    "locator":r["source"],"record_kind":"paraphrase",
                    "text":f["text"],"context":c["context"]+" / "+f["label"],
                    "editorial_note":r["review"]+" Source sections: "+", ".join(r["source_sections"]),
                    "reviewed_by":"assistant_independent_quotient_graph_generating_source_review_2026_10_20",
                    "human_verified":False})
                if c.get("held"):
                    held.append({"observation_id":oid,"term_id":tid,
                        "decision":"source_observed_held_not_mathematically_promoted",
                        "held_reason":"Bijection with only forward edge preservation does not reflect edges; graph-isomorphism source calls it equivalent to the two-direction condition, with explicit 3-vertex counterexample in dossier.",
                        "human_verified":False})
        if i!=N[key]:raise PipelineError("Individually source-observed variants mismatch "+key)
        leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
            "candidate_observation_id":f"obs.wave2.quot118.{key}.01",
            "source_access_outcome":"direct_page_read","editorial_reason":r["review"],
            "source_research_complete":True,"meaning_screened":False,
            "human_verified":False,"review_reference":"research.wave2.quot118."+key})
    if len(terms)!=4 or len(obs)!=7 or len(held)!=1 or held[0]["observation_id"]!="obs.wave2.quot118.graph-isomorphism.02":
        raise PipelineError("Expected four headings seven observations and one specific held error")
    w.ingest("terms",store(w.root/"intake/quot118_terms.jsonl",terms),batch_size=4)
    w.ingest("observations",store(w.root/"intake/quot118_observations.jsonl",obs),batch_size=7)
    store(w.root/LEADS,leads)
    store(w.root/"wave2/quot118_quarantined_source_claims.jsonl",held)
    cfgfile=w.root/"wave2/additional_source_lead_batches.json"
    cfg=json.loads(cfgfile.read_text(encoding="utf-8"))
    historic=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in
        (49,54,58,62,66,70,75,80,84,89,93,97,100,103,106,109,112,115)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (historic,historic+[LEADS]):
        raise PipelineError("Historical independent source batches changed")
    cfg["paths"]=historic+[LEADS];atomic_json(cfgfile,cfg)
    counts={s:len(w.records(s)) for s in AFTER}
    if counts!=AFTER:raise PipelineError("Expected source-only inventory mismatch")
    report={"batch":118,"counts":counts,"new_terms":4,"new_source_observations":7,
        "quarantined_source_claims_this_batch":1,
        "new_mathematical_meanings":0,"new_mathematical_links":0,
        "graph_forward_only_not_promoted":True,"normal_subgroup_three_equivalent_presentations":True,
        "quotient_requires_normality":True,"convergent_generating_function_not_formal":True,
        "historic_600_formulation_decisions_and_803_links_unchanged":True,
        "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
        "next":"Batch119 source-specific mathematical screens for four contexts/six formulations, held graph source excluded. Batch120 direct screened prerequisites."}
    atomic_json(w.root/"state/wave2_quot118_source_intake.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
