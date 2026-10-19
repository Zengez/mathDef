"""Independent Wave 2 batch 3: ring conventions and small categories.

Two full candidate definitions and one separately sourced scope convention.
No source snippets copied; each mathematical observation independently authored.
"""
import argparse,json
from pathlib import Path
from .core import Workspace,PipelineError,canonical,atomic_json

INPUTS=[
  dict(key="proofwiki.ring-associative", label="associative ring (identity optional)",
       source_id="src.proofwiki",
       locator="https://proofwiki.org/wiki/Definition%3ARing_%28Abstract_Algebra%29",
       text="An associative ring R has binary operations + and · such that (R,+) is an abelian group, (R,·) is a semigroup, and multiplication distributes over addition on both sides. The ProofWiki basic ring convention does not additionally require a multiplicative identity.",
       context="Ring theory: associative, not necessarily unital",
       note="Direct ProofWiki ring axiom list reviewed; do not conflate this convention with Stacks commutative unital rings."),
  dict(key="stacks.small-category",label="small category",
       source_id="src.stacks",
       locator="https://stacks.math.columbia.edu/tag/0013",
       text="A small category C consists of a set Ob(C), sets Hom_C(x,y) for every ordered pair of objects, composition maps Hom_C(y,z)×Hom_C(x,y)→Hom_C(x,z), and identity arrows id_x∈Hom_C(x,x), with associative composition and left and right identity laws.",
       context="Foundational category theory: small categories",
       note="Stacks Section 4.2 Definition 4.2.1. A set of objects is required; no silent extension to a proper class of objects."),
  dict(key="stacks.ring-convention",label="ring convention (Stacks Project)",
       source_id="src.stacks",
       locator="https://stacks.math.columbia.edu/tag/00AQ",
       text="In the Stacks Project, the word ring denotes a commutative ring equipped with a multiplicative identity 1; the zero ring is included. These are source conventions, not a standalone ring-axiom definition.",
       context="Conventions for commutative algebra",
       note="Stacks Section 10.2 is explicitly a convention, not a complete foundational ring definition. Do not publish as a separate rigorous ring definition without axioms.")
]

def run(root):
    w=Workspace(root)
    baseline=w.root/"state/baseline.json"
    if not baseline.exists() or json.loads(baseline.read_text())["mode"]!="second_wave":
        raise PipelineError("Requires independent Wave 2 workspace")
    if any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
        raise PipelineError("Stage sealed; no more unreviewed sources allowed")
    source_map=w.records("sources")
    terms=[]; observations=[];reviews=[]
    for inp in INPUTS:
        source=source_map.get(inp["source_id"])
        if not source or source["access"]!="free" or source["rights"] not in ("locator_only","permitted"):
            raise PipelineError("Source inaccessible or rights unreviewed")
        tid="term.wave2."+inp["key"]
        oid="obs.wave2."+inp["key"]
        terms.append({
          "id":tid,"label":inp["label"],"source_id":inp["source_id"],
          "locator":inp["locator"],"discovery_provenance":"independent_direct_mathematical_page_read_2026_10_19",
          "human_verified":False
        })
        observations.append({
          "id":oid,"term_id":tid,"source_id":inp["source_id"],
          "locator":inp["locator"],"record_kind":"paraphrase",
          "text":inp["text"],"context":inp["context"],
          "editorial_note":inp["note"],"reviewed_by":"assistant_independent_mathematical_source_review_2026_10_19",
          "human_verified":False
        })
        reviews.append({
          "term_id":tid,"source_id":inp["source_id"],"locator":inp["locator"],
          "source_access_outcome":"direct_page_read","candidate_observation_id":oid,
          "editorial_reason":inp["note"],"human_verified":False,
          "source_research_complete":True,"meaning_screened":False
        })
    def store(path,rows):
        path.parent.mkdir(parents=True,exist_ok=True)
        payload="".join(canonical(item)+"\n" for item in rows)
        if path.exists() and path.read_text(encoding="utf-8")!=payload:
            raise PipelineError("Research batch differs from prior committed intake")
        path.write_text(payload,encoding="utf-8")
        return path
    root=w.root
    tr=w.ingest("terms",store(root/"intake/foundations_batch_03_terms.jsonl",terms),batch_size=3)
    or_=w.ingest("observations",store(root/"intake/foundations_batch_03_observations.jsonl",observations),batch_size=3)
    store(root/"wave2/foundation_source_discovery_batch_03.jsonl",reviews)
    counts={s:len(w.records(s)) for s in ("sources","terms","observations","meanings","relations")}
    assert counts=={"sources":9,"terms":336,"observations":759,"meanings":426,"relations":445},counts
    report={
      "state":"third_source_review_batch_recorded_unsealed",
      "source_articles_read":3,
      "new_term_locator_records":3,
      "new_mathematical_paraphrase_observations":3,
      "counts":counts,
      "idempotent_term_skips":tr["already_present"],
      "idempotent_observation_skips":or_["already_present"],
      "mathematical_context_caveats":["Ring without required unity in the cited ProofWiki convention",
         "Stacks commutative and unital ring convention is not a full definition",
         "Stacks category is explicitly small (set of objects)"],
      "screened_meaning_additions":0,
      "sealed_stages":0,
      "next":"Form independently labeled candidate meanings for associative rings and small categories; record convention source only as supporting scope information.",
      "original_production_mathdef_consulted":False
    }
    atomic_json(root/"state/wave2_foundations_batch_03.json",report)
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workspace",required=True,type=Path)
    a=ap.parse_args()
    print(json.dumps(run(a.workspace),indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
