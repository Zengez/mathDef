"""Batch136 mathematical screening: convex set, falling factorial, numeric delta, bipartite graph.

The independently observed zero-index source corroboration and empty color
class convention remain explicit. No previous formulation decision altered.
"""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/convex_falling_delta_bipartite_source_batch135_2026-10-20.jsonl"
BASE={"sources":14,"terms":481,"observations":953,"meanings":591,"relations":869}
AFTER=dict(BASE,meanings=595)
SPECS=(
 ("convex-set","convex-real","Real-vector-space convex subset with equivalent two-point and Minkowski-set conditions"),
 ("falling-factorial","falling-real-nonnegative","Real falling factorial x under nonnegative index, zero as empty product"),
 ("kronecker-delta","numeric-delta","Numeric Kronecker delta as equality indicator on any set"),
 ("bipartite-simple-graph","simple-bipartite","Simple undirected bipartite graph by two-part cover or proper non-surjective two-coloring")
)
N={"convex-set":2,"falling-factorial":1,"kronecker-delta":2,"bipartite-simple-graph":2}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    contents="".join(canonical(row)+"\n" for row in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=contents:
        raise PipelineError("Prior source-specific mathematical formulation review changed")
    path.write_text(contents,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Requires unsealed independent Wave2")
    if {k:len(w.records(k)) for k in BASE} not in (BASE,AFTER):
        raise PipelineError("Independently sourced B135 baseline not yet committed")
    source_report=json.loads((w.root/"state/wave2_bridge135_source_intake.json").read_text())
    if source_report.get("new_source_headings")!=4 or source_report.get("new_observations")!=7 or not source_report.get("falling_factorial_zero_case_independently_corroborated"):
        raise PipelineError("Verified source evidence or zero-index corroboration missing")
    research={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    terms=w.records("terms");obs=w.records("observations")
    meanings=[];ind=[]
    for key,suffix,context in SPECS:
        r=research[key];tid="term.wave2.bridge135."+key
        if terms.get(tid,{}).get("locator")!=r["source"] or r["production_corpus_consulted"]:
            raise PipelineError("Missing exact independent source/term lineage "+key)
        forms=r["contexts"][0]["forms"];reason=r["review"]
        if len(forms)!=N[key] or len(reason)<390:
            raise PipelineError("Mathematical source review or variant count missing "+key)
        if key=="convex-set":
            if "tx+(1−t)y" not in forms[0]["text"] or "tC+(1−t)C⊆C" not in forms[1]["text"]:
                raise PipelineError("Convex two-point vs set-based equivalence incomplete")
        elif key=="falling-factorial":
            if "∏" not in forms[0]["text"] or "x^{" not in forms[0]["text"] or "n∈ℕ₀" not in forms[0]["text"] or "empty-product" not in forms[0]["text"]:
                raise PipelineError("Falling factorial lacks zero-index convention")
            if "Binomial_Coefficient_with_Zero" not in r["corroborating_source"]:
                raise PipelineError("Source n≥1 only, zero-index case needs extra provenance")
        elif key=="kronecker-delta":
            if "δ(a,b)=1" not in forms[0]["text"] or "[a=b]" not in forms[1]["text"]:
                raise PipelineError("Numeric equality indicator and Iverson forms not equivalent")
        elif key=="bipartite-simple-graph":
            if "either part may be empty" not in forms[0]["text"] or "surjectivity of c is not required" not in forms[1]["text"]:
                raise PipelineError("Edgeless graph convention not mathematically scoped")
        mid="meaning.wave2.bridge136."+suffix
        rows=[]
        for i,f in enumerate(forms,1):
            oid=f"obs.wave2.bridge135.{key}.{i:02d}"
            o=obs.get(oid)
            if not o or o["term_id"]!=tid or o["locator"]!=r["source"] or o["text"]!=f["text"]:
                raise PipelineError("Missing exact source evidence for individual mathematical form "+oid)
            fid="form.wave2.bridge136."+suffix+("."+str(i) if len(forms)>1 else "")
            rows.append({"id":fid,"text":f["text"],"evidence_ids":[oid],
                "review_state":"screened","human_verified":False,
                "mathematical_review_reason":reason,
                "source_screened_by":"assistant_independent_convex_falling_delta_bipartite_math_review_2026_10_20"})
            ind.append({"review_id":"review.wave2.bridge136."+suffix+("."+str(i) if len(forms)>1 else ""),
               "meaning_id":mid,"formulation_id":fid,"source_observation_id":oid,
               "source_locator":r["source"],"mathematical_reason":reason,
               "decision":"mathematically_screened_pending_individual_dependency_review",
               "human_verified":False,"production_corpus_used":False})
        meanings.append({"id":mid,"term_group_id":"wave2.bridge136."+key,
            "display_term":r["term"],"context":context,"term_ids":[tid],"formulations":rows,
            "editorial_status":"source_scoped_individually_mathematically_screened",
            "editorial_screening_reason":reason,"human_verified":False})
    if len(meanings)!=4 or len(ind)!=7:
        raise PipelineError("Four independently screened contexts and seven individual forms required")
    store(w.root/"wave2/bridge136_individual_mathematical_reviews.jsonl",ind)
    intake=store(w.root/"intake/bridge136_meanings.jsonl",meanings)
    old_ms=w.records("meanings")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    before=jsonl(ledger)
    if len(before) not in (632,639) or len({r["formulation_id"] for r in before})!=len(before):
        raise PipelineError("All 632 earlier formulation reviews must exist")
    if {i for r in before for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Previously source-reviewed 869 links not preserved")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_632_before_bridge136.jsonl"
    if len(old_ms)==591:
        if len(before)!=632 or any(r["meaning_catalog_digest"]!=digest(list(old_ms.values())) for r in before):
            raise PipelineError("Historical mathematical catalog digest differs")
        raw=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=raw:
            raise PipelineError("Historic 632-source formulation ledger altered")
        archive.write_text(raw,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_632_before_bridge136.json",
          {"rows":632,"prior_links":869,"sha256":hashlib.sha256(raw.encode()).hexdigest(),"human_peer_verified":False})
        w.ingest("meanings",intake,batch_size=4)
    ms=w.records("meanings")
    if len(ms)!=595 or any(ms.get(m["id"])!=m for m in meanings):
        raise PipelineError("Four independently scoped mathematical meanings not ingested")
    historic=jsonl(archive)
    if len(historic)!=632 or len({r["formulation_id"] for r in historic})!=632:
        raise PipelineError("Historical individual review snapshot absent")
    d=digest(list(ms.values()))
    updated=[dict(r,meaning_catalog_digest=d) for r in historic]
    for r in ind:
        updated.append({"formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
          "meaning_catalog_digest":d,"decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,"source":"independent_convex_falling_delta_bipartite_math_screen_batch136",
          "editorial_reason":"Individually source-screened mathematical meaning; separate prerequisite review pending.",
          "reviewed_by":None,"human_verified":False})
    if len(before)==639:
        if {r["formulation_id"]:r for r in before}!={r["formulation_id"]:r for r in updated}:
            raise PipelineError("Rerun would change existing source-screened mathematical reviews")
    else:atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);idx={r["formulation_id"]:r for r in final}
    if len(final)!=639 or len(idx)!=639:raise PipelineError("639 individual formulation reviews required")
    for r in historic:
        n=idx[r["formulation_id"]]
        if any(n.get(k)!=v for k,v in r.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Unrelated older mathematical decision altered")
    if dict(Counter(r["decision"] for r in final))!={"linked":626,"no_supported_target":6,"needs_review":7}:
        raise PipelineError("Unexpected historic or pending formulation decision distribution")
    check_cycles(ms,w.records("relations"))
    st=w.state("meanings")
    st.update(total=595,record_digest=d,screened_new_formulations=208,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",st)
    report={"batch":136,"screened_meanings":595,"reviewed_formulations":639,
      "new_contextual_meanings":4,"new_individual_formulations":7,
      "convex_set_two_equivalent_forms":True,"numeric_delta_two_equivalent_forms":True,
      "bipartite_two_equivalent_forms":True,
      "nonnegative_falling_factorial_zero_case_corroborated":True,
      "all_632_unrelated_reviews_and_869_links_preserved":True,
      "new_formulations_pending_link_review":7,
      "three_historical_held_source_errors_unpromoted":True,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch137 seven source-reviewed forms receive distinct direct prerequisite screens; Batch138 carefully backfill earlier convex hull and Stirling variants."}
    atomic_json(w.root/"state/wave2_bridge136_meaning_screen.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
