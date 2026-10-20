"""Batch 58: independent sourced integers, integer ring, fraction-field variants.

MathDef-specific adapter over generic Workspace. Never reads production
definitions, production website content or unrelated original mathDef data.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
REVIEWS="wave2/integer_fraction_field_source_review_batch57_2026-10-20.jsonl"
LEADS="wave2/foundation_source_discovery_batch_58.jsonl"
MANIFEST="wave2/additional_source_lead_batches.json"
FIRST={"sources":14,"terms":399,"observations":822,"meanings":500,"relations":676}
FINAL=dict(FIRST,terms=402,observations=826)
SOURCE_TERMS={
 "integer-equivalence-class":("src.proofwiki","https://proofwiki.org/wiki/Definition%3AInteger/Formal_Definition"),
 "integer-ring":("src.proofwiki","https://proofwiki.org/wiki/Definition%3ARing_of_Integers"),
 "fraction-field-integral-domain":("src.stacks","https://stacks.math.columbia.edu/tag/09FJ"),
}
SECONDARY="https://proofwiki.org/wiki/Definition%3AField_of_Quotients"
ALT_FORMULATION=(
 "For an integral domain D, a fraction field may equivalently be specified as "
 "a field F with an injective ring homomorphism i:D→F such that, for every "
 "field K and injective ring homomorphism j:D→K, there is a unique field "
 "homomorphism h:F→K satisfying h∘i=j. This universal mapping property "
 "characterizes the fraction field together with its embedding of D."
)
ALT_REASON=(
 "ProofWiki Definition:Field of Quotients, Definition 3, gives the universal "
 "property with the embedding as part of the data. The quantifier requires "
 "an injective D→K map so all nonzero denominator images are invertible. "
 "The morphism is required to be a field homomorphism compatible with the "
 "embeddings; this is equivalent to the fraction-pair construction after "
 "existence is shown, but is not a definition of the total quotient ring "
 "of an arbitrary ring with zero divisors."
)

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Previously sourced integer/fraction-field batch conflicts")
    path.write_text(content,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in FIRST):
        raise PipelineError("Unsealed independent Wave 2 workspace required")
    if {s:len(w.records(s)) for s in FIRST} not in (FIRST,FINAL):
        raise PipelineError("Unexpected starting research inventory")
    sources=w.records("sources")
    if sources["src.proofwiki"]["rights"]!="permitted" or sources["src.stacks"]["rights"]!="locator_only":
        raise PipelineError("Wrong source-rights status")
    researched={r["key"]:r for r in jsonl(w.root/REVIEWS)}
    if len(researched)!=3 or set(researched)!=set(SOURCE_TERMS):
        raise PipelineError("Only 3 individually examined source candidates permitted")
    terms=[];observations=[];leads=[]
    for key,(src,url) in SOURCE_TERMS.items():
        r=researched[key]
        if (r["source_id"]!=src or r["locator"]!=url or
            r["production_corpus_consulted"] or r["stage_ingested"] or r["meaning_screened"] or
            r["source_access_outcome"]!="direct_page_read" or len(r["reason"])<180):
            raise PipelineError("Invalid mathematical source review: "+key)
        term="term.wave2.integer58."+key
        obs="obs.wave2.integer58."+key
        terms.append({"id":term,"label":r["term"],"source_id":src,"locator":url,
                      "discovery_provenance":REVIEWS,"human_verified":False})
        observations.append({"id":obs,"source_id":src,"term_id":term,"locator":url,
                             "record_kind":"paraphrase","text":r["formulation"],
                             "context":r["context"],"editorial_note":r["reason"],
                             "source_crosscheck_urls":[r["secondary"]] if r.get("secondary") else [],
                             "reviewed_by":"assistant_independent_integer_source_check_2026_10_20",
                             "human_verified":False})
        leads.append({"term_id":term,"source_id":src,"locator":url,
                      "candidate_observation_id":obs,"source_access_outcome":"direct_page_read",
                      "editorial_reason":r["reason"],"source_research_complete":True,
                      "meaning_screened":False,"human_verified":False,
                      "review_reference":r["id"]})
    # A separate independent source supports the equivalent abstract formulation.
    observations.append({
      "id":"obs.wave2.integer58.fraction-field-universal",
      "term_id":"term.wave2.integer58.fraction-field-integral-domain",
      "source_id":"src.proofwiki","locator":SECONDARY,
      "record_kind":"paraphrase","text":ALT_FORMULATION,
      "context":"Fraction field of integral domain: equivalent universal mapping property",
      "editorial_note":ALT_REASON,
      "reviewed_by":"assistant_independent_fraction_field_universal_source_check_2026_10_20",
      "human_verified":False
    })
    if len(ALT_REASON)<220:
        raise PipelineError("Universal-property variant needs source-specific mathematical review")
    t=w.ingest("terms",store(w.root/"intake/integer_foundations_terms_batch58.jsonl",terms),batch_size=3)
    o=w.ingest("observations",store(w.root/"intake/integer_foundations_observations_batch58.jsonl",observations),batch_size=4)
    store(w.root/LEADS,leads)
    path=w.root/MANIFEST
    config=json.loads(path.read_text(encoding="utf-8"))
    expected=["wave2/foundation_source_discovery_batch_49.jsonl","wave2/foundation_source_discovery_batch_54.jsonl"]
    if config.get("schema_version")!=1 or config.get("paths") not in (expected,expected+[LEADS]):
        raise PipelineError("Supplemental source-lead manifest does not match current independently approved batches")
    config["paths"]=expected+[LEADS]
    atomic_json(path,config)
    counts={s:len(w.records(s)) for s in FINAL}
    if counts!=FINAL:
        raise PipelineError("Source intake record cardinality not as reviewed")
    report={
      "batch":58,"scope":"independent source-only integer ring and fraction-field variant intake",
      "counts":counts,"source_terms_added":3,"source_observations_added":4,
      "meaning_formulations_screened":0,"links_screened":0,
      "two_distinct_fraction_field_formulations_sourced":True,
      "integer_ring_integral_domain_status_a_separate_theorem":True,
      "different_from_total_quotient_ring_with_zero_divisors":True,
      "source_text_reused":False,"production_corpus_used":False,"human_peer_verified":False,
      "all_stages_unsealed":True,
      "next":"Screen three independent contextual meanings, with concrete and universal fraction-field variants and complete preservation of 512 previous reviews."
    }
    atomic_json(w.root/"state/wave2_integer_source_batch58.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    args=p.parse_args()
    print(json.dumps(run(args.workspace),indent=2))

if __name__=="__main__":main()
