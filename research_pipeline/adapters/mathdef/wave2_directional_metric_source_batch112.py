"""Batch 112: source-only audit with directional-derivative gradient claim held.

No mathematical promotion. The generic engine remains subject-neutral.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/directional_metric_topology_source_audit_batch112_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_112.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
BEFORE={"sources":14,"terms":449,"observations":898,"meanings":558,"relations":784}
AFTER=dict(BEFORE,terms=453,observations=906)
KEYS=("open-ball","closed-ball","homeomorphism","directional-derivative")
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    text="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=text:
        raise PipelineError("Previously source-reviewed data changed")
    path.write_text(text,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BEFORE):
        raise PipelineError("Unsealed independent Wave 2 is required")
    counts={k:len(w.records(k)) for k in BEFORE}
    if counts not in (BEFORE,AFTER):
        raise PipelineError("Unexpected source-only inventory "+str(counts))
    src=w.records("sources").get("src.proofwiki")
    if not src or src["rights"]!="permitted" or src["access"]!="free":
        raise PipelineError("Source access and rights approval required")
    data={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(data)!=set(KEYS):
        raise PipelineError("Four independently source-reviewed dossiers required")
    earlier={m["display_term"] for m in w.records("meanings").values()}
    if any(r["term"] in earlier for r in data.values()):
        raise PipelineError("Existing exact display title requires collision reconciliation")
    terms=[];obs=[];leads=[];held=[]
    for key in KEYS:
        r=data[key]
        if (r["source_id"]!="src.proofwiki" or r["source_access_outcome"]!="direct_page_read"
          or r["stage_ingested"] or r["meaning_screened"] or r["production_corpus_consulted"]
          or not r["source"].startswith("https://proofwiki.org/wiki/Definition") or len(r["review"])<300):
            raise PipelineError("Unverified source-specific source research "+key)
        if key=="directional-derivative" and (
            len(r["contexts"])!=2 or not r["contexts"][1].get("held") or
            "Counterexample" not in r["review"] or "gradient existence is insufficient" not in r["review"]):
            raise PipelineError("Gradient-only directional derivative must be explicitly held")
        tid="term.wave2.directional112."+key
        terms.append({"id":tid,"label":r["term"],"source_id":"src.proofwiki",
          "locator":r["source"],"discovery_provenance":DOSSIER,"human_verified":False})
        number=0
        for c in r["contexts"]:
            for f in c["forms"]:
                number+=1
                oid=f"obs.wave2.directional112.{key}.{number:02d}"
                obs.append({"id":oid,"term_id":tid,"source_id":"src.proofwiki",
                  "locator":r["source"],"record_kind":"paraphrase","text":f["text"],
                  "context":c["context"]+" / "+f["label"],
                  "editorial_note":r["review"]+" Sections: "+", ".join(r["sections"]),
                  "reviewed_by":"assistant_independent_directional_metric_topology_source_audit_2026_10_20",
                  "human_verified":False})
                if c.get("held"):
                    held.append({"observation_id":oid,"term_id":tid,
                     "held_reason":"Gradient merely exists does not imply total differentiability; unsafe equality with directional quotient; explicit counterexample in sourced dossier.",
                     "decision":"source_observed_held_not_mathematically_promoted",
                     "human_verified":False})
        expected={"open-ball":2,"closed-ball":2,"homeomorphism":2,"directional-derivative":2}[key]
        if number!=expected:
            raise PipelineError("Individual variant count mismatch "+key)
        leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
          "candidate_observation_id":f"obs.wave2.directional112.{key}.01",
          "source_access_outcome":"direct_page_read","editorial_reason":r["review"],
          "source_research_complete":True,"meaning_screened":False,
          "human_verified":False,"review_reference":"research.wave2.directional112."+key})
    if len(terms)!=4 or len(obs)!=8 or len(held)!=1:
        raise PipelineError("Exactly four headings, eight observations, one held gradient claim required")
    w.ingest("terms",store(w.root/"intake/directional112_terms.jsonl",terms),batch_size=4)
    w.ingest("observations",store(w.root/"intake/directional112_observations.jsonl",obs),batch_size=8)
    store(w.root/LEADS,leads)
    store(w.root/"wave2/directional112_quarantined_source_claims.jsonl",held)
    cfgpath=w.root/MANIFEST;cfg=json.loads(cfgpath.read_text(encoding="utf-8"))
    old=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in (49,54,58,62,66,70,75,80,84,89,93,97,100,103,106,109)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (old,old+[LEADS]):
        raise PipelineError("Historical source manifest changed")
    cfg["paths"]=old+[LEADS];atomic_json(cfgpath,cfg)
    now={k:len(w.records(k)) for k in AFTER}
    if now!=AFTER:raise PipelineError("Unexpected source-only totals")
    report={"batch":112,"counts":now,"new_source_terms":4,"new_source_observations":8,
      "held_gradient_claims":1,"new_mathematical_meanings":0,"new_links":0,
      "homeomorphism_two_equivalent_forms_source_only":True,
      "open_and_closed_ball_strict_inequality_distinct":True,
      "closed_metric_ball_not_assumed_closure_of_open_ball":True,
      "gradient_exists_not_sufficient_for_directional_formula":True,
      "earlier_587_reviews_and_784_links_preserved":True,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch113: separately screen six mathematical contexts, seven unheld formulations; keep gradient-only claim in held source registry."}
    atomic_json(w.root/"state/wave2_directional112_source_intake.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
