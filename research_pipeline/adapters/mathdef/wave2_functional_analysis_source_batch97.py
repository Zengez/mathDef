"""Source-only intake of four independently vetted functional-analysis topics.

The generic engine stays topic independent. Distinct contextual definitions
remain separate source observations for subsequent mathematical screening.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/functional_analysis_metric_source_audit_batch96_2026-10-20.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
LEADS="wave2/foundation_source_discovery_batch_97.jsonl"
BEFORE={"sources":14,"terms":428,"observations":865,"meanings":530,"relations":735}
AFTER=dict(BEFORE,terms=432,observations=872)
KEYS=("metric-space","norm-on-vector-space","normed-vector-space","inner-product-space")
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(row)+"\n" for row in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Historical individual source review differs")
    path.write_text(body,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Must use unsealed independently reconstructed Wave 2")
    if {s:len(w.records(s)) for s in BEFORE} not in (BEFORE,AFTER):
        raise PipelineError("Unexpected prior independent research inventory")
    src=w.records("sources").get("src.proofwiki")
    if not src or src["access"]!="free" or src["rights"]!="permitted":
        raise PipelineError("Approved source rights/access missing")
    research={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(research)!=set(KEYS):
        raise PipelineError("All four source-review dossiers required")
    earlier=w.records("meanings")
    names={r["term"] for r in research.values()}
    if any(m["display_term"] in names for m in earlier.values()):
        raise PipelineError("Existing exact-title mathematical meaning must be reconciled before source promotion")
    terms=[];obs=[];leads=[]
    for key in KEYS:
        r=research[key]
        if (not r["source_access_outcome"]=="direct_page_read"
          or r["stage_ingested"] or r["production_corpus_consulted"] or
          r["source_id"]!="src.proofwiki" or len(r["mathematical_review"])<280
          or len(r["contexts"])<1 or not r["source"].startswith("https://proofwiki.org/wiki/Definition")):
            raise PipelineError("Independently source-reviewed mathematical dossier missing: "+key)
        tid="term.wave2.analysis97."+key
        terms.append({"id":tid,"label":r["term"],"source_id":"src.proofwiki",
          "locator":r["source"],"discovery_provenance":DOSSIER,"human_verified":False})
        i=0
        for context in r["contexts"]:
            for form in context["formulations"]:
                i+=1
                oid=f"obs.wave2.analysis97.{key}.{i:02d}"
                obs.append({"id":oid,"term_id":tid,"source_id":"src.proofwiki",
                   "locator":r["source"],"record_kind":"paraphrase",
                   "text":form["text"],"context":context["context"]+" / "+form["label"],
                   "editorial_note":r["mathematical_review"]+" Sources: "+", ".join(r["source_sections"]),
                   "reviewed_by":"assistant_independent_metric_functional_analysis_source_review_2026_10_20",
                   "human_verified":False})
        if i not in (1,2):
            raise PipelineError("Unexpected source-variant count for "+key)
        leads.append({"term_id":tid,"source_id":"src.proofwiki",
          "locator":r["source"],"candidate_observation_id":f"obs.wave2.analysis97.{key}.01",
          "source_access_outcome":"direct_page_read",
          "editorial_reason":r["mathematical_review"],
          "source_research_complete":True,"meaning_screened":False,
          "human_verified":False,"review_reference":"research.wave2.analysis96."+key})
    if len(terms)!=4 or len(obs)!=7:
        raise PipelineError("Expected four source terms and seven independent formulations")
    w.ingest("terms",store(w.root/"intake/analysis97_terms.jsonl",terms),batch_size=4)
    w.ingest("observations",store(w.root/"intake/analysis97_observations.jsonl",obs),batch_size=7)
    store(w.root/LEADS,leads)
    path=w.root/MANIFEST
    cfg=json.loads(path.read_text(encoding="utf-8"))
    old=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in (49,54,58,62,66,70,75,80,84,89,93)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (old,old+[LEADS]):
        raise PipelineError("Historical supplemental source manifest mutated")
    cfg["paths"]=old+[LEADS]
    atomic_json(path,cfg)
    counts={s:len(w.records(s)) for s in AFTER}
    if counts!=AFTER:
        raise PipelineError("Independent source counts changed")
    report={
       "batch":97,"counts":counts,"new_source_terms":4,"new_source_observations":7,
       "screened_new_meanings":0,"new_links":0,
       "metric_nonempty_source_scope_preserved":True,
       "real_complex_inner_product_contexts_distinguished":True,
       "normed_division_ring_generality_preserved":True,
       "previous_428_term_decisions_preserved":True,
       "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
       "next":"Review six contextual mathematical meanings with seven formulations; check metric equivalent descriptions and real/complex inner products; individually screen prerequisites only after meanings."
    }
    atomic_json(w.root/"state/wave2_analysis97_source_intake.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
