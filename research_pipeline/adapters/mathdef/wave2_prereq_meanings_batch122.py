"""Batch122: five rigorously distinct subgroup/coset/series mathematical contexts."""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/subgroup_coset_real_series_source_batch121_2026-10-20.jsonl"
BASE={"sources":14,"terms":465,"observations":924,"meanings":572,"relations":811}
AFTER=dict(BASE,meanings=577)
SPECS=(
 ("subgroup",0,"subgroup","Subgroup with inherited operation of an ambient group"),
 ("coset",0,"left-coset","Left coset gH of a subgroup in a group"),
 ("coset",1,"right-coset","Right coset Hg of a subgroup in a group"),
 ("convergent-real-series",0,"real-series-convergent","Real infinite series with finite limit of partial sums"),
 ("real-power-series",0,"real-centered-power-series","Real coefficient power series about specified real center, convergence not assumed")
)
def store(path,items):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(x)+"\n" for x in items)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Previously mathematically reviewed source formulation changed")
    path.write_text(body,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Independent unsealed Wave2 needed")
    if {k:len(w.records(k)) for k in BASE} not in (BASE,AFTER):
        raise PipelineError("Verified B121 source baseline missing")
    report=json.loads((w.root/"state/wave2_prereq121_source_intake.json").read_text())
    if report.get("new_source_headings")!=4 or report.get("new_source_observations")!=5 or not report.get("coset_handedness_separate"):
        raise PipelineError("Source intake / coset orientation review missing")
    research={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    termdb=w.records("terms");obs=w.records("observations")
    added=[];screens=[]
    for key,cidx,suffix,context in SPECS:
        r=research[key];tid="term.wave2.prereq121."+key
        if termdb.get(tid,{}).get("locator")!=r["source"] or r["production_corpus_consulted"]:
            raise PipelineError("Source/term provenance mismatch "+suffix)
        c=r["contexts"][cidx];fs=c["forms"]
        if len(fs)!=1 or len(r["review"])<280:raise PipelineError("Individual mathematical context source review missing "+suffix)
        f=fs[0];s=f["text"];reason=r["review"]
        if key=="subgroup" and ("restriction" not in s or "itself a group" not in s):
            raise PipelineError("Subgroup inherited operation missing")
        if key=="coset":
            if cidx==0 and "gH={gh:h∈H}" not in s:raise PipelineError("Left coset orientation mismatch")
            if cidx==1 and "Hg={hg:h∈H}" not in s:raise PipelineError("Right coset orientation mismatch")
            reason+=" Left and right coset definitions share a term but remain different group-action handedness contexts."
        if key=="convergent-real-series" and ("partial sums" not in s or "s∈ℝ" not in s):
            raise PipelineError("Real finite-limit condition absent")
        if key=="real-power-series" and ("convergence at x is not assumed" not in s or "ξ∈ℝ" not in s):
            raise PipelineError("Centered expression and convergence distinction absent")
        oid=f"obs.wave2.prereq121.{key}.{cidx+1:02d}"
        o=obs.get(oid)
        if not o or o["locator"]!=r["source"] or o["term_id"]!=tid or o["text"]!=s:
            raise PipelineError("Individual original source observation missing "+oid)
        mid="meaning.wave2.prereq122."+suffix
        fid="form.wave2.prereq122."+suffix
        form={"id":fid,"text":s,"evidence_ids":[oid],"review_state":"screened",
           "human_verified":False,"mathematical_review_reason":reason,
           "source_screened_by":"assistant_independent_subgroup_coset_real_series_mathematical_review_2026_10_20"}
        added.append({"id":mid,"term_group_id":"wave2.prereq122."+key,"display_term":r["term"],
          "context":context,"term_ids":[tid],"formulations":[form],
          "editorial_status":"source_scoped_individually_mathematically_screened",
          "editorial_screening_reason":reason,"human_verified":False})
        screens.append({"review_id":"review.wave2.prereq122."+suffix,"meaning_id":mid,
          "formulation_id":fid,"source_observation_id":oid,"source_locator":r["source"],
          "mathematical_reason":reason,
          "decision":"mathematically_screened_pending_individual_prerequisite_review",
          "human_verified":False,"production_corpus_used":False})
    if len(added)!=len(screens)!=5:raise PipelineError("Exactly five source-backed scoped meanings required")
    store(w.root/"wave2/prereq122_individual_mathematical_reviews.jsonl",screens)
    intake=store(w.root/"intake/prereq122_meanings.jsonl",added)
    ms=w.records("meanings");ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prior=jsonl(ledger)
    if len(prior) not in (606,611) or len({r["formulation_id"] for r in prior})!=len(prior):
        raise PipelineError("606 historical formulation-specific mathematical decisions expected")
    if {i for r in prior for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("All 811 old relationships must have individual reviews")
    snap=w.root/"state/wave2_formulation_reviews_snapshot_606_before_prereq122.jsonl"
    if len(ms)==572:
        if len(prior)!=606 or any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in prior):
            raise PipelineError("Prior mathematical catalog digest unexpectedly changed")
        body=ledger.read_text(encoding="utf-8")
        if snap.exists() and snap.read_text(encoding="utf-8")!=body:
            raise PipelineError("Prior formulation review history changed")
        snap.write_text(body,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_606_before_prereq122.json",
           {"rows":606,"prior_links":811,"sha256":hashlib.sha256(body.encode()).hexdigest(),"human_peer_verified":False})
        w.ingest("meanings",intake,batch_size=5)
    meanings=w.records("meanings")
    if len(meanings)!=577 or any(meanings.get(r["id"])!=r for r in added):
        raise PipelineError("Five meaning contexts were not admitted")
    historic=jsonl(snap)
    if len(historic)!=606 or len({r["formulation_id"] for r in historic})!=606:
        raise PipelineError("Historical 606 review snapshot missing")
    d=digest(list(meanings.values()))
    updated=[dict(r,meaning_catalog_digest=d) for r in historic]
    for r in screens:
        updated.append({"formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
          "meaning_catalog_digest":d,"decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,"source":"independent_subgroup_coset_series_math_screen_batch122",
          "editorial_reason":"Definition sourced and mathematically scoped; individual dependency review pending.",
          "reviewed_by":None,"human_verified":False})
    if len(prior)==611:
        if {r["formulation_id"]:r for r in prior}!={r["formulation_id"]:r for r in updated}:
            raise PipelineError("Repeat would alter previous individual reviews")
    else:atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);index={r["formulation_id"]:r for r in final}
    if len(final)!=611 or len(index)!=611:raise PipelineError("611 individually reviewed or pending forms required")
    for r in historic:
        x=index[r["formulation_id"]]
        if any(x.get(k)!=v for k,v in r.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Older individual disposition altered")
    if dict(Counter(r["decision"] for r in final))!={"linked":600,"no_supported_target":6,"needs_review":5}:
        raise PipelineError("Unexpected pending/complete review decisions")
    check_cycles(meanings,w.records("relations"))
    state=w.state("meanings");state.update(total=577,record_digest=d,screened_new_formulations=180,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    result={"batch":122,"screened_meanings":577,"reviewed_formulations":611,
       "new_contextual_meanings":5,"new_source_formulations":5,
       "left_and_right_coset_meanings_distinct":True,
       "subgroup_inherited_operation_explicit":True,
       "series_convergence_and_power_series_expression_distinct":True,
       "all_606_old_reviews_and_811_links_preserved":True,
       "new_forms_pending_link_review":5,
       "both_historically_held_source_claims_not_promoted":True,
       "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
       "next":"Batch123 individual source-scoped prerequisites for five screened mathematical formulations."}
    atomic_json(w.root/"state/wave2_prereq122_meaning_screen.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
