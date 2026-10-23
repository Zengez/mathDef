"""Regression tests for the public cross-project definition snapshot."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.definition_export import (
    EXPORT_PATH, MANIFEST_SCHEMA, SNAPSHOT_SCHEMA, write_definition_export,
)


def sample(ident, term):
    return {
        "id": ident, "term": term, "aliases": [term.lower()],
        "body": "Let $X$ be a set.", "source": "https://example.org/proof",
        "status": "draft", "category": "Test", "path": "definitions/test/a.tex",
        "related": [], "dependencies": [
            {"id": "test.target", "label": "target", "start": 4, "end": 10,
             "formulation": "primary"}
        ],
    }


class ExportTests(unittest.TestCase):
    def test_stable_hash_and_change_detection(self):
        a = sample("test.a", "Alpha")
        b = sample("test.b", "Beta")
        with tempfile.TemporaryDirectory() as tmp:
            first = write_definition_export([b, a], tmp)
            path = Path(tmp) / EXPORT_PATH
            data = (path / "snapshot.json").read_bytes()
            manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema"], MANIFEST_SCHEMA)
            self.assertEqual(manifest["snapshot_schema"], SNAPSHOT_SCHEMA)
            self.assertEqual(manifest["sha256"], hashlib.sha256(data).hexdigest())
            self.assertEqual(manifest["definition_count"], 2)
            self.assertEqual(manifest["snapshot_path"], "snapshot.json")
            self.assertEqual(first, write_definition_export([a, b], tmp))
            self.assertEqual(data, (path / "snapshot.json").read_bytes())
            a["body"] = "Let $Y$ be another set."
            revised = write_definition_export([b, a], tmp)
            self.assertNotEqual(first["version"], revised["version"])

    def test_source_and_contextual_formulations_preserved(self):
        a = sample("test.a", "Alpha")
        a["formulations"] = [
            {"key": "primary", "label": "Original", "body": "First",
             "source": "https://example.org/a", "dependencies": []},
            {"key": "alternate", "label": "Alternative", "body": "Second",
             "source": "https://example.org/b", "dependencies": [
                 {"id": "test.target", "formulation": "alternate", "start": 0, "end": 6}
             ]},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            write_definition_export([a, sample("test.b", "Beta")], tmp)
            data = json.loads((Path(tmp) / EXPORT_PATH / "snapshot.json").read_text())
        self.assertEqual(data["schema"], SNAPSHOT_SCHEMA)
        entries = data["definitions"]
        self.assertEqual([e["id"] for e in entries], ["test.a", "test.b"])
        self.assertEqual(entries[0]["formulations"][1]["body"], "Second")
        self.assertEqual(entries[0]["formulations"][1]["source"], "https://example.org/b")
        self.assertEqual(entries[0]["formulations"][1]["dependencies"][0]["formulation"], "alternate")
        self.assertEqual(entries[1]["formulations"][0]["key"], "primary")
        self.assertEqual(entries[1]["formulations"][0]["body"], entries[1]["body"])
        self.assertEqual(entries[1]["dependencies"][0]["id"], "test.target")


if __name__ == "__main__":
    unittest.main()
