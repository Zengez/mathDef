"""Individually mathematically screen nine evidence-based Wave 2 foundation meanings.

Records source and cross-context checks, uses the recoverable revision-event
mechanism to promote each *unchanged* formulation text from candidate to
screened. This does NOT seal any Wave 2 stage or assert human peer review.
"""
import argparse,json,hashlib
from pathlib import Path
from .core import Workspace,PipelineError,digest,atomic_json,canonical
from .revisions import apply_revision

REVIEW={
 "group":(
  ["https://proofwiki.org/wiki/Definition%3AGroup",
   "https://math.libretexts.org/Bookshelves/Abstract_and_Geometric_Algebra/First-Semester_Abstract_Algebra%3A_A_Structural_Approach_%28Sklar%29/02%3A_Groups/2.03%3A_The_Definition_of_a_Group"],
  "Binary closure, associativity, two-sided identity and two-sided inverses checked against an independent undergraduate algebra textbook. No commutativity imposed."),
 "abelian-group":(
  ["https://proofwiki.org/wiki/Definition%3AAbelian_Group",
   "https://math.libretexts.org/Bookshelves/Abstract_and_Geometric_Algebra/An_Inquiry-Based_Approach_to_Abstract_Algebra_%28Ernst%29/02%3A_Introduction_to_Groups/2.03%3A_Groups"],
  "Verified this is a group whose operation is commutative. Do not conflate with objects in an abelian category."),
 "two-sided-ideal":(
  ["https://proofwiki.org/wiki/Definition%3AIdeal_of_Ring",
   "https://stacks.math.columbia.edu/tag/00AR"],
  "ProofWiki supplies full two-sided absorption condition and additive subgroup. Stacks 10.3 confirms ring ideal notation but assumes commutative rings; source contexts remain distinct."),
 "commutative-prime-ideal":(
  ["https://proofwiki.org/wiki/Definition%3APrime_Ideal_of_Ring/Commutative_and_Unitary_Ring",
   "https://stacks.math.columbia.edu/tag/00AR"],
  "Confirmed properness plus the elementwise product-primality condition in commutative unital rings. Not asserted for noncommutative prime ideals."),
 "left-module-nonunital":(
  ["https://proofwiki.org/wiki/Definition%3AModule_over_Ring",
   "https://stacks.math.columbia.edu/tag/00AQ"],
  "Directly verified left-action distributivity and associativity. ProofWiki's general definition omits the optional unital action axiom; Stacks conventions impose unity in coefficient rings, so do not equate the two module conventions silently."),
 "topological-space":(
  ["https://proofwiki.org/wiki/Definition%3ATopological_Space",
   "https://math.libretexts.org/Bookshelves/Applied_Mathematics/Seven_Sketches_in_Compositionality%3A_An_Invitation_to_Applied_Category_Theory_%28Fong_and_Spivak%29/07%3A_Logic_of_Behavior_-_Sheaves_Toposes_Languages/7.03%3A_Sheaves"],
  "Independent mathematics textbook matches the open-set axioms. Empty union gives the empty open set; empty underlying space remains allowed."),
 "regular-noetherian-ring":(
  ["https://stacks.math.columbia.edu/tag/00OD"],
  "Checked exact Definition 10.110.7, with regularity of each prime localization. Crucial Noetherian and commutative ring scope retained."),
 "associative-ring-identity-optional":(
  ["https://proofwiki.org/wiki/Definition%3ARing_%28Abstract_Algebra%29",
   "https://stacks.math.columbia.edu/tag/00AQ"],
  "ProofWiki explicitly adopts associative but not necessarily unital rings, whereas Stacks works with commutative unital rings. Both conventions retained, not merged."),
 "small-category":(
  ["https://stacks.math.columbia.edu/tag/0013"],
  "Stacks Definition 4.2.1 requires a set of objects, Hom sets, associative composition and identity arrows. Screen as a small category, not an unrestricted locally small large category.")
}

def run(root):
 w=Workspace(root)
 baseline=w.root/"state/baseline.json"
 if not baseline.exists() or json.loads(baseline.read_text())["mode"]!="second_wave":
     raise PipelineError("Cannot review definitions outside independent Wave 2")
 if w.state("meanings").get("sealed"):
     raise PipelineError("Meaning stage sealed; cannot revise")
 meanings=w.records("meanings")
 approved=[]
 for slug,(refs,reason) in REVIEW.items():
     id="meaning.wave2.foundation."+slug
     prior=meanings.get(id)
     if not prior:
         raise PipelineError("Candidate missing: "+id)
     if len(prior["formulations"])!=1 or prior["formulations"][0]["review_state"] not in (
           "candidate","screened"):
         raise PipelineError("Unexpected candidate review state: "+id)
     if len(reason)<90 or not all(x.startswith("https://") for x in refs):
         raise PipelineError("Inadequate mathematical review basis: "+id)
     approved.append({
       "meaning_id":id,"formulation_id":prior["formulations"][0]["id"],
       "source_evidence_ids":prior["formulations"][0]["evidence_ids"],
       "source_urls":refs,"editorial_review_reason":reason,
       "decision":"screen_formulation_with_context_as_written",
       "reviewed_by":"assistant_independent_mathematical_source_comparison_2026_10_19",
       "human_verified":False
     })
 intake=w.root/"wave2/foundation_meaning_review_batch_01.jsonl"
 intake.parent.mkdir(parents=True,exist_ok=True)
 content="".join(canonical(x)+"\n" for x in approved)
 if intake.exists() and intake.read_text(encoding="utf-8")!=content:
     raise PipelineError("Changed mathematical review decisions with same event identity")
 intake.write_text(content,encoding="utf-8")
 applied=0
 for row in approved:
     current=w.records("meanings")[row["meaning_id"]]
     form=current["formulations"][0]
     if form["review_state"]=="screened":
         if current.get("editorial_screening_reason")!=row["editorial_review_reason"]:
             raise PipelineError("Already screened meaning differs from recorded mathematical review")
         continue
     updated=dict(current)
     updated["formulations"]=[dict(form,review_state="screened",
                                 source_screened_by=row["reviewed_by"],
                                 human_verified=False)]
     updated["editorial_screening_reason"]=row["editorial_review_reason"]
     updated["crosschecked_source_urls"]=row["source_urls"]
     updated["human_verified"]=False
     result=apply_revision(w.root,{
         "event_id":"revision.wave2.foundation."+current["id"].rsplit(".",1)[-1]+".screen01",
         "stage":"meanings","record_id":row["meaning_id"],
         "before_digest":digest(current),
         "editor":row["reviewed_by"],
         "reason":row["editorial_review_reason"],
         "operation":"replace","replacement":updated
     })
     if result["status"] not in ("applied","already_applied"):
         raise PipelineError("Unable to track meaning revision")
     applied+=result["status"]=="applied"
 final=w.records("meanings")
 extra=[m for k,m in final.items() if k.startswith("meaning.wave2.foundation.")]
 if len(extra)!=9 or any(f["review_state"]!="screened" for m in extra for f in m["formulations"]):
     raise PipelineError("Not every one of the nine candidate formulations was screened")
 if len(final)!=428 or len(w.records("relations"))!=445:
     raise PipelineError("Unexpected effect on meaning or relation counts")
 state=w.state("meanings")
 if state.get("sealed"):
     raise PipelineError("Wave 2 meaning stage prematurely sealed")
 state["total"]=len(final)
 state["record_digest"]=digest(list(final.values()))
 state["screened_new_formulations"]=9
 state["stage4_review_complete"]=False
 atomic_json(w.root/"state/meanings.json",state)
 report={
  "phase":"individually_source_screened_foundational_meanings",
  "record_count":len(final),
  "screened_wave2_foundations":len(extra),
  "new_screenings_applied_this_invocation":applied,
  "inherited_meanings_preserved":419,
  "source_review_records":len(approved),
  "screened_meaning_stage_sealed":False,
  "mathematical_source_review_digest":hashlib.sha256(content.encode("utf-8")).hexdigest(),
  "human_peer_verified":False,
  "original_production_corpus_consulted":False,
  "pending_source_locator_reviews":8,
  "next":"Propose and individually review source-grounded dependency relationships; account for all newly screened formulation links before any Stage 5 seal."
 }
 atomic_json(w.root/"state/wave2_foundation_meanings_screened.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",required=True,type=Path)
 args=p.parse_args()
 print(json.dumps(run(args.workspace),indent=2,ensure_ascii=False))
if __name__=="__main__":
 main()
