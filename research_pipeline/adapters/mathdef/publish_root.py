"""Publish the already-verified merged mathematical corpus as the main site.

The source collections are immutable inputs, not an export to .tex.
Invoke AFTER scripts/build_index.py and the reconstruction preview builder.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from research_pipeline.adapters.mathdef.original_merge import (
    for_display, read_original,
)
from research_pipeline.ui.renderer import render as render_ui
from scripts.merged_definition_export import write_merged_definition_export


def publish(repo: Path, site: Path) -> dict:
    repo, site = repo.resolve(), site.resolve()
    # The GitHub Pages artifact nests previews under /reconstruction.
    # A standalone reconstruction smoke build already uses its own root.
    preview = site / "reconstruction" / "merged"
    if not (preview / "catalog.json").is_file():
        preview = site / "merged"
    catalog_path = preview / "catalog.json"
    if not catalog_path.is_file():
        raise FileNotFoundError(
            "Merged catalog missing; build the reconstruction preview before publishing"
        )
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    original_meanings = {
        meaning.get("original_definition_id"): meaning
        for group in catalog["groups"]
        for meaning in group["meanings"]
        if meaning.get("source_origin") == "original_mathdef"
    }
    originals = read_original(repo)
    if len(original_meanings) != len(originals):
        raise ValueError("The merged site does not preserve every original definition")
    for definition in originals:
        meaning = original_meanings.get(definition["id"])
        if meaning is None:
            raise ValueError(f"Missing original definition: {definition['id']}")
        expected = definition.get("formulations") or [{
            "key": "primary", "body": definition["body"]
        }]
        actual = {f["id"]: f["text"] for f in meaning["formulations"]}
        for form in expected:
            fid = "form.mathdef.original." + definition["id"] + "." + form["key"]
            if actual.get(fid) != for_display(form["body"]):
                raise ValueError(f"Original formulation not preserved: {fid}")
    branding = repo / "research_pipeline/adapters/mathdef/ui_branding.json"
    counts = render_ui(
        catalog_path,
        branding,
        site,
        "Complete mathematical definitions",
        "Original mathDef and research-added meanings, definitions, and links.",
        production=True,
        # Future accepted visitor suggestions must be explicitly approved
        # here before changing any displayed definition's priority.
        expansion_overrides_file=repo / "data/definition_expansion_priority_overrides.json",
    )
    # The canonical site publishes the complete meaning-level catalog and link
    # evidence too. The original .tex sources and comparison previews remain
    # available in the same repository/deployment.
    shutil.copyfile(catalog_path, site / "catalog.json")
    shutil.copyfile(preview / "link-report.json", site / "link-report.json")

    published = json.loads((site / "definitions-index.json").read_text(
        encoding="utf-8"
    ))
    if len(published) != len(catalog["groups"]):
        raise ValueError("Main site does not contain all merged term groups")
    merged_feed = write_merged_definition_export(catalog, published, site)
    if sum(len(group["meanings"]) for group in catalog["groups"]) < len(originals):
        raise ValueError("Main site contains fewer meanings than original mathDef")
    return {
        **counts,
        "original_definitions_preserved": len(originals),
        "merged_feed": merged_feed,
        "merged_meanings": sum(len(group["meanings"]) for group in catalog["groups"]),
        "linked_formulations": sum(
            bool(f["dependencies"])
            for term in published for f in term["formulations"]
        ),
        "production_root": str(site),
        "reconstruction_preview_preserved": preview.is_dir(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--site-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(publish(args.repo_root, args.site_root), indent=2))


if __name__ == "__main__":
    main()
