"""Build a strictly stage-only merged cleanup snapshot, WITHOUT global linking.

No final link audit, publication, production API export or browser build is
triggered. Historical original/Wave2/post-wave source corpora are read-only.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from research_pipeline.adapters.mathdef.preview import build as build_wave2
from research_pipeline.adapters.mathdef.original_merge import read_original, merge_original
from research_pipeline.adapters.mathdef.direct_additions import add_direct_research
from research_pipeline.adapters.mathdef.merged_cleanup import write_stage_only

WAVE2 = Path("research_pipeline/experiments/reconstruction-v2-independent")


def stage(repo: Path, output: Path) -> dict:
    repo = Path(repo).resolve()
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="mathdef-cleanup-wave2-") as tmp:
        draft = Path(tmp) / "wave2"
        build_wave2(repo / WAVE2, draft=True, output=draft)
        independent = json.loads((draft / "catalog.json").read_text(encoding="utf-8"))
    original = read_original(repo)
    combined, baseline = merge_original(independent, original)
    post_n = add_direct_research(
        combined["groups"], combined["relations"], repo / WAVE2 / "post_wave2" / "terms.json"
    )
    # Inventory existing term/meaning overlap only; no new term detection.
    cross_source = []
    research_only_multiple = []
    for group in combined["groups"]:
        meanings = group["meanings"]
        original_ids = [m["id"] for m in meanings
                        if m.get("source_origin") == "original_mathdef"]
        researched_ids = [m["id"] for m in meanings
                          if m.get("source_origin") != "original_mathdef"]
        if original_ids and researched_ids:
            cross_source.append({"title": group["title"], "group_id": group["id"],
                                 "original_ids": original_ids,
                                 "researched_ids": researched_ids})
        elif not original_ids and len(researched_ids) > 1:
            research_only_multiple.append(
                {"title": group["title"], "group_id": group["id"],
                 "researched_ids": researched_ids}
            )
    inventory = {
        "schema_version": 1, "stage": "existing_grouped_definitions_only",
        "original_versus_researched": sorted(cross_source,
                                            key=lambda row: row["title"].casefold()),
        "within_research": sorted(research_only_multiple,
                                  key=lambda row: row["title"].casefold()),
        "no_new_candidates": True,
    }
    (output / "comparison-inventory.stage-only.json").write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + chr(10),
        encoding="utf-8",
    )
    report = write_stage_only(combined, repo, output)
    report["original_new_overlap_groups_before_cleanup"] = len(cross_source)
    report["research_only_multi_groups_before_cleanup"] = len(research_only_multiple)
    report["upstream_original_count"] = len(original)
    report["upstream_post_wave2_count"] = post_n
    report["upstream_original_merge_baseline"] = baseline
    (output / "build-provenance.stage-only.json").write_text(
        json.dumps({
            "status": "stage_only_before_user_decision",
            "full_linking_rebuild_ran": False,
            "final_link_audit_ran": False,
            "published": False,
            "baseline": baseline,
            "post_wave2_added": post_n,
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(stage(args.repo_root, args.output), indent=2))


if __name__ == "__main__":
    main()
