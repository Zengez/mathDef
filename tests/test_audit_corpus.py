import unittest
from scripts.audit_corpus import audit_entry

class CorpusAuditTests(unittest.TestCase):
    def test_missing_source_and_short_not_reviewed(self):
        entry = {
            "id":"test.one", "term":"Example", "source":"", "body":"A short set.",
            "status":"draft", "path":"definitions/test/one.tex"
        }
        flags = [a for a, _ in audit_entry(entry, {"example":["test.one"]})]
        self.assertIn("no-source", flags)
        self.assertIn("very-short", flags)
        self.assertIn("not-reviewed", flags)
    def test_complete_sample(self):
        entry = {
            "id":"x", "term":"Complete example",
            "source":"https://encyclopediaofmath.org/wiki/Example",
            "body":"A sufficiently long and precise definition of a mathematical object containing all quantified conditions of membership.",
            "status":"reviewed", "path":"x"
        }
        self.assertEqual(audit_entry(entry, {"complete example":["x"]}), [])

if __name__ == "__main__":
    unittest.main()
