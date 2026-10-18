import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import Workspace
from research_pipeline.engine.source_manifest import generate


class ManifestTests(unittest.TestCase):
    def test_no_unapproved_sources_and_sitemap_uses_correct_host(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            w = Workspace(root / "work")
            w.init({"schema_version": 1, "project": "Test", "term_kind": "name",
                    "content_kind": "definition", "adapter": "mathdef",
                    "external_reference_mode": True})
            rows = [
                {"id": "approved", "title": "Allowed", "url": "https://example.org/index",
                 "index_profile": "glossary", "index_urls": [
                     "https://example.org/index", "https://example.org/terms"],
                 "authority_reviewed": True, "access": "free", "rights": "locator_only"},
                {"id": "blocked", "title": "Restricted", "url": "https://pay.example.edu",
                 "authority_reviewed": True, "access": "paid", "rights": "unknown"}
            ]
            p = root / "sources.jsonl"
            p.write_text("".join(json.dumps(x) + "\n" for x in rows))
            w.ingest("sources", p)
            sitemap = root / "map.xml"
            sitemap.write_text("""<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
              <url><loc>https://example.org/another</loc></url>
              <url><loc>https://unapproved.example.org/private</loc></url>
              </urlset>""")
            tasks = generate(w.root, sitemap_xml=sitemap, sitemap_source_id="approved")
            self.assertEqual(len(tasks), 3)
            self.assertTrue(all(x["source_id"] == "approved" for x in tasks))
            self.assertTrue(all(x["profile"] == "glossary" for x in tasks))


if __name__ == "__main__":
    unittest.main()
