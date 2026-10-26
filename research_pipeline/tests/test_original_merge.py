"""Fast smoke checks for the user-authorized post-Wave2 merge/scan."""
import unittest
import json
import tempfile
from copy import deepcopy
from pathlib import Path

from research_pipeline.adapters.mathdef.direct_additions import add_direct_research

from research_pipeline.adapters.mathdef.original_merge import (
    merge_original, fast_scan,
)
from research_pipeline.ui.renderer import to_index


class OriginalMergeTests(unittest.TestCase):
    def setUp(self):
        self.existing = {"groups": [{
            "id": "g.wave2", "title": "Vector space", "aliases": [],
            "meanings": [{"id": "m.wave2", "label": "Linear algebra",
                          "formulations": [{
                              "id": "f.wave2", "text": "A vector space over a field.",
                              "sources": [{"title": "Evidence",
                                           "url": "https://example.org/a"}]
                          }]}]
        }], "relations": []}
        self.original = [{
            "id": "linear.vector-space", "term": "Vector space",
            "body": "Let $V$ be a vector space. A linear space.",
            "category": "Linear algebra", "path": "definitions/linear/vector-space.tex",
            "source": "https://example.org/legacy", "source_title": "Legacy reference",
            "status": "draft", "form_label": "Original formulation",
            "aliases": ["Linear space"], "related": ["linear.matrix"],
        }, {
            "id": "linear.matrix", "term": "Matrix",
            "body": "An array of entries in a ring.",
            "category": "Linear algebra", "path": "definitions/linear/matrix.tex",
            "source": "https://example.org/matrix", "status": "draft",
            "form_label": "Original formulation", "aliases": [], "related": [],
        }]

    def test_no_mutation_exact_group_join_and_related_provenance(self):
        merged, stats = merge_original(self.existing, self.original)
        self.assertEqual(len(self.existing["groups"]), 1)
        self.assertEqual(stats["original_definitions"], 2)
        self.assertEqual(stats["shared_term_labels"], 1)
        self.assertEqual(stats["combined_meanings"], 3)
        group = next(x for x in merged["groups"] if x["title"] == "Vector space")
        self.assertEqual(len(group["meanings"]), 2)
        self.assertIn("Linear space", group["aliases"])
        self.assertEqual(len(merged["relations"]), 1)
        index = to_index(merged)
        self.assertEqual(len(index), 2)
        self.assertEqual(sum(len(x["formulations"]) for x in index), 3)
        self.assertTrue(any("Original mathDef" in x["label"] for x in group["meanings"]))

    def test_rapid_scan_covers_new_and_original_bodies(self):
        merged, stats = merge_original(self.existing, self.original)
        direct = [{"id": "m.direct", "term": "Special relation",
                   "definition": "A vector space is defined over a field."}]
        scan = fast_scan(direct, self.original, merged)
        self.assertEqual(scan["scan_scope"]["wave2_direct_meanings"], 1)
        self.assertEqual(scan["scan_scope"]["original_mathdef_definitions"], 2)
        self.assertEqual(scan["scan_scope"]["total_formulations_scanned"], 3)
        self.assertTrue(any(x["term"] == "vector space"
                            for x in scan["known_term_mentions"]))
        self.assertEqual(scan["status"], "rough_candidates_not_verified")


    def test_new_research_augments_combined_copy_not_independent(self):
        merged, _stats = merge_original(self.existing, self.original)
        independent_before = deepcopy(self.existing)
        scan_before = fast_scan([], self.original, merged)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "terms.json"
            path.write_text(json.dumps({
                "schema_version": 1,
                "entries": [{
                    "id": "meaning.postwave.test",
                    "term": "Locally small category",
                    "context": "Post-Wave2 · category theory",
                    "definition": "A category whose collections of morphisms are sets.",
                    "sources": [{"title": "Reference", "url": "https://example.org/locally-small",
                                 "verification_status": "source_checked"}],
                    "links": [{"target_meaning": "m.wave2",
                               "relation_type": "related"}]
                }]
            }), encoding="utf-8")
            added = add_direct_research(merged["groups"], merged["relations"], path)
        self.assertEqual(added, 1)
        self.assertEqual(self.existing, independent_before)
        self.assertEqual(scan_before["scan_scope"]["original_mathdef_definitions"], 2)
        self.assertEqual(sum(len(g["meanings"]) for g in merged["groups"]), 4)
        self.assertTrue(any(g["title"] == "Locally small category"
                            for g in merged["groups"]))
        self.assertTrue(any(rel["target_meaning"] == "m.wave2"
                            for rel in merged["relations"]))
        self.assertEqual(sum(len(g["meanings"]) for g in self.existing["groups"]), 1)

if __name__ == "__main__":
    unittest.main()
