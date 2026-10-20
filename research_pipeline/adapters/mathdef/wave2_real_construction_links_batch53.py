"""Batch 53: individually source-screened noncircular classical-real dependencies.

No production corpus is read; six new formulations receive exact review
decisions, and all previously screened relations/decisions are preserved.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from research_pipeline.engine.core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from research_pipeline.engine.stage5_review_gate import atomic_jsonl
from research_pipeline.engine.wave2_apply_links import locator,check_cycles

ROOT="research_pipeline/experiments/reconstruction-v2-independent"
PLANET="https://planetmath.org/dedekindcuts"
CSUSM="https://public.csusm.edu/aitken_html/m378_S2016/Ch9RealNumbers.pdf"
LIBRE="https://math.libretexts.org/Bookshelves/Analysis/A_Primer_of_Real_Analysis_%28Sloughter%29/01%3A_Fundamentals/1.04%3A_Real_Numbers"
CORNELL="https://pi.math.cornell.edu/~web304/reals.pdf"
# One source phrase can justify several independently distinct prerequisites.
LINKS=(
  ("01","form.wave2.real50.dedekind-rational-lower-cut","meaning.wave2.foundation.subset-proper",
   "subset A of Q",PLANET,"https://proofwiki.org/wiki/Definition%3ASubset",
   "A Dedekind lower cut is a proper subset of the rationals. The separately screened strict-subset meaning supplies exactly the additional non-equality to Q required by the source's nontriviality axiom."),
  ("02","form.wave2.real50.cut-model-reals","meaning.wave2.real50.dedekind-rational-lower-cut",
   "Dedekind cuts A of Q",PLANET,PLANET,
   "The model takes its elements to be Dedekind cuts of the rationals. This is a direct construction prerequisite; it does not assert the set model is literally the same underlying set as an axiomatic field."),
  ("03","form.wave2.real51.rational-cauchy-equivalence","meaning.wave2.real51.rational-cauchy",
   "rational Cauchy sequences",LIBRE,CORNELL,
   "The equivalence relation is defined on pairs of previously defined rational Cauchy sequences; no real-valued limit is invoked, and the direction of dependence is from equivalence to the Cauchy criterion."),
  ("04","form.wave2.real52.cauchy-quotient-reals","meaning.wave2.real51.rational-cauchy",
   "rational Cauchy sequences",CSUSM,CORNELL,
   "The quotient model starts from the set of rational Cauchy sequences. This is an explicit foundational requirement for its equivalence-class construction, independent of the eventual field and completeness theorems."),
  ("05","form.wave2.real52.cauchy-quotient-reals","meaning.wave2.real51.rational-cauchy-equivalence",
   "a∼b",CSUSM,LIBRE,
   "An equivalence class [a_n] and quotient C_Q/∼ require the independently defined zero-difference equivalence relation on rational Cauchy sequences; a mere set of sequences does not determine the quotient."),
  ("06","form.wave2.real52.positive-cauchy-class","meaning.wave2.real52.cauchy-quotient-reals",
   "Cauchy-equivalence class",CSUSM,CSUSM,
   "The positivity condition applies to real equivalence classes in the constructed quotient, not to raw rational sequences. Uniform eventual rational positivity ensures this class-level assertion survives representative changes.")
)
NO_TARGET={
 "formulation_id":"form.wave2.real51.rational-cauchy",
 "meaning_id":"meaning.wave2.real51.rational-cauchy",
 "source_locator":CORNELL,
 "decision":"no_supported_target",
 "mathematical_reason":"The independent corpus has screened no general elementary sequence-of-rationals meaning or rational absolute-value arithmetic meaning that can be linked here without confusing them with module exact sequences or real-function absolute value. The Cauchy definition quantifies over rational tolerances before real numbers have been built. Linking it to a real-valued limit or the newly constructed quotient would reverse the logical foundations and risk a circular dependency.",
 "missing_candidates":["elementary rational-number sequence (function N to Q)","rational absolute value and positive rational tolerance"],
 "reviewed_by":"assistant_independent_real_construction_relation_review_2026_10_20",
 "human_verified":False
}

def store(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    body="".join(canonical(r)+"\n" for r in rows)
    if path.exists() and path.read_text(encoding="utf-8")!=body:
        raise PipelineError("Altered prior individual mathematical link audit")
    path.write_text(body,encoding="utf-8")
    return path

def run(root):
    w=Workspace(root)
    if not w.config().get("independent_second_wave") or any(w.state(s).get("sealed") for s in ("sources","terms","observations","meanings","relations")):
        raise PipelineError("Only unsealed independent Wave 2 may receive links")
    expected={"sources":14,"terms":395,"observations":818,"meanings":496}
    if {s:len(w.records(s)) for s in expected}!=expected:
        raise PipelineError("Unexpected independently screened formulation catalog")
    meanings=w.records("meanings"); observations=w.records("observations")
    byform={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
    if len(byform)!=508:
        raise PipelineError("New meaning/formulation ID collision")
    current=w.records("relations")
    if len(current) not in (664,670):
        raise PipelineError("Other relationship changes need separate review")
    original={k:v for k,v in current.items() if not k.startswith("rel.wave2.real53.")}
    if len(original)!=664:
        raise PipelineError("Inherited 664 screened links lost")
    reviewfile=w.root/"state/wave2_formulation_reviews.jsonl"
    old=jsonl(reviewfile)
    indexed={r["formulation_id"]:r for r in old}
    if len(old)!=508 or len(indexed)!=508 or any(r["meaning_catalog_digest"]!=digest(list(meanings.values())) for r in old):
        raise PipelineError("Old individual formulation review inventory not current")
    if {id for r in old for id in r["relation_ids"]}!=set(current):
        raise PipelineError("Some screened link lacks individual current evidence")
    ids={
       "form.wave2.real50.dedekind-rational-lower-cut",
       "form.wave2.real50.cut-model-reals",
       "form.wave2.real51.rational-cauchy",
       "form.wave2.real51.rational-cauchy-equivalence",
       "form.wave2.real52.cauchy-quotient-reals",
       "form.wave2.real52.positive-cauchy-class"
    }
    if not ids.issubset(byform):
        raise PipelineError("Required six reviewed formulations missing")
    before={r["formulation_id"]:r for r in old if r["formulation_id"] not in ids}
    if len(before)!=502:
        raise PipelineError("Older 502-reviewed formulation identities differ")
    prepared=[]
    for num,fr,to,phrase,source_url,target_url,reason in LINKS:
        m,form=byform[fr]
        if (form["review_state"]!="screened" or
            locator(m,observations)!=source_url or
            to not in meanings or
            locator(meanings[to],observations)!=target_url):
            raise PipelineError("Link endpoints do not match independently reviewed source locations: "+num)
        if phrase not in form["text"] or len(reason)<180:
            raise PipelineError("Missing literal terminology/source-scoped mathematical justification: "+num)
        prepared.append({
           "id":"rel.wave2.real53."+num,
           "from_formulation":fr,"target_meaning":to,"relation_type":"definition_uses",
           "review_state":"screened","source_phrase":phrase,
           "editorial_reason":reason,"source_locator":source_url,
           "target_locator":target_url,"reviewed_by":"assistant_independent_real_construction_relation_review_2026_10_20",
           "human_verified":False
        })
    if any(x["id"] in original for x in prepared):
        raise PipelineError("New link IDs collide with historical links")
    byid={**original,**{x["id"]:x for x in prepared}}
    check_cycles(meanings,byid)
    if len(old)==508 and len(current)==664:
        hist=w.root/"state/wave2_formulation_reviews_snapshot_508_before_real53.jsonl"
        data=reviewfile.read_text(encoding="utf-8")
        if hist.exists() and hist.read_text(encoding="utf-8")!=data:
            raise PipelineError("Historical 508-formulation ledger conflict")
        hist.write_text(data,encoding="utf-8")
        atomic_json(w.root/"state/wave2_formulation_reviews_snapshot_508_before_real53.json",{
            "rows":508,"links":664,"sha256":hashlib.sha256(data.encode("utf-8")).hexdigest(),
            "human_peer_verified":False})
    hist=w.root/"state/wave2_formulation_reviews_snapshot_508_before_real53.jsonl"
    prior=jsonl(hist)
    if len(prior)!=508 or len({x["formulation_id"] for x in prior})!=508:
        raise PipelineError("Missing signed historical 508 reviews")
    priorby={x["formulation_id"]:x for x in prior}
    if any(priorby[k]!=v for k,v in before.items()):
        raise PipelineError("Previously screened unrelated dispositions changed")
    for fid in ids:
        r=priorby[fid]
        if r["decision"]!="needs_review" or r["relation_ids"]:
            raise PipelineError("A new formulation was already reviewed: "+fid)
    if (NO_TARGET["source_locator"]!=locator(byform[NO_TARGET["formulation_id"]][0],observations)
         or len(NO_TARGET["mathematical_reason"])<220):
        raise PipelineError("No-target rationale is unsupported or circular")
    store(w.root/"wave2/real_construction_no_target_decision_batch53.jsonl",[NO_TARGET])
    store(w.root/"wave2/real_construction_individual_links_batch53.jsonl",prepared)
    intake=store(w.root/"intake/wave2_real_construction_links_batch_53.jsonl",prepared)
    if len(current)==664:
        w.ingest("relations",intake,batch_size=6)
    links=w.records("relations")
    if len(links)!=670 or any(links.get(p["id"])!=p for p in prepared):
        raise PipelineError("Exact link batch not materialized")
    check_cycles(meanings,links)
    result=[]
    for r in prior:
        update=dict(r)
        fid=r["formulation_id"]
        if fid in ids:
            attached=[link["id"] for link in prepared if link["from_formulation"]==fid]
            if attached:
                update["decision"]="linked"
                update["relation_ids"]=attached
                update["source"]="wave2_independent_real_construction_relation_source_review_batch53"
                update["editorial_reason"]="Individually screened exact mathematical prerequisites with per-link source locators and non-cyclic dependency direction."
                update["reviewed_by"]="assistant_independent_real_construction_relation_review_2026_10_20"
            else:
                if fid!=NO_TARGET["formulation_id"]:
                    raise PipelineError("Unreviewed new formulation "+fid)
                update["decision"]="no_supported_target"
                update["source"]="wave2_independent_rational_Cauchy_no_supported_target_batch53"
                update["editorial_reason"]=NO_TARGET["mathematical_reason"]
                update["reviewed_by"]=NO_TARGET["reviewed_by"]
        result.append(update)
    if len(current)==670:
        if {r["formulation_id"]:r for r in old}!={r["formulation_id"]:r for r in result}:
            raise PipelineError("Previously applied 670 link reviews conflict")
    else:
        atomic_jsonl(reviewfile,sorted(result,key=lambda x:x["formulation_id"]))
    actual=jsonl(reviewfile)
    if len(actual)!=508 or len({r["formulation_id"] for r in actual})!=508:
        raise PipelineError("Formulation review coverage changed unexpectedly")
    byreview={r["formulation_id"]:r for r in actual}
    if any(byreview[k]!=v for k,v in before.items()):
        raise PipelineError("An earlier independent review changed silently")
    if {id for r in actual for id in r["relation_ids"]}!=set(links):
        raise PipelineError("Some screened relation is not traced to an individual formulation")
    dispositions=dict(Counter(r["decision"] for r in actual))
    if dispositions!={"linked":503,"no_supported_target":5}:
        raise PipelineError("Six individual reviews were not completed: "+str(dispositions))
    report={
      "phase":"six_individual_non_circular_real_construction_prerequisite_reviews",
      "screened_meanings_unchanged":496,"formulation_reviews":508,
      "historical_502_review_decisions_unchanged":True,
      "previous_664_links_preserved":True,
      "new_source_screened_links":6,
      "no_supported_target_currently":1,
      "all_formulations_have_individual_review":True,
      "relation_cycles":False,"human_peer_verified":False,
      "production_corpus_used":False,"all_stages_unsealed":True,
      "next":"Recheck completeness of supporting source citations and missing rational sequence/rational arithmetic foundations; pursue additional independent model variants without merging distinct set representations."
    }
    atomic_json(w.root/"state/wave2_real_construction_relations_batch53.json",report)
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace",type=Path,default=Path(ROOT))
    a=parser.parse_args()
    print(json.dumps(run(a.workspace),indent=2))

if __name__=="__main__":main()
