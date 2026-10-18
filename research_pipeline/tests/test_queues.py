import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import Workspace, jsonl
from research_pipeline.engine.queues import make_queue


class QueueTests(unittest.TestCase):
    def test_queues_are_deterministic_without_reading_production_corpus(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            w = Workspace(root / "blank")
            w.init({"schema_version": 1, "project": "Independent toy",
                    "term_kind": "name", "content_kind": "text",
                    "adapter": "mathdef", "external_reference_mode": True})
            q = make_queue(w.root, "sources")
            self.assertEqual(q["recommended_thinking"], "Medium")
            self.assertEqual(q["tasks"], 1)
            path = root / "sources.jsonl"
            path.write_text(json.dumps({
                "id": "ref.a", "title": "Independent source",
                "url": "https://example.org/reference",
                "authority_reviewed": True, "access": "free", "rights": "locator_only"
            }) + "\n")
            w.ingest("sources", path)
            self.assertEqual(make_queue(w.root, "terms")["tasks"], 1)
            self.assertEqual(make_queue(w.root, "terms")["tasks"], 1)
            entries = jsonl(w.root / "tasks/terms.jsonl")
            self.assertEqual(entries[0]["source_id"], "ref.a")
            self.assertNotIn("production", str(entries))


if __name__ == "__main__":
    unittest.main()
