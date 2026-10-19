"""Build seven context-specific, *candidate* Wave 2 meanings from directly read sources.

Candidates are explicitly unapproved: their review_state='candidate', so they
cannot be published until separate mathematical Stage 4 reviews approve them.
The sealed inherited first-wave meanings and relationships remain unmodified.
"""
import argparse
import json
from pathlib import Path
from .core import Workspace, PipelineError, canonical, atomic_json

SPECS = (
  ("group","group","term.wave2.proofwiki.group","obs.wave2.proofwiki.group",
   "Abstract group, with a two-sided identity and inverses; arbitrary binary operation",
   "A group is a set G with a binary operation *: G×G→G such that (a*b)*c = a*(b*c) for all a,b,c∈G, an element e∈G satisfies e*a = a = a*e for each a∈G, and every a∈G has b∈G with a*b = e = b*a.",
   "Requires a group law closed on G, associativity, two-sided identity and inverses; no commutativity imposed."),
  ("abelian-group","abelian group","term.wave2.proofwiki.abelian-group","obs.wave2.proofwiki.abelian-group",
   "Commutative group in abstract algebra",
   "An abelian group is a group (G,*) for which a*b = b*a for every a,b∈G.",
   "Depends on abstract group; distinguish abelian additive notation from categorical abelian objects."),
  ("two-sided-ideal","two-sided ideal of a ring","term.wave2.proofwiki.ideal-of-ring","obs.wave2.proofwiki.ideal-of-ring",
   "Two-sided ring ideal; multiplication need not be commutative",
   "Let R be a ring. A subset I⊆R is a two-sided ideal if (I,+) is an additive subgroup of (R,+) and, for every r∈R and i∈I, both ri and ir belong to I.",
   "Do not conflate left and right ideals for noncommutative rings."),
  ("commutative-prime-ideal","prime ideal of a commutative unital ring",
   "term.wave2.proofwiki.prime-ideal-commutative",
   "obs.wave2.proofwiki.prime-ideal-commutative",
   "Prime ideal in a commutative ring with multiplicative identity",
   "Let R be a commutative ring with identity. An ideal P⊊R is prime if, for all a,b∈R, ab∈P implies a∈P or b∈P.",
   "Properness and the commutative-unital ring hypothesis are necessary; not a generic noncommutative prime-ideal definition."),
  ("left-module-nonunital","left module over a ring, optionally nonunital",
   "term.wave2.proofwiki.left-module","obs.wave2.proofwiki.left-module",
   "General left R-module over an associative ring; unitality a separate condition",
   "Let R be an associative ring and (M,+) an abelian group. A left R-module structure on M is an action R×M→M, (r,m)↦rm, satisfying r(m+n)=rm+rn, (r+s)m=rm+sm, and (rs)m=r(sm). When R has identity, a unital left module additionally satisfies 1_R m=m for all m∈M.",
   "ProofWiki does not universally impose the unitality axiom; common Stacks commutative-algebra conventions do impose it."),
  ("topological-space","topological space",
   "term.wave2.proofwiki.topological-space","obs.wave2.proofwiki.topological-space",
   "Open-set axioms for arbitrary topological spaces, including the empty space",
   "A topological space is a pair (X,τ) with τ⊆P(X) such that ∅∈τ and X∈τ, any union of members of τ is in τ, and intersections of finitely many members of τ are in τ. Members of τ are the open subsets of X.",
   "Do not impose a nonempty underlying space; the open-set axioms allow X=∅."),
  ("regular-noetherian-ring","regular Noetherian ring",
   "term.wave2.regular-noetherian-ring","obs.wave2.regular-noetherian-ring.stacks-00od",
   "Noetherian commutative regular rings defined through regular localizations",
   "A Noetherian commutative ring R is regular if R_p is a regular local ring for every prime ideal p of R.",
   "Stacks Project Definition 10.110.7 tag 00OD; do not assert this exact definition for all non-Noetherian rings or arbitrary noncommutative contexts."),
)

def run(root):
    w=Workspace(root)
    baseline=w.root/"state/baseline.json"
    if not baseline.exists() or json.loads(baseline.read_text())["mode"]!="second_wave":
        raise PipelineError("Only create candidate meanings inside a Wave 2 fork")
    if w.state("meanings").get("sealed"):
        raise PipelineError("Cannot append candidate meanings after sealed Stage 4")
    terms=w.records("terms")
    evidence=w.records("observations")
    existing=w.records("meanings")
    curated=[]
    for slug,title,termid,obsid,context,definition,note in SPECS:
        if termid not in terms or obsid not in evidence:
            raise PipelineError("No actual source-backed evidence for "+slug)
        obs=evidence[obsid]
        if obs["term_id"]!=termid or obs["source_id"]!=terms[termid]["source_id"]:
            raise PipelineError("Candidate source identity mismatch: "+slug)
        if obs["record_kind"]!="paraphrase" or obs.get("human_verified") is not False:
            raise PipelineError("Candidate has wrong evidence provenance: "+slug)
        id="meaning.wave2.foundation."+slug
        row={
          "id":id,"term_group_id":"wave2.foundation."+slug,
          "display_term":title,"context":context,
          "term_ids":[termid],
          "formulations":[{
             "id":"form.wave2.foundation."+slug,
             "text":definition,
             "evidence_ids":[obsid],
             "review_state":"candidate",
             "mathematical_scope_note":note,
             "human_verified":False
          }],
          "candidate_source_locator":obs["locator"],
          "reviewed_by":"assistant_independent_research_candidate_2026_10_19",
          "human_verified":False,
          "editorial_status":"requires_independent_stage4_mathematical_screening"
        }
        if id in existing and row!=existing[id]:
            raise PipelineError("Immutable candidate meaning changed: "+id)
        curated.append(row)
    out=w.root/"intake/wave2_foundation_meaning_candidates_batch_01.jsonl"
    out.parent.mkdir(parents=True,exist_ok=True)
    payload="".join(canonical(x)+"\n" for x in curated)
    if out.exists() and out.read_text(encoding="utf-8")!=payload:
        raise PipelineError("Proposed replacement of existing candidate intake")
    out.write_text(payload,encoding="utf-8")
    applied=w.ingest("meanings",out,batch_size=3)
    meanings=w.records("meanings")
    if len(meanings)!=426 or len(w.records("relations"))!=445:
        raise PipelineError("Unexpected meanings/relations after candidate ingestion")
    if any(m["formulations"][0]["review_state"]!="candidate" for m in curated):
        raise PipelineError("Prematurely accepted source candidates")
    report={
        "status":"seven_wave2_foundation_meanings_are_candidates_only",
        "candidate_meanings_in_batch":7,
        "candidate_formulations_in_batch":7,
        "meanings_in_wave2":426,
        "formulations_in_wave2":438,
        "relations_in_wave2":445,
        "wave1_meanings_inherited_and_untouched":419,
        "new_formulations_screened":0,
        "wave2_meaning_stage_sealed":False,
        "source_review_required":True,
        "mathematical_scope_issues":[
           "Left modules can be nonunital in the cited source",
           "Prime ideal depends on a proper ideal in a commutative unital ring",
           "Regular ring defined over Noetherian commutative rings",
           "Topological space allows empty underlying set"],
        "original_production_mathdef_consulted":False,
        "next":"Triangulate with additional mathematical sources, run explicit candidate screening, then examine eligible definition-uses relations one by one."
    }
    atomic_json(w.root/"state/wave2_meaning_candidates_batch_01.json",report)
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workspace",required=True,type=Path)
    args=ap.parse_args()
    print(json.dumps(run(args.workspace),indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
