"""Batch124: retrospectively review six missing definition prerequisites.

Append source-reviewed edges to five older formulations without changing
any earlier edge, decision status, review rationale, source text or Wave1.
"""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":465,"observations":924,"meanings":577}
PW="https://proofwiki.org/wiki/Definition%3A"
NORMAL=PW+"Normal_Subgroup";QUOT=PW+"Quotient_Group";GEN=PW+"Generating_Function"
SUB=PW+"Subgroup";COSET=PW+"Coset";CONV=PW+"Convergent_Series";POWER=PW+"Power_Series/Real_Domain"
EDGES=(
 ("01","form.wave2.quot119.normal-subgroup.1","meaning.wave2.prereq122.subgroup","subgroup",NORMAL,SUB,
  "The normal-subgroup equal-cosets characterization explicitly assumes that N is already a subgroup N≤G. This newly independently sourced subgroup definition supplies the inherited group operation and subgroup condition before imposing normality."),
 ("02","form.wave2.quot119.normal-subgroup.2","meaning.wave2.prereq122.subgroup","subgroup",NORMAL,SUB,
  "Conjugation invariance defines normality only for a subgroup N of G. The previously missing standalone subgroup meaning now supplies inherited multiplication and subgroup axioms; ordinary normal subsets are not automatically groups."),
 ("03","form.wave2.quot119.normal-subgroup.3","meaning.wave2.prereq122.subgroup","subgroup",NORMAL,SUB,
  "The all-g conjugation inclusion criterion presupposes N≤G, not an arbitrary subset. The newly reviewed subgroup meaning supports that hypothesis, and the for-all-g quantifier is still needed for equivalence to equality."),
 ("04","form.wave2.quot119.quotient-group","meaning.wave2.prereq122.left-coset","left cosets",QUOT,COSET,
  "The quotient-group carrier G/N is the set of LEFT cosets gN, so the independently reviewed left-coset definition is a precise prerequisite. Normality is independently already linked and ensures product (aN)(bN)=(ab)N is representative-independent."),
 ("05","form.wave2.quot119.ordinary-real-ogf","meaning.wave2.prereq122.real-centered-power-series","∑",GEN,POWER,
  "The generating-function formula is obtained by evaluating a real power series with center ξ=0. The independently reviewed real centered power-series expression supplies coefficients and powers; convergence is a separate condition and not assumed at all real values."),
 ("06","form.wave2.quot119.ordinary-real-ogf","meaning.wave2.prereq122.real-series-convergent","converges",GEN,CONV,
  "The ordinary real generating function is defined exactly for z at which the numerical real series of terms a_n z^n converges. The new independently reviewed finite-partial-sum-limit definition supplies the convergence predicate without imposing absolute convergence.")
)
AFFECTED={e[1] for e in EDGES}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Independent historical review or backfill evidence changed")
    path.write_text(body,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BASE,"relations")):
        raise PipelineError("Independent unsealed Wave2 required")
    if {s:len(w.records(s)) for s in BASE}!=BASE:raise PipelineError("Batch123 mathematical meanings missing")
    done=json.loads((w.root/"state/wave2_prereq123_link_review.json").read_text())
    if done.get("screened_relationships")!=819 or done.get("reviewed_formulations")!=611:
        raise PipelineError("Batch123 reviewed baseline absent")
    missing=jsonl(w.root/"wave2/quot120_missing_prerequisite_target_candidates.jsonl")
    if len(missing)!=3:raise PipelineError("Original three explicit missing-target research records missing")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=611:raise PipelineError("611 original mathematical formulations not preserved")
    previous=w.records("relations")
    if len(previous) not in (819,825):raise PipelineError("Unexpected link graph baseline")
    historic={i:r for i,r in previous.items() if not i.startswith("rel.wave2.prereq124.")}
    if len(historic)!=819:raise PipelineError("All 819 previously reviewed relationships must be preserved")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    current=jsonl(ledger);index={r["formulation_id"]:r for r in current}
    if len(current)!=611 or len(index)!=611 or {i for r in current for i in r["relation_ids"]}!=set(previous):
        raise PipelineError("Previously complete formulation review ledger not preserved")
    if any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in current):
        raise PipelineError("Source-specific mathematical meaning catalog unexpectedly changed")
    reviewed=[]
    for n,fid,target,phrase,sourceurl,targeturl,reason in EDGES:
        if fid not in forms or target not in ms:raise PipelineError("Missing exact independent mathematical link endpoint "+n)
        _,f=forms[fid];e=f.get("evidence_ids",[])
        if (f["review_state"]!="screened" or len(e)!=1 or e[0] not in obs or
          obs[e[0]]["locator"]!=sourceurl or locator(ms[target],obs)!=targeturl or
          phrase not in f["text"] or len(reason)<150):
            raise PipelineError("Unsupported source phrase or target in retroactive review "+n)
        reviewed.append({"id":"rel.wave2.prereq124."+n,"from_formulation":fid,
          "target_meaning":target,"relation_type":"definition_uses","review_state":"screened",
          "source_phrase":phrase,"source_locator":sourceurl,"target_locator":targeturl,
          "editorial_reason":reason,
          "reviewed_by":"assistant_independent_subgroup_coset_series_retroactive_link_review_2026_10_20",
          "human_verified":False})
    if len(reviewed)!=6 or len(AFFECTED)!=5:
        raise PipelineError("Exactly six backfilled links to five existing formulations required")
    check_cycles(ms,{**historic,**{r["id"]:r for r in reviewed}})
    archive=w.root/"state/wave2_formulation_reviews_snapshot_611_before_prereq124.jsonl"
    if len(previous)==819:
        if any(index[fid]["decision"]!="linked" or not index[fid]["relation_ids"] for fid in AFFECTED):
            raise PipelineError("Prior individually linked forms not in expected reviewed state")
        content=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=content:
            raise PipelineError("Old 611-review history differs")
        archive.write_text(content,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_611_before_prereq124.json",{
          "rows":611,"prior_links":819,"sha256":hashlib.sha256(content.encode("utf-8")).hexdigest(),
          "human_peer_verified":False})
    saved=jsonl(archive);oldindex={r["formulation_id"]:r for r in saved}
    if len(saved)!=611 or len(oldindex)!=611:raise PipelineError("Historic complete prior review snapshot absent")
    store(w.root/"wave2/prereq124_individually_reviewed_retroactive_links.jsonl",reviewed)
    intake=store(w.root/"intake/prereq124_backfill_links.jsonl",reviewed)
    if len(previous)==819:w.ingest("relations",intake,batch_size=6)
    new_rel=w.records("relations")
    if len(new_rel)!=825 or any(new_rel.get(r["id"])!=r for r in reviewed):
        raise PipelineError("Six precise new source links not admitted")
    check_cycles(ms,new_rel)
    changed=[]
    for row in saved:
        r=dict(row)
        if r["formulation_id"] in AFFECTED:
            append=[e["id"] for e in reviewed if e["from_formulation"]==r["formulation_id"]]
            if not append or any(i in r["relation_ids"] for i in append):
                raise PipelineError("Duplicate or absent exact retroactive prerequisite")
            r["relation_ids"]=[*r["relation_ids"],*append]
        changed.append(r)
    if len(previous)==825:
        if {r["formulation_id"]:r for r in current}!={r["formulation_id"]:r for r in changed}:
            raise PipelineError("Repeat review would rewrite historic relations")
    else:atomic_jsonl(ledger,sorted(changed,key=lambda r:r["formulation_id"]))
    now=jsonl(ledger);ix={r["formulation_id"]:r for r in now}
    if len(now)!=611 or len(ix)!=611:raise PipelineError("611 individual form reviews required")
    for fid,r in oldindex.items():
        updated=ix[fid]
        if fid not in AFFECTED:
            if updated!=r:raise PipelineError("Unrelated old formulation decision changed")
        else:
            if any(updated.get(k)!=v for k,v in r.items() if k!="relation_ids"):
                raise PipelineError("Only appended IDs may change for prior reviewed forms")
            if updated["relation_ids"][:len(r["relation_ids"])]!=r["relation_ids"]:
                raise PipelineError("Original individual reviewed links were not kept in order")
    if {i for r in now for i in r["relation_ids"]}!=set(new_rel):
        raise PipelineError("Unreviewed relations after backfill")
    if dict(Counter(r["decision"] for r in now))!={"linked":605,"no_supported_target":6}:
        raise PipelineError("Unrelated individual formulation dispositions changed")
    for path in ("wave2/quot118_quarantined_source_claims.jsonl","wave2/directional112_quarantined_source_claims.jsonl"):
        held=jsonl(w.root/path)
        if len(held)!=1 or held[0]["observation_id"] in {eid for m in ms.values() for f in m["formulations"] for eid in f["evidence_ids"]}:
            raise PipelineError("Held incorrect source claim was accidentally promoted")
    result={"batch":124,"screened_meanings":577,"reviewed_formulations":611,"screened_relationships":825,
      "new_retrospectively_individually_reviewed_links":6,"prior_819_links_preserved":True,
      "all_611_previous_formulation_decisions_and_rationales_preserved":True,
      "five_existing_formulations_have_only_new_appended_relation_ids":True,
      "all_three_previous_dependency_target_gaps_reviewed":True,
      "normal_subgroup_requires_subgroup":True,"quotient_group_requires_left_coset":True,
      "ordinary_analytic_generating_function_uses_power_series_and_real_convergence":True,
      "both_held_source_errors_still_excluded":True,"dependency_graph_has_cycles":False,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch125 independent breadth discovery, plus further proof-quality audit without production corpus consultation."}
    atomic_json(w.root/"state/wave2_prereq124_retroactive_link_review.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
