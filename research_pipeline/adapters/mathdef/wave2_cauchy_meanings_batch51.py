"""Batch 51: individually screen two rational-Cauchy foundational meanings.

Keep the later quotient-field construction, positivity and uniqueness theorems
separate. No original production mathDef corpus is used.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace, PipelineError, jsonl, canonical, digest, atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
REVIEWS="wave2/real_constructions_independent_source_reviews_batch_48_2026-10-20.jsonl"
PREVIOUS={"sources":14,"terms":395,"observations":818,"meanings":492,"relations":664}
NEXT=dict(PREVIOUS,meanings=494)
CASES=(
 {
  "num":"04","review":"review.wave2.real48.rational-cauchy",
  "source":"src.cornell_math304","url":"https://pi.math.cornell.edu/~web304/reals.pdf",
  "meaning":"meaning.wave2.real51.rational-cauchy",
  "form":"form.wave2.real51.rational-cauchy",
  "label":"rational Cauchy sequence",
  "context":"Cauchy criterion using rational arithmetic before constructing real numbers",
  "formulation":"A sequence (a_n) of rational numbers is Cauchy if for every positive rational epsilon there is N such that |a_m−a_n|<epsilon whenever m and n are at least N.",
  "reason":"Cornell MATH 304 §4.1.3 defines a rational Cauchy sequence by arbitrarily tight pairs of entries in a tail. This quantifies over all positive rational tolerances and all pairs of sufficiently late indices. It does not assume an existing limit in Q or R, nor is it the weaker requirement that successive differences tend to zero."
 },
 {
  "num":"05","review":"review.wave2.real48.cauchy-equivalence",
  "source":"src.libretexts_sloughter",
  "url":"https://math.libretexts.org/Bookshelves/Analysis/A_Primer_of_Real_Analysis_%28Sloughter%29/01%3A_Fundamentals/1.04%3A_Real_Numbers",
  "meaning":"meaning.wave2.real51.rational-cauchy-equivalence",
  "form":"form.wave2.real51.rational-cauchy-equivalence",
  "label":"equivalence of rational Cauchy sequences",
  "context":"Difference tends to rational zero; equivalence precedes the real-number quotient construction",
  "formulation":"Two rational Cauchy sequences (a_n) and (b_n) are equivalent, written (a_n)∼(b_n), if for each positive rational epsilon there is N such that |a_n−b_n|<epsilon for every n≥N.",
  "reason":"Sloughter's real-number construction defines equivalence of rational Cauchy sequences by eventual rational epsilon-closeness at matching indices. Reflexivity and symmetry follow immediately, while transitivity uses the triangle inequality with epsilon/2. The definition must not refer to equality of real-valued limits, since the reals are still being constructed."
 },
)

def store(path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Previously reviewed Cauchy batch changed")
    path.write_text(content,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave"):
        raise PipelineError("Requires independent Wave 2")
    if any(w.state(s).get("sealed") for s in PREVIOUS):
        raise PipelineError("No stage may be sealed")
    counts={stage:len(w.records(stage)) for stage in PREVIOUS}
    if counts not in (PREVIOUS,NEXT):
        raise PipelineError("Unexpected independently screened count: "+str(counts))
    earlier_meanings=w.records("meanings")
    earlier_review_file=w.root/"state/wave2_formulation_reviews.jsonl"
    earlier_reviews=jsonl(earlier_review_file)
    earlier_ids={r["formulation_id"] for r in earlier_reviews}
    if len(earlier_ids)!=len(earlier_reviews) or len(earlier_reviews) not in (504,506):
        raise PipelineError("Prior individual mathematical review ledger inconsistent")
    current_links=w.records("relations")
    if {id for r in earlier_reviews for id in r["relation_ids"]} != set(current_links):
        raise PipelineError("Old links not individually documented")
    sources=w.records("sources")
    terms=w.records("terms")
    observations=w.records("observations")
    research={r["id"]:r for r in jsonl(w.root/REVIEWS)}
    if len(research)!=8:
        raise PipelineError("Individual source reviews incomplete")
    proposed=[]
    individual=[]
    for c in CASES:
        tid="term.wave2.real49."+c["num"]
        oid="obs.wave2.real49."+c["num"]
        r=research.get(c["review"]);t=terms.get(tid);o=observations.get(oid)
        if (not r or r["stage_ingested"] or r["production_corpus_consulted"]
            or r["source_primary"]["url"]!=c["url"]
            or not t or not o or t["source_id"]!=c["source"]
            or o["source_id"]!=c["source"] or o["term_id"]!=tid
            or o["locator"]!=c["url"] or o["record_kind"]!="paraphrase"):
            raise PipelineError("Independent real construction evidence incomplete: "+tid)
        src=sources.get(c["source"])
        if not src or src["rights"]!="locator_only" or src["access"]!="free":
            raise PipelineError("Missing independently reviewed locator-only source: "+c["source"])
        if len(c["reason"])<180:
            raise PipelineError("Too little individual mathematical reasoning")
        proposed.append({
          "id":c["meaning"],"term_group_id":"wave2.real51."+c["num"],
          "display_term":c["label"],"context":c["context"],"term_ids":[tid],
          "editorial_status":"source_scoped_mathematical_formulation_screened",
          "editorial_screening_reason":c["reason"],
          "independent_review_id":c["review"],"human_verified":False,
          "formulations":[{
            "id":c["form"],"text":c["formulation"],"review_state":"screened",
            "evidence_ids":[oid],"source_screened_by":"assistant_independent_cauchy_foundation_math_screen_2026_10_20",
            "human_verified":False}]
        })
        individual.append({
          "review_id":"review.wave2.real51."+c["num"],
          "meaning_id":c["meaning"],"formulation_id":c["form"],
          "source_evidence_id":oid,"source_locator":c["url"],
          "mathematical_reason":c["reason"],
          "decision":"individually_source_scoped_definition_screened",
          "prerequisites_not_yet_reviewed":True,
          "human_verified":False,"production_corpus_consulted":False,
          "reviewed_by":"assistant_independent_cauchy_foundation_math_screen_2026_10_20"
        })
    store(w.root/"wave2/cauchy_individual_meaning_reviews_batch_51.jsonl",individual)
    incoming=store(w.root/"intake/real51_cauchy_meanings.jsonl",proposed)
    archive=w.root/"state/wave2_formulation_reviews_snapshot_504_before_real51.jsonl"
    if len(earlier_meanings)==492:
        if len(earlier_reviews)!=504 or any(r["meaning_catalog_digest"]!=digest(list(earlier_meanings.values())) for r in earlier_reviews):
            raise PipelineError("Historical 504-row review catalog digest stale")
        oldtext=earlier_review_file.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=oldtext:
            raise PipelineError("Conflicting previous 504-review archive")
        archive.write_text(oldtext,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_504_before_real51.json",{
          "rows":504,"links":664,"sha256":hashlib.sha256(oldtext.encode("utf-8")).hexdigest(),
          "human_peer_verified":False})
        w.ingest("meanings",incoming,batch_size=2)
    all_meanings=w.records("meanings")
    if len(all_meanings)!=494 or any(all_meanings.get(x["id"])!=x for x in proposed):
        raise PipelineError("Unexpected Cauchy meaning revision or cardinality")
    previous=jsonl(archive)
    if len(previous)!=504 or len({x["formulation_id"] for x in previous})!=504:
        raise PipelineError("Missing 504 historical reviews")
    newhash=digest(list(all_meanings.values()))
    records=[dict(x,meaning_catalog_digest=newhash) for x in previous]
    for c in CASES:
        records.append({
          "formulation_id":c["form"],"meaning_id":c["meaning"],
          "meaning_catalog_digest":newhash,"decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,
          "source":"independent_rational_Cauchy_source_and_math_review_batch51",
          "editorial_reason":"Mathematical formulation screened; individual dependency review and noncircular link selection pending.",
          "human_verified":False,"reviewed_by":None
        })
    if len(earlier_reviews)==506:
        mapped={x["formulation_id"]:x for x in earlier_reviews}
        if len(mapped)!=506 or any(mapped.get(row["formulation_id"])!=row for row in records):
            raise PipelineError("Existing Cauchy review ledger conflicts")
    else:
        atomic_jsonl(earlier_review_file,sorted(records,key=lambda x:x["formulation_id"]))
    newest=jsonl(earlier_review_file)
    lookup={x["formulation_id"]:x for x in newest}
    if len(newest)!=506 or len(lookup)!=506:
        raise PipelineError("Review ledger missing Cauchy formulation")
    for original in previous:
        newer=lookup[original["formulation_id"]]
        if any(newer.get(k)!=v for k,v in original.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Historical review changed without source evidence")
    if {id for r in newest for id in r["relation_ids"]}!=set(current_links):
        raise PipelineError("Screened relationship lost prior review")
    check_cycles(all_meanings,current_links)
    if dict(Counter(r["decision"] for r in newest))!={
        "linked":498,"no_supported_target":4,"needs_review":4}:
        raise PipelineError("Unexpected individual decision distribution")
    meaningstate=w.state("meanings")
    meaningstate.update(total=494,record_digest=newhash,
                        screened_new_formulations=75,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",meaningstate)
    report={
       "phase":"two_rational_cauchy_foundations_source_screened",
       "screened_meanings":494,"reviewed_formulations":506,"new_meanings":2,
       "old_504_review_dispositions_preserved":True,
       "old_664_links_preserved":True,
       "new_prerequisite_reviews_pending":2,
       "equivalence_uses_only_rational_arithmetic_not_circular_real_limits":True,
       "remaining_Cauchy_quotient_and_positivity_candidates_unpromoted":2,
       "source_content_copied":False,
       "human_peer_verified":False,"production_corpus_used":False,
       "all_stages_unsealed":True,
       "next":"Individually review quotient-model and positive-class definitions; then screen exact, noncircular dependency links for four new formulations."
    }
    atomic_json(w.root/"state/wave2_cauchy_meaning_screen_batch51.json",report)
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace",type=Path,default=Path(ROOT))
    args=parser.parse_args()
    print(json.dumps(run(args.workspace),indent=2))

if __name__=="__main__":main()
