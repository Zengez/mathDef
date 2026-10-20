"""Source-scoped Batch 71: preserve conflicting conventions and split equivalents.

Connectedness:
    Stacks explicitly excludes the empty space; this is a valid convention.
    ProofWiki allows it; retain BOTH meanings under the SAME displayed group.
Noetherian:
    Amend the already-screened Stacks first formulation to finite generation.
    Add three ProofWiki alternatives under that SAME existing meaning.
Every in-place edit is archived and versioned with immutable research evidence.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,jsonl,canonical,digest,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
RESEARCH="wave2/cross_domain_equivalence_audit_batch69_2026-10-20.jsonl"
BEFORE={"sources":14,"terms":410,"observations":841,"meanings":509,"relations":693}
AFTER=dict(BEFORE,meanings=510)
STACKS_CONN="meaning.ab260940ea9c523d.connected-topological-space"
NOETH="meaning.86b5d488b98c612f.noetherian-commutative-ring"
CONNECTED="meaning.wave2.variant71.connected-empty-allowed"
NOETH_FID="form.86b5d488b98c612f.noetherian-commutative-ring"
NOETH_FIRST="A commutative ring R with identity is Noetherian if every ideal of R is finitely generated."
NOETH_EXTRA=("ascending-chain-condition","maximal-condition","noetherian-as-module")
def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(x)+"\n" for x in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Changed previously archived independent review")
    path.write_text(body,encoding="utf-8")
    return path
def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in BEFORE):
        raise PipelineError("Requires unsealed independent Wave 2")
    counts={s:len(w.records(s)) for s in BEFORE}
    if counts not in (BEFORE,AFTER):
        raise PipelineError("Unexpected independent meaning inventory")
    meanings=w.records("meanings")
    original_connected=meanings.get(STACKS_CONN)
    noeth=meanings.get(NOETH)
    if not original_connected or not noeth or len(original_connected["formulations"])!=1:
        raise PipelineError("Historic independent semantic collision was not checked")
    if not original_connected["formulations"][0]["text"].startswith("A nonempty topological space"):
        raise PipelineError("Historical Stacks nonempty convention changed")
    old_noeth_form=noeth["formulations"][0]
    if old_noeth_form["id"]!=NOETH_FID or "Noetherian" not in old_noeth_form["text"]:
        raise PipelineError("Existing screened Noetherian Stacks meaning changed")
    dossiers={r["research_id"]:r for r in jsonl(w.root/RESEARCH)}
    conn=dossiers.get("wave2.batch69.connected-topological-space")
    noeth_research=dossiers.get("wave2.batch69.noetherian-ring")
    if (not conn or not noeth_research or len(conn["reviewed_variants"])!=3
        or len(noeth_research["reviewed_variants"])!=4
        or conn["production_corpus_consulted"] or noeth_research["production_corpus_consulted"]):
        raise PipelineError("No individually source-audited alternate definitions")
    observations=w.records("observations")
    for kind,n in (("connected",3),("noetherian",4)):
        for i in range(1,n+1):
            oid=f"obs.wave2.variant70.{kind}.{i:02d}"
            o=observations.get(oid)
            if not o or o["source_id"]!="src.proofwiki" or o["term_id"]!=f"term.wave2.variant70.{kind}":
                raise PipelineError("Original independently sourced alternative unavailable "+oid)
    conn_forms=[]
    for i,variant in enumerate(conn["reviewed_variants"],1):
        conn_forms.append({
           "id":f"form.wave2.variant71.connected.{i:02d}",
           "text":variant["text"],"review_state":"screened",
           "evidence_ids":[f"obs.wave2.variant70.connected.{i:02d}"],
           "mathematical_review_reason":conn["mathematical_review"]+" Scope: "+variant["mathematical_scope"],
           "source_screened_by":"assistant_independent_two_connectedness_conventions_review_2026_10_20",
           "human_verified":False
        })
    connected={
      "id":CONNECTED,
      "term_group_id":original_connected["term_group_id"],
      "display_term":original_connected["display_term"],
      "context":"General topology: connected by no nontrivial open separation, empty space included",
      "term_ids":["term.wave2.variant70.connected"],
      "editorial_status":"separately_source_screened_context_convention",
      "editorial_screening_reason":conn["mathematical_review"],
      "terminology_note":"ProofWiki permits the empty space to be connected. The distinct Stacks-sourced meaning under this heading explicitly excludes it. Both conventions remain available.",
      "formulations":conn_forms,"human_verified":False
    }
    original_noeth=dict(noeth)
    prev_form=old_noeth_form["text"]
    if len(noeth["formulations"]) not in (1,4):
        raise PipelineError("Unexpected Noetherian existing alternatives")
    old_saved={
       **{k:v for k,v in original_noeth.items() if k!="variant_refinement_note"},
       "term_ids":["term.86b5d488b98c612f"],
       "formulations":[{**old_noeth_form,"text":prev_form if len(noeth["formulations"])==1 else
                        "A commutative ring R is Noetherian if every ideal of R is finitely generated; equivalently, every ascending chain I_1⊆I_2⊆⋯ of ideals eventually stabilizes."}]
    }
    if not old_saved["formulations"][0]["text"].startswith("A commutative ring R is Noetherian"):
        raise PipelineError("Historical Noetherian form cannot be reproduced")
    first={**old_saved["formulations"][0],"text":NOETH_FIRST}
    supplemental=[]
    for n,j in enumerate((2,3,4),1):
        variant=noeth_research["reviewed_variants"][j-1]
        supplemental.append({
           "id":f"form.wave2.variant71.noetherian.{NOETH_EXTRA[n-1]}",
           "text":variant["text"],"review_state":"screened",
           "evidence_ids":[f"obs.wave2.variant70.noetherian.{j:02d}"],
           "mathematical_review_reason":noeth_research["mathematical_review"]+" Scope: "+variant["mathematical_scope"],
           "source_screened_by":"assistant_independent_noetherian_variants_review_2026_10_20",
           "human_verified":False
        })
    revised={
       **old_saved,
       "term_ids":["term.86b5d488b98c612f","term.wave2.variant70.noetherian"],
       "formulations":[first]+supplemental,
       "variant_refinement_note":"Four equivalent independently sourced characterizations of Noetherian commutative unital rings. Stacks-based finite-generation formulation retained first; prior combined text is archived."
    }
    if original_noeth!=old_saved and original_noeth!=revised:
        raise PipelineError("Prior Noetherian definition changed without a review event")
    archive=w.root/"state/wave2_formulation_reviews_snapshot_524_before_variant71.jsonl"
    oldmeaning=w.root/"events/noetherian_meaning_before_variant71.jsonl"
    ledger=w.root/"state/wave2_formulation_reviews.jsonl"
    oldrows=jsonl(ledger)
    if len(oldrows) not in (524,530) or len({r["formulation_id"] for r in oldrows})!=len(oldrows):
        raise PipelineError("Prior formulation-level review inventory incomplete")
    if {id for r in oldrows for id in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Old screened dependency links not accounted for")
    if len(oldrows)==524:
        if any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in oldrows):
            raise PipelineError("Old screened meaning catalog version mismatch")
        oldtext=ledger.read_text(encoding="utf-8")
        if archive.exists() and archive.read_text(encoding="utf-8")!=oldtext:
            raise PipelineError("Historical 524-review snapshot mismatch")
        archive.write_text(oldtext,encoding="utf-8")
        store(oldmeaning,[old_saved])
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_524_before_variant71.json",{
          "rows":524,"links":693,"sha256":hashlib.sha256(oldtext.encode("utf-8")).hexdigest(),
          "human_peer_verified":False
        })
    historic=jsonl(archive)
    if len(historic)!=524 or len({r["formulation_id"] for r in historic})!=524:
        raise PipelineError("Missing older review snapshot")
    if jsonl(oldmeaning)!=[old_saved]:
        raise PipelineError("Old mathematical source preserved incorrectly")
    event={
       "event_id":"variant71.noetherian.split-axioms-under-original-meaning",
       "meaning_id":NOETH,"old_meaning_digest":digest(old_saved),
       "new_meaning_digest":digest(revised),
       "original_formulation_id":NOETH_FID,
       "old_first_formulation":old_saved["formulations"][0]["text"],
       "new_first_formulation":NOETH_FIRST,
       "new_source_formulation_ids":[form["id"] for form in supplemental],
       "original_St acks_evidence_preserved":True,
       "individual_mathematical_reason":noeth_research["mathematical_review"],
       "production_corpus_used":False,"human_verified":False
    }
    store(w.root/"events/noetherian_meaning_amendment_batch71.jsonl",[event])
    indiv=[]
    for m in (connected,):
        for f in m["formulations"]:
            indiv.append({"review_id":"review.variant71."+f["id"],"meaning_id":m["id"],
              "formulation_id":f["id"],"source_evidence_ids":f["evidence_ids"],
              "mathematical_reason":f["mathematical_review_reason"],
              "decision":"screened_pending_individual_relation_review",
              "human_verified":False,"production_corpus_used":False})
    for f in supplemental:
        indiv.append({"review_id":"review.variant71."+f["id"],"meaning_id":NOETH,
          "formulation_id":f["id"],"source_evidence_ids":f["evidence_ids"],
          "mathematical_reason":f["mathematical_review_reason"],
          "decision":"screened_pending_individual_relation_review",
          "human_verified":False,"production_corpus_used":False})
    store(w.root/"wave2/connected_noetherian_individual_reviews_batch71.jsonl",indiv)
    if CONNECTED not in meanings:
        w.ingest("meanings",store(w.root/"intake/connected_optional_empty_meaning_batch71.jsonl",[connected]),batch_size=1)
    after=w.records("meanings")
    if len(after)!=510:
        raise PipelineError("No distinct connected convention admitted")
    if after[NOETH]==old_saved:
        revised_inventory=[revised if m["id"]==NOETH else m for m in after.values()]
        for m in revised_inventory:
            w.validate("meanings",m)
        atomic_jsonl(w.root/"records/meanings.jsonl",revised_inventory)
        after=w.records("meanings")
    if after[NOETH]!=revised or after[CONNECTED]!=connected or after[STACKS_CONN]!=original_connected:
        raise PipelineError("Connected conventions or Noetherian equivalences changed")
    mh=digest(list(after.values()))
    updated=[dict(r,meaning_catalog_digest=mh) for r in historic]
    for row in indiv:
        updated.append({
          "formulation_id":row["formulation_id"],"meaning_id":row["meaning_id"],
          "meaning_catalog_digest":mh,"decision":"needs_review","relation_ids":[],
          "original_wave1_disposition":None,
          "source":"independent_proofwiki_variant_mathematical_review_batch71",
          "editorial_reason":"Individually sourced definition variant; exact prerequisite links pending separate review.",
          "human_verified":False,"reviewed_by":None
        })
    if len(oldrows)==530:
        current={r["formulation_id"]:r for r in oldrows}
        if current!={r["formulation_id"]:r for r in updated}:
            raise PipelineError("Prior completed variant refinement review differs")
    else:
        atomic_jsonl(ledger,sorted(updated,key=lambda r:r["formulation_id"]))
    result=jsonl(ledger)
    lookup={r["formulation_id"]:r for r in result}
    if len(result)!=530 or len(lookup)!=530:
        raise PipelineError("Missing individual source-scoped formulation review")
    for prior in historic:
        now=lookup[prior["formulation_id"]]
        if any(now.get(k)!=v for k,v in prior.items() if k!="meaning_catalog_digest"):
            raise PipelineError("Old 524-reviewed formulation decision changed")
    if {id for r in result for id in r["relation_ids"]}!=set(w.records("relations")):
        raise PipelineError("Previously reviewed relationship lost")
    check_cycles(after,w.records("relations"))
    if dict(Counter(r["decision"] for r in result))!={"linked":518,"no_supported_target":6,"needs_review":6}:
        raise PipelineError("New pending variants or older screened decisions inconsistent")
    state=w.state("meanings")
    state.update(total=510,record_digest=mh,
      screened_new_formulations=99,stage4_review_complete=False)
    atomic_json(w.root/"state/meanings.json",state)
    report={
       "batch":71,"contextual_meanings":510,"reviewed_formulations":530,
       "separate_connected_space_conventions":2,
       "existing_stacks_nonempty_convention_retained":True,
       "new_proofwiki_empty_allowed_connected_variants":3,
       "noetherian_existing_meaning_amended_not_duplicated":True,
       "noetherian_equivalent_formulations":4,
       "historical_524_review_decisions_preserved":True,
       "all_693_previous_links_preserved":True,
       "new_individual_link_reviews_pending":6,
       "all_stages_unsealed":True,"human_peer_verified":False,
       "production_corpus_used":False,
       "next":"Review exact source-specific prerequisite links for new connectedness and Noetherian variants; avoid nonempty/empty definition conflation and self-links."
    }
    atomic_json(w.root/"state/wave2_variant71_meanings.json",report)
    return report
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,default=Path(ROOT))
    print(json.dumps(run(p.parse_args().workspace),indent=2))
if __name__=="__main__":main()
