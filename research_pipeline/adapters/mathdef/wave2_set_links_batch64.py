"""Batch 64: individually reviewed set-theoretic links and one historic amendment.

All source/target contexts are independently screened in Wave 2. No original
production mathematical definitions, citations, or generated indexes are read.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":406,"observations":830,"meanings":508}
PW="https://proofwiki.org/wiki/Definition%3A"
INT=PW+"Integer/Formal_Definition"
EQ=PW+"Equivalence_Relation"
EC=PW+"Equivalence_Class"
QS=PW+"Quotient_Set"
NAT=PW+"Natural_Number"
REL=PW+"Relation"
PRODUCT=PW+"Cartesian_Product"
EDGES=(
 ("01","form.wave2.set63.relation-reflexive-symmetric-transitive",
  "meaning.wave2.foundation.binary-relation-subset","subset of S×S",EQ,REL,
  "The standard definition of equivalence relation first requires a binary relation on a set, interpreted as a subset of its Cartesian square. The existing subset-based binary-relation meaning provides the correct underlying object."),
 ("02","form.wave2.set63.relation-reflexive-symmetric-transitive",
  "meaning.wave2.foundation.cartesian-product-binary","S×S",EQ,PRODUCT,
  "A subset R of S×S refers to the Cartesian product of a set with itself. The independently screened binary Cartesian product meaning gives the precise collection of ordered pairs on which reflexivity, symmetry and transitivity are asserted."),
 ("03","form.wave2.set63.set-of-related-elements",
  "meaning.wave2.set63.relation-reflexive-symmetric-transitive","equivalence relation",EC,EQ,
  "An equivalence class is defined only after fixing an equivalence relation on S. This relation determines which y belong to the representative's class and thereby makes the set-of-related-elements definition unambiguous."),
 ("04","form.wave2.set63.set-of-equivalence-classes",
  "meaning.wave2.set63.set-of-related-elements","equivalence classes",QS,EC,
  "A quotient set is the collection of all equivalence classes of the given underlying set. The classes themselves must have been defined before the quotient of the set can be formed."),
 ("05","form.wave2.set63.set-of-equivalence-classes",
  "meaning.wave2.set63.relation-reflexive-symmetric-transitive","equivalence relation",QS,EQ,
  "The quotient is taken with respect to a specified equivalence relation. Different relations may yield distinct quotient partitions of the same underlying set; the relation is an essential component of the construction."),
 ("06","form.wave2.set63.natural-positive-convention",
  "meaning.wave2.set63.natural-including-zero","N_{>0}",NAT,NAT,
  "When N includes zero, the strictly positive indexing convention can be identified with N without the distinguished zero. This link preserves the explicit choice of a starting-index convention without equating the two underlying sets."),
 ("07","form.wave2.integer59.integer-equivalence-class",
  "meaning.wave2.set63.natural-including-zero","natural numbers",INT,NAT,
  "The concrete integer construction represents a signed difference by a pair (a,b) of natural numbers. The reviewed zero-inclusive convention supplies both the natural zero and the entries needed for the resulting difference-class quotient."),
 ("08","form.wave2.integer59.integer-equivalence-class",
  "meaning.wave2.set63.set-of-related-elements","equivalence class",INT,EC,
  "In the pair construction an integer is represented by an equivalence class of N×N under equal-difference equivalence. The independently sourced class definition specifies what such an equivalence class is without invoking integer arithmetic."),
 ("09","form.wave2.integer59.integer-equivalence-class",
  "meaning.wave2.set63.set-of-equivalence-classes","quotient set",INT,QS,
  "The set of integers in this concrete construction is the quotient of N×N by the specified equivalence relation. The quotient-set definition explains why its elements are classes, not individual natural-number pairs."),
 ("10","form.wave2.integer59.integer-equivalence-class",
  "meaning.wave2.foundation.cartesian-product-binary","N×N",INT,PRODUCT,
  "The integer difference construction begins with pairs in the Cartesian square of the natural numbers. The existing Cartesian-product meaning identifies the exact source set prior to taking equivalence classes.")
)
NO_TARGETS=(
 ("form.wave2.set63.natural-including-zero",
  "The zero-inclusive natural-number convention is a primitive set choice here; no separately screened Peano system or finite-ordinal characterization is yet available as a source-matched predecessor. Avoid linking it to the integer ring, which is constructed later."),
)
def store(path,records):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in records)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Prior individually screened graph decision has changed")
    path.write_text(body,encoding="utf-8")
    return path
def source_of_form(form,observations):
    refs=form.get("evidence_ids",[])
    if len(refs)!=1 or refs[0] not in observations:
        raise PipelineError("Ambiguous or missing particular formulation source")
    return observations[refs[0]]["locator"]

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BASE,"relations")):
        raise PipelineError("Independent unsealed Wave 2 only")
    if {s:len(w.records(s)) for s in BASE}!=BASE:
        raise PipelineError("Set theory meanings or source stage moved")
    meanings=w.records("meanings"); obs=w.records("observations")
    forms={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
    if len(forms)!=521:
        raise PipelineError("Expected 521 current reviewed formulations")
    current_rel=w.records("relations")
    if len(current_rel) not in (681,691):
        raise PipelineError("Previous screened link count changed")
    original={k:v for k,v in current_rel.items() if not k.startswith("rel.wave2.set64.")}
    if len(original)!=681:
        raise PipelineError("Some historic screened relations were modified")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prior=jsonl(ledger);idx={r["formulation_id"]:r for r in prior}
    if len(prior)!=521 or len(idx)!=521 or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in prior):
        raise PipelineError("Old 521-formulation review inventory stale")
    if {id for r in prior for id in r["relation_ids"]}!=set(current_rel):
        raise PipelineError("Some historical relationship lacks mathematical review")
    prepared=[]
    for number,fid,target,phrase,sourceurl,targeturl,reason in EDGES:
        if fid not in forms or target not in meanings:
            raise PipelineError("Missing individually screened mathematical source/target")
        m,form=forms[fid]
        if (form["review_state"]!="screened" or
            source_of_form(form,obs)!=sourceurl or
            locator(meanings[target],obs)!=targeturl or
            phrase not in form["text"] or len(reason)<180):
            raise PipelineError("Incorrect source-specific prerequisite "+number)
        prepared.append({
          "id":"rel.wave2.set64."+number,"from_formulation":fid,
          "target_meaning":target,"relation_type":"definition_uses",
          "review_state":"screened","source_phrase":phrase,
          "source_locator":sourceurl,"target_locator":targeturl,
          "editorial_reason":reason,
          "reviewed_by":"assistant_independent_set_foundation_relation_screen_2026_10_20",
          "human_verified":False
        })
    combined={**original,**{r["id"]:r for r in prepared}}
    check_cycles(meanings,combined)
    newly={f["id"] for m in meanings.values() if m["id"].startswith("meaning.wave2.set63.") for f in m["formulations"]}
    old_integer="form.wave2.integer59.integer-equivalence-class"
    if len(newly)!=5 or len(prepared)!=10:
        raise PipelineError("Incomplete individually reviewed set foundations")
    snapshot=w.root/"state/wave2_formulation_reviews_snapshot_521_before_set64.jsonl"
    if len(current_rel)==681:
        if idx[old_integer]["decision"]!="no_supported_target" or idx[old_integer]["relation_ids"]:
            raise PipelineError("Previous no-target integer review cannot be overridden silently")
        if any(idx[f]["decision"]!="needs_review" or idx[f]["relation_ids"] for f in newly):
            raise PipelineError("Previously reviewed foundation not in expected pending status")
        previous=ledger.read_text(encoding="utf-8")
        if snapshot.exists() and snapshot.read_text(encoding="utf-8")!=previous:
            raise PipelineError("Historical 521 formulation review snapshot changed")
        snapshot.write_text(previous,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_521_before_set64.json",{
          "rows":521,"links":681,
          "sha256":hashlib.sha256(previous.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
    earlier=jsonl(snapshot);byold={r["formulation_id"]:r for r in earlier}
    if len(earlier)!=521 or len(byold)!=521 or byold[old_integer]["decision"]!="no_supported_target":
        raise PipelineError("Incomplete previous integer no-target historical proof")
    amend={
       "event_id":"set64.amend.integer.no-target-to-natural-equivalence-quotient",
       "formulation_id":old_integer,
       "prior_review_digest":digest(byold[old_integer]),
       "prior_decision":"no_supported_target","new_decision":"linked",
       "prior_reason":byold[old_integer]["editorial_reason"],
       "supporting_links":[r["id"] for r in prepared if r["from_formulation"]==old_integer],
       "reason":"Four independently screened prerequisites now cover natural-number pairs, equivalence classes, quotient sets, and Cartesian product without relying on downstream integer/rational constructions.",
       "human_verified":False,"production_corpus_used":False
    }
    store(w.root/"events/integer_no_target_amendment_batch64.jsonl",[amend])
    store(w.root/"wave2/set_theory_individual_links_batch64.jsonl",prepared)
    store(w.root/"wave2/natural_zero_convention_no_target_batch64.jsonl",[
       {"formulation_id":fid,"source_locator":NAT,"decision":"no_supported_target",
        "mathematical_reason":reason,"human_verified":False} for fid,reason in NO_TARGETS])
    intake=store(w.root/"intake/set_theory_prerequisites_batch64.jsonl",prepared)
    if len(current_rel)==681:
        w.ingest("relations",intake,batch_size=10)
    after=w.records("relations")
    if len(after)!=691 or any(after.get(r["id"])!=r for r in prepared):
        raise PipelineError("Screened new source-specific links not ingested")
    check_cycles(meanings,after)
    reviewed=[]
    for old in earlier:
        row=dict(old);fid=row["formulation_id"]
        if fid in newly|{old_integer}:
            relations=[r["id"] for r in prepared if r["from_formulation"]==fid]
            row["relation_ids"]=relations
            row["reviewed_by"]="assistant_independent_set_foundation_relation_screen_2026_10_20"
            if relations:
                row["decision"]="linked"
                row["source"]="independent_set_foundation_prerequisite_screen_batch64"
                row["editorial_reason"]="Every exact source/target and mathematical context has been individually checked, and the resulting graph is acyclic."
            else:
                if fid!=NO_TARGETS[0][0]:
                    raise PipelineError("Missing prerequisite review for "+fid)
                row["decision"]="no_supported_target"
                row["source"]="independent_zero_including_natural_primitive_review_batch64"
                row["editorial_reason"]=NO_TARGETS[0][1]
            if fid==old_integer:
                row["previous_review_digest"]=digest(byold[old_integer])
                row["previous_wave2_decision"]="no_supported_target"
                row["override_event_id"]=amend["event_id"]
        reviewed.append(row)
    if len(current_rel)==691:
        if {r["formulation_id"]:r for r in reviewed}!={r["formulation_id"]:r for r in prior}:
            raise PipelineError("Previous set-theoretic link decisions changed")
    else:
        atomic_jsonl(ledger,sorted(reviewed,key=lambda r:r["formulation_id"]))
    now=jsonl(ledger);by={r["formulation_id"]:r for r in now}
    if len(now)!=521 or len(by)!=521:
        raise PipelineError("Not every formulation has one individual review")
    for key,old in byold.items():
        if key not in newly|{old_integer} and by[key]!=old:
            raise PipelineError("Unrelated previous mathematical decision changed")
    if {i for r in now for i in r["relation_ids"]}!=set(after):
        raise PipelineError("Unreviewed new source-screened prerequisite")
    outcomes=dict(Counter(r["decision"] for r in now))
    if outcomes!={"linked":516,"no_supported_target":5}:
        raise PipelineError("Incorrect individual review dispositions "+str(outcomes))
    report={
      "batch":64,"screened_meanings":508,"reviewed_formulations":521,
      "new_links":10,"links_total":691,"old_681_screened_links_preserved":True,
      "old_unrelated_515_formulation_decisions_preserved":True,
      "integer_prior_no_target_overridden_by_explicit_review_event":True,
      "zero_including_natural_no_supported_target_preserved":True,
      "all_521_formulations_individually_reviewed":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Resume broader independent source and variant discovery; keep primitive natural-number model and axiomatic Peano alternative as potential future contextual variants."
    }
    atomic_json(w.root/"state/wave2_set_dependency_review_batch64.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    a=p.parse_args()
    print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
