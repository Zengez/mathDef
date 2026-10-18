import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import Workspace, PipelineError
from research_pipeline.engine.source_intake import extract, safe_url

HTML = """<nav><h2>Navigation</h2></nav>
<h2 id="closure">Closure</h2><p>The smallest closed superset.</p>
<h2 id="algebra">Algebraic closure</h2><p>An extension field that is algebraically closed.</p>
<script><h2>False candidate</h2></script>
"""


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.w = Workspace(Path(self.tmp.name) / "new")
        self.w.init({"schema_version": 1, "project": "Test", "term_kind": "name",
                     "content_kind": "definition", "adapter": "mathdef",
                     "external_reference_mode": True})
        self.url = "https://example.org/index"
        self.base = {"id": "ref", "title": "Test ref", "url": self.url,
                     "authority_reviewed": True, "rights": "locator_only",
                     "access": "free"}
        self.file = Path(self.tmp.name) / "rows.jsonl"

    def feed(self, records, stage):
        import json
        self.file.write_text("".join(json.dumps(x) + "\n" for x in records))
        return self.w.ingest(stage, self.file)

    def test_offline_terms_and_locators_not_unlicensed_text(self):
        self.feed([self.base], "sources")
        terms = extract(self.w.root, "ref", self.url, HTML, stage="terms")
        self.assertEqual([x["label"] for x in terms], ["Closure", "Algebraic closure"])
        self.feed(terms, "terms")
        observations = extract(self.w.root, "ref", self.url, HTML, stage="observations")
        self.assertEqual(len(observations), 2)
        self.assertTrue(all(x["record_kind"] == "locator" and "text" not in x for x in observations))
        self.feed(observations, "observations")

    def test_explicit_license_for_excerpts(self):
        self.feed([self.base], "sources")
        with self.assertRaisesRegex(PipelineError, "Licensed excerpts"):
            extract(self.w.root, "ref", self.url, HTML, stage="observations", allow_excerpts=True)

    def test_reject_other_hosts_and_local_urls(self):
        for url in ("http://example.org", "https://127.0.0.1/index",
                    "https://example.org:8080/index", "https://evil.org/doc"):
            with self.assertRaises(PipelineError):
                safe_url(url, "example.org")

    def test_glossary_and_no_script_content(self):
        from research_pipeline.engine.source_intake import IndexReader
        reader = IndexReader(self.url, "glossary")
        reader.feed("<dl><dt>Closed set</dt><dd>A set equal to its closure.</dd></dl>")
        found = reader.candidates()
        self.assertEqual(found[0]["label"], "Closed set")
        self.assertIn("closure", found[0]["excerpt"])


if __name__ == "__main__":
    unittest.main()
