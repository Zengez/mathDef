"""Portable preflight artifacts, path isolation and failure-state regression."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from research_pipeline.engine.core import PipelineError, Workspace, digest
from research_pipeline.engine.dependency_graph import apply_inbox, graph_path, inventory_sync, read, store
from research_pipeline.engine.dependency_global_audit import load_live_snapshot, write_offline_packets
from research_pipeline.engine.dependency_review_export import export_review, workspace_files


class ReviewExportTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / "repo"
        self.w = self.repo / "workspace"
        Workspace(self.w).init({"schema_version": 1, "project": "Export fixture",
                               "adapter": "fixture", "term_kind": "item",
                               "content_kind": "description", "external_reference_mode": True,
                               "independent_second_wave": True})
        meanings = [{"id": "meaning." + label, "display_term": label,
                     "context": "Synthetic", "formulations": [{
                         "id": "form." + label, "text": "Fixture " + label + "."}]}
                    for label in ["one", "two"]]
        (self.w / "records/meanings.jsonl").write_text(
            "".join(json.dumps(x) + "\n" for x in meanings))
        (self.w / "records/relations.jsonl").write_text("")
        inventory_sync(self.w)
        self.graph = graph_path(self.w)
        inv = read(self.graph / "INVENTORY.json")
        store(self.w, [{"formulation_id": "form.one",
                        "version_sha256": inv["formulations"]["form.one"]["version_sha256"],
                        "complete": True,
                        "review_rationale": "Reviewed the complete synthetic fixture and every reference.",
                        "references": [
                            {"phrase": "two", "state": "existing", "target_meaning_id": "meaning.two"},
                            {"phrase": "input a", "context": "Fixture input", "state": "missing"},
                            {"phrase": "input b", "context": "Fixture input", "state": "missing"}]},
                       {"formulation_id": "form.two",
                        "version_sha256": inv["formulations"]["form.two"]["version_sha256"],
                        "complete": True, "references": [],
                        "review_rationale": "Reviewed the complete synthetic primitive fixture."}])
        self.snapshot = load_live_snapshot(self.w)
        node = self.snapshot["nodes"]["form.one"]
        self.manifest = {
            "schema_version": 1, "id": "fixture-review",
            "inventory_sha256": inv["source_inventory_sha256"],
            "unresolved_fingerprint": self.snapshot["state"]["summary"]["unresolved_fingerprint"],
            "reviewed_by": "Fixture reviewer",
            "review_rationale": "Reviewed the entire source and all references; mechanics-only test data.",
            "changes": [{"formulation_id": "form.one", "expected_node_sha256": digest(node),
                         "expected_occurrence_id": node["references"][0]["occurrence_id"],
                         "updates": {"phrase": "explicit fixture two"},
                         "reason": "Read the entire synthetic fixture; this only tests preservation of target data."}]}
        self.reviews = self.repo / "research_pipeline/reviews/fixture"
        self.reviews.mkdir(parents=True)
        self.manifest_file = self.reviews / "manifest.json"
        self.manifest_file.write_text(json.dumps(self.manifest))
        candidates = self.snapshot["candidates"]
        self.alias_file = self.reviews / "fixture-alias.json"
        self.alias_file.write_text(json.dumps({
            "schema_version": 1, "id": "fixture-alias", "mode": "alias",
            "aliases": [{"alias_id": "alias.fixture",
                         "alias_candidate_id": candidates[0]["id"],
                         "canonical_candidate_id": candidates[1]["id"],
                         "reviewed_by": "Fixture reviewer",
                         "reason": "Explicit synthetic reviewer decision; this test does not infer identity."}]}))
        self.output = self.root / "artifacts"

    def export(self, **kwargs):
        return export_review(self.repo, "workspace", self.output,
                             manifest=self.manifest_file.relative_to(self.repo).as_posix(), **kwargs)

    def test_export_exact_packets_inputs_hashes_and_unchanged_workspace(self):
        before = workspace_files(self.w)
        report = self.export()
        self.assertEqual(report["status"], "mechanically_preflighted_not_applied")
        self.assertTrue(report["workspace_unchanged"])
        self.assertFalse(report["mathematics_certified"])
        self.assertFalse(report["automatic_submission_performed"])
        self.assertEqual(before, workspace_files(self.w))
        self.assertEqual(report["amendment"]["packet_count"], 1)
        self.assertEqual(report["amendment"]["preflight"][0]["status"],
                         "mechanically_valid_not_applied")
        for name, sha in report["artifacts"].items():
            self.assertEqual(hashlib.sha256((self.output / name).read_bytes()).hexdigest(), sha)
        self.assertEqual((self.output / "reviewed-inputs/manifest/manifest.json").read_bytes(),
                         self.manifest_file.read_bytes())
        self.assertEqual(list((self.graph / "inbox").glob("fixture*")), [])

    def test_alias_only_and_combined_requests_stay_offline(self):
        alias = self.alias_file.relative_to(self.repo).as_posix()
        before = workspace_files(self.w)
        report = export_review(self.repo, "workspace", self.output, alias_packet=alias)
        self.assertIsNone(report["amendment"])
        self.assertEqual(report["alias"]["checked_events"], 1)
        self.assertEqual(before, workspace_files(self.w))
        self.output = self.root / "combined"
        report = self.export(alias_packet=alias)
        self.assertEqual(report["alias"]["mode"], "alias")
        self.assertTrue(report["workspace_unchanged"])

    def test_stale_manifest_cleans_packets_and_retains_failed_report(self):
        self.manifest["changes"][0]["expected_node_sha256"] = "0" * 64
        self.manifest_file.write_text(json.dumps(self.manifest))
        before = workspace_files(self.w)
        with self.assertRaisesRegex(PipelineError, "stale effective"):
            self.export()
        self.assertEqual(list(p.name for p in self.output.iterdir()), ["report.json"])
        self.assertEqual(json.loads((self.output / "report.json").read_text())["status"],
                         "failed_not_applied")
        self.assertEqual(before, workspace_files(self.w))

    def test_output_never_overwrites_existing_directory_or_enters_repository(self):
        self.output.mkdir()
        sentinel = self.output / "prior-evidence.txt"
        sentinel.write_text("preserve")
        with self.assertRaisesRegex(PipelineError, "overwrite"):
            self.export()
        self.assertEqual(sentinel.read_text(), "preserve")
        self.output = self.w / "dependency_graph/inbox/unsafe"
        with self.assertRaisesRegex(PipelineError, "outside the repository"):
            self.export()
        self.assertFalse(self.output.exists())

    def test_input_containment_and_symlinks(self):
        for relative in ["../outside.json", str(self.manifest_file), "workspace/project.json"]:
            with self.assertRaises(PipelineError):
                export_review(self.repo, "workspace", self.output, manifest=relative)
        outside = self.root / "outside.json"
        outside.write_text(self.manifest_file.read_text())
        linked = self.reviews / "linked.json"
        linked.symlink_to(outside)
        with self.assertRaisesRegex(PipelineError, "escapes"):
            export_review(self.repo, "workspace", self.output,
                          manifest=linked.relative_to(self.repo).as_posix())
        (self.w / "linked-record.json").symlink_to(outside)
        with self.assertRaisesRegex(PipelineError, "symlinks"):
            self.export()
        self.assertFalse(self.output.exists())

    def test_rejects_wrong_alias_mode_and_nonobject_input(self):
        self.alias_file.write_text(json.dumps({"mode": "amend"}))
        with self.assertRaisesRegex(PipelineError, "alias packet"):
            self.export(alias_packet=self.alias_file.relative_to(self.repo).as_posix())
        self.manifest_file.write_text("[]")
        with self.assertRaisesRegex(PipelineError, "JSON object"):
            self.export()
        self.assertFalse(self.output.exists())

    def test_changed_workspace_invalidates_whole_export(self):
        def altered(*args, **kwargs):
            result = write_offline_packets(*args, **kwargs)
            (self.w / "concurrent-file.json").write_text("{}")
            return result
        with patch("research_pipeline.engine.dependency_review_export.write_offline_packets",
                   side_effect=altered):
            with self.assertRaisesRegex(PipelineError, "changed during"):
                self.export()
        report = json.loads((self.output / "report.json").read_text())
        self.assertFalse(report["workspace_unchanged"])
        self.assertEqual(report["artifacts"], {})
        self.assertFalse((self.output / "generated-amendments").exists())

    def test_changed_review_input_invalidates_export(self):
        def altered(*args, **kwargs):
            result = write_offline_packets(*args, **kwargs)
            self.manifest_file.write_text(self.manifest_file.read_text() + "\n")
            return result
        with patch("research_pipeline.engine.dependency_review_export.write_offline_packets",
                   side_effect=altered):
            with self.assertRaisesRegex(PipelineError, "changed during"):
                self.export()
        report = json.loads((self.output / "report.json").read_text())
        self.assertFalse(report["reviewed_inputs_unchanged"])
        self.assertTrue(report["workspace_unchanged"])
        self.assertEqual(report["artifacts"], {})

    def test_cli_uses_same_export_contract(self):
        command = [sys.executable, "-m", "research_pipeline.engine.dependency_review_export",
                   "--repo-root", str(self.repo), "--workspace", "workspace",
                   "--manifest", self.manifest_file.relative_to(self.repo).as_posix(),
                   "--output-dir", str(self.output)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "mechanically_preflighted_not_applied")
        again = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(again.returncode, 0)
        self.assertIn("overwrite", again.stderr)

    def test_applied_receipt_is_historical_evidence_not_a_new_proposal(self):
        # Apply only inside the disposable fixture, then export an unchanged
        # receipt-backed historical input. Production/live data is never used.
        inbox = self.graph / "inbox" / self.alias_file.name
        inbox.parent.mkdir(exist_ok=True)
        inbox.write_bytes(self.alias_file.read_bytes())
        apply_inbox(self.w)
        before = workspace_files(self.w)
        report = export_review(self.repo, "workspace", self.output,
                               alias_packet=self.alias_file.relative_to(self.repo).as_posix())
        self.assertEqual(report["status"], "already_applied_no_new_proposals")
        self.assertEqual(report["already_applied_packet_ids"], ["fixture-alias"])
        self.assertEqual(report["new_proposal_packet_ids"], [])
        self.assertEqual(before, workspace_files(self.w))

    def test_requires_explicit_request_and_correct_checkout_anchor(self):
        with self.assertRaisesRegex(PipelineError, "at least one"):
            export_review(self.repo, "workspace", self.output)
        with self.assertRaisesRegex(PipelineError, "commit does not match"):
            self.export(commit="unverified-commit")
