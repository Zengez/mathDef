"""Batch115: admit four independent source headings and six scoped observations.

Only the mathDef adapter contains subject semantics. No meanings or links
are promoted in this first source-evidence stage.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/group_action_measure_partition_source_batch115_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_115.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
BASE={"sources":14,"terms":453,"observations":906,"meanings":564,"relations":794}
AFTER=dict(BASE,terms=457,observations=912)
KEYS=("orbit-group-action","stabilizer-group-action","pushforward-measure","set-partition")
COUNTS={"orbit-group-action":2,"stabilizer-group-action":1,"pushforward-measure":1,"set-partition":2}

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    contents="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=contents:
        raise PipelineError("Historical independent source record changed")
    path.write_text(contents,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Requires independent unsealed Wave2")
    counts={k:len(w.records(k)) for k in BASE}
    if counts not in (BASE,AFTER):
        raise PipelineError("Unexpected screened Wave2 source baseline "+str(counts))
    src=w.records("sources").get("src.proofwiki")
    if not src or src["access"]!="free" or src["rights"]!="permitted":
        raise PipelineError("Approved source registry rights absent")
    rows={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(rows)!=set(KEYS):
        raise PipelineError("Four directly sourced research topics required")
    existing={m["display_term"] for m in w.records("meanings").values()}
    if any(rows[key]["term"] in existing for key in KEYS):
        raise PipelineError("Exact title already has a meaning; collision reconciliation required")
    terms=[];observations=[];leads=[]
    for key in KEYS:
        r=rows[key]; tid="term.wave2.group115."+key
        if (r["source_id"]!="src.proofwiki" or r["source_access_outcome"]!="direct_page_read"
          or r["source_review_status"]!="individually_read_external_definition_with_variants"
          or r["stage_ingested"] or r["meaning_screened"] or r["production_corpus_consulted"]
          or not r["source"].startswith("https://proofwiki.org/wiki/Definition")
          or len(r["review"])<280 or len(r["contexts"])!=1):
            raise PipelineError("Individually sourced mathematical research absent "+key)
        if key=="orbit-group-action" and "equivalent" not in r["review"]:
            raise PipelineError("Orbit equivalence must be checked")
        if key=="set-partition" and "S=∅" not in r["review"]:
            raise PipelineError("Empty underlying set convention required")
        if key=="pushforward-measure" and "nonmeasurable" not in r["review"]:
            raise PipelineError("Measurability and target measure hypotheses missing")
        terms.append({"id":tid,"label":r["term"],"source_id":"src.proofwiki",
              "locator":r["source"],"discovery_provenance":DOSSIER,"human_verified":False})
        forms=r["contexts"][0]["forms"]
        if len(forms)!=COUNTS[key]:
            raise PipelineError("Unexpected source-specific formulations "+key)
        for i,f in enumerate(forms,1):
            if not f["label"] or len(f["text"])<95:
                raise PipelineError("Missing precise source paraphrase "+key)
            observations.append({
              "id":f"obs.wave2.group115.{key}.{i:02d}","term_id":tid,
              "source_id":"src.proofwiki","locator":r["source"],
              "record_kind":"paraphrase","text":f["text"],
              "context":r["contexts"][0]["context"]+" / "+f["label"],
              "editorial_note":r["review"]+" Source sections: "+", ".join(r["source_sections"]),
              "reviewed_by":"assistant_independent_group_measure_partition_source_intake_2026_10_20",
              "human_verified":False})
        leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
          "candidate_observation_id":f"obs.wave2.group115.{key}.01",
          "source_access_outcome":"direct_page_read","editorial_reason":r["review"],
          "source_research_complete":True,"meaning_screened":False,"human_verified":False,
          "review_reference":"research.wave2.group115."+key})
    if len(terms)!=4 or len(observations)!=6:
        raise PipelineError("Exactly four source headings and six observations expected")
    w.ingest("terms",store(w.root/"intake/group115_terms.jsonl",terms),batch_size=4)
    w.ingest("observations",store(w.root/"intake/group115_observations.jsonl",observations),batch_size=6)
    store(w.root/LEADS,leads)
    path=w.root/MANIFEST;cfg=json.loads(path.read_text(encoding="utf-8"))
    old=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in (49,54,58,62,66,70,75,80,84,89,93,97,100,103,106,109,112)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (old,old+[LEADS]):
        raise PipelineError("Historical source discovery manifest changed")
    cfg["paths"]=old+[LEADS];atomic_json(path,cfg)
    now={k:len(w.records(k)) for k in AFTER}
    if now!=AFTER:raise PipelineError("Source-only intake totals incorrect")
    result={"batch":115,"counts":now,"new_source_terms":4,"new_observations":6,
      "new_mathematical_meanings":0,"new_prerequisite_links":0,
      "orbit_equivalent_source_forms":True,"set_partition_equivalent_source_forms":True,
      "point_stabilizer_requires_action":True,"pushforward_uses_measurable_preimages":True,
      "empty_set_partition_allowed":True,"prior_594_reviews_and_794_links_untouched":True,
      "held_directional_gradient_observation_still_excluded":True,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch116 four mathematical contexts with six independent source formulations; Batch117 separately review prerequisites."}
    atomic_json(w.root/"state/wave2_group115_source_intake.json",result)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
