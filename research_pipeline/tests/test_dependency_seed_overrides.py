"""Replay and provenance tests for independent Wave2 historical seed overrides."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import PipelineError, Workspace, digest
from research_pipeline.engine.dependency_graph import (
    apply_inbox, graph_path, inventory_sync, missing_key, read, store,
)
from research_pipeline.engine.dependency_seed_overrides import (
    replay_seed_overrides, scan_missing_sources,
)


class SeedOverrideReplayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        Workspace(self.root).init({
            "schema_version": 1, "project": "Seed override replay fixture",
            "term_kind": "term", "content_kind": "definition",
            "adapter": "mathdef", "external_reference_mode": True,
            "independent_second_wave": True,
        })
        self.records = self.root / "records"
        self.src = {
            "id": "meaning.terminal", "display_term": "Terminal object",
            "context": "Category theory",
            "formulations": [{"id": "form.terminal",
                "text": "A terminal object in a category C receives exactly one "
                        "morphism from each object of C."}],
        }
        self.target = {
            "id": "meaning.small", "display_term": "Small category",
            "context": "Category theory",
            "formulations": [{"id": "form.small", "text": "A small category has a "
                              "set of objects and set of arrows."}],
        }
        self.rel = {
            "id": "rel.terminal.small", "relation_type": "definition_uses",
            "from_formulation": "form.terminal", "target_meaning": "meaning.small",
            "source_phrase": "category C", "review_state": "screened",
        }
        (self.records / "meanings.jsonl").write_text(
            json.dumps(self.src) + "\n" + json.dumps(self.target) + "\n",
            encoding="utf-8")
        (self.records / "relations.jsonl").write_text(
            json.dumps(self.rel) + "\n", encoding="utf-8")
        inventory_sync(self.root)
        self.graph = graph_path(self.root)
        self.inv = read(self.graph / "INVENTORY.json")
        self.candidate = missing_key("category (unrestricted)", "Category theory")
        store(self.root, [{
            "formulation_id": "form.terminal",
            "version_sha256": self.inv["formulations"]["form.terminal"]["version_sha256"],
            "complete": True,
            "review_rationale": "Complete review of the terminal definition, category "
                                "size, and its incoming and outgoing dependency context.",
            "references": [{
                "phrase": "category (unrestricted)",
                "state": "missing",
                "context": "Category theory",
            }],
        }, {
            "formulation_id": "form.small",
            "version_sha256": self.inv["formulations"]["form.small"]["version_sha256"],
            "complete": True,
            "review_rationale": "Reviewed the complete small category definition and "
                                "its absence of further independent prerequisites.",
            "references": [],
        }])
        self.seed = self.inv["seed_relations"][0]
        self.event = {
            "schema_version": 1,
            "seed_override_id": "seedoverride.test.001",
            "relation_id": self.seed["relation_id"],
            "expected_seed_sha256": digest(self.seed),
            "expected_version_sha256":
                self.inv["formulations"]["form.terminal"]["version_sha256"],
            "expected_old_target_meaning_id": "meaning.small",
            "replacement": {
                "state": "missing", "missing_candidate_id": self.candidate,
            },
            "reviewed_by": "mathematics context reviewer",
            "review_rationale": (
                "The terminal object universal arrow property does not require "
                "the entire ambient category to be small; the registered "
                "unrestricted category prerequisite preserves that scope."
            ),
        }

    def rows(self, filename):
        path = self.graph / filename
        return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()
                if x.strip()]

    def packet(self, name="seed-test-001", event=None):
        packet = {
            "schema_version": 1, "id": name, "mode": "seed_override",
            "seed_overrides": [event or self.event],
        }
        directory = self.graph / "inbox"
        directory.mkdir(exist_ok=True)
        (directory / (name + ".json")).write_text(
            json.dumps(packet, ensure_ascii=False) + "\n", encoding="utf-8")
        return packet

    def test_override_replaces_only_effective_historical_reference(self):
        prior = read(self.graph / "STATE.json")["summary"]
        baseline = next(x for x in self.rows("occurrences.jsonl")
                        if x.get("relation_id") == self.seed["relation_id"])
        self.assertEqual(baseline["state"], "existing")
        self.assertEqual(baseline["target_meaning_id"], "meaning.small")
        before_inventory = (self.graph / "INVENTORY.json").read_bytes()
        self.packet()
        output = apply_inbox(self.root)
        self.assertEqual(output["applied"], ["seed-test-001"])
        receipt = read(self.graph / "applied" / "seed-test-001.json")
        self.assertFalse(receipt["human_certified"])
        self.assertEqual(receipt["status"], "applied_in_independent_graph_only")
        after = read(self.graph / "STATE.json")["summary"]
        self.assertNotEqual(prior["unresolved_fingerprint"],
                            after["unresolved_fingerprint"])
        self.assertEqual(after["seed_relations"], prior["seed_relations"])
        self.assertEqual(after["scan_occurrences"], prior["scan_occurrences"])
        self.assertEqual(after["missing_candidates"], prior["missing_candidates"])
        self.assertEqual(after["scan_amendment_event_count"],
                         prior["scan_amendment_event_count"])
        self.assertFalse(after["consolidation_gate_valid"])
        self.assertEqual((self.graph / "INVENTORY.json").read_bytes(),
                         before_inventory)
        self.assertEqual(len(self.rows("seed_overrides.jsonl")), 1)
        row = next(x for x in self.rows("occurrences.jsonl")
                   if x.get("relation_id") == self.seed["relation_id"])
        self.assertEqual(row["occurrence_id"], baseline["occurrence_id"])
        self.assertEqual(row["state"], "missing")
        self.assertEqual(row["missing_candidate_id"], self.candidate)
        self.assertEqual(row["original_target_meaning_id"], "meaning.small")
        self.assertEqual(row["seed_override_id"], self.event["seed_override_id"])
        self.assertFalse(any(e["occurrence_id"] == baseline["occurrence_id"]
                             for e in self.rows("edges.jsonl")))
        self.assertEqual(
            sum(x["from_formulation"] == "form.terminal" and
                x["missing_candidate_id"] == self.candidate
                for x in self.rows("unresolved_occurrences.jsonl")), 2)
        second = apply_inbox(self.root)
        self.assertEqual(second["already_applied"], ["seed-test-001"])
        self.assertEqual(len(self.rows("seed_overrides.jsonl")), 1)

    def test_bad_version_and_wrong_target_abort_before_ledger(self):
        for field, value in (
            ("expected_seed_sha256", "wrong"),
            ("expected_version_sha256", "stale"),
            ("expected_old_target_meaning_id", "meaning.other"),
        ):
            with self.subTest(field=field):
                event = {**self.event, field: value}
                self.packet("bad-" + field, event=event)
                with self.assertRaises(PipelineError):
                    apply_inbox(self.root)
                self.assertFalse((self.graph / "seed_overrides.jsonl").exists())
                self.assertFalse((self.graph / "applied" / ("bad-" + field + ".json")).exists())
                (self.graph / "inbox" / ("bad-" + field + ".json")).unlink()

    def test_noncanonical_unobserved_or_duplicate_conflict_aborts(self):
        source = scan_missing_sources({
            "form.terminal": {"references": [{
                "state": "missing", "missing_candidate_id": self.candidate
            }]}
        })
        for invalid in ({"missing.elsewhere"}, {self.candidate}):
            events = [copy.deepcopy(self.event)]
            if invalid == {self.candidate}:
                with self.assertRaises(PipelineError):
                    replay_seed_overrides(self.inv, events, source,
                                          aliased=invalid)
            else:
                events[0]["replacement"]["missing_candidate_id"] = next(iter(invalid))
                with self.assertRaises(PipelineError):
                    replay_seed_overrides(self.inv, events, source)
        duplicate = copy.deepcopy(self.event)
        duplicate["seed_override_id"] = "seedoverride.test.002"
        with self.assertRaises(PipelineError):
            replay_seed_overrides(self.inv, [self.event, duplicate], source)

    def test_changed_source_version_makes_old_event_inactive(self):
        self.packet()
        apply_inbox(self.root)
        changed_src = copy.deepcopy(self.src)
        changed_src["formulations"][0]["text"] += " This formulation was revised."
        (self.records / "meanings.jsonl").write_text(
            json.dumps(changed_src) + "\n" + json.dumps(self.target) + "\n",
            encoding="utf-8")
        inventory_sync(self.root)
        self.assertEqual(len(self.rows("seed_overrides.jsonl")), 1)
        seeded = next(x for x in self.rows("occurrences.jsonl")
                      if x.get("relation_id") == self.seed["relation_id"])
        self.assertEqual(seeded["state"], "existing")
        self.assertEqual(seeded["target_meaning_id"], "meaning.small")
        self.assertEqual(read(self.graph / "STATE.json")["summary"]["unscanned"], 1)

    def test_grouped_conflict_never_writes_seed_override_ledger(self):
        first = self.packet("a-override")
        conflicting = copy.deepcopy(self.event)
        conflicting["seed_override_id"] = "seedoverride.test.other"
        self.packet("b-override", event=conflicting)
        with self.assertRaises(PipelineError):
            apply_inbox(self.root)
        self.assertFalse((self.graph / "seed_overrides.jsonl").exists())
        self.assertFalse((self.graph / "applied" / "a-override.json").exists())
        self.assertFalse((self.graph / "applied" / "b-override.json").exists())


if __name__ == "__main__":
    unittest.main()
