"""Batch 77: screen source-exact dependencies for four new concepts.

A previously justified Noetherian-ring no-target decision is changed ONLY
with an immutable 537-review snapshot and explicit amendment event.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":414,"observations":848,"meanings":514}
PW="https://proofwiki.org/wiki/Definition%3A"
NOETH=PW+"Noetherian_Module"
SUB=PW+"Submodule"
DISC=PW+"Discrete_Topology"
CONT=PW+"Continuous_Mapping_%28Topology%29"
TOPO=PW+"Topological_Space"
RING=PW+"Noetherian_Ring"
OLD="form.wave2.variant71.noetherian.noetherian-as-module"
EDGES=(
 ("01","form.wave2.foundation76.noetherian-module.01",
  "meaning.wave2.foundation76.submodule","submodule",NOETH,SUB,
  "The finite-generation condition quantifies over every A-submodule of the module M. The separately source-screened submodule meaning defines those subsets and inherited module operations, rather than ideals of an unrelated ring."),
 ("02","form.wave2.foundation76.noetherian-module.02",
  "meaning.wave2.foundation76.submodule","submodule",NOETH,SUB,
  "The ascending-chain condition uses submodules ordered by inclusion. The independently screened submodule meaning supplies the objects in the chains, and no Noetherian property is required to define these modules."),
 ("03","form.wave2.foundation76.noetherian-module.03",
  "meaning.wave2.foundation76.submodule","submodule",NOETH,SUB,
  "The maximal condition is taken over nonempty families of submodules, not arbitrary subsets. The source-scoped submodule definition supplies the correct domain of the quantifier independently of any Noetherian hypothesis."),
 ("04","form.wave2.foundation76.discrete-topology.01",
  "meaning.wave2.foundation.topological-space","topology",DISC,TOPO,
  "The discrete topology is the power set of a nonempty underlying set and is a particular instance of the independently screened topological-space axioms. This dependency does not import an unwarranted nonempty assumption into the general topological-space definition."),
 ("05","form.wave2.foundation76.continuous-topological-map.01",
  "meaning.wave2.foundation.topological-space","topological spaces",CONT,TOPO,
  "Continuity via inverse images of open subsets requires topologies on the domain and codomain. The independently screened topological-space definition supplies precisely those open sets; the source also permits empty domains."),
 ("06","form.wave2.foundation76.continuous-topological-map.02",
  "meaning.wave2.foundation.topological-space","open neighborhood",CONT,TOPO,
  "The pointwise open-neighborhood formulation depends on open subsets of the domain and codomain. This is an equivalent test for continuity everywhere and should not be linked to a distinct notion such as an open map."),
 ("07",OLD,"meaning.wave2.foundation76.noetherian-module",
  "R-module",RING,NOETH,
  "For a commutative unital ring R, being Noetherian as an R-module is now a mathematically meaningful independent predicate: the new module definition quantifies over finitely generated submodules, chains of submodules, or the maximal condition. These become ideals in the regular module R and yield the ring formulation without a circular link.")
)
NO_TARGET={
 "formulation_id":"form.wave2.foundation76.submodule.01",
 "source_locator":SUB,"decision":"no_supported_target",
 "reason":"The sourced submodule definition presupposes an underlying left module over a ring, together with its additive group structure. The independent meaning inventory does not currently contain a separately reviewed general module definition. Linking to Noetherian module would reverse the foundations, and ring ideals are only a special case, so neither is a supported direct target.",
 "human_verified":False
}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    s="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=s:
        raise PipelineError("Previously reviewed individual dependency changed")
    path.write_text(s,encoding="utf-8")
    return path
def form_url(f,observations):
    e=f.get("evidence_ids",[])
    if len(e)!=1 or e[0] not in observations:
        raise PipelineError("Cannot verify precise formulation source")
    return observations[e[0]]["locator"]
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BASE,"relations")):
        raise PipelineError("Independent Wave 2 must remain unsealed")
    if {s:len(w.records(s)) for s in BASE}!=BASE:
        raise PipelineError("Unexpected source/meaning baseline")
    meanings=w.records("meanings");observations=w.records("observations")
    forms={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
    if len(forms)!=537:
        raise PipelineError("Expected 537 screened formulations")
    previous_links=w.records("relations")
    if len(previous_links) not in (698,705):
        raise PipelineError("Concurrent unrelated link modification")
    original={i:r for i,r in previous_links.items() if not i.startswith("rel.wave2.foundation77.")}
    if len(original)!=698:
        raise PipelineError("Historical 698 links were modified")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prior=jsonl(ledger);reviewed={r["formulation_id"]:r for r in prior}
    if (len(prior)!=537 or len(reviewed)!=537
        or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in prior)
        or {id for r in prior for id in r["relation_ids"]}!=set(previous_links)):
        raise PipelineError("Previous individual review inventory incomplete")
    screened=[]
    for n,fid,target,phrase,sourceurl,targeturl,reason in EDGES:
        if fid not in forms or target not in meanings:
            raise PipelineError("Unreviewed source/target meaning "+n)
        m,f=forms[fid]
        if (f["review_state"]!="screened" or form_url(f,observations)!=sourceurl
            or locator(meanings[target],observations)!=targeturl
            or phrase not in f["text"] or len(reason)<170):
            raise PipelineError("No precise sourced mathematical dependency "+n)
        screened.append({
          "id":"rel.wave2.foundation77."+n,"from_formulation":fid,
          "target_meaning":target,"relation_type":"definition_uses",
          "review_state":"screened","source_phrase":phrase,
          "source_locator":sourceurl,"target_locator":targeturl,
          "editorial_reason":reason,
          "reviewed_by":"assistant_independent_module_topology_link_review_2026_10_20",
          "human_verified":False
        })
    prepared={**original,**{r["id"]:r for r in screened}}
    check_cycles(meanings,prepared)
    new={fid for fid in forms if fid.startswith("form.wave2.foundation76.")}
    if len(new)!=7 or len(screened)!=7:
        raise PipelineError("Incomplete new formulation screening")
    snap=w.root/"state/wave2_formulation_reviews_snapshot_537_before_foundation77.jsonl"
    if len(previous_links)==698:
        if reviewed[OLD]["decision"]!="no_supported_target" or reviewed[OLD]["relation_ids"]:
            raise PipelineError("Historical Noetherian-ring no-target was silently revised")
        if any(reviewed[id]["decision"]!="needs_review" or reviewed[id]["relation_ids"] for id in new):
            raise PipelineError("One of the seven new formulation reviews is not pending")
        earlier=ledger.read_text(encoding="utf-8")
        if snap.exists() and snap.read_text(encoding="utf-8")!=earlier:
            raise PipelineError("Prior 537-formulation snapshot changed")
        snap.write_text(earlier,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_537_before_foundation77.json",{
          "rows":537,"screened_links":698,
          "sha256":hashlib.sha256(earlier.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
    historical=jsonl(snap)
    old={r["formulation_id"]:r for r in historical}
    if len(historical)!=537 or len(old)!=537 or old[OLD]["decision"]!="no_supported_target":
        raise PipelineError("Required historical Noetherian no-target record lost")
    amendment={
      "event_id":"foundation77.review.noetherian-ring-module-no-target-to-module-definition",
      "formulation_id":OLD,"previous_review_digest":digest(old[OLD]),
      "previous_decision":"no_supported_target","new_decision":"linked",
      "previous_reason":old[OLD]["editorial_reason"],
      "source_scoped_new_link_ids":[r["id"] for r in screened if r["from_formulation"]==OLD],
      "reason":"The independently sourced Noetherian-module predicate now supplies a valid noncircular prerequisite to the ring-as-module equivalent criterion.",
      "human_verified":False,"production_corpus_used":False
    }
    store(w.root/"events/noetherian_module_review_amendment_batch77.jsonl",[amendment])
    store(w.root/"wave2/individual_foundation_links_batch77.jsonl",screened)
    store(w.root/"wave2/individual_foundation_no_target_batch77.jsonl",[NO_TARGET])
    file=store(w.root/"intake/foundation77_links.jsonl",screened)
    if len(previous_links)==698:
        w.ingest("relations",file,batch_size=7)
    links=w.records("relations")
    if len(links)!=705 or any(links.get(r["id"])!=r for r in screened):
        raise PipelineError("New individually screened links not committed")
    check_cycles(meanings,links)
    updated=[]
    for r in historical:
        nextrow=dict(r);fid=r["formulation_id"]
        if fid in new|{OLD}:
            refs=[edge["id"] for edge in screened if edge["from_formulation"]==fid]
            nextrow["relation_ids"]=refs
            nextrow["reviewed_by"]="assistant_independent_module_topology_link_review_2026_10_20"
            if refs:
                nextrow["decision"]="linked"
                nextrow["source"]="independent_cross_domain_foundation_link_review_batch77"
                nextrow["editorial_reason"]="Exact source phrase and independently screened noncircular target meaning verified with provenance."
            else:
                if fid!=NO_TARGET["formulation_id"]:
                    raise PipelineError("Unreviewed new mathematical formulation")
                nextrow["decision"]="no_supported_target"
                nextrow["source"]="independent_module_foundation_no_supported_target_batch77"
                nextrow["editorial_reason"]=NO_TARGET["reason"]
            if fid==OLD:
                nextrow["previous_review_digest"]=digest(old[OLD])
                nextrow["previous_wave2_decision"]="no_supported_target"
                nextrow["override_event_id"]=amendment["event_id"]
        updated.append(nextrow)
    if len(previous_links)==705:
        if {x["formulation_id"]:x for x in prior}!={x["formulation_id"]:x for x in updated}:
            raise PipelineError("Previous successful review differs from requested update")
    else:
        atomic_jsonl(ledger,sorted(updated,key=lambda x:x["formulation_id"]))
    actual=jsonl(ledger);by={r["formulation_id"]:r for r in actual}
    if len(actual)!=537 or len(by)!=537:
        raise PipelineError("Individual formulation reviews missing")
    for fid,r in old.items():
        if fid not in new|{OLD} and by[fid]!=r:
            raise PipelineError("Historical unrelated review changed")
    if {id for r in actual for id in r["relation_ids"]}!=set(links):
        raise PipelineError("Every screened link must be individually reviewed")
    counts=dict(Counter(r["decision"] for r in actual))
    if counts!={"linked":530,"no_supported_target":7}:
        raise PipelineError("Incorrect complete review outcomes "+str(counts))
    info={
      "batch":77,"screened_meanings":514,"reviewed_formulations":537,
      "screened_relations":705,"new_links":7,
      "historical_698_links_preserved":True,
      "all_529_unrelated_prior_formulation_decisions_preserved":True,
      "noetherian_ring_module_prior_no_target_amended_with_event":True,
      "submodule_base_module_definition_missing":True,
      "all_formulation_dependency_decisions_complete":True,
      "dependency_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Independent generic module foundational definition and broad mathematical variant discovery; do not infer links from textual similarity."
    }
    atomic_json(w.root/"state/wave2_foundations_links_batch77.json",info)
    return info
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
