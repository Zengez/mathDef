"""Batch 103: source-only intake of four distinct cross-field definition topics.

Preserves independent mathematical review inventories. Generic research engine
remains domain neutral; math-specific variants and provenance reside here.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/cross_field_source_variants_batch103_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_103.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
BASE={"sources":14,"terms":437,"observations":877,"meanings":541,"relations":754}
AFTER=dict(BASE,terms=441,observations=884)
KEYS=("lipschitz-continuity","tree-graph","independent-sigma-algebras","independent-random-variables")
EXPECTED_CONTEXTS={"lipschitz-continuity":2,"tree-graph":1,"independent-sigma-algebras":2,"independent-random-variables":1}
EXPECTED_FORMS={"lipschitz-continuity":2,"tree-graph":2,"independent-sigma-algebras":2,"independent-random-variables":1}

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Historical source/variant intake differs")
    path.write_text(content,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(stage).get("sealed") for stage in BASE):
        raise PipelineError("Requires independent and unsealed Wave 2")
    current={s:len(w.records(s)) for s in BASE}
    if current not in (BASE,AFTER):
        raise PipelineError("Unexpected independently screened research baseline: "+str(current))
    source=w.records("sources").get("src.proofwiki")
    if not source or source["rights"]!="permitted" or source["access"]!="free":
        raise PipelineError("Approved direct source rights unavailable")
    research={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(research)!=set(KEYS):
        raise PipelineError("Four exact individual source-variant dossiers missing")
    meanings=w.records("meanings")
    if any(m["display_term"] in {r["term"] for r in research.values()} for m in meanings.values()):
        raise PipelineError("Exact displayed meaning title already exists; source-only reconciliation required")
    terms=[];obs=[];leads=[]
    for key in KEYS:
        record=research[key]
        if (record.get("source_review_status")!="individually_read_external_definition_with_variants"
            or record["source_access_outcome"]!="direct_page_read"
            or record["source_id"]!="src.proofwiki"
            or record["stage_ingested"] or record["meaning_screened"] or record["production_corpus_consulted"]
            or len(record["mathematical_review"])<280
            or not record["source"].startswith("https://proofwiki.org/wiki/Definition")
            or len(record["contexts"])!=EXPECTED_CONTEXTS[key]):
            raise PipelineError("Insufficient source-specific scope or provenance: "+key)
        tid="term.wave2.cross103."+key
        terms.append({"id":tid,"label":record["term"],"source_id":"src.proofwiki",
             "locator":record["source"],"discovery_provenance":DOSSIER,"human_verified":False})
        i=0
        for context in record["contexts"]:
            for variant in context["formulations"]:
                i+=1
                if len(variant["text"])<75 or not variant["label"]:
                    raise PipelineError("Unreviewed individual formulation for "+key)
                obs.append({
                    "id":f"obs.wave2.cross103.{key}.{i:02d}",
                    "term_id":tid,"source_id":"src.proofwiki",
                    "locator":record["source"],"record_kind":"paraphrase",
                    "text":variant["text"],"context":context["context"]+" / "+variant["label"],
                    "editorial_note":record["mathematical_review"]+" Sections: "+", ".join(record["source_sections"]),
                    "reviewed_by":"assistant_independent_cross_field_source_variant_review_2026_10_20",
                    "human_verified":False})
        if i!=EXPECTED_FORMS[key]:
            raise PipelineError("Variant count mismatch "+key)
        leads.append({
            "term_id":tid,"source_id":"src.proofwiki","locator":record["source"],
            "candidate_observation_id":f"obs.wave2.cross103.{key}.01",
            "source_access_outcome":"direct_page_read",
            "editorial_reason":record["mathematical_review"],
            "source_research_complete":True,"meaning_screened":False,
            "human_verified":False,"review_reference":"research.wave2.cross103."+key})
    if len(terms)!=4 or len(obs)!=7:
        raise PipelineError("Expected 4 distinct source terms and 7 individual observations")
    w.ingest("terms",store(w.root/"intake/cross103_terms.jsonl",terms),batch_size=4)
    w.ingest("observations",store(w.root/"intake/cross103_observations.jsonl",obs),batch_size=7)
    store(w.root/LEADS,leads)
    cfgfile=w.root/MANIFEST
    cfg=json.loads(cfgfile.read_text(encoding="utf-8"))
    old=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in (49,54,58,62,66,70,75,80,84,89,93,97,100)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (old,old+[LEADS]):
        raise PipelineError("Historical source-review discovery manifest mutated")
    cfg["paths"]=old+[LEADS]
    atomic_json(cfgfile,cfg)
    counts={s:len(w.records(s)) for s in AFTER}
    if counts!=AFTER:
        raise PipelineError("Expected exact source-only intake counts")
    report={
      "batch":103,"counts":counts,"new_source_terms":4,"new_source_observations":7,
      "new_screened_meanings":0,"new_screened_links":0,
      "global_vs_anchored_lipschitz_distinct":True,
      "tree_two_equivalent_acyclicity_formulations_under_one_context":True,
      "pairwise_vs_mutual_sigma_independence_distinct":True,
      "independent_random_variables_use_generated_sigma_algebras":True,
      "old_566_individual_reviews_and_754_links_untouched":True,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch104 mathematical screening of six cross-field contexts with seven formulations; then Batch105 source-specific prerequisites."
    }
    atomic_json(w.root/"state/wave2_cross103_source_intake.json",report)
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(parser.parse_args().workspace),indent=2))
if __name__=="__main__":main()
