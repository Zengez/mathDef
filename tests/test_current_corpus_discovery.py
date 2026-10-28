"""Regression tests for recurring discovery as the canonical corpus grows."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.current_corpus_discovery import discover, normalize, read_decisions, run
from scripts.merged_definition_export import write_merged_definition_export
from scripts.validate_published_corpus import validate_site


def group(gid, title, fid, body, *, oid=None):
    return {
        "id": gid, "title": title, "aliases": [],
        "meanings": [{
            "id": "meaning." + gid,
            "label": title,
            "original_definition_id": oid,
            "source_origin": "original_mathdef" if oid else "post_wave2",
            "formulations": [{"id": fid, "text": body, "sources": []}],
        }],
    }


def example():
    a = group("group.vector", "Vector space", "form.vector",
              "A vector space is a mathematical structure.", oid="algebra.vector")
    b = group("group.ring", "Ring", "form.ring",
              "A commutative completion ring is a ring. "
              "This completion ring is a specialized mathematical ring.")
    return {"groups": [a, b], "relations": [], "consolidated_ids": {}}


def make_site(root, catalog):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    index = [
        {"id": g["id"], "term": g["title"], "aliases": list(g.get("aliases", [])),
         "formulations": [{"key": f["id"], "definition": f["text"]}
                          for m in g["meanings"] for f in m["formulations"]]}
        for g in catalog["groups"]
    ]
    (root / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
    (root / "definitions-index.json").write_text(json.dumps(index), encoding="utf-8")
    old_ids = [m["original_definition_id"] for g in catalog["groups"]
               for m in g["meanings"] if m.get("original_definition_id")]
    prior = root / "api/definitions/v1"
    prior.mkdir(parents=True, exist_ok=True)
    (prior / "snapshot.json").write_text(
        json.dumps({"definitions": [{"id": x} for x in old_ids]}), encoding="utf-8")
    (prior / "manifest.json").write_text(
        json.dumps({"definition_count": len(old_ids)}), encoding="utf-8")
    return write_merged_definition_export(catalog, index, root)


class CurrentCorpusDiscoveryTests(unittest.TestCase):
    def test_known_terms_and_high_recall_new_candidates(self):
        cat = example()
        with tempfile.TemporaryDirectory() as tmp:
            make_site(tmp, cat)
            v2 = json.loads((Path(tmp) / "api/definitions/v2/snapshot.json").read_text())
            result = discover(cat, v2)
        self.assertEqual(result["scope"]["meanings"], 2)
        self.assertEqual(result["scope"]["formulations"], 2)
        by_phrase = {e["phrase"]: e for e in result["entries"]}
        self.assertEqual(by_phrase["vector space"]["classification"], "already_defined")
        self.assertEqual(by_phrase["completion ring"]["classification"], "unreviewed_candidate")
        self.assertTrue(result["counts"]["phrase_occurrences"] >= len(result["entries"]))
        self.assertTrue(all(len(e["examples"]) <= 3 for e in result["entries"]))

    def test_recursion_automatically_recognizes_newly_published_heading(self):
        cat = example()
        with tempfile.TemporaryDirectory() as tmp:
            make_site(tmp, cat)
            first = run(Path(tmp), Path(tmp) / "results", Path(tmp) / "missing-decisions.json")
            self.assertEqual(first["scope"]["term_groups"], 2)
            cat["groups"].append(group("group.completion", "Completion ring",
                                       "form.completion", "A completion ring is a structure."))
            make_site(tmp, cat)
            second = run(Path(tmp), Path(tmp) / "new-results",
                         Path(tmp) / "missing-decisions.json")
            self.assertEqual(second["scope"]["term_groups"], 3)
            result = json.loads((Path(tmp) / "new-results/candidates.json").read_text())
            match = [e for e in result["entries"] if e["phrase"] == "completion ring"]
            self.assertEqual(len(match), 1)
            self.assertEqual(match[0]["classification"], "already_defined")
            self.assertNotEqual(first["input_feed_sha256"], second["input_feed_sha256"])

    def test_previous_editorial_decisions_do_not_auto_publish(self):
        cat = example()
        with tempfile.TemporaryDirectory() as tmp:
            make_site(tmp, cat)
            registry = Path(tmp) / "decisions.json"
            registry.write_text(json.dumps({
                "schema": "mathdef.discovery-decisions.v1",
                "decisions": [{"phrase": "completion ring", "status": "deferred",
                               "reason": "requires mathematical review"}],
            }), encoding="utf-8")
            v2 = json.loads((Path(tmp) / "api/definitions/v2/snapshot.json").read_text())
            rows = discover(cat, v2, decisions=read_decisions(registry))["entries"]
            selected = next(x for x in rows if x["phrase"] == "completion ring")
            self.assertEqual(selected["classification"], "previously_reviewed")
            self.assertEqual(selected["prior_decision"]["status"], "deferred")

    def test_manifest_sha_and_corpus_integrity_fail_closed(self):
        cat = example()
        with tempfile.TemporaryDirectory() as tmp:
            make_site(tmp, cat)
            self.assertEqual(validate_site(Path(tmp))["definition_count"], 2)
            feed = Path(tmp) / "api/definitions/v2/snapshot.json"
            feed.write_bytes(feed.read_bytes() + b" ")
            with self.assertRaisesRegex(ValueError, "sha256"):
                validate_site(Path(tmp))

    def test_adding_meanings_does_not_need_fixed_counts(self):
        cat = example()
        with tempfile.TemporaryDirectory() as tmp:
            make_site(tmp, cat)
            cat["groups"][1]["meanings"].append({
                "id": "meaning.alternate",
                "label": "Another meaning",
                "formulations": [{"id": "form.alternate", "text": "A special ring is obtained.",
                                  "sources": []}],
            })
            manifest = make_site(tmp, cat)
            current = validate_site(Path(tmp))
            self.assertEqual(current["meaning_count"], 3)
            self.assertEqual(manifest["formulation_count"], 3)
            self.assertEqual(current["definition_count"], 2)


if __name__ == "__main__":
    unittest.main()
