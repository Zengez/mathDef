"""Batch 68: individual prerequisite outcomes for three variant formulations.

Equivalence of compact and quasi-compact *terminology* does not produce a
definition-use edge; both formulations depend only on a topological space.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":408,"observations":834,"meanings":509}
TOPO_URL="https://proofwiki.org/wiki/Definition%3ATopological_Space"
COMPACT_URL="https://proofwiki.org/wiki/Definition%3ACompact_Topological_Space"
SIGMA_URL="https://proofwiki.org/wiki/Definition%3ASigma_Algebra"
NEW={
 "form.wave2.broad67.sigma-difference-disjoint-countable",
 "form.wave2.broad67.compact-open-cover",
 "form.wave2.broad67.compact-closed-fip"
}
LINKS=(
 ("01","form.wave2.broad67.compact-open-cover",
  "meaning.wave2.foundation.topological-space",
  "topological space X",COMPACT_URL,TOPO_URL,
  "The open-cover finite-subcover definition is a property of a topological space, where the collection of open subsets comes from the chosen topology. The independently screened topological-space meaning supplies that structure. No Hausdorff condition is required in either definition."),
 ("02","form.wave2.broad67.compact-closed-fip",
  "meaning.wave2.foundation.topological-space",
  "closed subsets of X",COMPACT_URL,TOPO_URL,
  "The finite-intersection definition is a property of a topological space and its closed subsets, namely complements of open sets in its topology. This prerequisite is noncircular and distinct from a synonym relationship to quasi-compactness or a separation axiom.")
)
NO_TARGET={
 "formulation_id":"form.wave2.broad67.sigma-difference-disjoint-countable",
 "source_locator":SIGMA_URL,
 "decision":"no_supported_target",
 "reviewed_by":"assistant_independent_measure_topology_variant_link_screen_2026_10_20",
 "reason":"The alternate sigma-algebra axioms use a family of subsets, set difference, and countable disjoint unions. The independently screened meaning of a sigma-algebra is the SAME meaning to which the alternative formulation was added, so linking it to itself would be an invalid recursive dependency. There is not yet a separately screened source-specific set-difference or countable-family prerequisite; do not manufacture a link merely to complete the graph.",
 "human_verified":False
}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Reviewed cross-domain link batch content changed")
    path.write_text(body,encoding="utf-8")
    return path
def form_locator(form,obs):
    refs=form.get("evidence_ids",[])
    if len(refs)!=1 or refs[0] not in obs:
        raise PipelineError("Variant source cannot be uniquely determined")
    return obs[refs[0]]["locator"]
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BASE,"relations")):
        raise PipelineError("Unsealed independently reconstructed Wave 2 required")
    if {s:len(w.records(s)) for s in BASE}!=BASE:
        raise PipelineError("Source/meaning inventory changed")
    meanings=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
    if len(forms)!=524 or not NEW.issubset(forms):
        raise PipelineError("New source-screened variant formulations missing")
    relations=w.records("relations")
    if len(relations) not in (691,693):
        raise PipelineError("Unexpected source-reviewed prerequisite count")
    prior_links={k:v for k,v in relations.items() if not k.startswith("rel.wave2.broad68.")}
    if len(prior_links)!=691:
        raise PipelineError("Earlier 691 screened relationships changed")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    current=jsonl(ledger)
    indexed={r["formulation_id"]:r for r in current}
    if (len(current)!=524 or len(indexed)!=524
        or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in current)
        or {rid for r in current for rid in r["relation_ids"]}!=set(relations)):
        raise PipelineError("Existing individual formulation reviews incomplete")
    prepared=[]
    for n,fid,target,phrase,source_url,target_url,reason in LINKS:
        if fid not in forms or target not in meanings:
            raise PipelineError("Missing independent source/target")
        m,f=forms[fid]
        if (f["review_state"]!="screened"
            or form_locator(f,obs)!=source_url
            or locator(meanings[target],obs)!=target_url
            or phrase not in f["text"] or len(reason)<185):
            raise PipelineError("Source-specific mathematical prerequisite not supported: "+n)
        prepared.append({
           "id":"rel.wave2.broad68."+n,"from_formulation":fid,
           "target_meaning":target,"relation_type":"definition_uses",
           "review_state":"screened","source_phrase":phrase,
           "source_locator":source_url,"target_locator":target_url,
           "editorial_reason":reason,
           "reviewed_by":"assistant_independent_measure_topology_variant_link_screen_2026_10_20",
           "human_verified":False
        })
    projected={**prior_links,**{r["id"]:r for r in prepared}}
    check_cycles(meanings,projected)
    if (forms[NO_TARGET["formulation_id"]][0]["id"]!="meaning.wave2.foundation.sigma-algebra"
        or form_locator(forms[NO_TARGET["formulation_id"]][1],obs)!=SIGMA_URL
        or len(NO_TARGET["reason"])<250):
        raise PipelineError("No-target decision not supported")
    snapshot=w.root/"state/wave2_formulation_reviews_snapshot_524_before_broad68.jsonl"
    if len(relations)==691:
        if any(indexed[fid]["decision"]!="needs_review" or indexed[fid]["relation_ids"] for fid in NEW):
            raise PipelineError("New variant review already revised without audit")
        prev=ledger.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=prev:
            raise PipelineError("Historical individual-review snapshot conflict")
        snapshot.write_text(prev,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_524_before_broad68.json",{
          "rows":524,"links":691,"sha256":hashlib.sha256(prev.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
    historic=jsonl(snapshot)
    if len(historic)!=524 or len({x["formulation_id"] for x in historic})!=524:
        raise PipelineError("Missing initial individual review ledger")
    store(w.root/"wave2/individual_broad_variant_links_batch68.jsonl",prepared)
    store(w.root/"wave2/broad_variant_no_target_batch68.jsonl",[NO_TARGET])
    batch=store(w.root/"intake/broad_variant_links_batch68.jsonl",prepared)
    if len(relations)==691:
        w.ingest("relations",batch,batch_size=2)
    links=w.records("relations")
    if len(links)!=693 or any(links.get(r["id"])!=r for r in prepared):
        raise PipelineError("Screened compactness dependencies not committed")
    check_cycles(meanings,links)
    review=[]
    for row in historic:
        nextrow=dict(row)
        fid=row["formulation_id"]
        if fid in NEW:
            attached=[r["id"] for r in prepared if r["from_formulation"]==fid]
            nextrow["relation_ids"]=attached
            nextrow["reviewed_by"]="assistant_independent_measure_topology_variant_link_screen_2026_10_20"
            if attached:
                nextrow["decision"]="linked"
                nextrow["source"]="independent_compactness_topology_source_screen_batch68"
                nextrow["editorial_reason"]="Exact topological-space prerequisite supported by independently screened source and target contexts; no implicit Hausdorff assumption and no synonym cycle."
            else:
                if fid!=NO_TARGET["formulation_id"]:
                    raise PipelineError("A new formulation still lacks a decision")
                nextrow["decision"]="no_supported_target"
                nextrow["source"]="independent_sigma_algebra_variant_no_self_link_review_batch68"
                nextrow["editorial_reason"]=NO_TARGET["reason"]
        review.append(nextrow)
    if len(relations)==693:
        if {r["formulation_id"]:r for r in review}!={r["formulation_id"]:r for r in current}:
            raise PipelineError("Prior screened outcomes differ")
    else:
        atomic_jsonl(ledger,sorted(review,key=lambda r:r["formulation_id"]))
    now=jsonl(ledger);by={r["formulation_id"]:r for r in now}
    if len(now)!=524 or len(by)!=524:
        raise PipelineError("Formulation review ledger incomplete")
    for r in historic:
        if r["formulation_id"] not in NEW and by[r["formulation_id"]]!=r:
            raise PipelineError("Previously reviewed mathematical context changed")
    if {rid for row in now for rid in row["relation_ids"]}!=set(links):
        raise PipelineError("Unreviewed definition relation exists")
    outcomes=dict(Counter(row["decision"] for row in now))
    if outcomes!={"linked":518,"no_supported_target":6}:
        raise PipelineError("Incorrect complete formulation review outcomes "+str(outcomes))
    info={
      "batch":68,"contextual_meanings":509,"reviewed_formulations":524,
      "screened_links":693,"new_individually_screened_links":2,
      "sigma_new_variant_explicit_no_supported_target_not_self_linked":True,
      "compact_topological_space_no_hausdorff_requirement":True,
      "all_521_previous_formulation_reviews_unchanged":True,
      "all_691_previous_screened_links_preserved":True,
      "no_dependency_cycles":True,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Continue breadth-first discovery across measure theory, topology, algebra and applied mathematics. Check source variants and conventions before declaring distinct contextual meanings."
    }
    atomic_json(w.root/"state/wave2_broad_relation_review_batch68.json",info)
    return info
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(parser.parse_args().workspace),indent=2))
if __name__=="__main__":main()
