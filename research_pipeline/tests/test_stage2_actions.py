"""Isolation, resume, source allowlist, and host-alias regression tests."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research_pipeline.engine.core import PipelineError, Workspace, jsonl
from research_pipeline.engine.source_intake import extract, safe_source_url
from research_pipeline.engine.stage2_actions import run


class Stage2ActionsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.w = Workspace(self.root / "experiment")
        self.w.init({"schema_version": 1, "project": "Independent test",
                     "term_kind": "name", "content_kind": "definition",
                     "adapter": "mathdef", "external_reference_mode": True})
        self.sources = [
            {"id": "src.planetmath", "title": "PlanetMath",
             "url": "https://www.planetmath.org/",
             "authority_reviewed": True, "rights": "permitted", "access": "free"},
            {"id": "src.stacks", "title": "Stacks",
             "url": "https://stacks.math.columbia.edu/",
             "authority_reviewed": True, "rights": "locator_only", "access": "free"},
            {"id": "src.openstax_calculus", "title": "Excluded",
             "url": "https://openstax.org/index",
             "authority_reviewed": True, "rights": "locator_only", "access": "free"},
        ]
        src_path = self.root / "sources.jsonl"
        src_path.write_text("".join(json.dumps(s) + "\n" for s in self.sources),
                            encoding="utf-8")
        self.w.ingest("sources", src_path)
        self.w.seal("sources")
        self.manifest = self.root / "manifest.jsonl"
        self.rows = [
            {"id": "page.pm", "source_id": "src.planetmath",
             "url": "https://www.planetmath.org/alphabetical.html",
             "profile": "linked-list"},
            {"id": "page.st", "source_id": "src.stacks",
             "url": "https://stacks.math.columbia.edu/browse",
             "profile": "headings"},
            {"id": "page.blocked", "source_id": "src.openstax_calculus",
             "url": "https://openstax.org/index", "profile": "glossary"},
        ]
        self.manifest.write_text("".join(json.dumps(r) + "\n" for r in self.rows),
                                 encoding="utf-8")
        self.out = self.root / "artifact"

    @staticmethod
    def fake_fetch(url, source, delay=1.25):
        if source["id"] == "src.planetmath":
            return ('<h2>A</h2><a href="#a">a</a>'
                    '<a href="https://planetmath.org/abeliangroup">abeliangroup</a>'
                    '<a href="https://unapproved.org/phony">Nope</a>')
        return '<h2 id="topic">Scheme</h2>'

    def test_planetmath_explicit_alias_rejects_other_hosts(self):
        self.assertEqual(safe_source_url("https://planetmath.org/abeliangroup",
                                         self.sources[0]).hostname, "planetmath.org")
        with self.assertRaises(PipelineError):
            safe_source_url("https://planetmath.org.evil.test/x", self.sources[0])
        with self.assertRaises(PipelineError):
            safe_source_url("https://planetmath.org/x", self.sources[1])
        with self.assertRaises(PipelineError):
            safe_source_url("http://planetmath.org/x", self.sources[0])

    def test_planetmath_alpha_links_outside_lists(self):
        found = extract(self.w.root, "src.planetmath",
                        "https://www.planetmath.org/alphabetical.html",
                        self.fake_fetch("", self.sources[0]), stage="terms",
                        profile="linked-list")
        self.assertEqual([x["label"] for x in found], ["abeliangroup"])

    def test_stacks_nested_section_labels_not_lemmas(self):
        html = ('<ul><li>Section <a href="/tag/004O">5.5</a>: Bases'
                '<ul><li>Definition <a href="/tag/004P">5.5.1</a></li></ul>'
                '</li><li>Section <a href="/tag/09GP">9.10</a>: Algebraic closure'
                '</li></ul>')
        found = extract(self.w.root, "src.stacks",
                        "https://stacks.math.columbia.edu/tag/004C",
                        html, stage="terms", profile="stacks-sections")
        self.assertEqual([row["label"] for row in found],
                         ["Bases", "Algebraic closure"])
        self.assertEqual(found[0]["locator"],
                         "https://stacks.math.columbia.edu/tag/004O")

    @patch("research_pipeline.engine.stage2_actions.fetch_index")
    def test_allowed_sources_only_and_resume(self, fetch):
        fetch.side_effect = self.fake_fetch
        first = run(self.w.root, self.manifest, self.out, max_pages=1)
        self.assertEqual(first["completed_pages"], 1)
        self.assertEqual(first["candidate_count"], 1)
        second = run(self.w.root, self.manifest, self.out, max_pages=2)
        self.assertEqual(second["completed_pages"], 2)
        self.assertEqual(second["candidate_count"], 2)
        self.assertEqual(fetch.call_count, 2)
        self.assertFalse((self.w.root / "state" / "terms.json").exists())
        self.assertFalse((self.w.root / "records" / "terms.jsonl").exists())
        self.assertTrue(all(x["source_id"] != "src.openstax_calculus"
                            for x in jsonl(self.out / "raw_terms.jsonl")))
        again = run(self.w.root, self.manifest, self.out)
        self.assertEqual(again["completed_pages"], 2)
        self.assertEqual(fetch.call_count, 2)

    @patch("research_pipeline.engine.stage2_actions.fetch_index")
    def test_failed_page_retry_and_manifest_change(self, fetch):
        fetch.side_effect = OSError("temporary robots failure")
        first = run(self.w.root, self.manifest, self.out, max_pages=1)
        self.assertEqual(first["completed_pages"], 0)
        self.assertEqual(len(first["errors"]), 1)
        fetch.side_effect = self.fake_fetch
        second = run(self.w.root, self.manifest, self.out, max_pages=2)
        self.assertEqual(second["completed_pages"], 2)
        self.assertEqual(second["errors"], [])
        self.manifest.write_text("".join(json.dumps(r) + "\n"
                                         for r in self.rows[:1]), encoding="utf-8")
        with self.assertRaisesRegex(PipelineError, "Manifest changed"):
            run(self.w.root, self.manifest, self.out)


if __name__ == "__main__":
    unittest.main()
