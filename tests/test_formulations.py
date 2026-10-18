import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.build_index import ROOT, parse, parse_variant, attach_formulations
from scripts.dependency_links import populate_dependencies


class FormulationTests(unittest.TestCase):
    def test_function_has_two_sourced_formulations_under_one_id(self):
        original = parse(ROOT / "definitions/functions/function.tex")
        self.assertEqual(original["id"], "functions.function")
        self.assertEqual(original["term"], "Function")
        attach_formulations([original])
        forms = original["formulations"]
        self.assertEqual([f["key"] for f in forms], ["primary", "graph"])
        self.assertEqual([f["label"] for f in forms],
                         ["Assignment formulation", "Set-theoretic (relation) formulation"])
        self.assertLess(forms[0]["order"], forms[1]["order"])
        self.assertIn("exactly one element", forms[0]["body"])
        self.assertIn("exists a unique", forms[1]["body"])
        self.assertIn("f\\subseteq X\\times Y", forms[1]["body"])
        self.assertTrue(all(f["source"].startswith("https://") for f in forms))

    def test_links_from_variant_have_variant_specific_positions(self):
        function = parse(ROOT / "definitions/functions/function.tex")
        product = parse(ROOT / "definitions/sets/cartesian-product.tex")
        attach_formulations([function, product])
        links, _ = populate_dependencies([function, product])
        primary, graph = function["formulations"]
        self.assertNotIn("sets.cartesian-product", [d["id"] for d in primary["dependencies"]])
        hits = [d for d in graph["dependencies"] if d["id"] == "sets.cartesian-product"]
        self.assertEqual(len(hits), 1)
        dep = hits[0]
        self.assertEqual(graph["body"][dep["start"]:dep["end"]].casefold(),
                         dep["label"].casefold())
        self.assertEqual(dep["formulation"], "graph")
        self.assertIn("sets.cartesian-product", [d["id"] for d in links["functions.function"]])
        self.assertEqual(len(links), 2)

    def test_invalid_variant_headers_do_not_silently_publish(self):
        with TemporaryDirectory() as temporary:
            invalid = Path(temporary) / "orphan.tex"
            invalid.write_text("% parent: invalid/id\n% key: graph\n% label: Graph\n% source: https://example.com\n\nA definition.")
            with self.assertRaisesRegex(ValueError, "parent"):
                parse_variant(invalid)

    def test_single_formulation_entries_preserve_old_shape(self):
        other = parse(ROOT / "definitions/sets/cartesian-product.tex")
        attach_formulations([other])
        self.assertNotIn("formulations", other)
        self.assertIn("body", other)


if __name__ == "__main__":
    unittest.main()
