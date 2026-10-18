"""Create conservative Stage 3 source-locator evidence from the sealed term index.

This is not definition-text acquisition: Stage 2 TOC labels remain candidates.
Only the reviewed Stacks Project section locator records are eligible here.
Nothing touches original mathDef definitions or opens unlicensed pages.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import PipelineError, Workspace, canonical
from .source_intake import safe_source_url

def collect(workspace, output, *, ingest=False):
    w = Workspace(workspace)
    if not w.config().get("external_reference_mode"):
        raise PipelineError("This runner requires isolated research mode")
    if not w.state("sources").get("sealed") or not w.state("terms").get("sealed"):
        raise PipelineError("Source and term registries must be sealed first")
    if w.state("observations").get("sealed"):
        raise PipelineError("Observation stage is already sealed")

    sources = w.records("sources")
    existing = w.records("observations")
    records = []
    for term in w.records("terms").values():
        if term["source_id"] not in ("src.stacks", "src.planetmath"):
            continue
        source = sources[term["source_id"]]
        parsed = safe_source_url(term["locator"], source)
        if term["source_id"] == "src.stacks":
            if not parsed.path.startswith("/tag/"):
                raise PipelineError("Unexpected Stacks locator for " + term["id"])
            verification = "index_locator_only"
            note = ("A Stacks section listed in a reviewed Stage 2 index. "
                    "No definition was read or verified for this observation.")
        else:
            verification = "unverified_source_locator"
            note = ("PlanetMath candidate URL inherited from the sealed Stage 2 "
                    "record. Automated robots policy was unavailable; this "
                    "locator is NOT evidence that the article was opened "
                    "or a mathematical definition was confirmed.")
        row = {
            "id": "obs.locator." + term["id"].removeprefix("term."),
            "term_id": term["id"],
            "source_id": term["source_id"],
            "locator": term["locator"],
            "record_kind": "locator",
            "discovery_method": "stage2.sealed-index",
            "verification_state": verification,
            "evidence_note": note,
        }
        w.validate("observations", row)
        if row["id"] in existing:
            if canonical(row) != canonical(existing[row["id"]]):
                # Preserve previously committed index-only evidence exactly.
                if (term["source_id"] == "src.stacks" and
                        existing[row["id"]]["term_id"] == term["id"] and
                        existing[row["id"]]["locator"] == term["locator"]):
                    continue
                raise PipelineError("Existing observation changed: " + row["id"])
            continue
        records.append(row)

    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(canonical(x) + "\n" for x in records),
                      encoding="utf-8")
    result = {"sources": ["src.stacks", "src.planetmath"], "new_locator_candidates": len(records),
              "previous_observations": len(existing),
              "ingested": False, "stage3_sealed": False,
              "note": "Index locators only; independent author paraphrases still required."}
    if ingest and records:
        outcome = w.ingest("observations", target, batch_size=25)
        result.update(outcome)
        result["ingested"] = True
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ingest", action="store_true")
    args = parser.parse_args()
    print(json.dumps(collect(args.workspace, args.output,
                             ingest=args.ingest), indent=2))

if __name__ == "__main__":
    main()
