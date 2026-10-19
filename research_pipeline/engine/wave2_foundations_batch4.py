"""Three directly reviewed Wave 2 foundational source observations.

Only author-original mathematical paraphrases are ingested. They are evidence
candidates, NOT automatically screened meanings. Wave 1 stays cryptographically
frozen, and this script never touches live mathDef definitions or references.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .core import Workspace, PipelineError, canonical, atomic_json

INPUTS = [
    dict(key="proofwiki.unit-of-ring", label="unit of a unital ring",
         source_id="src.proofwiki",
         locator="https://proofwiki.org/wiki/Definition%3AUnit_of_Ring",
         text="If R is an associative ring with multiplicative identity 1_R, an element u in R is a unit if another element v in R satisfies uv=1_R=vu. Its multiplicative inverse must be two-sided.",
         context="Ring theory: units in a ring with unity",
         note="Direct Definition 1; two-sided inverses in a ring with unity. The unit element u is not to be confused with the identity 1_R, sometimes called unity.",
         corroboration=["https://stacks.math.columbia.edu/tag/00AR"]),
    dict(key="stacks.integral-domain", label="integral domain in commutative unital algebra",
         source_id="src.stacks",
         locator="https://stacks.math.columbia.edu/tag/09FE",
         text="In the Stacks Project commutative-unital ring convention, an integral domain is a nonzero commutative ring R in which ab=0 entails a=0 or b=0 for all a,b in R. Thus it has no nonzero zerodivisors.",
         context="Commutative algebra: nonzero integral domain",
         note="Stacks Definition 9.2.2 read directly; Section 10.2 fixes the commutative unital ring convention. Zero ring is not an integral domain.",
         corroboration=["https://stacks.math.columbia.edu/tag/00AQ",
                        "https://proofwiki.org/wiki/Definition%3AIntegral_Domain"]),
    dict(key="proofwiki.maximal-ideal-of-ring", label="maximal ideal of a commutative unital ring",
         source_id="src.proofwiki",
         locator="https://proofwiki.org/wiki/Definition%3AMaximal_Ideal_of_Ring",
         text="For a commutative ring R with identity, an ideal m is maximal if m is proper and there is no ideal J with m strictly contained in J and J strictly contained in R. This is maximality among proper ring ideals.",
         context="Commutative algebra: maximal proper ideals",
         note="ProofWiki definition separates two-sided, left and right ideal variants; the present candidate intentionally restricts to commutative rings with identity. Stacks basic notions corroborate the quotient-field criterion.",
         corroboration=["https://stacks.math.columbia.edu/tag/00AR"]),
]

def run(root):
    w=Workspace(root)
    baseline=w.root/"state/baseline.json"
    if not baseline.exists() or json.loads(baseline.read_text(encoding="utf-8")).get("mode")!="second_wave":
        raise PipelineError("Only a genuine independent second-wave fork can be edited")
    if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
        raise PipelineError("Cannot add source observations after sealing")
    prior={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
    if prior["sources"]!=9 or prior["terms"] not in (336,339) or prior["observations"] not in (759,762):
        raise PipelineError("Unexpected source-term baseline: "+str(prior))
    if prior["meanings"]!=428 or prior["relations"]!=529:
        raise PipelineError("Do not run source expansion before current relationship batch is verified")
    source_map=w.records("sources")
    terms,observations,source_reviews=[],[],[]
    for inp in INPUTS:
        source=source_map[inp["source_id"]]
        if source["access"]!="free" or source["rights"] not in ("permitted","locator_only"):
            raise PipelineError("Disallowed source rights or access: "+inp["source_id"])
        tid="term.wave2."+inp["key"]
        oid="obs.wave2."+inp["key"]
        terms.append({
            "id":tid, "label":inp["label"], "source_id":inp["source_id"],
            "locator":inp["locator"],
            "discovery_provenance":"independent_direct_source_article_read_2026_10_19",
            "human_verified":False
        })
        observations.append({
            "id":oid,"term_id":tid,"source_id":inp["source_id"],
            "locator":inp["locator"],"record_kind":"paraphrase","text":inp["text"],
            "context":inp["context"],"source_definition":"Directly examined definition page",
            "editorial_note":inp["note"],
            "source_crosscheck_urls":inp["corroboration"],
            "reviewed_by":"assistant_independent_mathematical_direct_source_review_2026_10_19",
            "human_verified":False
        })
        source_reviews.append({
            "term_id":tid, "source_id":inp["source_id"],
            "locator":inp["locator"],"source_access_outcome":"direct_page_read",
            "candidate_observation_id":oid,"editorial_reason":inp["note"],
            "source_quality":"Source-specific content read; further semantic screening required",
            "source_crosscheck_urls":inp["corroboration"],
            "source_research_complete":True,"meaning_screened":False,
            "human_verified":False
        })
    def store(path, rows):
        path.parent.mkdir(parents=True,exist_ok=True)
        content="".join(canonical(row)+"\\n" for row in rows)
        if path.exists() and path.read_text(encoding="utf-8")!=content:
            raise PipelineError("Prior source-specific intake differs: "+str(path))
        path.write_text(content,encoding="utf-8")
        return path
    tr=w.ingest("terms",store(w.root/"intake/foundations_batch_04_terms.jsonl",terms),batch_size=3)
    ob=w.ingest("observations",store(w.root/"intake/foundations_batch_04_observations.jsonl",observations),batch_size=3)
    store(w.root/"wave2/foundation_source_discovery_batch_04.jsonl",source_reviews)
    final={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
    expect={"sources":9,"terms":339,"observations":762,"meanings":428,"relations":529}
    if final!=expect:
        raise PipelineError("Unexpected intake result: "+str(final))
    result={
      "state":"fourth_foundational_source_intake_candidate_observations_unsealed",
      "direct_source_articles_read":3,
      "term_records_added":3,"observation_records_added":3,
      "source_scoped_conventions":[
          "unit refers to invertible element of a unital ring, not its unity",
          "integral domain excludes the zero ring, with commutativity and 1 retained",
          "maximal ideal is a proper ideal without intermediate proper ideals in the commutative unital case"],
      "counts":final,"idempotent_term_skips":tr["already_present"],
      "idempotent_observation_skips":ob["already_present"],
      "screened_new_meanings":0,"stages_sealed":0,
      "original_production_mathdef_consulted":False,
      "next":"Rebuild 339-term source coverage without erasing the 336-term audit; then independently screen new meaning candidates and link only justified prerequisites."
    }
    atomic_json(w.root/"state/wave2_foundations_batch_04.json",result)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",required=True,type=Path)
    a=p.parse_args()
    print(json.dumps(run(a.workspace),indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
