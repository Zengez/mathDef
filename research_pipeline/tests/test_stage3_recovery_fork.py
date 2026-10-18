"""Recovery fork cannot silently inherit an incomplete Stage 4 seal."""
import json
import tempfile
import unittest
from pathlib import Path

from research_pipeline.engine.core import PipelineError, Workspace
from research_pipeline.engine.stage3_attempts import run
from research_pipeline.engine.stage3_recovery_fork import fork


class RecoveryForkTests(unittest.TestCase):
    def test_fork_requires_all_attempts_and_leaves_stage3_open(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = Workspace(root / "historic")
            old.init({"schema_version":1, "project":"Independent",
                      "term_kind":"names", "content_kind":"definitions",
                      "adapter":"mathdef", "external_reference_mode":True})
            src = [
                {"id":"src.stacks", "title":"Stacks",
                 "url":"https://stacks.math.columbia.edu/",
                 "rights":"locator_only", "access":"free", "authority_reviewed":True},
                {"id":"src.planetmath", "title":"PlanetMath",
                 "url":"https://www.planetmath.org/",
                 "rights":"permitted", "access":"free", "authority_reviewed":True}]
            terms = [
                {"id":"term.a", "label":"Algebraic closure",
                 "source_id":"src.stacks",
                 "locator":"https://stacks.math.columbia.edu/tag/09GP"},
                {"id":"term.b", "label":"basis",
                 "source_id":"src.planetmath",
                 "locator":"https://planetmath.org/basis"}]
            for stage, rows in (("sources",src),("terms",terms)):
                file = root / (stage+".jsonl")
                file.write_text("".join(json.dumps(x)+"\n" for x in rows))
                old.ingest(stage,file)
                old.seal(stage)
            obs_file=root/"obs.jsonl"
            obs_file.write_text(json.dumps({
                "id":"obs.1","term_id":"term.a","source_id":"src.stacks",
                "locator":terms[0]["locator"],"record_kind":"paraphrase",
                "text":"An algebraic closure of a field is an algebraic and algebraically closed field extension."})+"\n")
            old.ingest("observations",obs_file)
            old.seal("observations")
            ledger=old.root/"state/stage3_acquisition_attempts.jsonl"
            report=old.root/"state/stage3_acquisition_report.json"
            def fetch(url,source,*,delay,robots_cache):
                if source["id"]=="src.planetmath":
                    raise PipelineError("Robots policy unavailable")
                return ('<title>Section 9.10 (09GP): Algebraic closure—The Stacks project</title>'
                        '<a href="/tag/09GQ">Definition 9.10.1.</a>')
            dest=root/"recovered"
            run(old.root,ledger,report,batch_size=1,fetcher=fetch)
            with self.assertRaisesRegex(PipelineError,"only 1/2"):
                fork(old.root,dest)
            self.assertFalse(dest.exists())
            run(old.root,ledger,report,batch_size=1,fetcher=fetch)
            result=fork(old.root,dest)
            recovered=Workspace(dest)
            self.assertEqual(result["per_term_attempts_accounted"],2)
            self.assertTrue(recovered.state("terms")["sealed"])
            self.assertFalse(recovered.state("observations")["sealed"])
            self.assertEqual(len(recovered.records("observations")),1)
            self.assertEqual(len(recovered.records("meanings")),0)
            self.assertTrue(recovered.config()["require_reviewed_term_dispositions"])
            with self.assertRaisesRegex(PipelineError,"fetched terms still lack editorial review"):
                recovered.seal("observations")
            self.assertTrue(old.state("observations")["sealed"])


if __name__=="__main__":
    unittest.main()
