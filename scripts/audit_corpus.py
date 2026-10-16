#!/usr/bin/env python3
"""Editorial metadata audit, not a proof checker for mathematical definitions."""
import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

from scripts.build_index import parse
from scripts.wikipedia_candidate_scan import normalize

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ("id", "term", "path", "issue", "detail", "source")
BROAD_REFERENCE_PAGES = {
    "Functional_analysis", "Numerical_analysis", "Complex_analysis",
    "Algebraic_geometry", "Category_theory", "General_topology",
    "Number_theory", "Probability_theory", "Differential_geometry",
    "Set_theory", "Measure_theory", "Topology", "Mathematics"
}



def audit_entry(entry, duplicates):
    issues = []
    url = entry["source"]
    if not url:
        issues.append(("no-source", "No mathematical citation or discovery reference"))
    elif "en.wikipedia.org/wiki/List_of_" in url or "/Category:" in url:
        issues.append(("subject-list-only", "Source links to a subject index, not the definition"))
    source_path = urlparse(url).path if url else ""
    if url and (urlparse(url).netloc == "encyclopediaofmath.org"
                and source_path.rsplit("/", 1)[-1] in BROAD_REFERENCE_PAGES):
        issues.append(("general-encyclopedia-overview", "Subject overview should be checked against a direct concept reference"))
    if entry["body"].count(r"\[") != entry["body"].count(r"\]"):
        issues.append(("unbalanced-display-math", "Mismatched LaTeX display delimiters"))
    if len(entry["body"].strip()) < 90:
        issues.append(("very-short", "Definition body shorter than 90 characters"))
    # KaTeX supports \begin{...} inside math delimiters. Flag only TeX
    # environments appearing in the prose surrounding math expressions.
    text_outside_math = re.sub(
        r"\$\$.*?\$\$|\$[^$]*\$|\\\\\[.*?\\\\\]|\\\\\(.*?\\\\\)",
        "", entry["body"], flags=re.S)
    if r"\begin{" in text_outside_math:
        issues.append(("latex-environment", "TeX environment in prose outside math delimiters"))
    if entry["body"].count("$") % 2:
        issues.append(("unbalanced-dollar", "Odd number of dollar math delimiters; check source"))
    if len(duplicates[normalize(entry["term"])]) > 1:
        issues.append(("duplicate-term", "Multiple independent IDs use the same displayed name"))
    if entry["status"] != "reviewed":
        issues.append(("not-reviewed", "Review status is draft or example"))
    return issues


def audit(definitions):
    entries = [parse(p) for p in sorted(definitions.rglob("*.tex"))]
    duplicates = defaultdict(list)
    for entry in entries:
        duplicates[normalize(entry["term"])].append(entry["id"])
    issues = []
    for entry in entries:
        for kind, description in audit_entry(entry, duplicates):
            issues.append({
                "id": entry["id"], "term": entry["term"], "path": entry["path"],
                "issue": kind, "detail": description, "source": entry["source"],
            })
    return entries, issues, {k: sorted(ids) for k, ids in duplicates.items() if len(ids) > 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--definitions", type=Path, default=ROOT / "definitions")
    parser.add_argument("--out", type=Path, default=Path("_definition_audit.csv"))
    args = parser.parse_args()
    entries, issues, dup = audit(args.definitions)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(issues)
    counts = Counter(x["issue"] for x in issues)
    hosts = Counter(urlparse(e["source"]).netloc for e in entries if e["source"])
    source_urls = Counter(e["source"] for e in entries if e["source"])
    reused_source_urls = [
        {"source": url, "count": count}
        for url, count in sorted(source_urls.items(), key=lambda item: (-item[1], item[0]))
        if count > 1
    ][:30]
    summary = {
        "total": len(entries),
        "status": dict(Counter(e["status"] for e in entries)),
        "metadata_issues": dict(counts),
        "source_hosts": dict(hosts),
        "reused_source_urls_top": reused_source_urls,
        "duplicate_terms": dup,
        "audit_report": str(args.out),
        "note": "These are editorial flags, not validated mathematical errors.",
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
