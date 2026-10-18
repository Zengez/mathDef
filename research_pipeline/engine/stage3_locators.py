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

    source = w.records("sources")["src.stacks"]
    existing = w.records("observations")
    records = []
    for term in w.records("terms").values():
        if term["source_id"] != "src.stacks":
            continue
        parsed = safe_source_url(term["locator"], source)
        if not parsed.path.startswith("/tag/"):
            raise PipelineError("Unexpected Stacks locator for " + term["id"])
        row = {
            "id": "obs.locator." + term["id"].removeprefix("term."),
            "term_id": term["id"],
            "source_id": "src.stacks",
            "locator": term["locator"],
            "record_kind": "locator",
            "discovery_method": "stage2.sealed-index",
            "verification_state": "index_locator_only",
            "evidence_note": (
                "A reference to a Stacks section that appeared in the "
                "reviewed Stage 2 index. No definition text was fetched, "
                "and no mathematical claim is verified by this record."),
        }
        w.validate("observations", row)
        if row["id"] in existing:
            if canonical(row) != canonical(existing[row["id"]]):
                raise PipelineError("Existing observation changed: " + row["id"])
            continue
        records.append(row)

    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(canonical(x) + "\n" for x in records),
                      encoding="utf-8")
    result = {"source": "src.stacks", "new_locator_candidates": len(records),
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
