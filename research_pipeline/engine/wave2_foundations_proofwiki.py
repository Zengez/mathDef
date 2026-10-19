"""Second Wave 2 foundation intake from directly inspected ProofWiki articles.

These are six newly authored mathematical *paraphrase observations*, supported
by precise independently read source pages. No meaning is screened here and no
Wave 1 or production records are read or revised by this tool.
"""
import argparse
import json
from pathlib import Path
from .core import Workspace, PipelineError, canonical, atomic_json

ROWS = (
    ("group", "group", "https://proofwiki.org/wiki/Definition%3AGroup",
     "A group consists of a set G with a binary operation that is associative, has an identity element e acting on both sides, and gives every element of G a two-sided inverse.",
     "Abstract algebra: groups", "Associativity, identity and inverses explicitly checked."),
    ("abelian-group", "abelian group", "https://proofwiki.org/wiki/Definition%3AAbelian_Group",
     "An abelian group is a group G whose binary operation is commutative: for every a,b in G, ab = ba.",
     "Abstract algebra: commutative groups",
     "The source also offers an equivalence with the centre of G; the elementary commutativity test is the present candidate."),
    ("ideal-of-ring", "ideal of a ring", "https://proofwiki.org/wiki/Definition%3AIdeal_of_Ring",
     "A two-sided ideal I of a ring R is an additive subgroup of R with r i and i r in I for every r in R and i in I; over commutative rings left and right ideals coincide.",
     "Ring theory: two-sided ideals",
     "Retain the distinction between one-sided and two-sided ideals in noncommutative rings."),
    ("prime-ideal-commutative", "prime ideal of a commutative unital ring",
     "https://proofwiki.org/wiki/Definition%3APrime_Ideal_of_Ring/Commutative_and_Unitary_Ring",
     "In a commutative ring R with identity, a prime ideal P is a proper ideal such that for all a,b in R, ab in P implies a in P or b in P.",
     "Commutative algebra: prime ideals",
     "Properness is essential; source includes other equivalent tests, not assumed in this candidate."),
    ("left-module", "left module over a ring",
     "https://proofwiki.org/wiki/Definition%3AModule_over_Ring",
     "A left R-module is an abelian group M with a left action R times M to M that distributes over each additive variable and obeys (rs)m = r(sm); if a unital module is intended, add 1m = m as a separate hypothesis.",
     "Algebra: general left modules",
     "The cited ProofWiki entry does NOT impose unitality universally; preserve the optional convention instead of silently imposing 1m=m."),
    ("topological-space", "topological space",
     "https://proofwiki.org/wiki/Definition%3ATopological_Space",
     "A topological space is a pair (X,tau) where tau is a collection of subsets of X containing the empty set and X and closed under arbitrary unions and finite intersections; the elements of tau are the open sets.",
     "General topology: open-set axioms",
     "The source presents topology on a set and its open-set axioms; the empty space is permitted by this axiom formulation.")
)

def run(workspace):
    w=Workspace(workspace)
    base=w.root/"state/baseline.json"
    if not base.exists() or json.loads(base.read_text())["mode"] != "second_wave":
        raise PipelineError("Only use a genuine second-wave fork")
    if any(w.state(st).get("sealed") for st in ("sources","terms","observations","meanings","relations")):
        raise PipelineError("Cannot run second-wave intake after a stage is sealed")
    source=w.records("sources").get("src.proofwiki")
    if not source or source["access"]!="free" or source["rights"] not in ("permitted","locator_only"):
        raise PipelineError("ProofWiki is not an approved accessible source")
    terms,observations,reviews=[],[],[]
    for key,label,url,body,context,nuance in ROWS:
        tid="term.wave2.proofwiki."+key
        oid="obs.wave2.proofwiki."+key
        terms.append({"id":tid,"label":label,"source_id":"src.proofwiki","locator":url,
                      "discovery_provenance":"wave2_direct_web_source_read_2026_10_19",
                      "human_verified":False})
        observations.append({
            "id":oid,"term_id":tid,"source_id":"src.proofwiki","locator":url,
            "record_kind":"paraphrase", "text":body,"context":context,
            "source_definition":"ProofWiki specific definition article",
            "editorial_note":"Independently authored mathematical paraphrase of the direct source; unsealed, not third-party peer reviewed. "+nuance,
            "reviewed_by":"assistant_independent_source_read_2026_10_19",
            "human_verified":False
        })
        reviews.append({
            "term_id":tid,"source_id":"src.proofwiki","locator":url,"source_access_outcome":"direct_page_read",
            "source_quality":"Community edited; require cross-source mathematical verification before Stage 4 screening.",
            "editorial_reason":"Directly examined the exact ProofWiki definition article. "+nuance,
            "candidate_observation_id":oid,
            "mathematical_evidence_status":"paraphrase_candidate",
            "human_verified":False
        })
    out_dir=w.root/"intake"
    out_dir.mkdir(exist_ok=True)
    def save(name,rows):
        fp=out_dir/name
        payload="".join(canonical(row)+"\n" for row in rows)
        if fp.exists() and fp.read_text(encoding="utf-8")!=payload:
            raise PipelineError("Content differs from existing intake: "+str(fp))
        fp.write_text(payload,encoding="utf-8")
        return fp
    tpath=save("foundations_batch_02_terms.jsonl",terms)
    opath=save("foundations_batch_02_observations.jsonl",observations)
    result_terms=w.ingest("terms",tpath,batch_size=3)
    result_obs=w.ingest("observations",opath,batch_size=3)
    sdir=w.root/"wave2"
    sdir.mkdir(exist_ok=True)
    notes="".join(canonical(row)+"\n" for row in reviews)
    notes_path=sdir/"foundation_source_discovery_batch_02.jsonl"
    if notes_path.exists() and notes_path.read_text(encoding="utf-8")!=notes:
        raise PipelineError("Existing direct-source review notes differ")
    notes_path.write_text(notes,encoding="utf-8")
    counts={"sources":len(w.records("sources")),"terms":len(w.records("terms")),
            "observations":len(w.records("observations")),"meanings":len(w.records("meanings")),
            "relations":len(w.records("relations"))}
    if counts!={"sources":9,"terms":333,"observations":756,"meanings":419,"relations":445}:
        raise PipelineError("Unexpected revised corpus counts; investigate before checkpoint: "+str(counts))
    report={
        "state":"six_independent_proofwiki_foundation_observations_saved_unsealed",
        "accepted_as_verified_source_research_pages":6,
        "term_records_from_batch":len(terms),
        "paraphrase_observation_records_from_batch":len(observations),
        "idempotent_replay_terms_skipped":result_terms["already_present"],
        "idempotent_replay_observations_skipped":result_obs["already_present"],
        "registry_counts":counts,
        "all_second_wave_stages_unsealed":True,
        "source_context_alerts":["Left module unitality not imposed without extra axiom",
                                 "Prime ideal definition requires properness and commutative unital base",
                                 "Community source needs independent cross-checking"],
        "no_screened_new_meanings":True,
        "no_production_baseline_comparison":True,
        "next":"Cross-check foundation definitions with independent authoritative sources; revisit source-blocked EOM pages or replace them, then construct and screen mathematical meaning variants."
    }
    atomic_json(w.root/"state/wave2_foundations_batch_02.json",report)
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace",required=True,type=Path)
    args=parser.parse_args()
    print(json.dumps(run(args.workspace),indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
