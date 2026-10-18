"""Prevent repeats of the Stage 3 early-sealing error.

Tests deliberately include term records with only URL locators, and source
access failures. A URL is not a definition or a completed page acquisition.
"""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import Workspace, PipelineError
from research_pipeline.engine.stage3_attempts import (
    inspect_stacks_page, require_full_attempt_coverage, run, validate_ledger)
from research_pipeline.engine.core import jsonl


SAMPLE = """<!doctype html>
<html><head><title>Section 9.10 (09GP): Algebraic closure—The Stacks project</title></head>
<body><nav>Definition 9.10.999</nav><main>
<h2>9.10 Algebraic closure</h2>
<a href="/tag/09GQ">Definition 9.10.1.</a>
A field is said to be ... (not persisted).
<a href="/tag/09GT">Lemma 9.10.2.</a>
<a href="/tag/09GW">Definition 9.10.3.</a>
</main></body></html>"""


class Stage3AttemptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.w = Workspace(self.root / "experiment")
        self.w.init({"schema_version": 1, "project": "Independent trial",
                     "term_kind": "names", "content_kind": "definitions",
                     "adapter": "mathdef", "external_reference_mode": True})
        self.sources = [
            {"id": "src.stacks", "title": "Stacks Project",
             "url": "https://stacks.math.columbia.edu/",
             "authority_reviewed": True, "rights": "locator_only", "access": "free"},
            {"id": "src.planetmath", "title": "PlanetMath",
             "url": "https://www.planetmath.org/",
             "authority_reviewed": True, "rights": "permitted", "access": "free"},
        ]
        self.terms = [
            {"id": "term.alpha", "label": "Algebraic closure",
             "source_id": "src.stacks",
             "locator": "https://stacks.math.columbia.edu/tag/09GP"},
            {"id": "term.beta", "label": "banachspace",
             "source_id": "src.planetmath",
             "locator": "https://planetmath.org/banachspace"},
        ]
        for stage, rows in (("sources", self.sources), ("terms", self.terms)):
            path = self.root / (stage + ".jsonl")
            path.write_text("".join(json.dumps(row) + "\n" for row in rows))
            self.w.ingest(stage, path)
            self.w.seal(stage)
        self.ledger = self.w.root / "state/stage3_acquisition_attempts.jsonl"
        self.report = self.w.root / "state/stage3_acquisition_report.json"

    def fetch(self, url, source, *, delay, robots_cache):
        if source["id"] == "src.planetmath":
            raise PipelineError("Robots policy unavailable; use permitted offline input")
        return SAMPLE

    def test_source_page_definition_markers_are_structural_only(self):
        row = inspect_stacks_page(SAMPLE, self.terms[0])
        self.assertEqual(row["status"], "definition_markers_found")
        self.assertEqual(row["definition_marker_count"], 2)
        self.assertEqual([x["section_number"] for x in row["definition_candidates"]],
                         ["9.10.1", "9.10.3"])
        self.assertNotIn("A field is said", json.dumps(row))
        mismatch = inspect_stacks_page(SAMPLE, {**self.terms[0], "label": "Unrelated"})
        self.assertEqual(mismatch["status"], "page_heading_mismatch")

    def test_100_percent_coverage_gate_not_just_some_terms(self):
        result = run(self.w.root, self.ledger, self.report, batch_size=1,
                     fetcher=self.fetch)
        self.assertEqual(result["attempts_accounted_for"], 1)
        self.assertEqual(result["source_terms_total"], 2)
        with self.assertRaisesRegex(PipelineError, "only 1/2"):
            require_full_attempt_coverage(self.w.root, self.ledger)
        result = run(self.w.root, self.ledger, self.report, batch_size=1,
                     fetcher=self.fetch)
        self.assertEqual(result["attempts_accounted_for"], 2)
        self.assertEqual(result["source_documents_fetched"], 1)
        self.assertEqual(result["policy_blocked"], 1)
        self.assertTrue(require_full_attempt_coverage(self.w.root, self.ledger)
                        ["every_term_attempt_accounted_for"])
        self.assertFalse(require_full_attempt_coverage(self.w.root, self.ledger)
                         ["research_scope_complete"])
        # Sealed historic Stage 3 / 4 must not be modified by the recovery.
        self.assertFalse(self.w.state("observations").get("sealed", False))
        again = run(self.w.root, self.ledger, self.report, batch_size=2,
                    fetcher=self.fetch)
        self.assertEqual(again["processed_this_batch"], 0)

    def test_transient_errors_require_retry_before_covering(self):
        calls = {"n": 0}
        def flaky(url, source, *, delay, robots_cache):
            if source["id"] == "src.planetmath":
                raise PipelineError("Robots policy unavailable")
            calls["n"] += 1
            raise OSError("Temporary upstream timeout")
        first = run(self.w.root, self.ledger, self.report, batch_size=2,
                    fetcher=flaky)
        self.assertEqual(first["retryable_fetch_errors"], 1)
        with self.assertRaises(PipelineError):
            require_full_attempt_coverage(self.w.root, self.ledger)
        second = run(self.w.root, self.ledger, self.report, batch_size=2,
                     fetcher=flaky)
        self.assertEqual(second["retryable_fetch_errors"], 0)
        self.assertEqual(second["fetch_failed_after_retries"], 1)
        self.assertEqual(calls["n"], 2)
        self.assertTrue(require_full_attempt_coverage(self.w.root, self.ledger)
                        ["every_term_attempt_accounted_for"])
        self.assertEqual(second["source_documents_fetched"], 0)

    def test_repaired_workspace_cannot_seal_stage3_without_all_attempts(self):
        # Exercise the actual engine gate, not merely the standalone checker.
        config = json.loads(self.w.config_path.read_text(encoding="utf-8"))
        config["require_full_definition_attempts"] = True
        self.w.config_path.write_text(json.dumps(config), encoding="utf-8")
        obs = {"id": "obs.fake", "term_id": "term.alpha",
               "source_id": "src.stacks",
               "locator": self.terms[0]["locator"],
               "record_kind": "locator"}
        obs_path = self.root / "obs.jsonl"
        obs_path.write_text(json.dumps(obs) + "\n", encoding="utf-8")
        self.w.ingest("observations", obs_path)
        with self.assertRaisesRegex(PipelineError, "only 0/2"):
            self.w.seal("observations")
        run(self.w.root, self.ledger, self.report, batch_size=1, fetcher=self.fetch)
        with self.assertRaisesRegex(PipelineError, "only 1/2"):
            self.w.seal("observations")
        run(self.w.root, self.ledger, self.report, batch_size=1, fetcher=self.fetch)
        sealed = self.w.seal("observations")
        self.assertEqual(sealed["total"], 1)
        self.assertTrue(sealed["sealed"])

    def test_forged_success_missing_page_digest_is_rejected(self):
        run(self.w.root, self.ledger, self.report, batch_size=2,
            fetcher=self.fetch)
        rows = jsonl(self.ledger)
        target = next(x for x in rows if x["term_id"] == "term.alpha")
        target.pop("page_content_sha256")
        self.ledger.write_text("".join(json.dumps(x)+"\n" for x in rows))
        with self.assertRaisesRegex(PipelineError, "inspected-page evidence"):
            require_full_attempt_coverage(self.w.root, self.ledger)


if __name__ == "__main__":
    unittest.main()
