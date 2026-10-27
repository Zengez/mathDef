"""Bounded tests for one-pass, stage-only global link reconstruction."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.adapters.mathdef.rebuild_cleaned_links import (
    FinalLinkError, inspect_existing_links, rebuild, reconcile_deleted_source_edges,
)
from research_pipeline.ui.renderer import to_index


def group(gid, mid, fid, title, definition):
    return {"id":gid, "title":title, "meanings":[{
        "id":mid, "label":title, "subject":"Algebra",
        "formulations":[{"id":fid, "text":definition,
                         "sources":[{"title":"Source", "url":"https://example.org"}]}]
    }], "aliases":[]}


class CleanedGlobalLinksTests(unittest.TestCase):
    def setUp(self):
        self.catalog={"groups":[
            group("a","ma","fa","Abstract object", "Every open set is discussed."),
            group("b","mb","fb","Open set", "A subset with a topology."),
        ],"relations":[{"id":"screened","from_formulation":"fa",
                       "target_meaning":"mb","relation_type":"definition_uses",
                       "review_state":"screened", "span_start":0,
                       "span_end":8,"source_phrase":"old text"}]}

    def test_invalid_old_anchor_is_reset_but_reviewed_relation_remains(self):
        report=inspect_existing_links(self.catalog)
        self.assertEqual(len(report["stale_source_phrases_reset"]),1)
        relation=self.catalog["relations"][0]
        self.assertEqual(relation["id"],"screened")
        self.assertNotIn("span_start",relation)
        self.assertNotIn("source_phrase",relation)

    def test_original_screened_links_are_reanchored_to_current_wording(self):
        import research_pipeline.adapters.mathdef.merged_linking as linker
        inspect_existing_links(self.catalog)
        report=linker.link_merged_catalog(self.catalog)
        self.assertEqual(report["new_tentative_links"],0)
        self.assertEqual(report["existing_screened_links_anchored"],1)
        rel=self.catalog["relations"][0]
        self.assertEqual(self.catalog["groups"][0]["meanings"][0]["formulations"][0]
                         ["text"][rel["span_start"]:rel["span_end"]],"open set")
        self.assertEqual(len(to_index(self.catalog)[0]["formulations"][0]["dependencies"]),1)

    def test_historical_renamed_form_link_reconciliation(self):
        catalog={"groups":[
            group("old","mold","fold","Old","A borrowed vector space."),
            group("v","mv","fv","Vector space","A module over a field."),
        ],"relations":[{"id":"new","from_formulation":"fold","target_meaning":"mv",
                        "relation_type":"definition_uses","span_start":11,
                        "span_end":23,"source_phrase":"vector space"}]}
        report={"deleted_source_text_edges_needing_global_relink":["former"],
                "deleted_source_text_edge_details":[{
                    "old_relation_id":"former","reason":"source_formulation_consolidated",
                    "former_source_formulation_id":"f.deleted",
                    "live_source_formulation_id":"fold",
                    "former_target_meaning_id":"mv","live_target_meaning_id":"mv"
                }]}
        result=reconcile_deleted_source_edges(catalog,report)
        self.assertEqual(result["status_counts"],{"relinked_to_same_meaning":1})

    def test_literal_remaining_and_changed_wording_classify_without_guessing(self):
        catalog={"groups":[
            group("old","mold","fold","Old","A vector space is used."),
            group("v","mv","fv","Vector space","A module over a field."),
        ],"relations":[]}
        report={"deleted_source_text_edges_needing_global_relink":["former"],
                "deleted_source_text_edge_details":[{
                    "old_relation_id":"former","reason":"source_formulation_consolidated",
                    "former_source_formulation_id":"f.deleted",
                    "live_source_formulation_id":"fold",
                    "former_target_meaning_id":"mv","live_target_meaning_id":"mv"
                }]}
        self.assertEqual(reconcile_deleted_source_edges(catalog,report)
                         ["status_counts"],{"unlinked_literal_still_present_requires_review":1})
        catalog["groups"][0]["meanings"][0]["formulations"][0]["text"]="A linear space is used."
        self.assertEqual(reconcile_deleted_source_edges(catalog,report)["status_counts"],
                         {"no_longer_mentions_target_heading_in_visible_prose":1})

    def test_dangling_relationship_is_rejected_not_guessed(self):
        self.catalog["relations"][0]["target_meaning"]="m.no-such"
        with self.assertRaises(FinalLinkError):
            inspect_existing_links(self.catalog)

    def test_stale_span_in_math_is_removed(self):
        self.catalog["groups"][0]["meanings"][0]["formulations"][0]["text"] = (
            "We use $open set$ and then a different object.")
        self.catalog["relations"][0].update({"span_start":8,"span_end":16,
                                             "source_phrase":"open set"})
        report=inspect_existing_links(self.catalog)
        self.assertEqual(len(report["math_masked_anchors_reset"]),1)
        self.assertNotIn("span_start",self.catalog["relations"][0])


if __name__=="__main__":
    unittest.main()
