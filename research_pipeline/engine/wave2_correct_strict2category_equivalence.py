"""Correct the Stacks 4.29.4 equivalence context to a STRICT 2-category.

This is NOT a claim that the weak bicategory variant has been researched or
that every weak 2-category notion has a strict source. A candidate-to-screened
audited revision preserves all 621 previously screened links, 474 reviews,
and the original held Wave 1 disposition before link reconsideration.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

MID="meaning.ec5e3a0d13f85f3a.equivalence-objects-two-category"
FID="form.ec5e3a0d13f85f3a.equivalence-objects-two-category"
URL="https://stacks.math.columbia.edu/tag/003G"
OLD="Two objects X,Y in a 2-category are equivalent if there are 1-morphisms F:X→Y and G:Y→X with invertible 2-morphisms FG⇒id_Y and GF⇒id_X."
NEW="Two objects X,Y in a strict 2-category C are equivalent if there are 1-morphisms F:X→Y and G:Y→X together with invertible 2-morphisms F∘G⇒id_Y and G∘F⇒id_X. This is the Stacks Project strict 2-category convention; weak bicategory equivalences require a separate context/source review."
CONTEXT="Stacks 4.29.4 equivalence of objects in its explicitly defined strict 2-category, not an independently sourced arbitrary weak bicategory"
WHY=("Stacks Section 4.29 explicitly declares it is defining strict 2-categories at the outset, and Definition 4.29.4 defines equivalent objects within that framework by 1-morphisms F,G and invertible 2-isomorphisms FG≈id and GF≈id. "
     "The inherited wording was mathematically plausible but lacked this source-specific qualification, making an unrestricted link to a strict 2-category over-general. "
     "The revised definition is deliberately restricted to the documented Stacks context; general bicategory/weak 2-category equivalence remains a separate unscreened variant research need.")

def run(root):
 w=Workspace(root)
 if json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8")).get("mode")!="second_wave":
  raise PipelineError("Only an independent editable Wave 2 fork is accepted")
 if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Cannot mutate sealed research")
 if len(w.records("meanings"))!=462 or len(w.records("relations"))!=621:
  raise PipelineError("Requires the verified 462-meaning/621-relation independent checkpoint")
 linkreport=w.root/"state/wave2_link_review_batch_17.json"
 if not linkreport.exists() or json.loads(linkreport.read_text(encoding="utf-8")).get("total_screened_links")!=621:
  raise PipelineError("Latest 621 independent links are not source-verified")
 reviews_path=w.root/"state/wave2_formulation_reviews.jsonl"
 reviews=jsonl(reviews_path)
 mapping={r["formulation_id"]:r for r in reviews}
 if len(reviews)!=474 or len(mapping)!=474 or FID not in mapping:
  raise PipelineError("Expected 474 complete historical review identities")
 prior=mapping[FID]
 if prior["decision"]!="held_ambiguity" or prior["original_wave1_disposition"]!="held_ambiguity" or prior["relation_ids"]!=[]:
  raise PipelineError("The original mathematical hold is no longer in its source-review state")
 m=w.records("meanings").get(MID)
 if not m or m["source_citation"]["url"]!=URL or len(m["formulations"])!=1 or m["formulations"][0]["id"]!=FID:
  raise PipelineError("Wrong exact independent Stacks source")
 if m["formulations"][0]["text"] not in (OLD,NEW):
  raise PipelineError("Previously screened equivalence formulation has unexpected text")
 # First persist historical 474-row review evidence before meaning digest rebasing.
 snapshot=w.root/"state/wave2_formulation_reviews_snapshot_474_before_strict2cat.jsonl"
 archive=reviews_path.read_text(encoding="utf-8")
 if not snapshot.exists():
  snapshot.write_text(archive,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_474_before_strict2cat.json",{
    "historical_formulation_reviews":474,"screened_links":621,
    "review_sha256":hashlib.sha256(archive.encode("utf-8")).hexdigest(),
    "old_catalog_digest":prior["meaning_catalog_digest"],"human_peer_verified":False})
 historic=jsonl(snapshot)
 old={r["formulation_id"]:r for r in historic}
 if len(historic)!=474 or old[FID]["decision"]!="held_ambiguity":
  raise PipelineError("Original review snapshot is invalid")
 if m["formulations"][0]["text"]==OLD:
  candidate=dict(m)
  candidate["formulations"]=[dict(m["formulations"][0],text=NEW,review_state="candidate",human_verified=False)]
  candidate["context"]=CONTEXT
  candidate["editorial_status"]="reexamining_source_scope_in_editable_wave2"
  apply_revision(w.root,{"event_id":"revision.wave2.strict2cat_equivalence.context_candidate01",
    "stage":"meanings","record_id":MID,"before_digest":digest(m),
    "editor":"assistant_independent_stacks_4_29_source_review_2026_10_19",
    "reason":WHY,"operation":"replace","replacement":candidate})
 m=w.records("meanings")[MID]
 form=m["formulations"][0]
 if form["text"]!=NEW:raise PipelineError("Candidate source-specific correction differs")
 if form["review_state"]=="candidate":
  screened=dict(m)
  screened["formulations"]=[dict(form,review_state="screened",human_verified=False,
    source_screened_by="assistant_independent_stacks_4_29_source_review_2026_10_19")]
  screened["editorial_status"]="source_scoped_strict_2_category_equivalence_reviewed"
  screened["editorial_screening_reason"]=WHY
  apply_revision(w.root,{"event_id":"revision.wave2.strict2cat_equivalence.context_screen01",
    "stage":"meanings","record_id":MID,"before_digest":digest(m),
    "editor":"assistant_independent_stacks_4_29_source_review_2026_10_19",
    "reason":WHY,"operation":"replace","replacement":screened})
 meanings=w.records("meanings")
 if meanings[MID]["formulations"][0]["review_state"]!="screened":
  raise PipelineError("Source-specific strict formulation not screened")
 newdg=digest(list(meanings.values()))
 proposed=[]
 for r in historic:
  n=dict(r,meaning_catalog_digest=newdg)
  if r["formulation_id"]==FID:
   n["original_strict2cat_context_hold_reason"]=r["editorial_reason"]
   n["editorial_reason"]=WHY
   n["source"]="individual_wave2_strict2cat_context_mathematical_recheck"
   n["reviewed_by"]="assistant_independent_stacks_4_29_source_review_2026_10_19"
   n["human_verified"]=False
  proposed.append(n)
 latest=jsonl(reviews_path)
 if latest!=proposed:
  if latest!=historic:
   raise PipelineError("A review disposition changed during meaning rebase")
  atomic_jsonl(reviews_path,sorted(proposed,key=lambda r:r["formulation_id"]))
 after=jsonl(reviews_path)
 by={r["formulation_id"]:r for r in after}
 if len(by)!=474:raise PipelineError("Source review identities lost")
 for r in historic:
  now=by[r["formulation_id"]]
  if (now["decision"]!=r["decision"] or now["relation_ids"]!=r["relation_ids"] or
      now["original_wave1_disposition"]!=r["original_wave1_disposition"]):
   raise PipelineError("Historic source review decision or links changed")
 if {link for r in after for link in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Preexisting screened relationship coverage lost")
 check_cycles(meanings,w.records("relations"))
 state=w.state("meanings")
 state.update(total=462,record_digest=newdg,screened_new_formulations=43,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 audit={
  "formulation_id":FID,"source_url":URL,"source_definition":"Stacks 4.29.4 in explicitly strict 2-category Section 4.29",
  "previous_text":OLD,"new_text":NEW,
  "mathematical_reason":WHY,
  "prior_disposition":"held_ambiguity","current_disposition":"held_ambiguity",
  "weak_bicategory_context_still_unscreened":True,"link_accepted_in_this_phase":False,
  "human_verified":False
 }
 audit_path=w.root/"events/wave2_strict2cat_equivalence_scope_review.json"
 if audit_path.exists() and json.loads(audit_path.read_text(encoding="utf-8"))!=audit:
  raise PipelineError("Prior mathematical audit evidence differs")
 atomic_json(audit_path,audit)
 report={"phase":"strict2category_equivalence_source_context_corrected_and_screened",
  "screened_meanings":462,"formulation_reviews_preserved":474,"screened_links_preserved":621,
  "held_ambiguity_original_disposition_preserved":True,
  "weak_bicategory_variant_remains_future_research":True,
  "source_specific_strict_category_definition_screened":True,
  "link_to_strict_two_category_not_yet_applied":True,
  "human_peer_verified":False,"all_stages_unsealed":True,
  "original_production_mathdef_consulted":False}
 atomic_json(w.root/"state/wave2_strict2cat_equivalence_context_correction.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace",required=True,type=Path)
 a=p.parse_args();print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
