"""Deterministic crash/replay, cycle, ambiguity and version tests."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import Workspace, PipelineError
from research_pipeline.engine.dependency_graph import (
    inventory_sync, store, read, graph_path, tree, propose, research_queue, missing_key)
from research_pipeline.adapters.mathdef.dependency_scan import propose as lexical


class DependencyGraphTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        Workspace(self.root).init({
            "schema_version": 1, "project": "Independent fixture", "term_kind": "term",
            "content_kind": "definition", "adapter": "mathdef",
            "external_reference_mode": True, "independent_second_wave": True})
        self.meanings = []
        self.relations = []

    def add(self, name, text, context="Algebra"):
        key = name.casefold().replace(" ", "-")
        mid, fid = "meaning." + key, "form." + key
        self.meanings.append({"id": mid, "display_term": name, "context": context,
                              "formulations": [{"id": fid, "text": text}]})
        return mid, fid

    def write_fixture(self):
        records = self.root / "records"
        (records / "meanings.jsonl").write_text(
            "".join(json.dumps(x) + "\n" for x in self.meanings), encoding="utf-8")
        (records / "relations.jsonl").write_text(
            "".join(json.dumps(x) + "\n" for x in self.relations), encoding="utf-8")
        return inventory_sync(self.root)

    def entry(self, fid, references, complete=True):
        inv = read(graph_path(self.root) / "INVENTORY.json")
        return {"formulation_id": fid,
                "version_sha256": inv["formulations"][fid]["version_sha256"],
                "references": references, "complete": complete,
                "review_rationale": ("Explicit review of every token and mathematical dependency "
                                     "in this specific illustrative formulation.") if complete else ""}

    def ref(self, name):
        return {"state": "existing", "phrase": name,
                "target_meaning_id": "meaning." + name.casefold()}

    def test_cycle_closes_and_rooted_view_is_finite(self):
        for name, target in (("A", "B"), ("B", "C"), ("C", "A")):
            self.add(name, target)
        before = self.write_fixture()
        self.assertEqual(before["unscanned"], 3)
        result = store(self.root, [self.entry("form." + name.casefold(), [self.ref(target)])
                              for name, target in (("A", "B"), ("B", "C"), ("C", "A"))])
        self.assertEqual(result["closed"], 3)
        self.assertEqual(result["open"], 0)
        view = tree(self.root, "form.a")
        c_to_a = view["children"][0]["formulations"][0]["children"][0]["formulations"][0]["children"][0]["formulations"][0]
        self.assertTrue(c_to_a["cycle"])
        self.assertEqual(c_to_a["formulation_id"], "form.a")

    def test_shared_missing_and_incremental_resolution(self):
        self.add("A", "depends on Missing C")
        self.add("B", "depends on Missing C")
        self.write_fixture()
        ref = {"phrase": "Missing C", "context": "Algebra", "state": "missing"}
        result = store(self.root, [self.entry("form.a", [ref]), self.entry("form.b", [ref])])
        self.assertEqual(result["missing_candidates"], 1)
        self.assertEqual(result["missing_occurrences"], 2)
        self.assertEqual(result["open"], 2)
        self.assertEqual(read(graph_path(self.root) / "CHECKPOINT.json")["valid_node_snapshot_count"], 2)
        # Clean-process restart: rebuild does not reparse either saved node.
        prior = read(graph_path(self.root) / "nodes/form.a.json")
        self.assertEqual(inventory_sync(self.root)["scan_complete"], 2)
        self.assertEqual(prior, read(graph_path(self.root) / "nodes/form.a.json"))
        queue = research_queue(self.root)
        self.assertEqual(queue["candidates"][0]["upstream_formulation_count"], 2)
        self.assertEqual(queue["phase"], "research_missing_dependencies")

    def test_uncommitted_partial_and_marker_recovery(self):
        self.add("A", "B")
        self.add("B", "primitive")
        self.write_fixture()
        graph = graph_path(self.root)
        first = self.entry("form.a", [self.ref("B")])
        store(self.root, [first])
        # Incomplete JSON never counts as scanned.
        (graph / "nodes" / "form.b.json").write_text('{"schema_version": 1', encoding="utf-8")
        self.assertEqual(inventory_sync(self.root)["scan_complete"], 1)
        # Fully serialized adjacency with missing/incorrect manifest hash is invalid.
        (graph / "nodes" / "form.b.json").write_text(json.dumps({
            "schema_version": 1, "formulation_id": "form.b",
            "version_sha256": self.entry("form.b", [])["version_sha256"],
            "scan_status": "complete", "references": [],
        }), encoding="utf-8")
        self.assertEqual(inventory_sync(self.root)["scan_complete"], 1)
        self.assertEqual(store(self.root, [self.entry("form.b", [])])["closed"], 2)
        self.assertEqual(inventory_sync(self.root)["scan_complete"], 2)

    def test_stale_formulation_reopens_ancestors_without_rescanning(self):
        self.add("A", "B")
        self.add("B", "constant")
        self.write_fixture()
        store(self.root, [self.entry("form.a", [self.ref("B")]),
                          self.entry("form.b", [])])
        self.assertEqual(read(graph_path(self.root) / "STATE.json")["summary"]["closed"], 2)
        self.meanings[1]["formulations"][0]["text"] = "A revised definition"
        result = self.write_fixture()
        self.assertEqual(result["scan_complete"], 1)
        self.assertEqual(result["open"], 2)
        self.assertEqual(result["changed_or_added_formulations"], 1)
        with self.assertRaises(PipelineError):
            store(self.root, [self.entry("form.a", [self.ref("B")]),
                              {"formulation_id": "form.b", "version_sha256": "stale",
                               "references": [], "complete": True}])

    def test_ambiguous_homonyms_are_not_confident_links(self):
        self.meanings.extend([
            {"id": "meaning.closure.top", "display_term": "closure",
             "context": "Topology", "formulations": [{"id": "form.top", "text": "subsets"}]},
            {"id": "meaning.closure.field", "display_term": "closure",
             "context": "Field theory", "formulations": [{"id": "form.field", "text": "extensions"}]},
            {"id": "meaning.test", "display_term": "test", "context": "Algebra",
             "formulations": [{"id": "form.test", "text": "the closure is given"}]},
        ])
        self.write_fixture()
        inv = read(graph_path(self.root) / "INVENTORY.json")
        refs = lexical(inv["formulations"]["form.test"], inv["meanings"])
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0]["state"], "ambiguous")
        self.assertEqual(len(refs[0]["candidate_meaning_ids"]), 2)
        result = store(self.root, [self.entry("form.test", refs, complete=False)])
        self.assertEqual(result["scan_incomplete"], 1)
        self.assertEqual(result["closed"], 0)

    def test_proposals_not_exhaustive_and_replays_are_idempotent(self):
        self.add("A", "the B implies B")
        self.add("B", "constant")
        self.write_fixture()
        result = propose(self.root, "research_pipeline.adapters.mathdef.dependency_scan")
        self.assertEqual(result["proposed_this_run"], 2)
        self.assertEqual(result["scan_complete"], 0)
        self.assertEqual(result["closed"], 0)
        self.assertEqual(propose(self.root, "research_pipeline.adapters.mathdef.dependency_scan")["proposed_this_run"], 0)
        with self.assertRaises(PipelineError):
            store(self.root, [self.entry("form.a", [{"state": "existing",
                "phrase": "B", "target_meaning_id": "meaning.not-present"}])])

    def test_preexisting_deferred_is_inventory_seed_not_completed_scan(self):
        self.add("A", "a missing prerequisite")
        self.relations.append({"id": "rel.a", "from_formulation": "form.a",
                               "relation_type": "definition_uses",
                               "review_state": "candidate",
                               "target_query": "unresearched prerequisite"})
        summary = self.write_fixture()
        self.assertEqual(summary["missing_candidates"], 1)
        self.assertEqual(summary["unscanned"], 1)
        self.assertEqual(summary["open"], 1)
        self.assertEqual(read(graph_path(self.root) / "INVENTORY.json")["breadth_expansion"], "on_hold")


if __name__ == "__main__":
    unittest.main()
