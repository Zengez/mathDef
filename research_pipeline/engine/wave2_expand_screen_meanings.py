"""Add and individually screen three independent foundational meanings, then rebase reviews.

The three direct-source paraphrases are treated as candidate definitions first.
After explicit mathematical review events, append three new needs_review
formulations WITHOUT losing 440 earlier dispositions or 529 screened links.
Wave 1 and the production mathDef corpus are never opened or edited here.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

FOUNDATIONS = [
 {
 "key":"unit-of-ring",
 "term_group_id":"wave2.foundation.unit-of-ring",
 "display_term":"unit of a unital ring",
 "context":"Associative ring with 1: two-sided multiplicative invertibility; distinct from the unity 1_R",
 "term_id":"term.wave2.proofwiki.unit-of-ring",
 "observation_id":"obs.wave2.proofwiki.unit-of-ring",
 "locator":"https://proofwiki.org/wiki/Definition%3AUnit_of_Ring",
 "crosscheck":["https://proofwiki.org/wiki/Definition%3AUnit_of_Ring",
               "https://stacks.math.columbia.edu/tag/00AR"],
 "text":"Let R be an associative ring with identity 1_R. An element u in R is a unit if there exists v in R such that uv=1_R=vu. The identity is required, but u itself need not equal 1_R.",
 "scope":"Do not conflate invertible ring elements with the multiplicative identity, or impose commutativity. Both-sided inverses required.",
 "reason":"ProofWiki Definition 1 specifies an inverse on both sides in a ring with unity. Distinguish the element u from the identity element 1_R and do not infer commutativity from invertibility."
 },
 {
 "key":"integral-domain",
 "term_group_id":"wave2.foundation.integral-domain",
 "display_term":"integral domain (nonzero commutative unital convention)",
 "context":"Stacks commutative algebra: nonzero commutative ring with 1 and no nonzero zero divisors",
 "term_id":"term.wave2.stacks.integral-domain",
 "observation_id":"obs.wave2.stacks.integral-domain",
 "locator":"https://stacks.math.columbia.edu/tag/09FE",
 "crosscheck":["https://stacks.math.columbia.edu/tag/09FE",
               "https://stacks.math.columbia.edu/tag/00AQ",
               "https://proofwiki.org/wiki/Definition%3AIntegral_Domain"],
 "text":"An integral domain in the Stacks commutative-unital convention is a nonzero commutative ring R with identity 1_R in which ab=0 implies a=0 or b=0 for every a,b in R.",
 "scope":"Must exclude zero ring; assume commutativity and unity. Some algebra sources use domain more broadly, so do not silently generalize.",
 "reason":"Stacks Definition 9.2.2 requires a nonzero ring with only zero as a zerodivisor; Section 10.2 supplies the commutative unital convention. The product-zero criterion is an equivalent wording."
 },
 {
 "key":"commutative-maximal-ideal",
 "term_group_id":"wave2.foundation.maximal-ideal",
 "display_term":"maximal ideal of a commutative unital ring",
 "context":"Commutative algebra: proper maximal ring ideal, not a general noncommutative maximal left or right ideal",
 "term_id":"term.wave2.proofwiki.maximal-ideal-of-ring",
 "observation_id":"obs.wave2.proofwiki.maximal-ideal-of-ring",
 "locator":"https://proofwiki.org/wiki/Definition%3AMaximal_Ideal_of_Ring",
 "crosscheck":["https://proofwiki.org/wiki/Definition%3AMaximal_Ideal_of_Ring",
               "https://stacks.math.columbia.edu/tag/00AR"],
 "text":"Let R be a commutative ring with identity. An ideal m of R is maximal if m is properly contained in R and every ideal J with m⊆J⊆R satisfies J=m or J=R.",
 "scope":"Properness is essential; left/right/two-sided maximality agree in the commutative setting but need not coincide in noncommutative rings.",
 "reason":"Direct ProofWiki definition requires a proper ideal maximal by inclusion among proper ideals; Stacks basic notions supplies the commutative-unital convention and equivalent quotient-field property."
 }
]

def run(root):
    w=Workspace(root)
    baseline=w.root/"state/baseline.json"
    if not baseline.exists() or json.loads(baseline.read_text(encoding="utf-8")).get("mode")!="second_wave":
        raise PipelineError("Only an independently forked Wave 2 workspace can be edited")
    if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
        raise PipelineError("Never edit a sealed stage")
    terms,observations=w.records("terms"),w.records("observations")
    if len(terms)!=339 or len(observations)!=762 or len(w.records("relations"))!=529:
        raise PipelineError("Incomplete source intake or unexpected relationship ledger")
    specs=[]
    for item in FOUNDATIONS:
        term,ob=terms.get(item["term_id"]),observations.get(item["observation_id"])
        if not term or not ob or term["locator"]!=item["locator"] or ob["locator"]!=item["locator"]:
            raise PipelineError("Missing or divergent independently read source article: "+item["key"])
        if ob["record_kind"]!="paraphrase" or ob["term_id"]!=term["id"] or ob["human_verified"] is not False:
            raise PipelineError("Insufficient traceable source observation: "+item["key"])
        mid="meaning.wave2.foundation."+item["key"]
        fid="form.wave2.foundation."+item["key"]
        specs.append({
          "id":mid,"term_group_id":item["term_group_id"],
          "display_term":item["display_term"],"context":item["context"],
          "term_ids":[item["term_id"]],
          "formulations":[{
             "id":fid,"text":item["text"],
             "evidence_ids":[item["observation_id"]],
             "review_state":"candidate",
             "mathematical_scope_note":item["scope"],"human_verified":False
          }],
          "editorial_status":"candidate_pending_individual_mathematical_review",
          "human_verified":False
        })
    p=w.root/"intake/wave2_foundation_meaning_candidates_batch_03.jsonl"
    p.parent.mkdir(parents=True,exist_ok=True)
    payload=chr(10).join(canonical(x) for x in specs)+chr(10)
    if p.exists() and p.read_text(encoding="utf-8")!=payload:
        raise PipelineError("Existing meaning candidate batch has changed")
    p.write_text(payload,encoding="utf-8")
    meanings=w.records("meanings")
    if len(meanings)==428:
        result=w.ingest("meanings",p,batch_size=3)
    elif len(meanings)==431:
        for spec in specs:
            m=meanings.get(spec["id"])
            if not m or m["formulations"][0]["text"]!=spec["formulations"][0]["text"]:
                raise PipelineError("Partial meaning intake differs from original candidate")
    else:
        raise PipelineError("Unexpected number of contextual meanings")
    initial_reviews=[]
    for item in FOUNDATIONS:
        mid="meaning.wave2.foundation."+item["key"]
        curr=w.records("meanings")[mid]
        if len(curr["formulations"])!=1 or curr["formulations"][0]["id"]!="form.wave2.foundation."+item["key"]:
            raise PipelineError("Unexpected candidate formulation")
        review={
           "meaning_id":mid,"formulation_id":curr["formulations"][0]["id"],
           "source_urls":item["crosscheck"],"source_evidence_ids":[item["observation_id"]],
           "mathematical_reason":item["reason"],
           "reviewed_by":"assistant_independent_foundation_mathematical_comparison_2026_10_19",
           "human_verified":False,
           "decision":"screen_source_scoped_formulation_without_equating_conventions"
        }
        if len(review["mathematical_reason"])<125:
            raise PipelineError("Source review rationale is insufficient")
        initial_reviews.append(review)
        if curr["formulations"][0]["review_state"]=="screened":
            if curr.get("editorial_screening_reason")!=item["reason"]:
                raise PipelineError("Existing screened meaning has different rationale")
            continue
        if curr["formulations"][0]["review_state"]!="candidate":
            raise PipelineError("Unknown formulation review state")
        revised=dict(curr)
        revised["formulations"]=[dict(curr["formulations"][0],review_state="screened",
                            source_screened_by=review["reviewed_by"],human_verified=False)]
        revised["crosschecked_source_urls"]=item["crosscheck"]
        revised["editorial_screening_reason"]=item["reason"]
        revised["human_verified"]=False
        apply_revision(w.root,{
           "event_id":"revision.wave2.foundation."+item["key"]+".screen01",
           "stage":"meanings","record_id":mid,"before_digest":digest(curr),
           "editor":review["reviewed_by"],"reason":item["reason"],
           "operation":"replace","replacement":revised
        })
    review_path=w.root/"wave2/foundation_meaning_review_batch_02.jsonl"
    proof=chr(10).join(canonical(row) for row in initial_reviews)+chr(10)
    if review_path.exists() and review_path.read_text(encoding="utf-8")!=proof:
        raise PipelineError("Mathematical review evidence has changed")
    review_path.parent.mkdir(parents=True,exist_ok=True)
    review_path.write_text(proof,encoding="utf-8")
    meanings=w.records("meanings")
    forms={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
    if len(meanings)!=431 or len(forms)!=443:
        raise PipelineError("Expected exactly three additional screened meanings")
    if any(f["review_state"]!="screened" for m in meanings.values() for f in m["formulations"]):
        raise PipelineError("Candidate left unscreened before review rebase")
    state=w.state("meanings")
    state.update(total=431,record_digest=digest(list(meanings.values())),
                 screened_new_formulations=12,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    old_path=w.root/"state/wave2_formulation_reviews.jsonl"
    previous=jsonl(old_path)
    if len(previous)==440:
        old_by_id={row["formulation_id"]:row for row in previous}
        if len(old_by_id)!=440 or not set(old_by_id).issubset(forms):
            raise PipelineError("Missing or repeated previous review identities")
        relations=w.records("relations")
        if {rid for r in previous for rid in r["relation_ids"]}!=set(relations):
            raise PipelineError("Existing screened links and decisions diverge")
        old_digest=previous[0]["meaning_catalog_digest"]
        if any(row["meaning_catalog_digest"]!=old_digest for row in previous):
            raise PipelineError("Inconsistent older meaning catalog")
        snapshot=w.root/"state/wave2_formulation_reviews_snapshot_440.jsonl"
        snapshot_data=old_path.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=snapshot_data:
            raise PipelineError("440-review snapshot conflicts")
        snapshot.write_text(snapshot_data,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_440.json",{
          "review_count":440,"relationship_count":529,
          "meaning_catalog_digest":old_digest,
          "review_ledger_sha256":hashlib.sha256(snapshot_data.encode("utf-8")).hexdigest(),
          "snapshot_retains_historical_dispositions":True
        })
        new_digest=digest(list(meanings.values()))
        updated=[dict(row,meaning_catalog_digest=new_digest) for row in previous]
        for spec in specs:
            updated.append({
              "formulation_id":spec["formulations"][0]["id"],"meaning_id":spec["id"],
              "meaning_catalog_digest":new_digest,"decision":"needs_review",
              "relation_ids":[],"original_wave1_disposition":None,
              "source":"wave2_new_individually_screened_foundation",
              "editorial_reason":"New independently sourced meaning; requires formulation-specific prerequisite analysis and evidence-based links, not text matching.",
              "reviewed_by":None,"human_verified":False
            })
        atomic_jsonl(old_path,sorted(updated,key=lambda r:r["formulation_id"]))
    elif len(previous)==443:
        if not (w.root/"state/wave2_formulation_reviews_snapshot_440.jsonl").exists():
            raise PipelineError("Lost the original 440-review snapshot")
        if any(x.get("meaning_catalog_digest")!=digest(list(meanings.values())) for x in previous):
            raise PipelineError("Already rebased reviews have stale meaning digest")
    else:
        raise PipelineError("Formulation ledger cannot be safely expanded")
    reviews=jsonl(old_path)
    if len(reviews)!=443 or len({r["formulation_id"] for r in reviews})!=443:
        raise PipelineError("Incomplete rebased mathematical review identities")
    prior=jsonl(w.root/"state/wave2_formulation_reviews_snapshot_440.jsonl")
    now={r["formulation_id"]:r for r in reviews}
    for r in prior:
        v=now.get(r["formulation_id"])
        if not v or any(v.get(k)!=value for k,value in r.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Historical formulation decision was rewritten")
    if {rid for r in reviews for rid in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Relations no longer represented by review ledger")
    check_cycles(meanings,w.records("relations"))
    from collections import Counter
    dispositions=dict(Counter(r["decision"] for r in reviews))
    if dispositions!={"linked":411,"no_supported_target":27,"held_ambiguity":2,"needs_review":3}:
        raise PipelineError("Unexpected revised review dispositions: "+str(dispositions))
    report={
      "phase":"three_additional_source_screened_meanings_and_append_only_formulation_reviews",
      "meaning_count":431,"formulation_count":443,"screened_foundations_added":3,
      "total_new_wave2_screened_meanings":12,
      "screened_relations_preserved":529,
      "inherited_review_rows_preserved":440,
      "review_dispositions":dispositions,
      "new_formulations_requiring_link_review":3,
      "historical_440_review_snapshot_exists":True,
      "all_wave2_stages_unsealed":True,
      "original_production_mathdef_consulted":False,
      "human_peer_verified":False,
      "next":"Mathematically screen three new foundation dependencies, then investigate 27 missing-target cases using these new independently verified concepts."
    }
    atomic_json(w.root/"state/wave2_foundations_meaning_review_batch_02.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",required=True,type=Path)
    a=p.parse_args()
    print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":
    main()
