"""Plain researched-term additions for the independent Wave 2 preview.

This module deliberately does not implement a research queue, graph gate,
publication stage, or access to production/frozen mathematical corpora.
One small JSON content file -> the already working searchable preview.
"""
from __future__ import annotations

import json
from pathlib import Path

from research_pipeline.engine.core import PipelineError, digest


def _nonempty(value, field):
    if not isinstance(value, str) or not value.strip():
        raise PipelineError(f"Direct research entry requires {field}")
    return value


def _titlekey(title):
    return " ".join(title.casefold().split())


def add_direct_research(groups: list, relations: list, file: Path) -> int:
    """Add researched meanings/links to display data, without changing source files.

    The supplied groups and relations are the independent screened Wave2 preview
    catalog (not the production or frozen Wave1 catalog). Every link must point
    to a meaning in the combined preview; unresearched links can simply wait.
    """
    file = Path(file)
    if not file.is_file():
        return 0
    data = json.loads(file.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("entries"), list):
        raise PipelineError("Direct research file needs schema_version=1 and entries[]")
    group_by_title = {_titlekey(g["title"]): g for g in groups}
    meaning_ids = {m["id"] for g in groups for m in g["meanings"]}
    form_ids = {f["id"] for g in groups for m in g["meanings"] for f in m["formulations"]}
    staged = []
    for entry in data["entries"]:
        if not isinstance(entry, dict):
            raise PipelineError("Direct research entries must be objects")
        mid = _nonempty(entry.get("id"), "id")
        term = _nonempty(entry.get("term"), "term")
        context = _nonempty(entry.get("context"), "context")
        definition = _nonempty(entry.get("definition"), "definition")
        fid = "form." + mid
        if mid in meaning_ids or fid in form_ids:
            raise PipelineError(f"Duplicate direct-research meaning/formulation: {mid}")
        meaning_ids.add(mid)
        form_ids.add(fid)
        sources = entry.get("sources")
        if not isinstance(sources, list) or not sources:
            raise PipelineError(f"Missing source references for {mid}")
        citations = []
        for source in sources:
            title = _nonempty(source.get("title"), "source title")
            url = _nonempty(source.get("url"), "source url")
            if not url.startswith("https://"):
                raise PipelineError(f"Non-HTTPS source for {mid}")
            grade = _nonempty(source.get("verification_status"), "source verification status")
            citations.append({
                "title": title, "url": url, "locator": url,
                "role": "Independent research source (" + grade + "); not human certified",
                "verification_status": grade,
            })
        key = _titlekey(term)
        group = group_by_title.get(key)
        if group is None:
            gid = "preview.term." + digest(key)[:24]
            if any(x["id"] == gid for x in groups):
                raise PipelineError(f"Term group ID collision for {term}")
            group = {"id": gid, "title": term, "aliases": [], "meanings": []}
            groups.append(group)
            group_by_title[key] = group
        for alias in entry.get("aliases", []):
            _nonempty(alias, "alias")
            if alias.casefold() != term.casefold() and alias not in group["aliases"]:
                group["aliases"].append(alias)
        group["meanings"].append({
            "id": mid, "label": context, "display_term": term,
            "term_group_id": group["id"], "other_sources": [],
            "research_status": entry.get("research_status", "provisional"),
            "original_candidate_id": entry.get("candidate_id"),
            "formulations": [{
                "id": fid, "text": definition, "sha256": digest(definition),
                "sources": citations, "review_state": "screened",
                "research_status": "assistant-reviewed draft; not certified",
            }],
        })
        links = entry.get("links", [])
        if not isinstance(links, list):
            raise PipelineError(f"links must be an array for {mid}")
        staged.append((mid, fid, links))
    for mid, fid, links in staged:
        seen_targets = set()
        for number, link in enumerate(links):
            target = _nonempty(link.get("target_meaning"), "target_meaning")
            relation_type = link.get("relation_type", "related")
            if relation_type not in ("definition_uses", "related"):
                raise PipelineError(f"Unsupported link kind for {mid}: {relation_type}")
            if target not in meaning_ids:
                raise PipelineError(f"Unknown meaning link from {mid}: {target}")
            if target in seen_targets:
                raise PipelineError(f"Duplicate link to {target} from {mid}")
            seen_targets.add(target)
            relations.append({
                "id": "rel.wave2.direct." + mid + "." + str(number),
                "from_formulation": fid, "target_meaning": target,
                "relation_type": relation_type, "review_state": "screened",
            })
    for group in groups:
        group["meanings"].sort(key=lambda x: (x["label"].casefold(), x["id"]))
        group["aliases"].sort(key=str.casefold)
    groups.sort(key=lambda x: (x["title"].casefold(), x["id"]))
    return len(staged)
