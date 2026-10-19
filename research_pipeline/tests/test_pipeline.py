import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import PipelineError, Workspace, jsonl
from research_pipeline.adapters.mathdef.preview import build


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.workspace = Workspace(root / "reconstruction")
        self.workspace.init({
            "schema_version": 1, "project": "Artificial Closure Sample",
            "term_kind": "mathematical name", "content_kind": "definition",
            "adapter": "mathdef", "external_reference_mode": True,
        })
        self.inputs = root / "inputs"
        self.inputs.mkdir()

    def push(self, stage, rows, **kwargs):
        file = self.inputs / (stage + ".jsonl")
        file.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
        return self.workspace.ingest(stage, file, **kwargs)

    def source(self, name="encyclopedia"):
        return {"id": name, "title": "Sample scholarly reference",
                "url": "https://example.org/definitions",
                "rights": "locator_only", "access": "free",
                "authority_reviewed": True}

    def load_all(self):
        self.push("sources", [self.source()])
        self.workspace.seal("sources")
        self.push("terms", [
            {"id": "term.closure", "label": "Closure", "source_id": "encyclopedia", "locator": "A/1"},
            {"id": "term.algebraic", "label": "Algebraic closure", "source_id": "encyclopedia", "locator": "A/2"},
        ])
        self.workspace.seal("terms")
        self.push("observations", [
            {"id": "obs.top", "term_id": "term.closure", "source_id": "encyclopedia",
             "locator": "A/1", "record_kind": "paraphrase", "text": "Every neighborhood intersects A."},
            {"id": "obs.alg", "term_id": "term.algebraic", "source_id": "encyclopedia",
             "locator": "A/2", "record_kind": "paraphrase", "text": "An algebraic extension that is algebraically closed."},
        ])
        self.workspace.seal("observations")
        self.push("meanings", [
            {"id": "top.closure", "term_group_id": "closure", "display_term": "Closure",
             "context": "Closure of a subset in a topological space",
             "term_ids": ["term.closure"], "formulations": [{
                 "id": "top.closed", "text": "Smallest closed superset of a subset.",
                 "evidence_ids": ["obs.top"], "review_state": "screened"
             }, {"id": "top.neighborhood", "text": "Every neighborhood meets the subset.",
                 "evidence_ids": ["obs.top"], "review_state": "screened"}]},
            {"id": "field.closure", "term_group_id": "closure", "display_term": "Closure",
             "context": "Algebraic closure of a field",
             "term_ids": ["term.algebraic"], "formulations": [{
                 "id": "field.algebraic", "text": "An algebraic and algebraically closed field extension.",
                 "evidence_ids": ["obs.alg"], "review_state": "screened"}]}
        ])
        self.workspace.seal("meanings")
        self.push("relations", [{
            "id": "rel.closures", "from_formulation": "top.closed",
            "target_meaning": "field.closure", "relation_type": "related_usage",
            "review_state": "screened"
        }])
        self.workspace.seal("relations")

    def test_full_pipeline_two_meanings_one_term_and_second_wave(self):
        self.load_all()
        report = self.workspace.publish()
        self.assertEqual((report["published_meanings"], report["held_meanings"]), (2, 0))
        preview = build(self.workspace.root)
        self.assertEqual((preview["groups"], preview["meanings"]), (1, 2))
        page = (self.workspace.root / "preview/index.html").read_text()
        self.assertIn("View sources", page)
        self.assertIn("Not yet manually verified", page)
        self.assertTrue((self.workspace.root / "preview/catalog.json").exists())
        forked_root = Path(self.tmp.name) / "wave2"
        lineage = self.workspace.fork_second_wave(forked_root)
        forked = Workspace(forked_root)
        self.assertEqual(lineage["mode"], "second_wave")
        self.assertEqual(len(forked.records("meanings")), 2)
        self.assertFalse(forked.state("sources").get("sealed"))
        self.assertTrue(self.workspace.state("sources").get("sealed"))
        with self.assertRaisesRegex(PipelineError, "collision"):
            self.push_conflict(forked)
        tasks = self.workspace.wave2_plan()
        self.assertEqual(tasks["tasks"], 2 * (1 + 1) + 2)
        kinds = {x["kind"] for x in jsonl(self.workspace.root / "wave2/tasks.jsonl")}
        self.assertEqual(kinds, {"discover_sources_from_term", "search_variants_in_source",
                                  "audit_relationships"})

    def test_preview_does_not_group_unrelated_concepts_from_same_source_section(self):
        self.load_all()
        self.workspace.publish()
        published = self.workspace.root / "published/catalog.json"
        catalog = json.loads(published.read_text(encoding="utf-8"))
        second = next(m for m in catalog["meanings"] if m["id"] == "field.closure")
        # Both entries retain the same source-section term_group_id, but they
        # are distinct mathematics headings and must get separate search cards.
        second["display_term"] = "Algebraic closure"
        published.write_text(json.dumps(catalog), encoding="utf-8")
        result = build(self.workspace.root)
        self.assertEqual((result["groups"], result["meanings"]), (2, 2))
        view = json.loads((self.workspace.root / "preview/catalog.json").read_text())
        by_name = {g["title"]: g for g in view["groups"]}
        self.assertEqual(set(by_name), {"Closure", "Algebraic closure"})
        self.assertEqual(len(by_name["Closure"]["meanings"]), 1)
        self.assertEqual(len(by_name["Algebraic closure"]["meanings"]), 1)
        # Do not silently expose a source-section title as an alias for an
        # otherwise unrelated mathematical concept.
        self.assertNotIn("Algebraic closure", by_name["Closure"]["aliases"])
        self.assertNotIn("Closure", by_name["Algebraic closure"]["aliases"])
        self.assertEqual(len(view["relations"]), 1)

    def push_conflict(self, forked):
        source = dict(self.source(), title="Tampered text")
        path = self.inputs / "fork_conflict.jsonl"
        path.write_text(json.dumps(source) + "\n", encoding="utf-8")
        forked.ingest("sources", path)

    def test_restart_idempotency_and_collision(self):
        source = self.source()
        first = self.push("sources", [source], batch_size=1)
        self.assertEqual(first["added"], 1)
        second = Workspace(self.workspace.root).ingest(
            "sources", self.inputs / "sources.jsonl", batch_size=1)
        self.assertEqual(second, {"added": 0, "already_present": 1, "total": 1})
        conflict = dict(source, title="Changed without an explicit revision")
        with self.assertRaisesRegex(PipelineError, "collision"):
            self.push("sources", [conflict])
        self.assertEqual(len(self.workspace.records("sources")), 1)

    def test_paid_sources_may_be_catalogued_but_not_acquired(self):
        paid = dict(self.source("subscription"), access="paid")
        self.push("sources", [paid])
        self.workspace.seal("sources")
        self.push("terms", [{"id": "term.test", "label": "Test", "source_id": "subscription",
                              "locator": "Table of contents"}])
        self.workspace.seal("terms")
        with self.assertRaisesRegex(PipelineError, "paid or unpermitted"):
            self.push("observations", [{
                "id": "obs.bad", "term_id": "term.test", "source_id": "subscription",
                "locator": "Page 1", "record_kind": "paraphrase", "text": "Never fetched"
            }])

    def test_cannot_publish_unsealed_or_non_screened(self):
        self.push("sources", [self.source()])
        with self.assertRaisesRegex(PipelineError, "not sealed"):
            self.workspace.publish()
        with self.assertRaisesRegex(PipelineError, "prior stages"):
            self.workspace.seal("terms")

    def test_content_change_requires_review_not_silent_overwrite(self):
        self.load_all()
        self.workspace.publish()
        path = self.workspace.root / "records" / "meanings.jsonl"
        text = path.read_text()
        path.write_text(text.replace("Smallest closed superset", "Altered closed superset"))
        with self.assertRaisesRegex(PipelineError, "not sealed against"):
            self.workspace.publish()


if __name__ == "__main__":
    unittest.main()
