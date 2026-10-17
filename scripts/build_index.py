#!/usr/bin/env python3
"""Validate definitions/*.tex and generate a self-contained static site."""
import json
import re
import shutil
from pathlib import Path

from scripts.dependency_links import load_overrides, populate_dependencies

ROOT = Path(__file__).resolve().parent.parent
DEFS = ROOT / "definitions"
OUT = ROOT / "_site"
FIELD = re.compile(r"^%\s*(id|term|aliases|related|source|status|arxiv|locator|source_title):\s*(.*?)\s*$")
ID = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")

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
        aliases=[v.strip() for v in meta.get("aliases", "").split("|") if v.strip()],
        related=[v.strip() for v in meta.get("related", "").split(",") if v.strip()],
        category=path.parent.relative_to(DEFS).as_posix().replace("/", " / ").title(),
        path=path.relative_to(ROOT).as_posix()
    )

def main():
    entries = [parse(path) for path in sorted(DEFS.rglob("*.tex"))]
    if not entries:
        raise ValueError("No LaTeX definition files found")
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
