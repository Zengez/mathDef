"""Screen four independently sourced rational foundations, retaining 508 previous reviews.

This mathDef adapter uses only Wave 2 evidence and generic record operations.
Original mathDef production definitions/citations are not read.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from collections import Counter
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
RESEARCH="wave2/rational_foundations_source_review_batch54_2026-10-20.jsonl"
START={"sources":14,"terms":399,"observations":822,"meanings":496,"relations":670}
END=dict(START,meanings=500)
SPECS=[
 ("rational-number","Rational arithmetic: field of integer fractions, constructed without R"),
 ("rational-sequence","Infinite rational-valued function indexed by positive integers, not a rational limit"),
 ("rational-absolute-value","Rational-field modulus based on sign, not the real square-root definition"),
 ("strictly-positive-rational","Strict rational positivity for epsilon quantifiers; excludes zero")
]
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    payload="".join(canonical(row)+"\n" for row in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=payload:
        raise PipelineError("Conflict with individually sourced rational foundation research")
    path.write_text(payload,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in START):
        raise PipelineError("Independent unsealed Wave 2 required")
    counts={s:len(w.records(s)) for s in START}
    if counts not in (START,END):
        raise PipelineError("Unexpected source/definition baseline "+str(counts))
    researched={x["id"]:x for x in jsonl(w.root/RESEARCH)}
    if len(researched)!=4 or set(researched)!={key for key,_ in SPECS}:
        raise PipelineError("Expected four individually reviewed mathematical source candidates")
    original_meanings=w.records("meanings")
    sources=w.records("sources");terms=w.records("terms");obs=w.records("observations")
    source=sources.get("src.proofwiki")
    if not source or source["access"]!="free" or source["rights"]!="permitted":
        raise PipelineError("Expected reviewed independent source")
    incoming=[];individual=[]
    for key,context in SPECS:
        x=researched[key]
        term="term.wave2.rational54."+key
        evidence="obs.wave2.rational54."+key
        mid="meaning.wave2.rational55."+key
        fid="form.wave2.rational55."+key
        if (x["source_id"]!="src.proofwiki" or x["source_access_outcome"]!="direct_page_read"
            or x["meaning_screened"] or x["stage_ingested"] or x["production_corpus_consulted"]
            or x["human_verified"] is not False or len(x["reason"])<170
            or not terms.get(term) or terms[term]["locator"]!=x["source_url"]
            or not obs.get(evidence) or obs[evidence]["term_id"]!=term
            or obs[evidence]["locator"]!=x["source_url"]
            or obs[evidence]["source_id"]!="src.proofwiki"):
            raise PipelineError("Math/source/rights evidence changed "+key)
        if key=="strictly-positive-rational" and ("zero is excluded" not in x["text"] or "≥0" not in x["reason"]):
            raise PipelineError("Strictly positive rational cannot include epsilon=0")
        if key=="rational-absolute-value" and ("square roots" not in x["text"] or "without" not in x["text"]):
            raise PipelineError("Rational absolute value must not require reals")
        incoming.append({
            "id":mid,"term_group_id":"wave2.rational55."+key,
            "display_term":x["term"],"context":context,"term_ids":[term],
            "editorial_status":"source_scoped_mathematical_formulation_screened",
            "editorial_screening_reason":x["reason"],"human_verified":False,
            "source_research_id":x["review_id"],
            "formulations":[{
                "id":fid,"text":x["text"],"evidence_ids":[evidence],
                "review_state":"screened","human_verified":False,
                "source_screened_by":"assistant_independent_rational_foundations_math_screen_2026_10_20"
            }]
        })
        individual.append({
            "review_id":"review.wave2.rational55."+key,"formulation_id":fid,
            "meaning_id":mid,"source_evidence_id":evidence,
            "source_locator":x["source_url"],"mathematical_reason":x["reason"],
            "decision":"mathematically_screened_foundation_pending_dependency_review",
            "reviewed_by":"assistant_independent_rational_foundations_math_screen_2026_10_20",
            "human_verified":False,"production_corpus_used":False
        })
    store(w.root/"wave2/rational_foundations_individual_meaning_reviews_batch55.jsonl",individual)
    file=store(w.root/"intake/rational_foundations_meanings_batch55.jsonl",incoming)
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prior=jsonl(ledger)
    if len(prior) not in (508,512) or len({r["formulation_id"] for r in prior})!=len(prior):
        raise PipelineError("Prior formulation review ledger incomplete")
    original_rel=w.records("relations")
    if {i for r in prior for i in r["relation_ids"]}!=set(original_rel):
        raise PipelineError("Unreviewed existing relations")
    historical=w.root/"state/wave2_formulation_reviews_snapshot_508_before_rational55.jsonl"
    if len(original_meanings)==496:
        if len(prior)!=508 or any(r["meaning_catalog_digest"]!=digest(list(original_meanings.values())) for r in prior):
            raise PipelineError("Existing 508-row review version out of date")
        prior_text=ledger.read_text(encoding="utf-8")
        if historical.exists() and historical.read_text(encoding="utf-8")!=prior_text:
            raise PipelineError("Prior 508-row audit snapshot was modified")
        historical.write_text(prior_text,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_508_before_rational55.json",{
            "rows":508,"screened_links":670,"sha256":hashlib.sha256(prior_text.encode("utf-8")).hexdigest(),
            "human_peer_verified":False})
        w.ingest("meanings",file,batch_size=4)
    now=w.records("meanings")
    if len(now)!=500 or any(now.get(x["id"])!=x for x in incoming):
        raise PipelineError("Individually screened meaning definitions differ from research candidates")
    earlier=jsonl(historical)
    if len(earlier)!=508 or len({r["formulation_id"] for r in earlier})!=508:
        raise PipelineError("Missing prior individual review snapshot")
    version=digest(list(now.values()))
    updated=[dict(r,meaning_catalog_digest=version) for r in earlier]
    for item in incoming:
        updated.append({
           "formulation_id":item["formulations"][0]["id"],"meaning_id":item["id"],
           "meaning_catalog_digest":version,"decision":"needs_review","relation_ids":[],
           "original_wave1_disposition":None,
           "source":"independent_rational_arithmetic_foundation_screen_batch55",
           "editorial_reason":"Mathematical meaning screened; noncircular, exact-source prerequisite review is separate.",
           "human_verified":False,"reviewed_by":None
        })
    if len(prior)==512:
        previous={r["formulation_id"]:r for r in prior}
        if len(previous)!=512 or any(previous.get(r["formulation_id"])!=r for r in updated):
            raise PipelineError("Previous mathematical meaning review conflicts")
    else:
        atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger)
    current={r["formulation_id"]:r for r in final}
    if len(current)!=512 or len(final)!=512:
        raise PipelineError("Screened meaning lacks an individual review entry")
    for old in earlier:
        new=current[old["formulation_id"]]
        if any(new.get(k)!=v for k,v in old.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Historical review changed silently")
    if {i for r in final for i in r["relation_ids"]}!=set(original_rel):
        raise PipelineError("Historic relationship lost")
    check_cycles(now,original_rel)
    if dict(Counter(r["decision"] for r in final))!={"linked":503,"no_supported_target":5,"needs_review":4}:
        raise PipelineError("Unexpected screened/pending mathematical review outcomes")
    state=w.state("meanings")
    state.update(total=500,record_digest=version,
                 screened_new_formulations=81,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
       "phase":"four_individual_rational_arithmetic_and_sequence_foundations_screened",
       "counts":{s:len(w.records(s)) for s in END},
       "new_meanings":4,"formulations":512,
       "historical_508_dispositions_preserved":True,
       "original_670_links_preserved":True,
       "new_prerequisite_reviews_pending":4,
       "rational_epsilons_strictly_positive":True,
       "rational_absolute_value_does_not_require_reals":True,
       "peer_verified":False,"production_corpus_used":False,
       "all_stages_unsealed":True,
       "next":"Individually link rational Cauchy and equivalence definitions to these new foundations, without cycles or unsupported links."
    }
    atomic_json(w.root/"state/wave2_rational_meanings_batch55.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    args=p.parse_args()
    print(json.dumps(run(args.workspace),indent=2))

if __name__=="__main__":main()
