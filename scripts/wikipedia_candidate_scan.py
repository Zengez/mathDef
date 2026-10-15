#!/usr/bin/env python3
"""Inventory Wikipedia math-category articles missing from mathDef.

Only article titles, categories, IDs and URLs are saved. No Wikipedia article
prose is copied or automatically promoted to mathematical definitions.
"""
import argparse
import csv
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://en.wikipedia.org/w/api.php"
UA = "mathDef-definition-coverage-audit/0.1 (https://github.com/Zengez/mathDef)"
DEFAULTS = [
    "Category:Complex analysis",
    "Category:Several complex variables",
    "Category:Functional analysis",
    "Category:Operator theory",
    "Category:General topology",
    "Category:Dynamical systems",
    "Category:Algebraic geometry",
    "Category:Probability theory",
]
FIELDS = ("title", "wikipedia_url", "found_in_category", "category_depth",
          "coverage", "mathdef_ids", "possible_ids", "review_priority")
MAX_BYTES = 5_000_000


def normalize(name):
    text = unicodedata.normalize("NFKC", name)
    text = re.sub(r"\s*\([^)]*\)", "", text)
    text = re.sub(r"[^a-z0-9]+", " ", text.casefold())
    return " ".join(text.split())


def load_terms(definitions):
    """Match against real metadata, not just filenames."""
    terms = {}
    for path in sorted(definitions.rglob("*.tex")):
        data = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            if not line.startswith("%"):
                break
            m = re.fullmatch(r"%\s*(id|term|aliases):\s*(.*)", line.strip())
            if m:
                data[m.group(1)] = m.group(2).strip()
        did = data.get("id")
        if not did:
            continue
        names = [data.get("term", "")] + data.get("aliases", "").split("|")
        for name in names:
            key = normalize(name.strip())
            if key:
                terms.setdefault(key, set()).add(did)
    return terms


def classify(title, exact, terms):
    key = normalize(title)
    matches = sorted(terms.get(key, ()))
    maybe = []
    if not matches:
        target = set(key.split())
        if len(target) > 1:
            for name, ids in terms.items():
                words = set(name.split())
                if len(words) > 1 and (words <= target or target <= words):
                    maybe.extend(ids)
                    if len(maybe) >= 8:
                        break
    maybe = sorted(set(maybe))[:8]
    if matches:
        coverage = "present_exact_title_or_alias"
        priority = "already-covered"
    elif re.search(r"^(?:list|glossary|outline|index|timeline)\b|"
                   r"\b(?:biography|bibliography|conjecture|theorem|"
                   r"prize|award)\b", title, flags=re.I):
        coverage = "not_matched"
        priority = "review_low"
    else:
        coverage = "possible_name_variant" if maybe else "not_matched"
        priority = "review_medium" if maybe else "review_high"
    return coverage, "|".join(matches), "|".join(maybe), priority


class WikipediaReader:
    def __init__(self, delay=1.1):
        self.delay = max(1.0, delay)
        self.last = None

    def request(self, category, continuation=None):
        query = {
            "action": "query", "list": "categorymembers",
            "cmtitle": category, "cmtype": "page|subcat",
            "cmlimit": "100", "format": "json",
            "formatversion": "2",
        }
        if continuation:
            query["cmcontinue"] = continuation
        url = API + "?" + urllib.parse.urlencode(query)
        for attempt in range(4):
            if self.last is not None:
                time.sleep(max(0, self.delay - (time.monotonic() - self.last)))
            self.last = time.monotonic()
            req = urllib.request.Request(url, headers={
                "User-Agent": UA, "Accept": "application/json",
            })
            try:
                with urllib.request.urlopen(req, timeout=45) as response:
                    payload = response.read(MAX_BYTES + 1)
                if len(payload) > MAX_BYTES:
                    raise ValueError("Wikipedia API response too large")
                return json.loads(payload)
            except urllib.error.HTTPError as error:
                if error.code not in {429, 500, 502, 503, 504} or attempt == 3:
                    raise
                time.sleep(2 ** (attempt + 1))
        raise RuntimeError("Wikipedia API did not respond")


def inventory(reader, seeds, depth, max_categories, max_pages, terms):
    queue = deque((category, 0) for category in seeds)
    seen_cat, found = set(), {}
    while queue and len(seen_cat) < max_categories and len(found) < max_pages:
        category, level = queue.popleft()
        if category in seen_cat:
            continue
        seen_cat.add(category)
        print("Category:", category, "depth:", level, file=sys.stderr)
        continuation = None
        while True:
            response = reader.request(category, continuation)
            if "error" in response:
                raise RuntimeError(str(response["error"]))
            members = response.get("query", {}).get("categorymembers", [])
            for page in members:
                if page.get("ns") == 14 and level < depth:
                    queue.append((page["title"], level + 1))
                elif page.get("ns") == 0:
                    title = page["title"]
                    if title not in found:
                        url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(
                            title.replace(" ", "_"), safe="()")
                        status, ids, possible, priority = classify(title, False, terms)
                        found[title] = {
                            "title": title, "wikipedia_url": url,
                            "found_in_category": category,
                            "category_depth": level,
                            "coverage": status,
                            "mathdef_ids": ids,
                            "possible_ids": possible,
                            "review_priority": priority,
                        }
                if len(found) >= max_pages:
                    break
            if len(found) >= max_pages:
                break
            continuation = response.get("continue", {}).get("cmcontinue")
            if not continuation:
                break
    if not seen_cat:
        raise RuntimeError("No Wikipedia categories inspected")
    return sorted(found.values(), key=lambda x: (
        {"review_high": 0, "review_medium": 1,
         "already-covered": 2, "review_low": 3}.get(x["review_priority"], 4),
        x["title"].casefold()
    )), len(seen_cat)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", action="append", help="repeatable Wikipedia Category: name")
    parser.add_argument("--depth", type=int, default=1, help="subcategory levels (0-2)")
    parser.add_argument("--max-categories", type=int, default=12)
    parser.add_argument("--max-pages", type=int, default=1500)
    parser.add_argument("--delay", type=float, default=1.1)
    parser.add_argument("--definitions", type=Path, default=ROOT / "definitions")
    parser.add_argument("--out", type=Path, default=Path("_wikipedia_candidates.csv"))
    args = parser.parse_args()
    if not 0 <= args.depth <= 2:
        parser.error("--depth must be 0..2")
    if not 1 <= args.max_categories <= 100:
        parser.error("--max-categories must be 1..100")
    if not 1 <= args.max_pages <= 10000:
        parser.error("--max-pages must be 1..10000")
    seeds = args.seed or DEFAULTS
    seeds = [c if c.startswith("Category:") else "Category:" + c for c in seeds]
    terms = load_terms(args.definitions)
    print(f"Loaded {sum(map(len, terms.values()))} term/alias IDs from mathDef", file=sys.stderr)
    records, categories = inventory(
        WikipediaReader(args.delay), seeds, args.depth, args.max_categories,
        args.max_pages, terms)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)
    statuses = {}
    for r in records:
        statuses[r["review_priority"]] = statuses.get(r["review_priority"], 0) + 1
    print(json.dumps({"categories": categories, "articles": len(records),
                      "review_priority_counts": statuses, "output": str(args.out)},
                     indent=2))


if __name__ == "__main__":
    main()
