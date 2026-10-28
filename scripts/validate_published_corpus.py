"""Check a generated mathDef release against its OWN canonical data, never fixed totals.

Every addition or approved cleanup propagates through the catalog, UI index,
and public v2 feed. Any missing/duplicate content or inconsistent manifest fails.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_site(root: Path) -> dict:
    root = Path(root)
    catalog = _load(root / "catalog.json")
    index = _load(root / "definitions-index.json")
    v1 = _load(root / "api/definitions/v1/snapshot.json")
    v1_manifest = _load(root / "api/definitions/v1/manifest.json")
    v2_path = root / "api/definitions/v2/snapshot.json"
    payload = v2_path.read_bytes()
    v2 = json.loads(payload)
    manifest = _load(root / "api/definitions/v2/manifest.json")
    if v2.get("schema") != "mathdef.definition-snapshot.v2" or (
        manifest.get("schema") != "mathdef.definition-manifest.v2" or
        manifest.get("dataset") != "merged"
    ):
        raise ValueError("Wrong merged feed schema/dataset")
    digest = hashlib.sha256(payload).hexdigest()
    if manifest.get("sha256") != digest or manifest.get("version") != "sha256:" + digest:
        raise ValueError("Version/sha256 does not match exported bytes")
    groups = catalog["groups"]
    group_ids = [g["id"] for g in groups]
    index_ids = [g["id"] for g in index]
    feed_entries = v2["definitions"]
    feed_ids = [g["id"] for g in feed_entries]
    if (len(set(group_ids)) != len(group_ids) or
        len(set(index_ids)) != len(index_ids) or
        len(set(feed_ids)) != len(feed_ids) or
        set(group_ids) != set(index_ids) or
        set(group_ids) != set(feed_ids)):
        raise ValueError("Group IDs missing/duplicated between catalog, UI and feed")
    by_feed = {g["id"]: g for g in feed_entries}
    meaning_ids, form_ids, original_ids = set(), set(), set()
    for group in groups:
        record = by_feed[group["id"]]
        actual_meanings = [m["id"] for m in group["meanings"]]
        actual_forms = [f["id"] for m in group["meanings"] for f in m["formulations"]]
        if not actual_meanings or not actual_forms or (
            any(m in meaning_ids for m in actual_meanings) or
            any(f in form_ids for f in actual_forms)
        ):
            raise ValueError("Missing/duplicated mathematical meanings or formulations")
        meaning_ids.update(actual_meanings)
        form_ids.update(actual_forms)
        expected_originals = {oid for m in group["meanings"] for oid in (
            [m.get("original_definition_id")] + m.get("legacy_original_definition_ids", [])
        ) if oid}
        if expected_originals & original_ids:
            raise ValueError("Original definition ID assigned to two headings")
        original_ids.update(expected_originals)
        if (set(record["meaning_ids"]) != set(actual_meanings) or
            {f["key"] for f in record["formulations"]} != set(actual_forms) or
            set(record["original_ids"]) != expected_originals or
            {m["id"] for m in record["meanings"]} != set(actual_meanings)):
            raise ValueError("Feed silently dropped content for " + group["id"])
    original_snapshot_ids = [e["id"] for e in v1["definitions"]]
    if len(set(original_snapshot_ids)) != len(original_snapshot_ids) or (
        set(original_snapshot_ids) != original_ids
    ):
        raise ValueError("Original v1 IDs are not preserved in cleaned v2")
    if v1_manifest["definition_count"] != len(original_ids):
        raise ValueError("v1 manifest count is stale")
    expected = {
        "definition_count": len(group_ids),
        "meaning_count": len(meaning_ids),
        "formulation_count": len(form_ids),
        "original_definition_count": len(original_ids),
    }
    for name, value in expected.items():
        if manifest.get(name) != value:
            raise ValueError("Stale merged manifest: " + name)
    if v2.get("consolidated_ids") != catalog.get("consolidated_ids", {}):
        raise ValueError("Feed redirects differ from canonical catalog")
    for kind in ("group_aliases", "meaning_aliases", "formulation_aliases"):
        expected_count = len(catalog.get("consolidated_ids", {}).get(kind, {}))
        if manifest.get("retired_" + kind[:-1] + "_count") != expected_count:
            raise ValueError("Stale redirected-ID count: " + kind)
    for rel in catalog["relations"]:
        if rel.get("from_formulation") not in form_ids or rel.get("target_meaning") not in meaning_ids:
            raise ValueError("Broken relation endpoint: " + str(rel.get("id")))
    return {
        **expected, "relation_count": len(catalog["relations"]),
        "sha256": digest,
        "dataset": "merged",
        "status": "complete_dynamic_corpus_verified",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--site-root", type=Path, default=Path("_site"))
    args = p.parse_args()
    print(json.dumps(validate_site(args.site_root), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
