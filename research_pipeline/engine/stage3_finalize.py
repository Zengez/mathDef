"""Validate Stage 3 evidence without hardcoded, artificially small coverage caps.

In the corrected Wave 1 workspace, sealing additionally requires an actual
attempt for EVERY sealed term and a reviewed disposition for EVERY term.
Legacy immutable seals are reported as historical, not certified complete.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from .core import PipelineError, Workspace, atomic_json
from .source_intake import safe_source_url


def finalize(workspace):
    w = Workspace(workspace)
    config = w.config()
    if config.get("external_reference_mode") is not True:
        raise PipelineError("Not an independent reconstruction workspace")
    if not w.state("sources").get("sealed") or not w.state("terms").get("sealed"):
        raise PipelineError("Prior stages must be sealed")

    if w.state("observations").get("sealed"):
        if not config.get("require_full_definition_attempts"):
            return {
                "status": "historical_seal_only",
                "message": "The old Stage 3 seal checked source URLs, not attempted source research for all terms. Use the corrected Wave 1 continuation.",
                "observations": len(w.records("observations")),
                "full_attempt_coverage_verified": False,
            }
        return {"status": "already_sealed", "total": len(w.records("observations"))}

    # Do this BEFORE writing audit or sealing; missing/unreviewed terms are
    # blockers, never silently treated as empty or successful.
    if not config.get("require_full_definition_attempts") or not config.get(
            "require_reviewed_term_dispositions"):
        raise PipelineError(
            "Corrected Stage 3 requires both full-acquisition and reviewed-term coverage gates")
    from .stage3_attempts import require_full_attempt_coverage
    from .stage3_review_gate import require_reviewed_term_dispositions
    attempts = require_full_attempt_coverage(
        w.root, w.root / "state/stage3_acquisition_attempts.jsonl")
    decisions = require_reviewed_term_dispositions(
        w.root, w.root / "state/stage3_term_reviews.jsonl")

    terms = w.records("terms")
    sources = w.records("sources")
    observations = w.records("observations")
    locators = {}
    authored = []
    counts = Counter()
    for row in observations.values():
        w.validate("observations", row)
        term = terms[row["term_id"]]
        if row["source_id"] != term["source_id"] or row["locator"] != term["locator"]:
            raise PipelineError("Observation locator/source differs from its sealed term")
        safe_source_url(row["locator"], sources[row["source_id"]])
        if row["record_kind"] == "locator":
            if row["term_id"] in locators:
                raise PipelineError("Multiple locator rows for one term")
            if row.get("text"):
                raise PipelineError("Locator-only evidence may not contain sourced mathematical text")
            locators[row["term_id"]] = row
            counts["locator"] += 1
            if row["source_id"] == "src.planetmath":
                if row.get("verification_state") != "unverified_source_locator":
                    raise PipelineError("PlanetMath unverified-source lead mislabeled")
                counts["planetmath_unverified_locator"] += 1
        elif row["record_kind"] == "paraphrase":
            if (row.get("reproduction_policy") !=
                    "independently authored paraphrase; no source passage copied"):
                raise PipelineError("Math paraphrase missing explicit independent-authorship provenance")
            if not row.get("source_section") or not 35 <= len(row["text"]) <= 2500:
                raise PipelineError("Mathematical candidate lacks source section or adequate text")
            authored.append(row)
            counts["paraphrase"] += 1
        elif row["record_kind"] == "licensed_excerpt":
            if sources[row["source_id"]]["rights"] != "permitted" or not sources[
                    row["source_id"]].get("license_url"):
                raise PipelineError("Excerpt lacks source-specific license clearance")
            counts["licensed_excerpt"] += 1
        else:
            raise PipelineError("Unknown observation record kind")

    if set(locators) != set(terms):
        raise PipelineError("One source locator must exist for each sealed term")
    review_counts = decisions["decisions"]
    authored_ids = {row["term_id"] for row in authored}
    if review_counts.get("supported", 0) > len(authored_ids):
        raise PipelineError("More supported definitions reported than terms with authored evidence")
    audit = {
        "schema_version": 2, "stage": "observations",
        "scope": "corrected first-wave Stage 3, independent-source term coverage",
        "source_terms_total": len(terms),
        "source_acquisition_attempts_accounted": attempts["attempts_accounted_for"],
        "source_pages_fetched": attempts["source_documents_fetched"],
        "source_policy_blocked": attempts["policy_blocked"],
        "source_fetch_failures_after_retries": attempts["fetch_failed_after_retries"],
        "mathematical_dispositions": review_counts,
        "observations_total": len(observations),
        "observation_types": dict(counts),
        "terms_with_independently_authored_paraphrase": len(authored_ids),
        "terms_with_no_authored_paraphrase": len(terms) - len(authored_ids),
        "source_restriction_note": (
            "Access blocked terms are unresolved, not mathematical evidence. "
            "Structural definition markers are only investigation leads."),
        "human_verified": False,
    }
    atomic_json(w.root / "state/stage3_review.json", audit)
    info = w.seal("observations")  # Enforces both gates again in Workspace.
    return {"status": "sealed", **info, "coverage": audit}


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", required=True, type=Path)
    args = p.parse_args(argv)
    print(json.dumps(finalize(args.workspace), indent=2))


if __name__ == "__main__":
    main()
