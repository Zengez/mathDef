"""Batch138: append four formerly missing convex/Stirling prerequisites safely.

The prior 883 source-screened links and all 639 individual formulation
decisions and review rationales are immutable. Only append exact relation IDs.
"""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":481,"observations":953,"meanings":595}
STIR="https://proofwiki.org/wiki/Definition%3AStirling_Numbers_of_the_Second_Kind"
CONV="https://proofwiki.org/wiki/Definition%3AConvex_Hull"
DELTA="https://proofwiki.org/wiki/Definition%3AKronecker_Delta"
FALL="https://proofwiki.org/wiki/Definition%3AFalling_Factorial"
SET="https://proofwiki.org/wiki/Definition%3AConvex_Set_%28Vector_Space%29"
EDGES=(
 ("01","form.wave2.cross133.stirling-second-kind.1","meaning.wave2.bridge136.numeric-delta","δ",STIR,DELTA,
  "The second-kind Stirling recurrence uses the Kronecker delta for S(n,0)=δ_(n,0) and S(0,k)=δ_(0,k). The newly source-screened numerical equality-indicator delta supplies exact boundary cases without confusing it with the Dirac delta or a ring-valued output."),
 ("02","form.wave2.cross133.stirling-second-kind.2","meaning.wave2.bridge136.falling-real-nonnegative",r"x^{\underline{k}}",STIR,FALL,
  "The Stirling polynomial identity uses the kth falling factorial polynomial x^{underline k}, including the k=0 term equal to one. The independently sourced nonnegative falling-factorial definition now supplies exactly these basis polynomials, with its zero case externally corroborated."),
 ("03","form.wave2.cross133.convex-hull-real.2","meaning.wave2.bridge136.convex-real","C is convex",CONV,SET,
  "The convex-hull intersection definition quantifies over every convex subset C of the ambient real vector space that contains U. The newly reviewed convex-set meaning supplies the exact two-point real-segment closure property, without adding topological closedness."),
 ("04","form.wave2.cross133.convex-hull-real.3","meaning.wave2.bridge136.convex-real","convex subset",CONV,SET,
  "The unique least-convex-superset definition requires C itself to satisfy the convex-subset property before comparing it to every convex superset. The independently sourced convexity predicate supplies that condition, with the empty set included.")
)
AFFECTED={r[1] for r in EDGES}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    text="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=text:
        raise PipelineError("Historical mathematics backfill review evidence changed")
    path.write_text(text,encoding="utf-8");return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in (*BASE,"relations")):
        raise PipelineError("Independent unsealed Wave2 required")
    if {k:len(w.records(k)) for k in BASE}!=BASE:
        raise PipelineError("Batch137 reviewed mathematical meanings not present")
    r137=json.loads((w.root/"state/wave2_bridge137_link_review.json").read_text())
    missing=jsonl(w.root/"wave2/cross134_missing_prerequisite_targets.jsonl")
    if r137.get("screened_relationships")!=883 or r137.get("reviewed_formulations")!=639 or len(missing)!=3:
        raise PipelineError("Previous independent Batch134 missing targets / Batch137 review missing")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=639:raise PipelineError("Expected all 639 original source forms")
    before_rel=w.records("relations")
    if len(before_rel) not in (883,887):raise PipelineError("Unexpected prior screened link count")
    old={i:r for i,r in before_rel.items() if not i.startswith("rel.wave2.bridge138.")}
    if len(old)!=883:raise PipelineError("All 883 earlier reviewed links required")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    previous=jsonl(ledger);by={r["formulation_id"]:r for r in previous}
    if (len(previous)!=639 or len(by)!=639
      or any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in previous)
      or {i for r in previous for i in r["relation_ids"]}!=set(before_rel)):
        raise PipelineError("Earlier full individual formulation review ledger invalid")
    links=[]
    for n,fid,target,phrase,srcurl,tgturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Previously source-screened endpoint missing "+n)
        _,form=forms[fid];sourceids=form.get("evidence_ids",[])
        if (form["review_state"]!="screened" or len(sourceids)!=1 or sourceids[0] not in obs
            or obs[sourceids[0]]["locator"]!=srcurl or locator(ms[target],obs)!=tgturl
            or phrase not in form["text"] or len(reason)<150):
            raise PipelineError("Unverified direct source phrase or exact mathematical meaning "+n)
        links.append({"id":"rel.wave2.bridge138."+n,
          "from_formulation":fid,"target_meaning":target,"relation_type":"definition_uses",
          "review_state":"screened","source_phrase":phrase,
          "source_locator":srcurl,"target_locator":tgturl,
          "editorial_reason":reason,
          "reviewed_by":"assistant_independent_stirling_convex_retroactive_dependency_review_2026_10_20",
          "human_verified":False})
    if len(links)!=4 or len(AFFECTED)!=4:
        raise PipelineError("Four exact historic target gaps require individual checks")
    check_cycles(ms,{**old,**{r["id"]:r for r in links}})
    archive=w.root/"state/wave2_formulation_reviews_snapshot_639_before_bridge138.jsonl"
    if len(before_rel)==883:
        if any(by[fid]["decision"]!="linked" or not by[fid]["relation_ids"] for fid in AFFECTED):
            raise PipelineError("Previously sourced forms must have completed individual review")
        raw=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=raw:
            raise PipelineError("Historic review snapshot mutated")
        archive.write_text(raw,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_639_before_bridge138.json",{
          "rows":639,"prior_links":883,
          "sha256":hashlib.sha256(raw.encode()).hexdigest(),"human_peer_verified":False})
    saved=jsonl(archive);oldidx={r["formulation_id"]:r for r in saved}
    if len(saved)!=639 or len(oldidx)!=639:raise PipelineError("Full old 639 review snapshot missing")
    store(w.root/"wave2/bridge138_individual_backfill_links.jsonl",links)
    intake=store(w.root/"intake/bridge138_backfill_links.jsonl",links)
    if len(before_rel)==883:w.ingest("relations",intake,batch_size=4)
    rel=w.records("relations")
    if len(rel)!=887 or any(rel.get(r["id"])!=r for r in links):
        raise PipelineError("Four historical source-specific new links not present")
    check_cycles(ms,rel)
    changed=[]
    for p in saved:
        r=dict(p);fid=r["formulation_id"]
        if fid in AFFECTED:
            extras=[e["id"] for e in links if e["from_formulation"]==fid]
            if len(extras)!=1 or extras[0] in r["relation_ids"]:
                raise PipelineError("New prerequisite duplicated or lacks source form")
            r["relation_ids"]=[*r["relation_ids"],*extras]
        changed.append(r)
    if len(before_rel)==887:
        if {r["formulation_id"]:r for r in previous}!={r["formulation_id"]:r for r in changed}:
            raise PipelineError("Rerun would rewrite historical mathematical decisions")
    else:atomic_jsonl(ledger,sorted(changed,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);idx={r["formulation_id"]:r for r in final}
    if len(final)!=639 or len(idx)!=639:raise PipelineError("Full 639 reviews required")
    for fid,oldrow in oldidx.items():
        newer=idx[fid]
        if fid in AFFECTED:
            if (any(newer.get(k)!=v for k,v in oldrow.items() if k!="relation_ids")
                or newer["relation_ids"][:len(oldrow["relation_ids"])]!=oldrow["relation_ids"]):
                raise PipelineError("Original review rationale/decision or link order altered")
        elif newer!=oldrow:raise PipelineError("Unrelated historical review altered")
    if dict(Counter(r["decision"] for r in final))!={"linked":633,"no_supported_target":6}:
        raise PipelineError("Historically reviewed formulation decision distribution changed")
    if {i for r in final for i in r["relation_ids"]}!=set(rel):
        raise PipelineError("Unreviewed relation after target coverage backfill")
    for path in ("wave2/conv125_quarantined_source_claims.jsonl","wave2/quot118_quarantined_source_claims.jsonl","wave2/directional112_quarantined_source_claims.jsonl"):
        hold=jsonl(w.root/path)
        if len(hold)!=1 or hold[0]["observation_id"] in {i for m in ms.values() for f in m["formulations"] for i in f["evidence_ids"]}:
            raise PipelineError("Known bad mathematical source promoted")
    result={"batch":138,"screened_meanings":595,"reviewed_formulations":639,
      "screened_relationships":887,"new_individually_screened_backfill_links":4,
      "all_883_previous_relations_preserved":True,
      "all_639_individual_formulation_decisions_and_rationales_untouched":True,
      "only_four_existing_forms_have_appended_link_ids":True,
      "stirling_delta_and_falling_factorial_targets_recovered":True,
      "convex_hull_convex_set_target_recovered":True,
      "three_historical_source_holds_unchanged":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch139: independently sourced breadth outside current convex/Stirling/bipartite branch, or read-only mathematical source-quality audit."}
    atomic_json(w.root/"state/wave2_bridge138_retroactive_links.json",result);return result
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
