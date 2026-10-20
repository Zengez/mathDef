"""Batch 63: five source-screened meanings from four set-theoretic terms.

Natural-number conventions remain distinct meanings under one heading.
Every old meaning review is retained unchanged except for its catalog digest.
"""
from __future__ import annotations
import argparse,json,hashlib
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
REVIEW="wave2/foundational_set_theory_sources_batch61_2026-10-20.jsonl"
BEFORE={"sources":14,"terms":406,"observations":830,"meanings":503,"relations":681}
AFTER=dict(BEFORE,meanings=508)
MEANINGS=(
  ("natural-numbers","natural-including-zero","Natural numbers containing zero",
   "With the zero-inclusive convention, N is the collection of natural numbers 0,1,2,3,…; its positive subset N_{>0} consists of those elements different from 0.",
   "The ProofWiki Natural Numbers entry explicitly adopts the 0-inclusive convention and describes the distinct positive subset. This is the convention used in the independently screened integer construction and does not imply all textbook conventions include zero."),
  ("natural-numbers","natural-positive-convention","Natural numbers starting at one",
   "Under the positive-counting convention, the natural numbers are 1,2,3,…, denoted N_{>0} when N is defined to include 0.",
   "ProofWiki separately records the traditional counting convention excluding 0. This is a conventional alternative, not a claim that 0 lies in the positive naturals; preserve an explicit context whenever a source says 'natural numbers'."),
  ("equivalence-relation","relation-reflexive-symmetric-transitive","Binary equivalence relation on a set",
   "An equivalence relation ∼ on S is a subset of S×S such that x∼x for every x∈S; x∼y implies y∼x; and x∼y and y∼z together imply x∼z for all x,y,z∈S.",
   "The source states the reflexive, symmetric, transitive characterization of a relation on a set. The underlying set and relation must be specified; the definition is not the later equivalence-class or quotient-set construction."),
  ("equivalence-class","set-of-related-elements","Equivalence class under a relation",
   "If ∼ is an equivalence relation on S and x∈S, the equivalence class [x] is the set {y∈S:y∼x}. Its elements are representatives of the same class.",
   "The source constructs a subset of S associated with a fixed x, and symmetry permits use of y∼x or x∼y. An equivalence class is generally not a single element x and not the entire quotient collection."),
  ("quotient-set","set-of-equivalence-classes","Quotient set of an equivalence relation",
   "Given an equivalence relation ∼ on a set S, its quotient set is S/∼={[x]:x∈S}, the collection of all ∼-equivalence classes.",
   "ProofWiki explicitly defines the quotient as the set of classes, not any representative. A quotient ring/group requires additional compatibility of operations, while a quotient-set universal property is a separate theorem.")
)
def store(path,records):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in records)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Changed a prior individually screened set-theoretic review")
    path.write_text(body,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Independent unsealed Wave 2 required")
    counts={s:len(w.records(s)) for s in BEFORE}
    if counts not in (BEFORE,AFTER):
        raise PipelineError("Unexpected foundation meaning inventory")
    candidates={r["key"]:r for r in jsonl(w.root/REVIEW)}
    if len(candidates)!=4:
        raise PipelineError("Four independent mathematical source audits required")
    terms=w.records("terms");observations=w.records("observations")
    additions=[];reviews=[]
    for key,suffix,context,body,reason in MEANINGS:
        research=candidates.get(key)
        tid="term.wave2.set62."+key;oid="obs.wave2.set62."+key
        if (not research or research["source_id"]!="src.proofwiki"
            or research["source_access_outcome"]!="direct_page_read"
            or research["meaning_screened"] or research["production_corpus_used"]
            or tid not in terms or oid not in observations
            or observations[oid]["term_id"]!=tid
            or observations[oid]["locator"]!=research["source"]
            or len(reason)<180):
            raise PipelineError("Independent source/mathematical review mismatch: "+key)
        mid="meaning.wave2.set63."+suffix
        fid="form.wave2.set63."+suffix
        group="wave2.set63."+key
        additions.append({
            "id":mid,"term_group_id":group,"display_term":research["term"],
            "context":context,"term_ids":[tid],
            "editorial_status":"individually_source_and_mathematical_screened",
            "editorial_screening_reason":reason,
            "source_review_id":research["review_id"],"human_verified":False,
            "formulations":[{
                "id":fid,"text":body,"evidence_ids":[oid],
                "review_state":"screened","human_verified":False,
                "source_screened_by":"assistant_independent_set_theory_screen_2026_10_20",
                "mathematical_review_reason":reason
            }]
        })
        reviews.append({
            "review_id":"review.wave2.set63."+suffix,
            "meaning_id":mid,"formulation_id":fid,"source_observation_id":oid,
            "source_locator":research["source"],"individual_reason":reason,
            "decision":"individually_screened_pending_prerequisite_review",
            "human_verified":False,"production_corpus_used":False
        })
    if len({r["id"] for r in additions})!=5:
        raise PipelineError("Duplicate context-specific mathematical meanings")
    store(w.root/"wave2/set_theory_individual_meaning_reviews_batch63.jsonl",reviews)
    intake=store(w.root/"intake/set_theory_meanings_batch63.jsonl",additions)
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    historical_current=jsonl(ledger)
    before_meanings=w.records("meanings")
    if len(historical_current) not in (516,521) or len({r["formulation_id"] for r in historical_current})!=len(historical_current):
        raise PipelineError("History of individual formulation reviews inconsistent")
    if {i for row in historical_current for i in row["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Historical source-screened links unreviewed")
    snapshot=w.root/"state/wave2_formulation_reviews_snapshot_516_before_set63.jsonl"
    if len(before_meanings)==503:
        if len(historical_current)!=516 or any(r["meaning_catalog_digest"]!=digest(list(before_meanings.values())) for r in historical_current):
            raise PipelineError("Historical 516 review digest mismatch")
        text=ledger.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=text:
            raise PipelineError("Existing review snapshot changed")
        snapshot.write_text(text,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_516_before_set63.json",{
            "rows":516,"links":681,"sha256":hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "human_peer_verified":False
        })
        w.ingest("meanings",intake,batch_size=5)
    now=w.records("meanings")
    if len(now)!=508 or any(now.get(r["id"])!=r for r in additions):
        raise PipelineError("Meaning inventory changed outside the individually reviewed batch")
    previous=jsonl(snapshot)
    if len(previous)!=516 or len({x["formulation_id"] for x in previous})!=516:
        raise PipelineError("Missing 516-review snapshot")
    h=digest(list(now.values()))
    outgoing=[dict(r,meaning_catalog_digest=h) for r in previous]
    for meaning in additions:
        f=meaning["formulations"][0]
        outgoing.append({
            "formulation_id":f["id"],"meaning_id":meaning["id"],
            "meaning_catalog_digest":h,"decision":"needs_review",
            "relation_ids":[],"original_wave1_disposition":None,
            "source":"independent_set_theory_mathematical_review_batch63",
            "editorial_reason":"Mathematical formulation screened, exact noncircular individual prerequisite screening pending.",
            "reviewed_by":None,"human_verified":False
        })
    if len(historical_current)==521:
        indexed={r["formulation_id"]:r for r in historical_current}
        if len(indexed)!=521 or any(indexed.get(r["formulation_id"])!=r for r in outgoing):
            raise PipelineError("Previous set-theory screening disagrees with current reviews")
    else:
        atomic_jsonl(ledger,sorted(outgoing,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);idx={r["formulation_id"]:r for r in final}
    if len(idx)!=521 or len(final)!=521:
        raise PipelineError("Unreviewed new formulation")
    for old in previous:
        new=idx[old["formulation_id"]]
        if any(new.get(k)!=v for k,v in old.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Prior formulation decision modified")
    if {i for r in final for i in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Lost previously screened relationship provenance")
    check_cycles(now,w.records("relations"))
    if dict(Counter(r["decision"] for r in final))!={"linked":511,"no_supported_target":5,"needs_review":5}:
        raise PipelineError("Formulation disposition distribution changed unexpectedly")
    state=w.state("meanings")
    state.update(total=508,record_digest=h,screened_new_formulations=90,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
      "batch":63,"screened_meanings":508,"reviewed_formulations":521,"links":681,
      "new_meanings":5,"two_natural_number_contexts_same_term_group":True,
      "all_516_historical_formulation_decisions_preserved":True,
      "all_681_historical_links_preserved":True,"pending_prerequisite_decisions":5,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Individually review basic set-theoretic prerequisites and formally revise the integer-construction no-target decision only after validating exact concepts."
    }
    atomic_json(w.root/"state/wave2_set_meanings_batch63.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    args=p.parse_args()
    print(json.dumps(run(args.workspace),indent=2))

if __name__=="__main__":main()
