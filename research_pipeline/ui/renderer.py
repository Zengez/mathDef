"""Portable reference UI rendering; accepts a display-only catalog and branding.

No knowledge of mathDef, definitions, theorem records or production content paths.
Domain-specific adapters must convert their independently acquired research
into the 'groups/meanings/formulations/relations' display contract.
"""
from __future__ import annotations
import html
import json
import shutil
from collections import defaultdict
from pathlib import Path


class ViewError(ValueError):
    """Refuse incomplete and mismatched display data."""


def read_json(path: Path):
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ViewError("Expected a JSON object")
    return obj



def _validated_expansion_overrides(catalog: dict, overrides: dict | None,
                                   form_owner: dict, meaning_to_group: dict) -> dict:
    """Resolve approved display-only overrides against the actual live links.

    Each approval identifies a source formulation and linked term group. An
    optional exact character span scopes it to ONE occurrence, overriding a
    general rule when both exist. The selected target must be a real
    formulation of that group. No definition text or relation is edited.
    """
    if overrides is None:
        return {}
    if (not isinstance(overrides, dict) or overrides.get("schema_version") != 1
            or not isinstance(overrides.get("overrides"), list)):
        raise ViewError("Invalid approved expansion-priority registry")
    relations = catalog["relations"]
    rules = {}
    ids = set()
    for row in overrides["overrides"]:
        required = ("id", "source_formulation_id", "target_group_id",
                    "preferred_formulation_id", "approval_reference", "reason")
        if not isinstance(row, dict) or any(
                not isinstance(row.get(field), str) or not row[field].strip()
                for field in required):
            raise ViewError("Incomplete approved expansion-priority override")
        if row.get("status") != "approved":
            raise ViewError("Display priority may only use explicitly approved overrides")
        rule_id = row["id"]
        if rule_id in ids:
            raise ViewError("Duplicate expansion-priority override ID: " + rule_id)
        ids.add(rule_id)
        source, target = row["source_formulation_id"], row["target_group_id"]
        chosen = row["preferred_formulation_id"]
        if source not in form_owner:
            raise ViewError("Unknown override source formulation: " + source)
        if chosen not in form_owner or form_owner[chosen] != target:
            raise ViewError("Override priority target formulation is outside linked term: " + chosen)
        span = row.get("source_span")
        if span is not None:
            if (not isinstance(span, dict) or set(span) != {"start", "end"}
                    or any(type(span[k]) is not int for k in ("start", "end"))
                    or span["start"] < 0 or span["end"] <= span["start"]):
                raise ViewError("Invalid exact source span in override: " + rule_id)
            span_key = (span["start"], span["end"])
        else:
            span_key = None
        selector = (source, target, span_key)
        if selector in rules:
            raise ViewError("Conflicting/duplicate approved overrides for the same link selector")
        matched = [rel for rel in relations
                   if rel.get("relation_type") == "definition_uses"
                   and rel.get("from_formulation") == source
                   and meaning_to_group.get(rel.get("target_meaning")) == target
                   and (span_key is None or
                        (rel.get("span_start"), rel.get("span_end")) == span_key)]
        if not matched:
            raise ViewError("Approved override does not identify a live definition link: " + rule_id)
        rules[selector] = (chosen, rule_id)
    return rules

def to_index(catalog: dict, *, expansion_overrides: dict | None = None) -> list[dict]:
    """Convert source- and context-specific meanings into the common UI index.

    Group by supplied term identities only. Never infer equivalence or match
    mathematical concepts from labels, text, production definitions, etc.
    """
    groups = catalog.get("groups")
    relations = catalog.get("relations")
    if not isinstance(groups, list) or not isinstance(relations, list):
        raise ViewError("Display contract requires groups and relations")
    meaning_to_group = {}
    group_by_id = {}
    form_owner = {}
    for group in groups:
        gid = group["id"]
        if gid in group_by_id:
            raise ViewError("Duplicate term group")
        group_by_id[gid] = group
        for meaning in group["meanings"]:
            mid = meaning["id"]
            if mid in meaning_to_group:
                raise ViewError("Duplicate meaning")
            meaning_to_group[mid] = gid
            for form in meaning["formulations"]:
                fid = form["id"]
                if fid in form_owner:
                    raise ViewError("Duplicate formulation")
                form_owner[fid] = gid
    priority_rules = _validated_expansion_overrides(
        catalog, expansion_overrides, form_owner, meaning_to_group
    )
    dep_by_form = defaultdict(list)
    related_by_group = defaultdict(set)
    for rel in relations:
        source = form_owner.get(rel.get("from_formulation"))
        target = meaning_to_group.get(rel.get("target_meaning"))
        if source is None or target is None:
            raise ViewError("Broken displayed relation endpoint")
        if rel.get("review_state", "screened") not in ("screened", "lexical_candidate"):
            raise ViewError("Cannot render unsupported relationship state")
        if rel.get("relation_type") == "definition_uses":
            from_form = rel["from_formulation"]
            span = (rel.get("span_start", -1), rel.get("span_end", -1))
            # A specific approved occurrence takes precedence over a broad
            # source-formulation -> target-term rule.
            approved = priority_rules.get((from_form, target, span)) or (
                priority_rules.get((from_form, target, None)))
            dep = {
                "id": target, "label": group_by_id[target]["title"],
                "formulation": from_form,
                "target_meaning": rel["target_meaning"],
                "start": span[0], "end": span[1],
                "review_state": rel.get("review_state", "screened"),
                "source_phrase": rel.get("source_phrase", ""),
            }
            if approved is not None:
                dep["preferred_formulation"] = approved[0]
                dep["priority_override_id"] = approved[1]
            dep_by_form[from_form].append(dep)
        else:
            related_by_group[source].add(target)
    result = []
    for group in groups:
        forms = []
        dependencies = []
        seen_edges = {}
        for meaning in group["meanings"]:
            for form in meaning["formulations"]:
                sources = form.get("sources", [])
                if not sources or not all(s.get("title") and
                        (s.get("url") or s.get("locator")) for s in sources):
                    raise ViewError("Missing formulation source evidence")
                deps = dep_by_form.get(form["id"], [])
                forms.append({
                    "key": form["id"],
                    "label": meaning["label"],
                    "body": form["text"],
                    "source": sources[0].get("locator") or sources[0].get("url"),
                    "sources": sources,
                    "path": "",
                    "dependencies": deps,
                    "meaning_id": meaning["id"],
                    # Official mathematical Subject is inherited by every
                    # formulation of a given meaning. Never use the display
                    # category, historical cohort or term title in its place.
                    "subject": meaning.get("subject"),
                })
                for dep in deps:
                    if dep["id"] == group["id"]:
                        continue
                    # Nested mode has one group-level control per target.
                    # When a reviewed priority rule concerns a later source
                    # formulation, choose that link as its representative.
                    if dep["id"] not in seen_edges:
                        seen_edges[dep["id"]] = len(dependencies)
                        dependencies.append(dep)
                    elif dep.get("preferred_formulation") and not dependencies[
                            seen_edges[dep["id"]]].get("preferred_formulation"):
                        dependencies[seen_edges[dep["id"]]] = dep
        if not forms:
            raise ViewError("Empty term group")
        result.append({
            "id": group["id"],
            "term": group["title"],
            "aliases": group.get("aliases", []),
            "body": forms[0]["body"],
            "category": ((
                "Combined original mathDef + independent research"
                if any(m.get("source_origin") == "original_mathdef"
                       for m in group["meanings"])
                else "Independent research"
            ) + " · " + str(len(group["meanings"])) +
                (" context" if len(group["meanings"]) == 1 else " contexts")),
            "source": forms[0]["source"],
            "source_title": "",
            "status": "screened_draft",
            "path": "",
            "formulations": forms,
            "dependencies": dependencies,
            "related": sorted(r for r in related_by_group[group["id"]] if r != group["id"]),
        })
    return sorted(result, key=lambda x: (x["term"].casefold(), x["id"]))



def to_sources_index(catalog: dict, registry: dict) -> dict:
    """Validate a source registry for the *same* catalog being displayed.

    Source identity and primary citation assignments are supplied by the
    producing domain adapter; the portable renderer neither ranks research
    references nor interprets source verification states. All source evidence
    and internal source-file provenance remain distinct and traceable.
    """
    if (not isinstance(registry, dict) or registry.get("schema_version") != 1
            or not isinstance(registry.get("groups"), list)
            or not isinstance(registry.get("sources"), dict)):
        raise ViewError("Invalid source registry display contract")
    catalog_groups = {g["id"]: g for g in catalog["groups"]}
    form_owners = {}
    meaning_owners = {}
    for gid, group in catalog_groups.items():
        for meaning in group["meanings"]:
            meaning_owners[meaning["id"]] = gid
            for form in meaning["formulations"]:
                form_owners[form["id"]] = (gid, meaning["id"])
    source_ids = set(registry["sources"])
    for sid, source in registry["sources"].items():
        if (not isinstance(source, dict) or source.get("id") != sid
                or not isinstance(source.get("url"), str)
                or not source["url"].startswith("https://")
                or not isinstance(source.get("occurrences"), list)):
            raise ViewError("Invalid source registry citation identity: " + sid)
        for occurrence in source["occurrences"]:
            if not isinstance(occurrence, dict):
                raise ViewError("Malformed source occurrence: " + sid)
            gid, mid, fid = (occurrence.get(k) for k in
                              ("group_id", "meaning_id", "formulation_id"))
            if meaning_owners.get(mid) != gid:
                raise ViewError("Stale source occurrence meaning: " + sid)
            if fid is not None and form_owners.get(fid) != (gid, mid):
                raise ViewError("Stale source occurrence formulation: " + sid)
    seen_groups = set()
    for row in registry["groups"]:
        if not isinstance(row, dict):
            raise ViewError("Invalid source registry term entry")
        gid = row.get("group_id")
        if gid not in catalog_groups or gid in seen_groups:
            raise ViewError("Unknown or duplicate source registry term: " + str(gid))
        seen_groups.add(gid)
        actual = catalog_groups[gid]
        if row.get("term") != actual["title"]:
            raise ViewError("Stale source registry term label: " + gid)
        actual_meanings = {m["id"]: m for m in actual["meanings"]}
        meaning_rows = row.get("meanings", [])
        if {m.get("meaning_id") for m in meaning_rows} != set(actual_meanings):
            raise ViewError("Missing/stale meaning-level source registry: " + gid)
        for mr in meaning_rows:
            mid = mr["meaning_id"]
            actual_forms = {f["id"] for f in actual_meanings[mid]["formulations"]}
            primary_by_form = mr.get("primary_source_by_formulation", {})
            if not isinstance(primary_by_form, dict):
                raise ViewError("Malformed primary-source mapping: " + mid)
            if not set(primary_by_form).issubset(actual_forms):
                raise ViewError("Stale primary source formulation: " + mid)
            if not set(mr.get("source_ids", [])).issubset(source_ids):
                raise ViewError("Missing source identity in registry: " + mid)
            for sid in mr.get("source_ids", []):
                if not any(o.get("group_id") == gid and
                           o.get("meaning_id") == mid
                           for o in registry["sources"][sid]["occurrences"]):
                    raise ViewError("Source identity not cited by meaning: " + mid)
            for fid, sid in primary_by_form.items():
                if sid not in source_ids or not any(
                    occurrence.get("formulation_id") == fid and
                    occurrence.get("meaning_id") == mid and
                    not occurrence.get("provenance_only")
                    for occurrence in registry["sources"][sid]["occurrences"]
                ):
                    raise ViewError("Primary source lacks supporting occurrence: " + fid)
        if not set(row.get("source_ids", [])).issubset(source_ids):
            raise ViewError("Missing source identity for term: " + gid)
        for sid in row.get("source_ids", []):
            if not any(o.get("group_id") == gid
                       for o in registry["sources"][sid]["occurrences"]):
                raise ViewError("Source identity not cited by term: " + gid)
    if seen_groups != set(catalog_groups):
        raise ViewError("Source registry does not cover every displayed term")
    # Return the source registry as-is, preserving all cited evidence and
    # scope notes for the deliberately separate user-facing Sources dialog.
    return registry


def render(catalog_file: Path, branding_file: Path, destination: Path,
           stage: str, description: str, *, production: bool = False,
           expansion_overrides_file: Path | None = None,
           source_registry: dict | None = None) -> dict:
    """Build a standalone static UI without mutating independent research files."""
    catalog = read_json(catalog_file)
    brand = read_json(branding_file)
    if brand.get("schema_version") != 1:
        raise ViewError("Unsupported project branding configuration")
    fields = {
        "PROJECT_NAME": brand["project_name"],
        "LOGO": brand["logo"],
        "EYEBROW": brand["eyebrow"],
        "SUBTITLE": brand["subtitle"],
        "META_DESCRIPTION": brand.get("meta_description", ""),
        "REPOSITORY_URL": brand["repository_url"],
        "SUGGESTION_URL": brand.get("suggestion_url", brand["repository_url"] + "/issues"),
        "NOUN": brand.get("noun", "definition"),
        "NOUN_PLURAL": brand.get("noun_plural", "definitions"),
        "SEARCH_TERM_LABEL": brand.get("search_term_label", "terms"),
        "SEARCH_CONTENT_LABEL": brand.get("search_content_label", "definitions"),
        "STAGE_NAME": stage,
        "STAGE_DESCRIPTION": description,
    }
    index = to_index(catalog, expansion_overrides=(
        read_json(expansion_overrides_file) if expansion_overrides_file is not None else None
    ))
    frontend = Path(__file__).resolve().parent
    template = (frontend / "template.html").read_text(encoding="utf-8")
    if production:
        # The completed merged collection is the main product, not a
        # reconstruction preview. Research statuses are still visible on
        # individual formulations; source distinctions are never hidden.
        banner = (
            '<aside class="research-stage-notice">'
            '<strong>Expanded mathematical definitions.</strong> '
            'Browse the complete original mathDef collection together with '
            'independent research additions and alternate meanings. '
            'Research additions are source-attributed drafts, not formally '
            'peer-reviewed mathematical facts. '
            '<a href="./reconstruction/">Research history</a></aside>'
        )
        footer = (
            '<footer>mathDef · Mathematical definitions and variations · '
            '<a href="./reconstruction/">Research history</a></footer>'
        )
    else:
        banner = (
            '<aside class="research-stage-notice"><strong>' +
            html.escape(stage) + '</strong> — ' +
            html.escape(description) +
            ' <a href="../">All reconstruction stages ↗</a></aside>'
        )
        footer = (
            '<footer>' + html.escape(brand["project_name"]) + ' · ' +
            html.escape(stage) + ' · Independent research preview. '
            '<a href="../">Other stages ↗</a></footer>'
        )
    template = template.replace("{{STAGE_BANNER}}", banner)
    template = template.replace("{{SITE_FOOTER}}", footer)
    for key, value in fields.items():
        template = template.replace("{{" + key + "}}", html.escape(str(value), quote=True))
    config = dict(brand)
    config["stage"] = stage
    config["stage_description"] = description
    if source_registry is not None:
        config["sources_file"] = "sources-index.json"
    if production:
        # The root site has its own long-lived visitor setting, separate from
        # experiment previews. New visitors get the shared UI's In-Line mode.
        config["storage_key"] = "mathdef-explore-mode"
    serialized = json.dumps(config, ensure_ascii=False).replace("<", "\\u003c").replace(
        ">", "\\u003e").replace("&", "\\u0026")
    template = template.replace("{{UI_CONFIG_JSON}}", serialized)
    if "{{" in template or "}}" in template:
        raise ViewError("Unresolved reusable UI branding token")
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    for filename in ("app.js", "subject_priority.js", "sources_ui.js", "feedback.js", "styles.css"):
        shutil.copyfile(frontend / filename, destination / filename)
    (destination / "definitions-index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if source_registry is not None:
        validated = to_sources_index(catalog, source_registry)
        (destination / "sources-index.json").write_text(
            json.dumps(validated, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
    (destination / "index.html").write_text(template, encoding="utf-8")
    return {"terms": len(index), "formulations": sum(len(x["formulations"]) for x in index),
            "relations": len(catalog["relations"]), "stage": stage,
            "sources_available": source_registry is not None,
            "source_identities": len(source_registry["sources"]) if source_registry else 0}
