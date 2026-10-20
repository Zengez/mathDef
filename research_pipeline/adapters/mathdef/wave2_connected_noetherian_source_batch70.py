"""Source intake for two audited cross-domain variant families.

Do not consult original production mathDef. Preserve the distinct Stacks
nonempty-connected convention while sourcing ProofWiki's empty-allowed one.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
REVIEW="wave2/cross_domain_equivalence_audit_batch69_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_70.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
BEFORE={"sources":14,"terms":408,"observations":834,"meanings":509,"relations":693}
AFTER=dict(BEFORE,terms=410,observations=841)
TOPICS={
 "connected":"wave2.batch69.connected-topological-space",
 "noetherian":"wave2.batch69.noetherian-ring"
}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    s="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=s:
        raise PipelineError("Changed previously reviewed variant evidence")
    path.write_text(s,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Only unsealed independent Wave 2 allowed")
    if {s:len(w.records(s)) for s in BEFORE} not in (BEFORE,AFTER):
        raise PipelineError("Unexpected approved research baseline")
    source=w.records("sources").get("src.proofwiki")
    if not source or source["rights"]!="permitted" or source["access"]!="free":
        raise PipelineError("ProofWiki source missing/rights unapproved")
    existing=w.records("meanings")
    connected=existing.get("meaning.ab260940ea9c523d.connected-topological-space")
    noetherian=existing.get("meaning.86b5d488b98c612f.noetherian-commutative-ring")
    if (not connected or not noetherian or
         not connected["formulations"][0]["text"].startswith("A nonempty topological space") or
         "equivalently" not in noetherian["formulations"][0]["text"]):
        raise PipelineError("Source variant collisions or historical math meanings changed")
    research={r["research_id"]:r for r in jsonl(w.root/REVIEW)}
    if len(research)!=2 or set(research)!=set(TOPICS.values()):
        raise PipelineError("Two individually researched source dossiers required")
    termrows=[];observations=[];leads=[]
    for label,rid in TOPICS.items():
        r=research[rid]
        forms=r["reviewed_variants"]
        if (r["source_id"]!="src.proofwiki" or not r["source_checked"] or
            r["production_corpus_consulted"] or r["stage_ingested"] or
            r["meaning_screened"] or len(forms)!=(3 if label=="connected" else 4) or
            len(r["mathematical_review"])<260):
            raise PipelineError("Source-reviewed variant proof missing: "+label)
        tid="term.wave2.variant70."+label
        termrows.append({
          "id":tid,"label":r["term"],"source_id":"src.proofwiki",
          "locator":r["source_url"],"discovery_provenance":REVIEW,
          "human_verified":False
        })
        for i,variant in enumerate(forms,1):
            observations.append({
              "id":f"obs.wave2.variant70.{label}.{i:02d}",
              "term_id":tid,"source_id":"src.proofwiki",
              "locator":r["source_url"],"record_kind":"paraphrase",
              "text":variant["text"],"context":variant["label"],
              "editorial_note":r["mathematical_review"]+" Scope: "+variant["mathematical_scope"],
              "reviewed_by":"assistant_independent_variant70_external_source_review_2026_10_20",
              "human_verified":False
            })
        leads.append({
          "term_id":tid,"source_id":"src.proofwiki","locator":r["source_url"],
          "candidate_observation_id":f"obs.wave2.variant70.{label}.01",
          "source_access_outcome":"direct_page_read",
          "editorial_reason":r["mathematical_review"],
          "source_research_complete":True,"meaning_screened":False,
          "human_verified":False,"review_reference":rid
        })
    w.ingest("terms",store(w.root/"intake/variant70_terms.jsonl",termrows),batch_size=2)
    w.ingest("observations",store(w.root/"intake/variant70_observations.jsonl",observations),batch_size=7)
    store(w.root/LEADS,leads)
    m=w.root/MANIFEST
    config=json.loads(m.read_text(encoding="utf-8"))
    previous=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in (49,54,58,62,66)]
    if config.get("schema_version")!=1 or config.get("paths") not in (previous,previous+[LEADS]):
        raise PipelineError("Approved supplemental source lead manifest moved")
    config["paths"]=previous+[LEADS]
    atomic_json(m,config)
    counts={s:len(w.records(s)) for s in AFTER}
    if counts!=AFTER:
        raise PipelineError("Source evidence cardinality changed")
    result={
      "batch":70,"counts":counts,"term_candidates":2,
      "individual_formulation_evidence_added":7,"new_meanings_screened":0,
      "historical_stacks_nonempty_connected_meaning_preserved":True,
      "empty_connected_convention_distinct_context":True,
      "noetherian_existing_meaning_recognized":True,
      "original_production_mathdef_content_consulted":False,"human_peer_verified":False,
      "all_stages_unsealed":True,
      "next":"Add nonempty-optional connectedness as an explicitly distinct contextual meaning and audit four separate Noetherian equivalences under the existing meaning; preserve all 524 formulation review decisions."
    }
    atomic_json(w.root/"state/wave2_variant70_source_intake.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
