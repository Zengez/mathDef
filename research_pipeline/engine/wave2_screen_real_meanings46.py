"""Screen three source-scoped real/order meanings with recoverable review migration.

Distinguish a totally ordered field from a Dedekind-complete real ordered
field, and exclude a circular introductory set-of-rationals/irrationals
description. Preserve each of the previous 499 mathematical review decisions.
"""
from __future__ import annotations
import argparse,json,hashlib
from collections import Counter
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .revisions import apply_revision
from .stage5_review_gate import atomic_jsonl
from .wave2_apply_links import check_cycles

SPECS=[
 dict(key="totally-ordered-field",slug="totally-ordered-field",
      term="totally ordered field",
      context="Abstract field equipped with a compatible total order; no completeness assumed",
      text="A totally ordered field is a field F equipped with a total order ≤ such that, for all x,y,z∈F, x<y implies x+z<y+z and, if 0<z, also xz<yz. Dedekind completeness is not required.",
      reason="ProofWiki's Totally Ordered Field subsection requires a field with a total order compatible with ring operations. No least-upper-bound axiom is imposed. Rational numbers with their usual order are an example and are not Dedekind complete.",
      locator="https://proofwiki.org/wiki/Definition%3AOrdered_Field"),
 dict(key="dedekind-supremum",slug="dedekind-supremum-property",
      term="Dedekind completeness property",
      context="Order theory: supremum for all nonempty upper-bounded subsets of a partially ordered set",
      text="An ordered set (S,≤) has the Dedekind completeness property if every nonempty subset A⊆S that has an upper bound in S possesses a least upper bound sup(A)∈S. The requirement excludes the empty subset and does not demand a supremum for sets lacking upper bounds.",
      reason="ProofWiki explicitly requires nonempty subsets bounded above, and a supremum in the ambient ordered set. This is an order-theoretic least-upper-bound property, not unrestricted metric/Cauchy completeness and not existence of suprema for unbounded subsets.",
      locator="https://proofwiki.org/wiki/Definition%3ADedekind_Complete"),
 dict(key="complete-ordered-real-field",slug="axiomatic-complete-ordered-reals",
      term="real number system (complete ordered field)",
      context="Axiomatic real arithmetic: totally ordered commutative field complete for nonempty upper-bounded subsets",
      text="A real number system is a totally ordered field R such that every nonempty A⊆R bounded above has a least upper bound in R. It is characterized up to ordered-field isomorphism, not by literal equality of underlying sets.",
      reason="Use the independently read Axiomatic Definition of ProofWiki Real Number: a Dedekind-complete totally ordered field. The page's opening 'rationals plus irrationals' description explicitly admits it is circular and is rejected. Alternate Cauchy-sequence and cut models are not silently identified as equal sets.",
      locator="https://proofwiki.org/wiki/Definition%3AReal_Number")
]
def run(root):
 w=Workspace(root)
 b=json.loads((w.root/"state/baseline.json").read_text(encoding="utf-8"))
 if b.get("mode")!="second_wave" or any(w.state(s).get("sealed") for s in
      ("sources","terms","observations","meanings","relations")):
  raise PipelineError("Only unsealed independent Wave 2 can be reviewed")
 acquisition=w.root/"state/wave2_real_source_batch_45.json"
 if not acquisition.exists():
  raise PipelineError("Four source-specific real/order observations not committed")
 source=json.loads(acquisition.read_text(encoding="utf-8"))
 if (source.get("terms_after")!=388 or source.get("observations_after")!=811
     or not source.get("real_definition_circular_original_lead_rejected")
     or not source.get("ordered_field_distinct_from_complete_ordered_field")
     or source.get("links_preserved")!=659):
  raise PipelineError("Axiomatic scope/independent provenance not verified")
 if any(len(w.records(s))!=n for s,n in
    (("sources",9),("terms",388),("observations",811),("relations",659))):
  raise PipelineError("Source or screened relation baseline changed")
 prev=w.records("meanings")
 if len(prev) not in (487,490):
  raise PipelineError("Historical mathematical meaning baseline unexpected")
 terms,observ=w.records("terms"),w.records("observations")
 candidates=[];reviews=[]
 for item in SPECS:
  tid="term.wave2.real45."+item["slug"]
  oid="obs.wave2.real45."+item["slug"]
  t=terms.get(tid);o=observ.get(oid)
  if (not t or not o or t["locator"]!=item["locator"] or
      o["term_id"]!=tid or o["locator"]!=item["locator"] or
      o["record_kind"]!="paraphrase" or o["human_verified"] is not False):
   raise PipelineError("Unverified source of real/order mathematical candidate "+item["key"])
  if len(item["reason"])<185 or len(item["text"])<165:
   raise PipelineError("Mathematical source scope/reason insufficient "+item["key"])
  mid="meaning.wave2.real45."+item["key"]
  fid="form.wave2.real45."+item["key"]
  candidates.append({"id":mid,"term_group_id":"wave2.real45."+item["key"],
    "display_term":item["term"],"context":item["context"],"term_ids":[tid],
    "editorial_status":"individually_screened_candidate_pending_revision",
    "human_verified":False,
    "formulations":[{"id":fid,"text":item["text"],"evidence_ids":[oid],
        "review_state":"candidate","human_verified":False}]})
  reviews.append({"meaning_id":mid,"formulation_id":fid,"source_evidence_id":oid,
    "source_url":item["locator"],"mathematical_reason":item["reason"],
    "reviewed_by":"assistant_independent_real_order_math_review_2026_10_20",
    "decision":"individually_source_scoped_definition_screened",
    "human_verified":False})
 def store(path,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  data="".join(canonical(r)+"\n" for r in rows)
  if path.exists() and path.read_text(encoding="utf-8")!=data:
   raise PipelineError("Conflicting previous screened real mathematical evidence")
  path.write_text(data,encoding="utf-8")
  return path
 incoming=store(w.root/"intake/foundations_batch_46_real_meanings.jsonl",candidates)
 if len(prev)==487:
  w.ingest("meanings",incoming,batch_size=3)
 else:
  for c in candidates:
   m=prev.get(c["id"])
   if m is None or m["formulations"][0]["text"]!=c["formulations"][0]["text"]:
    raise PipelineError("Previously added real meaning conflicts")
 for c,r in zip(candidates,reviews):
  m=w.records("meanings")[c["id"]];f=m["formulations"][0]
  if f["review_state"]=="candidate":
   amended=dict(m)
   amended["formulations"]=[dict(f,review_state="screened",human_verified=False,
      source_screened_by=r["reviewed_by"])]
   amended["editorial_status"]="source_scoped_mathematical_formulation_screened"
   amended["editorial_screening_reason"]=r["mathematical_reason"]
   amended["human_verified"]=False
   apply_revision(w.root,{
     "event_id":"revision.wave2.real46."+c["id"].split(".")[-1]+".screen01",
     "stage":"meanings","record_id":c["id"],"before_digest":digest(m),
     "editor":r["reviewed_by"],"reason":r["mathematical_reason"],
     "operation":"replace","replacement":amended})
  elif f["review_state"]!="screened" or m.get("editorial_screening_reason")!=r["mathematical_reason"]:
   raise PipelineError("Prior mathematically screened ordered field conflicts")
 store(w.root/"wave2/real_meaning_individual_review_batch_46.jsonl",reviews)
 meanings=w.records("meanings")
 formids={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
 if (len(meanings)!=490 or len(formids)!=502 or
     any(f["review_state"]!="screened" for m in meanings.values() for f in m["formulations"])):
  raise PipelineError("Unexpected real/math screened meaning cardinality")
 ledger=w.root/"state/wave2_formulation_reviews.jsonl"
 earlier=jsonl(ledger)
 historic=w.root/"state/wave2_formulation_reviews_snapshot_499_before_real46.jsonl"
 if len(earlier)==499:
  if len({x["formulation_id"] for x in earlier})!=499 or {rid for x in earlier for rid in x["relation_ids"]}!=set(w.records("relations")):
   raise PipelineError("Lost original 499 independently reviewed mathematical formulations")
  before=ledger.read_text(encoding="utf-8")
  if historic.exists() and historic.read_text(encoding="utf-8")!=before:
   raise PipelineError("Historical 499-review snapshot conflicts")
  historic.write_text(before,encoding="utf-8")
  atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_499_before_real46.json",{
    "review_count":499,"screened_links":659,
    "sha256":hashlib.sha256(before.encode("utf-8")).hexdigest(),
    "human_peer_verified":False})
  d=digest(list(meanings.values()))
  incoming=[dict(x,meaning_catalog_digest=d) for x in earlier]
  for c in candidates:
   incoming.append({"formulation_id":c["formulations"][0]["id"],"meaning_id":c["id"],
     "meaning_catalog_digest":d,"decision":"needs_review","relation_ids":[],
     "original_wave1_disposition":None,"source":"independent_real_axiomatic_source_review",
     "editorial_reason":"Individually screened real/order definition requires separate non-circular mathematical prerequisite review.",
     "reviewed_by":None,"human_verified":False})
  atomic_jsonl(ledger,sorted(incoming,key=lambda x:x["formulation_id"]))
 elif len(earlier)==502:
  if not historic.exists() or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in earlier):
   raise PipelineError("Cannot certify previously screened 502-row review catalog")
 else:
  raise PipelineError("Unexpected historical formulation review count")
 history=jsonl(historic);now=jsonl(ledger);idx={r["formulation_id"]:r for r in now}
 if len(history)!=499 or len(now)!=502 or len(idx)!=502:
  raise PipelineError("Real source review migration missing historical review")
 for old in history:
  current=idx.get(old["formulation_id"])
  if not current or any(current.get(k)!=v for k,v in old.items() if k!="meaning_catalog_digest"):
   raise PipelineError("Historical formulation review changed without individual correction")
 if {rid for r in now for rid in r["relation_ids"]}!=set(w.records("relations")):
  raise PipelineError("Screened links no longer covered by individual reviews")
 check_cycles(meanings,w.records("relations"))
 decisions=dict(Counter(r["decision"] for r in now))
 if decisions!={"linked":494,"no_supported_target":5,"needs_review":3}:
  raise PipelineError("Incorrect new context review dispositions "+str(decisions))
 state=w.state("meanings")
 state.update(total=490,record_digest=digest(list(meanings.values())),
     screened_new_formulations=71,stage4_review_complete=False)
 atomic_json(w.root/"state/meanings.json",state)
 report={"phase":"three_axiomatic_ordered_real_meanings_individually_source_screened",
  "screened_meanings":490,"reviewed_formulations":502,
  "previous_499_review_dispositions_preserved":True,
  "previous_659_links_preserved":True,"new_formulations_pending_dependency_review":3,
  "dedekind_completeness_not_equated_to_metric_completeness":True,
  "ordered_field_not_assumed_complete":True,
  "circular_real_number_paraphrase_excluded":True,
  "production_corpus_consulted":False,
  "human_peer_verified":False,"all_stages_unsealed":True,
  "next":"Individually screen ordered field→field, complete real field→order/least upper bound, real absolute value→real-number structure, with exact source anchors and historic override events."}
 atomic_json(w.root/"state/wave2_real_meaning_screen_batch_46.json",report)
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--workspace",type=Path,required=True)
 a=p.parse_args()
 print(json.dumps(run(a.workspace),indent=2))
if __name__=="__main__":main()
