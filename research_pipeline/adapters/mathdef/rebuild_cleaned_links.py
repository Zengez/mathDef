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
import re
from pathlib import Path

from research_pipeline.adapters.mathdef.audit_merged_links import audit
from research_pipeline.adapters.mathdef.merged_linking import (
    link_merged_catalog, masked_prose, words, name_index, WORD_RE,
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



def _literal_target_headings_in_form(catalog: dict, form_id: str) -> set[str]:
    """Check surviving literal visible term mentions; no semantic guessing."""
    groups = {g["id"]: g for g in catalog["groups"]}
    body = next((f["text"] for g in catalog["groups"]
                 for m in g["meanings"] for f in m["formulations"]
                 if f["id"] == form_id), None)
    if body is None:
        raise FinalLinkError("Obsolete source formulation redirect: " + form_id)
    idx = name_index(catalog)
    masked = masked_prose(body)
    tokens = [(m.group(0).casefold(),m.start(),m.end())
              for m in WORD_RE.finditer(masked)]
    seen = set()
    for i in range(len(tokens)):
        for parts,gids in idx.get(tokens[i][0],()):
            end=i+len(parts)
            if end>len(tokens) or tuple(t[0] for t in tokens[i:end])!=parts:
                continue
            if any(not re.fullmatch(r"\s+|\s*[-–]\s*",body[tokens[k][2]:tokens[k+1][1]])
                   for k in range(i,end-1)):
                continue
            seen.update(gids)
    return seen


def reconcile_deleted_source_edges(catalog: dict, cleanup_report: dict) -> dict:
    """Explain every invalidated *historical* source-text link's disposition.

    These old IDs were removed intentionally because source wording changed
    or the original formulation was consolidated. A relation's old source
    span cannot be copied across texts. Identify whether the surviving
    formulation was re-linked to the identical target meaning, an alternate
    meaning in that same heading, or no longer has a literal target mention.
    """
    details = cleanup_report.get("deleted_source_text_edge_details", [])
    expected = cleanup_report.get("deleted_source_text_edges_needing_global_relink", [])
    if len(details)!=len(expected) or {x["old_relation_id"] for x in details}!=set(expected):
        raise FinalLinkError("Incomplete historical text-edge relocation ledger")
    meaning_groups = {m["id"]:g["id"]
                      for g in catalog["groups"] for m in g["meanings"]}
    by_form = {}
    for rel in catalog["relations"]:
        if rel["relation_type"]!="definition_uses":continue
        by_form.setdefault(rel["from_formulation"], []).append(rel)
    heading_cache={}
    result=[]
    for row in details:
        fid,mid=row["live_source_formulation_id"],row["live_target_meaning_id"]
        gid=meaning_groups.get(mid)
        if not gid: raise FinalLinkError("Historical source edge redirected to dead meaning: "+mid)
        if fid not in heading_cache:
            heading_cache[fid]=_literal_target_headings_in_form(catalog,fid)
        outgoing=by_form.get(fid,[])
        if any(r["target_meaning"]==mid for r in outgoing):
            status="relinked_to_same_meaning"
        elif any(meaning_groups[r["target_meaning"]]==gid for r in outgoing):
            status="relinked_to_same_heading_alternate_meaning"
        elif gid in heading_cache[fid]:
            status="unlinked_literal_still_present_requires_review"
        else:
            status="no_longer_mentions_target_heading_in_visible_prose"
        result.append({**row,"target_group_id":gid,"status":status})
    counts=dict(sorted(Counter(r["status"] for r in result).items()))
    return {"count":len(result),"status_counts":counts,"edges":result}


def _assert_clean_graph(audited: dict) -> None:
    blockers = ("errors", "duplicate_form_target", "overlapping_spans",
                "masked_source_anchor")
    present = {k: audited["anomaly_counts"].get(k, 0)
               for k in blockers if audited["anomaly_counts"].get(k, 0)}
    if present:
        samples = {key: audited["anomalies"].get(key, [])[:4] for key in present}
        raise FinalLinkError(f"Whole-graph audit blockers: {present}; examples: {samples}")


def _validated_scoped_resolutions(catalog: dict, ledger: dict | None) -> dict:
    if ledger is None:
        return {}
    if (ledger.get("schema_version") != 1 or not isinstance(ledger.get("rules"), list)):
        raise FinalLinkError("Invalid reviewed scoped link resolutions")
    meanings = {m["id"]:g["id"] for g in catalog["groups"] for m in g["meanings"]}
    groups = {g["id"] for g in catalog["groups"]}
    result = {}
    for row in ledger["rules"]:
        source = row.get("source_meaning_id")
        gid = row.get("target_group_id")
        target = row.get("preferred_target_meaning_id")
        if (not source in meanings or gid not in groups or meanings.get(target) != gid
                or not row.get("id") or not row.get("reason")):
            raise FinalLinkError("Stale or incomplete scoped resolution: " + str(row.get("id")))
        key = (source, gid)
        if key in result:
            raise FinalLinkError("Duplicate scoped source/target group resolution: "+str(key))
        result[key] = target
    return result


def rebuild(stage: Path, output: Path, *, overrides: dict | None = None,
            context_resolutions: dict | None = None) -> dict:
    stage, output = Path(stage), Path(output)
    catalog = deepcopy(_load(stage / "catalog.stage-only.json"))
    sources = _load(stage / "sources.stage-only.json")
    preexisting = {rel["id"] for rel in catalog["relations"]}
    cleanup_report = _load(stage / "cleanup-report.stage-only.json")
    fixed = inspect_existing_links(catalog)
    scoped = _validated_scoped_resolutions(catalog, context_resolutions)
    linking = link_merged_catalog(catalog, scoped_resolutions=scoped)
    seen = set(linking["scoped_context_selection_uses"])
    expected = {src+" -> "+gid for src, gid in scoped}
    if seen != expected:
        raise FinalLinkError("Scoped resolutions not used in source text: "+str(sorted(expected-seen)))
    # Preserve existing reviewed edges and their stable IDs while admitting
    # newly generated tentative, lexically anchored links.
    surviving = {rel["id"] for rel in catalog["relations"]}
    if not preexisting.issubset(surviving):
        raise FinalLinkError("The link rebuild discarded an existing reviewed relation")
    index = to_index(catalog, expansion_overrides=overrides)
    to_sources_index(catalog, sources)
    audited = audit(catalog, index)
    _assert_clean_graph(audited)
    historical_reconciliation = reconcile_deleted_source_edges(catalog, cleanup_report)
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
    again = link_merged_catalog(replay, scoped_resolutions=scoped)
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
        "reviewed_scoped_resolution_rules": len(scoped),
        "reviewed_scoped_resolution_occurrences":
            sum(linking["scoped_context_selection_uses"].values()),
        "cleanup_intentionally_dropped_links": cleanup_report.get(
            "deleted_source_text_edges_needing_global_relink", []),
        "historical_source_text_edge_reconciliation_counts":
            historical_reconciliation["status_counts"],
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
    _save(output / "historical-source-edge-reconciliation.json", historical_reconciliation)
    _save(output / "global-link-rebuild-summary.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--overrides", type=Path)
    parser.add_argument("--context-resolutions", type=Path)
    args = parser.parse_args()
    report = rebuild(args.stage, args.output, overrides=(
        _load(args.overrides) if args.overrides else None
    ), context_resolutions=(
        _load(args.context_resolutions) if args.context_resolutions else None
    ))
    print("CLEANED_GLOBAL_LINK_SUMMARY_JSON="+json.dumps(report, separators=(",", ":")))


if __name__ == "__main__":
    main()
