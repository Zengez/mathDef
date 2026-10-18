"""Finish bounded Wave 1 Stage 2 from reviewed-source index candidates.

A Stage 2 term is an index *candidate*, not a mathematically verified
definition. Preserve source locators and existing provenance. Only stage-local
files may be written. Stage 3 is not touched.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

from .core import PipelineError, Workspace, atomic_json, canonical, jsonl
from .source_intake import fingerprint, safe_source_url

GENERIC_HEADINGS = frozenset({
    "introduction", "definitions", "basic definitions", "basic notions",
    "conventions", "notation", "remarks", "miscellany", "examples",
    "more examples", "preliminaries", "overview", "summary",
    "exercises", "appendix", "references", "bibliography",
    "a meta-observation about prime ideals", "curiosity",
})
MIN_AUTOMATED = 200
MIN_SUCCESSFUL_CHAPTERS = 6


def finalize(workspace, artifact_dir):
    w = Workspace(workspace)
    if w.config().get("external_reference_mode") is not True:
        raise PipelineError("External-reference mode is required")
    if not w.state("sources").get("sealed"):
        raise PipelineError("Source registry must be sealed")
    if w.state("terms").get("sealed"):
        return {"status": "already_sealed", "total": len(w.records("terms"))}

    artifact_dir = Path(artifact_dir)
    report = json.loads((artifact_dir / "report.json").read_text(encoding="utf-8"))
    raw = jsonl(artifact_dir / "raw_terms.jsonl")
    successes = [p for p in report["page_results"]
                 if p["status"] == "ok" and p["id"].startswith("page.stacks.chapter.")]
    if len(successes) < MIN_SUCCESSFUL_CHAPTERS:
        raise PipelineError("Insufficient successful chapter indexes to close Stage 2")
    if len(raw) < MIN_AUTOMATED:
        raise PipelineError("Unexpectedly few raw candidates; manual review required")
    if report.get("errors"):
        raise PipelineError("Cannot finalize with unresolved index acquisition errors")

    sources = w.records("sources")
    prior = w.records("terms")
    seen = set()
    accepted = []
    held = []
    duplicates = []
    for item in raw:
        if item["id"] in seen:
            raise PipelineError("Duplicate raw candidate ID")
        seen.add(item["id"])
        w.validate("terms", item)
        source = sources[item["source_id"]]
        safe_source_url(item["locator"], source)
        if item["source_id"] != "src.stacks":
            raise PipelineError("Unexpected source in Stacks-only artifact")
        if urlparse(item["locator"]).path[:5] != "/tag/":
            raise PipelineError("Unexpected section locator")
        expected = "term." + fingerprint(
            item["source_id"] + "|" + item["locator"] + "|" + item["label"].casefold())
        if item["id"] != expected:
            raise PipelineError("Candidate fingerprint does not match source and label")
        if item["label"].strip().casefold() in GENERIC_HEADINGS:
            held.append({"id": item["id"], "label": item["label"],
                         "locator": item["locator"], "reason": "generic chapter heading"})
            continue
        old = prior.get(item["id"])
        if old is not None:
            if any(old.get(k) != item.get(k) for k in ("label", "source_id", "locator")):
                raise PipelineError("Conflicting source provenance: " + item["id"])
            duplicates.append({"id": item["id"],
                               "reason": "Existing source title and locator retained",
                               "old_discovery_method": old.get("discovery_method"),
                               "new_discovery_method": item.get("discovery_method")})
            continue
        accepted.append(item)

    if len(accepted) < 150:
        raise PipelineError("Unexpectedly few non-generic new title candidates")

    # Validate everything before writing. Ingest is append-only and idempotent.
    batch_path = artifact_dir / "reviewed_terms.jsonl"
    batch_path.write_text("".join(canonical(x) + "\n" for x in accepted),
                          encoding="utf-8")
    result = w.ingest("terms", batch_path, batch_size=25)
    if result["added"] != len(accepted):
        raise PipelineError("Unexpected changed candidate count during ingest")
    # Record the scope and exceptions before sealing. This is a first-wave
    # bounded discovery stage, not an assertion of exhaustive mathematical coverage.
    audit = {
        "schema_version": 1, "stage": "terms",
        "review_kind": "source-index structural screening; not mathematical verification",
        "raw_candidates": len(raw),
        "newly_ingested": len(accepted),
        "previously_recorded": len(prior),
        "preserved_id_collisions": duplicates,
        "held_navigation_headings": held,
        "successful_stacks_chapters": [x["id"] for x in successes],
        "deferred_sources": [x for x in report["page_results"]
                             if x["status"] == "blocked"],
        "coverage_limitation": (
            "Bounded six-chapter Stacks Project discovery plus preexisting "
            "PlanetMath locator candidates. Not an exhaustive mathematics term list. "
            "Source rights and robots restrictions prevented additional automatic "
            "acquisition. More terms and sources may be added in Wave 2."),
        "human_mathematical_verification": False,
        "stage3_started": False,
    }
    atomic_json(w.root / "state" / "stage2_review.json", audit)
    sealed = w.seal("terms")
    if sealed["total"] != len(prior) + len(accepted):
        raise PipelineError("Unexpected sealed term count")
    return {"status": "sealed", "stage": "terms", **sealed,
            "newly_ingested": len(accepted), "held": len(held),
            "preserved_collisions": len(duplicates)}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--artifact-dir", type=Path, required=True)
    args = p.parse_args(argv)
    print(json.dumps(finalize(args.workspace, args.artifact_dir), indent=2))


if __name__ == "__main__":
    main()
