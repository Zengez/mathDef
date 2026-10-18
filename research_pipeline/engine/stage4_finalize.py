"""Verify bounded Wave 1 mathematical meaning classifications before sealing.

Only independently authored Stage 3 paraphrases can support a screened
formulation; Stage 2/3 locator-only placeholders cannot become definitions.
This tool works entirely within a specified independent experiment workspace.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from .core import PipelineError, Workspace, atomic_json, canonical

EXPECTED_TERMS = 318
EXPECTED_AUTHORED_OBSERVATIONS = 31
EXPECTED_SUPPORTED_TERMS = 25
EXPECTED_MEANINGS = 31
EXPECTED_FORMULATIONS = 32


def audit(workspace, *, seal=False):
    w = Workspace(workspace)
    if w.config().get("external_reference_mode") is not True:
        raise PipelineError("Stage 4 requires an isolated reconstruction workspace")
    for stage in ("sources", "terms", "observations"):
        if not w.state(stage).get("sealed"):
            raise PipelineError("Previous stage is not sealed: " + stage)
    terms = w.records("terms")
    obs = w.records("observations")
    meanings = w.records("meanings")
    authored = {k: x for k, x in obs.items() if x["record_kind"] == "paraphrase"}
    supported = {x["term_id"] for x in authored.values()}
    if (len(terms), len(authored), len(supported)) != (
            EXPECTED_TERMS, EXPECTED_AUTHORED_OBSERVATIONS, EXPECTED_SUPPORTED_TERMS):
        raise PipelineError("Unexpected sealed upstream data; audit the checkpoint")
    if len(meanings) != EXPECTED_MEANINGS:
        raise PipelineError(f"Incomplete meaning classification: {len(meanings)} of {EXPECTED_MEANINGS}")

    encountered_evidence = Counter()
    formulations = set()
    grouped = defaultdict(list)
    diagnostics = []
    for item in meanings.values():
        w.validate("meanings", item)
        if item.get("human_verified") is not False:
            raise PipelineError("Do not assert independent human mathematical verification")
        if item.get("review_stage") != "source_cross_checked":
            raise PipelineError("Missing source cross-check review")
        if len(item["term_ids"]) != 1:
            raise PipelineError("Grouped meanings require unambiguous term attribution")
        tid = item["term_ids"][0]
        if tid not in supported:
            raise PipelineError("Unsubstantiated term was promoted to a meaning: " + tid)
        if item["term_group_id"] != "group." + tid.removeprefix("term."):
            raise PipelineError("Inconsistent term grouping: " + item["id"])
        if not item["context"].strip() or not item["display_term"].strip():
            raise PipelineError("Mathematical context and heading required")
        src = item.get("source_citation", {})
        if (src.get("source_id") != "src.stacks" or
                src.get("url") != terms[tid]["locator"] or not src.get("section")):
            raise PipelineError("Missing source citation: " + item["id"])
        grouped[tid].append(item)
        for form in item["formulations"]:
            if form["id"] in formulations:
                raise PipelineError("Formulation ID reused: " + form["id"])
            formulations.add(form["id"])
            if form["review_state"] != "screened":
                raise PipelineError("A proposed mathematical formulation remains unscreened")
            if not 30 <= len(form["text"]) <= 2200:
                raise PipelineError("Formulation text outside expected bounds")
            if not form.get("editorial_note") and not form.get("equivalence_note"):
                raise PipelineError("Missing context/equivalence rationale: " + form["id"])
            for eid in form["evidence_ids"]:
                source = authored.get(eid)
                if not source:
                    raise PipelineError("Locator-only evidence cannot justify a screened formula")
                if source["term_id"] != tid or source["locator"] != src["url"]:
                    raise PipelineError("Evidence points to unrelated term/source")
                if source.get("review_state") != "candidate" or source.get("confidence") != "source_checked":
                    raise PipelineError("Stage 3 evidence not source-checked")
                encountered_evidence[eid] += 1

    if set(encountered_evidence) != set(authored):
        missing = sorted(set(authored) - set(encountered_evidence))
        raise PipelineError("Missing classified mathematical observations: " + str(missing[:5]))
    if len(formulations) != EXPECTED_FORMULATIONS:
        raise PipelineError("Unexpected formulation count")
    duplicates = {tid: len(rows) for tid, rows in grouped.items() if len(rows) > 1}
    if sum(duplicates.values()) - len(duplicates) != EXPECTED_MEANINGS - EXPECTED_SUPPORTED_TERMS:
        raise PipelineError("Variant contexts were lost")
    if not any(len(x["formulations"]) > 1 for x in meanings.values()):
        raise PipelineError("Equivalent formulation alternatives were lost")
    unclassified = sorted(set(terms) - supported)
    if len(unclassified) != 293:
        raise PipelineError("Unsupported term coverage discrepancy")
    audit_record = {
        "schema_version": 1, "stage": "meanings",
        "scope": "bounded independent Wave 1; semantic review of available authored evidence",
        "sealed_upstream_term_count": len(terms),
        "substantive_observations_classified": len(authored),
        "supported_distinct_terms": len(supported),
        "meanings_with_explicit_contexts": len(meanings),
        "screened_formulations": len(formulations),
        "unresolved_locator_only_terms": len(unclassified),
        "unresolved_term_ids": unclassified,
        "multi_context_term_ids": sorted(duplicates),
        "multi_context_count": len(duplicates),
        "interpretive_caveat": (
            "One source section may define different objects; these are not synonymized "
            "without mathematical evidence. A normal domain is the domain-restricted "
            "case of a normal ring, and basis/subbasis, initial/final and "
            "quasi-compact space/map are distinct meanings."),
        "validation_policy": (
            "Source-checked independently written paraphrases only; all mathematical "
            "formulations passed an editorial screening step but are NOT independently "
            "human-verified. Index-only and unverified PlanetMath locators were NOT "
            "promoted into definitions."),
        "next_stage": "relations",
        "next_recommended_thinking": "High",
    }
    if seal:
        if w.state("meanings").get("sealed"):
            return {"sealed": True, "total": len(meanings), "already_sealed": True}
        atomic_json(w.root / "state" / "stage4_review.json", audit_record)
        result = w.seal("meanings")
        return {"sealed": True, **result, "screened_formulations": len(formulations),
                "unresolved_terms": len(unclassified)}
    return {"sealed": False, "meaning_count": len(meanings),
            "formulations": len(formulations), "unresolved_terms": len(unclassified)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--seal", action="store_true")
    args = parser.parse_args(argv)
    print(json.dumps(audit(args.workspace, seal=args.seal), indent=2))


if __name__ == "__main__":
    main()
