"""Small structural checks for directly researched Wave 2 terms."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.adapters.mathdef.direct_additions import add_direct_research
from research_pipeline.engine.core import PipelineError
from research_pipeline.ui.renderer import to_index


class DirectResearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / "terms.json"
        self.groups = [{
            "id": "preview.term.existing", "title": "Existing prerequisite",
            "aliases": [], "meanings": [{
                "id": "meaning.existing", "label": "General", "formulations": [{
                    "id": "form.existing", "text": "Already known.",
                    "sources": [{"title": "Reference", "url": "https://example.org"}]
                }]
            }]
        }]
        self.links = []
        self.one = {
            "id": "meaning.direct.example", "term": "Fresh term",
            "context": "Mathematics", "definition": "An original stated definition.",
            "sources": [{"title": "Research reference", "url": "https://example.org/a",
                         "verification_status": "source_lead"}],
            "links": [{"target_meaning": "meaning.existing", "relation_type": "definition_uses"}]
        }

    def write(self, entries):
        self.file.write_text(json.dumps({"schema_version": 1, "entries": entries}), encoding="utf-8")

    def test_new_term_is_searchable_in_display_index_and_linked(self):
        self.write([self.one])
        self.assertEqual(add_direct_research(self.groups, self.links, self.file), 1)
        idx = to_index({"groups": self.groups, "relations": self.links})
        found = next(e for e in idx if e["term"] == "Fresh term")
        self.assertEqual(found["dependencies"][0]["target_meaning"], "meaning.existing")
        self.assertEqual(found["formulations"][0]["sources"][0]["verification_status"], "source_lead")

    def test_unknown_link_is_rejected(self):
        self.write([{**self.one, "links": [{"target_meaning": "missing.meaning"}]}])
        with self.assertRaisesRegex(PipelineError, "Unknown meaning link"):
            add_direct_research(self.groups, self.links, self.file)

    def test_same_term_can_add_a_contextual_variant(self):
        self.write([{**self.one, "term": "Existing prerequisite"}])
        self.assertEqual(add_direct_research(self.groups, self.links, self.file), 1)
        self.assertEqual(len(self.groups), 1)
        self.assertEqual(len(self.groups[0]["meanings"]), 2)

    def test_duplicate_meaning_and_missing_source_rejected(self):
        self.write([{**self.one, "id": "meaning.existing"}])
        with self.assertRaisesRegex(PipelineError, "Duplicate"):
            add_direct_research(self.groups, self.links, self.file)
        self.write([{**self.one, "sources": []}])
        with self.assertRaisesRegex(PipelineError, "Missing source"):
            add_direct_research(self.groups, self.links, self.file)


if __name__ == "__main__":
    unittest.main()
