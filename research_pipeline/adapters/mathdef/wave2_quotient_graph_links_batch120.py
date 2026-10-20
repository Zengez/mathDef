"""Batch120 direct independent prerequisites with all past 803 edges preserved.

The subgroup prerequisite and power-series convergence concept remain
documented as source-identified target coverage gaps, not fabricated links.
"""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":461,"observations":919,"meanings":572}
PW="https://proofwiki.org/wiki/Definition%3A"
NORMAL=PW+"Normal_Subgroup";QUOT=PW+"Quotient_Group"
GRAPH=PW+"Graph_Isomorphism";OGF=PW+"Generating_Function"
GROUP=PW+"Group";SIMPLE=PW+"Simple_Graph";MAP=PW+"Mapping";REAL=PW+"Real_Number"
F="form.wave2.quot119."
M="meaning.wave2.quot119."
EDGES=(
 ("01",F+"normal-subgroup.1","meaning.wave2.foundation.group","group G",NORMAL,GROUP,
  "The coset equality gN=Ng is a condition on a specified subgroup N of a group G; group multiplication, identity and inverses are supplied by the separately sourced group meaning. No assumption of commutativity or finiteness is added."),
 ("02",F+"normal-subgroup.2","meaning.wave2.foundation.group","group G",NORMAL,GROUP,
  "The conjugation equation gNg⁻¹=N presupposes the binary operation and inversion of an ambient group G. The independently source-screened group target supplies those operations; N being a subgroup remains an additional explicit hypothesis."),
 ("03",F+"normal-subgroup.3","meaning.wave2.foundation.group","group G",NORMAL,GROUP,
  "The all-g conjugation inclusion gNg⁻¹⊆N uses group inverses and multiplication. Applying this same condition to g inverse yields the equality criterion, so this is equivalent normality only when it holds for every g in the group."),
 ("04",F+"quotient-group",M+"normal-subgroup","normal subgroup",QUOT,NORMAL,
  "The quotient group construction explicitly assumes N is a normal subgroup of G; this makes (aN)(bN)=(ab)N independent of representatives. The separately source-screened normal-subgroup definition is its direct prerequisite, not arbitrary equivalence classes."),
 ("05",F+"simple-graph-isomorphism","meaning.wave2.graph42.simple-undirected","simple undirected graphs",GRAPH,SIMPLE,
  "Both source graphs are simple undirected graphs with edges represented as two-element vertex subsets. The independently screened graph target fixes adjacency without loops or parallel edges; the isomorphism requires preservation and REFLECTION of adjacency."),
 ("06",F+"simple-graph-isomorphism","meaning.wave2.foundation.mapping-element-assignment","bijection",GRAPH,MAP,
  "An isomorphism between the two graph vertex sets is first a bijective total single-valued map. The independent mapping meaning supplies the function prerequisite, while the approved mathematical form requires both directions of edge preservation, not one direction alone."),
 ("07",F+"ordinary-real-ogf","meaning.wave2.real45.complete-ordered-real-field","ℝ",OGF,REAL,
  "The source-specific analytic ordinary generating function uses a real sequence of coefficients and sums on a subset of the real scalar field where the series converges. The independently sourced real number system is a direct prerequisite; formal-series equivalence is not asserted."),
 ("08",F+"ordinary-real-ogf","meaning.wave2.foundation.mapping-element-assignment","G_A:D→ℝ",OGF,MAP,
  "The convergent ordinary generating function is a real-valued map with domain D defined by convergence of its coefficient power series. The separately source-screened mapping concept supplies typed assignment, not a formal power series or exponential generating function.")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(row)+"\n" for row in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Previously verified source specific link event differs")
    path.write_text(content,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BASE,"relations")):
        raise PipelineError("Requires unsealed independent Wave2")
    if {s:len(w.records(s)) for s in BASE}!=BASE:
        raise PipelineError("Expected reviewed Batch119 mathematics baseline missing")
    report=json.loads((w.root/"state/wave2_quot119_meaning_screen.json").read_text())
    if report.get("screened_meanings")!=572 or report.get("reviewed_formulations")!=606 or not report.get("held_forward_only_graph_claim_unpromoted"):
        raise PipelineError("Batch119 mathematical review evidence not valid")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=606:raise PipelineError("Expected 606 reviewed formulation endpoints")
    before_links=w.records("relations")
    if len(before_links) not in (803,811):
        raise PipelineError("Unexpected historical mathematical prerequisite count")
    historic={i:r for i,r in before_links.items() if not i.startswith("rel.wave2.quot120.")}
    if len(historic)!=803:raise PipelineError("All 803 old links must be preserved")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    before=jsonl(ledger);index={r["formulation_id"]:r for r in before}
    if (len(before)!=606 or len(index)!=606 or
        any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in before) or
        {i for r in before for i in r["relation_ids"]}!=set(before_links)):
        raise PipelineError("Prior 606 individual review dispositions invalid")
    additions=[]
    for n,fid,target,phrase,sourceurl,targeturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Missing mathematical source/target for screened link "+n)
        _,f=forms[fid];evidence=f.get("evidence_ids",[])
        if (f["review_state"]!="screened" or len(evidence)!=1 or evidence[0] not in obs
          or obs[evidence[0]]["locator"]!=sourceurl or locator(ms[target],obs)!=targeturl
          or phrase not in f["text"] or len(reason)<150):
            raise PipelineError("Source/target scope insufficient to justify definition link "+n)
        additions.append({"id":"rel.wave2.quot120."+n,"from_formulation":fid,
          "target_meaning":target,"relation_type":"definition_uses",
          "review_state":"screened","source_phrase":phrase,
          "source_locator":sourceurl,"target_locator":targeturl,
          "editorial_reason":reason,"reviewed_by":"assistant_independent_group_graph_ogf_prerequisite_review_2026_10_20",
          "human_verified":False})
    fresh={fid for fid in forms if fid.startswith(F)}
    if len(fresh)!=6 or len(additions)!=8 or {r["from_formulation"] for r in additions}!=fresh:
        raise PipelineError("Six new formulations must have their exact eight dependencies checked")
    check_cycles(ms,{**historic,**{r["id"]:r for r in additions}})
    archive=w.root/"state/wave2_formulation_reviews_snapshot_606_before_quot120.jsonl"
    if len(before_links)==803:
        if any(index[fid]["decision"]!="needs_review" or index[fid]["relation_ids"] for fid in fresh):
            raise PipelineError("New formulations not pending link review")
        content=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=content:
            raise PipelineError("Historical 606 review snapshot altered")
        archive.write_text(content,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_606_before_quot120.json",
          {"rows":606,"prior_links":803,"sha256":hashlib.sha256(content.encode("utf-8")).hexdigest(),
           "human_peer_verified":False})
    saved=jsonl(archive);oldidx={r["formulation_id"]:r for r in saved}
    if len(saved)!=606 or len(oldidx)!=606:raise PipelineError("Complete historical review snapshots absent")
    store(w.root/"wave2/quot120_individually_source_screened_links.jsonl",additions)
    intake=store(w.root/"intake/quot120_links.jsonl",additions)
    if len(before_links)==803:w.ingest("relations",intake,batch_size=8)
    rel=w.records("relations")
    if len(rel)!=811 or any(rel.get(r["id"])!=r for r in additions):
        raise PipelineError("Eight new screened links missing")
    check_cycles(ms,rel)
    updated=[]
    for old in saved:
        r=dict(old);fid=r["formulation_id"]
        if fid in fresh:
            ids=[a["id"] for a in additions if a["from_formulation"]==fid]
            if not ids:raise PipelineError("Missing individualized new formulation link decision")
            r["relation_ids"]=ids;r["decision"]="linked"
            r["reviewed_by"]="assistant_independent_group_graph_ogf_prerequisite_review_2026_10_20"
            r["source"]="independent_group_graph_ogf_dependency_review_batch120"
            r["editorial_reason"]="Exact mathematical source phrase and target checked; missing subgroup and convergent-series definition targets documented as research gaps."
        updated.append(r)
    if len(before_links)==811:
        if {r["formulation_id"]:r for r in before}!={r["formulation_id"]:r for r in updated}:
            raise PipelineError("Repeated link review would change prior disposition")
    else:atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);by={r["formulation_id"]:r for r in final}
    if len(final)!=606 or len(by)!=606:raise PipelineError("All 606 individual mathematical review decisions required")
    for fid,r in oldidx.items():
        if fid not in fresh and by[fid]!=r:
            raise PipelineError("Older unrelated mathematical review mutated")
    if {i for r in final for i in r["relation_ids"]}!=set(rel):
        raise PipelineError("Not all mathematical links individually reviewed")
    if dict(Counter(r["decision"] for r in final))!={"linked":600,"no_supported_target":6}:
        raise PipelineError("Expected 600 linked formulations and 6 justifiably unlinked")
    held=jsonl(w.root/"wave2/quot118_quarantined_source_claims.jsonl")
    if len(held)!=1 or held[0]["observation_id"] in {e for m in ms.values() for fm in m["formulations"] for e in fm["evidence_ids"]}:
        raise PipelineError("Unsafe graph isomorphism source clause promoted")
    gaps=[
      {"source_formulations":[F+"normal-subgroup.1",F+"normal-subgroup.2",F+"normal-subgroup.3"],
       "missing_target":"standalone independently screened subgroup of group meaning",
       "action":"independent direct source discovery, not fabricated dependency"},
      {"source_formulations":[F+"ordinary-real-ogf"],"missing_target":"convergence of real power series",
       "action":"independent direct source discovery before linking"},
      {"source_formulations":[F+"quotient-group"],"missing_target":"left group coset / coset product",
       "action":"independent direct source review; no assumption that existing quotient set implies group structure"}]
    store(w.root/"wave2/quot120_missing_prerequisite_target_candidates.jsonl",gaps)
    result={"batch":120,"screened_meanings":572,"reviewed_formulations":606,
      "screened_relationships":811,"new_individual_links":8,
      "all_prior_803_links_preserved":True,"all_600_unrelated_formulation_dispositions_preserved":True,
      "all_six_new_formulations_separately_link_reviewed":True,
      "source_held_graph_forward_only_unpromoted":True,
      "normality_required_for_quotient_group":True,
      "convergent_ogf_not_conflated_with_formal_power_series":True,
      "three_missing_dependency_targets_logged_not_invented":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch121 new independent source research in unrelated fields, with targeted recovery of outstanding subgroup/coset/power-series prerequisites only if sources directly warrant."}
    atomic_json(w.root/"state/wave2_quot120_link_review.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
