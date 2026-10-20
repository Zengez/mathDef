"""Batch 56: exact, noncircular rational prerequisite links; audit one old override.

Uses ONLY independently built Wave 2 meanings and external source locators.
The former no-supported-target Cauchy decision is archived before revision.
"""
from __future__ import annotations
import argparse,json,hashlib
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
CORNELL="https://pi.math.cornell.edu/~web304/reals.pdf"
PW="https://proofwiki.org/wiki/Definition%3A"
SEQUENCE=PW+"Rational_Sequence"
RATIONAL=PW+"Rational_Number"
ABSOLUTE=PW+"Absolute_Value/Ordered_Integral_Domain"
POSITIVE=PW+"Strictly_Positive_Rational_Number"
BASE={"sources":14,"terms":399,"observations":822,"meanings":500}
# Each candidate relation has a checked source phrase, exact source and target
# locator, and an individual mathematical justification.
LINKS=(
 ("01","form.wave2.real51.rational-cauchy","meaning.wave2.rational55.rational-sequence",
  "sequence (a_n) of rational numbers",CORNELL,SEQUENCE,
  "Cornell's rational Cauchy criterion is a property of sequences taking values in Q. The independently screened rational-sequence meaning identifies that foundational domain and codomain without invoking convergence of rational sequences to real limits."),
 ("02","form.wave2.real51.rational-cauchy","meaning.wave2.rational55.rational-absolute-value",
  "|a_m−a_n|",CORNELL,ABSOLUTE,
  "The rational epsilon-Cauchy inequality explicitly uses absolute values of rational differences. The source-verified piecewise rational absolute-value function is the correct prerequisite; using an already constructed real absolute-value context would be logically unnecessary."),
 ("03","form.wave2.real51.rational-cauchy","meaning.wave2.rational55.strictly-positive-rational",
  "positive rational epsilon",CORNELL,POSITIVE,
  "The phrase for every positive rational epsilon requires every strictly positive rational tolerance, not merely the nonnegative values that include zero. This link prevents an incorrect epsilon-zero quantification that would force eventual constancy."),
 ("04","form.wave2.rational55.rational-sequence","meaning.wave2.rational55.rational-number",
  "a:N_{>=1}→Q",SEQUENCE,RATIONAL,
  "The independently sourced infinite rational sequence is a function with values in Q. The separate meaning of rational numbers as the fraction field of Z defines those values, not their index ordering or an already constructed real completion."),
 ("05","form.wave2.rational55.rational-absolute-value","meaning.wave2.rational55.rational-number",
  "q in Q",ABSOLUTE,RATIONAL,
  "The piecewise rational absolute-value operation has Q as its domain and codomain; it requires the rational field and its total ordering. It does not depend on square roots or on the field R from the later completion construction."),
 ("06","form.wave2.rational55.strictly-positive-rational","meaning.wave2.rational55.rational-number",
  "rational number ε",POSITIVE,RATIONAL,
  "Strict positivity is defined using the order on the rational field Q and a condition ε>0. The rational-number meaning establishes that base domain, independently of rational Cauchy sequences or any constructed real ordering.")
)
NO_TARGET={
 "formulation_id":"form.wave2.rational55.rational-number",
 "meaning_id":"meaning.wave2.rational55.rational-number",
 "decision":"no_supported_target",
 "source_locator":RATIONAL,
 "reason":"The fraction-field definition of Q depends on integers, their commutative integral-domain arithmetic, and the identification of equivalent numerator-denominator pairs. This independent reconstruction does not yet contain a suitably source-screened standalone integer/rational-field-foundation definition as a dependency target. Linking to real numbers, constructed later from rationals, would invert the foundations.",
 "missing":["integer ring Z and nonzero denominator","field of fractions of an integral domain"],
 "human_verified":False
}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Existing separately reviewed rational link batch changed")
    path.write_text(body,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BASE,"relations")):
        raise PipelineError("Independent unsealed Wave 2 required")
    if {s:len(w.records(s)) for s in BASE}!=BASE:
        raise PipelineError("Unexpected screened rational foundation baseline")
    meanings=w.records("meanings"); observations=w.records("observations")
    byform={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
    if len(byform)!=512:
        raise PipelineError("Expected 512 individual reviewed mathematical formulations")
    rels=w.records("relations")
    if len(rels) not in (670,676):
        raise PipelineError("Unexpected prior relationship corpus")
    original={i:r for i,r in rels.items() if not i.startswith("rel.wave2.rational56.")}
    if len(original)!=670:
        raise PipelineError("Earlier source-screened relations were changed")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    previous=jsonl(ledger)
    old={r["formulation_id"]:r for r in previous}
    if len(old)!=512 or len(previous)!=512 or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in previous):
        raise PipelineError("Old mathematical review ledger missing or stale")
    if {i for r in previous for i in r["relation_ids"]}!=set(rels):
        raise PipelineError("Existing relations not all reviewed")
    created=[]
    for num,fid,mid,phrase,fromurl,tourl,reason in LINKS:
        pair=byform.get(fid)
        target=meanings.get(mid)
        if not pair or not target:
            raise PipelineError("Missing independently screened meaning/target")
        meaning,form=pair
        if (form["review_state"]!="screened" or
            locator(meaning,observations)!=fromurl or
            locator(target,observations)!=tourl or
            phrase not in form["text"] or len(reason)<150):
            raise PipelineError("Imprecise source phrase/locator or mathematical review: "+num)
        created.append({
           "id":"rel.wave2.rational56."+num,"from_formulation":fid,
           "target_meaning":mid,"relation_type":"definition_uses",
           "review_state":"screened","source_phrase":phrase,
           "source_locator":fromurl,"target_locator":tourl,
           "editorial_reason":reason,
           "reviewed_by":"assistant_independent_rational_foundation_link_review_2026_10_20",
           "human_verified":False
        })
    newids={r["id"] for r in created}
    if len(newids)!=6 or newids&set(original):
        raise PipelineError("Conflicting or repeated independent links")
    revised_rels={**original,**{r["id"]:r for r in created}}
    check_cycles(meanings,revised_rels)
    ids={
       "form.wave2.rational55.rational-number",
       "form.wave2.rational55.rational-sequence",
       "form.wave2.rational55.rational-absolute-value",
       "form.wave2.rational55.strictly-positive-rational"
    }
    old_cauchy="form.wave2.real51.rational-cauchy"
    prior_cauchy=old[old_cauchy]
    if len(rels)==670:
        if prior_cauchy["decision"]!="no_supported_target" or prior_cauchy["relation_ids"]:
            raise PipelineError("Prior no-supported-target decision already revised without event")
        if any(old[k]["decision"]!="needs_review" or old[k]["relation_ids"] for k in ids):
            raise PipelineError("Prior new rational meanings were not left pending")
        snapshot=w.root/"state/wave2_formulation_reviews_snapshot_512_before_rational56.jsonl"
        oldtext=ledger.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=oldtext:
            raise PipelineError("Earlier 512 review snapshot changed")
        snapshot.write_text(oldtext,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_512_before_rational56.json",{
          "rows":512,"links":670,"sha256":hashlib.sha256(oldtext.encode("utf-8")).hexdigest(),
          "human_peer_verified":False})
    snapshot=w.root/"state/wave2_formulation_reviews_snapshot_512_before_rational56.jsonl"
    earlier=jsonl(snapshot)
    orig={r["formulation_id"]:r for r in earlier}
    if len(orig)!=512 or orig.get(old_cauchy,{}).get("decision")!="no_supported_target":
        raise PipelineError("Required earlier individual no-supported-target review lost")
    if len(orig)!=len(earlier):
        raise PipelineError("Historical repeated formulation ID")
    override={
       "event_id":"rational56.revise.cauchy.no-target-to-screened-dependencies",
       "formulation_id":old_cauchy,
       "previous_review_digest":digest(orig[old_cauchy]),
       "previous_decision":"no_supported_target",
       "new_decision":"linked",
       "previous_reason":orig[old_cauchy]["editorial_reason"],
       "new_supporting_relations":[r["id"] for r in created if r["from_formulation"]==old_cauchy],
       "reason":"Three new independently screened rational foundations now exist with exact source locators, allowing direct noncircular prerequisites in place of the earlier justified missing-target assessment.",
       "human_verified":False,
       "reviewed_by":"assistant_independent_rational_foundation_link_review_2026_10_20"
    }
    store(w.root/"events/rational_cauchy_override_batch56.jsonl",[override])
    store(w.root/"wave2/individual_rational_links_batch56.jsonl",created)
    store(w.root/"wave2/rational_number_no_target_review_batch56.jsonl",[NO_TARGET])
    input_file=store(w.root/"intake/rational_prerequisite_links_batch56.jsonl",created)
    if len(rels)==670:
        w.ingest("relations",input_file,batch_size=6)
    current=w.records("relations")
    if len(current)!=676 or any(current.get(r["id"])!=r for r in created):
        raise PipelineError("New independent source-screened links not ingested")
    check_cycles(meanings,current)
    replacement=[]
    for oldrow in earlier:
        row=dict(oldrow);fid=row["formulation_id"]
        if fid==old_cauchy or fid in ids:
            attached=[r["id"] for r in created if r["from_formulation"]==fid]
            row["relation_ids"]=attached
            row["reviewed_by"]="assistant_independent_rational_foundation_link_review_2026_10_20"
            if attached:
                row["decision"]="linked"
                row["source"]="independent_rational_foundation_mathematical_link_review_batch56"
                row["editorial_reason"]="Individually verified exact source-based foundational dependency with source/target locators and a cycle-free graph."
            else:
                if fid!=NO_TARGET["formulation_id"]:
                    raise PipelineError("Unreviewed rational formulation")
                row["decision"]="no_supported_target"
                row["source"]="independent_rational_number_explicit_no_target_review_batch56"
                row["editorial_reason"]=NO_TARGET["reason"]
            if fid==old_cauchy:
                row["previous_review_digest"]=digest(orig[old_cauchy])
                row["previous_wave2_decision"]="no_supported_target"
                row["override_event_id"]=override["event_id"]
        replacement.append(row)
    if len(rels)==676:
        previous_map={r["formulation_id"]:r for r in previous}
        if previous_map!={r["formulation_id"]:r for r in replacement}:
            raise PipelineError("Already committed reviewed dependency payload differs")
    else:
        atomic_jsonl(ledger,sorted(replacement,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger)
    results={r["formulation_id"]:r for r in final}
    if len(results)!=512 or len(final)!=512:
        raise PipelineError("Incomplete reviewed meaning ledger")
    if any(results[k]!=v for k,v in orig.items() if k not in ids|{old_cauchy}):
        raise PipelineError("A historical unrelated individual review changed")
    if {i for r in final for i in r["relation_ids"]}!=set(current):
        raise PipelineError("Incomplete source reviewed link coverage")
    outcomes=dict(Counter(r["decision"] for r in final))
    if outcomes!={"linked":507,"no_supported_target":5}:
        raise PipelineError("Unreviewed mathematical formulations remain: "+str(outcomes))
    report={
       "phase":"six_individual_rational_foundational_dependencies_and_one_no_target_override",
       "screened_meanings":500,"formulation_reviews":512,
       "links_total":676,"new_links":6,
       "historic_670_links_preserved":True,
       "old_unrelated_review_decisions_preserved":True,
       "previous_no_supported_target_overridden_with_explicit_event":True,
       "rational_number_no_supported_target_remaining":True,
       "remaining_unreviewed_new_formulations":0,
       "strict_epsilon_excludes_zero":True,
       "no_dependency_cycles":True,
       "all_stages_unsealed":True,
       "human_peer_verified":False,"production_corpus_used":False,
       "next":"Source missing integer/fraction-field foundations and audit cross-context source citation completeness. Continue broader independent variants, avoiding premature model conflation."
    }
    atomic_json(w.root/"state/wave2_rational_dependency_review_batch56.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    args=p.parse_args()
    print(json.dumps(run(args.workspace),indent=2))

if __name__=="__main__":main()
