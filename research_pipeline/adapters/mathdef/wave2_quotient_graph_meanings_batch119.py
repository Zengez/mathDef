"""Batch119 mathematical screening: normal/quotient groups, graph isomorphism, analytic OGF."""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,atomic_json,digest
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles
ROOT="research_pipeline/experiments/reconstruction-v2-independent"
DOSSIER="wave2/quotient_graph_generating_source_batch118_2026-10-20.jsonl"
BASE={"sources":14,"terms":461,"observations":919,"meanings":568,"relations":803}
AFTER=dict(BASE,meanings=572)
SPECS=(
 ("normal-subgroup","normal-subgroup","Normal subgroup of a group; three equivalent group-theoretic criteria"),
 ("quotient-group","quotient-group","Quotient group of G by normal subgroup N with coset product"),
 ("graph-isomorphism","simple-graph-isomorphism","Isomorphism between simple undirected graphs preserving and reflecting adjacency"),
 ("ordinary-generating-function","ordinary-real-ogf","Convergent ordinary generating function of a real sequence on its real convergence domain")
)
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Prior source-specific mathematical screening differs")
    path.write_text(body,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(k).get("sealed") for k in BASE):
        raise PipelineError("Independent unsealed Wave2 required")
    current={k:len(w.records(k)) for k in BASE}
    if current not in (BASE,AFTER):raise PipelineError("Source-only research not at Batch118 checkpoint")
    report=json.loads((w.root/"state/wave2_quot118_source_intake.json").read_text())
    held=jsonl(w.root/"wave2/quot118_quarantined_source_claims.jsonl")
    if report.get("new_terms")!=4 or report.get("new_source_observations")!=7 or len(held)!=1 or held[0]["observation_id"]!="obs.wave2.quot118.graph-isomorphism.02":
        raise PipelineError("Source research or graph source quarantine not verified")
    rows={r["key"]:r for r in jsonl(w.root/DOSSIER)}
    terms=w.records("terms");obsdb=w.records("observations")
    if len(rows)!=4:raise PipelineError("Four direct source topics missing")
    additions=[];individual=[]
    for key,suffix,context_label in SPECS:
        r=rows[key];tid="term.wave2.quot118."+key
        if terms.get(tid,{}).get("locator")!=r["source"] or r["production_corpus_consulted"]:
            raise PipelineError("Independent source/term locator mismatch "+key)
        c=r["contexts"][0]
        if c.get("held"):raise PipelineError("Unsafe graph observation cannot be promoted")
        fs=c["forms"];reason=r["review"]
        if key=="normal-subgroup":
            if len(fs)!=3 or "gN=Ng" not in fs[0]["text"] or "gNg⁻¹=N" not in fs[1]["text"] or "gNg⁻¹⊆N" not in fs[2]["text"]:
                raise PipelineError("Three equivalent normality criteria absent")
            reason+=" All three source formulations describe the SAME normal subgroup, provided normality is tested for all group elements."
        elif key=="quotient-group":
            if len(fs)!=1 or "normal subgroup" not in fs[0]["text"] or "(ab)N" not in fs[0]["text"]:
                raise PipelineError("Quotient product normality prerequisite absent")
            reason+=" An arbitrary quotient set does not automatically inherit a group multiplication."
        elif key=="graph-isomorphism":
            if len(fs)!=1 or "if and only if" not in fs[0]["text"] or "bijection" not in fs[0]["text"]:
                raise PipelineError("Adjacency reflection and preservation required for isomorphism")
            reason+=" The deficient one-way implication is held as source evidence only, not an approved meaning."
        elif key=="ordinary-generating-function":
            if len(fs)!=1 or "converges" not in fs[0]["text"] or "G_A:D→ℝ" not in fs[0]["text"]:
                raise PipelineError("Analytic generating function and explicit convergence domain required")
            reason+=" Convergent real-valued power series is not identified with an unrestricted formal series."
        mid="meaning.wave2.quot119."+suffix
        formulations=[]
        for i,f in enumerate(fs,1):
            oid=f"obs.wave2.quot118.{key}.{i:02d}"
            ob=obsdb.get(oid)
            if not ob or ob["term_id"]!=tid or ob["locator"]!=r["source"] or ob["text"]!=f["text"] or oid==held[0]["observation_id"]:
                raise PipelineError("Source-specific individually screened observation invalid "+oid)
            fid="form.wave2.quot119."+suffix+("."+str(i) if len(fs)>1 else "")
            formulations.append({"id":fid,"text":f["text"],"evidence_ids":[oid],
              "review_state":"screened","human_verified":False,
              "mathematical_review_reason":reason,
              "source_screened_by":"assistant_independent_group_graph_generating_math_review_2026_10_20"})
            individual.append({"review_id":"review.wave2.quot119."+suffix+("."+str(i) if len(fs)>1 else ""),
              "meaning_id":mid,"formulation_id":fid,"source_observation_id":oid,
              "source_locator":r["source"],"mathematical_reason":reason,
              "decision":"mathematically_screened_pending_individual_dependency_review",
              "human_verified":False,"production_corpus_used":False})
        additions.append({"id":mid,"term_group_id":"wave2.quot119."+key,
           "display_term":r["term"],"context":context_label,
           "term_ids":[tid],"formulations":formulations,
           "editorial_status":"source_scoped_individually_mathematically_screened",
           "editorial_screening_reason":reason,"human_verified":False})
    if len(additions)!=4 or len(individual)!=6 or len(additions[0]["formulations"])!=3:
        raise PipelineError("Expected four contexts and six accepted source forms")
    store(w.root/"wave2/quot119_individual_mathematical_reviews.jsonl",individual)
    intake=store(w.root/"intake/quot119_meanings.jsonl",additions)
    previous_ms=w.records("meanings");ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    previous=jsonl(ledger)
    if len(previous) not in (600,606) or len({r["formulation_id"] for r in previous})!=len(previous):
        raise PipelineError("600 historical individual formulation reviews missing")
    if {e for r in previous for e in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("803 preceding direct link dispositions missing")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_600_before_quot119.jsonl"
    if len(previous_ms)==568:
        if len(previous)!=600 or any(r["meaning_catalog_digest"]!=digest(list(previous_ms.values())) for r in previous):
            raise PipelineError("Prior screened meaning digest altered")
        old=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=old:
            raise PipelineError("Historic 600-form review archive differs")
        archive.write_text(old,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_600_before_quot119.json",
            {"rows":600,"prior_links":803,"sha256":hashlib.sha256(old.encode("utf-8")).hexdigest(),"human_peer_verified":False})
        w.ingest("meanings",intake,batch_size=4)
    ms=w.records("meanings")
    if len(ms)!=572 or any(ms.get(m["id"])!=m for m in additions):
        raise PipelineError("Expected four added mathematically screened contexts")
    history=jsonl(archive)
    if len(history)!=600 or len({r["formulation_id"] for r in history})!=600:
        raise PipelineError("Prior 600 mathematical reviews absent")
    d=digest(list(ms.values()))
    expected=[dict(r,meaning_catalog_digest=d) for r in history]
    for r in individual:
        expected.append({"formulation_id":r["formulation_id"],"meaning_id":r["meaning_id"],
          "meaning_catalog_digest":d,"decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,"source":"independent_normal_graph_ogf_screen_batch119",
          "editorial_reason":"Source-scoped mathematical formulation screened; prerequisite review pending.",
          "reviewed_by":None,"human_verified":False})
    if len(previous)==606:
        if {r["formulation_id"]:r for r in previous}!={r["formulation_id"]:r for r in expected}:
            raise PipelineError("Rerun would alter prior mathematical reviews")
    else:
        atomic_jsonl(ledger,sorted(expected,key=lambda r:r["formulation_id"]))
    final=jsonl(ledger);ix={r["formulation_id"]:r for r in final}
    if len(final)!=606 or len(ix)!=606:raise PipelineError("606 reviewed formulations expected")
    for p in history:
        now=ix[p["formulation_id"]]
        if any(now.get(k)!=v for k,v in p.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Unrelated reviewed formulation decision changed")
    if dict(Counter(r["decision"] for r in final))!={"linked":594,"no_supported_target":6,"needs_review":6}:
        raise PipelineError("Pending/new versus previous review decision mismatch")
    if held[0]["observation_id"] in {e for m in ms.values() for fm in m["formulations"] for e in fm["evidence_ids"]}:
        raise PipelineError("Unsafe graph source statement mathematically promoted")
    check_cycles(ms,w.records("relations"))
    state=w.state("meanings")
    state.update(total=572,record_digest=d,screened_new_formulations=175,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    result={"batch":119,"screened_meanings":572,"reviewed_formulations":606,
      "new_contextual_meanings":4,"new_formulations":6,
      "normal_subgroup_equivalent_three_formulations_grouped":True,
      "held_forward_only_graph_claim_unpromoted":True,
      "convergent_real_ogf_not_formal_series":True,"quotient_requires_normality":True,
      "previous_600_reviews_and_803_links_preserved":True,
      "six_formulations_await_individual_links":True,"all_stages_unsealed":True,
      "human_peer_verified":False,"production_corpus_used":False,
      "next":"Batch120 direct mathematics prerequisite review for all six formulations, without inferring group structure on arbitrary quotients."}
    atomic_json(w.root/"state/wave2_quot119_meaning_screen.json",result)
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
