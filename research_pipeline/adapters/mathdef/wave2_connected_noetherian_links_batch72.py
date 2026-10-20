"""Batch 72: individually source-screen all six newly reviewed formulation links.

The Stacks nonempty-connected convention remains unchanged. No links
equate alternate contexts or create recursive Noetherian dependencies.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BEFORE={"sources":14,"terms":410,"observations":841,"meanings":510}
URL_CONNECTED="https://proofwiki.org/wiki/Definition%3AConnected_Topological_Space"
URL_NOETH="https://proofwiki.org/wiki/Definition%3ANoetherian_Ring"
URL_TOPO="https://proofwiki.org/wiki/Definition%3ATopological_Space"
URL_IDEAL="https://proofwiki.org/wiki/Definition%3AIdeal_of_Ring"
LINKS=(
 ("01","form.wave2.variant71.connected.01","meaning.wave2.foundation.topological-space",
  "topological space X",URL_CONNECTED,URL_TOPO,
  "The no-separation definition is a statement about a topological space and its open subsets. This existing independently sourced topological-space meaning defines those open sets, while the separate Stacks convention excluding the empty space remains intact."),
 ("02","form.wave2.variant71.connected.02","meaning.wave2.foundation.topological-space",
  "topological space X",URL_CONNECTED,URL_TOPO,
  "The clopen-set characterization uses subsets both open and closed relative to the topology on X. The topological-space meaning supplies that exact ambient structure; neither a nonemptiness assumption nor a link to the competing Stacks convention is implied."),
 ("03","form.wave2.variant71.connected.03","meaning.wave2.foundation.topological-space",
  "topological space X",URL_CONNECTED,URL_TOPO,
  "The discrete two-point continuous-surjection test presupposes a topological-space source and target. The independently screened topological-space definition is a valid prerequisite, but continuous map and discrete two-point topology require future separate sourcing."),
 ("04","form.wave2.variant71.noetherian.ascending-chain-condition",
  "meaning.wave2.foundation.two-sided-ideal","ideals",URL_NOETH,URL_IDEAL,
  "The ascending-chain condition in the commutative unital ring is explicitly an ascending chain of ideals. The separately screened ring-ideal definition supplies these objects and the prerequisite direction does not reference the Noetherian condition."),
 ("05","form.wave2.variant71.noetherian.maximal-condition",
  "meaning.wave2.foundation.two-sided-ideal","ideals",URL_NOETH,URL_IDEAL,
  "The maximal-condition characterization quantifies over nonempty collections of ideals ordered by inclusion. The independent ring-ideal meaning supplies their mathematical nature; the existence of a maximal ideal in each collection is additional Noetherian finiteness.")
)
NO_TARGET={
 "formulation_id":"form.wave2.variant71.noetherian.noetherian-as-module",
 "decision":"no_supported_target","source_locator":URL_NOETH,
 "reason":"The equivalence expressing a Noetherian ring as a Noetherian module over itself requires an independently screened definition of a Noetherian module, which the current corpus has not yet supplied. A generic module or ring is not the same predicate; linking to the Noetherian ring itself would be circular. Keep this valid source-screened variant visible and record the missing independently sourced Noetherian-module target.",
 "human_verified":False
}
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    s="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=s:
        raise PipelineError("Changed independently reviewed dependency disposition")
    path.write_text(s,encoding="utf-8")
    return path
def form_url(f,obs):
    e=f.get("evidence_ids",[])
    if len(e)!=1 or e[0] not in obs:
        raise PipelineError("Cannot determine unique variant source")
    return obs[e[0]]["locator"]
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BEFORE,"relations")):
        raise PipelineError("Only unsealed independently researched Wave 2")
    if {s:len(w.records(s)) for s in BEFORE}!=BEFORE:
        raise PipelineError("Source-screened meaning stage has moved")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=530:
        raise PipelineError("Expected six new variants and 524 screened old formulations")
    rel=w.records("relations")
    if len(rel) not in (693,698):
        raise PipelineError("Unrelated relationship edits present")
    oldrels={id:r for id,r in rel.items() if not id.startswith("rel.wave2.variant72.")}
    if len(oldrels)!=693:
        raise PipelineError("Historical reviewed links were changed")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    old=jsonl(ledger);idx={r["formulation_id"]:r for r in old}
    if len(old)!=530 or len(idx)!=530 or any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in old):
        raise PipelineError("Historical individual formulation review ledger stale")
    if {id for r in old for id in r["relation_ids"]}!=set(rel):
        raise PipelineError("Previously reviewed source links not in review ledger")
    prepared=[]
    for n,fid,mid,phrase,fromurl,tourl,reason in LINKS:
        if fid not in forms or mid not in ms:
            raise PipelineError("Missing independent meaning/variant target")
        m,f=forms[fid]
        if (f["review_state"]!="screened" or form_url(f,obs)!=fromurl
             or locator(ms[mid],obs)!=tourl or phrase not in f["text"] or len(reason)<160):
            raise PipelineError("Exact source phrase or target is unsupported: "+n)
        prepared.append({
           "id":"rel.wave2.variant72."+n,"from_formulation":fid,
           "target_meaning":mid,"relation_type":"definition_uses",
           "review_state":"screened","source_phrase":phrase,
           "source_locator":fromurl,"target_locator":tourl,
           "editorial_reason":reason,
           "reviewed_by":"assistant_independent_variant72_mathematical_relation_review_2026_10_20",
           "human_verified":False
        })
    f=NO_TARGET["formulation_id"]
    if f not in forms or form_url(forms[f][1],obs)!=URL_NOETH or len(NO_TARGET["reason"])<230:
        raise PipelineError("Unsourced no-target decision")
    proposals={**oldrels,**{r["id"]:r for r in prepared}}
    check_cycles(ms,proposals)
    pending={fid for fid in forms if fid.startswith("form.wave2.variant71.")}
    if len(pending)!=6:
        raise PipelineError("Unexpected variant batch reviewed scope")
    snapshot=w.root/"state/wave2_formulation_reviews_snapshot_530_before_variant72.jsonl"
    if len(rel)==693:
        if any(idx[fid]["decision"]!="needs_review" or idx[fid]["relation_ids"] for fid in pending):
            raise PipelineError("Pending new variant already had a previous link review")
        text=ledger.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=text:
            raise PipelineError("Prior 530-formulation review snapshot conflict")
        snapshot.write_text(text,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_530_before_variant72.json",{
            "rows":530,"screened_links":693,
            "sha256":hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "human_peer_verified":False
        })
    historic=jsonl(snapshot)
    if len(historic)!=530 or len({r["formulation_id"] for r in historic})!=530:
        raise PipelineError("Prior complete review history missing")
    store(w.root/"wave2/individual_variant72_links.jsonl",prepared)
    store(w.root/"wave2/individual_variant72_no_target.jsonl",[NO_TARGET])
    batch=store(w.root/"intake/variant72_links.jsonl",prepared)
    if len(rel)==693:
        w.ingest("relations",batch,batch_size=5)
    current=w.records("relations")
    if len(current)!=698 or any(current.get(r["id"])!=r for r in prepared):
        raise PipelineError("Source-screened dependency additions missing")
    check_cycles(ms,current)
    changes=[]
    for row in historic:
        nextrow=dict(row)
        fid=row["formulation_id"]
        if fid in pending:
            links=[r["id"] for r in prepared if r["from_formulation"]==fid]
            nextrow["relation_ids"]=links
            nextrow["reviewed_by"]="assistant_independent_variant72_mathematical_relation_review_2026_10_20"
            if links:
                nextrow["decision"]="linked"
                nextrow["source"]="independent_cross_domain_variant_link_review_batch72"
                nextrow["editorial_reason"]="Individually checked independent source phrase, mathematical prerequisite meaning and directed acyclic dependency; distinct connected conventions preserved."
            else:
                if fid!=NO_TARGET["formulation_id"]:
                    raise PipelineError("Unscreened variant dependency")
                nextrow["decision"]="no_supported_target"
                nextrow["source"]="independent_noetherian_module_missing_target_review_batch72"
                nextrow["editorial_reason"]=NO_TARGET["reason"]
        changes.append(nextrow)
    if len(rel)==698:
        if {r["formulation_id"]:r for r in changes}!={r["formulation_id"]:r for r in old}:
            raise PipelineError("Repeated dependency screen disagrees with prior result")
    else:
        atomic_jsonl(ledger,sorted(changes,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);lookup={r["formulation_id"]:r for r in final}
    if len(final)!=530 or len(lookup)!=530:
        raise PipelineError("Incomplete individual link review")
    for r in historic:
        if r["formulation_id"] not in pending and lookup[r["formulation_id"]]!=r:
            raise PipelineError("Historical unrelated review changed")
    if {id for r in final for id in r["relation_ids"]}!=set(current):
        raise PipelineError("Some screened relation lacks individual review")
    counts=dict(Counter(r["decision"] for r in final))
    if counts!={"linked":523,"no_supported_target":7}:
        raise PipelineError("Unexpected final review dispositions "+str(counts))
    report={
       "batch":72,"screened_meanings":510,"reviewed_formulations":530,
       "screened_links":698,"new_source_screened_links":5,
       "old_693_links_preserved":True,"old_524_formulation_reviews_preserved":True,
       "separate_connected_conventions_retained":True,
       "noetherian_module_formulation_requires_new_source_target":True,
       "every_formulation_has_individual_review":True,"graph_acyclic":True,
       "all_stages_unsealed":True,"human_peer_verified":False,
       "original_production_mathdef_used":False,
       "next":"Independently research Noetherian module and foundational continuous maps, then resume subfield-rotating discovery. Do not collapse alternative connectedness conventions."
    }
    atomic_json(w.root/"state/wave2_variant72_links.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
