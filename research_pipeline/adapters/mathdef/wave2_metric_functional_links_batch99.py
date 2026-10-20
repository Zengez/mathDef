"""Batch 99: source- and meaning-specific metric/functional prerequisites.

No assertion that the source corpus contains all foundations. Do not link the
normed-division-ring generality to a commutative-field-only vector space.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":432,"observations":872,"meanings":536}
REAL="meaning.wave2.real45.complete-ordered-real-field"
TOPO="meaning.wave2.foundation.topological-space"
VECTOR="meaning.b64bc15f46fe0245.vector-space-over-field"
NORM="meaning.wave2.analysis98.norm-over-normed-division-ring"
SRC_METRIC="https://proofwiki.org/wiki/Definition%3AMetric_Space"
SRC_NORM="https://proofwiki.org/wiki/Definition%3ANorm_on_Vector_Space"
SRC_NORMED="https://proofwiki.org/wiki/Definition%3ANormed_Vector_Space"
SRC_INNER="https://proofwiki.org/wiki/Definition%3AInner_Product_Space"
URL_REAL="https://proofwiki.org/wiki/Definition%3AReal_Number"
URL_TOPO="https://proofwiki.org/wiki/Definition%3ATopological_Space"
URL_VECTOR="https://stacks.math.columbia.edu/tag/09FM"
EDGES=(
 ("01","form.wave2.analysis98.metric-space",REAL,"ℝ",SRC_METRIC,URL_REAL,
  "The source-defined metric is real-valued and subject to positive distance and triangle inequalities. The independently axiomatized ordered real number system supplies its ordered numerical codomain. This is a codomain prerequisite, not an assertion that a metric space itself is complete."),
 ("02","form.wave2.analysis98.metric-space.compatible",TOPO,"topology",SRC_METRIC,URL_TOPO,
  "The topology induced by all open metric balls is a genuine topological space satisfying the open-set axioms. The associated triple must use the specific induced topology τ_d; a merely metrizable topology without a chosen inducing d is not equivalent as specified data."),
 ("03","form.wave2.analysis98.norm-over-normed-division-ring",REAL,"ℝ≥0",SRC_NORM,URL_REAL,
  "The vector norm is a nonnegative real-valued map, so the independently screened ordered real field supplies its output and order structure. A normed division ring K and its scalar absolute-value function are additional foundations not yet independently screened; a field-only source is NOT substituted for them."),
 ("04","form.wave2.analysis98.norm-over-real-or-complex",VECTOR,"vector space",SRC_NORM,URL_VECTOR,
  "The real or complex case presupposes a vector space over the corresponding commutative field. The independently screened field-vector-space definition matches this restricted scalar setting. This link does not claim that all division rings are commutative fields."),
 ("05","form.wave2.analysis98.normed-vector-space",NORM,"norm",SRC_NORMED,SRC_NORM,
  "The source-defined normed vector space is a vector space equipped with a specified norm over a normed division ring. The screened general vector-norm meaning defines exactly that additional function; neither completeness nor an inner product is required, and no field-only simplification is imposed."),
 ("06","form.wave2.analysis98.real-inner-product-space",VECTOR,"real vector space",SRC_INNER,URL_VECTOR,
  "A real inner-product space begins with a real vector space and adds a positive-definite symmetric bilinear form. The independently screened field-vector-space meaning supplies its underlying scalar-vector structure; this link does not impose norm completeness or a complex conjugation convention."),
 ("07","form.wave2.analysis98.complex-inner-product-space",VECTOR,"complex vector space",SRC_INNER,URL_VECTOR,
  "A complex inner-product space begins with a complex vector space and adds a positive-definite Hermitian sesquilinear form. ProofWiki's convention is linear in the first argument and conjugate-linear in the second. The vector-space target is valid over the complex field, not an inner-product equivalence between real and complex settings.")
)

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    text="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=text:
        raise PipelineError("Historical individual functional-analysis link review modified")
    path.write_text(text,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BASE,"relations")):
        raise PipelineError("Independent unsealed Wave 2 required")
    if {s:len(w.records(s)) for s in BASE}!=BASE:
        raise PipelineError("New meaning catalog must be verified before link screening")
    meaning_report=json.loads((w.root/"state/wave2_analysis98_meaning_screen.json").read_text())
    if (meaning_report.get("screened_contextual_meanings")!=536 or
        meaning_report.get("reviewed_formulations")!=561 or
        not meaning_report.get("metric_induced_topology_condition_explicit") or
        not meaning_report.get("prior_554_reviews_preserved")):
        raise PipelineError("Batch98 context screening provenance absent")
    ms=w.records("meanings");obs=w.records("observations")
    forms={form["id"]:(m,form) for m in ms.values() for form in m["formulations"]}
    if len(forms)!=561:
        raise PipelineError("561 individual formulations required")
    oldlinks=w.records("relations")
    if len(oldlinks) not in (735,742):
        raise PipelineError("Unexpected prior reviewed relation count")
    historic={i:r for i,r in oldlinks.items() if not i.startswith("rel.wave2.analysis99.")}
    if len(historic)!=735:
        raise PipelineError("Previous 735 links missing")
    path=w.root/"state/wave2_formulation_reviews.jsonl"
    reviews=jsonl(path);index={r["formulation_id"]:r for r in reviews}
    if (len(reviews)!=561 or len(index)!=561 or
        any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in reviews) or
        {rid for r in reviews for rid in r["relation_ids"]}!=set(oldlinks)):
        raise PipelineError("Previous complete 561-formulation review ledger absent")
    screened=[]
    for n,fid,target,phrase,sourceurl,targeturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Invalid source or target prerequisite "+n)
        m,f=forms[fid]
        ids=f.get("evidence_ids",[])
        if (f["review_state"]!="screened" or len(ids)!=1 or ids[0] not in obs
            or obs[ids[0]]["locator"]!=sourceurl or
            locator(ms[target],obs)!=targeturl or
            phrase not in f["text"] or len(reason)<190):
            raise PipelineError("Individual source phrase, scope, or target locator failed "+n)
        screened.append({
          "id":"rel.wave2.analysis99."+n,"from_formulation":fid,
          "target_meaning":target,"relation_type":"definition_uses",
          "review_state":"screened","source_phrase":phrase,
          "source_locator":sourceurl,"target_locator":targeturl,
          "editorial_reason":reason,
          "reviewed_by":"assistant_independent_metric_functional_link_screen_2026_10_20",
          "human_verified":False
        })
    if len(screened)!=7:
        raise PipelineError("Seven formulation-specific links required")
    newly={f for f in forms if f.startswith("form.wave2.analysis98.")}
    if len(newly)!=7 or {e["from_formulation"] for e in screened}!=newly:
        raise PipelineError("All seven source-screened variants require separate prerequisite decision")
    if any(forms[e["from_formulation"]][0]["id"]==e["target_meaning"] for e in screened):
        raise PipelineError("Self-referential metric/functional link")
    check_cycles(ms,{**historic,**{r["id"]:r for r in screened}})
    snapshot=w.root/"state/wave2_formulation_reviews_snapshot_561_before_analysis99.jsonl"
    if len(oldlinks)==735:
        if any(index[fid]["decision"]!="needs_review" or index[fid]["relation_ids"] for fid in newly):
            raise PipelineError("Batch98 unresolved reviews were prematurely changed")
        text=path.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=text:
            raise PipelineError("Prior 561-formulation review history changed")
        snapshot.write_text(text,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_561_before_analysis99.json",{
          "rows":561,"existing_relations":735,
          "sha256":hashlib.sha256(text.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
    prior=jsonl(snapshot);priormap={r["formulation_id"]:r for r in prior}
    if len(priormap)!=561:
        raise PipelineError("Review snapshot incomplete")
    store(w.root/"wave2/analysis99_individual_source_screened_links.jsonl",screened)
    intake=store(w.root/"intake/analysis99_links.jsonl",screened)
    if len(oldlinks)==735:
        w.ingest("relations",intake,batch_size=7)
    rel=w.records("relations")
    if len(rel)!=742 or any(rel.get(e["id"])!=e for e in screened):
        raise PipelineError("Batch99 individual relationships not ingested")
    check_cycles(ms,rel)
    updated=[]
    for old in prior:
        v=dict(old)
        fid=v["formulation_id"]
        if fid in newly:
            assigned=[e["id"] for e in screened if e["from_formulation"]==fid]
            if len(assigned)!=1:
                raise PipelineError("Exactly one direct prerequisite expected for "+fid)
            v["relation_ids"]=assigned
            v["decision"]="linked"
            v["reviewed_by"]="assistant_independent_metric_functional_link_screen_2026_10_20"
            v["source"]="independent_metric_functional_prerequisite_review_batch99"
            v["editorial_reason"]="Exact source text/locator and semantic target individually checked; additional possible foundations remain research tasks."
        updated.append(v)
    if len(oldlinks)==742:
        if {r["formulation_id"]:r for r in reviews}!={r["formulation_id"]:r for r in updated}:
            raise PipelineError("Repeat run would change previous individual reviews")
    else:
        atomic_jsonl(path,sorted(updated,key=lambda r:r["formulation_id"]))
    final=jsonl(path);ix={r["formulation_id"]:r for r in final}
    if len(ix)!=561 or len(final)!=561:
        raise PipelineError("Final individual review count incorrect")
    for fid,old in priormap.items():
        if fid not in newly and ix[fid]!=old:
            raise PipelineError("Unrelated earlier reviewed mathematical dependency overwritten")
    if {id for r in final for id in r["relation_ids"]}!=set(rel):
        raise PipelineError("Unreviewed dependency link")
    if dict(Counter(r["decision"] for r in final))!={"linked":555,"no_supported_target":6}:
        raise PipelineError("Incorrect formulation review dispositions")
    result={
      "batch":99,"screened_contextual_meanings":536,"reviewed_formulations":561,
      "screened_relationships":742,"new_individual_links":7,
      "prior_735_individual_links_preserved":True,
      "prior_554_unrelated_formulation_reviews_preserved":True,
      "all_seven_new_formulations_individually_link_reviewed":True,
      "metric_topology_relation_requires_canonical_induced_topology":True,
      "division_ring_general_case_not_equated_to_field":True,
      "unresolved_scalar_normed_division_ring_foundation":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch100+: independently source and screen a normed division ring / division ring-valued scalar absolute value, without assuming commutativity, and broaden nonlinear source discovery."
    }
    atomic_json(w.root/"state/wave2_analysis99_link_review.json",result)
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(ap.parse_args().workspace),indent=2))
if __name__=="__main__":
    main()
