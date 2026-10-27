"""Versioned cross-project feed of the canonical merged mathDef term library.

v1 remains the original .tex-only contract. v2 publishes ALL merged term groups,
meanings, and formulations without changing their independently recorded sources.
"""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

MERGED_EXPORT_PATH = Path("api/definitions/v2")
MERGED_MANIFEST_SCHEMA = "mathdef.definition-manifest.v2"
MERGED_SNAPSHOT_SCHEMA = "mathdef.definition-snapshot.v2"


def original_ids_for_meaning(meaning: dict) -> list[str]:
    """Original aliases survive when their mathematical meaning is consolidated."""
    ids = [meaning.get("original_definition_id"),
           *meaning.get("legacy_original_definition_ids", [])]
    return sorted(set(x for x in ids if x))





def write_merged_definition_export(catalog: dict, index: list[dict], site_root: Path) -> dict:
    groups = {g["id"]: g for g in catalog["groups"]}
    if len(groups) != len(catalog["groups"]):
        raise ValueError("Duplicate merged term group")
    if len(index) != len(groups):
        raise ValueError("Merged index missing term groups")
    original_ids = set()
    definitions = []
    meaning_ids = set()
    formulation_ids = set()
    for entry in sorted(index, key=lambda d: d["id"]):
        gid = entry["id"]
        group = groups.get(gid)
        if not group:
            raise ValueError(f"Unknown merged index term: {gid}")
        ids = [m["id"] for m in group["meanings"]]
        originals = sorted({
            oid for m in group["meanings"]
            for oid in original_ids_for_meaning(m)
        })
        if not ids or len(set(ids)) != len(ids):
            raise ValueError(f"Duplicate/empty mathematical meanings for {gid}")
        if any(i in meaning_ids for i in ids):
            raise ValueError("Mathematical meaning occurs under two headings")
        meaning_ids.update(ids)
        if any(i in original_ids for i in originals):
            raise ValueError("Original definition ID occurs under two headings")
        original_ids.update(originals)
        expected_forms = {f["id"] for m in group["meanings"]
                          for f in m["formulations"]}
        actual_forms = {f["key"] for f in entry["formulations"]}
        if len(actual_forms) != len(entry["formulations"]) or expected_forms != actual_forms:
            raise ValueError(f"Missing/duplicate rendered formulation for {gid}")
        if any(i in formulation_ids for i in actual_forms):
            raise ValueError("Formulation shared across term groups")
        formulation_ids.update(actual_forms)
        record = deepcopy(entry)
        record["original_ids"] = sorted(originals)
        record["meaning_ids"] = ids
        # The group identifier answers "which searchable heading?" while a
        # meaning identifier answers "which mathematical interpretation?".
        # Preserve both, with the source cohort, so consumers can prioritize
        # the context cited by a theorem rather than picking the first entry.
        record["meanings"] = [{
            "id": m["id"],
            "label": m.get("label", ""),
            "display_term": m.get("display_term") or group["title"],
            "source_origin": m.get("source_origin", "independent_research"),
            "research_status": m.get("research_status", "research_draft"),
            "original_definition_id": m.get("original_definition_id"),
            "legacy_original_definition_ids": m.get("legacy_original_definition_ids", []),
            "subject": m.get("subject"),
            "context": m.get("context"),
            "formulation_ids": [f["id"] for f in m["formulations"]],
        } for m in group["meanings"]]
        definitions.append(record)
    expected_originals = {oid for group in groups.values()
                          for m in group["meanings"]
                          for oid in original_ids_for_meaning(m)}
    expected_meanings = {m["id"] for group in groups.values()
                         for m in group["meanings"]}
    expected_forms = {f["id"] for group in groups.values()
                      for m in group["meanings"] for f in m["formulations"]}
    if (original_ids != expected_originals or meaning_ids != expected_meanings
            or formulation_ids != expected_forms or len(definitions) != len(groups)):
        raise ValueError("Merged API must exactly match canonical published corpus")
    target = Path(site_root) / MERGED_EXPORT_PATH
    target.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "schema": MERGED_SNAPSHOT_SCHEMA,
        "definitions": definitions,
        # Cross-project consumers can resolve old group/meaning/formulation
        # identifiers to the surviving cleaned meaning without rewriting any
        # frozen research source records.
        "consolidated_ids": deepcopy(catalog.get("consolidated_ids", {})),
    }
    payload = (json.dumps(snapshot, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    sha = hashlib.sha256(payload).hexdigest()
    manifest = {
        "schema": MERGED_MANIFEST_SCHEMA,
        "snapshot_schema": MERGED_SNAPSHOT_SCHEMA,
        "dataset": "merged",
        "version": "sha256:" + sha,
        "sha256": sha,
        "definition_count": len(definitions),
        "meaning_count": len(meaning_ids),
        "formulation_count": len(formulation_ids),
        "original_definition_count": len(original_ids),
        "retired_group_alias_count": len(catalog.get("consolidated_ids", {}).get("group_aliases", {})),
        "retired_meaning_alias_count": len(catalog.get("consolidated_ids", {}).get("meaning_aliases", {})),
        "retired_formulation_alias_count": len(catalog.get("consolidated_ids", {}).get("formulation_aliases", {})),
        "snapshot_path": "snapshot.json",
    }
    (target / "snapshot.json").write_bytes(payload)
    (target / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest
