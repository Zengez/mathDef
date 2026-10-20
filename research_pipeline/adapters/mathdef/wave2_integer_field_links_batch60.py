"""Batch 60: screen exact integer/fraction-field prerequisites and amend one review.

No original mathDef mathematical corpus or frozen-wave content is consulted.
A new rational-number support changes the historical no-target disposition
ONLY with its preceding review snapshot and explicit amendment event.
"""
from __future__ import annotations
import argparse,json,hashlib
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":402,"observations":826,"meanings":503}
PWINTEGER="https://proofwiki.org/wiki/Definition%3AInteger/Formal_Definition"
PWRING="https://proofwiki.org/wiki/Definition%3ARing_of_Integers"
PWRATIONAL="https://proofwiki.org/wiki/Definition%3ARational_Number"
PWFIELD="https://proofwiki.org/wiki/Definition%3AField_of_Quotients"
STACKS_FIELD="https://stacks.math.columbia.edu/tag/09FJ"
STACKS_DOMAIN="https://stacks.math.columbia.edu/tag/09FE"
EDGES=(
 ("01","form.wave2.integer59.integer-ring","meaning.wave2.integer59.integer-equivalence-class",
  "set of integers",PWRING,PWINTEGER,
  "The ring Z uses the set of integers as its underlying carrier. The independently screened integer-construction meaning provides exactly that object; the ring operations are distinct and must be verified separately."),
 ("02","form.wave2.integer59.fraction-field-integral-domain","meaning.wave2.foundation.integral-domain",
  "commutative integral domain D",STACKS_FIELD,STACKS_DOMAIN,
  "The explicit fraction-pair quotient is defined for an integral domain so the nonzero denominators support the equivalence relation and inverses. A separate Stacks-screened integral-domain meaning matches this exact hypothesis."),
 ("03","form.wave2.integer59.fraction-field-universal","meaning.wave2.foundation.integral-domain",
  "integral domain D",PWFIELD,STACKS_DOMAIN,
  "The universal characterization starts from an integral domain D and requires injective maps into fields. It depends on the same independently defined zero-divisor-free commutative-unital domain, not on arbitrary rings."),
 ("04","form.wave2.rational55.rational-number","meaning.wave2.integer59.integer-ring",
  "integers p",PWRATIONAL,PWRING,
  "The rational fraction representation p/q uses integer numerator and nonzero integer denominator, so the ring Z provides the arithmetic and multiplication needed to compare representations; this cannot depend on later-constructed real numbers."),
 ("05","form.wave2.rational55.rational-number","meaning.wave2.integer59.fraction-field-integral-domain",
  "field of fractions of Z",PWRATIONAL,STACKS_FIELD,
  "The rational field Q is the specific fraction-field construction of the integral domain Z. Its representing equivalence classes are an instance of the independently sourced general fraction-field definition; the models are linked by specialization, not by confusing arbitrary fraction fields with Q.")
)
INTEGER_NO_TARGET={
  "formulation_id":"form.wave2.integer59.integer-equivalence-class",
  "meaning_id":"meaning.wave2.integer59.integer-equivalence-class",
  "source_locator":PWINTEGER,
  "reason":"An integer represented by an equivalence class of natural-number pairs depends on an independently defined natural-number object, the Cartesian product N×N and equivalence classes. None of those basic objects has an appropriately screened dedicated prerequisite meaning in the current reconstruction; an integral domain or rational field is conceptually downstream and would create an invalid foundation reversal.",
  "decision":"no_supported_target","human_verified":False
}

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    payload="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=payload:
        raise PipelineError("Changed independently reviewed relationship record")
    path.write_text(payload,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BASE,"relations")):
        raise PipelineError("Only unsealed independent Wave 2 accepted")
    if {s:len(w.records(s)) for s in BASE}!=BASE:
        raise PipelineError("Unexpected mathematically screened stage")
    meanings=w.records("meanings");obs=w.records("observations")
    byform={form["id"]:(m,form) for m in meanings.values() for form in m["formulations"]}
    if len(byform)!=516:
        raise PipelineError("Expected all 516 individually reviewed formulations")
    earlier_links=w.records("relations")
    if len(earlier_links) not in (676,681):
        raise PipelineError("Unrelated source links changed unexpectedly")
    original={k:v for k,v in earlier_links.items() if not k.startswith("rel.wave2.integer60.")}
    if len(original)!=676:
        raise PipelineError("Historical 676 links must stay intact")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    existing=jsonl(ledger);index={r["formulation_id"]:r for r in existing}
    if len(index)!=516 or len(existing)!=516 or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in existing):
        raise PipelineError("Prior formulation review inventory stale")
    if {id for r in existing for id in r["relation_ids"]}!=set(earlier_links):
        raise PipelineError("Unreviewed old source links")
    additions=[]
    for num,fid,target,phrase,fromurl,targeturl,reason in EDGES:
        if fid not in byform or target not in meanings:
            raise PipelineError("Source/target identity unknown: "+num)
        m,form=byform[fid]
        if (form["review_state"]!="screened"
            or locator(m,obs)!=fromurl or locator(meanings[target],obs)!=targeturl
            or phrase not in form["text"] or len(reason)<170):
            raise PipelineError("Missing exact source-backed mathematical context: "+num)
        additions.append({
          "id":"rel.wave2.integer60."+num,
          "from_formulation":fid,"target_meaning":target,
          "relation_type":"definition_uses","review_state":"screened",
          "source_phrase":phrase,"source_locator":fromurl,
          "target_locator":targeturl,"editorial_reason":reason,
          "reviewed_by":"assistant_independent_integer_fraction_field_links_2026_10_20",
          "human_verified":False
        })
    projected={**original,**{r["id"]:r for r in additions}}
    check_cycles(meanings,projected)
    targets={
       "form.wave2.integer59.integer-equivalence-class",
       "form.wave2.integer59.integer-ring",
       "form.wave2.integer59.fraction-field-integral-domain",
       "form.wave2.integer59.fraction-field-universal"
    }
    rational="form.wave2.rational55.rational-number"
    if len(earlier_links)==676:
        if index[rational]["decision"]!="no_supported_target" or index[rational]["relation_ids"]:
            raise PipelineError("Prior rational-number no-target disposition changed without review")
        if any(index[fid]["decision"]!="needs_review" or index[fid]["relation_ids"] for fid in targets):
            raise PipelineError("Newly screened integer formulations already reviewed")
        text=ledger.read_text(encoding="utf-8")
        archive=w.root/"state/wave2_formulation_reviews_snapshot_516_before_integer60.jsonl"
        if archive.exists() and archive.read_text(encoding="utf-8")!=text:
            raise PipelineError("Historical integer review snapshot mismatch")
        archive.write_text(text,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_516_before_integer60.json",{
          "rows":516,"links":676,"sha256":hashlib.sha256(text.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
    archive=w.root/"state/wave2_formulation_reviews_snapshot_516_before_integer60.jsonl"
    history=jsonl(archive)
    historic={r["formulation_id"]:r for r in history}
    if len(history)!=516 or len(historic)!=516 or historic[rational]["decision"]!="no_supported_target":
        raise PipelineError("No auditable original rational-number decision")
    correction={
       "event_id":"integer60.review.rational-number.no-target-to-two-foundations",
       "formulation_id":rational,
       "previous_review_digest":digest(historic[rational]),
       "previous_decision":"no_supported_target","new_decision":"linked",
       "previous_mathematical_reason":historic[rational]["editorial_reason"],
       "source_scoped_support_ids":[r["id"] for r in additions if r["from_formulation"]==rational],
       "new_reason":"Independently screened integer ring and general fraction-field definitions now give the rational Q=Frac(Z) representation an exact, noncircular foundation.",
       "reviewed_by":"assistant_independent_integer_fraction_field_links_2026_10_20",
       "human_verified":False,"production_corpus_used":False
    }
    store(w.root/"events/rational_number_review_amendment_batch60.jsonl",[correction])
    store(w.root/"wave2/individual_integer_field_links_batch60.jsonl",additions)
    store(w.root/"wave2/integer_construction_no_target_batch60.jsonl",[INTEGER_NO_TARGET])
    intake=store(w.root/"intake/integer_field_prerequisites_batch60.jsonl",additions)
    if len(earlier_links)==676:
        w.ingest("relations",intake,batch_size=5)
    links=w.records("relations")
    if len(links)!=681 or any(links.get(r["id"])!=r for r in additions):
        raise PipelineError("Required independent mathematical relations not recorded")
    check_cycles(meanings,links)
    reviewed=[]
    for original_row in history:
        row=dict(original_row);fid=row["formulation_id"]
        if fid in targets|{rational}:
            refs=[r["id"] for r in additions if r["from_formulation"]==fid]
            row["relation_ids"]=refs
            row["reviewed_by"]="assistant_independent_integer_fraction_field_links_2026_10_20"
            if refs:
                row["decision"]="linked"
                row["source"]="independent_integer_and_fraction_field_prerequisite_review_batch60"
                row["editorial_reason"]="Reviewed exact source term and target meaning with independent provenance, correct dependency orientation and verified acyclicity."
            else:
                if fid!=INTEGER_NO_TARGET["formulation_id"]:
                    raise PipelineError("Unscreened new mathematical prerequisite")
                row["decision"]="no_supported_target"
                row["source"]="independent_integer_construction_no_supported_target_review_batch60"
                row["editorial_reason"]=INTEGER_NO_TARGET["reason"]
            if fid==rational:
                row["previous_review_digest"]=digest(historic[rational])
                row["previous_wave2_decision"]="no_supported_target"
                row["override_event_id"]=correction["event_id"]
        reviewed.append(row)
    if len(earlier_links)==681:
        if {r["formulation_id"]:r for r in existing}!={r["formulation_id"]:r for r in reviewed}:
            raise PipelineError("Repeated integer prerequisites differ from prior screening")
    else:
        atomic_jsonl(ledger,sorted(reviewed,key=lambda r:r["formulation_id"]))
    resulting=jsonl(ledger)
    current={r["formulation_id"]:r for r in resulting}
    if len(current)!=516 or len(resulting)!=516:
        raise PipelineError("Some independently screened formulations unreviewed")
    for fid,old in historic.items():
        if fid not in targets|{rational} and current[fid]!=old:
            raise PipelineError("Historical individual formulation decision altered")
    if {i for r in resulting for i in r["relation_ids"]}!=set(links):
        raise PipelineError("Not all source-linked mathematical relations reviewed")
    dispositions=dict(Counter(x["decision"] for x in resulting))
    if dispositions!={"linked":511,"no_supported_target":5}:
        raise PipelineError("Unexpected pending dependency dispositions "+str(dispositions))
    report={
      "batch":60,"screened_meanings":503,"reviewed_formulations":516,
      "screened_links":681,"new_source_scoped_links":5,
      "unrelated_historical_511_reviews_unchanged":True,
      "old_676_links_preserved":True,
      "one_no_supported_target_explicitly_amended":True,
      "integer_construction_still_awaits_natural_number_foundations":True,
      "all_formulations_individually_reviewed":True,
      "dependency_cycles":False,"human_peer_verified":False,
      "production_corpus_used":False,"all_stages_unsealed":True,
      "next":"Source natural numbers and equivalence-class foundations; continue broad independent missing-term/variant discovery; never conflate real models or field-of-fractions with arbitrary total quotient rings."
    }
    atomic_json(w.root/"state/wave2_integer_field_prerequisite_batch60.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    a=p.parse_args()
    print(json.dumps(run(a.workspace),indent=2))

if __name__=="__main__":main()
