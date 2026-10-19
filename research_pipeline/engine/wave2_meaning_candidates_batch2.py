"""Two additional meaning candidates with explicit mathematical conventions."""
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

SPECS=[
  {
    "id":"meaning.wave2.foundation.associative-ring-identity-optional",
    "term_group_id":"wave2.foundation.associative-ring",
    "display_term":"associative ring (identity optional)",
    "context":"ProofWiki abstract ring convention: associative multiplication, no required multiplicative identity",
    "term_ids":["term.wave2.proofwiki.ring-associative"],
    "formulations":[{
      "id":"form.wave2.foundation.associative-ring-identity-optional",
      "text":"An associative ring R is a set with operations + and · for which (R,+) is an abelian group, (R,·) is associative, and multiplication distributes over addition on both sides. A multiplicative identity is not part of this particular source's general ring axioms.",
      "evidence_ids":["obs.wave2.proofwiki.ring-associative"],
      "review_state":"candidate",
      "context_scope":"This includes associative non-unital rings; standard commutative algebra sources commonly impose unity separately.",
      "human_verified":False
    }],
    "editorial_status":"candidate_requires_scope_comparison_with_stacks_ring_convention",
    "human_verified":False
  },
  {
    "id":"meaning.wave2.foundation.small-category",
    "term_group_id":"wave2.foundation.small-category",
    "display_term":"small category",
    "context":"Stacks Project Definition 4.2.1: categories with a set of objects and a set of morphisms for each ordered pair",
    "term_ids":["term.wave2.stacks.small-category"],
    "formulations":[{
      "id":"form.wave2.foundation.small-category",
      "text":"A small category C has a set Ob(C) of objects, sets Hom_C(x,y) for every ordered pair of objects, composition maps Hom_C(y,z)×Hom_C(x,y)→Hom_C(x,z), and arrows id_x∈Hom_C(x,x); compositions are associative and identities act as left and right units.",
      "evidence_ids":["obs.wave2.stacks.small-category"],
      "review_state":"candidate",
      "context_scope":"Stacks 4.2.1: 'small' means object collection is a set, not merely a proper class; avoid automatically generalizing to big categories.",
      "human_verified":False
    }],
    "editorial_status":"candidate_requires_cross_definition_relations_review",
    "human_verified":False
  }
]
def run(root):
    w=Workspace(root)
    baseline=w.root/"state/baseline.json"
    if not baseline.exists() or json.loads(baseline.read_text())["mode"]!="second_wave":
        raise PipelineError("Requires independent Wave 2 fork")
    if w.state("meanings").get("sealed"):
        raise PipelineError("Meanings are sealed")
    existing=w.records("meanings")
    obs=w.records("observations")
    for meaning in SPECS:
        for f in meaning["formulations"]:
            for oid in f["evidence_ids"]:
                if oid not in obs:
                    raise PipelineError("Meaning evidence absent: "+oid)
        if meaning["id"] in existing and meaning!=existing[meaning["id"]]:
            raise PipelineError("Existing meaning changed without revision")
    path=w.root/"intake/wave2_foundation_meaning_candidates_batch_02.jsonl"
    path.parent.mkdir(parents=True,exist_ok=True)
    payload="".join(canonical(row)+"\n" for row in SPECS)
    if path.exists() and path.read_text(encoding="utf-8")!=payload:
        raise PipelineError("Reused prior batch identity with changed definitions")
    path.write_text(payload,encoding="utf-8")
    w.ingest("meanings",path,batch_size=2)
    result=w.records("meanings")
    assert len(result)==428 and sum(len(r["formulations"]) for r in result.values())==440
    assert len(w.records("relations"))==445
    report={
      "status":"two_additional_context_scoped_meaning_candidates_recorded",
      "new_meanings_in_batch":2,
      "total_wave2_meanings":428,
      "total_wave2_formulations":440,
      "inherited_wave1_meanings_unchanged":419,
      "new_candidate_meanings_total":9,
      "mathematically_screened_new_meanings":0,
      "total_inherited_relationships":445,
      "source_conventions_kept_distinct":True,
      "candidate_scope_notes":["ProofWiki ring axioms do not universally require 1",
                             "Stacks convention is commutative and unital",
                             "Stacks category definition is specifically small"],
      "original_production_corpus_consulted":False,
      "next":"Cross-check new concepts and propose then screen only mathematically valid relationship dependencies."
    }
    atomic_json(w.root/"state/wave2_meaning_candidates_batch_02.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",required=True,type=Path)
    x=p.parse_args()
    print(json.dumps(run(x.workspace),indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
