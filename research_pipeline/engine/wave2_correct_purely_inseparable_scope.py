"""Correct unsupported characteristic-zero addendum in an independent Stacks meaning.

Stacks 9.14.1 explicitly assumes characteristic p>0. Source 9.28.1(3)
also restricts to p>0. An inherited formulation added a zero-characteristic
trivial-extension convention that is NOT justified by those cited sources.
This independently audited Wave 2 correction preserves all earlier links,
472? (actually 474) reviews, and the frozen independent Wave 1 corpus.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

MID="meaning.12e554f8d49d5361.purely-inseparable-extension"
FID="form.12e554f8d49d5361.purely-inseparable-extension"
URL="https://stacks.math.columbia.edu/tag/09HD"
OLD="For a field F of characteristic p greater than zero, an extension K/F is purely inseparable if, for every alpha in K, some p-power alpha^(p^n) lies in F. The trivial extension is also purely inseparable in any characteristic."
NEW="For a field F of characteristic p greater than zero, an extension K/F is purely inseparable if, for every alpha in K, some p-power alpha^(p^n) lies in F."
SCOPE="Stacks Definition 9.14.1: extension in characteristic p>0, every element has a suitable p-power in the base field"
REASON=("Stacks Definition 9.14.1 explicitly assumes a base field of characteristic p>0, and Stacks Definition 9.28.1(3) repeats the same condition. Both cite the p-power criterion. "
        "The inherited sentence asserting that the trivial extension is purely inseparable in any characteristic is not supported by these particular Stacks citations. Remove that extension from this source-specific formulation without claiming its converse is false in other algebra textbooks. "
        "The two preexisting relations to field characteristic and field extension remain exactly anchored in the unchanged source text and their historic IDs are preserved.")
def run(root):
 w=Workspace(root)
 baseline=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if baseline.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Independent unsealed Wave 2 fork required")
 if len(w.records("meanings"))!=462 or len(w.records("relations"))!=622:
  raise PipelineError("Requires independently screened 462-meaning, 622-link checkpoint")
 comparison=w.root/"wave2/cross_source_field_theory_variant_reviews_2026-10-19.jsonl"
 findings=jsonl(comparison)
 issue=next((x for x in findings if x["task_id"]=="v2.cross_source_variant_review.99300a2cc682bb12ac04"),None)
 if not issue or issue.get("source_scope_correction_needed") is not True:
  raise PipelineError("Missing individual cross-source mathematical discrepancy review")
 catalog=w.records("meanings")
 old=catalog.get(MID)
 if not old or old["source_citation"]["url"]!=URL or len(old["formulations"])!=1 or old["formulations"][0]["id"]!=FID:
  raise PipelineError("Wrong independent Stacks meaning or citation")
 if old["formulations"][0]["text"] not in (OLD,NEW):
  raise PipelineError("A different source-specific formulation is already in place")
 reviews_path=w.root/"state/wave2_formulation_reviews.jsonl"
 reviews=jsonl(reviews_path)
 by={x["formulation_id"]:x for x in reviews}
 if len(reviews)!=474 or len(by)!=474 or by[FID]["decision"]!="linked":
  raise PipelineError("Historical review catalog changed unexpectedly")
 if by[FID]["relation_ids"]!=["rel.stage5.purely-inseparable-extension.to.field-characteristic","rel.stage5.purely-inseparable-extension.to.field-extension"]:
  raise PipelineError("Unexpected independent source-linked mathematical dependencies")
 archive=w.root/"state/wave2_formulation_reviews_snapshot_474_before_inseparable_scope.jsonl"
 before=reviews_path.read_text(encoding="utf-8")
 if not archive.exists():
  archive.write_text(before,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_474_before_inseparable_scope.json",{
   "review_count":474,"screened_relations":622,
   "sha256":hashlib.sha256(before.encode("utf-8")).hexdigest(),
   "previous_catalog_digest":by[FID]["meaning_catalog_digest"],"human_peer_verified":False})
 historic=jsonl(archive)
 if len(historic)!=474:raise PipelineError("Incomplete audit review snapshot")
 if old["formulations"][0]["text"]==OLD:
  candidate=dict(old)
  candidate["formulations"]=[dict(old["formulations"][0],text=NEW,review_state="candidate",human_verified=False)]
  candidate["context"]=SCOPE
  candidate["editorial_status"]="source_scope_candidate_revision"
  apply_revision(w.root,{"event_id":"revision.wave2.inseparable.positive_characteristic_candidate01",
   "stage":"meanings","record_id":MID,"before_digest":digest(old),
   "editor":"assistant_independent_stacks_field_theory_source_audit_2026_10_19",
   "reason":REASON,"operation":"replace","replacement":candidate})
 current=w.records("meanings")[MID]
 f=current["formulations"][0]
 if f["text"]!=NEW:raise PipelineError("Candidate source-specific wording differs")
 if f["review_state"]=="candidate":
  revised=dict(current)
  revised["formulations"]=[dict(f,review_state="screened",human_verified=False,
    source_screened_by="assistant_independent_stacks_field_theory_source_audit_2026_10_19")]
  revised["editorial_status"]="individually_screened_source_scope_correction"
  revised["editorial_screening_reason"]=REASON
  apply_revision(w.root,{"event_id":"revision.wave2.inseparable.positive_characteristic_screen01",
   "stage":"meanings","record_id":MID,"before_digest":digest(current),
   "editor":"assistant_independent_stacks_field_theory_source_audit_2026_10_19",
   "reason":REASON,"operation":"replace","replacement":revised})
 catalog=w.records("meanings")
 if catalog[MID]["formulations"][0]["review_state"]!="screened":
  raise PipelineError("Context-corrected meaning was not screened")
 rels=w.records("relations")
 for r in rels.values():
  if r["from_formulation"]==FID and r["source_phrase"].casefold() not in NEW.casefold():
   raise PipelineError("Existing mathematical source anchor destroyed by correction "+r["id"])
 new_digest=digest(list(catalog.values()))
 updated=[]
 for r in historic:
  v=dict(r,meaning_catalog_digest=new_digest)
  if r["formulation_id"]==FID:
   v["original_source_scope_review_reason"]=r["editorial_reason"]
   v["editorial_reason"]=REASON
   v["source"]="individually_audited_stacks_positive_characteristic_correction"
   v["reviewed_by"]="assistant_independent_stacks_field_theory_source_audit_2026_10_19"
   v["human_verified"]=False
  updated.append(v)
 old_current=jsonl(reviews_path)
 if old_current!=updated:
  if old_current!=historic:
   raise PipelineError("Formulation review ledger changed without audited source evidence")
  atomic_jsonl(reviews_path,sorted(updated,key=lambda r:r["formulation_id"]))
 fresh=jsonl(reviews_path)
 newmap={r["formulation_id"]:r for r in fresh}
 if len(newmap)!=474:
  raise PipelineError("Reviewed formulation identities lost")
 for r in historic:
  now=newmap[r["formulation_id"]]
  if (now["decision"]!=r["decision"] or now["relation_ids"]!=r["relation_ids"] or
      now["original_wave1_disposition"]!=r["original_wave1_disposition"]):
   raise PipelineError("Previously individually screened links or historic dispositions changed")
 if {i for r in fresh for i in r["relation_ids"]}!=set(rels):
  raise PipelineError("A screened link is missing its review")
 check_cycles(catalog,rels)
 state=w.state("meanings")
 state.update(total=462,record_digest=new_digest,screened_new_formulations=43,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 report={"phase":"positive_characteristic_purely_inseparable_source_context_corrected",
   "source_url":URL,"meanings":462,"reviews_preserved":474,"screened_links_preserved":622,
   "inherited_wave1_source_context_correction_audited_only_in_wave2":True,
   "unsupported_characteristic_zero_statement_not_silently_claimed":True,
   "char_zero_alternative_requires_independent_source":True,
   "source_anchors_and_original_dispositions_preserved":True,
   "all_stages_unsealed":True,"human_peer_verified":False,
   "original_production_mathdef_consulted":False}
 atomic_json(w.root/"state/wave2_pure_inseparable_scope_correction.json",report)
 return report
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace",required=True,type=Path)
 a=p.parse_args();print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
