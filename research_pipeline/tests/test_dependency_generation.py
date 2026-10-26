"""Synthetic-only tests for guarded gates and generation staging."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import PipelineError, Workspace
from research_pipeline.engine.dependency_graph import (
    inventory_sync, store, read, graph_path, digest, seal_consolidation,
)
from research_pipeline.engine.dependency_phase_gate import run, evaluate
from research_pipeline.engine.dependency_generation import create, stage, status
from research_pipeline.engine.population import snapshot


class PhaseGateGenerationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        Workspace(self.root).init({
            "schema_version": 1, "project": "Synthetic independent fixture",
            "term_kind": "term", "content_kind": "definition",
            "adapter": "mathdef", "external_reference_mode": True,
            "independent_second_wave": True,
        })
        self.meanings = [{
            "id": "meaning.a", "display_term": "A", "context": "Algebra",
            "formulations": [{"id": "form.a", "text": "Uses an unknown typed notion N."}]
        }]
        self.policy = self.root / "test-policy.json"
        self.write_input()
        self.write_scans()
        self.state = read(graph_path(self.root) / "STATE.json")["summary"]
        self.gate = {
            "schema_version": 1, "inventory_sha256": self.state["inventory_sha256"],
            "unresolved_fingerprint": self.state["unresolved_fingerprint"],
            "reviewed_by": "synthetic reviewer for isolated unit tests",
            "rationale": "Synthetic scoped mathematical occurrence review in a "
                         "fully classified independent fixture with one new notion."
        }
        self.policy.write_text(json.dumps({
            "schema_version": 1, "enabled": True,
            "owner_approved_standing_routine": True,
            "subsequent_routine_gates_enabled": True,
            "initial_reviewed_gate": self.gate,
        }), encoding="utf-8")

    def write_input(self):
        p = self.root / "records" / "meanings.jsonl"
        p.write_text("".join(json.dumps(x) + "\n" for x in self.meanings),
                     encoding="utf-8")
        inventory_sync(self.root)

    def write_scans(self):
        inv = read(graph_path(self.root) / "INVENTORY.json")
        entries = []
        for mid in self.meanings:
            f = mid["formulations"][0]
            refs = ([{"phrase": "unknown typed notion", "state": "missing",
                      "context": "Algebra: new notion N"}] if f["id"] == "form.a" else [])
            entries.append({
                "formulation_id": f["id"],
                "version_sha256": inv["formulations"][f["id"]]["version_sha256"],
                "references": refs, "complete": True,
                "review_rationale": "Entire isolated synthetic text was classified "
                                    "with each mathematical type checked explicitly.",
            })
        store(self.root, entries)

    def test_gate_policy_seals_only_after_valid_explicit_review(self):
        before = evaluate(self.root, self.policy)
        self.assertEqual(before["status"], "ready")
        self.assertFalse(read(graph_path(self.root) / "STATE.json")["summary"]
                         ["consolidation_gate_valid"])
        self.assertEqual(run(self.root, self.policy, apply=False)["status"], "ready")
        result = run(self.root, self.policy, apply=True)
        self.assertEqual(result["status"], "sealed")
        self.assertEqual(result["phase"], "research_missing_dependencies")
        self.assertEqual(run(self.root, self.policy, apply=True)["status"],
                         "already_valid")

    def test_gate_does_not_run_with_pending_inbox_packet(self):
        graph = graph_path(self.root)
        pending = graph / "inbox" / "reviewed-in-future.json"
        pending.parent.mkdir(parents=True, exist_ok=True)
        pending.write_text(json.dumps({
            "schema_version": 1, "id": "reviewed-in-future",
            "mode": "amend", "amendments": []
        }), encoding="utf-8")
        self.assertEqual(evaluate(self.root, self.policy)["status"],
                         "waiting_for_complete_classification")
        self.assertFalse((graph / "CONSOLIDATION.json").exists())

    def test_explicit_hold_blocks_gate(self):
        hold = self.root / "generation_staging" / "GATE_HOLDS.json"
        hold.parent.mkdir(parents=True, exist_ok=True)
        hold.write_text(json.dumps({"block_gate": True, "reason": "substantive math"}),
                        encoding="utf-8")
        self.assertEqual(run(self.root, self.policy, apply=True)["status"], "review_hold")
        self.assertFalse((graph_path(self.root) / "CONSOLIDATION.json").exists())

    def test_source_research_stages_without_mutating_graph_or_population(self):
        with self.assertRaises(PipelineError):
            create(self.root)
        run(self.root, self.policy, apply=True)
        result = create(self.root)
        self.assertEqual(result["count"], 1)
        self.assertEqual(create(self.root)["status"], "already_exists")
        manifest = read(self.root / "generation_staging" / "MANIFEST.json")
        original = manifest["candidates"][0]
        candidate = original["id"]
        self.assertEqual(original["query"], "unknown typed notion")
        state_before = (graph_path(self.root) / "STATE.json").read_bytes()
        inventory_before = (graph_path(self.root) / "INVENTORY.json").read_bytes()
        source = self.root / "generation_staging" / "research-input.json"
        record = {
            "schema_version": 1, "candidate_id": candidate,
            "original_query": "unknown typed notion",
            "disposition": "new_meaning",
            "definition": "A mathematical object of the specified new type.",
            "reasoning": "Complete mathematical argument and distinction from all "
                         "currently independently recorded contextual meanings.",
            "sources": [{"url": "https://example.org/academic-section",
                         "section": "Definition 1", "relevance": "Source supplies the definition"}],
            "comparison": {
                "accepted_meanings_sha256": manifest["accepted_meanings_file_sha256"],
                "provisional_meanings_sha256": digest(snapshot(self.root)[0]["meanings"]),
                "reviewed_accepted_independent_corpus": True,
                "reviewed_provisional_independent_corpus": True,
                "earlier_staged_candidate_ids": [],
                "rationale": "The source definition is mathematically distinct "
                             "from the accepted and provisional fixture entries."
            },
            "new_missing_dependencies": ["other notion"],
            "defer_new_missing_dependencies": True,
        }
        source.write_text(json.dumps(record), encoding="utf-8")
        self.assertEqual(stage(self.root, source)["status"], "staged")
        self.assertEqual(stage(self.root, source)["status"], "unchanged")
        self.assertTrue(status(self.root)["ready_for_reviewed_integration"])
        self.assertEqual(state_before, (graph_path(self.root) / "STATE.json").read_bytes())
        self.assertEqual(inventory_before,
                         (graph_path(self.root) / "INVENTORY.json").read_bytes())
        self.assertFalse((self.root / "population" / "records" / "meanings.jsonl").exists())

    def test_unreviewed_source_and_recursion_are_rejected(self):
        run(self.root, self.policy, apply=True)
        create(self.root)
        manifest = read(self.root / "generation_staging" / "MANIFEST.json")
        cid = manifest["candidates"][0]["id"]
        submission = self.root / "generation_staging" / "research-input.json"
        candidate = {
            "schema_version": 1, "candidate_id": cid,
            "original_query": manifest["candidates"][0]["query"],
            "disposition": "new_meaning", "definition": "Any preliminary definition with enough detail.",
            "reasoning": "Mathematical definition researched but source certification "
                         "has not been completed for the isolated test input.",
            "sources": [], "comparison": {},
        }
        submission.write_text(json.dumps(candidate), encoding="utf-8")
        with self.assertRaises(PipelineError):
            stage(self.root, submission)

    def test_future_routine_gate_requires_prior_integration_receipt(self):
        run(self.root, self.policy, apply=True)
        create(self.root)
        manifest = read(self.root / "generation_staging" / "MANIFEST.json")
        submission = self.root / "generation_staging" / "source-reviewed.json"
        submission.write_text(json.dumps({
            "schema_version": 1,
            "candidate_id": manifest["candidates"][0]["id"],
            "original_query": manifest["candidates"][0]["query"],
            "disposition": "new_meaning",
            "definition": "A new independent mathematical object with a suitable definition.",
            "reasoning": "Mathematical separation of the new object from all "
                         "existing independent meanings in the synthetic fixture.",
            "sources": [{"url": "https://example.org/math-reference",
                         "section": "Definition 1", "relevance": "Defines object N"}],
            "comparison": {
                "accepted_meanings_sha256": manifest["accepted_meanings_file_sha256"],
                "provisional_meanings_sha256": digest(snapshot(self.root)[0]["meanings"]),
                "reviewed_accepted_independent_corpus": True,
                "reviewed_provisional_independent_corpus": True,
                "earlier_staged_candidate_ids": [],
                "rationale": "The first generation in the synthetic test "
                             "has been fully checked against all existing records."
            }
        }), encoding="utf-8")
        stage(self.root, submission)
        self.meanings.append({
            "id": "meaning.b", "display_term": "B", "context": "Algebra",
            "formulations": [{"id": "form.b", "text": "The next independent definition."}]
        })
        self.write_input()
        self.write_scans()
        self.assertEqual(evaluate(self.root, self.policy)["status"],
                         "prior_generation_not_integrated")
        receipt = self.root / "generation_staging" / "INTEGRATION_RECEIPT.json"
        receipt.write_text(json.dumps({
            "status": "integration_complete",
            "prior_gate_inventory_sha256": self.gate["inventory_sha256"],
            "prior_gate_unresolved_fingerprint": self.gate["unresolved_fingerprint"],
            "global_mathematical_audit": "completed",
            "source_verification_review": "completed",
            "reviewed_by": "synthetic human review fixture",
            "review_rationale": "All source-backed candidate dispositions were "
                                "assessed and the complete first generation integrated."
        }), encoding="utf-8")
        self.assertEqual(evaluate(self.root, self.policy)["status"], "ready")
        self.assertEqual(run(self.root, self.policy, apply=True)["status"], "sealed")
        result = create(self.root)
        self.assertEqual(result["status"], "created")
        self.assertTrue((self.root / "generation_staging" / "history").is_dir())
        self.assertFalse(receipt.exists())


if __name__ == "__main__":
    unittest.main()
