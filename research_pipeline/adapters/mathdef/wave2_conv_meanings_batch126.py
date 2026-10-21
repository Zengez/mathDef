"""Batch126: screen six source-specific meanings, seven safe formulations."""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/convergence_eigen_source_batch125_2026-10-20.jsonl"
BASE={"sources":14,"terms":469,"observations":932,"meanings":577,"relations":825}
AFTER=dict(BASE,meanings=583)
SPECS=(
 ("pointwise-convergence",0,"pointwise-real","Pointwise convergence on a real-function domain, point-dependent cutoff"),
 ("pointwise-convergence",1,"pointwise-topological","Pointwise convergence to map into arbitrary topological target via product topology"),
 ("uniform-convergence",0,"uniform-metric","Uniform convergence on a set to metric-valued function, one cutoff for all inputs"),
 ("uniform-convergence",1,"uniform-real","Uniform convergence of real-valued functions on real domain"),
 ("locally-uniform-convergence",0,"locally-uniform-metric","Locally uniform convergence on topological source to metric target"),
 ("eigenvector-operator",0,"eigenvector-linear-operator","Nonzero eigenvector of a K-linear endomorphism for its eigenvalue")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Historical individual mathematical source screens would change")
    path.write_text(body,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Independent unsealed Wave2 required")
    if {k:len(w.records(k)) for k in BASE} not in (BASE,AFTER):
        raise PipelineError("B125 independently sourced baseline missing")
    report=json.loads((w.root/"state/wave2_conv125_source_intake.json").read_text())
    held=jsonl(w.root/"wave2/conv125_quarantined_source_claims.jsonl")
    if report.get("new_observations")!=8 or len(held)!=1 or held[0]["observation_id"]!="obs.wave2.conv125.uniform-convergence.03":
        raise PipelineError("Unsafe summed-f_n observation not source-held")
    rows={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    db=w.records("terms");obs=w.records("observations")
    additions=[];screens=[]
    for key,ci,suffix,context in SPECS:
        r=rows[key];tid="term.wave2.conv125."+key
        if db.get(tid,{}).get("locator")!=r["source"] or r["production_corpus_consulted"]:
            raise PipelineError("Source lineage mismatch "+suffix)
        c=r["contexts"][ci];fs=c["forms"];reason=r["review"]
        if c.get("held") or len(reason)<370:
            raise PipelineError("Held source claim or mathematically insufficient rationale")
        if key=="pointwise-convergence" and ci==0 and "every x∈D" not in fs[0]["text"]:
            raise PipelineError("Pointwise quantifier order lost")
        if key=="uniform-convergence" and ("all x" not in fs[0]["text"] and "every x" not in fs[0]["text"]):
            raise PipelineError("Uniform quantifier order lost")
        if key=="locally-uniform-convergence" and "neighborhood" not in fs[0]["text"]:
            raise PipelineError("Local neighborhoods required")
        if key=="eigenvector-operator" and (len(fs)!=2 or any("v≠0" not in f["text"] for f in fs)):
            raise PipelineError("Eigenvectors must be nonzero in both equivalent presentations")
        reason+=" This independently scoped mathematical meaning is distinct from broader or stronger convergence/eigenstructure interpretations."
        mid="meaning.wave2.conv126."+suffix
        frows=[]
        for j,f in enumerate(fs,1):
            oi=(j if key=="eigenvector-operator" else ci+1)
            oid=f"obs.wave2.conv125.{key}.{oi:02d}"
            o=obs.get(oid)
            if not o or o["text"]!=f["text"] or o["term_id"]!=tid or o["locator"]!=r["source"] or oid==held[0]["observation_id"]:
                raise PipelineError("Exact individual mathematical source evidence missing "+oid)
            fid="form.wave2.conv126."+suffix+("."+str(j) if len(fs)>1 else "")
            frows.append({"id":fid,"text":f["text"],"evidence_ids":[oid],"review_state":"screened",
              "human_verified":False,"mathematical_review_reason":reason,
              "source_screened_by":"assistant_independent_convergence_eigen_math_review_2026_10_20"})
            screens.append({"review_id":"review.wave2.conv126."+suffix+("."+str(j) if len(fs)>1 else ""),
              "meaning_id":mid,"formulation_id":fid,"source_observation_id":oid,
              "source_locator":r["source"],"mathematical_reason":reason,
              "decision":"mathematically_screened_pending_individual_dependency_review",
              "human_verified":False,"production_corpus_used":False})
        additions.append({"id":mid,"term_group_id":"wave2.conv126."+key,
           "display_term":r["term"],"context":context,"term_ids":[tid],"formulations":frows,
           "editorial_status":"source_scoped_individually_mathematically_screened",
           "editorial_screening_reason":reason,"human_verified":False})
    if len(additions)!=6 or len(screens)!=7:
        raise PipelineError("Six contexts and seven safe mathematical presentations required")
    store(w.root/"wave2/conv126_individual_mathematical_reviews.jsonl",screens)
    intake=store(w.root/"intake/conv126_meanings.jsonl",additions)
    ms=w.records("meanings");ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    previous=jsonl(ledger)
    if len(previous) not in (611,618) or len({r["formulation_id"] for r in previous})!=len(previous):
        raise PipelineError("All 611 previous formulation decisions must be present")
    if {i for r in previous for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Previous 825 link decisions not preserved")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_611_before_conv126.jsonl"
    if len(ms)==577:
        if len(previous)!=611 or any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in previous):
            raise PipelineError("Prior independent mathematical digest mismatched")
        body=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=body:
            raise PipelineError("Historical formulation review snapshot changed")
        archive.write_text(body,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_611_before_conv126.json",
           {"rows":611,"prior_relations":825,"sha256":hashlib.sha256(body.encode()).hexdigest(),"human_peer_verified":False})
        w.ingest("meanings",intake,batch_size=6)
    meanings=w.records("meanings")
    if len(meanings)!=583 or any(meanings.get(m["id"])!=m for m in additions):
        raise PipelineError("Six correctly sourced mathematical meanings absent")
    prior=jsonl(archive)
    if len(prior)!=611 or len({r["formulation_id"] for r in prior})!=611:
        raise PipelineError("Historic 611 reviewed forms absent")
    d=digest(list(meanings.values()))
    updated=[dict(r,meaning_catalog_digest=d) for r in prior]
    for s in screens:
        updated.append({"formulation_id":s["formulation_id"],"meaning_id":s["meaning_id"],
           "meaning_catalog_digest":d,"decision":"needs_review","relation_ids":[],
           "original_wave1_disposition":None,"source":"independent_convergence_eigen_math_screen_batch126",
           "editorial_reason":"Precise source-specific definition mathematically screened; individual prerequisites await review.",
           "reviewed_by":None,"human_verified":False})
    if len(previous)==618:
        if {r["formulation_id"]:r for r in previous}!={r["formulation_id"]:r for r in updated}:
            raise PipelineError("Repeat screen would alter prior mathematical review")
    else:atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);ix={r["formulation_id"]:r for r in final}
    if len(final)!=618 or len(ix)!=618:raise PipelineError("618 individually dispositioned forms required")
    for r in prior:
        now=ix[r["formulation_id"]]
        if any(now.get(k)!=v for k,v in r.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Old source mathematical decision altered")
    if dict(Counter(r["decision"] for r in final))!={"linked":605,"no_supported_target":6,"needs_review":7}:
        raise PipelineError("Unexpected old/pending review split")
    if held[0]["observation_id"] in {i for m in meanings.values() for f in m["formulations"] for i in f["evidence_ids"]}:
        raise PipelineError("Held erroneous source line was promoted")
    check_cycles(meanings,w.records("relations"))
    state=w.state("meanings");state.update(total=583,record_digest=d,screened_new_formulations=187,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    result={"batch":126,"screened_meanings":583,"reviewed_formulations":618,
      "new_contextual_meanings":6,"new_source_specific_formulations":7,
      "prior_611_mathematical_review_decisions_preserved":True,"prior_825_links_preserved":True,
      "real_and_topological_pointwise_distinguished":True,
      "metric_and_real_uniform_distinguished":True,
      "locally_uniform_neighborhoods_preserved":True,
      "eigenvector_two_equivalent_forms_grouped":True,"zero_vector_not_eigenvector":True,
      "held_uniform_series_typo_unpromoted":True,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch127 independently review direct source links for all seven formulations, preserve 825 earlier edges."}
    atomic_json(w.root/"state/wave2_conv126_meaning_screen.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
