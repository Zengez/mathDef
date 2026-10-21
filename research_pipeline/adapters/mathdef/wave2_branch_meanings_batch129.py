"""Batch129: four distinct, individually sourced mathematical meanings; six forms.

Product topology's subbasis and finite-support basis are equivalent; operator
eigenvalue's nonzero shifted-kernel and equation conditions are equivalent.
No production-original mathDef mathematical definitions are consulted.
"""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/product_eigen_graph_egf_source_batch128_2026-10-20.jsonl"
BASE={"sources":14,"terms":473,"observations":938,"meanings":583,"relations":840}
AFTER=dict(BASE,meanings=587)
SPECS=(
 ("product-topology","indexed-product-topology","Indexed product topology with finite-support restrictions"),
 ("eigenvalue-linear-operator","operator-eigenvalue","Eigenvalue of a K-linear endomorphism without finite-dimensionality assumption"),
 ("connected-simple-graph","nonempty-connected-graph","Connected nonempty simple undirected graph by walks"),
 ("exponential-generating-function","real-convergent-egf","Analytic exponential generating function of a real sequence")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    content="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=content:
        raise PipelineError("Individually reviewed source or mathematical evidence changed")
    path.write_text(content,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Requires unsealed independent Wave2")
    if {k:len(w.records(k)) for k in BASE} not in (BASE,AFTER):
        raise PipelineError("Source-only Batch128 not committed")
    src_report=json.loads((w.root/"state/wave2_branch128_source_intake.json").read_text())
    if src_report.get("new_terms")!=4 or src_report.get("new_source_observations")!=6:
        raise PipelineError("Batch128 independent source registry unverified")
    research={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    terms=w.records("terms");obsdb=w.records("observations")
    additions=[];individual=[]
    for key,suffix,scope in SPECS:
        r=research[key];tid="term.wave2.branch128."+key
        if terms.get(tid,{}).get("locator")!=r["source"] or r["production_corpus_consulted"]:
            raise PipelineError("Missing exact source-term lineage "+key)
        ctx=r["contexts"][0];fs=ctx["forms"];reason=r["review"]
        if len(fs)!=(2 if key in ("product-topology","eigenvalue-linear-operator") else 1) or len(reason)<370:
            raise PipelineError("Wrong independent equivalent mathematical source variant counts")
        if key=="product-topology":
            if "subbasis" not in fs[0]["text"] or "all but finitely many" not in fs[1]["text"]:
                raise PipelineError("Subbasis/finite-support product topology distinction missing")
            reason+=" The cylinder subbasis generates exactly the topology with finite-support product basis; do not confuse with box topology."
        elif key=="eigenvalue-linear-operator":
            if "ker(A−λI_V)≠{0_V}" not in fs[0]["text"] or "nonzero v" not in fs[1]["text"]:
                raise PipelineError("Nontrivial-kernel and nonzero-vector equivalent conditions not explicitly retained")
            reason+=" Eigenvalues are scalars; both definitions require nontrivial eigenvectors indirectly, even if dim V is infinite."
        elif key=="connected-simple-graph":
            if "nonempty" not in fs[0]["text"] or "finite walk" not in fs[0]["text"]:
                raise PipelineError("Connected graph's empty-graph scope or finite walk absent")
        elif key=="exponential-generating-function":
            if "n!" not in fs[0]["text"] or "converges" not in fs[0]["text"]:
                raise PipelineError("EGF factorial denominator and analytic convergence required")
        mid="meaning.wave2.branch129."+suffix
        forms=[]
        for j,f in enumerate(fs,1):
            oid=f"obs.wave2.branch128.{key}.{j:02d}"
            o=obsdb.get(oid)
            if not o or o["term_id"]!=tid or o["locator"]!=r["source"] or o["text"]!=f["text"]:
                raise PipelineError("Exact individual source observation absent "+oid)
            fid="form.wave2.branch129."+suffix+("."+str(j) if len(fs)>1 else "")
            forms.append({"id":fid,"text":f["text"],"evidence_ids":[oid],
              "review_state":"screened","human_verified":False,
              "mathematical_review_reason":reason,
              "source_screened_by":"assistant_independent_product_eigen_graph_egf_mathematical_screen_2026_10_20"})
            individual.append({"review_id":"review.wave2.branch129."+suffix+("."+str(j) if len(fs)>1 else ""),
              "meaning_id":mid,"formulation_id":fid,"source_observation_id":oid,
              "source_locator":r["source"],"mathematical_reason":reason,
              "decision":"mathematically_screened_pending_individual_link_review",
              "human_verified":False,"production_corpus_used":False})
        additions.append({"id":mid,"term_group_id":"wave2.branch129."+key,
          "display_term":r["term"],"context":scope,"term_ids":[tid],"formulations":forms,
          "editorial_status":"source_scoped_individually_mathematically_screened",
          "editorial_screening_reason":reason,"human_verified":False})
    if len(additions)!=4 or len(individual)!=6:
        raise PipelineError("Four screened meanings and six source formulations expected")
    store(w.root/"wave2/branch129_individual_mathematical_reviews.jsonl",individual)
    intake=store(w.root/"intake/branch129_meanings.jsonl",additions)
    before_ms=w.records("meanings")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    previous=jsonl(ledger)
    if len(previous) not in (618,624) or len({r["formulation_id"] for r in previous})!=len(previous):
        raise PipelineError("618 prior reviewed mathematical formulation records required")
    if {i for r in previous for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("All historic 840 relations must be individually reviewed")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_618_before_branch129.jsonl"
    if len(before_ms)==583:
        if len(previous)!=618 or any(r["meaning_catalog_digest"]!=digest(list(before_ms.values())) for r in previous):
            raise PipelineError("Prior independent meaning digest invalid")
        content=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=content:
            raise PipelineError("Old 618 review disposition snapshot changed")
        archive.write_text(content,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_618_before_branch129.json",
            {"rows":618,"prior_relations":840,
             "sha256":hashlib.sha256(content.encode("utf-8")).hexdigest(),"human_peer_verified":False})
        w.ingest("meanings",intake,batch_size=4)
    meanings=w.records("meanings")
    if len(meanings)!=587 or any(meanings.get(m["id"])!=m for m in additions):
        raise PipelineError("Four new source-screened contexts not found")
    historic=jsonl(archive)
    if len(historic)!=618 or len({r["formulation_id"] for r in historic})!=618:
        raise PipelineError("Historic individual review snapshot missing")
    d=digest(list(meanings.values()))
    upcoming=[dict(p,meaning_catalog_digest=d) for p in historic]
    for p in individual:
        upcoming.append({"formulation_id":p["formulation_id"],"meaning_id":p["meaning_id"],
          "meaning_catalog_digest":d,"decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,"source":"independent_product_eigen_graph_egf_math_screen_batch129",
          "editorial_reason":"Individual mathematical source formulation screened; prerequisite links require distinct screening.",
          "reviewed_by":None,"human_verified":False})
    if len(previous)==624:
        if {p["formulation_id"]:p for p in previous}!={p["formulation_id"]:p for p in upcoming}:
            raise PipelineError("Rerun would overwrite previously screened evidence")
    else:atomic_jsonl(ledger,sorted(upcoming,key=lambda r:r["formulation_id"]))
    actual=jsonl(ledger);index={r["formulation_id"]:r for r in actual}
    if len(actual)!=624 or len(index)!=624:raise PipelineError("624 individual mathematical dispositions expected")
    for p in historic:
        now=index[p["formulation_id"]]
        if any(now.get(k)!=v for k,v in p.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Unrelated prior mathematical decision altered")
    if dict(Counter(r["decision"] for r in actual))!={"linked":612,"no_supported_target":6,"needs_review":6}:
        raise PipelineError("Wrong new/past mathematical decision split")
    check_cycles(meanings,w.records("relations"))
    st=w.state("meanings");st.update(total=587,record_digest=d,screened_new_formulations=193,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",st)
    report={"batch":129,"screened_meanings":587,"reviewed_formulations":624,
      "new_contextual_meanings":4,"new_source_specific_formulations":6,
      "product_subbasis_finite_support_basis_equivalent":True,
      "operator_eigenvalue_two_nonzero_kernel_forms_equivalent":True,
      "nonempty_connected_graph_scope_explicit":True,"egf_convergence_restriction_preserved":True,
      "old_618_formulation_decisions_and_840_links_preserved":True,"pending_individual_form_review":6,
      "three_historical_held_source_defects_unpromoted":True,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch130: individually link each of six formulations, preserve 840 historic dependencies, then consider targeted independent backfill."}
    atomic_json(w.root/"state/wave2_branch129_meaning_screen.json",report);return report
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
