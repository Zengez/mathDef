"""Build corrected Stage 4 context-specific mathematical meaning candidates.

Every independently authored, reviewed Stage 3 paraphrase is retained as one
formulation. Distinct objects/contexts are NOT merged merely because they
occur on the same source page. Only the explicitly listed, mathematically
equivalent characterizations are grouped as formulations of one meaning.

No original production mathDef content is ever accessed. The output remains
a SOURCE-SCREENED editorial reconstruction, not a human-refereed corpus.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from .core import PipelineError, Workspace, canonical, jsonl
from .stage3_attempts import require_full_attempt_coverage
from .stage3_review_gate import require_reviewed_term_dispositions

# Manually inspected equivalences within a single Stacks source section.
# Only pairings where the same mathematical property is characterized twice.
# Labels are suffix keys from the independent observation IDs, with either
# underscores (old evidence) or hyphens (new independent review evidence).
EQUIVALENT = {
    "Jacobson rings": [
        ("jacobson-ring", "jacobson-ring-prime-characterization"),
    ],
    "Geometrically normal algebras": [
        ("geometrically-normal-algebra", "geometrically-normal-perfect-closure-test"),
    ],
    "Pure ideals": [
        ("pure-ideal", "pure-ideal-intersection-test"),
    ],
    "Formally unramified maps": [
        ("formally-unramified-map", "formally-unramified-differential-test"),
    ],
    "Local rings": [
        ("local-ring-unique-maximal", "local-ring-nonunit-ideal"),
    ],
    "Reduced schemes": [
        ("reduced-scheme", "reduced-scheme-sections-equivalent"),
    ],
    "Geometrically reduced algebras": [
        ("geometrically-reduced-algebra", "geometric-reducedness-perfect-test"),
    ],
    "Profinite spaces": [
        ("profinite-topological-space", "profinite-space-compact-characterization"),
    ],
    "Geometrically integral algebras": [
        ("geometrically-integral-algebra", "geometrically-integral-algebra-closure-test"),
    ],
    "The Jacobson radical of a ring": [
        ("jacobson-radical-ring", "jacobson-radical-unit-test"),
    ],
    "Noetherian topological spaces": [],
    "Hausdorff spaces": [
        ("hausdorff-space", "hausdorff-diagonal-characterization"),
    ],
    "Relatively prime polynomials": [
        ("relatively-prime-polynomials", "relatively-prime-polynomials-roots"),
    ],
    "Perfect fields": [
        ("perfect-field",),
    ],
    "Artin-Schreier extensions": [],
    "Étale ring maps": [],
    "Geometrically connected algebras": [],
    "Formally smooth maps": [],
    "Normal rings": [],
}

def identifier_suffix(observation, term_id):
    if observation["id"].startswith("obs.recovery."):
        prefix = "obs.recovery." + term_id.removeprefix("term.") + "."
    else:
        prefix = "obs.paraphrase." + term_id.removeprefix("term.") + "."
    if not observation["id"].startswith(prefix):
        raise PipelineError("Unrecognized source observation ID: " + observation["id"])
    return observation["id"][len(prefix):].replace("_", "-")

def context_label(item):
    hint = item.get("context_hint") or "Mathematical definition"
    return hint.split(":", 1)[-1].strip()

def build(workspace, output):
    w=Workspace(workspace)
    cfg=w.config()
    if not cfg.get("require_full_definition_attempts") or not cfg.get("require_reviewed_term_dispositions"):
        raise PipelineError("Must use corrected independent research workspace")
    if not w.state("observations").get("sealed"):
        raise PipelineError("Corrected Stage 3 evidence must be sealed first")
    if w.state("meanings").get("sealed"):
        raise PipelineError("Cannot rebuild a sealed meaning registry")
    require_full_attempt_coverage(w.root,w.root/"state/stage3_acquisition_attempts.jsonl")
    require_reviewed_term_dispositions(w.root,w.root/"state/stage3_term_reviews.jsonl")
    reviews={x["term_id"]:x for x in jsonl(w.root/"state/stage3_term_reviews.jsonl")}
    terms=w.records("terms")
    obs=w.records("observations")
    candidates=defaultdict(list)
    for item in obs.values():
        if item["record_kind"] != "paraphrase":
            continue
        tid=item["term_id"]
        if reviews[tid]["decision"]!="supported":
            raise PipelineError("Unreviewed mathematical paraphrase exists for "+tid)
        if item.get("confidence")!="source_checked" or not item.get("source_section"):
            raise PipelineError("Source reference or editorial review missing: "+item["id"])
        candidates[tid].append(item)
    if set(candidates)!={t for t,r in reviews.items() if r["decision"]=="supported"}:
        raise PipelineError("Source-supported terms differ from source-checked observation inventory")

    rows=[]
    used=set()
    equivalent_groups=0
    for tid in sorted(candidates):
        term=terms[tid]
        observations=sorted(candidates[tid],key=lambda x:x["id"])
        by_key={identifier_suffix(x,tid):x for x in observations}
        if len(by_key)!=len(observations):
            raise PipelineError("Duplicate semantic keys for term "+tid)
        partitions=[]
        for group in EQUIVALENT.get(term["label"], []):
            if not all(k in by_key for k in group):
                raise PipelineError("Explicit equivalence grouping no longer matches the sealed source evidence: "+term["label"]+" "+repr(group))
            if any(k in used for k in (tid+"."+x for x in group)):
                raise PipelineError("Duplicate equivalence assignment")
            for key in group:used.add(tid+"."+key)
            partitions.append(([by_key[k] for k in group], "verified_equivalent_formulations"))
            equivalent_groups+=int(len(group)>1)
        for key in sorted(by_key):
            if tid+"."+key not in used:
                used.add(tid+"."+key)
                partitions.append(([by_key[key]],"distinct_source_context"))
        for collection,rule in partitions:
            lead=collection[0]
            first=identifier_suffix(lead,tid)
            forms=[]
            for item in collection:
                suffix=identifier_suffix(item,tid)
                forms.append({
                    "id":"form."+tid.removeprefix("term.")+"."+suffix,
                    "text":item["text"],
                    "review_state":"screened",
                    "evidence_ids":[item["id"]],
                    "editorial_note":"Independently paraphrased from the cited source and reviewed as a source-backed mathematical candidate; not human-refereed.",
                })
            meaning={
                "id":"meaning."+tid.removeprefix("term.")+"."+first,
                "term_group_id":"group."+tid.removeprefix("term."),
                "display_term":context_label(lead),
                "context":lead["context_hint"],
                "term_ids":[tid],
                "formulations":forms,
                "source_citation":{
                    "source_id":lead["source_id"],
                    "url":lead["locator"],
                    "section":"; ".join(dict.fromkeys(x["source_section"] for x in collection)),
                },
                "semantic_classification":rule,
                "review_stage":"source_cross_checked",
                "human_verified":False,
                "grouping_note":(
                    "Mathematical equivalence explicitly checked against cited source."
                    if rule=="verified_equivalent_formulations" else
                    "Distinct semantic label retained; later cross-page synonym/variant refinement remains open."),
            }
            w.validate("meanings",meaning)
            rows.append(meaning)
    if len(used)!=len(obs)-sum(x["record_kind"]=="locator" for x in obs.values()):
        raise PipelineError("Not all independent mathematical observations accounted for")
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text("".join(canonical(x)+"\n" for x in rows),encoding="utf-8")
    return {"meaning_candidates":len(rows),"formulations":sum(len(x["formulations"]) for x in rows),
            "terms_supported":len(candidates),"explicit_equivalence_groups":equivalent_groups,
            "distinct_meaning_groups_with_multiple_forms":sum(len(x["formulations"])>1 for x in rows),
            "source_reviewed_candidates_only":True,"human_refereed":False}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args(argv)
    print(json.dumps(build(args.workspace,args.output),indent=2))

if __name__=="__main__":
    main()
