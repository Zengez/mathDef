"""Batch121 source-only independent intake for subgroup/coset and real series."""
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/subgroup_coset_real_series_source_batch121_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_121.jsonl"
BEFORE={"sources":14,"terms":461,"observations":919,"meanings":572,"relations":811}
AFTER=dict(BEFORE,terms=465,observations=924)
KEYS=("subgroup","coset","convergent-real-series","real-power-series")
COUNTS={"subgroup":1,"coset":2,"convergent-real-series":1,"real-power-series":1}
def store(path,items):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(x)+"\n" for x in items)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Previously inspected independent source evidence differs")
    path.write_text(body,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Requires independent and unsealed Wave2")
    if {s:len(w.records(s)) for s in BEFORE} not in (BEFORE,AFTER):
        raise PipelineError("Unexpected exact prior screened research counts")
    source=w.records("sources").get("src.proofwiki")
    if not source or source["rights"]!="permitted" or source["access"]!="free":
        raise PipelineError("Independent source registry rights not approved")
    dossier={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if set(dossier)!=set(KEYS):raise PipelineError("Missing four direct verified source reviews")
    titles={m["display_term"] for m in w.records("meanings").values()}
    if any(dossier[k]["term"] in titles for k in KEYS):
        raise PipelineError("Independent mathematical title already exists; manually reconcile")
    terms=[];observations=[];leads=[]
    for key in KEYS:
        row=dossier[key];tid="term.wave2.prereq121."+key
        if (row["source_id"]!="src.proofwiki" or row["source_access_outcome"]!="direct_page_read" or
            row["source_review_status"]!="individually_read_external_definition_with_variants" or
            row["stage_ingested"] or row["meaning_screened"] or row["production_corpus_consulted"] or
            not row["source"].startswith("https://proofwiki.org/wiki/Definition") or len(row["review"])<280):
            raise PipelineError("Direct-source scope or mathematical caveats missing "+key)
        if key=="coset" and ("nonabelian" not in row["review"] or len(row["contexts"])!=2):
            raise PipelineError("Left vs right coset scope must be explicit")
        if key=="real-power-series" and "NOT" not in row["review"]:
            raise PipelineError("Power-series analytic/formal ambiguity not screened")
        terms.append({"id":tid,"label":row["term"],"source_id":"src.proofwiki",
           "locator":row["source"],"discovery_provenance":DOSSIER,"human_verified":False})
        i=0
        for context in row["contexts"]:
            for f in context["forms"]:
                i+=1
                if not f["label"] or len(f["text"])<100:
                    raise PipelineError("Insufficient individual source definition "+key)
                observations.append({"id":f"obs.wave2.prereq121.{key}.{i:02d}",
                  "term_id":tid,"source_id":"src.proofwiki","locator":row["source"],
                  "record_kind":"paraphrase","text":f["text"],
                  "context":context["context"]+" / "+f["label"],
                  "editorial_note":row["review"]+" Source sections: "+", ".join(row["source_sections"]),
                  "reviewed_by":"assistant_independent_subgroup_coset_series_source_review_2026_10_20",
                  "human_verified":False})
        if i!=COUNTS[key]:raise PipelineError("Source observations count mismatch "+key)
        leads.append({"term_id":tid,"source_id":"src.proofwiki","locator":row["source"],
            "candidate_observation_id":f"obs.wave2.prereq121.{key}.01",
            "source_access_outcome":"direct_page_read","editorial_reason":row["review"],
            "source_research_complete":True,"meaning_screened":False,"human_verified":False,
            "review_reference":"research.wave2.prereq121."+key})
    if len(terms)!=4 or len(observations)!=5:raise PipelineError("Expected four headings and five observations")
    w.ingest("terms",store(w.root/"intake/prereq121_terms.jsonl",terms),batch_size=4)
    w.ingest("observations",store(w.root/"intake/prereq121_observations.jsonl",observations),batch_size=5)
    store(w.root/LEADS,leads)
    path=w.root/"wave2/additional_source_lead_batches.json"
    cfg=json.loads(path.read_text(encoding="utf-8"))
    historical=[f"wave2/foundation_source_discovery_batch_{n}.jsonl" for n in
      (49,54,58,62,66,70,75,80,84,89,93,97,100,103,106,109,112,115,118)]
    if cfg.get("schema_version")!=1 or cfg.get("paths") not in (historical,historical+[LEADS]):
        raise PipelineError("Historical source research manifest mutated")
    cfg["paths"]=historical+[LEADS]
    atomic_json(path,cfg)
    now={s:len(w.records(s)) for s in AFTER}
    if now!=AFTER:raise PipelineError("Source-only counts wrong")
    result={"batch":121,"counts":now,"new_source_headings":4,"new_source_observations":5,
      "new_meanings":0,"new_links":0,"coset_handedness_separate":True,
      "subgroup_inherited_group_operation":True,"real_series_convergence_by_partial_sums":True,
      "power_series_expression_not_universal_convergent_function":True,
      "prior_606_formulation_reviews_and_811_links_preserved":True,
      "both_previously_held_claims_unpromoted":True,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch122 five scoped mathematical meanings and five individually sourced formulations, followed by Batch123 individual dependency screens."}
    atomic_json(w.root/"state/wave2_prereq121_source_intake.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
