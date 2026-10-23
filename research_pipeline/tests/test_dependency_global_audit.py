"""Regression tests for the source-free, read-only global audit workflow."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import PipelineError, Workspace, digest
from research_pipeline.engine.dependency_graph import (
    graph_path, inventory_sync, live_nodes, read, store,
)
from research_pipeline.engine.dependency_global_audit import (
    analyze_snapshot, build_review_packages, candidate_leads,
    load_live_snapshot, strongly_connected, write_offline_packets,
)


class GlobalAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        Workspace(self.root).init({
            "schema_version": 1, "project": "Portable review fixture",
            "term_kind": "term", "content_kind": "definition",
            "adapter": "mathdef", "external_reference_mode": True,
            "independent_second_wave": True,
        })
        records = self.root / "records"
        meanings = [
            {"id": "meaning.alpha", "display_term": "Alpha",
             "context": "Category theory",
             "formulations": [{"id": "form.alpha",
                "text": "For objects X,Y of category C, an alpha is an object with two arrows."}]},
            {"id": "meaning.beta", "display_term": "Beta",
             "context": "Category theory",
             "formulations": [{"id": "form.beta",
                "text": "Beta is a mathematical structure."}]},
        ]
        (records / "meanings.jsonl").write_text(
            "".join(json.dumps(m) + "\n" for m in meanings), encoding="utf-8")
        (records / "relations.jsonl").write_text("", encoding="utf-8")
        inventory_sync(self.root)
        self.graph = graph_path(self.root)
        self.inv = read(self.graph / "INVENTORY.json")
        store(self.root, [
            {"formulation_id": "form.alpha",
             "version_sha256": self.inv["formulations"]["form.alpha"]["version_sha256"],
             "complete": True,
             "review_rationale": "Reviewed the full contextual Alpha definition and its individual references.",
             "references": [
                 {"phrase": "category C", "state": "existing",
                  "target_meaning_id": "meaning.beta"},
                 {"phrase": "other category", "state": "existing",
                  "target_meaning_id": "meaning.beta"},
             ]},
            {"formulation_id": "form.beta",
             "version_sha256": self.inv["formulations"]["form.beta"]["version_sha256"],
             "complete": True,
             "review_rationale": "Reviewed the full mathematical primitive Beta definition.",
             "references": []},
        ])

    def snapshot(self):
        return load_live_snapshot(self.root)

    def manifest(self, changes):
        snapshot = self.snapshot()
        return {
            "schema_version": 1, "id": "global-review-fixture",
            "inventory_sha256": self.inv["source_inventory_sha256"],
            "unresolved_fingerprint": snapshot["state"]["summary"]["unresolved_fingerprint"],
            "reviewed_by": "assistant-contextual-reviewer",
            "review_rationale": "Checked the full mathematical source, link target and object types against the effective node.",
            "changes": changes,
        }

    def change(self, index=0):
        prior = live_nodes(self.graph, self.inv)["form.alpha"]
        return {
            "formulation_id": "form.alpha",
            "expected_node_sha256": digest(prior),
            "reference_index": index,
            "expected_occurrence_id": prior["references"][index]["occurrence_id"],
            "reason": "This is an explicitly verified contextual change with an appropriate target.",
            "replacement": {"phrase": "category C", "state": "existing",
                            "target_meaning_id": "meaning.alpha"},
        }

    def test_global_report_does_not_mutate_live_graph(self):
        before = {p.name: p.read_bytes() for p in self.graph.iterdir() if p.is_file()}
        report = analyze_snapshot(self.snapshot(), include_effective_snapshot=True)
        self.assertTrue(report["read_only"])
        self.assertFalse(report["mathematics_certified"])
        self.assertEqual(report["summary"]["complete_effective_formulations"], 2)
        self.assertEqual(report["summary"]["cycle_components"], 0)
        self.assertEqual(report["effective_formulations"]["form.alpha"]
                         ["effective_node_sha256"],
                         digest(live_nodes(self.graph, self.inv)["form.alpha"]))
        self.assertEqual(before, {p.name: p.read_bytes()
                                  for p in self.graph.iterdir() if p.is_file()})

    def test_cycles_include_self_and_mutual(self):
        self.assertEqual(strongly_connected({"a": {"a"}, "b": {"c"},
                                             "c": {"b"}, "d": set()}),
                         [["b", "c"], ["a"]])
        self.assertEqual(strongly_connected({"a": {"b"}, "b": set()}), [])

    def test_category_scope_heuristic_is_warning_not_edit(self):
        snapshot = self.snapshot()
        # Simulate a known size-restricted target for a generic category.
        snapshot["inventory"]["meanings"]["meaning.wave2.foundation.small-category"] = {
            "display_term": "Small category"}
        snapshot["nodes"]["form.alpha"]["references"][0]["target_meaning_id"] = (
            "meaning.wave2.foundation.small-category")
        report = analyze_snapshot(snapshot)
        codes = [f["code"] for f in report["flags"]]
        self.assertIn("category_size_scope", codes)
        self.assertTrue(report["automatic_aliases_or_edits"] is False)
        self.assertFalse(report["mathematics_certified"])

    def test_candidate_surface_suggestion_never_merges(self):
        registry = [
            {"id": "missing.first", "query": "parallel arrows",
             "context": "Category theory: arrows with common domain and codomain"},
            {"id": "missing.second", "query": "parallel arrows",
             "context": "Category theory: another construction"},
            {"id": "missing.third", "query": "parallel arrows",
             "context": "Ring theory: unrelated homonym"},
        ]
        result = candidate_leads(registry)
        self.assertEqual(result["possible_pairs"], 1)
        self.assertFalse(result["leads"][0]["established_equivalent"])
        self.assertEqual(result["candidate_count"], 3)

    def test_full_node_preservation_and_two_edits_one_event(self):
        before = live_nodes(self.graph, self.inv)["form.alpha"]
        a, b = self.change(0), self.change(1)
        b["replacement"] = {"phrase": "different valid link", "state": "existing",
                            "target_meaning_id": "meaning.alpha"}
        packages = build_review_packages(self.snapshot(), self.manifest([a, b]))
        self.assertEqual(len(packages), 1)
        amendment = packages[0]["amendments"][0]
        self.assertEqual(len(amendment["references"]), 2)
        self.assertEqual(amendment["expected_node_sha256"], digest(before))
        self.assertEqual(amendment["version_sha256"], before["version_sha256"])
        self.assertEqual(len(packages[0]["amendments"]), 1)
        self.assertEqual({r["target_meaning_id"] for r in amendment["references"]},
                         {"meaning.alpha"})
        self.assertEqual(before["references"][0]["target_meaning_id"], "meaning.beta")

    def test_preparer_rejects_stale_and_duplicate_occurrences(self):
        one = self.change(0)
        stale = dict(one, expected_node_sha256="a" * 64)
        with self.assertRaisesRegex(PipelineError, "stale effective occurrence"):
            build_review_packages(self.snapshot(), self.manifest([stale]))
        with self.assertRaisesRegex(PipelineError, "Duplicate edit"):
            build_review_packages(self.snapshot(), self.manifest([one, one]))
        new_missing = dict(one, replacement={
            "phrase": "completely novel concept", "state": "missing",
            "context": "Never previously registered mathematical context",
        })
        with self.assertRaisesRegex(PipelineError, "invent missing"):
            build_review_packages(self.snapshot(), self.manifest([new_missing]))

    def test_offline_preflight_does_not_submit_to_inbox(self):
        change = self.change()
        manifest = self.manifest([change])
        manifest_path = self.root / "reviewed.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        out = self.root / "offline"
        result = write_offline_packets(self.root, manifest_path, out)
        self.assertEqual(result["packet_count"], 1)
        self.assertEqual(result["changed_formulation_count"], 1)
        self.assertEqual(result["preflight"][0]["status"],
                         "mechanically_valid_not_applied")
        self.assertEqual(list((self.graph / "inbox").glob("global-review-fixture*")), [])
        self.assertFalse(result["human_certified"])
        with self.assertRaisesRegex(PipelineError, "overwrit"):
            write_offline_packets(self.root, manifest_path, out)


if __name__ == "__main__":
    unittest.main()
