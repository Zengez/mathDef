"""Lossless display overlay and intentionally rough terminology scan.

An explicitly user-authorized, post-reconstruction comparison of original
mathDef with independent Wave 2. Never mutates either source collection.
Not a dependency graph, citation verification, or definition admission gate.
"""
from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
import html
import json
import re
import unicodedata
from pathlib import Path

from scripts.build_index import parse, attach_formulations


MATH_NOUNS = (
    "algebra", "basis", "category", "closure", "cover", "derivative",
    "differential", "embedding", "element", "extension", "field", "function",
    "functor", "graph", "group", "homomorphism", "ideal", "interior",
    "interval", "lattice", "limit", "manifold", "map", "mapping", "matrix",
    "measure", "metric", "module", "morphism", "norm", "operator", "order",
    "point", "polynomial", "product", "projection", "quotient", "relation",
    "representation", "ring", "sequence", "series", "set", "sheaf", "space",
    "subgroup", "submodule", "subset", "subspace", "sum", "tensor",
    "topology", "transformation",
)
# This is deliberately a rough, error-tolerant phrase finder, not an audit.
PHRASE_RE = re.compile(
    r"\b(?:(?:[a-z][a-z-]{2,})\s+){1,3}(?:" +
    "|".join(MATH_NOUNS) + r")s?\b", re.IGNORECASE,
)


def key(value):
    value = unicodedata.normalize("NFKC", value).casefold()
    value = re.sub(r"\\(?:emph|textbf|textit|mathrm|text|operatorname)\{([^{}]*)\}", r"\1", value)
    value = re.sub(r"\\([a-z]+)\b", r"\1", value)
    return " ".join(re.sub(r"[^\w]+", " ", value).split())


def for_display(value):
    """Use math delimiters understood by the reusable preview UI."""
    value = value.replace(r"\(", "$").replace(r"\)", "$")
    value = value.replace(r"\[", "$$").replace(r"\]", "$$")
    # Prose wrappers are not currently supported by the reference preview.
    return re.sub(
        r"\\(?:emph|textbf|textit)\{([^{}]*)\}",
        lambda match: match.group(1), value,
    )


def read_original(repo):
    """Read all original .tex definitions and their alternative formulations."""
    from scripts import build_index
    # build_index.parse categorizes paths relative to its own DEFS constant.
    # Use its established, validated metadata parser; never modify the source.
    originals = [
        parse(path) for path in sorted((Path(repo) / "definitions").rglob("*.tex"))
    ]
    if not originals:
        raise ValueError("No original mathDef definitions found")
    attach_formulations(originals, require_all_parents=True)
    ids = [entry["id"] for entry in originals]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate original mathDef definition IDs")
    return originals


def merge_original(catalog, originals):
    """Add all original definitions to a COPIED display catalog.

    Exact term labels cohabit one search heading. A source definition retains
    its own meaning and all original formulations: no automatic assertion that
    matching names imply equivalent mathematical contexts.
    """
    merged = deepcopy(catalog)
    groups, relations = merged["groups"], merged["relations"]
    grouped = {key(g["title"]): g for g in groups}
    original_ids = {d["id"]: "meaning.mathdef.original." + d["id"] for d in originals}
    original_fids = {}
    shared = 0
    added_groups = 0

    for entry in originals:
        term = entry["term"]
        normalized = key(term)
        if normalized in grouped:
            group = grouped[normalized]
            shared += 1
        else:
            # Existing original IDs are stable; namespace a unique search group.
            from research_pipeline.engine.core import digest
            gid = "preview.term." + digest("original merge: " + normalized)[:24]
            group = {"id": gid, "title": term, "aliases": [], "meanings": []}
            groups.append(group)
            grouped[normalized] = group
            added_groups += 1
        for alias in entry.get("aliases", []):
            if alias and key(alias) != normalized and alias not in group["aliases"]:
                group["aliases"].append(alias)
        original_source = (
            "https://github.com/Zengez/mathDef/blob/main/" + entry["path"]
        )
        forms = entry.get("formulations") or [{
            "key": "primary", "label": entry.get("form_label", "Original formulation"),
            "body": entry["body"], "source": entry["source"], "path": entry["path"],
            "status": entry["status"],
        }]
        formatted = []
        for form in forms:
            form_id = "form.mathdef.original." + entry["id"] + "." + form["key"]
            if form["key"] == "primary":
                original_fids[entry["id"]] = form_id
            cited = form.get("source") or entry.get("source")
            cites = [{
                "title": entry.get("source_title") or "Original mathDef editorial source",
                "url": cited or original_source,
                "locator": cited or original_source,
                "verification_status": "original_mathdef_editorial",
                "role": ("Original mathDef citation; editorial draft, not "
                         "reverified in this cross-corpus merge")
                if cited else "Source-file provenance only, not mathematical evidence",
            }]
            if cited:
                cites.append({
                    "title": "Original mathDef source file", "url": original_source,
                    "locator": original_source, "role": "Definition provenance",
                })
            formatted.append({
                "id": form_id, "text": for_display(form["body"]),
                "sources": cites, "review_state": "screened",
                "origin_path": form.get("path", entry["path"]),
                "original_status": form.get("status", entry["status"]),
            })
        # If an original alternative is marked "primary" differently, ensure a
        # stable first formulation for the original related-term edges.
        if entry["id"] not in original_fids:
            original_fids[entry["id"]] = formatted[0]["id"]
        group["meanings"].append({
            "id": original_ids[entry["id"]],
            "label": "Original mathDef · " + entry["category"],
            "display_term": term, "term_group_id": group["id"],
            "research_status": "original_mathdef_editorial_draft",
            "source_origin": "original_mathdef",
            "original_definition_id": entry["id"],
            "formulations": formatted, "other_sources": [],
        })

    valid_original = set(original_ids)
    original_links = 0
    for entry in originals:
        source_id = original_fids[entry["id"]]
        for related in entry.get("related", []):
            if related not in valid_original:
                raise ValueError(
                    f"Original mathDef related ID missing: {entry['id']} -> {related}"
                )
            if related == entry["id"]:
                continue
            relations.append({
                "id": f"rel.mathdef.original.{entry['id']}.to.{related}",
                "from_formulation": source_id,
                "target_meaning": original_ids[related],
                "relation_type": "related", "review_state": "screened",
                "editorial_reason": "Related link from original mathDef metadata",
            })
            original_links += 1
    for group in groups:
        group["meanings"].sort(key=lambda m: (m["label"].casefold(), m["id"]))
        group["aliases"].sort(key=str.casefold)
    groups.sort(key=lambda g: (g["title"].casefold(), g["id"]))
    return merged, {
        "original_definitions": len(originals),
        "original_variants": sum(
            len(d.get("formulations", [])) - 1 for d in originals if d.get("formulations")
        ),
        "shared_term_labels": shared,
        "new_term_groups": added_groups,
        "original_related_links": original_links,
        "combined_meanings": sum(len(g["meanings"]) for g in groups),
        "combined_term_groups": len(groups),
    }


def fast_scan(direct_entries, originals, combined_catalog):
    """Rough one-pass phrase and term-name scan; does NOT add definitions.

    Sources scanned: the 363 directly researched meanings AND all original
    mathematical definition bodies (including alternate formulations).
    Leaves the completed independent 958-meaning snapshot unchanged.
    """
    docs = [
        {"id": d["id"], "term": d["term"], "origin": "wave2_direct",
         "text": d["definition"]}
        for d in direct_entries
    ]
    for d in originals:
        variants = d.get("formulations") or [{"body": d["body"]}]
        for i, variant in enumerate(variants):
            docs.append({
                "id": d["id"] + ":" + str(i), "term": d["term"],
                "origin": "original_mathdef",
                "text": variant["body"],
            })

    # A known title or alias is *only* an occurrence hint; no semantic
    # equivalence of multiple contexts is inferred.
    names = {}
    for group in combined_catalog["groups"]:
        for label in [group["title"], *group.get("aliases", [])]:
            n = key(label)
            if len(n) >= 4 and (len(n.split()) > 1 or len(n) > 6):
                names.setdefault(n, group["id"])
    known = defaultdict(lambda: {"count": 0, "examples": []})
    proposed = defaultdict(lambda: {"count": 0, "examples": []})
    # Build an inverted index by first word to avoid an expensive global
    # every-name-against-every-definition scan.
    title_index = defaultdict(list)
    for phrase, gid in names.items():
        title_index[phrase.split()[0]].append((tuple(phrase.split()), phrase, gid))
    for values in title_index.values():
        values.sort(key=lambda v: -len(v[0]))
    max_words = max((len(t.split()) for t in names), default=1)
    for doc in docs:
        text = key(doc["text"])
        words = text.split()
        hits = set()
        for i, first in enumerate(words):
            for parts, label, gid in title_index.get(first, []):
                if tuple(words[i:i + len(parts)]) == parts:
                    if key(doc["term"]) != label:
                        hits.add((label, gid))
                    break   # longest matching term at this word position
        for label, gid in hits:
            record = known[(label, gid)]
            record["count"] += 1
            if len(record["examples"]) < 3:
                record["examples"].append({
                    "origin": doc["origin"], "source": doc["id"],
                    "term": doc["term"],
                })
        candidate_hits = {
            key(match.group(0))
            for match in PHRASE_RE.finditer(text)
        }
        for phrase in candidate_hits:
            if phrase in names or len(phrase) < 10:
                continue
            record = proposed[phrase]
            record["count"] += 1
            if len(record["examples"]) < 3:
                record["examples"].append({
                    "origin": doc["origin"], "source": doc["id"],
                    "term": doc["term"],
                })
    known_sorted = sorted(
        ({"term": phrase, "target_group": gid, **v} for (phrase, gid), v in known.items()),
        key=lambda o: (-o["count"], o["term"]),
    )
    candidate_sorted = sorted(
        ({"phrase": phrase, **v} for phrase, v in proposed.items()),
        key=lambda o: (-o["count"], o["phrase"]),
    )
    return {
        "schema_version": 1,
        "status": "rough_candidates_not_verified",
        "scan_scope": {
            "wave2_direct_meanings": len(direct_entries),
            "original_mathdef_definitions": len(originals),
            "original_variant_formulations": sum(
                len(d.get("formulations", [])) - 1
                for d in originals if d.get("formulations")
            ),
            "total_formulations_scanned": len(docs),
        },
        "notes": [
            "Fast lexical scan only. False positives, ambiguous concepts and omissions expected.",
            "Known-term mentions are potential contextual links, not validated dependencies.",
            "Suggested phrases are tentative research leads; no candidate admission gate.",
            "Original mathDef source meanings have been merged for browsing separately.",
            "The independent Wave 2 snapshot stays unchanged for comparison.",
        ],
        "known_term_mentions": known_sorted,
        "possible_new_terminology": candidate_sorted,
        "counts": {
            "known_term_mentions": len(known_sorted),
            "new_phrase_leads": len(candidate_sorted),
        },
    }


def scan_report_html(report, merge_counts):
    """Small human-readable entry to the generated JSON research report."""
    rows = []
    for record in report["possible_new_terminology"][:80]:
        rows.append(
            "<tr><td>" + html.escape(record["phrase"]) +
            "</td><td>" + str(record["count"]) + "</td></tr>"
        )
    scope = report["scan_scope"]
    return """<!doctype html><html lang="en"><meta charset="utf-8">
<title>Original mathDef + Wave 2 rapid terminology scan</title>
<style>body{font:16px system-ui;max-width:850px;margin:36px auto;padding:0 20px;line-height:1.5}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #ddd;text-align:left;padding:7px}
code{background:#f1f1f1;padding:3px}a{color:#21549e}</style>
<h1>First combined terminology scan</h1>
<p>This is a deliberately rough, error-tolerant scan, <strong>not</strong> an audit or
an approved list of mathematically distinct definitions.</p>
<p>Scanned """ + str(scope["wave2_direct_meanings"]) + """ new Wave 2 definitions,
""" + str(scope["original_mathdef_definitions"]) + """ original mathDef definitions
and """ + str(scope["original_variant_formulations"]) + """ original alternatives.</p>
<p>Found <strong>""" + str(report["counts"]["new_phrase_leads"]) + """</strong> candidate phrase leads,
and <strong>""" + str(report["counts"]["known_term_mentions"]) + """</strong> known-title mentions.
The merged preview includes """ + str(merge_counts["combined_meanings"]) + """ source-provenanced meanings,
under """ + str(merge_counts["combined_term_groups"]) + """ searchable term headings.</p>
<p><a href="index.html">Merged searchable mathDef</a> ·
<a href="scan-report.json">Complete machine-readable scan results</a> ·
<a href="../wave2/">Unmodified independent Wave 2 snapshot</a></p>
<h2>First 80 candidate phrases (ranked by occurrences)</h2>
<table><thead><tr><th>Unverified phrase</th><th>Definition occurrences</th></tr></thead>
<tbody>""" + "".join(rows) + """</tbody></table></html>"""
