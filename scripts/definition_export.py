"""Stable, versioned, public definition feed for other reference projects.

This feed is built from the existing *production* mathDef index, after
formulations and text dependencies have been computed. It does not ingest
independent Wave 1/Wave 2 research or edit any source definitions.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

SNAPSHOT_SCHEMA = "mathdef.definition-snapshot.v1"
MANIFEST_SCHEMA = "mathdef.definition-manifest.v1"
EXPORT_PATH = Path("api/definitions/v1")


def public_entry(entry):
    """Keep the stable IDs, exact source bodies and contextual formulations."""
    formulations = entry.get("formulations") or [{
        "key": "primary",
        "label": entry.get("form_label", "Original formulation"),
        "order": entry.get("form_order", 0),
        "body": entry["body"],
        "source": entry.get("source", ""),
        "status": entry.get("status", "example"),
        "path": entry.get("path", ""),
        "dependencies": entry.get("dependencies", []),
    }]
    return {
        "id": entry["id"],
        "term": entry["term"],
        "aliases": entry.get("aliases", []),
        "body": entry["body"],
        "source": entry.get("source", ""),
        "status": entry.get("status", "example"),
        "category": entry.get("category", ""),
        "path": entry.get("path", ""),
        "related": entry.get("related", []),
        "dependencies": entry.get("dependencies", []),
        "formulations": formulations,
    }


def write_definition_export(entries, site_root):
    """Write the snapshot and change signal to the generated Pages site.

    Content-addressed versions are stable across identical rebuilds.
    Consumers GET the small manifest, then only GET the snapshot if the
    version differs from their cached copy. Publish as one Pages artifact.
    """
    output = Path(site_root) / EXPORT_PATH
    output.mkdir(parents=True, exist_ok=True)
    sorted_entries = sorted(entries, key=lambda e: e["id"])
    snapshot = {
        "schema": SNAPSHOT_SCHEMA,
        "definitions": [public_entry(e) for e in sorted_entries],
    }
    payload = (json.dumps(snapshot, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "snapshot_schema": SNAPSHOT_SCHEMA,
        "dataset": "production",
        "version": "sha256:" + digest,
        "sha256": digest,
        "definition_count": len(sorted_entries),
        "snapshot_path": "snapshot.json",
    }
    (output / "snapshot.json").write_bytes(payload)
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest
