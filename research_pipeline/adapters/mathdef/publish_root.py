"""Publish the approved, globally relinked cleaned mathDef collection.

The historical independent previews stay independent and frozen. This
function builds the verified cleaned catalog anew from read-only source data,
validates redirects for every original ID and source formulation, checks
all links, then renders the root UI and the v2 API. Nothing deploys to Pages
until the GitHub Pages workflow itself passes all release checks.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from research_pipeline.adapters.mathdef.original_merge import for_display, read_original
from research_pipeline.adapters.mathdef.stage_cleanup import stage as stage_cleanup
from research_pipeline.adapters.mathdef.rebuild_cleaned_links import rebuild as rebuild_links
from research_pipeline.adapters.mathdef.merged_cleanup import compile_source_registry
from research_pipeline.adapters.mathdef.audit_merged_links import audit
from research_pipeline.ui.renderer import render as render_ui
from scripts.merged_definition_export import (
    write_merged_definition_export, original_ids_for_meaning,
)


def verify_original_preservation(catalog: dict, originals: list[dict],
                                 historical: dict) -> dict:
    """Allow only documented approved redirects and explicit text adaptations.

    Validate the original-before-cleanup catalog against the immutable TeX.
    Then verify every original definition/formulation has a canonical home,
    carries its original provenance, and any canonical wording change has a
    recorded before/after decision. This is stricter than only counting IDs.
    """
    hist = {m.get("original_definition_id"): m for g in historical["groups"]
            for m in g["meanings"] if m.get("source_origin") == "original_mathdef"}
    forms = {f["id"]: f for g in catalog["groups"]
             for m in g["meanings"] for f in m["formulations"]}
    members = {}
    for group in catalog["groups"]:
        for m in group["meanings"]:
            for oid in original_ids_for_meaning(m):
                if oid in members:
                    raise ValueError("Original ID assigned to multiple surviving meanings: "+oid)
                members[oid] = m
    form_aliases = catalog.get("consolidated_ids", {}).get("formulation_aliases", {})
    modified = merged = unchanged = 0
    for original in originals:
        oid = original["id"]
        h = hist.get(oid)
        if not h:
            raise ValueError("Frozen original definition missing from historical merged catalog: "+oid)
        live = members.get(oid)
        if not live:
            raise ValueError("Original definition ID not preserved by cleanup redirects: "+oid)
        original_forms = original.get("formulations") or [{
            "key": "primary", "body": original["body"]}]
        historical_forms = {f["id"]:f for f in h["formulations"]}
        for f in original_forms:
            old_id = "form.mathdef.original."+oid+"."+f["key"]
            expected = for_display(f["body"])
            if old_id not in historical_forms or historical_forms[old_id]["text"] != expected:
                raise ValueError("Historical original source text mismatch: "+old_id)
            live_id = form_aliases.get(old_id, old_id)
            current = forms.get(live_id)
            if not current:
                raise ValueError("Original formulation has no live redirect: "+old_id)
            if old_id in form_aliases:
                merged += 1
                # A consolidated original definition must retain its source
                # provenance in the winning form's citation records.
                path = "https://github.com/Zengez/mathDef/blob/main/"+original["path"]
                if not any(x.get("url") == path for x in current.get("sources", [])):
                    raise ValueError("Redirected original lost source-file provenance: "+old_id)
            elif current["text"] == expected:
                unchanged += 1
            else:
                edit = current.get("canonical_editorial_edit") or current.get("editorial_translation")
                if not edit or edit.get("original_text") != expected or edit.get("text") != current["text"]:
                    raise ValueError("Original formulation altered without an approved recorded edit: "+old_id)
                modified += 1
    if set(members) != {x["id"] for x in originals}:
        raise ValueError("Additional or missing historical original aliases in cleaned corpus")
    return {
        "original_definition_count": len(originals),
        "original_formulations_unchanged": unchanged,
        "original_formulations_editorially_adapted": modified,
        "original_formulations_consolidated_with_source_provenance": merged,
        "original_definition_ids_preserved": len(members),
    }


def publish(repo: Path, site: Path) -> dict:
    repo, site = repo.resolve(), site.resolve()
    preview = site / "reconstruction" / "merged"
    if not (preview / "catalog.json").is_file():
        preview = site / "merged"
    historical_file = preview / "catalog.json"
    if not historical_file.is_file():
        raise FileNotFoundError(
            "Historical merged research preview missing; build reconstruction previews first"
        )
    originals = read_original(repo)
    historical = json.loads(historical_file.read_text(encoding="utf-8"))
    with TemporaryDirectory(prefix="mathdef-release-") as tmp:
        work = Path(tmp)
        stage_cleanup(repo, work / "staged")
        link_result = rebuild_links(
            work / "staged", work / "linked",
            overrides=json.loads((repo / "data/definition_expansion_priority_overrides.json")
                                 .read_text(encoding="utf-8")),
            context_resolutions=json.loads((repo / "data/global_link_context_resolutions_2026-10-27.json")
                                           .read_text(encoding="utf-8")),
        )
        catalog_path = work / "linked" / "catalog.global-linked.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        preservation = verify_original_preservation(catalog, originals, historical)
        source_registry = compile_source_registry(catalog, repo=repo)
        source_registry["consolidated_ids"] = catalog.get("consolidated_ids", {})
        branding = repo / "research_pipeline/adapters/mathdef/ui_branding.json"
        counts = render_ui(
            catalog_path, branding, site,
            "Complete mathematical definitions",
            "Original mathDef and research-added meanings, definitions, and links.",
            production=True,
            expansion_overrides_file=repo / "data/definition_expansion_priority_overrides.json",
            source_registry=source_registry,
        )
        # The public catalog, UI index, API feed and full-graph audit MUST all
        # come from this exact version of the cleaned data.
        shutil.copyfile(catalog_path, site / "catalog.json")
        shutil.copyfile(work / "linked" / "link-report.global-linked.json",
                        site / "link-report.json")
        (site / "audits").mkdir(exist_ok=True)
        shutil.copyfile(work / "linked" / "global-link-rebuild-summary.json",
                        site / "audits" / "global-link-rebuild.json")
        shutil.copyfile(work / "linked" / "historical-source-edge-reconciliation.json",
                        site / "audits" / "historical-source-edges.json")
        published = json.loads((site / "definitions-index.json").read_text(encoding="utf-8"))
        full_audit = audit(catalog, published)
        blocked = ("errors", "duplicate_form_target", "overlapping_spans", "masked_source_anchor")
        if any(full_audit["anomaly_counts"].get(key, 0) for key in blocked):
            raise ValueError("Published site introduces broken link graph: "+
                             str(full_audit["anomaly_counts"]))
        (site / "audits" / "full-link-graph.json").write_text(
            json.dumps(full_audit, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        # Check the generated canonical corpus, not historical cohort sizes:
        # newly approved meanings/headings MUST be able to grow this release.
        expected_terms = len(catalog["groups"])
        expected_forms = sum(len(m["formulations"]) for g in catalog["groups"]
                             for m in g["meanings"])
        if counts["terms"] != expected_terms or counts["formulations"] != expected_forms:
            raise ValueError("Rendered cleaned corpus differs from canonical catalog")
        merged_feed = write_merged_definition_export(catalog, published, site)
        if merged_feed["original_definition_count"] != len(originals):
            raise ValueError("v2 feed dropped original definitions after cleanup")
        from scripts.validate_published_corpus import validate_site
        validate_site(site)
        return {
            **counts, **preservation,
            "merged_feed": merged_feed,
            "merged_meanings": link_result["stats"]["meanings"],
            "linked_formulations": sum(
                bool(f["dependencies"]) for term in published
                for f in term["formulations"]),
            "relations": len(catalog["relations"]),
            "global_link_audit_anomalies": full_audit["anomaly_counts"],
            "unlinked_existing_term_occurrences": link_result["unlinked_existing_term_occurrences"],
            "production_root": str(site),
            "reconstruction_preview_preserved": preview.is_dir(),
            "cleaned_source_identities": len(source_registry["sources"]),
        }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=Path.cwd())
    p.add_argument("--site-root", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(publish(args.repo_root, args.site_root), indent=2))


if __name__ == "__main__":
    main()
