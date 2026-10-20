"""Batch111: individually screened linearity/image/rank/accumulation prerequisites.

Keeps all 774 earlier source-reviewed links, 580 unrelated formulation
decisions, and 7 newly reviewed forms. Never equates sequence accumulation
with set accumulation or finite rank with infinite-image dimension.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":449,"observations":898,"meanings":558}
PW="https://proofwiki.org/wiki/Definition%3A"
LIN=PW+"Linear_Transformation"
IMG=PW+"Image_of_Mapping"
RANK=PW+"Rank_of_Linear_Transformation"
ACC=PW+"Accumulation_Point"
MODULE=PW+"Module_over_Ring"
VEC="https://stacks.math.columbia.edu/tag/09FM"
MAP=PW+"Mapping"
TOP=PW+"Topological_Space"
CLOS=PW+"Closure_%28Topology%29"
F="form.wave2.cross110."
M="meaning.wave2.cross110."
EDGES=(
 ("01",F+"module-linear","meaning.wave2.foundation.left-module-nonunital","left R-modules",LIN,MODULE,
  "The general R-linear map is defined on a pair of left R-modules over the same ring. The independently screened left-module definition supplies additive groups and left scalar actions; the map imposes the two preservation equations additionally."),
 ("02",F+"field-vector-linear","meaning.b64bc15f46fe0245.vector-space-over-field","vector spaces",LIN,VEC,
  "The field-specific version of a linear transformation presupposes vector spaces V and W over one common commutative field K. Their scalar actions and addition are precisely the structures needed by the combined K-linearity identity."),
 ("03",F+"field-vector-linear",M+"module-linear","K-linear",LIN,LIN,
  "A K-vector space is a left module over K, and the combined K-linear condition implies the additive and scalar-compatibility conditions of the already separately sourced module-linear context. This is a specialization from field-vector linearity to module linearity, not a converse equivalence."),
 ("04",F+"image-of-mapping.1","meaning.wave2.foundation.mapping-element-assignment","total map",IMG,MAP,
  "The codomain-value existence description of image requires a total single-valued mapping f:S→T as a prerequisite. The independently screened mapping meaning supplies this structure; image need not coincide with the codomain absent surjectivity."),
 ("05",F+"image-of-mapping.2","meaning.wave2.foundation.mapping-element-assignment","total map",IMG,MAP,
  "The direct-image-of-whole-domain formulation f[S] presupposes a total mapping on S. The same independently reviewed map structure supports this equivalent image presentation, without treating image as an arbitrary subset of the codomain."),
 ("06",F+"finite-image-rank",M+"field-vector-linear","K-linear transformation",RANK,LIN,
  "The rank under review applies to a K-linear transformation between vector spaces. The independently sourced field-vector-linear map is therefore a direct prerequisite; this source's finite-dimensional-image qualification is preserved."),
 ("07",F+"finite-image-rank",M+"image-of-mapping","im(T)",RANK,IMG,
  "Finite rank is the dimension of the IMAGE im(T) of the linear map, not necessarily the dimension of its codomain. The separately sourced mapping-image meaning supplies im(T), and its finite dimensionality is an explicit extra assumption."),
 ("08",F+"sequence-accumulation","meaning.wave2.foundation.topological-space","topological space",ACC,TOP,
  "A sequence accumulation point is characterized by infinitely many INDEXED sequence terms lying in every open neighborhood of x. The independently screened topology supplies those neighborhoods; no injectivity, metrizability or convergence is required."),
 ("09",F+"set-accumulation",M.replace("cross110.","cross107.")+"topological-closure","cl_X",ACC,CLOS,
  "An accumulation point of A is a point x in the closure of A minus {x}, relative to the chosen ambient topological space. The independently screened topological closure supplies that exact operator and avoids assuming finite or distinct sequence indexes."),
 ("10",F+"set-accumulation","meaning.wave2.foundation.topological-space","topological space",ACC,TOP,
  "The underlying space X, subset A, open neighborhoods and closure of A\\{x} are all interpreted in an arbitrary topology. This independent topological-space dependency does not require metric or T1 assumptions.")
)

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    data="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=data:
        raise PipelineError("Historical source-specific Batch111 links changed")
    path.write_text(data,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in (*BASE,"relations")):
        raise PipelineError("Independent unsealed Wave2 required")
    if {k:len(w.records(k)) for k in BASE}!=BASE:
        raise PipelineError("Six already-source-screened Batch110 meanings expected")
    report=json.loads((w.root/"state/wave2_cross110_meaning_screen.json").read_text())
    if report.get("screened_meanings")!=558 or report.get("reviewed_formulations")!=587 or not report.get("accumulation_sequence_vs_set_separated"):
        raise PipelineError("Batch110 mathematically screened contexts not complete")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=587:
        raise PipelineError("Expected 587 source-specific screened formulations")
    oldrels=w.records("relations")
    if len(oldrels) not in (774,784):
        raise PipelineError("Unexpected prior screened links")
    historical={k:r for k,r in oldrels.items() if not k.startswith("rel.wave2.cross111.")}
    if len(historical)!=774:
        raise PipelineError("All 774 prior relationships must be retained")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    oldreviews=jsonl(ledger);oldindex={r["formulation_id"]:r for r in oldreviews}
    if (len(oldreviews)!=587 or len(oldindex)!=587 or
        any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in oldreviews)
        or {i for r in oldreviews for i in r["relation_ids"]}!=set(oldrels)):
        raise PipelineError("Current complete individual review history invalid")
    checked=[]
    for n,fid,target,phrase,sourceurl,targeturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Independent target/source endpoint missing "+n)
        meaning,f=forms[fid];evidence=f.get("evidence_ids",[])
        if (f["review_state"]!="screened" or len(evidence)!=1 or evidence[0] not in obs
            or obs[evidence[0]]["locator"]!=sourceurl or
            locator(ms[target],obs)!=targeturl or phrase not in f["text"] or
            len(reason)<150):
            raise PipelineError("Exact source phrase or target evidence not verified "+n)
        checked.append({
          "id":"rel.wave2.cross111."+n,"from_formulation":fid,
          "target_meaning":target,"relation_type":"definition_uses",
          "review_state":"screened","source_phrase":phrase,
          "source_locator":sourceurl,"target_locator":targeturl,
          "editorial_reason":reason,
          "reviewed_by":"assistant_independent_cross_domain_source_dependency_screen_2026_10_20",
          "human_verified":False})
    fresh={fid for fid in forms if fid.startswith(F)}
    if len(fresh)!=7 or len(checked)!=10 or {r["from_formulation"] for r in checked}!=fresh:
        raise PipelineError("Every one of 7 new forms requires a direct reviewed prerequisite")
    check_cycles(ms,{**historical,**{r["id"]:r for r in checked}})
    snap=w.root/"state/wave2_formulation_reviews_snapshot_587_before_cross111.jsonl"
    if len(oldrels)==774:
        if any(oldindex[fid]["decision"]!="needs_review" or oldindex[fid]["relation_ids"] for fid in fresh):
            raise PipelineError("New individual formulations cannot already have screened edges")
        raw=ledger.read_text(encoding="utf-8")
        if snap.exists() and snap.read_text(encoding="utf-8")!=raw:
            raise PipelineError("Historical 587 decision ledger mutated")
        snap.write_text(raw,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_587_before_cross111.json",{
          "rows":587,"historic_screened_links":774,
          "sha256":hashlib.sha256(raw.encode("utf-8")).hexdigest(),
          "human_peer_verified":False})
    before=jsonl(snap);idx={r["formulation_id"]:r for r in before}
    if len(before)!=587 or len(idx)!=587:
        raise PipelineError("Prior individual review snapshot missing")
    store(w.root/"wave2/cross111_individually_source_screened_links.jsonl",checked)
    intake=store(w.root/"intake/cross111_links.jsonl",checked)
    if len(oldrels)==774:
        w.ingest("relations",intake,batch_size=10)
    current=w.records("relations")
    if len(current)!=784 or any(current.get(r["id"])!=r for r in checked):
        raise PipelineError("Expected 10 exactly sourced relations")
    check_cycles(ms,current)
    updated=[]
    for p in before:
        row=dict(p);fid=row["formulation_id"]
        if fid in fresh:
            relevant=[r["id"] for r in checked if r["from_formulation"]==fid]
            if not relevant: raise PipelineError("Missing specific new formulation prerequisite "+fid)
            row["relation_ids"]=relevant
            row["decision"]="linked"
            row["reviewed_by"]="assistant_independent_cross_domain_source_dependency_screen_2026_10_20"
            row["source"]="independent_cross_domain_dependency_review_batch111"
            row["editorial_reason"]="Source-grounded independent prerequisite checked, all older reviewed dependencies retained."
        updated.append(row)
    if len(oldrels)==784:
        if {r["formulation_id"]:r for r in oldreviews}!={r["formulation_id"]:r for r in updated}:
            raise PipelineError("Completed individual review differs on repeat")
    else:
        atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);index={r["formulation_id"]:r for r in final}
    if len(final)!=587 or len(index)!=587:
        raise PipelineError("587 individually dispositioned formulations required")
    for fid,p in idx.items():
        if fid not in fresh and index[fid]!=p:
            raise PipelineError("Old mathematical review/disposition overwritten")
    if {i for r in final for i in r["relation_ids"]}!=set(current):
        raise PipelineError("Screened links not exhaustively mapped to formulation decisions")
    if dict(Counter(r["decision"] for r in final))!={"linked":581,"no_supported_target":6}:
        raise PipelineError("Unexpected final review dispositions")
    result={
      "batch":111,"screened_meanings":558,"reviewed_formulations":587,
      "screened_relationships":784,"new_source_specific_links":10,
      "all_774_historic_screened_links_preserved":True,
      "all_580_unrelated_formulation_reviews_preserved":True,
      "all_seven_new_forms_individually_link_reviewed":True,
      "finite_image_rank_constraint_preserved":True,
      "mapping_image_two_equivalent_forms_grouped":True,
      "topological_set_vs_sequence_accumulation_separate":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch112: bounded independent source discovery outside recently researched branches; avoid endless prerequisite recursion or premature Wave2 stage sealing."}
    atomic_json(w.root/"state/wave2_cross111_link_review.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
