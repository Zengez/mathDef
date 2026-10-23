"""Deterministic crash/replay, cycle, ambiguity and version tests."""
import json
import tempfile
import unittest
from unittest.mock import patch
import research_pipeline.engine.dependency_graph as graph_module
from pathlib import Path

from research_pipeline.engine.core import Workspace, PipelineError, digest
from research_pipeline.engine.dependency_graph import (
    inventory_sync, store, read, graph_path, tree, propose, research_queue, missing_key,
    resolve, amend, live_nodes, apply_inbox, alias_candidates,
     meaning_version, scan_worklist, seal_consolidation, consolidation_worklist)
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


    def test_occurrence_first_scanning_never_assigns_premature_missing_meaning(self):
        self.add("A", "an unusual notion related to B")
        self.add("B", "a basic example")
        self.write_fixture()
        fid = "form.a"
        todo = scan_worklist(self.root, limit=1)
        self.assertFalse(todo["external_research"])
        self.assertEqual(todo["total_remaining"], 2)
        self.assertIn("unusual notion", todo["items"][0]["text"])
        self.assertEqual(read(graph_path(self.root) / "STATE.json")
                         ["summary"]["phase"], "scan_and_link_existing")
        ref = {"phrase": "an unusual notion", "state": "unassigned",
               "context": "Abstract algebra: unspecified unusual notion"}
        store(self.root, [self.entry(fid, [ref]),
                          self.entry("form.b", [])])
        graph = graph_path(self.root)
        summary = read(graph / "STATE.json")["summary"]
        self.assertEqual(summary["scan_complete"], 2)
        self.assertEqual(summary["unassigned_occurrences"], 1)
        self.assertEqual(summary["unresolved_missing_candidates"], 0)
        self.assertEqual(summary["phase"], "consolidate_occurrences")
        row = json.loads((graph / "unresolved_occurrences.jsonl").read_text().strip())
        self.assertEqual(row["state"], "unassigned")
        grouped = consolidation_worklist(self.root)
        self.assertEqual(grouped["total_unresolved_occurrences"], 1)
        self.assertEqual(grouped["groups"][0]["surface_key"], "an unusual notion")
        self.assertFalse(grouped["external_definition_research_permitted"])
        self.assertEqual(research_queue(self.root)["missing_research_permitted"], False)
        self.assertEqual(research_queue(self.root)["candidates"], [])
        with self.assertRaises(PipelineError):
            seal_consolidation(self.root, {"schema_version": 1})

    def test_consolidation_gate_requires_full_scan_and_stale_gate_reopens(self):
        self.add("A", "A notion D to define later")
        self.add("B", "another notion")
        self.write_fixture()
        graph = graph_path(self.root)
        store(self.root, [self.entry("form.a", [
            {"phrase": "notion D", "state": "missing", "context": "Algebra: notion D"}]),
            self.entry("form.b", [])])
        before = read(graph / "STATE.json")["summary"]
        self.assertEqual(before["phase"], "consolidate_occurrences")
        gate = {"schema_version": 1, "inventory_sha256": before["inventory_sha256"],
                "unresolved_fingerprint": before["unresolved_fingerprint"],
                "reviewed_by": "fixture-contextual-review",
                "rationale": "All prior occurrence candidates were inspected as a complete "
                             "fixed input; the exact mathematical missing notion is D."}
        self.assertEqual(seal_consolidation(self.root, gate)["phase"],
                         "research_missing_dependencies")
        self.assertTrue(research_queue(self.root)["missing_research_permitted"])
        self.assertEqual(seal_consolidation(self.root, gate)["phase"],
                         "research_missing_dependencies")
        # A revised existing formulation makes the gate stale; do not research
        # definitions based on an old graph inventory or omitted occurrences.
        self.meanings[1]["formulations"][0]["text"] = "updated mathematical context"
        self.write_fixture()
        after = read(graph / "STATE.json")["summary"]
        self.assertEqual(after["phase"], "scan_and_link_existing")
        self.assertFalse(after["consolidation_gate_valid"])
        with self.assertRaises(PipelineError):
            seal_consolidation(self.root, gate)

    def test_inbox_limit_ignores_applied_batches_and_validates_all_receipts(self):
        self.add("A", "a mathematical example")
        self.write_fixture()
        graph = graph_path(self.root)
        inbox = graph / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        # Many previously processed batches should not starve the first new one.
        for i in range(25):
            batch = {"schema_version": 1, "id": "batch-%02d" % i,
                     "mode": "ingest", "items": []}
            (inbox / (batch["id"] + ".json")).write_text(json.dumps(batch))
        result = apply_inbox(self.root, limit=20)
        self.assertEqual(len(result["applied"]), 20)
        result = apply_inbox(self.root, limit=20)
        self.assertEqual(result["applied"], ["batch-%02d" % i for i in range(20, 25)])
        self.assertEqual(len(result["already_applied"]), 20)
        self.assertEqual(apply_inbox(self.root, limit=20)["applied"], [])
        first = inbox / "batch-00.json"
        bad = json.loads(first.read_text())
        bad["mutated"] = True
        first.write_text(json.dumps(bad))
        with self.assertRaises(PipelineError):
            apply_inbox(self.root, limit=20)

    def test_completed_tracks_recursive_existing_traversal_not_direct_missing(self):
        self.add("A", "requires B")
        self.add("B", "requires missing C")
        self.write_fixture()
        store(self.root, [self.entry("form.a", [self.ref("B")])])
        status = read(graph_path(self.root) / "STATE.json")["formulations"]
        self.assertTrue(status["form.a"]["encountered"])
        self.assertFalse(status["form.a"]["completed"])
        self.assertFalse(status["form.b"]["encountered"])
        self.assertFalse(status["form.b"]["completed"])
        store(self.root, [self.entry("form.b", [
            {"phrase": "missing C", "state": "missing", "context": "Algebra"}])])
        status = read(graph_path(self.root) / "STATE.json")["formulations"]
        self.assertTrue(status["form.a"]["completed"])
        self.assertTrue(status["form.b"]["completed"])
        self.assertEqual(status["form.a"]["structural_status"], "open")

    def test_missing_resolution_is_pinned_to_target_content(self):
        self.add("A", "missing important concept C")
        self.add("C", "initial statement")
        self.write_fixture()
        ref = {"phrase": "concept C", "context": "Algebra", "state": "missing"}
        store(self.root, [self.entry("form.a", [ref]),
                          self.entry("form.c", [])])
        graph = graph_path(self.root)
        inv = read(graph / "INVENTORY.json")
        row = {"missing_candidate_id": missing_key("concept C", "Algebra"),
               "target_meaning_id": "meaning.c",
               "target_version_sha256": meaning_version(inv, "meaning.c"),
               "review_rationale": "Explicit mathematical equivalence of missing concept C "
                                   "and the existing contextual meaning C in this fixture."}
        resolve(self.root, [row])
        self.assertEqual(read(graph / "STATE.json")["summary"]["unresolved_missing_candidates"], 0)
        self.meanings[1]["formulations"][0]["text"] = "mathematically different replacement"
        self.write_fixture()
        summary = read(graph / "STATE.json")["summary"]
        self.assertEqual(summary["unresolved_missing_candidates"], 1)
        self.assertEqual(summary["open"], 2)

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
        self.assertEqual(queue["candidate_preview_only"][0]["upstream_formulation_count"], 2)
        self.assertEqual(queue["phase"], "consolidate_occurrences")
        self.assertFalse(queue["missing_research_permitted"])

    def test_reviewed_missing_alias_deduplicates_without_erasing_occurrences(self):
        self.add("A", "the first principal construction")
        self.add("B", "the equivalent generated construction")
        self.write_fixture()
        context = "Ring theory: ideal generated by one element"
        store(self.root, [
            self.entry("form.a", [{"phrase": "principal ideal",
                                   "context": context, "state": "missing"}]),
            self.entry("form.b", [{"phrase": "generated by one element",
                                   "context": context, "state": "missing"}]),
        ])
        graph = graph_path(self.root)
        self.assertEqual(read(graph / "STATE.json")["summary"]["unresolved_missing_candidates"], 2)
        primary = missing_key("principal ideal", context)
        alternate = missing_key("generated by one element", context)
        event = {"alias_id": "alias.principal-one-generator",
                 "alias_candidate_id": alternate, "canonical_candidate_id": primary,
                 "reviewed_by": "mathematics-context-reviewer-fixture",
                 "reason": "In this identical ring-ideal context, generation by one "
                           "element defines precisely a principal ideal, not another meaning."}
        stats = alias_candidates(self.root, [event])
        self.assertEqual(stats["unresolved_missing_candidates"], 1)
        self.assertEqual(stats["alias_candidate_records"], 1)
        self.assertEqual(stats["missing_occurrences"], 2)
        candidates = [json.loads(t) for t in (graph / "missing_candidates.jsonl")
                      .read_text().splitlines() if t.strip()]
        main = next(c for c in candidates if c["id"] == primary)
        self.assertEqual(main["incoming_formulation_ids"], ["form.a", "form.b"])
        self.assertEqual(main["occurrence_count"], 2)
        alias = next(c for c in candidates if c["id"] == alternate)
        self.assertEqual(alias["status"], "alias")
        self.assertEqual(alias["alias_of"], primary)
        tree_b = tree(self.root, "form.b")
        self.assertEqual(tree_b["children"][0]["missing_candidate_id"], primary)
        self.assertEqual(alias_candidates(self.root, [event])["unresolved_missing_candidates"], 1)
        self.assertEqual(len((graph / "candidate_aliases.jsonl").read_text().splitlines()), 1)
        with self.assertRaises(PipelineError):
            alias_candidates(self.root, [dict(event, alias_id="alias.reverse",
                alias_candidate_id=primary, canonical_candidate_id=alternate)])
        with self.assertRaises(PipelineError):
            alias_candidates(self.root, [dict(event, reason="Modified old review")])
        # The second occurrence retains its immutable original scanned ID.
        original = read(graph / "nodes/form.b.json")
        self.assertEqual(original["references"][0]["missing_candidate_id"], alternate)
        self.assertEqual(inventory_sync(self.root)["unresolved_missing_candidates"], 1)

    def test_missing_resolution_propagates_and_new_missing_reopens(self):
        self.add("A", "a missing prerequisite")
        self.add("B", "another missing prerequisite")
        self.write_fixture()
        ref = {"phrase": "Missing C", "context": "Algebra", "state": "missing"}
        store(self.root, [self.entry("form.a", [ref]), self.entry("form.b", [ref])])
        self.add("C", "depends on D")
        self.write_fixture()
        self.assertEqual(inventory_sync(self.root)["unscanned"], 1)
        inv = read(graph_path(self.root) / "INVENTORY.json")
        cid = missing_key("Missing C", "Algebra")
        row = {"missing_candidate_id": cid, "target_meaning_id": "meaning.c",
               "target_version_sha256": meaning_version(inv, "meaning.c"),
               "review_rationale": "Source-backed contextual comparison in the test establishes "
                                   "that the missing prerequisite denotes exactly meaning C."}
        self.assertEqual(resolve(self.root, [row])["open"], 3)
        self.assertEqual(resolve(self.root, [row])["unresolved_missing_candidates"], 0)
        after_resolution = tree(self.root, "form.a")
        target = after_resolution["children"][0]
        self.assertEqual(target["target_meaning_id"], "meaning.c")
        self.assertEqual(target["formulations"][0]["formulation_id"], "form.c")
        self.assertEqual(target["provenance"], "scan:candidate_resolution")
        new_ref = {"phrase": "D", "context": "Algebra", "state": "missing"}
        result = store(self.root, [self.entry("form.c", [new_ref])])
        self.assertEqual(result["unresolved_missing_candidates"], 1)
        self.assertEqual(result["open"], 3)
        self.add("D", "a primitive")
        self.write_fixture()
        inv = read(graph_path(self.root) / "INVENTORY.json")
        row_d = {"missing_candidate_id": missing_key("D", "Algebra"),
                 "target_meaning_id": "meaning.d",
                 "target_version_sha256": meaning_version(inv, "meaning.d"),
                 "review_rationale": "The same narrow algebraic context makes D precisely "
                                     "the newly represented definition in this fixture."}
        resolve(self.root, [row_d])
        self.assertEqual(store(self.root, [self.entry("form.d", [])])["closed"], 4)

    def test_grouped_inbox_amendments_one_rebuild_with_individual_receipts(self):
        self.add("A", "A depends on B")
        self.add("B", "B depends on C")
        self.add("C", "C is primitive")
        self.write_fixture()
        graph = graph_path(self.root)
        store(self.root, [self.entry("form.a", []),
                          self.entry("form.b", []),
                          self.entry("form.c", [])])
        inv = read(graph / "INVENTORY.json")
        before = live_nodes(graph, inv)
        for fid, dep, serial in [("form.a", "B", "a"),
                                 ("form.b", "C", "b")]:
            event = {
                **self.entry(fid, [self.ref(dep)]),
                "amendment_id": "amend.group-" + serial,
                "expected_node_sha256": digest(before[fid]),
                "reviewed_by": "independent-contextual-fixture-reviewer",
                "reason": "Reviewed the complete source and identified this "
                          "mathematically meaningful and previously omitted "
                          "independent category dependency.",
            }
            folder = graph / "inbox"
            folder.mkdir(exist_ok=True)
            name = "group-" + serial
            (folder / (name + ".json")).write_text(json.dumps({
                "schema_version": 1, "id": name, "mode": "amend",
                "amendments": [event],
            }))
        result = apply_inbox(self.root)
        self.assertEqual(result["applied"], ["group-a", "group-b"])
        self.assertEqual(len((graph / "amendments.jsonl").read_text().splitlines()), 2)
        self.assertEqual(read(graph / "STATE.json")["summary"]
                         ["scan_amendment_event_count"], 2)
        for name in ["group-a", "group-b"]:
            receipt = read(graph / "applied" / (name + ".json"))
            self.assertEqual(receipt["status"], "applied_in_independent_graph_only")
            self.assertFalse(receipt["human_certified"])
        self.assertEqual(apply_inbox(self.root)["already_applied"],
                         ["group-a", "group-b"])

    def test_grouped_inbox_stale_second_event_rolls_back_whole_group(self):
        self.add("A", "A depends on B")
        self.add("B", "B depends on A")
        self.write_fixture()
        graph = graph_path(self.root)
        store(self.root, [self.entry("form.a", []), self.entry("form.b", [])])
        inv = read(graph / "INVENTORY.json")
        original = live_nodes(graph, inv)
        folder = graph / "inbox"
        folder.mkdir(exist_ok=True)
        for fid, dep, serial in [("form.a", "B", "a"),
                                 ("form.b", "A", "b")]:
            event = {
                **self.entry(fid, [self.ref(dep)]),
                "amendment_id": "amend.rollback-" + serial,
                "expected_node_sha256": (
                    digest(original[fid]) if serial == "a" else "f" * 64),
                "reviewed_by": "independent-contextual-fixture-reviewer",
                "reason": "Checked the entire independent source and every "
                          "preexisting graph relation prior to proposing "
                          "this illustrative append-only amendment.",
            }
            name = "rollback-" + serial
            (folder / (name + ".json")).write_text(json.dumps({
                "schema_version": 1, "id": name, "mode": "amend",
                "amendments": [event],
            }))
        with self.assertRaisesRegex(PipelineError, "Stale or missing base"):
            apply_inbox(self.root)
        self.assertFalse((graph / "amendments.jsonl").exists())
        self.assertFalse((graph / "applied" / "rollback-a.json").exists())
        self.assertFalse((graph / "applied" / "rollback-b.json").exists())
        self.assertEqual(live_nodes(graph, inv), original)

    def test_grouped_alias_inbox_one_rebuild_with_individual_receipts(self):
        for name in ("A", "B", "C"):
            self.add(name, "a distinct original mathematical source")
        self.write_fixture()
        context = "Algebraic identity in a common domain"
        store(self.root, [
            self.entry("form." + name.casefold(),
                       [{"phrase": "candidate " + name, "context": context,
                         "state": "missing"}])
            for name in ("A", "B", "C")
        ])
        graph = graph_path(self.root)
        folder = graph / "inbox"
        folder.mkdir(exist_ok=True)
        for name in ("B", "C"):
            event = {"alias_id": "alias.grouped-" + name.casefold(),
                     "alias_candidate_id": missing_key("candidate " + name, context),
                     "canonical_candidate_id": missing_key("candidate A", context),
                     "reviewed_by": "source-free-fixture-reviewer",
                     "reason": "The complete original mathematical context has "
                               "been reviewed and this is the same prerequisite."}
            batch_id = "aliases-group-" + name.casefold()
            (folder / (batch_id + ".json")).write_text(json.dumps({
                "schema_version": 1, "id": batch_id, "mode": "alias",
                "aliases": [event],
            }))
        with patch.object(graph_module, "rebuild", wraps=graph_module.rebuild) as rebuild:
            result = apply_inbox(self.root)
            self.assertEqual(rebuild.call_count, 1)
        self.assertEqual(result["applied"], ["aliases-group-b", "aliases-group-c"])
        self.assertEqual(read(graph / "STATE.json")["summary"]
                         ["unresolved_missing_candidates"], 1)
        self.assertEqual(read(graph / "STATE.json")["summary"]
                         ["alias_candidate_records"], 2)
        for name in result["applied"]:
            receipt = read(graph / "applied" / (name + ".json"))
            self.assertFalse(receipt["human_certified"])
            self.assertEqual(receipt["status"], "applied_in_independent_graph_only")
        with patch.object(graph_module, "rebuild", wraps=graph_module.rebuild) as rebuild:
            self.assertEqual(apply_inbox(self.root)["applied"], [])
            self.assertEqual(rebuild.call_count, 0)

    def test_grouped_alias_inbox_rejects_conflict_without_partial_receipts(self):
        for name in ("A", "B"):
            self.add(name, "independent underlying construction")
        self.write_fixture()
        context = "Commutative algebra source"
        store(self.root, [
            self.entry("form." + name.casefold(),
                       [{"phrase": "object " + name, "context": context,
                         "state": "missing"}])
            for name in ("A", "B")
        ])
        graph = graph_path(self.root)
        folder = graph / "inbox"
        folder.mkdir(exist_ok=True)
        for label, source, dest in (("a", "B", "A"), ("b", "A", "B")):
            batch_id = "bad-alias-" + label
            (folder / (batch_id + ".json")).write_text(json.dumps({
                "schema_version": 1, "id": batch_id, "mode": "alias",
                "aliases": [{
                    "alias_id": "alias.bad-" + label,
                    "alias_candidate_id": missing_key("object " + source, context),
                    "canonical_candidate_id": missing_key("object " + dest, context),
                    "reviewed_by": "fixture-reviewer",
                    "reason": "Two source-context identities reviewed for the "
                              "deliberately invalid cyclic alias regression.",
                }],
            }))
        with self.assertRaises(PipelineError):
            apply_inbox(self.root)
        self.assertFalse((graph / "candidate_aliases.jsonl").exists())
        self.assertFalse((graph / "applied/bad-alias-a.json").exists())
        self.assertFalse((graph / "applied/bad-alias-b.json").exists())
        self.assertEqual(read(graph / "STATE.json")["summary"]
                         ["unresolved_missing_candidates"], 2)

    def test_grouped_resolution_inbox_one_rebuild_and_mode_order(self):
        for name in ("A", "B", "C"):
            self.add(name, "a distinct independent mathematical source")
        self.write_fixture()
        context = "Module-theoretic definition context"
        store(self.root, [
            self.entry("form." + name.casefold(),
                       [{"phrase": "missing " + name, "context": context,
                         "state": "missing"}])
            for name in ("A", "B")
        ] + [self.entry("form.c", [])])
        graph = graph_path(self.root)
        inv = read(graph / "INVENTORY.json")
        folder = graph / "inbox"
        folder.mkdir(exist_ok=True)
        for name in ("A", "B"):
            batch_id = "resolutions-group-" + name.casefold()
            (folder / (batch_id + ".json")).write_text(json.dumps({
                "schema_version": 1, "id": batch_id, "mode": "resolve",
                "resolutions": [{
                    "missing_candidate_id": missing_key("missing " + name, context),
                    "target_meaning_id": "meaning.c",
                    "target_version_sha256": meaning_version(inv, "meaning.c"),
                    "review_rationale": "This reviewed prerequisite points to "
                                        "existing meaning C, in the same mathematical "
                                        "setting; not an assertion of certification.",
                }],
            }))
        with patch.object(graph_module, "rebuild", wraps=graph_module.rebuild) as rebuild:
            result = apply_inbox(self.root)
            self.assertEqual(rebuild.call_count, 1)
        self.assertEqual(result["applied"],
                         ["resolutions-group-a", "resolutions-group-b"])
        self.assertEqual(read(graph / "STATE.json")["summary"]
                         ["unresolved_missing_candidates"], 0)
        self.assertEqual(read(graph / "STATE.json")["summary"]
                         ["missing_occurrences"], 0)
        for name in result["applied"]:
            self.assertFalse(read(graph / "applied" / (name + ".json"))
                             ["human_certified"])

    def test_grouped_inbox_preserves_order_across_alias_resolve_boundaries(self):
        for name in ("A", "B", "C"):
            self.add(name, "independent source")
        self.write_fixture()
        context = "One mathematical context"
        store(self.root, [
            self.entry("form." + name.casefold(),
                       [{"phrase": "candidate " + name, "context": context,
                         "state": "missing"}])
            for name in ("A", "B")
        ] + [self.entry("form.c", [])])
        graph = graph_path(self.root)
        inv = read(graph / "INVENTORY.json")
        inbox = graph / "inbox"
        inbox.mkdir(exist_ok=True)
        alias = {"schema_version": 1, "id": "mixed-01-alias", "mode": "alias",
                 "aliases": [{
                     "alias_id": "alias.mixed",
                     "alias_candidate_id": missing_key("candidate B", context),
                     "canonical_candidate_id": missing_key("candidate A", context),
                     "reviewed_by": "fixture-reviewer",
                     "reason": "The complete original contexts have the same "
                               "mathematical prerequisite despite different naming.",
                 }]}
        resolution = {"schema_version": 1, "id": "mixed-02-resolve",
                      "mode": "resolve", "resolutions": [{
                          "missing_candidate_id": missing_key("candidate A", context),
                          "target_meaning_id": "meaning.c",
                          "target_version_sha256": meaning_version(inv, "meaning.c"),
                          "review_rationale": "After prerequisite aliasing this "
                                              "previously missing concept has the "
                                              "exact existing version-bounded meaning C.",
                      }]}
        for packet in (alias, resolution):
            (inbox / (packet["id"] + ".json")).write_text(json.dumps(packet))
        with patch.object(graph_module, "rebuild", wraps=graph_module.rebuild) as rebuild:
            result = apply_inbox(self.root)
            self.assertEqual(rebuild.call_count, 2)
        self.assertEqual(result["applied"], ["mixed-01-alias", "mixed-02-resolve"])
        self.assertEqual(read(graph / "STATE.json")["summary"]
                         ["unresolved_missing_candidates"], 0)

    def test_append_only_scan_amendment_restart_replay_and_stale_guard(self):
        self.add("A", "B and C")
        self.add("B", "a primitive")
        self.write_fixture()
        graph = graph_path(self.root)
        store(self.root, [self.entry("form.a", [self.ref("B")]),
                          self.entry("form.b", [])])
        self.assertEqual(read(graph / "STATE.json")["summary"]["closed"], 2)
        original = read(graph / "nodes/form.a.json")
        item = {
            **self.entry("form.a", [{"phrase": "C", "state": "missing",
                                     "context": "Algebra"}]),
            "amendment_id": "amend.form-a.c-found",
            "expected_node_sha256": digest(original),
            "reason": "On second exhaustive source-specific semantic review, C was "
                      "identified as a prerequisite omitted from the original pass.",
            "reviewed_by": "unit-fixture-reviewer",
        }
        first = amend(self.root, [item])
        self.assertEqual(first["missing_candidates"], 1)
        self.assertEqual(first["open"], 1)
        self.assertEqual(read(graph / "nodes/form.a.json"), original)
        self.assertEqual(len((graph / "amendments.jsonl").read_text().splitlines()), 1)
        self.assertEqual(amend(self.root, [item])["open"], 1)
        self.assertEqual(len((graph / "amendments.jsonl").read_text().splitlines()), 1)
        # Lost derived indexes do not force rescanning or erase corrections.
        (graph / "reverse_index.json").unlink()
        (graph / "STATE.json").unlink()
        self.assertEqual(inventory_sync(self.root)["missing_candidates"], 1)
        self.assertEqual(live_nodes(graph, read(graph / "INVENTORY.json"))["form.a"]
                         ["references"][0]["state"], "missing")
        rejected = dict(item, amendment_id="amend.invalid-review",
                        expected_node_sha256=digest(original))
        with self.assertRaises(PipelineError):
            amend(self.root, [rejected])
        rejected2 = dict(item, reason="Conflicting amended rationale!")
        with self.assertRaises(PipelineError):
            amend(self.root, [rejected2])
        # A second valid, chained amendment can restore a resolved dependency.
        current = live_nodes(graph, read(graph / "INVENTORY.json"))["form.a"]
        second = {
            **self.entry("form.a", [self.ref("B")]),
            "amendment_id": "amend.form-a.restore-b",
            "expected_node_sha256": digest(current),
            "reason": "Second detailed review showed the C reference was a "
                      "transcription mistake; original B dependency is appropriate.",
            "reviewed_by": "unit-fixture-reviewer",
        }
        self.assertEqual(amend(self.root, [second])["closed"], 2)
        self.assertEqual(len((graph / "amendments.jsonl").read_text().splitlines()), 2)
        self.assertEqual(read(graph / "nodes/form.a.json"), original)

    def test_corrupt_amendment_chain_reopens_not_closes(self):
        self.add("A", "B")
        self.write_fixture()
        graph = graph_path(self.root)
        store(self.root, [self.entry("form.a", [])])
        original = read(graph / "nodes/form.a.json")
        item = {**self.entry("form.a", []),
                "amendment_id": "amend.corrupt", "expected_node_sha256": digest(original),
                "reason": "Test the immutable amendment chain without trusting "
                          "a stale or corrupted reference set to certify closure.",
                "reviewed_by": "unit-fixture-reviewer"}
        amend(self.root, [item])
        file = graph / "amendments.jsonl"
        event = json.loads(file.read_text())
        event["expected_node_sha256"] = "corrupt"
        file.write_text(json.dumps(event) + "\n", encoding="utf-8")
        result = inventory_sync(self.root)
        self.assertEqual(result["unscanned"], 1)
        self.assertEqual(result["closed"], 0)

    def test_committed_graph_inbox_receipts_are_replay_safe(self):
        self.add("A", "primitive")
        self.write_fixture()
        graph = graph_path(self.root)
        inbox = graph / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        batch = {"schema_version": 1, "id": "semantic-a", "mode": "ingest",
                 "items": [self.entry("form.a", [])]}
        path = inbox / "semantic-a.json"
        path.write_text(json.dumps(batch), encoding="utf-8")
        self.assertEqual(apply_inbox(self.root)["applied"], ["semantic-a"])
        self.assertEqual(read(graph / "STATE.json")["summary"]["closed"], 1)
        receipt = read(graph / "applied/semantic-a.json")
        self.assertFalse(receipt["human_certified"])
        self.assertEqual(apply_inbox(self.root)["already_applied"], ["semantic-a"])
        path.write_text(json.dumps(dict(batch, injected="tamper")), encoding="utf-8")
        with self.assertRaises(PipelineError):
            apply_inbox(self.root)
        path.write_text(json.dumps(batch), encoding="utf-8")
        # Crash after full graph mutation but before receipt: exact replay
        # must reconstruct the receipt and leave the same scanned node.
        (graph / "applied/semantic-a.json").unlink()
        result = apply_inbox(self.root)
        self.assertEqual(result["applied"], ["semantic-a"])
        self.assertEqual(read(graph / "STATE.json")["summary"]["closed"], 1)

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

    def test_cross_domain_word_is_ambiguity_not_confident_meaning(self):
        self.add("Source", "A positive integer occurs here.", "Commutative algebra")
        self.add("integer", "a foundational integer concept", "Foundational number theory")
        self.write_fixture()
        graph = graph_path(self.root)
        inv = read(graph / "INVENTORY.json")
        suggestions = lexical(inv["formulations"]["form.source"], inv["meanings"])
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0]["state"], "ambiguous")
        self.assertEqual(suggestions[0]["candidate_meaning_ids"], ["meaning.integer"])
        # Recreate an earlier adapter's overconfident lexical proposal; the
        # new adapter fingerprint refreshes ONLY this unreviewed incomplete node.
        old = [{"phrase": "integer", "span": [11, 18],
                "state": "existing", "target_meaning_id": "meaning.integer",
                "origin": "unreviewed_lexical_proposal"}]
        store(self.root, [self.entry("form.source", old, complete=False),
                          self.entry("form.integer", [], complete=True)])
        result = propose(self.root, "research_pipeline.adapters.mathdef.dependency_scan", limit=10)
        self.assertEqual(result["proposed_this_run"], 1)
        self.assertEqual(read(graph / "STATE.json")["summary"]["scan_complete"], 1)
        node = live_nodes(graph, read(graph / "INVENTORY.json"))["form.source"]
        self.assertEqual(node["references"][0]["state"], "ambiguous")
        self.assertTrue(node.get("proposal_fingerprint"))
        self.assertEqual(propose(self.root, "research_pipeline.adapters.mathdef.dependency_scan")
                         ["proposed_this_run"], 0)

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
