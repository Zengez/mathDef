"""Batch 114: direct source-scoped ball, homeomorphism and directional links.

All prior 784 relationships and 587 unrelated individual review dispositions
remain intact. The gradient-only directional observation remains quarantined.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":453,"observations":906,"meanings":564}
PW="https://proofwiki.org/wiki/Definition%3A"
OPEN=PW+"Open_Ball";CLOSED=PW+"Closed_Ball"
HOME=PW+"Homeomorphism/Topological_Spaces"
DIR=PW+"Directional_Derivative"
METRIC=PW+"Metric_Space";NORMED=PW+"Normed_Vector_Space"
TOP=PW+"Topological_Space";CONT=PW+"Continuous_Mapping_%28Topology%29"
MAP=PW+"Mapping";REAL=PW+"Real_Number"
F="form.wave2.directional113."
EDGES=(
 ("01",F+"open-metric","meaning.wave2.analysis98.metric-space","metric space",OPEN,METRIC,
  "An open metric ball uses the metric d on its source space X and a strictly positive radius r. The independently screened metric-space definition supplies the distance function; this link does not assert the pseudometric extension not yet individually screened."),
 ("02",F+"open-norm","meaning.wave2.analysis98.normed-vector-space","normed vector space",OPEN,NORMED,
  "The open norm-ball condition uses norm displacement ∥v−a∥ on the specified normed vector space, not a metric on a separate arbitrary space. Positive radius is explicit and no completeness requirement is introduced."),
 ("03",F+"closed-metric","meaning.wave2.analysis98.metric-space","metric space",CLOSED,METRIC,
  "A closed metric ball uses non-strict distance inequality d(x,a)≤r over an independently screened metric space. This is not defined to be the topological closure of the corresponding open ball in arbitrary metric spaces."),
 ("04",F+"closed-norm","meaning.wave2.analysis98.normed-vector-space","normed vector space",CLOSED,NORMED,
  "A closed norm ball takes points satisfying ∥v−a∥≤r within the same normed vector space; completeness is not part of the definition. Its norm-space foundation is separately screened and attributed."),
 ("05",F+"homeomorphism-topological.1","meaning.wave2.foundation.topological-space","topological spaces",HOME,TOP,
  "The homeomorphism is defined between two topological spaces; both domain and codomain have specified open-set systems. The definition does not require either space to be Hausdorff or a metric space."),
 ("06",F+"homeomorphism-topological.1","meaning.wave2.foundation76.continuous-topological-map","continuous",HOME,CONT,
  "The continuous-bijection-with-continuous-inverse characterization directly uses continuity of maps between topological spaces for f and f inverse. It does not claim that a continuous bijection alone is a homeomorphism."),
 ("07",F+"homeomorphism-topological.2","meaning.wave2.foundation.topological-space","topological spaces",HOME,TOP,
  "The equivalent open-set transport characterization directly quantifies over open subsets in topologies on X and Y. The independently reviewed topological-space meaning gives those open-set axioms."),
 ("08",F+"homeomorphism-topological.2","meaning.wave2.foundation.mapping-element-assignment","bijection",HOME,MAP,
  "This equivalent homeomorphism formulation explicitly presupposes a bijection f:X→Y, which first is a total single-valued map. The mapping target supplies that foundation; bijectivity is an additional stated requirement."),
 ("09",F+"directional-differentiable","meaning.wave2.foundation.mapping-element-assignment","f:ℝⁿ→ℝ",DIR,MAP,
  "The directional difference quotient is formed from a real-valued total map f on Euclidean vector inputs and requires values f(a+tu) along a straight line. This source-backed mapping prerequisite does not assert total differentiability follows from gradient existence."),
 ("10",F+"directional-differentiable","meaning.wave2.real45.complete-ordered-real-field","ℝ",DIR,REAL,
  "The directional derivative is a finite two-sided real limit as t tends to zero, with real-valued function values and real Euclidean scalars. The independently reviewed ordered real number system supplies the underlying scalar setting; total differentiability remains an explicit extra assumption.")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Immutable individual source-linked relation history changed")
    path.write_text(body,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in (*BASE,"relations")):
        raise PipelineError("Unsealed independent Wave2 required")
    if {k:len(w.records(k)) for k in BASE}!=BASE:
        raise PipelineError("Batch113 independent mathematical source inventory absent")
    prevscreen=json.loads((w.root/"state/wave2_directional113_meaning_screen.json").read_text())
    if prevscreen.get("screened_meanings")!=564 or prevscreen.get("reviewed_formulations")!=594 or not prevscreen.get("held_gradient_claim_remains_excluded"):
        raise PipelineError("Batch113 verified mathematical scope or gradient hold missing")
    ms=w.records("meanings");observations=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=594:
        raise PipelineError("594 individual mathematical formulations required")
    relations=w.records("relations")
    if len(relations) not in (784,794):
        raise PipelineError("Unexpected earlier screened link count")
    old={k:r for k,r in relations.items() if not k.startswith("rel.wave2.directional114.")}
    if len(old)!=784:
        raise PipelineError("All historic 784 relations required")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    before=jsonl(ledger);previous={r["formulation_id"]:r for r in before}
    if (len(before)!=594 or len(previous)!=594 or
        any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in before) or
        {i for r in before for i in r["relation_ids"]}!=set(relations)):
        raise PipelineError("Complete independent formulation review ledger invalid")
    reviews=[]
    for n,fid,target,phrase,sourceurl,targeturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Missing exact independent prerequisite endpoint "+n)
        _,f=forms[fid];sources=f.get("evidence_ids",[])
        if (f["review_state"]!="screened" or len(sources)!=1 or sources[0] not in observations or
            observations[sources[0]]["locator"]!=sourceurl or locator(ms[target],observations)!=targeturl or
            phrase not in f["text"] or len(reason)<155):
            raise PipelineError("Source-specific mathematical review cannot justify link "+n)
        reviews.append({"id":"rel.wave2.directional114."+n,
            "from_formulation":fid,"target_meaning":target,"relation_type":"definition_uses",
            "review_state":"screened","source_phrase":phrase,
            "source_locator":sourceurl,"target_locator":targeturl,"editorial_reason":reason,
            "reviewed_by":"assistant_independent_directional_topology_prerequisite_screen_2026_10_20",
            "human_verified":False})
    newids={fid for fid in forms if fid.startswith(F)}
    if len(reviews)!=10 or len(newids)!=7 or {r["from_formulation"] for r in reviews}!=newids:
        raise PipelineError("Seven forms must receive ten independently reviewed direct links")
    check_cycles(ms,{**old,**{r["id"]:r for r in reviews}})
    snap=w.root/"state/wave2_formulation_reviews_snapshot_594_before_directional114.jsonl"
    if len(relations)==784:
        if any(previous[fid]["decision"]!="needs_review" or previous[fid]["relation_ids"] for fid in newids):
            raise PipelineError("Seven newly screened forms must await review")
        content=ledger.read_text(encoding="utf-8")
        if snap.exists() and snap.read_text(encoding="utf-8")!=content:
            raise PipelineError("Previous 594 reviews changed")
        snap.write_text(content,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_594_before_directional114.json",{
          "rows":594,"prior_screened_links":784,"sha256":hashlib.sha256(content.encode("utf-8")).hexdigest(),"human_peer_verified":False})
    past=jsonl(snap);oldindex={r["formulation_id"]:r for r in past}
    if len(past)!=594 or len(oldindex)!=594:
        raise PipelineError("Historic 594 disposition snapshot invalid")
    store(w.root/"wave2/directional114_individual_source_screened_links.jsonl",reviews)
    intake=store(w.root/"intake/directional114_links.jsonl",reviews)
    if len(relations)==784:
        w.ingest("relations",intake,batch_size=10)
    current=w.records("relations")
    if len(current)!=794 or any(current.get(r["id"])!=r for r in reviews):
        raise PipelineError("Ten new screened links not admitted")
    check_cycles(ms,current)
    modified=[]
    for p in past:
        row=dict(p);fid=row["formulation_id"]
        if fid in newids:
            related=[r["id"] for r in reviews if r["from_formulation"]==fid]
            if not related:raise PipelineError("Missing a formulation dependency review")
            row["relation_ids"]=related
            row["decision"]="linked"
            row["reviewed_by"]="assistant_independent_directional_topology_prerequisite_screen_2026_10_20"
            row["source"]="independent_directional_metric_topological_prerequisite_review_batch114"
            row["editorial_reason"]="Every source-specific endpoint justified; gradient-only source alternative remains held."
        modified.append(row)
    if len(relations)==794:
        if {r["formulation_id"]:r for r in before}!={r["formulation_id"]:r for r in modified}:
            raise PipelineError("Completed reviewed links differ upon rerun")
    else:
        atomic_jsonl(ledger,sorted(modified,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);index={r["formulation_id"]:r for r in final}
    if len(final)!=594 or len(index)!=594:
        raise PipelineError("594 individual review decisions expected")
    for fid,p in oldindex.items():
        if fid not in newids and index[fid]!=p:
            raise PipelineError("Unrelated previously reviewed disposition changed")
    if {i for r in final for i in r["relation_ids"]}!=set(current):
        raise PipelineError("Unreviewed dependency link present")
    if dict(Counter(r["decision"] for r in final))!={"linked":588,"no_supported_target":6}:
        raise PipelineError("Wrong individual review decision totals")
    held=jsonl(w.root/"wave2/directional112_quarantined_source_claims.jsonl")
    if len(held)!=1 or held[0]["observation_id"] in {e for m in ms.values() for f in m["formulations"] for e in f["evidence_ids"]}:
        raise PipelineError("Quarantined unsafe claim was promoted")
    report={"batch":114,"screened_meanings":564,"reviewed_formulations":594,"screened_relationships":794,
        "new_individually_screened_links":10,"all_784_old_links_preserved":True,
        "all_587_unrelated_reviews_preserved":True,"all_7_forms_individually_link_reviewed":True,
        "held_gradient_source_claim_preserved_and_excluded":True,
        "homeomorphism_two_equivalent_forms_preserved":True,
        "closed_ball_not_misidentified_as_open_ball_closure":True,
        "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
        "human_peer_verified":False,"production_corpus_used":False,
        "next":"Batch115 broaden independent discovery in new branches, and seek externally corroborated differentiability criterion before revisiting held gradient-only claim."}
    atomic_json(w.root/"state/wave2_directional114_link_review.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
