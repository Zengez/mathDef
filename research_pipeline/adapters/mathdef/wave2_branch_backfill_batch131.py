"""Batch131: three retroactive direct prerequisites to independently recovered targets.

The previously reviewed pointwise convergence and both eigenvector forms
gain only additional source-grounded relation IDs. Their decisions/rationales,
and the prior 852 edges, are preserved in exact order.
"""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":473,"observations":938,"meanings":587}
POINT="https://proofwiki.org/wiki/Definition%3APointwise_Convergence"
EIGV="https://proofwiki.org/wiki/Definition%3AEigenvector/Linear_Operator"
PROD="https://proofwiki.org/wiki/Definition%3AProduct_Topology"
EIG="https://proofwiki.org/wiki/Definition%3AEigenvalue"
EDGES=(
 ("01","form.wave2.conv126.pointwise-topological","meaning.wave2.branch129.indexed-product-topology","product space T^D",POINT,PROD,
  "Topological pointwise convergence is explicitly convergence in the product topology of function space T^D. Its domain D indexes a product with every factor T, so the independently screened product-topology definition supplies this exact previously missing prerequisite."),
 ("02","form.wave2.conv126.eigenvector-linear-operator.1","meaning.wave2.branch129.operator-eigenvalue","eigenvalue",EIGV,EIG,
  "The source's equation definition of eigenvector v≠0 assumes scalar λ is an eigenvalue of A. That operator eigenvalue is independently screened by nontrivial shifted kernel and is now available as a direct prerequisite without reversing the dependency."),
 ("03","form.wave2.conv126.eigenvector-linear-operator.2","meaning.wave2.branch129.operator-eigenvalue","eigenvalue",EIGV,EIG,
  "The source's nonzero shifted-kernel definition of eigenvector explicitly fixes eigenvalue λ. The independently sourced scalar eigenvalue meaning ensures the kernel is nontrivial; the earlier eigenvector meaning does not define eigenvalue itself.")
)
AFFECTED={r[1] for r in EDGES}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Historical backfill mathematical source evidence differs")
    path.write_text(body,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in (*BASE,"relations")):
        raise PipelineError("Independent editable Wave2 required")
    if {k:len(w.records(k)) for k in BASE}!=BASE:
        raise PipelineError("B130 mathematically reviewed catalog baseline missing")
    report=json.loads((w.root/"state/wave2_branch130_link_review.json").read_text())
    prior_gaps=jsonl(w.root/"wave2/conv127_missing_prerequisite_targets.jsonl")
    if report.get("screened_relationships")!=852 or report.get("reviewed_formulations")!=624 or len(prior_gaps)!=2:
        raise PipelineError("Verified B130 links or B127 missing prerequisite records absent")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=624:raise PipelineError("Expected 624 original source-specific formulation records")
    prior=w.records("relations")
    if len(prior) not in (852,855):raise PipelineError("Unexpected previous reviewed link count")
    historic={i:r for i,r in prior.items() if not i.startswith("rel.wave2.branch131.")}
    if len(historic)!=852:raise PipelineError("All 852 earlier reviewed relations required")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    current=jsonl(ledger);index={r["formulation_id"]:r for r in current}
    if (len(current)!=624 or len(index)!=624 or
        any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in current) or
        {i for r in current for i in r["relation_ids"]}!=set(prior)):
        raise PipelineError("Prior complete individual review ledger invalid")
    additions=[]
    for n,fid,target,phrase,srcurl,tgturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Missing exact independent link endpoint "+n)
        _,f=forms[fid];evidence=f.get("evidence_ids",[])
        if (f["review_state"]!="screened" or len(evidence)!=1 or evidence[0] not in obs or
            obs[evidence[0]]["locator"]!=srcurl or locator(ms[target],obs)!=tgturl or
            phrase not in f["text"] or len(reason)<150):
            raise PipelineError("Unsupported mathematical source or target phrase "+n)
        additions.append({"id":"rel.wave2.branch131."+n,"from_formulation":fid,
           "target_meaning":target,"relation_type":"definition_uses",
           "review_state":"screened","source_phrase":phrase,"source_locator":srcurl,
           "target_locator":tgturl,"editorial_reason":reason,
           "reviewed_by":"assistant_independent_product_eigen_target_backfill_2026_10_20",
           "human_verified":False})
    if len(additions)!=3 or len(AFFECTED)!=3:
        raise PipelineError("Exactly three independently sourced historical backfill links required")
    check_cycles(ms,{**historic,**{r["id"]:r for r in additions}})
    archive=w.root/"state/wave2_formulation_reviews_snapshot_624_before_branch131.jsonl"
    if len(prior)==852:
        if any(index[fid]["decision"]!="linked" or not index[fid]["relation_ids"] for fid in AFFECTED):
            raise PipelineError("Historical forms not already individually linked")
        data=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=data:
            raise PipelineError("Existing historic 624-row review ledger changed")
        archive.write_text(data,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_624_before_branch131.json",
            {"rows":624,"prior_links":852,"sha256":hashlib.sha256(data.encode()).hexdigest(),"human_peer_verified":False})
    saved=jsonl(archive);old={r["formulation_id"]:r for r in saved}
    if len(saved)!=624 or len(old)!=624:raise PipelineError("Full individual review snapshot missing")
    store(w.root/"wave2/branch131_individual_backfill_links.jsonl",additions)
    intake=store(w.root/"intake/branch131_backfill_links.jsonl",additions)
    if len(prior)==852:w.ingest("relations",intake,batch_size=3)
    after=w.records("relations")
    if len(after)!=855 or any(after.get(r["id"])!=r for r in additions):
        raise PipelineError("Exactly three new reviewed historical links absent")
    check_cycles(ms,after)
    revised=[]
    for old_row in saved:
        row=dict(old_row);fid=row["formulation_id"]
        if fid in AFFECTED:
            added=[r["id"] for r in additions if r["from_formulation"]==fid]
            if len(added)!=1 or any(i in row["relation_ids"] for i in added):
                raise PipelineError("Duplicate or unmatched retroactive target")
            row["relation_ids"]=[*row["relation_ids"],*added]
        revised.append(row)
    if len(prior)==855:
        if {r["formulation_id"]:r for r in current}!={r["formulation_id"]:r for r in revised}:
            raise PipelineError("Repeat backfill would modify historical decisions")
    else:atomic_jsonl(ledger,sorted(revised,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);by={r["formulation_id"]:r for r in final}
    if len(final)!=624 or len(by)!=624:raise PipelineError("624 reviewed source formulations required")
    for fid,r in old.items():
        after_row=by[fid]
        if fid in AFFECTED:
            if any(after_row.get(k)!=v for k,v in r.items() if k!="relation_ids") or after_row["relation_ids"][:len(r["relation_ids"])]!=r["relation_ids"]:
                raise PipelineError("Historic review conclusion or prior link order modified")
        elif after_row!=r:
            raise PipelineError("Unrelated old review was overwritten")
    if {i for r in final for i in r["relation_ids"]}!=set(after):
        raise PipelineError("Unreviewed edge remains after retroactive screen")
    if dict(Counter(r["decision"] for r in final))!={"linked":618,"no_supported_target":6}:
        raise PipelineError("Former mathematical decision distributions changed")
    result={"batch":131,"screened_meanings":587,"reviewed_formulations":624,"screened_relationships":855,
      "new_individually_reviewed_historical_links":3,"all_852_prior_links_preserved":True,
      "all_624_existing_formulation_decisions_and_rationales_preserved":True,
      "three_old_formulations_have_only_appended_link_ids":True,
      "pointwise_product_topology_gap_closed":True,"eigenvector_eigenvalue_gap_closed_noncircular":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch132: further independent mathematical breadth, read-only cross-variant rigor audit and additional source citations; avoid recursive unbounded prerequisite chasing."}
    atomic_json(w.root/"state/wave2_branch131_retroactive_links.json",result);return result
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
