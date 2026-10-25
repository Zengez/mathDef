"""Compare offline export replay on a synthetic amendment-heavy graph only."""
import argparse
import importlib.util
import json
from pathlib import Path
import statistics
import tempfile
import time
from unittest.mock import patch

from research_pipeline.engine import dependency_global_audit as audit
from research_pipeline.engine import dependency_review_preflight as preflight
from research_pipeline.engine.core import Workspace, digest
from research_pipeline.engine.dependency_graph import (
    amend, graph_path, inventory_sync, live_nodes, make_snapshot, read, store,
)


def measure(baseline_file: Path, *, repeats=3):
    spec = importlib.util.spec_from_file_location("prior_audit", baseline_file)
    prior = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prior)
    with tempfile.TemporaryDirectory(prefix="preflight-benchmark-") as directory:
        root = Path(directory)
        w = root / "workspace"
        Workspace(w).init({"schema_version": 1, "project": "Synthetic benchmark",
                           "term_kind": "item", "content_kind": "description",
                           "adapter": "fixture", "external_reference_mode": True,
                           "independent_second_wave": True})
        rows = [{"id": f"meaning.{i}", "display_term": f"Item {i}", "context": "Fixture",
                 "formulations": [{"id": f"form.{i}", "text": f"Fixture {i}."}]}
                for i in range(80)]
        (w / "records/meanings.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in rows))
        (w / "records/relations.jsonl").write_text("")
        inventory_sync(w)
        graph = graph_path(w)
        inv = read(graph / "INVENTORY.json")
        def refs(n):
            return [{"phrase": "fixture notation", "state": "external",
                     "disposition": f"Reviewed synthetic local notation version {n}; no dependency introduced."}]
        store(w, [{"formulation_id": fid, "version_sha256": f["version_sha256"],
                   "references": refs(0), "complete": True,
                   "review_rationale": "Reviewed full synthetic source and every notation reference."}
                  for fid, f in inv["formulations"].items()])
        nodes = live_nodes(graph, inv)
        amendments = []
        for version in range(1, 11):
            for fid, f in inv["formulations"].items():
                rationale = "Reviewed complete synthetic source and preserved external notation scope."
                amendments.append({"amendment_id": f"amend.{fid}.{version}",
                                   "formulation_id": fid, "version_sha256": f["version_sha256"],
                                   "expected_node_sha256": digest(nodes[fid]), "complete": True,
                                   "references": refs(version), "reason": rationale,
                                   "review_rationale": rationale, "reviewed_by": "Fixture reviewer"})
                nodes[fid] = make_snapshot(inv, fid, refs(version), "complete", rationale)
        amend(w, amendments)
        snapshot = audit.load_live_snapshot(w)
        manifest = {"schema_version": 1, "id": "benchmark-review",
                    "inventory_sha256": inv["source_inventory_sha256"],
                    "unresolved_fingerprint": snapshot["state"]["summary"]["unresolved_fingerprint"],
                    "reviewed_by": "Fixture reviewer",
                    "review_rationale": "Reviewed all synthetic sources; this benchmark tests mechanical export only.",
                    "changes": [{"formulation_id": fid, "expected_node_sha256": digest(node),
                                 "expected_occurrence_id": node["references"][0]["occurrence_id"],
                                 "updates": {"disposition": "Reviewed the complete fixture; this remains local external notation."},
                                 "reason": "Full synthetic source review preserves the independent notation disposition."}
                                for fid, node in list(snapshot["nodes"].items())[:20]]}
        path = root / "manifest.json"
        path.write_text(json.dumps(manifest))
        result = {"synthetic_only": True, "formulations": 80, "historical_amendments": 800,
                  "exported_formulations": 20, "packets": 4, "repeats": repeats}
        for label, module in [("before", prior), ("after", audit)]:
            runs = []
            for index in range(repeats):
                start = time.perf_counter()
                with patch.object(module, "live_nodes", wraps=live_nodes) as initial, \
                        patch.object(preflight, "live_nodes", wraps=live_nodes) as replay:
                    output = module.write_offline_packets(w, path, root / f"{label}-{index}")
                runs.append({"elapsed_seconds": time.perf_counter() - start,
                             "graph_replays": initial.call_count + replay.call_count,
                             "packet_digests": [digest(json.loads(Path(f).read_text()))
                                                for f in output["files"]]})
            result[label] = {"median_seconds": statistics.median(x["elapsed_seconds"] for x in runs),
                             "runs": runs}
        assert len({tuple(r["packet_digests"]) for label in ["before", "after"]
                    for r in result[label]["runs"]}) == 1
        result["all_packet_digests_identical"] = True
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-file", required=True, type=Path)
    parser.add_argument("--repeats", default=3, type=int)
    args = parser.parse_args()
    print(json.dumps(measure(args.baseline_file, repeats=args.repeats), indent=2))
