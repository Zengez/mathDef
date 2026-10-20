"""Batch 104 mathematical review: distinguish Lipschitz, tree and independence contexts.

Six contextual meanings, seven source-specific formulations; the two
tree acyclicity characterizations are source-equivalent in one meaning.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/cross_field_source_variants_batch103_2026-10-20.jsonl"
BASE={"sources":14,"terms":441,"observations":884,"meanings":541,"relations":754}
AFTER=dict(BASE,meanings=547)
SPECS=(
 ("lipschitz-continuity",0,"lipschitz-global","Globally Lipschitz mapping of metric spaces"),
 ("lipschitz-continuity",1,"lipschitz-at-point-anchored","Lipschitz bound anchored at one point, not neighborhood-local Lipschitz"),
 ("tree-graph",0,"tree-unrooted","Unrooted simple connected graph with no circuits or cycles"),
 ("independent-sigma-algebras",0,"independent-sigma-pair","Independence of two sub-sigma-algebras"),
 ("independent-sigma-algebras",1,"independent-sigma-countable","Mutual independence of a countably indexed family of sub-sigma-algebras"),
 ("independent-random-variables",0,"independent-rv-countable","Mutual independence of a sequence of measurable-space-valued random variables")
)

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    data="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=data:
        raise PipelineError("Historical cross-field mathematical reviews changed")
    path.write_text(data,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Unsealed independent second wave required")
    now={k:len(w.records(k)) for k in BASE}
    if now not in (BASE,AFTER):
        raise PipelineError("Unverified prior independent source counts "+str(now))
    intake_report=json.loads((w.root/"state/wave2_cross103_source_intake.json").read_text(encoding="utf-8"))
    if intake_report.get("new_source_terms")!=4 or intake_report.get("new_source_observations")!=7 or intake_report.get("new_screened_meanings")!=0:
        raise PipelineError("Batch103 reviewed source-only intake not verified")
    research={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if len(research)!=4:
        raise PipelineError("All four specific source research topics required")
    termdb=w.records("terms");obsdb=w.records("observations")
    additions=[];individual=[]
    for key,context_index,suffix,label in SPECS:
        row=research[key]
        tid="term.wave2.cross103."+key
        if tid not in termdb or row["source"]!=termdb[tid]["locator"]:
            raise PipelineError("Research title/locator mismatch "+key)
        context=row["contexts"][context_index]
        reason=row["mathematical_review"]
        if len(reason)<280 or row["production_corpus_consulted"] or row["stage_ingested"]:
            raise PipelineError("Invalid mathematical review provenance")
        if key=="lipschitz-continuity":
            if context_index==0 and "x,y" not in context["formulations"][0]["text"]:
                raise PipelineError("Global two-point condition missing")
            if context_index==1 and "f(a)" not in context["formulations"][0]["text"]:
                raise PipelineError("Anchored Lipschitz condition missing")
            reason+=(" Global implies all anchored conditions; an anchored condition at a selected point "
                     "does not imply neighborhood two-point Lipschitz continuity and must not be equated with it.")
        elif key=="tree-graph":
            if len(context["formulations"])!=2 or "no cycles" not in context["formulations"][1]["text"]:
                raise PipelineError("Tree's equivalent circuit/cycle formulations missing")
            reason+=(" No finiteness, root, or selected vertex is required by either formulation.")
        elif key=="independent-sigma-algebras":
            if context_index==0 and "A∩B" not in context["formulations"][0]["text"]:
                raise PipelineError("Binary probability factorization missing")
            if context_index==1 and "distinct indices" not in context["formulations"][0]["text"]:
                raise PipelineError("Mutual finite-index factorization missing")
            reason+=(" Binary and arbitrary countable mutual independence are not represented as equivalent fixed-family properties.")
        elif key=="independent-random-variables":
            if "σ(X_n)" not in context["formulations"][0]["text"] or "Σ_S" not in context["formulations"][0]["text"]:
                raise PipelineError("Correct measurable target and generated sigma-algebra condition missing")
            reason+=(" Independence is mutual independence of generated sub-sigma-algebras, not pairwise independence.")
        mid="meaning.wave2.cross104."+suffix
        group="wave2.cross104."+key
        formset=[]
        for i,source_form in enumerate(context["formulations"],start=1):
            global_index=i if key=="tree-graph" else context_index+1
            oid=f"obs.wave2.cross103.{key}.{global_index:02d}"
            o=obsdb.get(oid)
            if not o or o["term_id"]!=tid or o["source_id"]!="src.proofwiki" or o["locator"]!=row["source"] or o["text"]!=source_form["text"]:
                raise PipelineError("Individual source formulation missing "+suffix+"/"+str(i))
            fid="form.wave2.cross104."+suffix+("." +str(i) if len(context["formulations"])>1 else "")
            formset.append({
                "id":fid,"text":source_form["text"],"evidence_ids":[oid],
                "review_state":"screened","human_verified":False,
                "mathematical_review_reason":reason,
                "source_screened_by":"assistant_independent_cross_field_mathematical_review_2026_10_20"})
            individual.append({
                "review_id":"review.wave2.cross104."+suffix+("." +str(i) if len(context["formulations"])>1 else ""),
                "meaning_id":mid,"formulation_id":fid,"source_observation_id":oid,
                "source_locator":row["source"],"mathematical_reason":reason,
                "decision":"source_screened_pending_individual_dependency_review",
                "human_verified":False,"production_corpus_used":False})
        additions.append({
           "id":mid,"term_group_id":group,"display_term":row["term"],
           "context":label,"term_ids":[tid],"formulations":formset,
           "editorial_status":"source_scoped_individually_mathematically_screened",
           "editorial_screening_reason":reason,"human_verified":False})
    if len(additions)!=6 or len(individual)!=7 or sum(len(m["formulations"]) for m in additions)!=7:
        raise PipelineError("Six meanings and seven formulations expected")
    store(w.root/"wave2/cross104_individual_mathematical_reviews.jsonl",individual)
    inputfile=store(w.root/"intake/cross104_meanings.jsonl",additions)
    oldms=w.records("meanings")
    path=w.root/"state/wave2_formulation_reviews.jsonl"
    prior=jsonl(path)
    if len(prior) not in (566,573) or len({x["formulation_id"] for x in prior})!=len(prior):
        raise PipelineError("566 historic individual reviews required")
    if {i for r in prior for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Prior 754 reviewed links missing")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_566_before_cross104.jsonl"
    if len(oldms)==541:
        if len(prior)!=566 or any(x["meaning_catalog_digest"]!=digest(list(oldms.values())) for x in prior):
            raise PipelineError("Historical meaning digest mismatch")
        content=path.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=content:
            raise PipelineError("Historical 566 review snapshot changed")
        archive.write_text(content,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_566_before_cross104.json",{
          "rows":566,"historic_links":754,"sha256":hashlib.sha256(content.encode("utf-8")).hexdigest(),
          "human_peer_verified":False})
        w.ingest("meanings",inputfile,batch_size=6)
    ms=w.records("meanings")
    if len(ms)!=547 or any(ms.get(x["id"])!=x for x in additions):
        raise PipelineError("Approved mathematical context admission differs")
    old=jsonl(archive)
    if len(old)!=566 or len({x["formulation_id"] for x in old})!=566:
        raise PipelineError("Missing complete previous formulation history")
    d=digest(list(ms.values()))
    updated=[dict(x,meaning_catalog_digest=d) for x in old]
    for r in individual:
        updated.append({
            "formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
            "meaning_catalog_digest":d,"decision":"needs_review",
            "relation_ids":[],"original_wave1_disposition":None,
            "source":"independent_cross_field_source_specific_meaning_screen_batch104",
            "editorial_reason":"Mathematical concept and source context checked; individual prerequisite decisions pending.",
            "reviewed_by":None,"human_verified":False})
    if len(prior)==573:
        if {x["formulation_id"]:x for x in prior}!={x["formulation_id"]:x for x in updated}:
            raise PipelineError("Existing meaning review differs on rerun")
    else:
        atomic_jsonl(path,sorted(updated,key=lambda x:x["formulation_id"]))
    current=jsonl(path);index={r["formulation_id"]:r for r in current}
    if len(current)!=len(index)!=573:
        raise PipelineError("573 individual reviews required")
    for oldr in old:
        nowr=index[oldr["formulation_id"]]
        if any(nowr.get(k)!=v for k,v in oldr.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Historical mathematical review disposition altered")
    if {i for r in current for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Previously approved link references changed")
    check_cycles(ms,w.records("relations"))
    if dict(Counter(x["decision"] for x in current))!={"linked":560,"no_supported_target":6,"needs_review":7}:
        raise PipelineError("Unexpected prior/new review disposition")
    state=w.state("meanings")
    state.update(total=547,record_digest=d,screened_new_formulations=142,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
      "batch":104,"screened_meanings":547,"reviewed_formulations":573,
      "new_contextual_meanings":6,"new_individual_formulations":7,
      "old_566_formulation_decisions_preserved":True,
      "old_754_dependency_links_preserved":True,
      "tree_acyclicity_formulations_equivalent":True,
      "point_anchored_vs_global_lipschitz_distinct":True,
      "pairwise_vs_mutual_independence_distinct":True,
      "pending_individual_link_reviews":7,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch105 independently review each of seven formulations against existing metric, simple graph, probability, sigma algebra and general random-variable definitions."
    }
    atomic_json(w.root/"state/wave2_cross104_meaning_screen.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__": main()
