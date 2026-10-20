"""Screen integer construction, integer ring, and two fraction-field variants.

Uses only independently source-reviewed Wave 2 records. Does not consult
production mathDef mathematical content or alter the frozen Wave 1.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
RESEARCH="wave2/integer_fraction_field_source_review_batch57_2026-10-20.jsonl"
BEFORE={"sources":14,"terms":402,"observations":826,"meanings":500,"relations":676}
AFTER=dict(BEFORE,meanings=503)
CONCRETE={
 "integer-equivalence-class":(
    "Integer: natural-pair difference classes",
    "An integer is an equivalence class [a,b] of pairs of natural numbers, where (a,b)∼(c,d) exactly when a+d=b+c. The integers may be realized as the quotient set (N×N)/∼, with [a,b] understood as the formal difference of a and b.",
    "The equivalence relation is expressed using only natural addition, and so avoids circularly using integer subtraction. This is a concrete model of the integers; the induced additive structure and ring operations are separately proved well-defined."
 ),
 "integer-ring":(
    "Algebraic integer ring Z under its usual addition and multiplication",
    "The ring of integers is the structure (Z,+,·) formed by the set of integers together with integer addition and integer multiplication.",
    "ProofWiki's precise definition is the named algebraic structure (Z,+,·). Commutativity, identity and the absence of zero divisors are properties established by separate theorems; they must not be silently used as the definition. This is not the ring of integers of an arbitrary number field."
 ),
 "fraction-field-integral-domain":(
    "Integral-domain fraction field: concrete fraction-equivalence construction",
    "For a commutative integral domain D, the fraction field Frac(D) is constructed from pairs (a,b) with a∈D and 0≠b∈D, where (a,b)∼(c,d) iff ad=bc. The class of (a,b) is written a/b; addition and multiplication are defined on such classes so that D embeds into the resulting field.",
    "The Stacks Project Example 9.3.4 explicitly describes fractions over a domain, the equivalence criterion and the resulting quotient field. The assumption that D has no zero divisors ensures this is an equivalence relation and allows inverses of nonzero classes. It differs from a localization at non-zero-divisors of an arbitrary ring."
 )
}
ALT={
 "id":"form.wave2.integer59.fraction-field-universal",
 "text":"Equivalently, a fraction field of an integral domain D is a field F with an injective ring map i:D→F satisfying: for every field K and injective ring map j:D→K, there exists a unique field homomorphism h:F→K for which h∘i=j.",
 "reason":"ProofWiki Definition:Field of Quotients, Definition 3, states the universal property for a chosen embedding. The injectivity of j ensures the nonzero denominators remain invertible. The statement is equivalent to the fraction-pairs construction once existence and uniqueness are established, but it does not specify a total quotient ring of a ring with zero divisors.",
 "obs":"obs.wave2.integer58.fraction-field-universal",
 "url":"https://proofwiki.org/wiki/Definition%3AField_of_Quotients"
}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Individual screening is not idempotent")
    path.write_text(content,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Only unsealed independent Wave 2 may change")
    counts={s:len(w.records(s)) for s in BEFORE}
    if counts not in (BEFORE,AFTER):
        raise PipelineError("Unexpected source-screened baseline: "+str(counts))
    researched={r["key"]:r for r in jsonl(w.root/RESEARCH)}
    if len(researched)!=3 or set(researched)!=set(CONCRETE):
        raise PipelineError("Three source-researched candidate decisions required")
    observations=w.records("observations")
    terms=w.records("terms")
    sources=w.records("sources")
    new=[];individual=[]
    for key,(context,body,reason) in CONCRETE.items():
        r=researched[key]
        term="term.wave2.integer58."+key
        obs="obs.wave2.integer58."+key
        mid="meaning.wave2.integer59."+key
        fid="form.wave2.integer59."+key
        if (r["production_corpus_consulted"] or r["meaning_screened"] or r["stage_ingested"]
            or not terms.get(term) or terms[term]["source_id"]!=r["source_id"]
            or terms[term]["locator"]!=r["locator"]
            or not observations.get(obs) or observations[obs]["term_id"]!=term
            or observations[obs]["source_id"]!=r["source_id"]
            or observations[obs]["locator"]!=r["locator"]
            or sources[r["source_id"]]["access"]!="free"
            or sources[r["source_id"]]["rights"] not in ("permitted","locator_only")
            or len(reason)<175):
            raise PipelineError("Source and mathematical context not verified for "+key)
        form={"id":fid,"text":body,"evidence_ids":[obs],"review_state":"screened",
              "source_screened_by":"assistant_independent_integer_math_screen_2026_10_20",
              "human_verified":False,"mathematical_review_reason":reason}
        forms=[form]
        if key=="fraction-field-integral-domain":
            other=observations.get(ALT["obs"])
            if (not other or other["term_id"]!=term or other["source_id"]!="src.proofwiki"
                or other["locator"]!=ALT["url"] or len(ALT["reason"])<180):
                raise PipelineError("Missing independent universal-property source")
            forms.append({
              "id":ALT["id"],"text":ALT["text"],"evidence_ids":[ALT["obs"]],
              "review_state":"screened","human_verified":False,
              "source_screened_by":"assistant_independent_fraction_field_alternative_screen_2026_10_20",
              "mathematical_review_reason":ALT["reason"]
            })
        new.append({
           "id":mid,"term_group_id":"wave2.integer59."+key,
           "display_term":r["term"],"context":context,"term_ids":[term],
           "editorial_status":"individual_source_and_math_screened",
           "editorial_screening_reason":reason,
           "independent_review_id":r["id"],"human_verified":False,
           "formulations":forms
        })
        for f in forms:
            individual.append({
              "review_id":"review.wave2.integer59."+f["id"],
              "meaning_id":mid,"formulation_id":f["id"],
              "source_observation_id":f["evidence_ids"][0],
              "mathematical_reason":f["mathematical_review_reason"],
              "decision":"mathematically_screened_pending_independent_prerequisite_review",
              "human_verified":False,"production_corpus_used":False
            })
    store(w.root/"wave2/integer_field_meaning_individual_reviews_batch59.jsonl",individual)
    f=store(w.root/"intake/integer_field_meanings_batch59.jsonl",new)
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    existing=jsonl(ledger)
    earlier=w.records("meanings")
    if len(existing) not in (512,516) or len({r["formulation_id"] for r in existing})!=len(existing):
        raise PipelineError("Historical formulation review coverage invalid")
    if {id for r in existing for id in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Historical relationship reviews do not match")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_512_before_integer59.jsonl"
    if len(earlier)==500:
        if len(existing)!=512 or any(r["meaning_catalog_digest"]!=digest(list(earlier.values())) for r in existing):
            raise PipelineError("Historical meaning review digest stale")
        prior=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=prior:
            raise PipelineError("Conflicting historical review snapshot")
        archive.write_text(prior,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_512_before_integer59.json",{
          "rows":512,"screened_links":676,
          "sha256":hashlib.sha256(prior.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
        w.ingest("meanings",f,batch_size=3)
    meanings=w.records("meanings")
    if len(meanings)!=503 or any(meanings.get(x["id"])!=x for x in new):
        raise PipelineError("New source-screened definitions are missing or changed")
    past=jsonl(archive)
    if len(past)!=512 or len({r["formulation_id"] for r in past})!=512:
        raise PipelineError("Missing preserved 512-review history")
    version=digest(list(meanings.values()))
    reviews=[dict(r,meaning_catalog_digest=version) for r in past]
    for x in new:
        for form in x["formulations"]:
            reviews.append({
              "formulation_id":form["id"],"meaning_id":x["id"],
              "meaning_catalog_digest":version,"decision":"needs_review",
              "relation_ids":[],"original_wave1_disposition":None,
              "source":"independent_integer_fraction_field_review_batch59",
              "editorial_reason":"Individually screened mathematical meaning and source; exact noncircular prerequisite decision pending.",
              "human_verified":False,"reviewed_by":None
            })
    if len(existing)==516:
        indexed={r["formulation_id"]:r for r in existing}
        if len(indexed)!=516 or any(indexed.get(r["formulation_id"])!=r for r in reviews):
            raise PipelineError("Previously run integer screening disagrees with current meaning state")
    else:
        atomic_jsonl(ledger,sorted(reviews,key=lambda r:r["formulation_id"]))
    current=jsonl(ledger)
    checked={r["formulation_id"]:r for r in current}
    if len(current)!=516 or len(checked)!=516:
        raise PipelineError("New screened meaning lacks a review row")
    for previous in past:
        new_row=checked[previous["formulation_id"]]
        if any(new_row.get(k)!=v for k,v in previous.items() if k!="meaning_catalog_digest"):
            raise PipelineError("A prior screened formulation decision was altered")
    if {id for r in current for id in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("An old source-linked relationship was altered")
    check_cycles(meanings,w.records("relations"))
    if dict(Counter(r["decision"] for r in current))!={
        "linked":507,"no_supported_target":5,"needs_review":4
    }:
        raise PipelineError("Review disposition cardinality mismatch")
    state=w.state("meanings")
    state.update(total=503,record_digest=version,screened_new_formulations=85,
                 stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
      "batch":59,"meanings":503,"formulations":516,"links":676,
      "new_contextual_meanings":3,"new_screened_formulations":4,
      "fraction_field_equivalent_contextual_variants":2,
      "prior_512_individual_review_decisions_preserved":True,
      "prior_676_links_preserved":True,"pending_prerequisite_reviews":4,
      "ring_Z_integral_domain_status_is_a_theorem":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "all_stages_unsealed":True,
      "next":"Screen explicit fraction/integer prerequisites, preserve 512 old reviews and review rational number no-target override only when exact foundations exist."
    }
    atomic_json(w.root/"state/wave2_integer_meanings_batch59.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    args=p.parse_args()
    print(json.dumps(run(args.workspace),indent=2))

if __name__=="__main__":main()
