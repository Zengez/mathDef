"""Read-only prioritization of overlaps AMONG EXISTING mathDef formulations.

This is NOT a term-discovery tool. Every returned item is an existing live
group, meaning and formulation ID. Similarity is NEVER a merge decision.
The full merged link reconstruction is neither imported nor invoked here.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import json
import re

TOK = re.compile(r"[a-z][a-z0-9]{2,}", re.I)
STOP = frozenset(("the", "and", "with", "for", "that", "such", "are", "has",
                  "have", "there", "from", "each", "which", "then", "its",
                  "into", "can", "all", "set", "every", "let", "some",
                  "this", "when", "one", "over", "also", "any", "where",
                  "called", "said", "given", "satisfies", "defined",
                  "exactly", "respectively", "iff", "if", "only", "being"))


def _title(s: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", s.casefold()))


def _tokens(body: str) -> frozenset[str]:
    # This intentionally lossy index is used ONLY to find review comparisons.
    # It is never used to remove a formulation or declare semantic identity.
    return frozenset(t for t in TOK.findall(body.casefold()) if t not in STOP)


def screen(catalog: dict, *, limit: int = 60, cutoff: float = 0.73) -> dict:
    """Screen the supplied existing IDs and produce a bounded review index."""
    groups = catalog["groups"]
    forms = []
    labels = defaultdict(list)
    term_groups = {}
    for group in groups:
        gid = group["id"]
        term_groups[gid] = group["title"]
        for label in [group["title"], *group.get("aliases", [])]:
            normalized = _title(label)
            # Very short aliases are often ambiguous symbols, not concepts.
            if len(normalized) >= 8 and gid not in labels[normalized]:
                labels[normalized].append(gid)
        for m in group["meanings"]:
            for f in m["formulations"]:
                forms.append({
                    "group_id": gid, "term": group["title"], "meaning_id": m["id"],
                    "formulation_id": f["id"], "tokens": _tokens(f["text"]),
                    "body": f["text"],
                })
    collisions = []
    for label, ids in labels.items():
        if len(ids) < 2:
            continue
        for left, right in combinations(sorted(ids), 2):
            collisions.append({
                "shared_name_or_alias": label,
                "left_group": left, "left_term": term_groups[left],
                "right_group": right, "right_term": term_groups[right],
                "classification": "inspect_existing_headings_not_assumed_equivalent",
            })

    inverted = defaultdict(list)
    for n, form in enumerate(forms):
        if len(form["tokens"]) < 7:
            continue
        for token in form["tokens"]:
            inverted[token].append(n)
    shared = Counter()
    for token, indices in inverted.items():
        if len(indices) > 120:
            continue  # Common words do not help prioritize.
        for a, b in combinations(indices, 2):
            if forms[a]["group_id"] != forms[b]["group_id"]:
                shared[(a, b)] += 1
    scored = []
    for (a, b), overlap in shared.items():
        if overlap < 7:
            continue
        fa, fb = forms[a], forms[b]
        ta, tb = fa["tokens"], fb["tokens"]
        common = len(ta & tb)
        ratio = common / len(ta | tb)
        if ratio < cutoff:
            continue
        scored.append({
            "lexical_jaccard": round(ratio, 4),
            "left_group": fa["group_id"], "left_term": fa["term"],
            "left_meaning": fa["meaning_id"],
            "left_formulation": fa["formulation_id"],
            "right_group": fb["group_id"], "right_term": fb["term"],
            "right_meaning": fb["meaning_id"],
            "right_formulation": fb["formulation_id"],
            "left_excerpt": fa["body"][:240],
            "right_excerpt": fb["body"][:240],
            "classification": "screen_only_requires_mathematical_review",
        })
    scored.sort(key=lambda v: (-v["lexical_jaccard"], v["left_term"],
                               v["right_term"], v["left_formulation"],
                               v["right_formulation"]))
    collisions.sort(key=lambda v: (v["shared_name_or_alias"],
                                   v["left_term"], v["right_term"]))
    multi_meaning = sorted((
        {"term": g["title"], "group_id": g["id"],
         "meaning_ids": [m["id"] for m in g["meanings"]]}
        for g in groups if len(g["meanings"]) > 1
    ), key=lambda v: (v["term"].casefold(), v["group_id"]))
    multi_form = sorted((
        {"term": g["title"], "meaning_id": m["id"],
         "formulation_ids": [f["id"] for f in m["formulations"]]}
        for g in groups for m in g["meanings"] if len(m["formulations"]) > 1
    ), key=lambda v: (v["term"].casefold(), v["meaning_id"]))
    return {
        "schema_version": 1,
        "kind": "existing_definitions_only_no_vocabulary_discovery",
        "status": "nonadjudicative_screen_not_research_approval",
        "notes": [
            "All group, meaning and formulation IDs are already present in the staged corpus.",
            "Lexical similarity and alias collisions are not mathematical equivalence.",
            "No new terminology is collected and no action edits links, definitions or sources.",
        ],
        "counts": {
            "groups": len(groups), "formulations": len(forms),
            "name_alias_collision_pairs": len(collisions),
            "cross_heading_lexical_pairs_above_cutoff": len(scored),
            "multi_meaning_groups": len(multi_meaning),
            "within_meaning_multi_formulations": len(multi_form),
        },
        "name_alias_collisions": collisions[:limit],
        "cross_heading_lexical_screen": scored[:limit],
        "multi_meaning_groups": multi_meaning,
        "within_meaning_multiform": multi_form,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=60)
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    result = screen(catalog, limit=args.limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "counts": result["counts"],
        "alias_collisions": result["name_alias_collisions"][:25],
        "cross_heading_examples": result["cross_heading_lexical_screen"][:30],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
