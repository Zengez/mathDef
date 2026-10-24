"""Independent Wave2 preflight amortizes expensive effective-graph replay."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research_pipeline.engine.core import Workspace, digest
from research_pipeline.engine.dependency_graph import (
    graph_path, inventory_sync, live_nodes, read, store,
)
from research_pipeline.engine.dependency_review_submit import review_packet_collection
from research_pipeline.engine.dependency_review_preflight import review_preflight


class BatchedPreflightReplayTests(unittest.TestCase):
    def test_two_disjoint_packets_one_replay_and_no_graph_mutation(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            Workspace(root).init({
                "schema_version": 1, "project": "Preflight cache fixture",
                "term_kind": "term", "content_kind": "definition",
                "adapter": "mathdef", "external_reference_mode": True,
                "independent_second_wave": True,
            })
            rec = root / "records"
            rows = [
                {"id": "meaning.one", "display_term": "One",
                 "context": "Abstract algebra",
                 "formulations": [{"id": "form.one",
                                    "text": "One is a test mathematical concept."}]},
                {"id": "meaning.two", "display_term": "Two",
                 "context": "Abstract algebra",
                 "formulations": [{"id": "form.two",
                                    "text": "Two is a separate mathematical concept."}]},
            ]
            (rec / "meanings.jsonl").write_text(
                "".join(json.dumps(x) + "\n" for x in rows), encoding="utf-8")
            (rec / "relations.jsonl").write_text("", encoding="utf-8")
            inventory_sync(root)
            graph = graph_path(root)
            inv = read(graph / "INVENTORY.json")
            def source(fid):
                return {
                    "formulation_id": fid,
                    "version_sha256": inv["formulations"][fid]["version_sha256"],
                    "complete": True,
                    "references": [],
                    "review_rationale": (
                        "Read the complete source and verified all initial references."),
                }
            store(root, [source("form.one"), source("form.two")])
            old_nodes = live_nodes(graph, inv)
            packets = root / "offline-packets"
            packets.mkdir()
            for i, fid in enumerate(("form.one", "form.two")):
                entry = source(fid)
                entry["references"] = [{
                    "phrase": "a primitive notation convention",
                    "state": "external",
                    "disposition": (
                        "No new mathematical concept is presupposed by this "
                        "ordinary mathematical notation convention."),
                }]
                entry.update({
                    "amendment_id": "amend.cache-fixture-" + str(i),
                    "expected_node_sha256": digest(old_nodes[fid]),
                    "reason": (
                        "Reviewed the complete parent text and determined "
                        "the appropriate non-dependent convention status."),
                    "reviewed_by": "independent-source-reviewer",
                })
                packet_id = "cache-fixture-" + str(i)
                (packets / (packet_id + ".json")).write_text(json.dumps({
                    "schema_version": 1, "id": packet_id, "mode": "amend",
                    "amendments": [entry],
                }), encoding="utf-8")

            before = {p.name: p.read_bytes() for p in graph.iterdir() if p.is_file()}
            with patch(
                "research_pipeline.engine.dependency_review_preflight.live_nodes",
                wraps=live_nodes,
            ) as replay:
                reviewed = review_packet_collection(root, packets)
                self.assertEqual(replay.call_count, 1)
            self.assertEqual(reviewed["packet_count"], 2)
            self.assertFalse(reviewed["mathematics_certified"])
            self.assertEqual(
                before, {p.name: p.read_bytes()
                         for p in graph.iterdir() if p.is_file()})
            self.assertFalse((graph / "applied").exists())
            self.assertFalse((graph / "amendments.jsonl").exists())

            # Ordinary standalone use still reloads the authoritative graph.
            result = review_preflight(root, packets / "cache-fixture-0.json")
            self.assertEqual(result["status"], "mechanically_valid_not_applied")


if __name__ == "__main__":
    unittest.main()
