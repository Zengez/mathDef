"""Batch 100: source-only discovery of scalar division-ring conventions.

Five direct ProofWiki definitions are individually paraphrased and admitted as
source evidence, not promoted to mathematical meanings or dependency links.
The math-specific policy resides in this adapter, not in generic engine code.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/division_ring_scalar_convention_research_batch100_2026-10-20.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
LEADS="wave2/foundation_source_discovery_batch_100.jsonl"
BEFORE={"sources":14,"terms":432,"observations":872,"meanings":536,"relations":742}
AFTER=dict(BEFORE,terms=437,observations=877)
KEYS=("division-ring","division-ring-multiplicative-norm","normed-division-ring",
      "left-vector-over-division-ring","right-vector-over-division-ring")

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Prior source-review data disagrees with audited candidate")
    path.write_text(content,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Independent unsealed Wave2 required")
    counts={s:len(w.records(s)) for s in BEFORE}
    if counts not in (BEFORE,AFTER):
        raise PipelineError("Unexpected independent source baseline "+str(counts))
    source=w.records("sources").get("src.proofwiki")
    if not source or source["access"]!="free" or source["rights"]!="permitted":
        raise PipelineError("Source approval or license record absent")
    rows={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(rows)!=set(KEYS):
        raise PipelineError("Exactly five individual direct source reviews required")
    existing=w.records("meanings")
    if any(m["display_term"] in {r["term"] for r in rows.values()} for m in existing.values()):
        raise PipelineError("Exact mathematical meaning/title collision must be reconciled")
    terms=[];observations=[];leads=[]
    for key in KEYS:
        r=rows[key]
        if (r.get("source_review_status")!="independent_exact_external_definition_checked"
            or r.get("source_access_outcome")!="direct_page_read"
            or r.get("source_id")!="src.proofwiki"
            or r.get("stage_ingested") or r.get("meaning_screened") or r.get("production_corpus_consulted")
            or not r["source"].startswith("https://proofwiki.org/wiki/Definition")
            or len(r["definition"])<145 or len(r["mathematical_review"])<280):
            raise PipelineError("Unsuitable source evidence or scope "+key)
        if key=="division-ring-multiplicative-norm" and ("|ab|_D=|a|_D|b|_D" not in r["definition"]):
            raise PipelineError("Multiplicativity cannot be replaced by submultiplicativity")
        if key=="normed-division-ring" and "lacking bibliographic" not in r["mathematical_review"]:
            raise PipelineError("Uncited derivative ProofWiki page must be flagged")
        if key.startswith("left-vector") and "D×V→V" not in r["definition"]:
            raise PipelineError("Left action scope incorrect")
        if key.startswith("right-vector") and "V×D→V" not in r["definition"]:
            raise PipelineError("Right action scope incorrect")
        tid="term.wave2.scalar100."+key
        oid="obs.wave2.scalar100."+key
        terms.append({
          "id":tid,"label":r["term"],"source_id":"src.proofwiki","locator":r["source"],
          "discovery_provenance":DOSSIER,"human_verified":False})
        observations.append({
          "id":oid,"term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
          "record_kind":"paraphrase","text":r["definition"],"context":r["context"],
          "editorial_note":r["mathematical_review"]+" Page sections: "+", ".join(r["source_sections"]),
          "reviewed_by":"assistant_independent_scalar_division_ring_source_review_2026_10_20",
          "human_verified":False})
        leads.append({
          "term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
          "candidate_observation_id":oid,"source_access_outcome":"direct_page_read",
          "editorial_reason":r["mathematical_review"],"source_research_complete":True,
          "meaning_screened":False,"human_verified":False,
          "review_reference":"research.wave2.scalar100."+key})
    if len(terms)!=5 or len(observations)!=5:
        raise PipelineError("Five source headings and observations required")
    w.ingest("terms",store(w.root/"intake/scalar100_terms.jsonl",terms),batch_size=5)
    w.ingest("observations",store(w.root/"intake/scalar100_observations.jsonl",observations),batch_size=5)
    store(w.root/LEADS,leads)
    manifest=w.root/MANIFEST
    cfg=json.loads(manifest.read_text(encoding="utf-8"))
    old=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in (49,54,58,62,66,70,75,80,84,89,93,97)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (old,old+[LEADS]):
        raise PipelineError("Historical source lead manifest changed")
    cfg["paths"]=old+[LEADS]
    atomic_json(manifest,cfg)
    now={s:len(w.records(s)) for s in AFTER}
    if now!=AFTER:
        raise PipelineError("Unexpected source-only counts")
    report={
      "batch":100,"counts":now,"new_source_terms":5,"new_source_observations":5,
      "new_screened_meanings":0,"new_screened_links":0,
      "division_ring_requires_associativity_unity_and_inverses":True,
      "scalar_division_ring_norm_requires_multiplicativity":True,
      "ring_norm_submultiplicative_convention_separate":True,
      "left_and_right_actions_not_equated":True,
      "uncited_derived_normed_division_ring_source_marked":True,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch101 separately screen five mathematical contexts, identifying unital left/right division-ring vector spaces and source quality caveat before link review."
    }
    atomic_json(w.root/"state/wave2_scalar100_source_intake.json",report)
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(parser.parse_args().workspace),indent=2))
if __name__=="__main__":
    main()
