import unittest

from scripts.dependency_links import populate_dependencies


def entry(ident, term, body, related=(), aliases=()):
    section = ident.split(".")[0]
    return {
        "id": ident, "term": term, "body": body,
        "related": list(related), "aliases": list(aliases),
        "path": f"definitions/{section}/{ident.split('.')[-1]}.tex",
    }


class DependencyMatchingTests(unittest.TestCase):
    def test_phrase_precedence_inflection_and_full_words(self):
        corpus = [
            entry("algebra.group", "Group", "A group has elements."),
            entry("algebra.normal-subgroup", "Normal subgroup", "A normal subgroup of a group."),
            entry("algebra.example", "Example", "Every normal subgroup is a subgroup of a group."),
            entry("algebra.ring", "Ring", "A ring."),
            entry("algebra.spring", "Spring", "A spring."),
        ]
        linked, _ = populate_dependencies(corpus)
        found = [v["id"] for v in linked["algebra.example"]]
        self.assertIn("algebra.normal-subgroup", found)
        self.assertIn("algebra.group", found)
        self.assertNotIn("algebra.spring", found)
        self.assertNotIn("algebra.ring", found)

    def test_math_masking_and_exact_latex_alias(self):
        corpus = [
            entry("algebra.group", "Group", "A group."),
            entry("pde.h1", "Sobolev space $H^1$", "A Sobolev space.",
                  aliases=["$H^1$"]),
            entry("pde.example", "Example", r"Let $G=\mathrm{group}$ and take $H^1$."),
        ]
        linked, _ = populate_dependencies(corpus)
        found = [v["id"] for v in linked["pde.example"]]
        self.assertIn("pde.h1", found)
        self.assertNotIn("algebra.group", found)

    def test_ambiguous_target_skipped_unless_context_resolves(self):
        corpus = [
            entry("metric.open-set", "Open set", "Metric topology."),
            entry("topology.open-set", "Open set", "Topology."),
            entry("functions.example", "Example", "An open set is needed."),
            entry("topology.example", "Example", "An open set is needed."),
            entry("functions.qualified", "Qualified", "An open set is needed.",
                  related=["metric.open-set"]),
        ]
        linked, report = populate_dependencies(corpus)
        self.assertEqual(linked["functions.example"], [])
        self.assertIn("metric.open-set", [v["id"] for v in linked["functions.qualified"]])
        self.assertIn("topology.open-set", [v["id"] for v in linked["topology.example"]])
        self.assertGreaterEqual(report["unresolved_ambiguous_occurrences"], 1)

    def test_manual_exclusions_inclusions_resolution(self):
        corpus = [
            entry("metric.open-set", "Open set", "Metric openness."),
            entry("topology.open-set", "Open set", "Topological openness."),
            entry("functions.foo", "Foo", "An open set is used."),
        ]
        overrides = {"functions.foo": {
            "resolve": {"open set": "metric.open-set"},
            "include": ["topology.open-set"],
        }}
        linked, _ = populate_dependencies(corpus, overrides)
        self.assertEqual({v["id"] for v in linked["functions.foo"]},
                         {"metric.open-set", "topology.open-set"})
        linked2, _ = populate_dependencies(corpus, {
            "functions.foo": {"exclude": ["topology.open-set"], "resolve": {"open set": "metric.open-set"}}
        })
        self.assertEqual([v["id"] for v in linked2["functions.foo"]], ["metric.open-set"])

    def test_source_offsets_and_related_not_sufficient(self):
        corpus = [
            entry("algebra.group", "Group", "A mathematical group."),
            entry("algebra.foo", "Foo", "A ring is mentioned, but not a group.",
                  related=["algebra.group"]),
            entry("algebra.ring", "Ring", "A mathematical ring."),
            entry("algebra.bar", "Bar", "No familiar dependency here.",
                  related=["algebra.group"]),
        ]
        linked, _ = populate_dependencies(corpus)
        d = next(x for x in linked["algebra.foo"] if x["id"] == "algebra.ring")
        self.assertEqual(corpus[1]["body"][d["start"]:d["end"]], "ring")
        self.assertEqual(linked["algebra.bar"], [])


if __name__ == "__main__":
    unittest.main()
