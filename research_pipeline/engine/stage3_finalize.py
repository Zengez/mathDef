"""Audit and seal bounded first-wave Stage 3 evidence.

Every Stage 2 term must have one locator, but only source-checked authored
paraphrases can support semantic classification. Index-only records are not
promoted to mathematical verification. This script never opens production data.
"""
from __future__ import annotations

import json
from pathlib import Path

from .core import PipelineError, Workspace, atomic_json
from .source_intake import safe_source_url

def finalize(workspace):
    w = Workspace(workspace)
    if w.config().get("external_reference_mode") is not True:
        raise PipelineError("Not an isolated workspace")
    if not w.state("sources").get("sealed") or not w.state("terms").get("sealed"):
        raise PipelineError("Prior stages must be sealed")
    if w.state("observations").get("sealed"):
        return {"status": "already_sealed", "total": len(w.records("observations"))}
    sources, terms, observations = w.records("sources"), w.records("terms"), w.records("observations")
    locators = {}
    authored = []
    counts = {"stacks_index_locators": 0, "planetmath_unverified_locators": 0,
              "authored_paraphrases": 0, "licensed_excerpts": 0}
    for row in observations.values():
        w.validate("observations", row)
        term = terms[row["term_id"]]
        if row["source_id"] != term["source_id"] or row["locator"] != term["locator"]:
            raise PipelineError("Observation locator/source differs from its sealed term")
        safe_source_url(row["locator"], sources[row["source_id"]])
        if row["record_kind"] == "locator":
            if row["term_id"] in locators:
                raise PipelineError("Multiple locator rows for one term")
            locators[row["term_id"]] = row
            if row["source_id"] == "src.stacks":
                if row.get("verification_state") != "index_locator_only":
                    raise PipelineError("Stacks title record is not index-only evidence")
                counts["stacks_index_locators"] += 1
            elif row["source_id"] == "src.planetmath":
                if row.get("verification_state") != "unverified_source_locator":
                    raise PipelineError("Unverified PlanetMath candidate mislabeled")
                counts["planetmath_unverified_locators"] += 1
            else:
                raise PipelineError("Unknown source in locator registry")
            if row.get("text"):
                raise PipelineError("Locator-only observation contains text")
        elif row["record_kind"] == "paraphrase":
            if row["source_id"] != "src.stacks" or row.get("confidence") != "source_checked":
                raise PipelineError("Paraphrases must refer to checked permitted Stacks pages")
            if row.get("reproduction_policy") != "independently authored paraphrase; no source passage copied":
                raise PipelineError("Paraphrase provenance policy missing")
            if not row.get("source_section") or not 35 <= len(row["text"]) <= 2000:
                raise PipelineError("Malformed paraphrase or missing source section")
            authored.append(row)
            counts["authored_paraphrases"] += 1
        else:
            counts["licensed_excerpts"] += 1
            raise PipelineError("No licensed source passages were approved for Stage 3")

    if set(locators) != set(terms):
        raise PipelineError("One locator per sealed term is required")
    if counts != {"stacks_index_locators": 291, "planetmath_unverified_locators": 27,
                  "authored_paraphrases": 31, "licensed_excerpts": 0}:
        raise PipelineError("Unexpected evidence counts; review before sealing")
    authored_term_ids = sorted({r["term_id"] for r in authored})
    audit = {
        "schema_version": 1, "stage": "observations",
        "evidence_scope": "bounded first-wave acquisition, not exhaustive mathematical verification",
        "records_total": len(observations),
        "sealed_terms_total": len(terms),
        **counts,
        "terms_with_independently_authored_paraphrase": len(authored_term_ids),
        "terms_without_authored_paraphrase": len(terms) - len(authored_term_ids),
        "authored_term_ids": authored_term_ids,
        "planetmath_robots_restriction": (
            "Direct acquisition was not attempted where robots policy was unavailable. "
            "27 source URLs are UNVERIFIED Stage 2 leads only."),
        "evidence_limitations": (
            "Index-only references do not verify that linked pages define the index label. "
            "Source-checked authored paraphrases are editorial CANDIDATES, not screened "
            "definitions. Terms without paraphrases need human research in later stages/waves."),
        "reproduction_policy": "No unlicensed source text was copied; all substantive text is independent paraphrase.",
        "human_verification_claim": False,
        "next_recommended_thinking": "High",
        "next_stage": "meanings",
    }
    atomic_json(w.root / "state" / "stage3_review.json", audit)
    sealed = w.seal("observations")
    return {"status": "sealed", "stage": "observations", **sealed, "audit": counts,
            "terms_with_paraphrases": len(authored_term_ids)}

def main():
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(finalize(args.workspace), indent=2))

if __name__ == "__main__":
    main()
