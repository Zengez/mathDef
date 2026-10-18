import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import Workspace, PipelineError
from research_pipeline.engine.effort import log_effort, summarize


class EffortTests(unittest.TestCase):
    def test_user_entered_counts_no_invention_and_idempotency(self):
        with tempfile.TemporaryDirectory() as d:
            w = Workspace(Path(d) / "experiment")
            w.init({"schema_version": 1, "project": "Toy", "term_kind": "name",
                    "content_kind": "definition", "adapter": "mathdef",
                    "external_reference_mode": True})
            event = {"id": "batch.one", "stage": "sources", "thinking": "Medium",
                     "minutes": 15, "research_calls": 7, "records_examined": 25}
            self.assertFalse(log_effort(w.root, event)["already_logged"])
            self.assertTrue(log_effort(w.root, event)["already_logged"])
            self.assertEqual(summarize(w.root)["events"], 1)
            self.assertEqual(summarize(w.root)["minutes"], 15)
            with self.assertRaises(PipelineError):
                log_effort(w.root, dict(event, id="batch.bad", thinking="Extra High"))


if __name__ == "__main__":
    unittest.main()
