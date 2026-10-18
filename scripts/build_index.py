#!/usr/bin/env python3
"""Validate definitions/*.tex and generate a self-contained static site."""
import json
import re
import shutil
from pathlib import Path

if __package__:
    from scripts.dependency_links import load_overrides, populate_dependencies
else:
    from dependency_links import load_overrides, populate_dependencies

ROOT = Path(__file__).resolve().parent.parent
DEFS = ROOT / "definitions"
VARIANTS = ROOT / "variants"
OUT = ROOT / "_site"
FIELD = re.compile(r"^%\s*(id|term|aliases|related|source|status|arxiv|locator|source_title|form_label|form_order):\s*(.*?)\s*$")
ID = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")
VARIANT_FIELD = re.compile(r"^%\s*(parent|key|label|order|source|status):\s*(.*?)\s*$")

def parse(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    meta, start = {}, 0
    for i, line in enumerate(lines):
        match = FIELD.fullmatch(line)
        if match:
            key, value = match.groups()
            if key in meta:
                raise ValueError(f"{path}: duplicate {key}")
            meta[key] = value
            start = i + 1
        elif not line.strip() or line.strip().startswith("%"):
            start = i + 1
        else:
            break
    if not meta.get("id") or not meta.get("term") or not ID.fullmatch(meta.get("id", "")):
        raise ValueError(f"{path}: missing/invalid id or term")
    body = "\n".join(lines[start:]).strip()
    if not body:
        raise ValueError(f"{path}: definition body is empty")
    source = meta.get("source", "")
    status = meta.get("status", "example")
    if source and (not source.startswith("https://") or any(ch.isspace() for ch in source)):
        raise ValueError(f"{path}: source must be an HTTPS reference URL")
    if status not in {"draft", "reviewed", "example"}:
        raise ValueError(f"{path}: invalid status {status}")
    arxiv = meta.get("arxiv", "")
    locator = meta.get("locator", "")
    if arxiv and not re.fullmatch(r"\d{4}\.\d{4,5}(?:v\d+)?", arxiv):
        raise ValueError(f"{path}: invalid arXiv identifier")
    if arxiv and source != f"https://arxiv.org/abs/{arxiv.split('v')[0]}":
        raise ValueError(f"{path}: arXiv source must match the canonical abstract URL")
    if arxiv and not locator:
        raise ValueError(f"{path}: arXiv entries require a definition locator")
    return dict(
        id=meta["id"], term=meta["term"], body=body,
        source=source, status=status, arxiv=arxiv,
        locator=locator, source_title=meta.get("source_title", ""),
        form_label=meta.get("form_label", "Original formulation"),
        form_order=int(meta.get("form_order", "0")),
        aliases=[v.strip() for v in meta.get("aliases", "").split("|") if v.strip()],
        related=[v.strip() for v in meta.get("related", "").split(",") if v.strip()],
        category=path.parent.relative_to(DEFS).as_posix().replace("/", " / ").title(),
        path=path.relative_to(ROOT).as_posix()
    )

def parse_variant(path):
    """An alternative formulation of an existing definition, not a new concept."""
    lines = path.read_text(encoding="utf-8").splitlines()
    meta, start = {}, 0
    for i, line in enumerate(lines):
        match = VARIANT_FIELD.fullmatch(line)
        if match:
            key, value = match.groups()
            if key in meta:
                raise ValueError(f"{path}: duplicate {key}")
            meta[key] = value
            start = i + 1
        elif not line.strip() or line.strip().startswith("%"):
            start = i + 1
        else:
            break
    if not ID.fullmatch(meta.get("parent", "")):
        raise ValueError(f"{path}: invalid or missing parent definition ID")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta.get("key", "")):
        raise ValueError(f"{path}: invalid/missing formulation key")
    label = meta.get("label", "").strip()
    if not label:
        raise ValueError(f"{path}: missing formulation label")
    body = "\n".join(lines[start:]).strip()
    if not body:
        raise ValueError(f"{path}: empty alternative formulation")
    source = meta.get("source", "")
    if not source.startswith("https://") or any(c.isspace() for c in source):
        raise ValueError(f"{path}: alternative formulation requires an HTTPS source")
    status = meta.get("status", "draft")
    if status not in {"draft", "reviewed", "example"}:
        raise ValueError(f"{path}: invalid formulation status")
    try:
        order = int(meta.get("order", "100"))
    except ValueError as exc:
        raise ValueError(f"{path}: formulation order must be an integer") from exc
    return dict(parent=meta["parent"], key=meta["key"], label=label,
                order=order, body=body, source=source, status=status,
                path=path.relative_to(ROOT).as_posix())


def attach_formulations(entries):
    by_id = {d["id"]: d for d in entries}
    for path in sorted(VARIANTS.rglob("*.tex")):
        variant = parse_variant(path)
        parent = by_id.get(variant.pop("parent"))
        if parent is None:
            raise ValueError(f"{path}: formulation parent does not exist")
        if "formulations" not in parent:
            parent["formulations"] = [{
                "key": "primary", "label": parent["form_label"],
                "order": parent["form_order"], "body": parent["body"],
                "source": parent["source"], "status": parent["status"],
                "path": parent["path"],
            }]
        if any(f["key"] == variant["key"] for f in parent["formulations"]):
            raise ValueError(f"{path}: duplicate formulation key for {parent['id']}")
        parent["formulations"].append(variant)
    for d in entries:
        if "formulations" in d:
            d["formulations"].sort(key=lambda x: (x["order"], x["key"]))


def main():
    entries = [parse(path) for path in sorted(DEFS.rglob("*.tex"))]
    if not entries:
        raise ValueError("No LaTeX definition files found")
    attach_formulations(entries)
    ids = set()
    for entry in entries:
        if entry["id"] in ids:
            raise ValueError(f"Duplicate id: {entry['id']}")
        ids.add(entry["id"])
    for entry in entries:
        for linked in entry["related"]:
            if linked not in ids:
                raise ValueError(f"{entry['id']}: unknown related ID {linked}")
    overrides = load_overrides(ROOT / "data" / "link_overrides.json")
    dependencies, link_report = populate_dependencies(entries, overrides)
    for entry in entries:
        entry["dependencies"] = dependencies[entry["id"]]
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "web", OUT)
    entries.sort(key=lambda d: (d["term"].casefold(), d["id"]))
    (OUT / "definitions-index.json").write_text(json.dumps(entries,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUT / "dependency-review.json").write_text(
        json.dumps(link_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / ".nojekyll").touch()
    print(f"Built {len(entries)} definitions and {link_report['links']} proposed links "
          f"across {link_report['definitions_with_links']} entries; "
          f"{link_report['unresolved_ambiguous_occurrences']} ambiguous occurrences omitted.")

if __name__ == "__main__":
    main()
