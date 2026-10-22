"""Read-only contextual consolidation worklist regression tests."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import Workspace, digest
from research_pipeline.engine.dependency_graph import (
    graph_path, inventory_sync, live_nodes, read, store, amend,
)
from research_pipeline.engine.dependency_context_worklist import build_review_bundle


class ContextualWorklistTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        Workspace(self.root).init({
            "schema_version": 1, "project": "Fixture", "term_kind": "term",
            "content_kind": "definition", "adapter": "mathdef",
            "external_reference_mode": True, "independent_second_wave": True,
        })
        records = self.root / "records"
        entries = [
            {"id": "meaning.alpha", "display_term": "Alpha",
             "context": "Illustrative general mathematics",
             "formulations": [{
                 "id": "form.alpha",
                 "text": "Alpha uses a rare context-bound construction and Beta."}]},
            {"id": "meaning.beta", "display_term": "Beta",
             "context": "Illustrative general mathematics",
             "formulations": [{"id": "form.beta", "text": "Beta is primitive."}]},
        ]
        (records / "meanings.jsonl").write_text(
            "".join(json.dumps(x) + "\n" for x in entries), encoding="utf-8")
        (records / "relations.jsonl").write_text("", encoding="utf-8")
        inventory_sync(self.root)
        inv = read(graph_path(self.root) / "INVENTORY.json")
        store(self.root, [
            {"formulation_id": "form.alpha",
             "version_sha256": inv["formulations"]["form.alpha"]["version_sha256"],
             "complete": True,
             "review_rationale": "Exhaustively examined Alpha and its two dependencies.",
             "references": [
                 {"phrase": "rare context-bound construction",
                  "state": "unassigned",
                  "context": "A specific mathematical construction in Alpha."},
                 {"phrase": "Beta", "state": "existing",
                  "target_meaning_id": "meaning.beta"},
             ]},
            {"formulation_id": "form.beta",
             "version_sha256": inv["formulations"]["form.beta"]["version_sha256"],
             "complete": True,
             "review_rationale": "Explicitly checked complete primitive Beta.",
             "references": []},
        ])

    def test_source_enriched_bundle_uses_effective_digest_without_mutation(self):
        graph = graph_path(self.root)
        before = {
            x.name: x.read_bytes() for x in graph.iterdir() if x.is_file()
        }
        result = build_review_bundle(
            self.root, limit=5, contains="rare context")
        self.assertTrue(result["read_only"])
        self.assertFalse(result["external_definition_research_permitted"])
        self.assertEqual(result["matched_surface_groups"], 1)
        self.assertEqual(result["returned_surface_groups"], 1)
        self.assertEqual(result["groups"][0]["surface_key"],
                         "rare context-bound construction")
        entry = result["formulations"]["form.alpha"]
        node = live_nodes(graph, read(graph / "INVENTORY.json"))["form.alpha"]
        self.assertEqual(entry["effective_node_sha256"], digest(node))
        self.assertTrue(entry["complete_scan"])
        self.assertIn("rare context-bound construction",
                      entry["source_definition"])
        self.assertEqual(entry["source_meaning_id"], "meaning.alpha")
        self.assertEqual(len(entry["reference_template"]), 2)
        self.assertNotIn("occurrence_id", entry["reference_template"][0])
        self.assertEqual(entry["linked_existing_meanings"][0]["meaning_id"],
                         "meaning.beta")
        self.assertEqual(before, {
            x.name: x.read_bytes() for x in graph.iterdir() if x.is_file()
        })

    def test_filter_without_matches_and_zero_limit(self):
        empty = build_review_bundle(self.root, contains="not present")
        self.assertEqual(empty["matched_surface_groups"], 0)
        self.assertEqual(empty["formulations"], {})
        zero = build_review_bundle(self.root, limit=0)
        self.assertEqual(zero["returned_surface_groups"], 0)
        self.assertEqual(zero["formulations"], {})


    def test_repeatable_surface_filters_are_or_and_deduplicate_source_load(self):
        graph = graph_path(self.root)
        inv = read(graph / "INVENTORY.json")
        prior = live_nodes(graph, inv)["form.alpha"]
        refs = [{k: v for k, v in r.items() if k != "occurrence_id"}
                for r in prior["references"]]
        refs.append({
            "phrase": "a second unrelated mathematical construction",
            "state": "unassigned",
            "context": "Another meaning, not inferred from the surface phrase.",
        })
        amend(self.root, [{
            "amendment_id": "amend.multi-filter-fixture",
            "formulation_id": "form.alpha",
            "version_sha256": inv["formulations"]["form.alpha"]["version_sha256"],
            "expected_node_sha256": digest(prior),
            "complete": True,
            "reviewed_by": "test-fixture-reviewer",
            "review_rationale": "Independently examined both unassigned contextual phrases in the source fixture.",
            "reason": "Adds a second synthetic unresolved occurrence to test navigation-only surface selection without a semantic-equivalence inference.",
            "references": refs,
        }])
        before = {p.name: p.read_bytes() for p in graph.iterdir() if p.is_file()}
        found = build_review_bundle(
            self.root, limit=20,
            contains_any=("rare context", "second unrelated", "NO MATCH"))
        self.assertTrue(found["read_only"])
        self.assertEqual(found["matched_surface_groups"], 2)
        self.assertEqual(found["returned_surface_groups"], 2)
        self.assertEqual(len(found["formulations"]), 1)
        self.assertEqual(set(g["surface_key"] for g in found["groups"]), {
            "rare context-bound construction",
            "a second unrelated mathematical construction",
        })
        self.assertEqual(found["surface_filters_any"],
                         ["rare context", "second unrelated", "NO MATCH"])
        # Old single-filter API and combined-filter semantics remain stable.
        old = build_review_bundle(self.root, contains="rare context")
        self.assertEqual(old["matched_surface_groups"], 1)
        combined = build_review_bundle(
            self.root, contains="rare context",
            contains_any=("second unrelated",))
        self.assertEqual(combined["matched_surface_groups"], 2)
        limited = build_review_bundle(
            self.root, limit=1, contains_any=("rare", "second unrelated"))
        self.assertEqual(limited["matched_surface_groups"], 2)
        self.assertEqual(limited["returned_surface_groups"], 1)
        self.assertEqual(before, {
            p.name: p.read_bytes() for p in graph.iterdir() if p.is_file()
        })


if __name__ == "__main__":
    unittest.main()
