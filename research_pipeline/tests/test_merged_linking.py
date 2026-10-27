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


    def test_broad_representative_prioritized_without_discarding_variants(self):
        source = group("src", "Countability", "m.src", "f.src",
                       "Any topological space has a topology.")
        g = group("top", "Topological space",
                  "meaning.wave2.foundation.topological-space", "f.a",
                  "A space with open sets.", label="General topological space")
        g["meanings"].append({
            "id": "meaning.mathdef.original.topology.topological-space",
            "label": "Original mathDef · Topology",
            "formulations": [{"id": "f.b", "text": "An alternate equivalent axiom set.",
                              "sources": [{"title": "Reference", "url": "https://example.org"}]}],
        })
        c = {"groups": [source, g], "relations": []}
        report = link_merged_catalog(c)
        self.assertEqual(report["new_tentative_links"], 1)
        self.assertEqual(c["relations"][0]["target_meaning"],
                         "meaning.wave2.foundation.topological-space")
        self.assertEqual(len(g["meanings"]), 2)

    def test_affine_scheme_ring_maps_are_unital_but_generic_maps_abstain(self):
        source = group("src", "Affine scheme", "m.src", "f.src",
                       "An affine scheme is defined through a ring homomorphism.",
                       label="Algebraic geometry: affine scheme morphisms")
        generic = group("gen", "Ring homomorphism",
                        "meaning.wave2.foundation.ring-map-general", "fg",
                        "Preserves addition and multiplication without necessarily preserving 1.")
        generic["meanings"].append({
            "id": "meaning.wave2.foundation.ring-map-unital",
            "label": "Unital ring homomorphism",
            "formulations": [{"id": "fu", "text": "Preserves 1 too",
                              "sources": [{"title": "Source", "url": "https://example.org"}]}],
        })
        c = {"groups": [source, generic], "relations": []}
        report = link_merged_catalog(c)
        self.assertEqual(report["new_tentative_links"], 1)
        self.assertEqual(c["relations"][0]["target_meaning"],
                         "meaning.wave2.foundation.ring-map-unital")
        source["meanings"][0]["label"] = "General algebra"
        c2 = {"groups": [source, generic], "relations": []}
        report2 = link_merged_catalog(c2)
        self.assertEqual(report2["new_tentative_links"], 0)
        self.assertGreater(report2["ambiguous_contexts_total_occurrences"], 0)


    def test_random_variable_general_and_explicit_real_context(self):
        target = group("rv", "Random variable",
                       "meaning.wave2.prob90.random-variable-general",
                       "f.general", "A measurable map into a measurable state space.")
        target["meanings"].extend([
            {"id": "meaning.wave2.prob90.random-variable-real",
             "label": "Real-valued random variable",
             "formulations": [{"id":"f.real","text":"A measurable real-valued map.",
                               "sources":[{"title":"Ref","url":"https://example.org"}]}]},
            {"id": "meaning.mathdef.original.prob.random-variable",
             "label":"Original mathDef · Probability",
             "formulations":[{"id":"f.old","text":"A random variable.",
                              "sources":[{"title":"Ref","url":"https://example.org"}]}]},
        ])
        generic = group("g", "Almost-sure equality", "m.g", "f.g",
                        "Two random variables are equal almost surely.")
        real = group("v", "Bernoulli distribution", "m.v", "f.v",
                     "A real random variable follows a Bernoulli distribution.")
        c={"groups":[target,generic,real],"relations":[]}
        report=link_merged_catalog(c)
        self.assertEqual(report["new_tentative_links"],2)
        by_form={rel["from_formulation"]:rel["target_meaning"] for rel in c["relations"]}
        self.assertEqual(by_form["f.g"],"meaning.wave2.prob90.random-variable-general")
        self.assertEqual(by_form["f.v"],"meaning.wave2.prob90.random-variable-real")
        self.assertEqual(report["ambiguous_contexts_total_occurrences"],0)

    def test_distinct_inner_product_and_natural_number_conventions_still_abstain(self):
        nats=group("n","Natural numbers","meaning.wave2.set63.natural-including-zero",
                   "fn0","Natural numbers can include zero.")
        nats["meanings"].append({
            "id":"meaning.wave2.set63.natural-positive-convention","label":"Positive convention",
            "formulations":[{"id":"fn1","text":"Natural numbers start at one.",
                             "sources":[{"title":"Ref","url":"https://example.org"}]}],
        })
        ip=group("ip","Inner product space",
                 "meaning.wave2.analysis98.real-inner-product-space",
                 "fip1","Positive symmetric bilinear product.")
        ip["meanings"].append({
            "id":"meaning.wave2.analysis98.complex-inner-product-space",
            "label":"Complex positive-definite Hermitian inner product",
            "formulations":[{"id":"fip2","text":"Hermitian positive product.",
                             "sources":[{"title":"Ref","url":"https://example.org"}]}],
        })
        source=group("a","Orthogonal complement","ma","fa",
                     "In an inner product space, take the orthogonal complement "
                     "of a sequence indexed by natural numbers.")
        c={"groups":[nats,ip,source],"relations":[]}
        report=link_merged_catalog(c)
        self.assertEqual(report["new_tentative_links"],0)
        self.assertEqual(report["ambiguous_contexts_total_occurrences"],2)

    def test_discrete_martingale_source_override_not_continuous_by_default(self):
        source=group("m","Martingale transform",
                     "meaning.mathdef.original.stochastic.martingale-transform",
                     "fm","A martingale transform uses increments of a martingale.")
        target=group("t","Martingale","meaning.wave2.research81.martingale-discrete",
                     "fd","An adapted integrable discrete sequence.")
        target["meanings"].append({
            "id":"meaning.wave2.research81.martingale-continuous-index",
            "label":"Real-valued martingale indexed continuously",
            "formulations":[{"id":"fc","text":"Adapted continuous-time process",
                             "sources":[{"title":"Ref","url":"https://example.org"}]}],
        })
        c={"groups":[source,target],"relations":[]}
        report=link_merged_catalog(c)
        self.assertEqual(report["new_tentative_links"],1)
        self.assertEqual(c["relations"][0]["target_meaning"],
                         "meaning.wave2.research81.martingale-discrete")



    def test_krull_dimension_supremum_chooses_general_order_concept(self):
        source=group("src","Height of a prime ideal","m.height","f.height",
                     "The height is the supremum of lengths of prime chains.",
                     label="Commutative algebra: prime ideal height")
        target=group("target","Supremum",
                     "meaning.wave2.direct.066b1d1b9032a2e86bdd","f.ord",
                     "Least upper bound in a partially ordered set.")
        target["meanings"].append({
            "id":"meaning.mathdef.original.real.supremum", "label":"Real analysis",
            "formulations":[{"id":"f.real","text":"Least upper bound of real numbers.",
                             "sources":[{"title":"Ref","url":"https://example.org"}]}],
        })
        c={"groups":[source,target],"relations":[]}
        report=link_merged_catalog(c)
        self.assertEqual(report["new_tentative_links"],1)
        self.assertEqual(c["relations"][0]["target_meaning"],
                         "meaning.wave2.direct.066b1d1b9032a2e86bdd")

    def test_zero_divisor_conventions_scoped_to_nontrivial_pair(self):
        source=group("s","Zero polynomial",
                     "meaning.mathdef.postwave.scan-zero-polynomial-20261026",
                     "f.s","Over rings with zero divisors, the zero polynomial exists.")
        target=group("t","Zero divisor",
                     "meaning.mathdef.original.commalg.zero-divisor",
                     "f.broad","Some zero products occur in commutative rings.")
        target["meanings"].append({
            "id":"meaning.wave2.direct.8f2dea7e2bd1211c0cf6",
            "label":"Nonzero zero divisor convention",
            "formulations":[{"id":"f.narrow","text":"Two nonzero elements annihilate one another.",
                             "sources":[{"title":"Ref","url":"https://example.org"}]}],
        })
        c={"groups":[source,target],"relations":[]}
        report=link_merged_catalog(c)
        self.assertEqual(report["new_tentative_links"],1)
        self.assertEqual(c["relations"][0]["target_meaning"],
                         "meaning.wave2.direct.8f2dea7e2bd1211c0cf6")



    def test_quasi_metric_directional_balls_not_mislinked_to_metric_ball(self):
        parent = group("backward", "Backward quasi-metric ball",
                       "meaning.mathdef.original.quasimetric.backward-ball",
                       "f.backward",
                       "The backward open ball is the set of points close in the reverse direction.")
        parent2 = group("forward", "Forward quasi-metric ball",
                        "meaning.mathdef.original.quasimetric.forward-ball",
                        "f.forward",
                        "The forward open ball uses the forward quasi-metric.")
        target = group("ball", "Open ball",
                       "meaning.mathdef.original.metric.open-ball",
                       "f.ball", "A set defined by a symmetric metric.")
        target["meanings"].append({
            "id":"meaning.wave2.directional113.open-norm",
            "label":"Normed-space open ball",
            "formulations":[{"id":"f.norm","text":"A norm-based open ball.",
                             "sources":[{"title":"Ref","url":"https://example.org"}]}],
        })
        data={"groups":[parent,parent2,target],"relations":[]}
        report=link_merged_catalog(data)
        self.assertEqual(report["new_tentative_links"],0)
        self.assertEqual(report["skipped_context_false_positive"],2)
        self.assertEqual(report["ambiguous_contexts_total_occurrences"],0)

    def test_original_krull_dimension_supremum_is_order_theoretic(self):
        source=group("krull","Krull dimension",
                     "meaning.mathdef.original.commalg.krull-dimension",
                     "f.krull",
                     "Dimension is the supremum of lengths of prime chains.")
        target=group("sup","Supremum",
                     "meaning.wave2.direct.066b1d1b9032a2e86bdd",
                     "f.ord","Least upper bound in a poset.")
        target["meanings"].append({
            "id":"meaning.mathdef.original.real.supremum",
            "label":"Real analysis",
            "formulations":[{"id":"f.real","text":"Supremum of real numbers.",
                             "sources":[{"title":"Ref","url":"https://example.org"}]}],
        })
        d={"groups":[source,target],"relations":[]}
        report=link_merged_catalog(d)
        self.assertEqual(report["new_tentative_links"],1)
        self.assertEqual(d["relations"][0]["target_meaning"],
                         "meaning.wave2.direct.066b1d1b9032a2e86bdd")


if __name__ == "__main__":
    unittest.main()
