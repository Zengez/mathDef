"""Focused regression tests for the corpus-wide *existing link* auditor."""
import unittest

from research_pipeline.adapters.mathdef.audit_merged_links import audit
from research_pipeline.ui.renderer import to_index


def mkgroup(gid, mid, fid, term, body):
    return {
        "id": gid, "title": term, "aliases": [],
        "meanings": [{
            "id": mid, "label": "Mathematics", "formulations": [{
                "id": fid, "text": body, "sources": [
                    {"title": "Reference", "url": "https://example.org/test"}],
            }],
        }],
    }


class FullCorpusLinkAuditTests(unittest.TestCase):
    def setUp(self):
        self.source = mkgroup("g.src", "m.src", "f.src",
                              "Source concept",
                              "An open set is used in this construction.")
        self.target = mkgroup("g.target", "m.target", "f.target",
                              "Open set", "An open subset in a topology.")
        text = self.source["meanings"][0]["formulations"][0]["text"]
        start = text.index("open set")
        self.link = {
            "id": "rel.1", "from_formulation": "f.src",
            "target_meaning": "m.target", "relation_type": "definition_uses",
            "review_state": "lexical_candidate", "span_start": start,
            "span_end": start+len("open set"), "source_phrase": "open set",
        }

    def test_complete_catalog_integrity_and_coverage(self):
        catalog = {"groups": [self.source, self.target],
                   "relations": [self.link]}
        result = audit(catalog, to_index(catalog))
        self.assertEqual(result["stats"]["relations"], 1)
        self.assertEqual(result["relation_totals"]["anchored_def_uses"], 1)
        self.assertEqual(result["relation_totals"]["exact_anchor_matches"], 1)
        self.assertEqual(result["known_existing_term_unlinked"]["total_occurrences"], 0)
        self.assertEqual(result["anomaly_counts"].get("errors", 0), 0)

    def test_unlinked_existing_heading_is_not_new_candidate_discovery(self):
        catalog = {"groups": [self.source, self.target], "relations": []}
        result = audit(catalog, to_index(catalog))
        self.assertTrue(result["no_candidate_discovery"])
        self.assertEqual(result["known_existing_term_unlinked"]["total_occurrences"], 1)
        self.assertEqual(result["known_existing_term_unlinked"]["top"][0]["target_term"],
                         "Open set")

    def test_broken_source_link_is_detected_even_when_renderer_not_run(self):
        catalog = {"groups": [self.source, self.target],
                   "relations": [{**self.link, "from_formulation": "f.nonexistent"}]}
        index = to_index({"groups": catalog["groups"], "relations": []})
        result = audit(catalog, index)
        self.assertIn("errors", result["anomaly_counts"])
        self.assertEqual(result["anomalies"]["errors"][0]["error"],
                         "dangling_relation")

    def test_link_with_incorrect_source_span_is_detected(self):
        catalog = {"groups": [self.source, self.target],
                   "relations": [{**self.link, "span_start": 0,
                                  "span_end": len("open set")}]}
        result = audit(catalog, to_index(catalog))
        self.assertTrue(any(e["error"] == "span_phrase_mismatch"
                            for e in result["anomalies"]["errors"]))


if __name__ == "__main__":
    unittest.main()
