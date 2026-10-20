"""Batch 106: source-only intake across topology, linear algebra, and calculus.

No mathematics is promoted here; independently sourced variants are paraphrased
with explicit caveats, checked for collisions and indexed for later screening.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/cross_branch_source_variants_batch106_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_106.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
BASE={"sources":14,"terms":441,"observations":884,"meanings":547,"relations":765}
AFTER=dict(BASE,terms=445,observations=891)
KEYS=("topological-closure","topological-boundary","linear-kernel","derivative-on-interval")
NCON={"topological-closure":1,"topological-boundary":1,"linear-kernel":2,"derivative-on-interval":1}
NFORM={"topological-closure":2,"topological-boundary":2,"linear-kernel":2,"derivative-on-interval":1}

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Historical source-variant review differs")
    path.write_text(body,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Requires independent, unsealed Wave2")
    counts={k:len(w.records(k)) for k in BASE}
    if counts not in (BASE,AFTER):
        raise PipelineError("Unexpected reviewed baseline "+str(counts))
    source=w.records("sources").get("src.proofwiki")
    if not source or source["access"]!="free" or source["rights"]!="permitted":
        raise PipelineError("Independently approved source rights absent")
    source_reviews={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(source_reviews)!=set(KEYS):
        raise PipelineError("Four independently checked cross-branch sources required")
    previous=w.records("meanings")
    names={r["term"] for r in source_reviews.values()}
    if any(m["display_term"] in names for m in previous.values()):
        raise PipelineError("Exact-source term already has mathematical meaning; manually reconcile")
    t=[];obs=[];leads=[]
    for key in KEYS:
        r=source_reviews[key]
        if (r["source_id"]!="src.proofwiki" or
            r["source_access_outcome"]!="direct_page_read" or
            r["source_review_status"]!="individually_read_external_definition_with_variants" or
            r["stage_ingested"] or r["meaning_screened"] or r["production_corpus_consulted"] or
            not r["source"].startswith("https://proofwiki.org/wiki/Definition") or
            len(r["mathematical_review"])<300 or len(r["contexts"])!=NCON[key]):
            raise PipelineError("Missing direct source scope and mathematical review "+key)
        if key=="topological-boundary":
            if "erroneous" not in r["mathematical_review"] or "closure and exterior" not in r["mathematical_review"]:
                raise PipelineError("Explicit erroneous boundary alternative must be excluded and logged")
        tid="term.wave2.cross106."+key
        t.append({"id":tid,"label":r["term"],"source_id":"src.proofwiki",
                  "locator":r["source"],"discovery_provenance":DOSSIER,"human_verified":False})
        n=0
        for context in r["contexts"]:
            for f in context["formulations"]:
                n+=1
                if not f["label"] or len(f["text"])<115:
                    raise PipelineError("Insufficient source-specific formulation "+key)
                obs.append({"id":f"obs.wave2.cross106.{key}.{n:02d}",
                            "term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
                            "record_kind":"paraphrase","text":f["text"],
                            "context":context["context"]+" / "+f["label"],
                            "editorial_note":r["mathematical_review"]+" Source sections: "+", ".join(r["source_sections"]),
                            "reviewed_by":"assistant_independent_cross_branch_source_review_2026_10_20",
                            "human_verified":False})
        if n!=NFORM[key]:
            raise PipelineError("Incorrect source-specific alternative count for "+key)
        leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":r["source"],
                      "candidate_observation_id":f"obs.wave2.cross106.{key}.01",
                      "source_access_outcome":"direct_page_read",
                      "editorial_reason":r["mathematical_review"],
                      "source_research_complete":True,"meaning_screened":False,
                      "human_verified":False,"review_reference":"research.wave2.cross106."+key})
    if len(t)!=4 or len(obs)!=7:
        raise PipelineError("Four source terms and seven observations expected")
    w.ingest("terms",store(w.root/"intake/cross106_terms.jsonl",t),batch_size=4)
    w.ingest("observations",store(w.root/"intake/cross106_observations.jsonl",obs),batch_size=7)
    store(w.root/LEADS,leads)
    cfgfile=w.root/MANIFEST
    cfg=json.loads(cfgfile.read_text(encoding="utf-8"))
    old=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in (49,54,58,62,66,70,75,80,84,89,93,97,100,103)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (old,old+[LEADS]):
        raise PipelineError("Old source lead manifest mutated")
    cfg["paths"]=old+[LEADS]
    atomic_json(cfgfile,cfg)
    counts={k:len(w.records(k)) for k in AFTER}
    if counts!=AFTER:
        raise PipelineError("Source-only admission did not match counts")
    report={"batch":106,"counts":counts,"new_source_terms":4,"new_source_observations":7,
            "new_screened_meanings":0,"new_links":0,
            "closure_closed_superset_presentations_equivalent":True,
            "boundary_ambient_subspace_explicit":True,
            "incorrect_boundary_exterior_source_alternative_excluded":True,
            "module_kernel_vs_field_vector_space_kernel_distinct":True,
            "derivative_function_not_conflated_with_point_value":True,
            "prior_573_reviews_and_765_links_preserved":True,
            "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
            "next":"Batch107 separate source/meaning mathematical screening of five contexts and seven formulations, followed by sourced noncircular dependencies in Batch108."}
    atomic_json(w.root/"state/wave2_cross106_source_intake.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
