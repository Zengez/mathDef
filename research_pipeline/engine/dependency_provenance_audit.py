"""Read-only independent Wave2 evidence/variant integrity report.

This tool checks structural provenance and contextual variant bookkeeping only.
It never fetches external sources and never certifies a mathematical formulation.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

from .core import Workspace
from .dependency_graph import graph_path, read
from .population import snapshot


def summarize_provenance(inventory, observations, sources, example_limit=12):
    """Report source-link integrity without mistaking locator coverage for review."""
    forms = inventory["formulations"]
    meanings = inventory["meanings"]
    by_origin, evidence_kinds, verification_states, source_counts = (
        Counter(), Counter(), Counter(), Counter()
    )
    missing_observations = []
    missing_sources = []
    missing_locators = []
    observed_links = 0
    unique_observation_ids = set()
    for fid, formulation in sorted(forms.items()):
        by_origin[formulation["origin"]] += 1
        for oid in formulation.get("evidence_ids", []):
            observed_links += 1
            unique_observation_ids.add(oid)
            evidence = observations.get(oid)
            if evidence is None:
                missing_observations.append({"formulation_id": fid, "evidence_id": oid})
                continue
            evidence_kinds[evidence.get("record_kind", "unspecified")] += 1
            verification_states[evidence.get("verification_state", "unspecified")] += 1
            sid = evidence.get("source_id")
            source_counts[sid or "unspecified"] += 1
            if sid not in sources:
                missing_sources.append({"formulation_id": fid, "evidence_id": oid,
                                        "source_id": sid})
            if not str(evidence.get("locator", "")).strip():
                missing_locators.append({"formulation_id": fid, "evidence_id": oid})
    zero_evidence = [fid for fid, f in sorted(forms.items())
                     if not f.get("evidence_ids")]
    duplicate_names = defaultdict(list)
    multiple_variants = []
    for mid, meaning in sorted(meanings.items()):
        duplicate_names[meaning["display_term"].casefold().strip()].append(mid)
        if len(meaning["formulation_ids"]) > 1:
            multiple_variants.append(mid)
    duplicates = {name: ids for name, ids in sorted(duplicate_names.items())
                  if len(ids) > 1}
    incomplete = bool(zero_evidence or missing_observations or missing_sources or missing_locators)
    return {
        "read_only": True,
        "external_content_verified_by_this_command": False,
        "human_certified": False,
        "source_inventory_sha256": inventory["source_inventory_sha256"],
        "formulations": len(forms),
        "meanings": len(meanings),
        "source_record_count": len(sources),
        "observation_record_count": len(observations),
        "evidence_links": observed_links,
        "unique_observation_ids_used": len(unique_observation_ids),
        "formulation_origin_counts": dict(sorted(by_origin.items())),
        "record_kind_counts": dict(sorted(evidence_kinds.items())),
        "explicit_verification_state_counts": dict(sorted(verification_states.items())),
        "source_evidence_counts": dict(sorted(source_counts.items())),
        "zero_evidence_formulations": len(zero_evidence),
        "missing_evidence_records": len(missing_observations),
        "missing_source_records": len(missing_sources),
        "missing_locator_fields": len(missing_locators),
        "structural_provenance_complete": not incomplete,
        "meanings_with_multiple_formulations": len(multiple_variants),
        "formulation_texts_in_multiple_formulation_meanings": sum(
            len(meanings[mid]["formulation_ids"]) for mid in multiple_variants
        ),
        "duplicate_display_name_groups": len(duplicates),
        "examples": {
            "zero_evidence": zero_evidence[:example_limit],
            "missing_observations": missing_observations[:example_limit],
            "missing_sources": missing_sources[:example_limit],
            "missing_locators": missing_locators[:example_limit],
            "duplicate_display_names": [
                {"term": key, "meaning_ids": ids}
                for key, ids in list(duplicates.items())[:example_limit]
            ],
        },
        "interpretation": (
            "A structurally complete record chain is not external citation "
            "verification, mathematical correctness or human certification. "
            "Unspecified verification_state must remain unspecified."
        ),
    }


def audit_workspace(workspace, example_limit=12):
    workspace = Path(workspace)
    base = Workspace(workspace)
    if base.config().get("independent_second_wave") is not True:
        raise ValueError("Audit requires an independent Wave2 workspace")
    inventory = read(graph_path(workspace) / "INVENTORY.json")
    if not inventory:
        raise ValueError("Read-only audit needs the existing independent inventory")
    draft, _ = snapshot(workspace)
    observations = {**base.records("observations"), **draft["observations"]}
    sources = {**base.records("sources"), **draft["sources"]}
    return summarize_provenance(inventory, observations, sources, example_limit)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--example-limit", type=int, default=12)
    args = p.parse_args()
    result = audit_workspace(args.workspace, max(0, args.example_limit))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
