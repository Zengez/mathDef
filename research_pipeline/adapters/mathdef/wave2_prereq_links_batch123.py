"""Batch123 individually verify eight direct subgroup/coset/real-series links.

Keep 811 historic links, 606 prior form reviews, and both held source claims.
No invented reverse links to earlier normal/quotient/generating forms.
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
SUB=PW+"Subgroup";COSET=PW+"Coset";CONV=PW+"Convergent_Series"
POWER=PW+"Power_Series/Real_Domain";GROUP=PW+"Group";SET=PW+"Subset";REAL=PW+"Real_Number"
F="form.wave2.prereq122."
M="meaning.wave2.prereq122."
EDGES=(
 ("01",F+"subgroup","meaning.wave2.foundation.group","group",SUB,GROUP,
  "A subgroup is a subgroup of an AMBIENT GROUP G and inherits the same group operation. The independently screened group axioms give associativity, identity and inverse, with closure and inherited operation required on H."),
 ("02",F+"subgroup","meaning.wave2.foundation.subset-nonstrict","H⊆G",SUB,SET,
  "A subgroup H is first a subset H⊆G equipped with the ambient operation, and may equal G. The separately sourced non-strict subset relation provides exact inclusion; no proper-subgroup requirement is presumed."),
 ("03",F+"left-coset",M+"subgroup","subgroup",COSET,SUB,
  "The left coset gH presupposes subgroup H≤G of the acting ambient group, not merely an arbitrary subset with an operation. This independently reviewed subgroup meaning supplies that specific group-theoretic prerequisite."),
 ("04",F+"left-coset","meaning.wave2.foundation.group","group G",COSET,GROUP,
  "The left coset gH={gh:h∈H} uses multiplication of an ambient group G, with g on the LEFT. The source's more general algebraic-structure usage was deliberately narrowed to groups and no commutativity is asserted."),
 ("05",F+"right-coset",M+"subgroup","subgroup",COSET,SUB,
  "The right coset Hg presupposes a subgroup H≤G under the inherited operation. This source-specific subgroup prerequisite does not identify Hg with gH unless H is normal."),
 ("06",F+"right-coset","meaning.wave2.foundation.group","group G",COSET,GROUP,
  "The right coset Hg={hg:h∈H} requires ambient group multiplication with g on the RIGHT. Keeping operand order prevents silently conflating left/right cosets in nonabelian groups."),
 ("07",F+"real-series-convergent","meaning.wave2.real45.complete-ordered-real-field","ℝ",CONV,REAL,
  "Convergence of a real series is a finite real limit of its finite partial sums. The independently screened real ordered number system supplies the scalar field in which sums and their finite limiting values lie; extended infinite limits do not count."),
 ("08",F+"real-centered-power-series","meaning.wave2.real45.complete-ordered-real-field","ℝ",POWER,REAL,
  "A real centered power series has real center, real coefficients and real variable. Its unevaluated series expression does NOT assume convergence for all real x; the separately screened real-number meaning supplies the coefficient/center field.")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Historical individual source-to-meaning screening differs")
    path.write_text(body,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BASE,"relations")):
        raise PipelineError("Requires unsealed independent Wave2")
    if {s:len(w.records(s)) for s in BASE}!=BASE:
        raise PipelineError("Expected Batch122 mathematical source-screened contexts")
    mreport=json.loads((w.root/"state/wave2_prereq122_meaning_screen.json").read_text())
    if mreport.get("screened_meanings")!=577 or mreport.get("reviewed_formulations")!=611 or not mreport.get("left_and_right_coset_meanings_distinct"):
        raise PipelineError("Verified 122 mathematical review missing")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=611:raise PipelineError("611 source-screened mathematical formulations required")
    prior_links=w.records("relations")
    if len(prior_links) not in (811,819):
        raise PipelineError("Unexpected prior mathematical link count")
    historical={i:r for i,r in prior_links.items() if not i.startswith("rel.wave2.prereq123.")}
    if len(historical)!=811:raise PipelineError("All 811 previously screened links must be preserved")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    before=jsonl(ledger);index={r["formulation_id"]:r for r in before}
    if (len(before)!=611 or len(index)!=611 or
      any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in before) or
      {i for r in before for i in r["relation_ids"]}!=set(prior_links)):
        raise PipelineError("Full current individual formulation history invalid")
    checks=[]
    for n,fid,target,phrase,sourceurl,targeturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Independently reviewed mathematical endpoint absent "+n)
        _,fm=forms[fid];evid=fm.get("evidence_ids",[])
        if (fm["review_state"]!="screened" or len(evid)!=1 or evid[0] not in obs
           or obs[evid[0]]["locator"]!=sourceurl or locator(ms[target],obs)!=targeturl
           or phrase not in fm["text"] or len(reason)<145):
            raise PipelineError("Unverified exact source phrase or target for dependency "+n)
        checks.append({"id":"rel.wave2.prereq123."+n,"from_formulation":fid,
          "target_meaning":target,"relation_type":"definition_uses",
          "review_state":"screened","source_phrase":phrase,
          "source_locator":sourceurl,"target_locator":targeturl,
          "editorial_reason":reason,"reviewed_by":"assistant_independent_subgroup_coset_series_link_review_2026_10_20",
          "human_verified":False})
    fresh={fid for fid in forms if fid.startswith(F)}
    if len(fresh)!=5 or len(checks)!=8 or {r["from_formulation"] for r in checks}!=fresh:
        raise PipelineError("Every new form must receive individualized mathematical prerequisite review")
    check_cycles(ms,{**historical,**{r["id"]:r for r in checks}})
    archive=w.root/"state/wave2_formulation_reviews_snapshot_611_before_prereq123.jsonl"
    if len(prior_links)==811:
        if any(index[fid]["decision"]!="needs_review" or index[fid]["relation_ids"] for fid in fresh):
            raise PipelineError("New formulations have unexpected pre-reviewed status")
        body=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=body:
            raise PipelineError("Historical review snapshot changed")
        archive.write_text(body,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_611_before_prereq123.json",
          {"rows":611,"prior_links":811,"sha256":hashlib.sha256(body.encode()).hexdigest(),"human_peer_verified":False})
    past=jsonl(archive);old={r["formulation_id"]:r for r in past}
    if len(past)!=611 or len(old)!=611:raise PipelineError("Archived historical review ledger missing")
    store(w.root/"wave2/prereq123_individual_source_screened_links.jsonl",checks)
    intake=store(w.root/"intake/prereq123_links.jsonl",checks)
    if len(prior_links)==811:w.ingest("relations",intake,batch_size=8)
    rel=w.records("relations")
    if len(rel)!=819 or any(rel.get(r["id"])!=r for r in checks):
        raise PipelineError("Eight screened relations not present")
    check_cycles(ms,rel)
    new=[]
    for p in past:
        row=dict(p);fid=row["formulation_id"]
        if fid in fresh:
            ids=[x["id"] for x in checks if x["from_formulation"]==fid]
            if not ids:raise PipelineError("New source formulation lacks link")
            row["relation_ids"]=ids;row["decision"]="linked"
            row["reviewed_by"]="assistant_independent_subgroup_coset_series_link_review_2026_10_20"
            row["source"]="independent_subgroup_coset_series_direct_links_batch123"
            row["editorial_reason"]="Individually reviewed exact mathematical source/target, preserving all older edges."
        new.append(row)
    if len(prior_links)==819:
        if {r["formulation_id"]:r for r in before}!={r["formulation_id"]:r for r in new}:
            raise PipelineError("Rerun would modify completed math screening decisions")
    else:atomic_jsonl(ledger,sorted(new,key=lambda r:r["formulation_id"]))
    now=jsonl(ledger);ix={r["formulation_id"]:r for r in now}
    if len(now)!=611 or len(ix)!=611:raise PipelineError("611 completed form review decisions required")
    for fid,p in old.items():
        if fid not in fresh and ix[fid]!=p:
            raise PipelineError("Older unrelated formulation decision altered")
    if {i for r in now for i in r["relation_ids"]}!=set(rel):
        raise PipelineError("Unscreened dependency relation remains")
    if dict(Counter(r["decision"] for r in now))!={"linked":605,"no_supported_target":6}:
        raise PipelineError("Formulation review disposition distribution mismatch")
    for path in ("wave2/quot118_quarantined_source_claims.jsonl","wave2/directional112_quarantined_source_claims.jsonl"):
        held=jsonl(w.root/path)
        if len(held)!=1 or held[0]["observation_id"] in {eid for m in ms.values() for f in m["formulations"] for eid in f["evidence_ids"]}:
            raise PipelineError("Previously source-held mathematical error was promoted")
    gaps={"reviewed_new_targets":["subgroup","left-coset","right-coset","convergent-real-series","real-power-series"],
       "earlier_missing_dependency_review_can_now_resume":True,
       "retroactive_links_not_added_this_batch":True,
       "recommended_next":"Individually re-review prior normal-subgroup/quotient-group/OGF formulations to new target meanings without altering any old decisions, then independently screen related broader definitions."}
    atomic_json(w.root/"state/wave2_prereq123_backfill_recommendation.json",gaps)
    result={"batch":123,"screened_meanings":577,"reviewed_formulations":611,
      "screened_relationships":819,"new_individual_links":8,
      "all_prior_811_links_preserved":True,
      "all_606_unrelated_reviews_preserved":True,
      "all_five_new_forms_individually_linked":True,
      "coset_orientation_remains_distinct":True,
      "real_power_series_not_assumed_convergent_everywhere":True,
      "backfill_of_earlier_dependency_targets_explicitly_deferred":True,
      "both_historically_held_source_claims_excluded":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch124 individually reviewed retroactive links to newly source-screened subgroup/coset/convergent real series concepts, preserving earlier decisions, then breadth expansion."}
    atomic_json(w.root/"state/wave2_prereq123_link_review.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
