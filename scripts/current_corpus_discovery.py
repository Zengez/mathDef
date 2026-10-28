#!/usr/bin/env python3
"""High-recall terminology discovery from the CURRENT published merged corpus.

Read the same catalog and SHA-verified v2 snapshot used by the production
site. Never read a frozen old snapshot as the live corpus, and never add
definitions automatically. False positives are expected and welcome in Pass 1.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from scripts.validate_published_corpus import validate_site

# Seed heads broaden recall beyond the terms already in the corpus; heads from
# ALL current headings/aliases are also learned dynamically on each run.
SEED_HEADS = frozenset("""
algebra algebraic algebraic-set basis category chain closure cohomology
compactification completion complex connection convergence correspondence
cover covering cycle decomposition derivative differential dimension
distribution embedding endomorphism equivalence extension field filtration
flow form function functor graph group homology homomorphism homeomorphism
ideal identity interior interval isomorphism kernel lattice limit manifold
map mapping matrix measure metric model module monoid morphism norm object
operator order point polynomial product projection property quotient radical
relation representation resolution ring scheme sequence series set sheaf
space spectrum structure subgroup submodule subset subspace sum surface
tensor topology transformation variety vector
""".split())

# Deliberately broad adjective/qualifier extraction; not a validator.
WORD = re.compile(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", re.UNICODE)
MATH = re.compile(r"\$\$.*?\$\$|\$[^$]*\$|\\\(.*?\\\)|\\\[.*?\\\]", re.S)
COMMAND = re.compile(r"\\[A-Za-z]+(?:\[[^]]*\])?", re.UNICODE)
STOP_LAST = frozenset("the a an of and or to in for with by from is are that which if then such where".split())
MAX_WORDS = 5
EXAMPLE_LIMIT = 3


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(WORD.findall(value.replace("_", " ")))


def variants(value: str) -> set[str]:
    """Lexical hints only; mathematical equivalence is never inferred."""
    name = normalize(value)
    result = {name}
    parts = name.split()
    if parts:
        word = parts[-1]
        for end, replacement in (("ies", "y"), ("es", ""), ("s", "")):
            if word.endswith(end) and len(word) > len(end) + 2:
                result.add(" ".join(parts[:-1] + [word[:-len(end)] + replacement]))
    return result


def plain_words(value: str) -> list[str]:
    # Math is not English prose; suppress symbols/commands to reduce nonsense.
    text = MATH.sub(" ", value)
    text = COMMAND.sub(" ", text)
    return [w.casefold() for w in WORD.findall(unicodedata.normalize("NFKC", text))]


def extract_phrases(words: list[str], heads: set[str]):
    """Return broad n-grams ending in an existing or seeded mathematics head."""
    for end, token in enumerate(words):
        head = token
        if head not in heads and not any(v in heads for v in variants(head)):
            continue
        for n in range(2, min(MAX_WORDS, end + 1) + 1):
            piece = words[end - n + 1:end + 1]
            if piece[0] in STOP_LAST or any(len(w) == 1 for w in piece):
                continue
            phrase = " ".join(piece)
            if len(phrase) >= 8:
                yield phrase


def discover(catalog: dict, snapshot: dict, *, decisions: dict | None = None) -> dict:
    definitions = snapshot["definitions"]
    groups = {g["id"]: g for g in catalog["groups"]}
    if set(groups) != {d["id"] for d in definitions}:
        raise ValueError("Discovery must use the same complete merged catalog as v2")
    indexed = defaultdict(set)
    heads = set(SEED_HEADS)
    for d in definitions:
        for title in [d["term"], *d.get("aliases", [])]:
            norm = normalize(title)
            if not norm:
                continue
            indexed[norm].add(d["id"])
            heads.add(norm.split()[-1])
    # Existing full-heading spelling variants are hints, not formal synonyms.
    variant_index = defaultdict(set)
    for normalized, group_ids in indexed.items():
        for form in variants(normalized):
            variant_index[form].update(group_ids)
    previous = decisions or {}
    candidate_map = {}
    counters = Counter()
    for d in sorted(definitions, key=lambda d: d["id"]):
        group = groups[d["id"]]
        for meaning in sorted(group["meanings"], key=lambda m: m["id"]):
            for f in sorted(meaning["formulations"], key=lambda f: f["id"]):
                counters["formulations_scanned"] += 1
                words = plain_words(f["text"])
                counters["prose_words"] += len(words)
                # A repeated phrase can appear more than once in one formulation.
                for phrase in extract_phrases(words, heads):
                    counters["phrase_occurrences"] += 1
                    norm = normalize(phrase)
                    exact = indexed.get(norm)
                    possible = variant_index.get(norm)
                    if exact:
                        status = "already_defined"
                        matched = exact
                    elif possible:
                        status = "possible_variant"
                        matched = possible
                    elif norm in previous:
                        status = "previously_reviewed"
                        matched = set()
                    else:
                        status = "unreviewed_candidate"
                        matched = set()
                    key = (norm, status)
                    if key not in candidate_map:
                        candidate_map[key] = {
                            "id": "term." + hashlib.sha256(norm.encode("utf-8")).hexdigest()[:20],
                            "phrase": phrase,
                            "normalized": norm,
                            "classification": status,
                            "matched_group_ids": sorted(matched),
                            "occurrences": 0,
                            "formulation_count": 0,
                            "_formulations": set(),
                            "examples": [],
                        }
                        if status == "previously_reviewed":
                            candidate_map[key]["prior_decision"] = previous[norm]
                    entry = candidate_map[key]
                    entry["occurrences"] += 1
                    if f["id"] not in entry["_formulations"]:
                        entry["_formulations"].add(f["id"])
                        entry["formulation_count"] += 1
                    # Keep a bounded, deterministic sample. Never embed entire sources.
                    if len(entry["examples"]) < EXAMPLE_LIMIT:
                        source = {
                            "group_id": d["id"], "group_title": d["term"],
                            "meaning_id": meaning["id"],
                            "formulation_id": f["id"],
                        }
                        if source not in entry["examples"]:
                            entry["examples"].append(source)
    for item in candidate_map.values():
        del item["_formulations"]
    entries = sorted(candidate_map.values(), key=lambda x: (
        {"unreviewed_candidate": 0, "possible_variant": 1,
         "previously_reviewed": 2, "already_defined": 3}[x["classification"]],
        -x["formulation_count"], -x["occurrences"], x["phrase"]))
    status_counts = Counter(e["classification"] for e in entries)
    status_occurrences = Counter()
    for item in entries:
        status_occurrences[item["classification"]] += item["occurrences"]
    return {
        "schema": "mathdef.current-corpus-discovery.v1",
        "status": "unverified_high_recall_candidates",
        "scope": {
            "term_groups": len(groups),
            "meanings": sum(len(g["meanings"]) for g in groups.values()),
            "formulations": counters["formulations_scanned"],
            "prose_words": counters["prose_words"],
        },
        "counts": {
            "phrase_occurrences": counters["phrase_occurrences"],
            "distinct_phrases": len(entries),
            "distinct_by_classification": dict(sorted(status_counts.items())),
            "occurrences_by_classification": dict(sorted(status_occurrences.items())),
        },
        "notes": [
            "Pass 1 only: no proof of mathematical validity, no admissions and no edits.",
            "Phrase heads include newly published term headings automatically.",
            "Possible spelling/plural variants are hints, not asserted equivalent terms.",
            "Previous decisions are optional and must be maintained by editorial review.",
            "Rerun after any publication; the input is generated anew from canonical sources.",
        ],
        "entries": entries,
    }


def read_decisions(path: Path) -> dict:
    if not path.is_file():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("schema") != "mathdef.discovery-decisions.v1":
        raise ValueError("Unrecognized editorial decision registry schema")
    result = {}
    for entry in raw.get("decisions", []):
        phrase = normalize(entry["phrase"])
        if phrase in result:
            raise ValueError("Duplicate reviewed candidate: " + phrase)
        if entry["status"] not in {"accepted", "rejected", "deferred", "duplicate", "ignored"}:
            raise ValueError("Unsupported editorial decision: " + entry["status"])
        result[phrase] = {"status": entry["status"], "reason": entry.get("reason", ""),
                          "target_group_id": entry.get("target_group_id")}
    return result


def run(site: Path, out: Path, decisions: Path) -> dict:
    manifest_counts = validate_site(site)
    catalog = json.loads((site / "catalog.json").read_text(encoding="utf-8"))
    snapshot = json.loads((site / "api/definitions/v2/snapshot.json").read_text(encoding="utf-8"))
    report = discover(catalog, snapshot, decisions=read_decisions(decisions))
    report["input_feed_sha256"] = manifest_counts["sha256"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "candidates.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (out / "candidates.tsv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, dialect="excel-tab")
        writer.writerow(["candidate_id", "phrase", "classification", "occurrences",
                         "formulation_count", "source_formulation_ids", "matched_group_ids"])
        for item in report["entries"]:
            writer.writerow([item["id"], item["phrase"], item["classification"],
                             item["occurrences"], item["formulation_count"],
                             "|".join(x["formulation_id"] for x in item["examples"]),
                             "|".join(item["matched_group_ids"])])
    summary = {k: report[k] for k in
               ("schema", "status", "input_feed_sha256", "scope", "counts", "notes")}
    (out / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--site-root", type=Path, default=Path("_site"))
    p.add_argument("--output", type=Path, default=Path("_discovery"))
    p.add_argument("--decisions", type=Path,
                   default=Path("research_pipeline/discovery/decisions.json"))
    args = p.parse_args()
    print(json.dumps(run(args.site_root, args.output, args.decisions), indent=2))


if __name__ == "__main__":
    main()
