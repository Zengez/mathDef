"""Initialize 440-entry Wave 2 formulation review ledger, preserving Wave 1 decisions.

Never modifies original Wave 1 ledgers. Adds explicit needs_review for newly
screened formulations. Any later replacement of an inherited no-link/held
disposition must record its predecessor, rationale, and concrete new evidence.
"""
import argparse,json,hashlib
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json,jsonl,digest

def build(first,second):
    a,b=Workspace(first),Workspace(second)
    frozen=json.loads((a.root/"state/wave1_freeze.json").read_text())
    baseline=json.loads((b.root/"state/baseline.json").read_text())
    if frozen["state"]!="FROZEN" or baseline["first_wave_digest"]!=frozen["published_catalog_digest"]:
        raise PipelineError("Wave 2 formulation reviews require unchanged first-wave lineage")
    if digest(a.publication())!=frozen["published_catalog_digest"]:
        raise PipelineError("First wave frozen source mutated")
    meanings=b.records("meanings")
    forms={}
    for m in meanings.values():
        for f in m["formulations"]:
            if f["id"] in forms:
                raise PipelineError("Duplicate formulation ID in Wave 2")
            if f["review_state"]!="screened":
                raise PipelineError("Wave 2 source meaning is not screened: "+f["id"])
            forms[f["id"]]=m["id"]
    if len(forms)!=440 or len(meanings)!=428:
        raise PipelineError("Expected nine additionally screened independent foundations")
    inherited=jsonl(a.root/"state/stage5_formulation_reviews.jsonl")
    if len(inherited)!=431:
        raise PipelineError("Incomplete Wave 1 per-formulation reviews")
    base={r["formulation_id"]:r for r in inherited}
    if len(base)!=431 or not set(base).issubset(forms):
        raise PipelineError("Stage 5 inherited review identity mismatch")
    existing_links=b.records("relations")
    if len(existing_links)!=445:
        raise PipelineError("Prepare before Wave 2 relationship research")
    rows=[]
    current_digest=digest(list(meanings.values()))
    for fid,mid in sorted(forms.items()):
        if fid in base:
            orig=base[fid]
            if orig["meaning_id"]!=mid:
                raise PipelineError("Inherited formulation changed meaning")
            if any(rid not in existing_links for rid in orig["relation_ids"]):
                raise PipelineError("Missing inherited screened relation")
            rows.append({
                "formulation_id":fid,"meaning_id":mid,
                "meaning_catalog_digest":current_digest,
                "decision":orig["decision"],
                "relation_ids":list(orig["relation_ids"]),
                "original_wave1_disposition":orig["decision"],
                "original_review_digest":digest(orig),
                "source":"frozen_wave1_screened_ledger",
                "editorial_reason":orig["editorial_reason"],
                "reviewed_by":orig["reviewed_by"],
                "human_verified":False
            })
        else:
            rows.append({
                "formulation_id":fid,"meaning_id":mid,
                "meaning_catalog_digest":current_digest,
                "decision":"needs_review","relation_ids":[],
                "original_wave1_disposition":None,
                "source":"wave2_new_source_screened_meaning",
                "editorial_reason":"Requires independent formulation-specific comparison with reconstructed prerequisite meanings and mathematical context.",
                "reviewed_by":None,"human_verified":False
            })
    output=b.root/"state/wave2_formulation_reviews.jsonl"
    payload="".join(canonical(r)+"\n" for r in rows)
    if output.exists() and output.read_text(encoding="utf-8")!=payload:
        raise PipelineError("An existing Wave 2 review ledger must not be silently reinitialized")
    output.write_text(payload,encoding="utf-8")
    decisions={}
    for row in rows: decisions[row["decision"]]=decisions.get(row["decision"],0)+1
    report={
      "phase":"Wave 2 formulation review ledger initialized",
      "formulations":440,
      "inherited_wave1_review_decisions":431,
      "new_wave2_formulations_requiring_link_review":9,
      "meaning_count":428,
      "existing_screened_relations":445,
      "decisions":decisions,
      "meaning_catalog_digest":current_digest,
      "review_ledger_sha256":hashlib.sha256(payload.encode("utf-8")).hexdigest(),
      "inherited_dispositions_overridden":0,
      "stage5_wave2_complete":False,
      "original_mathdef_corpus_consulted":False,
      "next":"Individually source-check and append Wave 2 dependencies, explicitly preserving superseded original decisions and all inherited links."
    }
    atomic_json(b.root/"state/wave2_relation_review_seed.json",report)
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wave1",required=True,type=Path)
    ap.add_argument("--wave2",required=True,type=Path)
    a=ap.parse_args()
    print(json.dumps(build(a.wave1,a.wave2),indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
