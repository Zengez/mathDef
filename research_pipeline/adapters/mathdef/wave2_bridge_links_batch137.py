"""Batch137: individually screen fourteen direct mathematical prerequisites.

No previous 869 link or unrelated 632 formulation decisions may change.
Previously missing Stirling and convex-hull targets are reviewed separately.
"""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":481,"observations":953,"meanings":595}
P="https://proofwiki.org/wiki/Definition%3A"
CONV=P+"Convex_Set_%28Vector_Space%29";FALL=P+"Falling_Factorial"
DELTA=P+"Kronecker_Delta";BIP=P+"Bipartite_Graph"
VEC="https://stacks.math.columbia.edu/tag/09FM"
SUB=P+"Subset";REAL=P+"Real_Number";NAT=P+"Natural_Number"
MAP=P+"Mapping";SIMPLE=P+"Simple_Graph"
F="form.wave2.bridge136."
EDGES=(
 ("01",F+"convex-real.1","meaning.b64bc15f46fe0245.vector-space-over-field","vector space over ℝ",CONV,VEC,
  "Two-point convexity is defined in a real vector space, whose scalar multiplication and vector sum permit tx+(1−t)y. The independently screened field-vector-space concept supplies the linear structure, specialized to the real field."),
 ("02",F+"convex-real.1","meaning.wave2.foundation.subset-nonstrict","C⊆V",CONV,SUB,
  "Convexity belongs to a specified subset C⊆V of the ambient vector space, not to any unrelated abstract structure. The independently sourced subset meaning supplies nonstrict inclusion, including C=∅."),
 ("03",F+"convex-real.1","meaning.wave2.real45.complete-ordered-real-field","t∈[0,1]",CONV,REAL,
  "The coefficient t ranges over the ordered real interval [0,1], so scalar arithmetic, the order and endpoints 0 and 1 come from the independently sourced real-number field; complex unordered scalars are not admitted."),
 ("04",F+"convex-real.2","meaning.b64bc15f46fe0245.vector-space-over-field","real vector space",CONV,VEC,
  "Set-based convexity tC+(1−t)C requires vector addition and scalar multiplication in an ambient real vector space, exactly the specialized independently reviewed vector-space definition."),
 ("05",F+"convex-real.2","meaning.wave2.foundation.subset-nonstrict","C⊆V",CONV,SUB,
  "The Minkowski-set inclusion formulation assumes C is a subset of V and demands tC+(1−t)C⊆C. The independent nonstrict subset concept supplies inclusion, rather than treating subset containment as strict."),
 ("06",F+"convex-real.2","meaning.wave2.real45.complete-ordered-real-field","t∈[0,1]",CONV,REAL,
  "The Minkowski convexity condition quantifies over real t in [0,1]. The independently sourced real-number system supplies both real coefficients and the order defining that interval."),
 ("07",F+"falling-real-nonnegative","meaning.wave2.real45.complete-ordered-real-field","x∈ℝ",FALL,REAL,
  "The falling factorial finite product has a real argument x with each factor x−j formed by real subtraction. The reviewed real field supplies this arithmetic; factorial quotient restrictions are not silently imposed."),
 ("08",F+"falling-real-nonnegative","meaning.wave2.set63.natural-including-zero","n∈ℕ₀",FALL,NAT,
  "The falling factorial index is a nonnegative integer, explicitly including n=0 through an independently sourced vacuous-product rule. The zero-inclusive natural-number meaning supplies the required k=0 Stirling polynomial term."),
 ("09",F+"numeric-delta.1","meaning.wave2.foundation.mapping-element-assignment","δ:Γ×Γ→{0,1}",DELTA,MAP,
  "A numeric Kronecker delta is a total single-valued assignment δ from ordered index pairs to the numerical set {0,1}. The independently sourced mapping definition supplies this typed function interpretation."),
 ("10",F+"numeric-delta.2","meaning.wave2.foundation.mapping-element-assignment","Kronecker delta",DELTA,MAP,
  "The Iverson-indicator representation δ(a,b)=[a=b] is still a function of the index pair, assigning exactly one numerical value. The independently sourced mapping meaning supplies its function-type prerequisite."),
 ("11",F+"simple-bipartite.1","meaning.wave2.graph42.simple-undirected","simple undirected graph",BIP,SIMPLE,
  "The two-part edge criterion is stated for a simple loopless undirected graph G=(V,E), so every edge has two distinct unordered endpoints. The independent simple-graph meaning supplies this edge structure."),
 ("12",F+"simple-bipartite.1","meaning.wave2.foundation.subset-nonstrict","A,B⊆V",BIP,SUB,
  "A bipartition here consists of disjoint subsets A and B of the full vertex set V, with A∪B=V, and either may be empty. The nonstrict subset definition supplies exactly this relation, without importing nonempty-block partition conventions."),
 ("13",F+"simple-bipartite.2","meaning.wave2.graph42.simple-undirected","simple undirected graph",BIP,SIMPLE,
  "The edge-respecting two-color criterion quantifies over edges of a simple undirected graph. The independently sourced simple-graph definition supplies those unordered pairs and excludes loops or parallel edges."),
 ("14",F+"simple-bipartite.2","meaning.wave2.foundation.mapping-element-assignment","function c:V→{0,1}",BIP,MAP,
  "A proper two-coloring is a total vertex-to-color map c:V→{0,1}, whose image need not contain both colors. The independently sourced mapping meaning supplies the typed assignment; color inequality along edges adds the bipartite property.")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Prior source-specific mathematical link review record changed")
    path.write_text(body,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in (*BASE,"relations")):
        raise PipelineError("Requires unsealed independent Wave2")
    if {k:len(w.records(k)) for k in BASE}!=BASE:
        raise PipelineError("Verified Batch136 mathematical meaning baseline missing")
    review=json.loads((w.root/"state/wave2_bridge136_meaning_screen.json").read_text())
    if review.get("screened_meanings")!=595 or review.get("reviewed_formulations")!=639 or not review.get("nonnegative_falling_factorial_zero_case_corroborated"):
        raise PipelineError("Mathematical source reviews from B136 not verified")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=639:raise PipelineError("639 reviewed forms required")
    prior_rel=w.records("relations")
    if len(prior_rel) not in (869,883):raise PipelineError("Unexpected previous individually reviewed link total")
    previous={i:r for i,r in prior_rel.items() if not i.startswith("rel.wave2.bridge137.")}
    if len(previous)!=869:raise PipelineError("All 869 earlier links must be preserved")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    before=jsonl(ledger);old_index={r["formulation_id"]:r for r in before}
    if (len(before)!=639 or len(old_index)!=639
        or any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in before)
        or {i for r in before for i in r["relation_ids"]}!=set(prior_rel)):
        raise PipelineError("Historical individual form review ledger or source attribution invalid")
    edges=[]
    for n,fid,target,phrase,srcurl,tgturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Missing independently screened mathematical source/target "+n)
        _,form=forms[fid];evidence=form.get("evidence_ids",[])
        if (form["review_state"]!="screened" or len(evidence)!=1 or evidence[0] not in obs
            or obs[evidence[0]]["locator"]!=srcurl or locator(ms[target],obs)!=tgturl
            or phrase not in form["text"] or len(reason)<150):
            raise PipelineError("Unverified source phrase, scope or target locator "+n)
        edges.append({"id":"rel.wave2.bridge137."+n,"from_formulation":fid,
          "target_meaning":target,"relation_type":"definition_uses",
          "review_state":"screened","source_phrase":phrase,
          "source_locator":srcurl,"target_locator":tgturl,"editorial_reason":reason,
          "reviewed_by":"assistant_independent_convex_falling_delta_bipartite_dependency_review_2026_10_20",
          "human_verified":False})
    new={fid for fid in forms if fid.startswith(F)}
    if len(new)!=7 or len(edges)!=14 or {x["from_formulation"] for x in edges}!=new:
        raise PipelineError("Exactly fourteen individually screened edges across seven new source forms required")
    check_cycles(ms,{**previous,**{r["id"]:r for r in edges}})
    archive=w.root/"state/wave2_formulation_reviews_snapshot_639_before_bridge137.jsonl"
    if len(prior_rel)==869:
        if any(old_index[fid]["decision"]!="needs_review" or old_index[fid]["relation_ids"] for fid in new):
            raise PipelineError("New forms unexpectedly have completed reviews")
        raw=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=raw:
            raise PipelineError("Older 639-form decision snapshot mutated")
        archive.write_text(raw,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_639_before_bridge137.json",
          {"rows":639,"prior_links":869,"sha256":hashlib.sha256(raw.encode()).hexdigest(),"human_peer_verified":False})
    saved=jsonl(archive);saved_by={r["formulation_id"]:r for r in saved}
    if len(saved)!=639 or len(saved_by)!=639:raise PipelineError("All 639 previous review records must be archived")
    store(w.root/"wave2/bridge137_individual_source_screened_links.jsonl",edges)
    intake=store(w.root/"intake/bridge137_links.jsonl",edges)
    if len(prior_rel)==869:w.ingest("relations",intake,batch_size=14)
    rel=w.records("relations")
    if len(rel)!=883 or any(rel.get(r["id"])!=r for r in edges):
        raise PipelineError("Fourteen individually reviewed relationships not admitted")
    check_cycles(ms,rel)
    changed=[]
    for old in saved:
        row=dict(old);fid=row["formulation_id"]
        if fid in new:
            ids=[x["id"] for x in edges if x["from_formulation"]==fid]
            if not ids:raise PipelineError("One of seven new definitions lacks a direct link disposition")
            row["relation_ids"]=ids;row["decision"]="linked"
            row["reviewed_by"]="assistant_independent_convex_falling_delta_bipartite_dependency_review_2026_10_20"
            row["source"]="independent_convex_falling_delta_bipartite_prerequisites_batch137"
            row["editorial_reason"]="Individually screened mathematical source phrase, target source and convention; prior review decisions unchanged."
        changed.append(row)
    if len(prior_rel)==883:
        if {r["formulation_id"]:r for r in before}!={r["formulation_id"]:r for r in changed}:
            raise PipelineError("Rerun would rewrite previous mathematical individual decisions")
    else:atomic_jsonl(ledger,sorted(changed,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);idx={r["formulation_id"]:r for r in final}
    if len(final)!=639 or len(idx)!=639:raise PipelineError("All 639 individual formulation decisions required")
    for fid,old in saved_by.items():
        if fid not in new and idx[fid]!=old:
            raise PipelineError("Unrelated old formulation review altered")
    if {i for r in final for i in r["relation_ids"]}!=set(rel):
        raise PipelineError("At least one screened mathematical link lacks disposition")
    if dict(Counter(r["decision"] for r in final))!={"linked":633,"no_supported_target":6}:
        raise PipelineError("Final linked/no-target review distribution wrong")
    for path in ("wave2/conv125_quarantined_source_claims.jsonl","wave2/quot118_quarantined_source_claims.jsonl","wave2/directional112_quarantined_source_claims.jsonl"):
        hold=jsonl(w.root/path)
        if len(hold)!=1 or hold[0]["observation_id"] in {i for m in ms.values() for f in m["formulations"] for i in f["evidence_ids"]}:
            raise PipelineError("A known incorrect external source claim was promoted")
    result={"batch":137,"screened_meanings":595,"reviewed_formulations":639,
      "screened_relationships":883,"new_individually_screened_links":14,
      "all_869_prior_links_preserved":True,"all_632_unrelated_formulation_reviews_preserved":True,
      "all_seven_new_formulations_individually_reviewed":True,
      "convex_empty_set_and_real_scalar_conventions_retained":True,
      "falling_factorial_n0_external_corroboration_retained":True,
      "bipartite_empty_color_class_retained":True,
      "three_historic_held_source_claims_unpromoted":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch138 separate retroactive source-specific links from old convex hull and Stirling forms to newly screened convex subset, falling factorial and numeric Kronecker delta."}
    atomic_json(w.root/"state/wave2_bridge137_link_review.json",result);return result
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
