"""Batch117: nine source-grounded group action, measure and partition links.

All prior 794 mathematical links and 594 unrelated individual formulation
dispositions are snapshotted and preserved. Generic engine remains unchanged.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":457,"observations":912,"meanings":568}
PW="https://proofwiki.org/wiki/Definition%3A"
ORBIT=PW+"Orbit_%28Group_Theory%29"
STAB=PW+"Stabilizer"
PUSH=PW+"Pushforward_Measure"
PART=PW+"Set_Partition"
ACTION="https://stacks.math.columbia.edu/tag/000T"
EQUIV=PW+"Equivalence_Relation"
MEASURE=PW+"Measure_%28Measure_Theory%29"
SPACE=PW+"Measurable_Space"
MAP=PW+"Mapping"
SUB=PW+"Subset"
F="form.wave2.group116."
M="meaning.wave2.group116."
EDGES=(
 ("01",F+"group-orbit.1","meaning.6a3d6fae0a1573e0.group-left-action","group acting",ORBIT,ACTION,
  "The orbit as the set {g·x:g∈G} of reached points is defined by the selected LEFT action of G on X. The independently sourced left group action supplies the identity and compatibility axioms; no right-action or group-size assumption is inferred."),
 ("02",F+"group-orbit.2","meaning.6a3d6fae0a1573e0.group-left-action","left G-action",ORBIT,ACTION,
  "The equivalence-class presentation defines the underlying relation specifically from a LEFT group action. The action axioms ensure reflexivity, symmetry and transitivity of this derived relation; without a specified action this is not the same orbit."),
 ("03",F+"group-orbit.2","meaning.wave2.set63.relation-reflexive-symmetric-transitive","equivalence relation",ORBIT,EQUIV,
  "The orbit of x as [x] is an equivalence class under the action-induced relation on X. The independently screened equivalence-relation meaning supplies exactly the reflexive, symmetric, transitive structure; the group action establishes these properties."),
 ("04",F+"group-stabilizer","meaning.6a3d6fae0a1573e0.group-left-action","G act on X",STAB,ACTION,
  "The stabilizer {g∈G:g·x=x} is action-dependent: changing the left G-action can change the fixing subgroup. The reviewed left group-action source supplies that action, while group closure is a theorem and not a separate defining hypothesis."),
 ("05",F+"measure-pushforward","meaning.wave2.foundation.nonnegative-measure","measure",PUSH,MEASURE,
  "The pushforward formula (f_*μ)(B)=μ(f⁻¹(B)) explicitly evaluates a nonnegative countably additive measure μ on measurable source sets. The independently screened nonnegative-measure target supplies this object, not probability normalization."),
 ("06",F+"measure-pushforward","meaning.wave2.prob90.measurable-space","measurable spaces",PUSH,SPACE,
  "Both domain (X,Σ) and target (Y,Τ) of the pushforward construction are measurable spaces with their own sigma-algebras. The source-specific preimage condition relies on the target events B belonging to Τ and their inverse images to Σ."),
 ("07",F+"measure-pushforward","meaning.wave2.foundation.mapping-element-assignment","measurable map",PUSH,MAP,
  "The pushforward uses a total single-valued map f:X→Y as part of its hypotheses, with measurable preimages as the additional required property. The independently sourced mapping meaning supplies the underlying typed assignment; a nonmeasurable map is insufficient."),
 ("08",F+"set-partition.1","meaning.wave2.foundation.subset-nonstrict","subsets",PART,SUB,
  "A partition into pairwise disjoint nonempty blocks is a collection of subsets B⊆S covering the base set S. The independently screened non-strict subset relation supplies each block's inclusion; no finite-set or nonempty-base requirement is added."),
 ("09",F+"set-partition.2","meaning.wave2.foundation.subset-nonstrict","subsets",PART,SUB,
  "The equivalent unique-containing-block formulation quantifies over nonempty subsets B⊆S and each s∈S. It therefore also depends on the general subset relation; the empty S admits the empty partition with both formulations valid.")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    text="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=text:
        raise PipelineError("Individual screened source relationship history changed")
    path.write_text(text,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in (*BASE,"relations")):
        raise PipelineError("Unsealed independent Wave2 required")
    if {k:len(w.records(k)) for k in BASE}!=BASE:
        raise PipelineError("Previous verified Batch116 mathematics inventory missing")
    review=json.loads((w.root/"state/wave2_group116_meaning_screen.json").read_text())
    if review.get("screened_meanings")!=568 or review.get("reviewed_formulations")!=600 or not review.get("orbit_equivalent_forms_one_meaning"):
        raise PipelineError("Batch116 individual mathematical source screens unverified")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=600:
        raise PipelineError("Expected six hundred individually screened formulations")
    before_rel=w.records("relations")
    if len(before_rel) not in (794,803):
        raise PipelineError("Historic relation count differs")
    historical={id:r for id,r in before_rel.items() if not id.startswith("rel.wave2.group117.")}
    if len(historical)!=794:
        raise PipelineError("All 794 previously screened relationships must be preserved")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    before=jsonl(ledger);oldindex={r["formulation_id"]:r for r in before}
    if (len(before)!=600 or len(oldindex)!=600 or
      any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in before) or
      {i for r in before for i in r["relation_ids"]}!=set(before_rel)):
        raise PipelineError("Complete previous 600 individual mathematical reviews required")
    checked=[]
    for n,fid,target,phrase,srcurl,tgturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Exact independently screened source/target missing "+n)
        meaning,form=forms[fid];ids=form.get("evidence_ids",[])
        if (form["review_state"]!="screened" or len(ids)!=1 or ids[0] not in obs or
          obs[ids[0]]["locator"]!=srcurl or locator(ms[target],obs)!=tgturl or
          phrase not in form["text"] or len(reason)<150):
            raise PipelineError("Insufficient direct source phrase and prerequisite scope "+n)
        checked.append({"id":"rel.wave2.group117."+n,"from_formulation":fid,
          "target_meaning":target,"relation_type":"definition_uses",
          "review_state":"screened","source_phrase":phrase,"source_locator":srcurl,
          "target_locator":tgturl,"editorial_reason":reason,
          "reviewed_by":"assistant_independent_group_measure_partition_direct_link_review_2026_10_20",
          "human_verified":False})
    fresh={fid for fid in forms if fid.startswith(F)}
    if len(fresh)!=6 or len(checked)!=9 or {e["from_formulation"] for e in checked}!=fresh:
        raise PipelineError("Nine screened prerequisite links must cover all six new forms")
    check_cycles(ms,{**historical,**{r["id"]:r for r in checked}})
    archive=w.root/"state/wave2_formulation_reviews_snapshot_600_before_group117.jsonl"
    if len(before_rel)==794:
        if any(oldindex[fid]["decision"]!="needs_review" or oldindex[fid]["relation_ids"] for fid in fresh):
            raise PipelineError("New individual formulations already marked as reviewed")
        old=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=old:
            raise PipelineError("Historical 600 decision snapshot changed")
        archive.write_text(old,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_600_before_group117.json",{
          "rows":600,"historical_relations":794,"sha256":hashlib.sha256(old.encode("utf-8")).hexdigest(),"human_peer_verified":False})
    saved=jsonl(archive);savedindex={r["formulation_id"]:r for r in saved}
    if len(saved)!=600 or len(savedindex)!=600:
        raise PipelineError("Historical individual source review snapshots absent")
    store(w.root/"wave2/group117_individually_source_screened_links.jsonl",checked)
    inputfile=store(w.root/"intake/group117_links.jsonl",checked)
    if len(before_rel)==794:
        w.ingest("relations",inputfile,batch_size=9)
    rel=w.records("relations")
    if len(rel)!=803 or any(rel.get(r["id"])!=r for r in checked):
        raise PipelineError("Nine reviewed mathematical prerequisites not present")
    check_cycles(ms,rel)
    revisions=[]
    for original in saved:
        r=dict(original);fid=r["formulation_id"]
        if fid in fresh:
            linked=[link["id"] for link in checked if link["from_formulation"]==fid]
            if not linked:raise PipelineError("New individual form lacks screened prerequisite "+fid)
            r["relation_ids"]=linked;r["decision"]="linked"
            r["reviewed_by"]="assistant_independent_group_measure_partition_direct_link_review_2026_10_20"
            r["source"]="independent_group_action_pushforward_partition_dependency_review_batch117"
            r["editorial_reason"]="Precise source-specific mathematical dependencies checked; prior reviews and frozen source corpus protected."
        revisions.append(r)
    if len(before_rel)==803:
        if {r["formulation_id"]:r for r in before}!={r["formulation_id"]:r for r in revisions}:
            raise PipelineError("Rerun would change reviewed formulation relationship assignments")
    else:
        atomic_jsonl(ledger,sorted(revisions,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);idx={r["formulation_id"]:r for r in final}
    if len(final)!=600 or len(idx)!=600:
        raise PipelineError("Every one of 600 mathematical forms requires disposition")
    for fid,p in savedindex.items():
        if fid not in fresh and idx[fid]!=p:
            raise PipelineError("Unrelated historical mathematical decision altered")
    if {id for r in final for id in r["relation_ids"]}!=set(rel):
        raise PipelineError("Unreviewed link or missing individual link disposition")
    if dict(Counter(r["decision"] for r in final))!={"linked":594,"no_supported_target":6}:
        raise PipelineError("600-review disposition split wrong")
    held=jsonl(w.root/"wave2/directional112_quarantined_source_claims.jsonl")
    if len(held)!=1 or held[0]["observation_id"] in {e for m in ms.values() for f in m["formulations"] for e in f["evidence_ids"]}:
        raise PipelineError("Earlier unsafe directional source quarantine altered")
    result={"batch":117,"screened_meanings":568,"reviewed_formulations":600,
      "screened_relationships":803,"new_individual_links":9,
      "all_794_prior_mathematical_links_preserved":True,
      "all_594_unrelated_individual_reviews_preserved":True,
      "all_six_new_formulations_separately_link_reviewed":True,
      "group_orbit_action_orientation_explicit":True,
      "stabilizer_depends_on_action":True,"pushforward_requires_measurability":True,
      "set_partition_empty_base_convention_retained":True,
      "held_directional_gradient_source_excluded":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch118 broaden independent source-rich mathematical discovery outside orbit, stabilizer, partition and measure pushforward."}
    atomic_json(w.root/"state/wave2_group117_link_review.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
