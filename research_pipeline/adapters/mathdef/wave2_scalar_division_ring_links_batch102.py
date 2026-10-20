"""Batch 102: individually screen scalar division-ring prerequisites.

Preserves the previous 742 links and all 566 formulation identities, with
explicit append-only extension events for two earlier norm definitions.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
BASE={"sources":14,"terms":437,"observations":877,"meanings":541}
URI="https://proofwiki.org/wiki/Definition%3A"
DIV=URI+"Division_Ring"
SCALAR=URI+"Norm_on_Division_Ring"
NORMED=URI+"Normed_Division_Ring"
LEFT=URI+"Vector_Space_over_Division_Ring/Left_Vector_Space"
RIGHT=URI+"Vector_Space_over_Division_Ring/Right_Vector_Space"
GENVEC=URI+"Norm_on_Vector_Space"
NORMVEC=URI+"Normed_Vector_Space"
RING=URI+"Ring_%28Abstract_Algebra%29"
MOD=URI+"Unitary_Module_over_Ring"
REALS=URI+"Real_Number"
TARGET=lambda key:"meaning.wave2.scalar101."+key
F=lambda key:"form.wave2.scalar101."+key
GEN="form.wave2.analysis98.norm-over-normed-division-ring"
NV="form.wave2.analysis98.normed-vector-space"
EDGES=(
 ("01",F("division-ring"),"meaning.wave2.foundation.associative-ring-identity-optional",
  "associative unital ring",DIV,RING,
  "The source's associative division ring has abelian additive group, associative multiplication and distributivity, hence satisfies all axioms of the independently screened general associative ring. Its identity and inverse conditions are additional restrictions; commutativity is not assumed."),
 ("02",F("division-ring-multiplicative-norm"),TARGET("division-ring"),
  "division ring",SCALAR,DIV,
  "The multiplicative norm is defined on a genuine associative division ring, which supplies scalar multiplication, additive inverses and two-sided inverses. The real-valued function is extra structure rather than a replacement for the underlying ring axioms."),
 ("03",F("division-ring-multiplicative-norm"),"meaning.wave2.real45.complete-ordered-real-field",
  "ℝ_{≥0}",SCALAR,REALS,
  "The source's norm has nonnegative real outputs and the triangle inequality; the independently defined ordered real field supplies this ordered numerical codomain. This does not impose a completeness condition on the division ring itself."),
 ("04",F("normed-division-ring"),TARGET("division-ring"),
  "division ring",NORMED,DIV,
  "A normed division ring explicitly presupposes an associative unital division ring. The source page lacks bibliographic citations, a caveat preserved on the screened meaning; the independent underlying division-ring source specifies the multiplication and inverse axioms."),
 ("05",F("normed-division-ring"),TARGET("division-ring-multiplicative-norm"),
  "multiplicative norm",NORMED,SCALAR,
  "The source-specific normed division ring is an associative division ring equipped with the separately source-defined exact multiplicative scalar norm. We do not substitute the weaker submultiplicative norm on an arbitrary ring."),
 ("06",F("left-vector-over-division-ring"),"meaning.wave2.module94.unital-left-module",
  "left D-vector space",LEFT,MOD,
  "The left vector space obeys both distribution axioms, (ab)v=a(bv), and 1_Dv=v; these are precisely the laws of a unital left D-module already screened. Requiring D to be a division ring is additional scalar structure, and is not forced on generic unital modules."),
 ("07",F("left-vector-over-division-ring"),TARGET("division-ring"),
  "division ring",LEFT,DIV,
  "The left scalar action D×V→V requires the separately screened associative unital division ring. The source does not demand that D be commutative; reversing the scalar order is not a valid general conversion to a right vector space."),
 ("08",F("right-vector-over-division-ring"),"meaning.wave2.module94.unital-right-module",
  "right D-vector space",RIGHT,MOD,
  "The right vector space obeys (va)b=v(ab), both distributivities and v1_D=v, matching the separately screened unital right module structure. The noncommutative division-ring condition is an added restriction rather than ordinary field-vector equivalence."),
 ("09",F("right-vector-over-division-ring"),TARGET("division-ring"),
  "division ring",RIGHT,DIV,
  "The right action V×D→V requires an associative division ring and its right scalar multiplication order. ProofWiki explicitly warns that a left action over a noncommutative D is not automatically a right action over the same D."),
 ("10",GEN,TARGET("normed-division-ring"),
  "normed division ring",GENVEC,NORMED,
  "The previously screened generic vector norm explicitly presupposes a normed scalar division ring. The newly independent source-screened scalar structure defines this requirement, preserving its earlier real-output link and the derived source's missing-bibliography warning."),
 ("11",GEN,TARGET("left-vector-over-division-ring"),
  "∥av∥",GENVEC,LEFT,
  "The generic norm axioms explicitly write ∥av∥=|a|_D∥v∥, which uses a left D×V scalar action. Its source-screened left division-ring vector space supplies the exact orientation. This link is not silently applied to right division-ring vector spaces."),
 ("12",NV,TARGET("normed-division-ring"),
  "normed division ring",NORMVEC,NORMED,
  "The previously screened normed vector space assumes a normed division ring as its scalar structure, whose newly independently screened definition supplies the scalar norm; the already reviewed underlying vector norm link is retained. Its wording does not fix a new right-action norm convention.")
)
PREVIOUS={GEN,NV}

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Previously reviewed scalar division-ring links changed")
    path.write_text(body,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in (*BASE,"relations")):
        raise PipelineError("Requires unsealed independent Wave 2")
    if {s:len(w.records(s)) for s in BASE}!=BASE:
        raise PipelineError("Missing Batch101 reviewed mathematical meanings")
    sr=json.loads((w.root/"state/wave2_scalar101_meaning_screen.json").read_text())
    if sr.get("screened_meanings")!=541 or sr.get("reviewed_formulations")!=566 or not sr.get("uncited_derived_pair_page_caveat_preserved"):
        raise PipelineError("Source-scoped mathematical screen missing")
    ms=w.records("meanings");obs=w.records("observations")
    forms={f["id"]:(m,f) for m in ms.values() for f in m["formulations"]}
    if len(forms)!=566:
        raise PipelineError("Expected 566 screened prior formulations")
    oldrel=w.records("relations")
    if len(oldrel) not in (742,754):
        raise PipelineError("Concurrent relation catalog mismatch")
    base={i:r for i,r in oldrel.items() if not i.startswith("rel.wave2.scalar102.")}
    if len(base)!=742:
        raise PipelineError("All prior 742 relations required")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    prev=jsonl(ledger);prior={r["formulation_id"]:r for r in prev}
    if (len(prev)!=566 or len(prior)!=566 or
        any(r["meaning_catalog_digest"]!=digest(list(ms.values())) for r in prev) or
        {id for r in prev for id in r["relation_ids"]}!=set(oldrel)):
        raise PipelineError("Complete current 566-review history required")
    checked=[]
    for n,fid,target,phrase,sourceurl,targeturl,reason in EDGES:
        if fid not in forms or target not in ms:
            raise PipelineError("Missing independent prerequisite endpoint "+n)
        m,f=forms[fid]
        sources=f.get("evidence_ids",[])
        if (f["review_state"]!="screened" or len(sources)!=1 or
            sources[0] not in obs or obs[sources[0]]["locator"]!=sourceurl or
            locator(ms[target],obs)!=targeturl or phrase not in f["text"] or
            len(reason)<150):
            raise PipelineError("Exact source phrase or target evidence unavailable: "+n)
        checked.append({
          "id":"rel.wave2.scalar102."+n,"from_formulation":fid,"target_meaning":target,
          "relation_type":"definition_uses","review_state":"screened",
          "source_phrase":phrase,"source_locator":sourceurl,
          "target_locator":targeturl,"editorial_reason":reason,
          "reviewed_by":"assistant_independent_scalar_division_ring_dependency_screen_2026_10_20",
          "human_verified":False
        })
    newforms={F(key) for key in ("division-ring","division-ring-multiplicative-norm","normed-division-ring",
        "left-vector-over-division-ring","right-vector-over-division-ring")}
    if len(checked)!=12 or {r["from_formulation"] for r in checked}!=newforms|PREVIOUS:
        raise PipelineError("All five new and two historical reviews require exact links")
    check_cycles(ms,{**base,**{r["id"]:r for r in checked}})
    snap=w.root/"state/wave2_formulation_reviews_snapshot_566_before_scalar102.jsonl"
    if len(oldrel)==742:
        if any(prior[fid]["decision"]!="needs_review" or prior[fid]["relation_ids"] for fid in newforms):
            raise PipelineError("Previous five new formulation reviews already changed")
        if any(prior[fid]["decision"]!="linked" or not prior[fid]["relation_ids"] for fid in PREVIOUS):
            raise PipelineError("Historical already-linked norm reviews missing")
        olddata=ledger.read_text(encoding="utf-8")
        if snap.exists() and snap.read_text(encoding="utf-8")!=olddata:
            raise PipelineError("Historical 566-review snapshot differs")
        snap.write_text(olddata,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_566_before_scalar102.json",{
            "rows":566,"existing_links":742,"sha256":hashlib.sha256(olddata.encode()).hexdigest(),
            "human_peer_verified":False})
    old=jsonl(snap);older={r["formulation_id"]:r for r in old}
    if len(old)!=566 or len(older)!=566:
        raise PipelineError("Missing historical 566 review snapshot")
    events=[]
    for fid in sorted(PREVIOUS):
        added=[x["id"] for x in checked if x["from_formulation"]==fid]
        previous=older[fid]
        if not added or not previous["relation_ids"]:
            raise PipelineError("Existing norm links must not be replaced")
        events.append({
          "event_id":"scalar102.extend-"+fid.replace(".","-"),
          "formulation_id":fid,"previous_review_digest":digest(previous),
          "previous_decision":"linked","new_decision":"linked",
          "previous_relation_ids":previous["relation_ids"],
          "additional_relation_ids":added,
          "reason":"Newly independently sourced scalar ring foundations now support additional noncircular prerequisites; preserve the historic reviewed real-valued/norm prerequisites and source review reason.",
          "human_verified":False,"production_corpus_used":False})
    store(w.root/"events/scalar102_norm_link_extension_events.jsonl",events)
    store(w.root/"wave2/scalar102_individual_prerequisite_reviews.jsonl",checked)
    intake=store(w.root/"intake/scalar102_links.jsonl",checked)
    if len(oldrel)==742:
        w.ingest("relations",intake,batch_size=12)
    nowrel=w.records("relations")
    if len(nowrel)!=754 or any(nowrel.get(x["id"])!=x for x in checked):
        raise PipelineError("All new screened links were not committed")
    check_cycles(ms,nowrel)
    updated=[]
    for previous in old:
        r=dict(previous)
        fid=r["formulation_id"]
        if fid in newforms|PREVIOUS:
            added=[x["id"] for x in checked if x["from_formulation"]==fid]
            if not added:
                raise PipelineError("Required reviewed link set empty")
            r["relation_ids"]=previous["relation_ids"]+added
            r["decision"]="linked"
            r["reviewed_by"]="assistant_independent_scalar_division_ring_dependency_screen_2026_10_20"
            r["source"]="independent_scalar_division_ring_dependency_review_batch102"
            r["editorial_reason"]="Exact source-supported prerequisite target and action orientation individually screened; previous dependency links retained."
            if fid in PREVIOUS:
                event=next(e for e in events if e["formulation_id"]==fid)
                r["previous_review_digest"]=digest(previous)
                r["link_extension_event_id"]=event["event_id"]
        updated.append(r)
    if len(oldrel)==754:
        if {r["formulation_id"]:r for r in prev}!={r["formulation_id"]:r for r in updated}:
            raise PipelineError("Rerun changed a previously completed individual review")
    else:
        atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);lookup={r["formulation_id"]:r for r in final}
    if len(final)!=len(lookup)!=566:
        raise PipelineError("566 complete link decisions required")
    for fid,entry in older.items():
        if fid not in newforms|PREVIOUS and lookup[fid]!=entry:
            raise PipelineError("Unrelated mathematical review mutated")
    for event in events:
        assert all(x in lookup[event["formulation_id"]]["relation_ids"] for x in event["previous_relation_ids"])
    if {i for r in final for i in r["relation_ids"]}!=set(nowrel):
        raise PipelineError("Some screened link lacks an individual reviewing disposition")
    if dict(Counter(r["decision"] for r in final))!={"linked":560,"no_supported_target":6}:
        raise PipelineError("Unexpected final review decision counts")
    report={
      "batch":102,"screened_contextual_meanings":541,
      "reviewed_formulations":566,"screened_relationships":754,
      "new_individually_source_justified_links":12,
      "all_742_prior_links_preserved":True,
      "all_559_unrelated_reviews_preserved":True,
      "two_previous_norm_formulation_reviews_extended_with_events":True,
      "noncommutative_left_right_scope_preserved":True,
      "multiplicative_norm_vs_submultiplicative_ring_norm_distinct":True,
      "source_bibliography_warning_preserved":True,
      "dependency_graph_has_cycles":False,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Further cross-source evidence for noncommutative multiplicative scalar norms and substantially broader non-linear discovery; avoid recursion into assumed completeness."
    }
    atomic_json(w.root/"state/wave2_scalar102_link_review.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
