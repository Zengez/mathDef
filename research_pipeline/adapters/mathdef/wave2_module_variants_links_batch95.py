"""Batch 95: independently screen five module convention prerequisites.

Preserve the full 730-link graph. The historic submodule no-supported-target
review incorrectly missed the already independently sourced left module;
retain its previous decision as an explicit source-backed correction event.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":428,"observations":865,"meanings":530}
LEFT="meaning.wave2.foundation.left-module-nonunital"
RIGHT="meaning.wave2.module94.right-module-nonunital"
OLD="form.wave2.foundation76.submodule.01"
LEFT_URL="https://proofwiki.org/wiki/Definition%3AModule_over_Ring"
UNIT_URL="https://proofwiki.org/wiki/Definition%3AUnitary_Module_over_Ring"
SUB_URL="https://proofwiki.org/wiki/Definition%3ASubmodule"
ABEL_URL="https://proofwiki.org/wiki/Definition%3AAbelian_Group"
RING_URL="https://proofwiki.org/wiki/Definition%3ARing_%28Abstract_Algebra%29"
EDGES=(
 ("01","form.wave2.module94.right-module-nonunital",
  "meaning.wave2.foundation.abelian-group","abelian group",LEFT_URL,ABEL_URL,
  "The ordinary right module is built on an underlying additive abelian group. This independently sourced target specifies the commutative group law; a right scalar action adds distributivity and compatibility with ring multiplication, without requiring a multiplicative identity action."),
 ("02","form.wave2.module94.right-module-nonunital",
  "meaning.wave2.foundation.associative-ring-identity-optional","associative ring",LEFT_URL,RING_URL,
  "The independently screened abstract associative ring supplies the scalar-addition and multiplication operations and does not require a unit. This exactly matches the nonunital general right-module source convention; neither commutativity of R nor action of 1_R is silently assumed."),
 ("03","form.wave2.module94.unital-left-module",
  LEFT,"unital left R-module",UNIT_URL,LEFT_URL,
  "The unitary left module satisfies all ordinary left-action distribution and associative scalar-action axioms and additionally requires a ring identity satisfying 1_R m=m. The existing independent ordinary-left meaning supplies the strictly weaker underlying module structure."),
 ("04","form.wave2.module94.unital-right-module",
  RIGHT,"unital right R-module",UNIT_URL,LEFT_URL,
  "The unitary right module satisfies the ordinary right-action scalar laws and additionally imposes m1_R=m for a ring with identity. The independently screened nonunitary right-module meaning supplies precisely its underlying convention, without collapsing right and left actions."),
 ("05",OLD,LEFT,"left R-module",SUB_URL,LEFT_URL,
  "A submodule is defined as an additive subgroup and scalar-stable subset of an existing left R-module M. The independently sourced general-left module meaning already defines this ambient object, so it is a valid noncircular direct prerequisite; the earlier missing-target decision overlooked this existing entry.")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Historical mathematical link review disagrees")
    path.write_text(body,encoding="utf-8")
    return path
def source(form,obs):
    ids=form.get("evidence_ids",[])
    if len(ids)!=1 or ids[0] not in obs:
        raise PipelineError("Formulation-specific independent source unknown")
    return obs[ids[0]]["locator"]
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BASE,"relations")):
        raise PipelineError("Independent Wave 2 must be unsealed")
    if {s:len(w.records(s)) for s in BASE}!=BASE:
        raise PipelineError("Unexpected prior screen meanings/source state")
    meanings=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
    if len(forms)!=554:
        raise PipelineError("Expected 554 individually mathematical formulations")
    rel=w.records("relations")
    if len(rel) not in (730,735):
        raise PipelineError("Concurrent independent link inventory change")
    earlier={i:r for i,r in rel.items() if not i.startswith("rel.wave2.module95.")}
    if len(earlier)!=730:
        raise PipelineError("Historical 730 source-screened relations modified")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    previous=jsonl(ledger);idx={r["formulation_id"]:r for r in previous}
    if (len(previous)!=554 or len(idx)!=554 or
        any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in previous) or
        {rid for r in previous for rid in r["relation_ids"]}!=set(rel)):
        raise PipelineError("Full 554 historical review state not current")
    screened=[]
    for n,fid,target,phrase,sourceurl,targeturl,reason in EDGES:
        if fid not in forms or target not in meanings:
            raise PipelineError("Missing independently sourced mathematical concept "+n)
        m,form=forms[fid]
        if (form["review_state"]!="screened" or source(form,obs)!=sourceurl or
            locator(meanings[target],obs)!=targeturl or
            phrase not in form["text"] or len(reason)<185):
            raise PipelineError("Not individually sourced exact prerequisite "+n)
        screened.append({
          "id":"rel.wave2.module95."+n,"from_formulation":fid,
          "target_meaning":target,"relation_type":"definition_uses",
          "review_state":"screened","source_phrase":phrase,
          "source_locator":sourceurl,"target_locator":targeturl,
          "editorial_reason":reason,
          "reviewed_by":"assistant_independent_module_convention_link_review_2026_10_20",
          "human_verified":False
        })
    if len(screened)!=5:
        raise PipelineError("Five separate source-checked module dependencies required")
    check_cycles(meanings,{**earlier,**{r["id"]:r for r in screened}})
    pending={fid for fid in forms if fid.startswith("form.wave2.module94.")}
    if len(pending)!=3:
        raise PipelineError("Not precisely three newly screened module variants")
    snap=w.root/"state/wave2_formulation_reviews_snapshot_554_before_module95.jsonl"
    if len(rel)==730:
        if any(idx[fid]["decision"]!="needs_review" or idx[fid]["relation_ids"] for fid in pending):
            raise PipelineError("Module convention relation screens already changed")
        if idx[OLD]["decision"]!="no_supported_target" or idx[OLD]["relation_ids"]:
            raise PipelineError("Original submodule no-target decision must be archived")
        prev=ledger.read_text(encoding="utf-8")
        if snap.exists() and snap.read_text(encoding="utf-8")!=prev:
            raise PipelineError("Historic 554 individual review snapshot changed")
        snap.write_text(prev,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_554_before_module95.json",{
            "rows":554,"links":730,
            "sha256":hashlib.sha256(prev.encode("utf-8")).hexdigest(),
            "human_peer_verified":False
        })
    historical=jsonl(snap);older={r["formulation_id"]:r for r in historical}
    if len(historical)!=554 or len(older)!=554 or older[OLD]["decision"]!="no_supported_target":
        raise PipelineError("Prior submodule decision not preserved")
    event={
      "event_id":"module95.submodule.old-no-supported-target-to-existing-left-module",
      "formulation_id":OLD,
      "previous_review_digest":digest(older[OLD]),
      "previous_decision":"no_supported_target","new_decision":"linked",
      "previous_mathematical_reason":older[OLD]["editorial_reason"],
      "new_screened_link_id":"rel.wave2.module95.05",
      "reason":"Correction of an independently screened target lookup omission: the general left module had already been vetted and directly supplies the ambient object for submodules. The original absent-target reasoning is preserved verbatim.",
      "human_verified":False,"production_corpus_used":False
    }
    store(w.root/"events/submodule_missing_target_correction_batch95.jsonl",[event])
    store(w.root/"wave2/module95_individually_screened_links.jsonl",screened)
    file=store(w.root/"intake/module95_links.jsonl",screened)
    if len(rel)==730:
        w.ingest("relations",file,batch_size=5)
    current=w.records("relations")
    if len(current)!=735 or any(current.get(r["id"])!=r for r in screened):
        raise PipelineError("Screened new source-specific module links missing")
    check_cycles(meanings,current)
    reviews=[]
    for old in historical:
        newer=dict(old);fid=old["formulation_id"]
        if fid in pending|{OLD}:
            assigned=[r["id"] for r in screened if r["from_formulation"]==fid]
            if not assigned:
                raise PipelineError("Not all module/submodule formulations linked")
            newer["decision"]="linked"
            newer["relation_ids"]=assigned
            newer["source"]="independent_module_convention_prerequisite_review_batch95"
            newer["reviewed_by"]="assistant_independent_module_convention_link_review_2026_10_20"
            newer["editorial_reason"]="All exact source locations, action direction, and unit requirements individually checked; no graph cycles."
            if fid==OLD:
                newer["previous_review_digest"]=digest(older[OLD])
                newer["previous_wave2_decision"]="no_supported_target"
                newer["override_event_id"]=event["event_id"]
        reviews.append(newer)
    if len(rel)==735:
        if {r["formulation_id"]:r for r in reviews}!={r["formulation_id"]:r for r in previous}:
            raise PipelineError("Repeated link reviews disagree with previously committed history")
    else:
        atomic_jsonl(ledger,sorted(reviews,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);lookup={r["formulation_id"]:r for r in final}
    if len(final)!=554 or len(lookup)!=554:
        raise PipelineError("Screened mathematical review coverage incomplete")
    for fid,old in older.items():
        if fid not in pending|{OLD} and lookup[fid]!=old:
            raise PipelineError("Unrelated historical mathematical review was modified")
    if {rid for r in final for rid in r["relation_ids"]}!=set(current):
        raise PipelineError("Unreviewed source-screened graph link")
    counts=dict(Counter(r["decision"] for r in final))
    if counts!={"linked":548,"no_supported_target":6}:
        raise PipelineError("Unexpected final review disposition "+str(counts))
    report={
      "batch":95,"screened_meanings":530,"reviewed_formulations":554,
      "screened_relationships":735,"new_individual_links":5,
      "historic_730_links_preserved":True,
      "historic_550_unrelated_formulation_reviews_preserved":True,
      "old_submodule_no_target_explicitly_amended":True,
      "left_right_unital_nonunital_semantics_distinct":True,
      "all_554_formulations_individually_reviewed":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Widen independent discovery to unrelated branches; right and left module conventions completed with the original-left meaning unchanged. Consider a later UI alias normalization with explicit provenance."
    }
    atomic_json(w.root/"state/wave2_module95_link_review.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
