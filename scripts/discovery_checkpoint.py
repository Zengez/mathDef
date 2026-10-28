"""Incremental, persistent, source-level mathDef discovery checkpoints.

A "scanned candidate" is a canonical source formulation (stable ID + content
hash), NOT a suggestion automatically rejected. Unchanged formulations are
never tokenized or phrase-extracted again in routine runs. Newly published term
heads can be applied to cached tokens, without re-reading source texts.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from scripts.current_corpus_discovery import (
    EXAMPLE_LIMIT, SEED_HEADS, extract_phrases, normalize, plain_words, variants,
)

SCHEMA = "mathdef.discovery-checkpoint.v1"
SCANNER_VERSION = 1


def new_checkpoint():
    return {
        "schema": SCHEMA, "scanner_version": SCANNER_VERSION,
        "formulations": {}, "heads": [], "seen_leads": [],
        "runs": 0, "last_feed_sha256": None,
    }


def read_checkpoint(path: Path):
    path = Path(path)
    if not path.is_file():
        return new_checkpoint()
    result = json.loads(path.read_text(encoding="utf-8"))
    if (result.get("schema") != SCHEMA or
        result.get("scanner_version") != SCANNER_VERSION or
        not isinstance(result.get("formulations"), dict) or
        not isinstance(result.get("heads"), list) or
        not isinstance(result.get("seen_leads"), list) or
        not isinstance(result.get("runs"), int)):
        raise ValueError("Incompatible checkpoint; use an explicit migration or backup")
    if (len(result["seen_leads"]) != len(set(result["seen_leads"])) or
        any(normalize(x) != x for x in result["seen_leads"])):
        raise ValueError("Corrupt saved candidate history")
    for fid, record in result["formulations"].items():
        if not isinstance(record, dict) or not isinstance(record.get("words"), list) or (
            not isinstance(record.get("phrase_counts"), dict)
        ) or not record.get("sha256"):
            raise ValueError("Corrupt cached formulation: " + fid)
    return result


def _digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def incremental_discover(catalog, snapshot, checkpoint, *,
                         decisions=None, force=False, force_forms=(), force_groups=()):
    if snapshot.get("schema") != "mathdef.definition-snapshot.v2":
        raise ValueError("Incremental discovery requires exact canonical v2 feed")
    definitions = snapshot["definitions"]
    groups = {g["id"]: g for g in catalog["groups"]}
    if len(groups) != len(catalog["groups"]) or set(groups) != {d["id"] for d in definitions}:
        raise ValueError("Cannot scan incomplete/duplicated merged corpus")
    known = defaultdict(set)
    heads = set(SEED_HEADS)
    for d in definitions:
        for title in [d["term"], *d.get("aliases", [])]:
            name = normalize(title)
            if name:
                known[name].add(d["id"])
                heads.add(name.split()[-1])
    variants_index = defaultdict(set)
    for phrase, gids in known.items():
        for variant in variants(phrase):
            variants_index[variant].update(gids)

    old = checkpoint["formulations"]
    prev_heads = set(checkpoint["heads"])
    additional_heads = heads - prev_heads
    # A checkpoint without coverage is a new baseline, not a deliberate rescan.
    previous_seen = set(checkpoint["seen_leads"])
    current = {}
    stats = Counter()
    phrase_map = {}
    for d in sorted(definitions, key=lambda item: item["id"]):
        group = groups[d["id"]]
        for m in sorted(group["meanings"], key=lambda item: item["id"]):
            for f in sorted(m["formulations"], key=lambda item: item["id"]):
                fid = f["id"]
                signature = _digest(f["text"])
                former = old.get(fid)
                explicitly_forced = force or fid in force_forms or d["id"] in force_groups
                changed = former is not None and former["sha256"] != signature
                must_scan = former is None or changed or explicitly_forced
                if must_scan:
                    words = plain_words(f["text"])
                    hits = Counter(extract_phrases(words, heads))
                    if former is None:
                        stats["new_formulations_scanned"] += 1
                    elif explicitly_forced:
                        stats["explicitly_rescanned_formulations"] += 1
                    else:
                        stats["changed_formulations_scanned"] += 1
                else:
                    # No reading/tokenizing/extracting the same source again.
                    words = former["words"]
                    hits = Counter(former["phrase_counts"])
                    stats["unchanged_formulations_skipped"] += 1
                    if additional_heads:
                        # Only NEW vocabulary heads are checked against cached
                        # tokens; original source is NOT scanned again.
                        added = Counter(extract_phrases(words, additional_heads))
                        for key, n in added.items():
                            hits[key] = n
                        if added:
                            stats["cached_vocabulary_extensions"] += 1
                current[fid] = {
                    "sha256": signature, "group_id": d["id"],
                    "meaning_id": m["id"], "group_title": d["term"],
                    "words": words,
                    "phrase_counts": dict(sorted(hits.items())),
                }
                stats["current_formulations"] += 1
                stats["prose_words"] += len(words)
                for phrase, count in hits.items():
                    norm = normalize(phrase)
                    matched = known.get(norm)
                    possible = variants_index.get(norm)
                    if matched:
                        status, gids = "already_defined", matched
                    elif possible:
                        status, gids = "possible_variant", possible
                    elif norm in (decisions or {}):
                        status, gids = "previously_reviewed", set()
                    else:
                        status, gids = "unreviewed_candidate", set()
                    if norm not in phrase_map:
                        entry = {
                            "id": "term." + _digest(norm)[:20], "phrase": phrase,
                            "normalized": norm, "classification": status,
                            "matched_group_ids": sorted(gids),
                            "occurrences": 0, "formulation_count": 0,
                            "examples": [],
                        }
                        if status == "previously_reviewed":
                            entry["prior_decision"] = decisions[norm]
                        phrase_map[norm] = entry
                    entry = phrase_map[norm]
                    entry["occurrences"] += count
                    entry["formulation_count"] += 1
                    if len(entry["examples"]) < EXAMPLE_LIMIT:
                        entry["examples"].append({
                            "group_id": d["id"], "group_title": d["term"],
                            "meaning_id": m["id"], "formulation_id": fid,
                        })
    stats["removed_formulations"] = len(set(old) - set(current))
    priority = {"unreviewed_candidate": 0, "possible_variant": 1,
                "previously_reviewed": 2, "already_defined": 3}
    entries = sorted(phrase_map.values(), key=lambda e: (
        priority[e["classification"]], -e["formulation_count"],
        -e["occurrences"], e["normalized"],
    ))
    fresh = []
    for entry in entries:
        if entry["classification"] in ("unreviewed_candidate", "possible_variant"):
            if entry["normalized"] not in previous_seen:
                entry["discovery_state"] = "new"
                fresh.append(entry)
            else:
                entry["discovery_state"] = "previously_encountered"
        elif entry["classification"] == "previously_reviewed":
            entry["discovery_state"] = "editorially_reviewed"
        else:
            entry["discovery_state"] = "published"
    after_seen = previous_seen | {
        entry["normalized"] for entry in entries
        if entry["classification"] in ("unreviewed_candidate",
                                       "possible_variant", "previously_reviewed")
    }
    next_checkpoint = {
        "schema": SCHEMA, "scanner_version": SCANNER_VERSION,
        "formulations": current, "heads": sorted(heads),
        "seen_leads": sorted(after_seen), "runs": checkpoint["runs"] + 1,
        "last_feed_sha256": checkpoint.get("last_feed_sha256"),
    }
    classes = Counter(e["classification"] for e in entries)
    report = {
        "schema": "mathdef.current-corpus-discovery.v1",
        "status": "unverified_high_recall_candidates",
        "scope": {
            "term_groups": len(groups),
            "meanings": sum(len(g["meanings"]) for g in groups.values()),
            "formulations": stats["current_formulations"],
            "prose_words": stats["prose_words"],
        },
        "counts": {
            "phrase_occurrences": sum(x["occurrences"] for x in entries),
            "distinct_phrases": len(entries),
            "distinct_by_classification": dict(sorted(classes.items())),
            "new_leads_this_run": len(fresh),
            "previously_encountered_leads": sum(
                x["discovery_state"] == "previously_encountered" for x in entries),
            "source_checkpoint": dict(sorted(stats.items())),
        },
        "notes": [
            "Source-level incremental scan: only new, edited or forced formulations are re-tokenized.",
            "Previously seen candidates are NOT rejected and remain in complete candidates.json.",
            "Only new leads are in new_candidates.tsv; old leads are preserved without re-review.",
            "New term vocabulary is checked against cached word lists, not original source text.",
            "Force rescan is an explicit manual action; no automatic approval or rejection.",
        ],
        "entries": entries,
    }
    return report, next_checkpoint, fresh
