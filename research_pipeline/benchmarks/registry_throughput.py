"""Synthetic, offline bulk-registry benchmark; never opens a research dataset.

Use --core-file with a saved prior core.py for a controlled before/after run.
Timings are local measurements, not an estimate of scholarly review effort.
"""
from __future__ import annotations

import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import statistics
import tempfile
import time
from unittest.mock import patch

from research_pipeline.engine import core


def measure(module=core, *, size=300, repeats=3):
    if size < 1 or repeats < 1:
        raise ValueError("size and repeats must be positive")
    measurements = []
    for _ in range(repeats):
        with tempfile.TemporaryDirectory(prefix="registry-benchmark-") as directory:
            root = Path(directory)
            w = module.Workspace(root / "workspace")
            w.init({"schema_version": 1, "project": "Synthetic benchmark",
                    "term_kind": "item", "content_kind": "description",
                    "adapter": "fixture", "external_reference_mode": True})
            rows = {
                "sources": [{"id": "source.fixture", "title": "Fixture",
                             "url": "https://example.org/", "rights": "locator_only",
                             "access": "free", "authority_reviewed": True}],
                "terms": [{"id": f"term.{i}", "label": f"Item {i}",
                           "source_id": "source.fixture", "locator": f"item/{i}"}
                          for i in range(size)],
                "observations": [{"id": f"obs.{i}", "term_id": f"term.{i}",
                                  "source_id": "source.fixture", "locator": f"item/{i}",
                                  "record_kind": "paraphrase", "text": f"Fixture item {i}."}
                                 for i in range(size)],
                "meanings": [{"id": f"meaning.{i}", "term_group_id": f"group.{i}",
                              "display_term": f"Item {i}", "context": "Synthetic fixture",
                              "term_ids": [f"term.{i}"], "formulations": [{
                                  "id": f"form.{i}", "text": f"Fixture statement {i}.",
                                  "evidence_ids": [f"obs.{i}"], "review_state": "screened"}]}
                             for i in range(size)],
                "relations": [{"id": f"rel.{i}", "from_formulation": f"form.{i}",
                               "target_meaning": f"meaning.{(i+1) % size}",
                               "relation_type": "related_usage", "review_state": "screened"}
                              for i in range(size)],
            }
            for stage, values in rows.items():
                (root / (stage + ".jsonl")).write_text(
                    "".join(json.dumps(x) + "\n" for x in values), encoding="utf-8")
            reads = Counter()
            original = module.jsonl
            def counted(path):
                if Path(path).parent.name == "records":
                    reads[Path(path).stem] += 1
                return original(path)
            start = time.perf_counter()
            with patch.object(module, "jsonl", side_effect=counted):
                for stage in module.STAGES:
                    w.ingest(stage, root / (stage + ".jsonl"), batch_size=50)
                    w.seal(stage)
                publication = w.publication()
            measurements.append({"elapsed_seconds": time.perf_counter() - start,
                                 "record_file_reads": dict(reads),
                                 "publication_sha256": module.digest(publication)})
    assert len({x["publication_sha256"] for x in measurements}) == 1
    return {"schema_version": 1, "synthetic_only": True, "rows_per_non_source_stage": size,
            "repeats": repeats, "median_seconds": statistics.median(
                x["elapsed_seconds"] for x in measurements), "runs": measurements}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=300)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--core-file", type=Path)
    args = parser.parse_args()
    module = core
    if args.core_file:
        spec = importlib.util.spec_from_file_location("prior_core", args.core_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    print(json.dumps(measure(module, size=args.size, repeats=args.repeats), indent=2))


if __name__ == "__main__":
    main()
