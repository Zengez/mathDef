"""Batch133: four mathematical meanings and eight source-specific formulations.

Bell, Stirling, convex hull and simple-graph vertex degree are screened with
equivalent representations kept under a single contextual meaning per topic.
"""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/combinatorics_convex_graph_source_batch132_2026-10-20.jsonl"
BASE={"sources":14,"terms":477,"observations":946,"meanings":587,"relations":855}
AFTER=dict(BASE,meanings=591)
SPECS=(
 ("bell-number","bell-number","Bell number B_n counts all partitions of n-element sets including n=0"),
 ("stirling-second-kind","stirling-second-kind","Second-kind Stirling numbers by recurrence and falling factorial polynomial coefficients"),
 ("convex-hull","convex-hull-real","Convex hull in a real vector space, finite combinations and least convex superset"),
 ("vertex-degree","vertex-degree-simple","Degree of vertex in loopless simple undirected graph, incidence and neighbor counts")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Historical individual mathematical screen changed")
    path.write_text(content,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Independent unsealed Wave2 required")
    if {k:len(w.records(k)) for k in BASE} not in (BASE,AFTER):
        raise PipelineError("Source-only Batch132 evidence absent")
    src=json.loads((w.root/"state/wave2_cross132_source_intake.json").read_text())
    if src.get("new_source_headings")!=4 or src.get("new_observations")!=8:
        raise PipelineError("Batch132 approved exact source intake missing")
    rows={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if len(rows)!=4:raise PipelineError("Four source-screened research topics required")
    termdb=w.records("terms");obsdb=w.records("observations")
    meanings=[];form_reviews=[]
    for key,suffix,scope in SPECS:
        r=rows[key];tid="term.wave2.cross132."+key
        if termdb.get(tid,{}).get("locator")!=r["source"] or r["production_corpus_consulted"]:
            raise PipelineError("Source-specific independent lineage missing "+key)
        fs=r["contexts"][0]["forms"];reason=r["review"]
        expected={"bell-number":1,"stirling-second-kind":2,"convex-hull":3,"vertex-degree":2}[key]
        if len(fs)!=expected or len(reason)<390:raise PipelineError("Not all equivalent source forms reviewed")
        if key=="bell-number":
            if "B_0=1" not in fs[0]["text"] or "nonempty pairwise disjoint blocks" not in fs[0]["text"]:
                raise PipelineError("Empty-set partition counting convention missing")
        if key=="stirling-second-kind":
            if "δ" not in fs[0]["text"] or "falling" not in fs[1]["label"]:
                raise PipelineError("Recursive base-case and polynomial expansion variants incomplete")
        if key=="convex-hull":
            if "conv(∅)=∅" not in fs[0]["text"] or "convex and U⊆C" not in fs[1]["text"] or "least" not in fs[2]["text"]:
                raise PipelineError("Three equivalent convex hull constructions not screened")
        if key=="vertex-degree":
            if "simple undirected graph" not in fs[0]["text"] or "simple undirected graph" not in fs[1]["text"] or "multigraphs" not in reason:
                raise PipelineError("Neighbor-incidence equivalence incorrectly extended to multigraphs")
        mid="meaning.wave2.cross133."+suffix
        fs_rows=[]
        for i,f in enumerate(fs,1):
            oid=f"obs.wave2.cross132.{key}.{i:02d}"
            ob=obsdb.get(oid)
            if not ob or ob["term_id"]!=tid or ob["locator"]!=r["source"] or ob["text"]!=f["text"]:
                raise PipelineError("Exact mathematical individual source observation missing "+oid)
            fid="form.wave2.cross133."+suffix+("."+str(i) if len(fs)>1 else "")
            fs_rows.append({"id":fid,"text":f["text"],"evidence_ids":[oid],
                "review_state":"screened","human_verified":False,
                "mathematical_review_reason":reason,
                "source_screened_by":"assistant_independent_bell_stirling_convex_degree_math_review_2026_10_20"})
            form_reviews.append({"review_id":"review.wave2.cross133."+suffix+("."+str(i) if len(fs)>1 else ""),
                "meaning_id":mid,"formulation_id":fid,"source_observation_id":oid,
                "source_locator":r["source"],"mathematical_reason":reason,
                "decision":"mathematically_screened_pending_individual_prerequisite_review",
                "human_verified":False,"production_corpus_used":False})
        meanings.append({"id":mid,"term_group_id":"wave2.cross133."+key,
           "display_term":r["term"],"context":scope,"term_ids":[tid],"formulations":fs_rows,
           "editorial_status":"source_scoped_individually_mathematically_screened",
           "editorial_screening_reason":reason,"human_verified":False})
    if len(meanings)!=4 or len(form_reviews)!=8:
        raise PipelineError("Expected 4 source-scoped meanings and 8 separate formulations")
    store(w.root/"wave2/cross133_individual_mathematical_reviews.jsonl",form_reviews)
    intake=store(w.root/"intake/cross133_meanings.jsonl",meanings)
    old_ms=w.records("meanings");ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    current=jsonl(ledger)
    if len(current) not in (624,632) or len({r["formulation_id"] for r in current})!=len(current):
        raise PipelineError("624 historic reviewed formulations required")
    if {i for r in current for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("All 855 historic relations must have individual reviews")
    backup=w.root/"state/wave2_formulation_reviews_snapshot_624_before_cross133.jsonl"
    if len(old_ms)==587:
        if len(current)!=624 or any(r["meaning_catalog_digest"]!=digest(list(old_ms.values())) for r in current):
            raise PipelineError("Older meaning digest does not match reviewed catalog")
        raw=ledger.read_text(encoding="utf-8")
        if backup.exists() and backup.read_text(encoding="utf-8")!=raw:
            raise PipelineError("Historical review snapshot altered")
        backup.write_text(raw,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_624_before_cross133.json",
            {"rows":624,"prior_relations":855,"sha256":hashlib.sha256(raw.encode()).hexdigest(),"human_peer_verified":False})
        w.ingest("meanings",intake,batch_size=4)
    ms=w.records("meanings")
    if len(ms)!=591 or any(ms.get(m["id"])!=m for m in meanings):
        raise PipelineError("Four mathematically screened contextual meanings missing")
    historic=jsonl(backup)
    if len(historic)!=624 or len({r["formulation_id"] for r in historic})!=624:
        raise PipelineError("Historical 624 form review snapshot absent")
    d=digest(list(ms.values()))
    updated=[dict(r,meaning_catalog_digest=d) for r in historic]
    for r in form_reviews:
        updated.append({"formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
            "meaning_catalog_digest":d,"decision":"needs_review","relation_ids":[],
            "original_wave1_disposition":None,"source":"independent_bell_stirling_convex_degree_math_screen_batch133",
            "editorial_reason":"Individual mathematical source form screened; direct prerequisite screening pending.",
            "reviewed_by":None,"human_verified":False})
    if len(current)==632:
        if {r["formulation_id"]:r for r in current}!={r["formulation_id"]:r for r in updated}:
            raise PipelineError("Already completed mathematical screening changed on rerun")
    else:atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);idx={r["formulation_id"]:r for r in final}
    if len(final)!=632 or len(idx)!=632:
        raise PipelineError("632 mathematically screened formulation dispositions required")
    for p in historic:
        r=idx[p["formulation_id"]]
        if any(r.get(k)!=v for k,v in p.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Unrelated mathematical formulation review altered")
    if dict(Counter(r["decision"] for r in final))!={"linked":618,"no_supported_target":6,"needs_review":8}:
        raise PipelineError("Historic decisions or new pending screens incorrect")
    if {i for r in final for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Historically reviewed links lost")
    check_cycles(ms,w.records("relations"))
    st=w.state("meanings");st.update(total=591,record_digest=d,screened_new_formulations=201,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",st)
    report={"batch":133,"screened_meanings":591,"reviewed_formulations":632,
        "new_contextual_meanings":4,"new_individual_formulations":8,
        "stirling_equivalent_forms_one_meaning":True,"convex_hull_three_equivalent_forms_one_meaning":True,
        "degree_equivalent_only_for_simple_graphs":True,
        "B0_one_empty_partition":True,"previous_624_reviews_and_855_links_preserved":True,
        "eight_formulations_pending_link_review":True,
        "three_historical_source_holds_unchanged":True,"all_stages_unsealed":True,
        "human_peer_verified":False,"production_corpus_used":False,
        "next":"Batch134: source-specific direct link screens and missing convex/falling-factorial prerequisite registry."}
    atomic_json(w.root/"state/wave2_cross133_meaning_screen.json",report);return report
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
