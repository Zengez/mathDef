#!/usr/bin/env python3
"""Validate definitions/*.tex and generate a self-contained static site."""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFS = ROOT / "definitions"
OUT = ROOT / "_site"
FIELD = re.compile(r"^%\s*(id|term|aliases|related):\s*(.*?)\s*$")
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
    return dict(
        id=meta["id"], term=meta["term"], body=body,
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
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "web", OUT)
    entries.sort(key=lambda d: (d["term"].casefold(), d["id"]))
    (OUT / "definitions-index.json").write_text(json.dumps(entries,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUT / ".nojekyll").touch()
    print(f"Built {len(entries)} definitions in {OUT}")

if __name__ == "__main__":
    main()
