"""Targeted regression checks for merged-only lexical inline linking."""
import copy
import unittest

from research_pipeline.adapters.mathdef.merged_linking import (
    link_merged_catalog, masked_prose, words,
)
from research_pipeline.ui.renderer import to_index


def group(gid, term, mid, fid, body, label="Mathematics", aliases=None):
    return {"id": gid, "title": term, "aliases": aliases or [], "meanings": [{
        "id": mid, "label": label,
        "formulations": [{
            "id": fid, "text": body,
            "sources": [{"title": "Reference", "url": "https://example.org/source"}],
        }]
    }]}


class MergedLinkingTests(unittest.TestCase):
    def test_literal_links_have_exact_offsets_and_inline_index(self):
        source = group("g.top", "Topological space", "m.top", "f.top",
                       "A topological space has a collection of open sets.")
        target = group("g.open", "Open set", "m.open", "f.open",
                       "A subset is open if it belongs to the topology.")
        catalog = {"groups": [source, target], "relations": []}
        report = link_merged_catalog(catalog)
        self.assertEqual(report["new_tentative_links"], 1)
        rel = catalog["relations"][0]
        self.assertEqual(rel["target_meaning"], "m.open")
        self.assertEqual(source["meanings"][0]["formulations"][0]["text"]
                         [rel["span_start"]:rel["span_end"]], "open sets")
        # The index keeps provenance, exact offsets and the selected meaning.
        indexed = to_index(catalog)
        item = next(x for x in indexed if x["id"] == "g.top")
        dep = item["formulations"][0]["dependencies"][0]
        self.assertEqual(dep["start"], rel["span_start"])
        self.assertEqual(dep["end"], rel["span_end"])
        self.assertEqual(dep["review_state"], "lexical_candidate")

    def test_math_masks_and_term_boundaries(self):
        self.assertEqual(words("Vector space"), ("vector", "space"))
        masked = masked_prose(r"An open set and $open\ set$ and \(open\ set\)")
        self.assertEqual(masked.count("open set"), 1)
        parent = group("p", "Compact space", "a", "fa",
                       r"Let $A=\mathrm{open\ set}$ and let an open set exist.")
        tgt = group("q", "Open set", "b", "fb", "A member of the topology.")
        d = {"groups": [parent, tgt], "relations": []}
        link_merged_catalog(d)
        self.assertEqual(len(d["relations"]), 1)
        r = d["relations"][0]
        self.assertEqual(parent["meanings"][0]["formulations"][0]["text"]
                         [r["span_start"]:r["span_end"]], "open set")

    def test_abstains_from_ambiguous_context(self):
        parent = group("one", "Object", "one-m", "one-f",
                       "Consider the closure of this set.")
        target = group("two", "Closure", "two-a", "two-f",
                       "A smallest closed set.")
        target["meanings"].append({
            "id": "two-b", "label": "Algebraic closure context",
            "formulations": [{
                "id": "two-fb", "text": "An algebraic field extension.",
                "sources": [{"title": "Source", "url": "https://example.org"}],
            }]
        })
        result = {"groups": [parent, target], "relations": []}
        report = link_merged_catalog(result)
        self.assertEqual(report["new_tentative_links"], 0)
        self.assertGreater(report["ambiguous_contexts_total_occurrences"], 0)

    def test_CW_weak_topology_explicit_context_override(self):
        source = group("cw", "CW complex",
                       "meaning.mathdef.original.alg-topology.cell-complex",
                       "f-cw", "A set is closed with the weak topology.")
        fa = group("functional", "Weak topology", "m.functional", "f-functional",
                   "A topology on a Banach space.")
        cw = group("cw-weak", "weak topology of a CW complex",
                   "meaning.mathdef.postwave.scan-weak-topology-cw-complex-20261026",
                   "f-cw-weak", "Closed on each cell.")
        catalog = {"groups": [source, fa, cw], "relations": []}
        link_merged_catalog(catalog)
        targets = {x["target_meaning"] for x in catalog["relations"]}
        self.assertIn(cw["meanings"][0]["id"], targets)
        self.assertNotIn("m.functional", targets)

    def test_existing_screened_relation_anchored_without_duplicate(self):
        source = group("x", "Finite collection", "x-m", "x-f",
                       "A finite collection is a vector space.")
        target = group("v", "Vector space", "v-m", "v-f",
                       "A set with linear operations.")
        existing = {"id": "original", "from_formulation": "x-f",
                    "target_meaning": "v-m",
                    "relation_type": "definition_uses", "review_state": "screened"}
        original = {"groups": [source, target], "relations": [existing]}
        copied = copy.deepcopy(original)
        report = link_merged_catalog(copied)
        self.assertEqual(report["new_tentative_links"], 0)
        self.assertEqual(report["existing_screened_links_anchored"], 1)
        self.assertEqual(len(copied["relations"]), 1)
        self.assertNotIn("span_start", original["relations"][0])
        self.assertEqual(copied["relations"][0]["source_phrase"].lower(), "vector space")


    def test_does_not_bridge_math_paragraphs_or_tex_macros(self):
        source = group("s", "Some object", "m.s", "f.s",
                       r"An open $x$ set is given. Also an open." +
                       "\n\n" + "set at the start of a new paragraph." +
                       r" Also an open \emph{important} set.")
        target = group("t", "Open set", "m.t", "f.t", "An element of the topology.")
        catalog = {"groups": [source, target], "relations": []}
        report = link_merged_catalog(catalog)
        self.assertEqual(report["new_tentative_links"], 0)

    def test_ambiguous_context_report_carries_source_examples(self):
        parent = group("one", "Abstract object", "one-m", "one-f",
                       "Consider the closure of an object in this setting.")
        target = group("two", "Closure", "two-a", "two-f", "Topological closure")
        target["meanings"].append({
            "id": "two-b", "label": "Algebraic field closure",
            "formulations": [{"id": "two-fb", "text": "Field theory",
                              "sources": [{"title": "Reference",
                                           "url": "https://example.org"}]}],
        })
        report = link_merged_catalog({"groups": [parent, target], "relations": []})
        self.assertEqual(report["ambiguous_contexts_total_occurrences"], 1)
        example = report["ambiguous_context_examples"]["Closure"][0]
        self.assertEqual(example["from_formulation"], "one-f")
        self.assertEqual(example["matched_text"], "closure")
        self.assertEqual(len(example["eligible_meanings"]), 2)


if __name__ == "__main__":
    unittest.main()
