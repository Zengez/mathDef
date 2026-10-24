"""Regression tests for the source-free, read-only global audit workflow."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import PipelineError, Workspace, digest
from research_pipeline.engine.dependency_graph import (
    graph_path, inventory_sync, live_nodes, read, store,
)
from research_pipeline.engine.dependency_audit_acceleration import (
    audit_fingerprint, math_signature, rank_findings, validate_review_ledger,
)
from research_pipeline.engine.dependency_review_submit import (
    review_packet_collection, stage_reviewed_packets,
)
from research_pipeline.engine.dependency_global_audit import (
    analyze_snapshot, build_review_packages, candidate_leads,
    candidate_review_bundle, load_live_snapshot, strongly_connected,
    write_offline_packets,
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

    def test_small_groupoid_scope_checks_respect_explicit_size(self):
        # A generic groupoid has invertible arrows but does not require
        # smallness; the only existing groupoid meaning in this fixture is
        # explicitly small. Review leads must honor both size declarations
        # and the typed Groupoids target category, not escaped regex text.
        snapshot = self.snapshot()
        small_id = "meaning.wave2.foundation.small-groupoid"
        snapshot["inventory"]["meanings"][small_id] = {
            "display_term": "Small groupoid"}
        ref = snapshot["nodes"]["form.alpha"]["references"][0]
        ref["phrase"] = "groupoid G"
        ref["target_meaning_id"] = small_id
        source = snapshot["inventory"]["formulations"]["form.alpha"]

        source["text"] = "For a groupoid G, every arrow has an inverse."
        flags = analyze_snapshot(snapshot)["flags"]
        self.assertEqual(
            sum(f["code"] == "groupoid_size_scope" for f in flags), 1)

        source["text"] = "For a small groupoid G, every arrow has an inverse."
        flags = analyze_snapshot(snapshot)["flags"]
        self.assertFalse(any(f["code"] == "groupoid_size_scope" for f in flags))

        source["text"] = "A functor F:C→Groupoids assigns a groupoid to each C-object."
        flags = analyze_snapshot(snapshot)["flags"]
        self.assertFalse(any(f["code"] == "groupoid_size_scope" for f in flags))

        source["text"] = "The functor assigns a groupoid via preGroupoids data."
        flags = analyze_snapshot(snapshot)["flags"]
        self.assertEqual(
            sum(f["code"] == "groupoid_size_scope" for f in flags), 1)

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

    def test_focus_queue_prioritizes_canonical_recurrence_without_edits(self):
        snapshot = self.snapshot()
        snapshot["candidates"] = [
            {"id": "missing.top", "status": "unresearched",
             "query": "a high-impact missing construction",
             "context": "Category theory: specified diagram source",
             "occurrence_count": 7, "upstream_formulation_count": 2,
             "incoming_formulation_ids": ["form.alpha", "form.beta"]},
            {"id": "missing.low", "status": "unresearched",
             "query": "low-impact object",
             "context": "Ring theory: distinct construction",
             "occurrence_count": 1, "upstream_formulation_count": 1,
             "incoming_formulation_ids": ["form.beta"]},
            {"id": "missing.alias", "status": "alias",
             "alias_of": "missing.top", "query": "renamed construction",
             "occurrence_count": 15,
             "incoming_formulation_ids": ["form.alpha"]},
            {"id": "missing.resolved", "status": "resolved",
             "resolved_target_meaning_id": "meaning.beta",
             "query": "already covered", "occurrence_count": 20,
             "incoming_formulation_ids": ["form.alpha"]},
        ]
        before = {p.name: p.read_bytes()
                  for p in self.graph.iterdir() if p.is_file()}
        report = candidate_review_bundle(snapshot, limit=1,
                                         max_formulations=1)
        self.assertTrue(report["read_only"])
        self.assertFalse(report["mathematics_certified"])
        self.assertFalse(report["automatic_aliases_or_edits"])
        self.assertEqual(report["active_canonical_candidates"], 2)
        self.assertEqual(report["candidates"][0]["candidate_id"], "missing.top")
        self.assertEqual(report["candidates"][0]["sources_truncated"], 1)
        source = report["candidates"][0]["source_formulations"][0]
        self.assertEqual(source["full_source_text"],
                         self.inv["formulations"]["form.alpha"]["text"])
        self.assertEqual(source["effective_node_sha256"],
                         digest(self.snapshot()["nodes"]["form.alpha"]))
        self.assertEqual(len(source["all_effective_references"]), 2)
        self.assertEqual(before, {p.name: p.read_bytes()
                                  for p in self.graph.iterdir() if p.is_file()})
        selected = candidate_review_bundle(
            snapshot, candidate_ids=("missing.low",), contains="unmatched",
            max_formulations=4)
        self.assertEqual(selected["candidates"][0]["candidate_id"], "missing.low")
        self.assertEqual(selected["candidates"][0]["sources_truncated"], 0)
        with self.assertRaises(PipelineError):
            candidate_review_bundle(snapshot, candidate_ids=("missing.alias",))
        with self.assertRaises(PipelineError):
            candidate_review_bundle(snapshot, max_formulations=0)

    def test_focus_bundle_retains_context_specific_alias_source_phrases(self):
        # Canonical query labels must not replace a source's different
        # mathematical predicate (e.g., closed versus convex supersets).
        snapshot = self.snapshot()
        node = snapshot["nodes"]["form.alpha"]
        node["references"][0] = {
            "phrase": "intersection of convex supersets",
            "state": "missing",
            "context": "Set theory: intersection over all convex supersets.",
            "missing_candidate_id": "missing.convex",
            "occurrence_id": "occ.context.1",
        }
        snapshot["candidates"] = [{
            "id": "missing.closed",
            "query": "intersection of all closed supersets",
            "context": "Set theory: arbitrary family intersection",
            "status": "unresearched",
            "alias_ids": ["missing.convex"],
            "incoming_formulation_ids": ["form.alpha"],
            "occurrence_count": 1,
        }]
        result = candidate_review_bundle(
            snapshot, candidate_ids=("missing.closed",),
            max_formulations=4)
        item = result["candidates"][0]
        self.assertEqual(item["query"],
                         "intersection of all closed supersets")
        observed = item["source_formulations"][0]["matching_source_references"]
        self.assertEqual(len(observed), 1)
        self.assertEqual(observed[0]["reference_index"], 0)
        self.assertEqual(observed[0]["phrase"],
                         "intersection of convex supersets")
        self.assertEqual(observed[0]["observed_candidate_id"], "missing.convex")
        self.assertEqual(observed[0]["occurrence_id"], "occ.context.1")
        self.assertNotIn("matching_source_references",
                         snapshot["nodes"]["form.alpha"]["references"][0])

    def test_focus_queue_term_filter_and_fingerprint(self):
        snapshot = self.snapshot()
        snapshot["candidates"] = [
            {"id": "missing.ring", "status": "unresearched",
             "query": "commutative ideal", "context": "Ring theory",
             "occurrence_count": 3,
             "incoming_formulation_ids": ["form.beta"]},
            {"id": "missing.cat", "status": "unresearched",
             "query": "functor", "context": "Category theory: ordinary",
             "occurrence_count": 2,
             "incoming_formulation_ids": ["form.alpha"]},
        ]
        report = candidate_review_bundle(snapshot, contains="CATEGORY",
                                         limit=10)
        self.assertEqual([c["candidate_id"] for c in report["candidates"]],
                         ["missing.cat"])
        self.assertEqual(report["unresolved_fingerprint"],
                         snapshot["state"]["summary"]["unresolved_fingerprint"])
        self.assertEqual(report["inventory_sha256"],
                         self.inv["source_inventory_sha256"])

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

    def test_notation_conflicts_do_not_count_as_equivalence(self):
        from research_pipeline.engine.dependency_global_audit import candidate_leads
        candidates = [
            {"id": "a", "query": "map X→M_i splitting M_i→X",
             "context": "Category theory: a split map"},
            {"id": "b", "query": "map M_i→X splitting X→M_i",
             "context": "Category theory: a reverse split map"},
        ]
        lead = candidate_leads(candidates)["leads"][0]
        self.assertEqual(lead["surface_jaccard"], 1.0)
        self.assertTrue(lead["notation_conflict"])
        self.assertFalse(lead["established_equivalent"])
        self.assertLess(lead["review_priority"], lead["surface_jaccard"])
        self.assertNotEqual(math_signature(candidates[0]["query"])["arrows"],
                            math_signature(candidates[1]["query"])["arrows"])

    def test_seed_graph_cycle_coverage_includes_original_relations(self):
        snapshot = self.snapshot()
        snapshot["inventory"]["seed_relations"] = [{
            "from_formulation": "form.beta",
            "target_meaning_id": "meaning.alpha",
            "relation_id": "rel.fixture.beta-alpha"},
        ]
        # Add a scanned opposite edge, closing a cycle only when seed edges
        # are combined with the effective reference graph.
        snapshot["nodes"]["form.alpha"]["references"][0][
            "target_meaning_id"] = "meaning.beta"
        report = analyze_snapshot(snapshot)
        self.assertTrue(report["graph_cycle_includes_seed_relations"])
        self.assertEqual(report["summary"]["seed_dependency_edges"], 1)
        self.assertEqual(report["summary"]["cycle_components"], 1)

    def test_anchored_accepted_review_suppresses_only_exact_heuristic(self):
        snapshot = self.snapshot()
        snapshot["inventory"]["meanings"]["meaning.wave2.foundation.small-category"] = {
            "display_term": "Small category"}
        snapshot["nodes"]["form.alpha"]["references"][0]["target_meaning_id"] = (
            "meaning.wave2.foundation.small-category")
        first = analyze_snapshot(snapshot)
        item = next(x for x in first["flags"] if x["code"] == "category_size_scope")
        ledger = {
            **audit_fingerprint(item),
            "disposition": "accepted_as_correct", "reviewed_by": "fixture-editor",
            "rationale": ("Reviewed the full formulation and all its assumptions; "
                          "the apparent category scope is justified here by "
                          "additional conditions visible to the reviewer."),
        }
        snapshot["review_ledger"] = [ledger]
        report = analyze_snapshot(snapshot)
        self.assertEqual(report["summary"]["accepted_review_count"], 1)
        self.assertNotIn("category_size_scope", [f["code"] for f in report["flags"]])
        snapshot["nodes"]["form.alpha"]["review_rationale"] += " Context reassessed."
        stale = analyze_snapshot(snapshot)
        self.assertEqual(stale["summary"]["accepted_review_count"], 0)
        self.assertEqual(stale["summary"]["stale_review_count"], 1)
        with self.assertRaisesRegex(PipelineError, "Structural integrity"):
            validate_review_ledger([dict(ledger, code="self_dependency")])

    def test_delta_edits_preserve_unmodified_reference_fields(self):
        original = live_nodes(self.graph, self.inv)["form.alpha"]
        edit = self.change()
        edit.pop("replacement")
        edit["updates"] = {"phrase": "new mathematical target", "state": "existing",
                           "target_meaning_id": "meaning.alpha"}
        p = build_review_packages(self.snapshot(), self.manifest([edit]))
        updated = p[0]["amendments"][0]["references"]
        self.assertEqual(updated[1]["phrase"], original["references"][1]["phrase"])
        self.assertEqual(updated[1]["target_meaning_id"],
                         original["references"][1]["target_meaning_id"])
        self.assertEqual(len(updated), len(original["references"]))
        self.assertEqual(updated[0]["phrase"], "new mathematical target")

    def test_stale_target_not_allowed_in_delta_change(self):
        edit = self.change()
        edit.pop("replacement")
        edit["updates"] = {"state": "external",
                           "disposition": "This is defining local structure."}
        with self.assertRaisesRegex(PipelineError, "stale target"):
            build_review_packages(self.snapshot(), self.manifest([edit]))
        edit["remove_fields"] = ["target_meaning_id"]
        p = build_review_packages(self.snapshot(), self.manifest([edit]))
        ref = p[0]["amendments"][0]["references"][0]
        self.assertEqual(ref["state"], "external")
        self.assertNotIn("target_meaning_id", ref)

    def test_staging_is_explicit_and_does_not_push_or_touch_other_files(self):
        manifest = self.manifest([self.change()])
        manifest_path = self.root / "review-manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        packets = self.root / "offline-reviewed"
        write_offline_packets(self.root, manifest_path, packets)
        initial = review_packet_collection(self.root, packets)
        self.assertEqual(initial["packet_count"], 1)
        dry = stage_reviewed_packets(self.root, packets)
        self.assertFalse(dry["stage_performed"])
        self.assertFalse((self.graph / "inbox" /
                          "global-review-fixture-001.json").exists())
        with self.assertRaisesRegex(PipelineError, "explicit --approved"):
            stage_reviewed_packets(self.root, packets, commit=True)
        applied = stage_reviewed_packets(self.root, packets, approved=True)
        self.assertTrue(applied["stage_performed"])
        self.assertFalse(applied["commit_created"])
        self.assertFalse(applied["push_performed"])
        self.assertTrue((self.graph / "inbox" /
                         "global-review-fixture-001.json").exists())
        with self.assertRaisesRegex(PipelineError, "overwrit"):
            stage_reviewed_packets(self.root, packets)

    def test_reviewed_packet_collection_rejects_duplicate_formulation(self):
        manifest = self.manifest([self.change()])
        manifest_path = self.root / "review-manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        packets = self.root / "offline-reviewed"
        write_offline_packets(self.root, manifest_path, packets)
        first = next(packets.glob("*.json"))
        copy = json.loads(first.read_text(encoding="utf-8"))
        copy["id"] = "second-reviewed-packet"
        copy["amendments"][0]["amendment_id"] = "amend.second-reviewed-packet"
        (packets / (copy["id"] + ".json")).write_text(
            json.dumps(copy), encoding="utf-8")
        with self.assertRaisesRegex(PipelineError, "Repeated formulation"):
            review_packet_collection(self.root, packets)

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
