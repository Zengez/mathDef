"""Offline tests of the documented read-only merged feed client."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from examples.consume_mathdef_v2 import BASE_URL, sync_mathdef


def fixture(body="Original formulation."):
    snapshot = {
        "schema": "mathdef.definition-snapshot.v2",
        "definitions": [{
            "id": "preview.term.alpha", "term": "Compact space",
            "original_ids": ["topology.compactness"],
            "meanings": [
                {"id": "m.original", "formulation_ids": ["f.original"]}
            ],
            "formulations": [{
                "key": "f.original", "meaning_id": "m.original",
                "body": body
            }]
        }]
    }
    raw = (json.dumps(snapshot, ensure_ascii=False, sort_keys=True)+"\n").encode()
    digest = hashlib.sha256(raw).hexdigest()
    manifest = {
        "schema": "mathdef.definition-manifest.v2",
        "snapshot_schema": "mathdef.definition-snapshot.v2",
        "dataset": "merged",
        "version": "sha256:" + digest,
        "sha256": digest,
        "snapshot_path": "snapshot.json",
        "definition_count": 1, "meaning_count": 1, "formulation_count": 1,
        "original_definition_count": 1,
    }
    return json.dumps(manifest).encode(), raw


class MergedFeedConsumerTests(unittest.TestCase):
    def test_first_fetch_then_manifest_only_on_unchanged_version(self):
        manifest, snapshot = fixture()
        calls = []
        def get(url):
            calls.append(url)
            return manifest if url.endswith("manifest.json") else snapshot
        with tempfile.TemporaryDirectory() as tmp:
            with patch("examples.consume_mathdef_v2.get_bytes", side_effect=get):
                first, changed, fallback = sync_mathdef(Path(tmp))
                self.assertTrue(changed)
                self.assertFalse(fallback)
                self.assertEqual(first["definitions"][0]["original_ids"],
                                 ["topology.compactness"])
                repeat, changed, fallback = sync_mathdef(Path(tmp))
                self.assertFalse(changed)
                self.assertFalse(fallback)
                self.assertEqual(first, repeat)
            self.assertEqual(sum("snapshot.json" in x for x in calls), 1)
            self.assertEqual(sum("manifest.json" in x for x in calls), 2)

    def test_invalid_changed_snapshot_retains_last_verified_copy(self):
        old_m, old_s = fixture("Old formula")
        new_m, new_s = fixture("New formula")
        with tempfile.TemporaryDirectory() as tmp:
            with patch("examples.consume_mathdef_v2.get_bytes",
                       side_effect=lambda url: old_m if "manifest" in url else old_s):
                old, _, _ = sync_mathdef(Path(tmp))
            with patch("examples.consume_mathdef_v2.get_bytes",
                       side_effect=lambda url: new_m if "manifest" in url else b"CORRUPT"):
                still_old, changed, offline = sync_mathdef(Path(tmp))
            self.assertEqual(still_old, old)
            self.assertFalse(changed)
            self.assertTrue(offline)
            self.assertEqual(json.loads((Path(tmp)/"manifest.json").read_text())["sha256"],
                             json.loads(old_m)["sha256"])

    def test_updated_snapshot_replaces_cache_atomically(self):
        old_m, old_s = fixture("Old formula")
        new_m, new_s = fixture("New formula")
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp)
            for m, s in [(old_m, old_s), (new_m, new_s)]:
                with patch("examples.consume_mathdef_v2.get_bytes",
                           side_effect=lambda url, m=m, s=s: m if "manifest" in url else s):
                    updated, changed, offline = sync_mathdef(cache)
                    self.assertTrue(changed)
                    self.assertFalse(offline)
            self.assertEqual(updated["definitions"][0]["formulations"][0]["body"],
                             "New formula")
            self.assertEqual(json.loads((cache/"manifest.json").read_text())["sha256"],
                             json.loads(new_m)["sha256"])


if __name__ == "__main__":
    unittest.main()
