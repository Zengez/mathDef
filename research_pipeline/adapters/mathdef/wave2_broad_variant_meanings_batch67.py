"""Wave 2 Batch 67: audited meaning refinement, never duplicate σ-algebra.

One screened formulation is appended to the *existing* independent
sigma-algebra meaning; a distinct compact-space terminological context
receives two formulations. Original production content is never read.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
REVIEW="wave2/broad_source_variant_reviews_batch65_2026-10-20.jsonl"
PRE={"sources":14,"terms":408,"observations":834,"meanings":508,"relations":691}
POST=dict(PRE,meanings=509)
SIGMA_ID="meaning.wave2.foundation.sigma-algebra"
COMPACT_ID="meaning.wave2.broad67.compact-topological-space"
COMPACT_GROUP="wave2.broad67.compact-topological-space"
SIGMA_TERM="term.wave2.broad66.sigma-algebra"
COMPACT_TERM="term.wave2.broad66.compact-space"
SIGMA_ALT_ID="form.wave2.broad67.sigma-difference-disjoint-countable"
COMPACT_FORM_IDS=[
 "form.wave2.broad67.compact-open-cover",
 "form.wave2.broad67.compact-closed-fip"
]
def store(path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    s="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=s:
        raise PipelineError("Previous reviewed variant batch changed")
    path.write_text(s,encoding="utf-8")
    return path
def source_form(id,text,obs,reason):
    return {
      "id":id,"text":text,"evidence_ids":[obs],"review_state":"screened",
      "human_verified":False,"source_screened_by":"assistant_independent_variant_mathematical_screen_batch67_2026_10_20",
      "editorial_review_reason":reason
    }
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in PRE):
        raise PipelineError("Requires unsealed independent Wave 2")
    counts={s:len(w.records(s)) for s in PRE}
    if counts not in (PRE,POST):
        raise PipelineError("Unexpected mathematical source/review baseline "+str(counts))
    candidates={r["id"]:r for r in jsonl(w.root/REVIEW)}
    sigma=candidates.get("wave2.batch65.sigma-algebra")
    compact=candidates.get("wave2.batch65.compact-space")
    if not sigma or not compact or len(sigma["formulations"])!=2 or len(compact["formulations"])!=2:
        raise PipelineError("Full independent alternative source review absent")
    originals=w.records("meanings")
    prev_sigma=originals.get(SIGMA_ID)
    if not prev_sigma or COMPACT_TERM not in w.records("terms") or SIGMA_TERM not in w.records("terms"):
        raise PipelineError("Existing meaning or term not source-reviewed")
    observations=w.records("observations")
    for term,key in ((SIGMA_TERM,"sigma-algebra"),(COMPACT_TERM,"compact-space")):
        for i in (1,2):
            oid=f"obs.wave2.broad66.{key}.{i:02d}"
            o=observations.get(oid)
            if not o or o["term_id"]!=term or o["source_id"]!="src.proofwiki":
                raise PipelineError("Alternative formulation lacks independently sourced observation: "+oid)
    original_forms=prev_sigma["formulations"]
    if not original_forms or original_forms[0]["id"]!="form.wave2.foundation.sigma-algebra":
        raise PipelineError("Existing independently screened sigma meaning does not match")
    if len(original_forms) not in (1,2):
        raise PipelineError("Unexpected additional sigma-algebra variants require comparison")
    old_sigma={
        **{k:v for k,v in prev_sigma.items() if k!="variant_refinement_note"},
        "term_ids":["term.wave2.foundation26.sigma-algebra"],
        "formulations":[original_forms[0]]
    }
    if len(sigma["mathematical_review"])<275 or len(compact["mathematical_review"])<275:
        raise PipelineError("Mathematical equivalence rationale insufficient")
    sigma_alt=source_form(SIGMA_ALT_ID,sigma["formulations"][1]["text"],
      "obs.wave2.broad66.sigma-algebra.02",
      sigma["mathematical_review"]+" This is equivalent to the existing standard complement-and-countable-union formulation by finite Boolean closure and disjointification.")
    sigma_new={
        **old_sigma,
        "term_ids":old_sigma["term_ids"]+[SIGMA_TERM],
        "formulations":[original_forms[0],sigma_alt],
        "variant_refinement_note":"Additional independently sourced equivalent axioms for the same set-system meaning; the original screened formulation is preserved."
    }
    compact_forms=[
       source_form(COMPACT_FORM_IDS[i],compact["formulations"][i]["text"],
         f"obs.wave2.broad66.compact-space.{i+1:02d}",
         compact["mathematical_review"]+" Equivalence follows by taking complements of covers/closed families.")
       for i in range(2)
    ]
    compact_meaning={
      "id":COMPACT_ID,"term_group_id":COMPACT_GROUP,
      "display_term":"compact topological space",
      "context":"General topology: compactness by finite open subcovers or closed-set finite intersection property; no Hausdorff assumption",
      "term_ids":[COMPACT_TERM],
      "editorial_status":"individually_source_scoped_equivalent_formulations",
      "editorial_screening_reason":compact["mathematical_review"],
      "terminology_note":"In this convention compact is equivalent to quasi-compact; in some sources compact additionally requires Hausdorff. The existing independent quasi-compact entry is retained for contextual searching.",
      "human_verified":False,"formulations":compact_forms
    }
    if prev_sigma!=old_sigma and prev_sigma!=sigma_new:
        raise PipelineError("Existing sigma meaning changed outside controlled review")
    if COMPACT_ID in originals and originals[COMPACT_ID]!=compact_meaning:
        raise PipelineError("Existing compactness meaning differs")
    individual=[
      {"review_id":"review.wave2.broad67.sigma","meaning_id":SIGMA_ID,
       "formulation_id":SIGMA_ALT_ID,"source_observation_id":"obs.wave2.broad66.sigma-algebra.02",
       "mathematical_reason":sigma_alt["editorial_review_reason"],
       "decision":"screened_equivalent_variant_pending_link_review","human_verified":False},
      *[
       {"review_id":f"review.wave2.broad67.compact.{i+1}",
        "meaning_id":COMPACT_ID,"formulation_id":form["id"],
        "source_observation_id":form["evidence_ids"][0],
        "mathematical_reason":form["editorial_review_reason"],
        "decision":"screened_equivalent_variant_pending_link_review",
        "human_verified":False}
       for i,form in enumerate(compact_forms)
      ]
    ]
    store(w.root/"wave2/broad_individual_variant_reviews_batch67.jsonl",individual)
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    old_review_rows=jsonl(ledger)
    oldreview={r["formulation_id"]:r for r in old_review_rows}
    if len(old_review_rows) not in (521,524) or len(oldreview)!=len(old_review_rows):
        raise PipelineError("Historical formulation review coverage differs")
    if {rid for r in old_review_rows for rid in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Old source-reviewed links not accounted")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_521_before_broad67.jsonl"
    meaning_archive=w.root/"events/sigma_algebra_meaning_before_broad67.jsonl"
    if len(old_review_rows)==521:
        if any(r["meaning_catalog_digest"]!=digest(list(originals.values())) for r in old_review_rows):
            raise PipelineError("Historical meaning version digest mismatch")
        old_text=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=old_text:
            raise PipelineError("Review archive conflict")
        archive.write_text(old_text,encoding="utf-8")
        store(meaning_archive,[old_sigma])
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_521_before_broad67.json",{
           "rows":521,"relationships":691,"sha256":hashlib.sha256(old_text.encode("utf-8")).hexdigest(),
           "human_peer_verified":False
        })
    prior=jsonl(archive)
    if len(prior)!=521 or len({r["formulation_id"] for r in prior})!=521:
        raise PipelineError("Missing immutable pre-variant review snapshot")
    stored_old=jsonl(meaning_archive)
    if stored_old!=[old_sigma]:
        raise PipelineError("Old sigma meaning historical snapshot changed")
    event={
      "event_id":"broad67.sigma-existing-meaning-add-equivalent-formulation",
      "meaning_id":SIGMA_ID,"previous_meaning_digest":digest(old_sigma),
      "new_meaning_digest":digest(sigma_new),
      "added_formulation_id":SIGMA_ALT_ID,
      "added_source_term":SIGMA_TERM,
      "prior_screened_formulation_preserved":True,
      "mathematical_reason":sigma_alt["editorial_review_reason"],
      "source_review":"wave2.batch65.sigma-algebra",
      "human_verified":False,"production_corpus_used":False
    }
    store(w.root/"events/sigma_algebra_equivalent_variant_amendment_batch67.jsonl",[event])
    if COMPACT_ID not in originals:
        w.ingest("meanings",
          store(w.root/"intake/compact_topology_meaning_batch67.jsonl",[compact_meaning]),batch_size=1)
    now=w.records("meanings")
    if len(now)!=509:
        raise PipelineError("Expected one new compact topological context")
    if now[SIGMA_ID]==old_sigma:
        revised=[sigma_new if m["id"]==SIGMA_ID else m for m in now.values()]
        for meaning in revised:
            w.validate("meanings",meaning)
        atomic_jsonl(w.root/"records/meanings.jsonl",revised)
        now=w.records("meanings")
    if now[SIGMA_ID]!=sigma_new or now[COMPACT_ID]!=compact_meaning:
        raise PipelineError("Audited sigma/compact variant refinement not reflected")
    version=digest(list(now.values()))
    history=[dict(r,meaning_catalog_digest=version) for r in prior]
    for row in individual:
        history.append({
          "formulation_id":row["formulation_id"],"meaning_id":row["meaning_id"],
          "meaning_catalog_digest":version,"decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,
          "source":"independent_equivalent_variants_math_screen_batch67",
          "editorial_reason":"Source-screened equivalent formulation; individual definition dependency review pending.",
          "human_verified":False,"reviewed_by":None
        })
    if len(old_review_rows)==524:
        newindexed={r["formulation_id"]:r for r in old_review_rows}
        if len(newindexed)!=524 or newindexed!={r["formulation_id"]:r for r in history}:
            raise PipelineError("Existing current review ledger conflicts with archived prior decisions")
    else:
        atomic_jsonl(ledger,sorted(history,key=lambda r:r["formulation_id"]))
    current=jsonl(ledger)
    indexed={r["formulation_id"]:r for r in current}
    if len(current)!=524 or len(indexed)!=524:
        raise PipelineError("Incomplete revised formulation ledger")
    for old in prior:
        updated=indexed[old["formulation_id"]]
        if any(updated.get(k)!=v for k,v in old.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Historical formulation-level decision changed")
    if {rid for r in current for rid in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Old screened relationship lost")
    check_cycles(now,w.records("relations"))
    if dict(Counter(r["decision"] for r in current))!={"linked":516,"no_supported_target":5,"needs_review":3}:
        raise PipelineError("Source-screened formulation disposition totals differ")
    state=w.state("meanings")
    state.update(total=509,record_digest=version,
      screened_new_formulations=93,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
       "batch":67,"contextual_meanings":509,"reviewed_formulations":524,
       "new_meanings":1,"new_source_screened_formulations":3,
       "existing_sigma_algebra_meaning_amended_not_duplicated":True,
       "historical_521_formulation_reviews_preserved":True,
       "historical_691_relationships_preserved":True,
       "compact_no_hausdorff_convention_explicit":True,
       "new_dependency_reviews_pending":3,
       "all_stages_unsealed":True,"human_peer_verified":False,
       "production_corpus_used":False,
       "next":"Individually screen contextual links for three variants; preserve equivalent compact/quasicompact terminology without a false prerequisite cycle."
    }
    atomic_json(w.root/"state/wave2_broad_meanings_batch67.json",report)
    return report

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(a.parse_args().workspace),indent=2))
if __name__=="__main__":main()
