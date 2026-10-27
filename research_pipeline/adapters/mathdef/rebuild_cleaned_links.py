"""One authorized post-cleanup *global link* rebuild and full link audit.

Strictly stage-only: the independent Wave2, original TeX, and post-Wave2
research inputs are read-only. No new vocabulary scan, no root publication,
no v2 export, and no GitHub Pages deployment.

The upstream cleanup intentionally drops dependent-text spans when wording or
formulation ownership changes. Rebuild links on the canonical survivor texts,
preserving reviewed relationship IDs and recording unavoidable uncertainty.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path

from research_pipeline.adapters.mathdef.audit_merged_links import audit
from research_pipeline.adapters.mathdef.merged_linking import (
    link_merged_catalog, masked_prose,
)
from research_pipeline.ui.renderer import to_index, to_sources_index


class FinalLinkError(ValueError):
    """Invalid or unrepairable global link graph after a cleanup rebuild."""


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def inspect_existing_links(catalog: dict) -> dict:
    """Deanchor *only* stale source spans, never silently drop a relation.

    The linker then reanchors surviving screened links when their actual term
    occurs in the updated source wording. Invalid spans cannot be rendered.
    """
    bodies = {
        form["id"]: form["text"]
        for group in catalog["groups"]
        for meaning in group["meanings"]
        for form in meaning["formulations"]
    }
    meaning_ids = {
        meaning["id"]
        for group in catalog["groups"] for meaning in group["meanings"]
    }
    report = {
        "invalid_span_positions_reset": [],
        "stale_source_phrases_reset": [],
        "math_masked_anchors_reset": [],
    }
    for rel in catalog["relations"]:
        fid, mid = rel.get("from_formulation"), rel.get("target_meaning")
        if fid not in bodies or mid not in meaning_ids:
            raise FinalLinkError(f"Dangling pre-rebuild relation {rel.get('id')}: {fid} -> {mid}")
        if rel.get("relation_type") != "definition_uses":
            continue
        start, end = rel.get("span_start", -1), rel.get("span_end", -1)
        if (isinstance(start, int) and start < 0
                and (end is None or not isinstance(end, int) or end < 0)):
            continue  # Curated unpositioned link.
        body = bodies[fid]
        if (type(start) is not int or type(end) is not int
                or start < 0 or end <= start or end > len(body)):
            reason = "invalid_span_positions_reset"
        elif body[start:end] != rel.get("source_phrase", body[start:end]):
            reason = "stale_source_phrases_reset"
        elif not masked_prose(body)[start:end].strip():
            reason = "math_masked_anchors_reset"
        else:
            continue
        report[reason].append({
            "relation_id": rel.get("id"), "source_formulation": fid,
            "target_meaning": mid, "old_source_phrase": rel.get("source_phrase"),
        })
        for k in ("span_start", "span_end", "source_phrase"):
            rel.pop(k, None)
    return report


def _assert_clean_graph(audited: dict) -> None:
    blockers = ("errors", "duplicate_form_target", "overlapping_spans",
                "masked_source_anchor")
    present = {k: audited["anomaly_counts"].get(k, 0)
               for k in blockers if audited["anomaly_counts"].get(k, 0)}
    if present:
        samples = {key: audited["anomalies"].get(key, [])[:4] for key in present}
        raise FinalLinkError(f"Whole-graph audit blockers: {present}; examples: {samples}")


def rebuild(stage: Path, output: Path, *, overrides: dict | None = None) -> dict:
    stage, output = Path(stage), Path(output)
    catalog = deepcopy(_load(stage / "catalog.stage-only.json"))
    sources = _load(stage / "sources.stage-only.json")
    preexisting = {rel["id"] for rel in catalog["relations"]}
    cleanup_report = _load(stage / "cleanup-report.stage-only.json")
    fixed = inspect_existing_links(catalog)
    linking = link_merged_catalog(catalog)
    # Preserve existing reviewed edges and their stable IDs while admitting
    # newly generated tentative, lexically anchored links.
    surviving = {rel["id"] for rel in catalog["relations"]}
    if not preexisting.issubset(surviving):
        raise FinalLinkError("The link rebuild discarded an existing reviewed relation")
    index = to_index(catalog, expansion_overrides=overrides)
    to_sources_index(catalog, sources)
    audited = audit(catalog, index)
    _assert_clean_graph(audited)
    # The renderer must preserve term/formulation count and every link, not
    # just a majority of the original corpus.
    if len(index) != len(catalog["groups"]):
        raise FinalLinkError("Rendered global term heading count drift")
    formulation_total = sum(len(e["formulations"]) for e in index)
    if formulation_total != cleanup_report["surviving_formulations"]:
        raise FinalLinkError("A formulation disappeared during link rebuilding")
    # Second linker pass should not discover any *new* lexical edges. Retain
    # the original catalog with exactly one rebuild; test idempotence on copy.
    replay = deepcopy(catalog)
    again = link_merged_catalog(replay)
    if again["new_tentative_links"] or replay["relations"] != catalog["relations"]:
        raise FinalLinkError(
            "Global link rebuild is not idempotent: "+
            str(again["new_tentative_links"])+" second-pass additions")
    form_ids = {f["id"] for g in catalog["groups"]
                for m in g["meanings"] for f in m["formulations"]}
    meaning_ids = {m["id"] for g in catalog["groups"] for m in g["meanings"]}
    aliases = catalog.get("consolidated_ids", {})
    for old, live in aliases.get("formulation_aliases", {}).items():
        if old in form_ids or live not in form_ids:
            raise FinalLinkError("Broken formulation redirect: " + old)
    for old, live in aliases.get("meaning_aliases", {}).items():
        if old in meaning_ids or live not in meaning_ids:
            raise FinalLinkError("Broken meaning redirect: " + old)
    stats = audited["stats"]
    result = {
        "schema_version": 1,
        "scope": "cleaned_mathdef_global_existing_term_link_rebuild",
        "status": "audited_stage_only_not_published",
        "no_new_terminology_discovery": True,
        "publication_or_v2_export": False,
        "stats": stats,
        "rebuild": {k:v for k,v in linking.items() if k not in (
            "links_by_form", "new_tentative_link_examples", "ambiguous_context_examples")},
        "preexisting_relations_retained": len(preexisting),
        "anchor_repairs": fixed,
        "cleanup_intentionally_dropped_links": cleanup_report.get("relations_needing_relink", []),
        "graph_audit_anomaly_counts": audited["anomaly_counts"],
        "unlinked_existing_term_occurrences":
            audited["known_existing_term_unlinked"]["total_occurrences"],
        "unlinked_existing_term_targets":
            audited["known_existing_term_unlinked"]["distinct_target_labels"],
        "subject_and_priority_override_display_preserved": True,
        "source_registry_identities": len(sources["sources"]),
        "original_ids_retained": cleanup_report.get("original_definition_ids_retained"),
        "idempotent": True,
        "remarks": [
            "Suggested lexical links are not certified mathematical implications.",
            "Unlinked existing-term labels can reflect legitimate source-convention ambiguity.",
            "All original/Wave1/independent-Wave2 source collections remain immutable.",
        ],
    }
    _save(output / "catalog.global-linked.json", catalog)
    _save(output / "definitions-index.global-linked.json", index)
    _save(output / "link-report.global-linked.json", linking)
    _save(output / "link-audit.global-linked.json", audited)
    _save(output / "global-link-rebuild-summary.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--overrides", type=Path)
    args = parser.parse_args()
    report = rebuild(args.stage, args.output, overrides=(
        _load(args.overrides) if args.overrides else None
    ))
    print("CLEANED_GLOBAL_LINK_SUMMARY_JSON="+json.dumps(report, separators=(",", ":")))


if __name__ == "__main__":
    main()
