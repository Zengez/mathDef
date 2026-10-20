"""Batch116: four independently justified contexts, six sourced formulations.

Orbit and partition each have two equivalent definitions in ONE mathematical
meaning; stabilizer and pushforward are separate contexts. Old review decisions
and source-specific relations are snapshotted unchanged.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/group_action_measure_partition_source_batch115_2026-10-20.jsonl"
BASE={"sources":14,"terms":457,"observations":912,"meanings":564,"relations":794}
AFTER=dict(BASE,meanings=568)
SPECS=(
 ("orbit-group-action","group-orbit","Orbit of an element under a left group action"),
 ("stabilizer-group-action","group-stabilizer","Point stabilizer of a specified left group action"),
 ("pushforward-measure","measure-pushforward","Pushforward of a nonnegative measure by a measurable map"),
 ("set-partition","set-partition","Partition into nonempty disjoint blocks, arbitrary base set")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    data="".join(canonical(row)+"\n" for row in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=data:
        raise PipelineError("Previously source-screened individual mathematical record changed")
    path.write_text(data,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Independent unsealed Wave2 required")
    current={k:len(w.records(k)) for k in BASE}
    if current not in (BASE,AFTER):
        raise PipelineError("Unexpected independent source registry "+str(current))
    source_report=json.loads((w.root/"state/wave2_group115_source_intake.json").read_text())
    if (source_report.get("new_source_terms")!=4 or source_report.get("new_observations")!=6
        or source_report.get("new_mathematical_meanings")!=0 or not source_report.get("empty_set_partition_allowed")):
        raise PipelineError("Verified source-only evidence from Batch115 is missing")
    research={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    if len(research)!=4:
        raise PipelineError("Four individually reviewed mathematical sources missing")
    termdb=w.records("terms");obsdb=w.records("observations")
    additions=[];reviews=[]
    for key,suffix,scope in SPECS:
        r=research[key];tid="term.wave2.group115."+key
        if tid not in termdb or termdb[tid]["locator"]!=r["source"] or r["production_corpus_consulted"]:
            raise PipelineError("Mathematical term lacks specific direct-source evidence "+key)
        context=r["contexts"][0];forms=context["forms"];reason=r["review"]
        if len(reason)<280 or len(forms)!=(2 if key in ("orbit-group-action","set-partition") else 1):
            raise PipelineError("Unexpected mathematically sourced equivalent variants "+key)
        if key=="orbit-group-action":
            if "equivalence class" not in forms[1]["text"] or "g·x" not in forms[0]["text"]:
                raise PipelineError("Orbit forms not genuinely equivalent under a group action")
            reason+=" Both source forms identify the same orbit; the equivalence class relation must be action-induced."
        if key=="stabilizer-group-action":
            if "g·x=x" not in forms[0]["text"]:
                raise PipelineError("Group stabilizer fixing-point criterion missing")
            reason+=" Subgroup closure is a theorem derived from the action, not an additional assumption."
        if key=="pushforward-measure":
            if "μ(f⁻¹(B))" not in forms[0]["text"] or "measurable" not in forms[0]["text"]:
                raise PipelineError("Measurable preimage pushforward identity missing")
            reason+=" The pushed measure is on the target σ-algebra, and target sets are pulled back."
        if key=="set-partition":
            if "⋃" not in forms[0]["text"] or "exactly one" not in forms[1]["text"]:
                raise PipelineError("Set-partition equivalence and total-cover hypotheses missing")
            reason+=" For the empty base set the empty collection is admissible and unique."
        mid="meaning.wave2.group116."+suffix
        frows=[]
        for i,f in enumerate(forms,1):
            oid=f"obs.wave2.group115.{key}.{i:02d}"
            o=obsdb.get(oid)
            if not o or o["term_id"]!=tid or o["locator"]!=r["source"] or o["text"]!=f["text"]:
                raise PipelineError("Individual source text and citation mismatch "+key+"/"+str(i))
            fid="form.wave2.group116."+suffix+("."+str(i) if len(forms)>1 else "")
            frows.append({"id":fid,"text":f["text"],"evidence_ids":[oid],
              "review_state":"screened","human_verified":False,
              "mathematical_review_reason":reason,
              "source_screened_by":"assistant_independent_group_measure_partition_mathematical_screen_2026_10_20"})
            reviews.append({"review_id":"review.wave2.group116."+suffix+("."+str(i) if len(forms)>1 else ""),
              "meaning_id":mid,"formulation_id":fid,"source_observation_id":oid,"source_locator":r["source"],
              "mathematical_reason":reason,"decision":"mathematically_screened_pending_individual_link_review",
              "human_verified":False,"production_corpus_used":False})
        additions.append({"id":mid,"term_group_id":"wave2.group116."+key,"display_term":r["term"],
          "context":scope,"term_ids":[tid],"formulations":frows,
          "editorial_status":"source_scoped_individually_mathematically_screened",
          "editorial_screening_reason":reason,"human_verified":False})
    if len(additions)!=4 or len(reviews)!=6 or sum(len(m["formulations"]) for m in additions)!=6:
        raise PipelineError("Four contexts and six independently sourced formulations required")
    store(w.root/"wave2/group116_individual_mathematical_reviews.jsonl",reviews)
    intake=store(w.root/"intake/group116_meanings.jsonl",additions)
    previous_ms=w.records("meanings")
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    before=jsonl(ledger)
    if len(before) not in (594,600) or len({r["formulation_id"] for r in before})!=len(before):
        raise PipelineError("All 594 previous reviewed formulation decisions must be present")
    if {id for r in before for id in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("All original 794 direct prerequisites must have review attribution")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_594_before_group116.jsonl"
    if len(previous_ms)==564:
        if len(before)!=594 or any(r["meaning_catalog_digest"]!=digest(list(previous_ms.values())) for r in before):
            raise PipelineError("Historical form review catalog digest changed")
        text=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=text:
            raise PipelineError("Historical 594-review snapshot changed")
        archive.write_text(text,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_594_before_group116.json",{
          "rows":594,"prior_links":794,"sha256":hashlib.sha256(text.encode("utf-8")).hexdigest(),
          "human_peer_verified":False})
        w.ingest("meanings",intake,batch_size=4)
    ms=w.records("meanings")
    if len(ms)!=568 or any(ms.get(m["id"])!=m for m in additions):
        raise PipelineError("Four mathematically screened contextual meanings missing")
    historical=jsonl(archive)
    if len(historical)!=594 or len({r["formulation_id"] for r in historical})!=594:
        raise PipelineError("Original individual reviews not archived")
    d=digest(list(ms.values()))
    expected=[dict(r,meaning_catalog_digest=d) for r in historical]
    for r in reviews:
        expected.append({"formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
          "meaning_catalog_digest":d,"decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,"source":"independent_group_measure_mathematical_screen_batch116",
          "editorial_reason":"Individual sourced formulation reviewed mathematically, prerequisites separate pending work.",
          "reviewed_by":None,"human_verified":False})
    if len(before)==600:
        if {r["formulation_id"]:r for r in before}!={r["formulation_id"]:r for r in expected}:
            raise PipelineError("Previously screened mathematical batch would change on rerun")
    else:
        atomic_jsonl(ledger,sorted(expected,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);index={r["formulation_id"]:r for r in final}
    if len(final)!=600 or len(index)!=600:
        raise PipelineError("600 distinct individual dispositions required")
    for r in historical:
        n=index[r["formulation_id"]]
        if any(n.get(k)!=v for k,v in r.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Old mathematical source review decision mutated")
    if dict(Counter(r["decision"] for r in final))!={"linked":588,"no_supported_target":6,"needs_review":6}:
        raise PipelineError("New pending forms or prior completed decisions have incorrect totals")
    if {id for r in final for id in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Existing reviewed link references lost")
    check_cycles(ms,w.records("relations"))
    state=w.state("meanings")
    state.update(total=568,record_digest=d,screened_new_formulations=169,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={"batch":116,"screened_meanings":568,"reviewed_formulations":600,
      "new_mathematical_contexts":4,"new_source_specific_formulations":6,
      "prior_594_formulation_decisions_preserved":True,"prior_794_relations_preserved":True,
      "orbit_equivalent_forms_one_meaning":True,"partition_equivalent_forms_one_meaning":True,
      "stabilizer_action_dependency_separate":True,"pushforward_requires_measurable_map":True,
      "held_directional_source_claim_unpromoted":True,"pending_individual_form_link_reviews":6,
      "all_stages_unsealed":True,"human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch117 individually source-screen orbit/stabilizer/action, partition/mapping, pushforward/measure/measurable space prerequisites and preserve historic graph."}
    atomic_json(w.root/"state/wave2_group116_meaning_screen.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
