"""Versioned merged public feed: complete meanings, stable original-id aliases."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.merged_definition_export import (
    MERGED_EXPORT_PATH, MERGED_MANIFEST_SCHEMA, MERGED_SNAPSHOT_SCHEMA,
    write_merged_definition_export,
)


def sample():
    g1 = {"id": "preview.term.a", "title": "Compact space", "meanings": [
        {"id": "meaning.mathdef.original.topology.compactness",
         "source_origin": "original_mathdef",
         "original_definition_id": "topology.compactness",
         "formulations": [{"id": "f.a", "text": "Compact metric space."}]},
        {"id": "meaning.wave2.compact.topology",
         "formulations": [{"id": "f.b", "text": "Every cover has a finite subcover."}]},
    ]}
    g2 = {"id": "preview.term.b", "title": "Open set", "meanings": [
        {"id": "meaning.wave2.open", "formulations": [
            {"id": "f.c", "text": "An element of a topology."}]},
    ]}
    idx = [
        {"id": "preview.term.a", "term": "Compact space", "aliases": ["compact"],
         "body": "Compact metric space.", "formulations": [
             {"key": "f.a", "meaning_id": "meaning.mathdef.original.topology.compactness",
              "body": "Compact metric space.", "source": "https://example.org"},
             {"key": "f.b", "meaning_id": "meaning.wave2.compact.topology",
              "body": "Every cover has a finite subcover.", "source": "https://example.org"},
         ], "dependencies": [], "related": []},
        {"id": "preview.term.b", "term": "Open set", "aliases": [],
         "body": "An element of a topology.", "formulations": [
             {"key": "f.c", "meaning_id": "meaning.wave2.open",
              "body": "An element of a topology.", "source": "https://example.org"}
         ], "dependencies": [], "related": []},
    ]
    return {"groups": [g1, g2], "relations": []}, idx


class MergedDefinitionExportTests(unittest.TestCase):
    def test_complete_versioned_feed_and_stable_original_aliases(self):
        catalog, idx = sample()
        with tempfile.TemporaryDirectory() as tmp:
            first = write_merged_definition_export(catalog, idx[::-1], tmp)
            folder = Path(tmp) / MERGED_EXPORT_PATH
            body = (folder / "snapshot.json").read_bytes()
            data = json.loads(body)
            self.assertEqual(first["schema"], MERGED_MANIFEST_SCHEMA)
            self.assertEqual(data["schema"], MERGED_SNAPSHOT_SCHEMA)
            self.assertEqual(first["dataset"], "merged")
            self.assertEqual(first["definition_count"], 2)
            self.assertEqual(first["meaning_count"], 3)
            self.assertEqual(first["formulation_count"], 3)
            self.assertEqual(first["original_definition_count"], 1)
            self.assertEqual(first["sha256"], hashlib.sha256(body).hexdigest())
            self.assertEqual(first, write_merged_definition_export(catalog, idx, tmp))
            self.assertEqual((folder / "snapshot.json").read_bytes(), body)
            by_term = {d["term"]: d for d in data["definitions"]}
            self.assertEqual(by_term["Compact space"]["original_ids"], ["topology.compactness"])
            self.assertEqual(len(by_term["Compact space"]["meaning_ids"]), 2)
            self.assertEqual(len(by_term["Compact space"]["formulations"]), 2)
            self.assertEqual([m["id"] for m in by_term["Compact space"]["meanings"]],
                             by_term["Compact space"]["meaning_ids"])
            self.assertEqual(by_term["Compact space"]["meanings"][0]["original_definition_id"],
                             "topology.compactness")
            self.assertEqual(by_term["Compact space"]["meanings"][0]["formulation_ids"],
                             ["f.a"])
            self.assertEqual(by_term["Compact space"]["meanings"][1]["formulation_ids"],
                             ["f.b"])
            idx[0]["formulations"][1]["body"] = "New researched formulation."
            changed = write_merged_definition_export(catalog, idx, tmp)
            self.assertNotEqual(changed["version"], first["version"])

    def test_unrelated_future_meaning_additions_are_accepted(self):
        catalog, idx = sample()
        catalog["groups"].append({
            "id": "preview.term.c", "title": "New mathematical concept",
            "meanings": [{
                "id": "meaning.nextwave.new", "label": "New context",
                "formulations": [{"id": "f.new", "text": "A new definition."}]
            }]
        })
        idx.append({
            "id": "preview.term.c", "term": "New mathematical concept",
            "aliases": [], "body": "A new definition.",
            "formulations": [{"key": "f.new", "body": "A new definition.",
                              "meaning_id": "meaning.nextwave.new"}],
            "dependencies": [], "related": [],
        })
        with tempfile.TemporaryDirectory() as tmp:
            manifest = write_merged_definition_export(catalog, idx, tmp)
        self.assertEqual(manifest["definition_count"], 3)
        self.assertEqual(manifest["meaning_count"], 4)

    def test_rejects_incomplete_rendered_index(self):
        catalog, idx = sample()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                write_merged_definition_export(catalog, idx[:1], tmp)
            idx[0]["formulations"].pop()
            with self.assertRaises(ValueError):
                write_merged_definition_export(catalog, idx, tmp)


if __name__ == "__main__":
    unittest.main()
