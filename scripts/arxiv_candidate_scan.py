#!/usr/bin/env python3
"""Discover explicit LaTeX definition environments in arXiv paper sources.

Writes locator-only CSV, NOT extracted definition text.
Requires Python 3.10+; network queries use dedicated export.arxiv.org.
"""
import argparse
import csv
import gzip
import hashlib
import io
import re
import sys
import tarfile
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ID_RE = re.compile(r"^\d{4}\.\d{4,5}(?:v\d+)?$")
DEF_DECL = re.compile(
    r"\\newtheorem\*?\s*\{\s*([A-Za-z0-9_-]+)\s*\}"
    r"(?:\[[^\]]+\])?\s*\{\s*Definitions?\s*\}", re.I)
BEGIN = re.compile(
    r"\\begin\s*\{\s*([A-Za-z0-9_-]+)\s*\}"
    r"(?:\s*\[([^\]]{0,160})\])?")
MAX_DOWNLOAD = 25_000_000
MAX_UNPACKED = 55_000_000
MAX_TEX = 5_000_000
FIELDS = ("arxiv_id", "paper_title", "source_file", "line",
          "environment", "heading", "body_sha256", "body_characters", "paper_url")
USER_AGENT = "mathDef-candidate-scanner/0.1 (https://github.com/Zengez/mathDef)"


def scan_tex(text, filename, arxiv_id, title=""):
    """Yield candidate locators only; never preserve the definition prose."""
    envs = {"definition", "definitions", "defn", "def"}
    envs.update(m.group(1).lower() for m in DEF_DECL.finditer(text))
    records = []
    for match in BEGIN.finditer(text):
        env = match.group(1)
        if env.lower() not in envs:
            continue
        end = re.search(
            r"\\end\s*\{\s*" + re.escape(env) + r"\s*\}",
            text[match.end():])
        if not end:
            continue
        definition = text[match.end():match.end() + end.start()].strip()
        if not definition:
            continue
        records.append({
            "arxiv_id": arxiv_id, "paper_title": title,
            "source_file": filename,
            "line": text.count("\n", 0, match.start()) + 1,
            "environment": env,
            "heading": (match.group(2) or "").strip()[:100],
            "body_sha256": hashlib.sha256(definition.encode("utf-8")).hexdigest(),
            "body_characters": len(definition),
            "paper_url": "https://arxiv.org/abs/" + arxiv_id.split("v")[0],
        })
    return records


def source_files(raw):
    """Read .tex files in memory; no extraction of untrusted archive paths."""
    try:
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:*") as archive:
            total = 0
            for member in archive:
                if not member.isfile() or not member.name.lower().endswith((".tex", ".ltx")):
                    continue
                if member.size > MAX_TEX:
                    continue
                total += member.size
                if total > MAX_UNPACKED:
                    raise ValueError("expanded LaTeX exceeds safety limit")
                fh = archive.extractfile(member)
                if fh is not None:
                    data = fh.read(MAX_TEX + 1)
                    if len(data) <= MAX_TEX:
                        yield member.name, data.decode("utf-8", errors="replace")
        return
    except tarfile.ReadError:
        pass
    if raw[:2] == b"\x1f\x8b":
        with gzip.GzipFile(fileobj=io.BytesIO(raw)) as fh:
            data = fh.read(MAX_TEX + 1)
    else:
        data = raw
    if len(data) > MAX_TEX:
        raise ValueError("single LaTeX source exceeds safety limit")
    yield "main.tex", data.decode("utf-8", errors="replace")


class PoliteReader:
    def __init__(self, delay=3.5):
        self.delay = max(delay, 3.2)
        self.last = None

    def get(self, url):
        if self.last is not None:
            time.sleep(max(0, self.delay - (time.monotonic() - self.last)))
        self.last = time.monotonic()
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=55) as response:
            payload = response.read(MAX_DOWNLOAD + 1)
        if len(payload) > MAX_DOWNLOAD:
            raise ValueError("source exceeds download safety limit")
        return payload


def list_category(reader, category, maximum):
    if not re.fullmatch(r"math\.[A-Z]{2}", category):
        raise ValueError("category format must be math.DS or math.AG, etc.")
    query = urllib.parse.urlencode({
        "search_query": "cat:" + category,
        "start": 0, "max_results": maximum,
        "sortBy": "submittedDate", "sortOrder": "descending",
    })
    data = ET.fromstring(reader.get("https://export.arxiv.org/api/query?" + query))
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []
    for node in data.findall("atom:entry", ns):
        uri = node.findtext("atom:id", default="", namespaces=ns)
        paper_id = uri.rstrip("/").split("/")[-1]
        if ID_RE.fullmatch(paper_id):
            title = " ".join(node.findtext("atom:title", default="", namespaces=ns).split())
            papers.append((paper_id, title))
    return papers


def harvest(reader, paper_id, title=""):
    if not ID_RE.fullmatch(paper_id):
        raise ValueError("invalid arXiv ID: " + paper_id)
    raw = reader.get("https://export.arxiv.org/src/" + paper_id)
    records = []
    for filename, content in source_files(raw):
        records.extend(scan_tex(content, filename, paper_id, title))
    return records


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", action="append", default=[], help="repeatable arXiv ID")
    parser.add_argument("--category", help="math.DS, math.AG, etc.")
    parser.add_argument("--max-papers", type=int, default=12)
    parser.add_argument("--delay", type=float, default=3.5)
    parser.add_argument("--source", type=Path, help="local source .tar.gz or .tex")
    parser.add_argument("--out", type=Path, default=Path("_arxiv_candidates.csv"))
    args = parser.parse_args(argv)
    if not 1 <= args.max_papers <= 100:
        parser.error("--max-papers must be 1 to 100")
    if args.source and (args.category or len(args.id) != 1):
        parser.error("--source requires one --id and no --category")
    if not args.id and not args.category:
        parser.error("provide --id or --category")
    reader = PoliteReader(args.delay)
    papers = []
    if args.category:
        papers.extend(list_category(reader, args.category, args.max_papers))
    papers.extend((paper_id, "") for paper_id in args.id)
    seen = set()
    unique = []
    for paper_id, title in papers:
        if paper_id not in seen:
            seen.add(paper_id)
            unique.append((paper_id, title))
    results = []
    for paper_id, title in unique[:args.max_papers]:
        try:
            if args.source:
                candidates = []
                for filename, content in source_files(args.source.read_bytes()):
                    candidates.extend(scan_tex(content, filename, paper_id, title))
            else:
                candidates = harvest(reader, paper_id, title)
            results.extend(candidates)
            print(f"{paper_id}: {len(candidates)} candidates", file=sys.stderr)
        except Exception as exc:
            print(f"{paper_id}: skipped ({exc})", file=sys.stderr)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(results)
    print(f"Wrote {len(results)} locator-only candidates to {args.out}")


if __name__ == "__main__":
    main()
