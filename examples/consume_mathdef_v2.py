#!/usr/bin/env python3
"""Example consumer for mathDef's PUBLIC, COMPLETE v2 mathematical-term feed.

Usage: python examples/consume_mathdef_v2.py --cache-dir .cache/mathdef
Standard-library only. Read-only: never modifies mathDef or its definitions.
The download is versioned and SHA-256-checked; transient network failures
reuse the last verified snapshot. Copy/adapt into mathThm when development
of that project resumes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import urllib.request
from pathlib import Path

BASE_URL = "https://zengez.github.io/mathDef/api/definitions/v2/"
MANIFEST_SCHEMA = "mathdef.definition-manifest.v2"
SNAPSHOT_SCHEMA = "mathdef.definition-snapshot.v2"


def get_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": "mathDef-feed-example/1.0",
        "Cache-Control": "no-cache",
    })
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read()


def check_snapshot(raw: bytes, manifest: dict) -> dict:
    if hashlib.sha256(raw).hexdigest() != manifest["sha256"]:
        raise ValueError("Snapshot checksum does not match the manifest")
    snapshot = json.loads(raw.decode("utf-8"))
    if snapshot.get("schema") != SNAPSHOT_SCHEMA:
        raise ValueError("Unrecognized snapshot schema")
    groups = snapshot.get("definitions")
    if not isinstance(groups, list) or len(groups) != manifest["definition_count"]:
        raise ValueError("Incomplete or incorrectly shaped definition snapshot")
    if len({x["id"] for x in groups}) != len(groups):
        raise ValueError("Duplicate term-group IDs")
    all_meanings = [m for g in groups for m in g["meanings"]]
    all_forms = [f for g in groups for f in g["formulations"]]
    if len(all_meanings) != manifest["meaning_count"]:
        raise ValueError("Meaning count differs from manifest")
    if len(all_forms) != manifest["formulation_count"]:
        raise ValueError("Formulation count differs from manifest")
    return snapshot


def read_cached(cache_dir: Path):
    """Return the last verified pair (manifest, snapshot) or None."""
    try:
        manifest = json.loads((cache_dir / "manifest.json").read_text("utf-8"))
        digest = manifest["sha256"]
        raw = (cache_dir / ("snapshot-" + digest + ".json")).read_bytes()
        return manifest, check_snapshot(raw, manifest)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return None


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".tmp.")
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def sync_mathdef(cache_dir: Path):
    """Return (snapshot, changed, used_offline_cache).

    A project may call this during CI builds, startup, or a scheduled refresh.
    The SHA-256 content version is an equality token, *not* a time-ordering
    or Git revision number. Never swap in a partially downloaded snapshot.
    """
    previous = read_cached(cache_dir)
    try:
        raw_manifest = get_bytes(BASE_URL + "manifest.json")
        manifest = json.loads(raw_manifest.decode("utf-8"))
        if (manifest.get("schema") != MANIFEST_SCHEMA or
            manifest.get("snapshot_schema") != SNAPSHOT_SCHEMA or
            manifest.get("dataset") != "merged" or
            manifest.get("snapshot_path") != "snapshot.json"):
            raise ValueError("This client expects the complete merged v2 feed")
        digest = manifest.get("sha256", "")
        if not isinstance(digest, str) or len(digest) != 64 or any(
            x not in "0123456789abcdef" for x in digest
        ) or manifest.get("version") != "sha256:" + digest:
            raise ValueError("Malformed version hash")
        if previous and previous[0]["sha256"] == digest:
            return previous[1], False, False
        # Query string avoids confusing a freshly deployed manifest with a
        # CDN-cached snapshot from an older Pages deployment.
        raw_snapshot = get_bytes(BASE_URL + manifest["snapshot_path"] + "?v=" + digest)
        snapshot = check_snapshot(raw_snapshot, manifest)
        cache_dir.mkdir(parents=True, exist_ok=True)
        atomic_write(cache_dir / ("snapshot-" + digest + ".json"), raw_snapshot)
        # Update the cache manifest *last*: readers always see a complete pair.
        atomic_write(cache_dir / "manifest.json", raw_manifest)
        return snapshot, True, False
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        if previous:
            print("Warning: refresh failed; using verified cached definitions:", exc)
            return previous[1], False, True
        raise RuntimeError("No live or cached verified mathDef v2 snapshot") from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=Path(".cache/mathdef"))
    args = parser.parse_args()
    snapshot, changed, offline = sync_mathdef(args.cache_dir)
    definitions = snapshot["definitions"]
    original_map = {original_id: group
                    for group in definitions for original_id in group["original_ids"]}
    print(json.dumps({
        "term_groups": len(definitions),
        "meanings": sum(len(g["meanings"]) for g in definitions),
        "formulations": sum(len(g["formulations"]) for g in definitions),
        "updated_cache": changed,
        "using_offline_cache": offline,
        "legacy_example": original_map.get("topology.compactness", {}).get("term"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
