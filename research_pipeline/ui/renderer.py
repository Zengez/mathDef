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


def to_index(catalog: dict) -> list[dict]:
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
    dep_by_form = defaultdict(list)
    related_by_group = defaultdict(set)
    for rel in relations:
        source = form_owner.get(rel.get("from_formulation"))
        target = meaning_to_group.get(rel.get("target_meaning"))
        if source is None or target is None:
            raise ViewError("Broken displayed relation endpoint")
        if rel.get("review_state", "screened") != "screened":
            raise ViewError("Cannot render unscreened relationship")
        if rel.get("relation_type") == "definition_uses":
            dep_by_form[rel["from_formulation"]].append({
                "id": target, "label": group_by_id[target]["title"],
                "formulation": rel["from_formulation"],
                "target_meaning": rel["target_meaning"],
                "start": -1, "end": -1
            })
        else:
            related_by_group[source].add(target)
    result = []
    for group in groups:
        forms = []
        dependencies = []
        seen_edges = set()
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
                })
                for dep in deps:
                    if dep["id"] != group["id"] and dep["id"] not in seen_edges:
                        dependencies.append(dep)
                        seen_edges.add(dep["id"])
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


def render(catalog_file: Path, branding_file: Path, destination: Path,
           stage: str, description: str) -> dict:
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
    index = to_index(catalog)
    frontend = Path(__file__).resolve().parent
    template = (frontend / "template.html").read_text(encoding="utf-8")
    for key, value in fields.items():
        template = template.replace("{{" + key + "}}", html.escape(str(value), quote=True))
    config = dict(brand)
    config["stage"] = stage
    config["stage_description"] = description
    serialized = json.dumps(config, ensure_ascii=False).replace("<", "\\u003c").replace(
        ">", "\\u003e").replace("&", "\\u0026")
    template = template.replace("{{UI_CONFIG_JSON}}", serialized)
    if "{{" in template or "}}" in template:
        raise ViewError("Unresolved reusable UI branding token")
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    for filename in ("app.js", "feedback.js", "styles.css"):
        shutil.copyfile(frontend / filename, destination / filename)
    (destination / "definitions-index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (destination / "index.html").write_text(template, encoding="utf-8")
    return {"terms": len(index), "formulations": sum(len(x["formulations"]) for x in index),
            "relations": len(catalog["relations"]), "stage": stage}
