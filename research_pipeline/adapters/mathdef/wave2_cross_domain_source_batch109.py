"""Batch109: independent source-only discovery across algebra and topology.

All topic-specific decisions remain in this mathDef adapter. Four vetted
source headings and seven variant observations; no meanings or links promoted.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/cross_domain_source_variants_batch109_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_109.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
BASE={"sources":14,"terms":445,"observations":891,"meanings":552,"relations":774}
AFTER=dict(BASE,terms=449,observations=898)
KEYS=("linear-transformation","image-mapping","rank-linear","accumulation-point")
NCON={"linear-transformation":2,"image-mapping":1,"rank-linear":1,"accumulation-point":2}
NFORM={"linear-transformation":2,"image-mapping":2,"rank-linear":1,"accumulation-point":2}

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Source-specific immutable intake history changed")
    path.write_text(content,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Independent unsealed Wave2 required")
    counts={k:len(w.records(k)) for k in BASE}
    if counts not in (BASE,AFTER):
        raise PipelineError("Unexpected previous reviewed counts "+str(counts))
    src=w.records("sources").get("src.proofwiki")
    if not src or src["access"]!="free" or src["rights"]!="permitted":
        raise PipelineError("Approved source registry and rights required")
    dossiers={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(dossiers)!=set(KEYS):
        raise PipelineError("All four direct source dossiers required")
    present=w.records("meanings")
    if any(m["display_term"] in {r["term"] for r in dossiers.values()} for m in present.values()):
        raise PipelineError("A meaning with the same display title needs human scope reconciliation")
    terms=[];obs=[];leads=[]
    for key in KEYS:
        r=dossiers[key]
        if (r["source_id"]!="src.proofwiki" or r["source_access_outcome"]!="direct_page_read"
          or r["source_review_status"]!="individually_read_external_definition_with_variants"
          or r["stage_ingested"] or r["meaning_screened"] or r["production_corpus_consulted"]
          or not r["source"].startswith("https://proofwiki.org/wiki/Definition")
          or len(r["mathematical_review"])<320 or len(r["contexts"])!=NCON[key]):
            raise PipelineError("Unverified source review "+key)
        if key=="rank-linear" and "FINITE-DIMENSIONAL" not in r["mathematical_review"]:
            raise PipelineError("Explicit finite-image rank source caveat missing")
        if key=="accumulation-point" and "INFINITELY MANY indices" not in r["mathematical_review"]:
            raise PipelineError("Sequence index multiplicities not source-screened")
        tid="term.wave2.cross109."+key
        terms.append({"id":tid,"label":r["term"],"source_id":"src.proofwiki",
                      "locator":r["source"],"discovery_provenance":DOSSIER,"human_verified":False})
        n=0
        for c in r["contexts"]:
            for f in c["formulations"]:
                n+=1
                if not f["label"] or len(f["text"])<110:
                    raise PipelineError("Insufficient individual mathematical source observation "+key)
                obs.append({
                  "id":f"obs.wave2.cross109.{key}.{n:02d}","term_id":tid,
                  "source_id":"src.proofwiki","locator":r["source"],
                  "record_kind":"paraphrase","text":f["text"],
                  "context":c["context"]+" / "+f["label"],
                  "editorial_note":r["mathematical_review"]+" Sections: "+", ".join(r["source_sections"]),
                  "reviewed_by":"assistant_independent_cross_domain_source_read_2026_10_20",
                  "human_verified":False})
        if n!=NFORM[key]:
            raise PipelineError("Formulation evidence count mismatch "+key)
        leads.append({
          "term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
          "candidate_observation_id":f"obs.wave2.cross109.{key}.01",
          "source_access_outcome":"direct_page_read",
          "editorial_reason":r["mathematical_review"],
          "source_research_complete":True,"meaning_screened":False,
          "human_verified":False,"review_reference":"research.wave2.cross109."+key})
    if len(terms)!=4 or len(obs)!=7:
        raise PipelineError("Exactly four headings and seven source observations required")
    w.ingest("terms",store(w.root/"intake/cross109_terms.jsonl",terms),batch_size=4)
    w.ingest("observations",store(w.root/"intake/cross109_observations.jsonl",obs),batch_size=7)
    store(w.root/LEADS,leads)
    path=w.root/MANIFEST
    config=json.loads(path.read_text(encoding="utf-8"))
    historical=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in
      (49,54,58,62,66,70,75,80,84,89,93,97,100,103,106)]
    if config.get("schema_version")!=1 or config.get("paths") not in (historical,historical+[LEADS]):
        raise PipelineError("Previous source evidence manifest mutated")
    config["paths"]=historical+[LEADS]
    atomic_json(path,config)
    now={k:len(w.records(k)) for k in AFTER}
    if now!=AFTER:
        raise PipelineError("Unexpected source-only registry counts "+str(now))
    report={
      "batch":109,"counts":now,"new_source_terms":4,"new_source_observations":7,
      "new_screened_meanings":0,"new_screened_links":0,
      "module_and_field_vector_linearity_distinct":True,
      "two_image_forms_equivalent":True,
      "rank_finite_image_condition_retained":True,
      "accumulation_point_sequence_and_set_distinct":True,
      "no_production_corpus_consulted":True,
      "old_580_individual_reviews_and_774_links_preserved":True,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch110: individually screen six source-defined meanings with seven formulations, including finite-image rank and index-multiplicity caveats."}
    atomic_json(w.root/"state/wave2_cross109_source_intake.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
