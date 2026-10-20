"""Batch 89 source-only intake of three distinct probability/measure terms.

The already screened general left-module meaning is not recreated. Generic
research engine APIs remain subject independent; scope is mathDef-adapter data.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/probability_and_module_foundations_research_batch87_2026-10-20.jsonl"
CHECK="wave2/found87_collision_and_module_conventions_batch88_2026-10-20.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
LEADS="wave2/foundation_source_discovery_batch_89.jsonl"
BEFORE={"sources":14,"terms":422,"observations":858,"meanings":523,"relations":719}
AFTER=dict(BEFORE,terms=425,observations=862)
KEYS=("measurable-space","probability-space","random-variable")
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Earlier individually screened source data differ")
    path.write_text(body,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Requires unsealed independent Wave 2")
    if {s:len(w.records(s)) for s in BEFORE} not in (BEFORE,AFTER):
        raise PipelineError("Unexpected independently sourced stage inventory")
    pw=w.records("sources").get("src.proofwiki")
    if not pw or pw["access"]!="free" or pw["rights"]!="permitted":
        raise PipelineError("Permitted independently vetted source missing")
    reviewed={x["key"]:x for x in jsonl(w.root/DOSSIER)}
    collisions={x["key"]:x for x in jsonl(w.root/CHECK)}
    if set(reviewed)!=set(KEYS)|{"module"} or set(collisions)!=set(reviewed):
        raise PipelineError("Source and independent collision review incomplete")
    if collisions["module"]["decision"]!="hold_from_duplicate_intake;retain existing left-module and investigate right/unitary alternatives":
        raise PipelineError("Do not duplicate previously screened left module")
    existing=w.records("meanings")
    if not existing.get("meaning.wave2.foundation.left-module-nonunital"):
        raise PipelineError("Historical screened ordinary left module missing")
    for name in ("measurable space","probability space","random variable"):
        if any(m["display_term"].strip().lower()==name for m in existing.values()):
            raise PipelineError("Potential existing mathematical meaning collision "+name)
    terms=[];observations=[];leads=[]
    for key in KEYS:
        r=reviewed[key];decision=collisions[key]
        if (r["source_id"]!="src.proofwiki" or r["stage_ingested"] or
            r["production_corpus_consulted"] or
            not r["source_status"]=="direct_page_read" or
            not decision["proofwiki_source_verified"] or
            not decision["decision"].startswith("admit_source_evidence") or
            decision["source_locator"]!=r["source_locator"] or
            len(r["mathematical_review"])<235 or
            len(r["variants"])!=(2 if key=="random-variable" else 1)):
            raise PipelineError("Individual exact-source review insufficient: "+key)
        tid="term.wave2.prob89."+key
        terms.append({
            "id":tid,"label":r["term"],"source_id":"src.proofwiki",
            "locator":r["source_locator"],"discovery_provenance":DOSSIER,
            "human_verified":False
        })
        for i,form in enumerate(r["variants"],1):
            observations.append({
                "id":f"obs.wave2.prob89.{key}.{i:02d}",
                "term_id":tid,"source_id":"src.proofwiki",
                "locator":r["source_locator"],"record_kind":"paraphrase",
                "text":form["text"],"context":r["domain"]+" / "+form["label"],
                "editorial_note":r["mathematical_review"],
                "reviewed_by":"assistant_independent_probability_source_review_2026_10_20",
                "human_verified":False
            })
        leads.append({
            "term_id":tid,"source_id":"src.proofwiki","locator":r["source_locator"],
            "candidate_observation_id":f"obs.wave2.prob89.{key}.01",
            "source_access_outcome":"direct_page_read",
            "editorial_reason":r["mathematical_review"],
            "source_research_complete":True,"meaning_screened":False,
            "human_verified":False,"review_reference":"batch87.collisions."+key
        })
    w.ingest("terms",store(w.root/"intake/prob89_terms.jsonl",terms),batch_size=3)
    w.ingest("observations",store(w.root/"intake/prob89_observations.jsonl",observations),batch_size=4)
    store(w.root/LEADS,leads)
    manifest=w.root/MANIFEST
    data=json.loads(manifest.read_text(encoding="utf-8"))
    earlier=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in (49,54,58,62,66,70,75,80,84)]
    if data.get("schema_version")!=1 or data.get("paths") not in (earlier,earlier+[LEADS]):
        raise PipelineError("Historical individually reviewed source manifest differs")
    data["paths"]=earlier+[LEADS]
    atomic_json(manifest,data)
    current={s:len(w.records(s)) for s in AFTER}
    if current!=AFTER:
        raise PipelineError("Unexpected source admission counts")
    report={
      "batch":89,"counts":current,"source_terms_added":3,"individual_source_observations_added":4,
      "mathematical_meanings_added":0,"links_added":0,
      "existing_left_module_not_duplicated":True,
      "three_concepts_have_no_existing_exact_meaning":True,
      "all_422_old_term_dispositions_preserved":True,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Screen one measurable-space and one probability-space meaning plus general/real random-variable contexts. Do not conflate object/codomain types."
    }
    atomic_json(w.root/"state/wave2_prob89_source_intake.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
