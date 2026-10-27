"""Global cross-chunk audit of the *existing* mathDef merged link graph.

Strictly read-only. No term discovery, candidate collection or link creation.
Every existing group, meaning, formulation, relation and rendered dependency
is checked in one graph, including edges between research/source cohorts.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from research_pipeline.adapters.mathdef.merged_linking import (
    masked_prose, name_index, words, WORD_RE,
)


def audit(catalog: dict, rendered: list[dict]) -> dict:
    findings = defaultdict(list)
    totals = Counter()
    groups = catalog["groups"]
    relations = catalog["relations"]
    group_map = {}
    meaning_group = {}
    form_map = {}
    form_group = {}
    form_origin = {}
    target_form = {}
    for group in groups:
        gid = group["id"]
        if gid in group_map:
            findings["errors"].append({"error": "duplicate_group_id", "group": gid})
        group_map[gid] = group
        for meaning in group["meanings"]:
            mid = meaning["id"]
            if mid in meaning_group:
                findings["errors"].append({"error": "duplicate_meaning_id", "meaning": mid})
            meaning_group[mid] = gid
            for form in meaning["formulations"]:
                fid = form["id"]
                if fid in form_map:
                    findings["errors"].append({"error": "duplicate_formulation_id", "formulation": fid})
                form_map[fid] = form
                form_group[fid] = gid
                form_origin[fid] = meaning.get("source_origin", "independent_or_postwave")
                target_form[fid] = mid

    rel_ids = set()
    edges = defaultdict(list)
    by_source = defaultdict(list)
    for rel in relations:
        rid = rel.get("id")
        if rid in rel_ids:
            findings["errors"].append({"error": "duplicate_relation_id", "relation": rid})
        rel_ids.add(rid)
        fid, mid = rel.get("from_formulation"), rel.get("target_meaning")
        totals["all_relations"] += 1
        if fid not in form_map or mid not in meaning_group:
            findings["errors"].append({"error": "dangling_relation", "relation": rid,
                                        "from": fid, "to": mid})
            continue
        source_gid, target_gid = form_group[fid], meaning_group[mid]
        cross = form_origin[fid] + "->" + (
            "original_mathdef" if mid.startswith("meaning.mathdef.original.") else
            "postwave" if mid.startswith("meaning.mathdef.postwave.") else "wave2"
        )
        totals["cross_cohort." + cross] += 1
        reltype = rel.get("relation_type")
        totals["relation_type." + str(reltype)] += 1
        if reltype != "definition_uses":
            totals["related_edges"] += 1
            if source_gid == target_gid:
                findings["same_group_related"].append({"relation": rid, "term": group_map[source_gid]["title"]})
            continue
        totals["definition_uses"] += 1
        edges[(fid, mid)].append(rid)
        by_source[fid].append(rel)
        if source_gid == target_gid:
            findings["self_group_definition_links"].append({"relation": rid, "group": source_gid})
        start, end = rel.get("span_start", -1), rel.get("span_end", -1)
        anchored = isinstance(start, int) and isinstance(end, int) and start >= 0
        if not anchored:
            totals["unanchored_def_uses"] += 1
            continue
        totals["anchored_def_uses"] += 1
        body = form_map[fid]["text"]
        if end <= start or end > len(body):
            findings["errors"].append({"error": "span_out_of_bounds", "relation": rid,
                                        "form": fid, "span": [start, end]})
            continue
        raw = body[start:end]
        if raw != rel.get("source_phrase", raw):
            findings["errors"].append({"error": "span_phrase_mismatch", "relation": rid,
                                        "from": fid, "found": raw,
                                        "declared": rel.get("source_phrase")})
        if any(c != " " and c != "\\n" for c in masked_prose(body)[start:end]) and not raw.strip():
            findings["errors"].append({"error": "empty_source_span", "relation": rid})
        # Distinguish a valid literal phrase from a position that falls in a
        # TeX math expression: source spans should be visible ordinary prose.
        if not masked_prose(body)[start:end].strip():
            findings["masked_source_anchor"].append({"relation": rid, "form": fid,
                                                       "phrase": raw[:80]})
    for (fid, mid), ids in edges.items():
        if len(ids) > 1:
            findings["duplicate_form_target"].append({"formulation": fid, "target": mid,
                                                       "relations": ids})
    for fid, rels in by_source.items():
        anchored = sorted((r["span_start"], r["span_end"], r["id"],
                           r["target_meaning"]) for r in rels
                          if isinstance(r.get("span_start"), int) and r["span_start"] >= 0)
        for left, right in zip(anchored, anchored[1:]):
            if right[0] < left[1]:
                findings["overlapping_spans"].append({"formulation": fid,
                    "first": left, "second": right})
    rendered_by_id = {x["id"]: x for x in rendered}
    if len(rendered_by_id) != len(rendered):
        findings["errors"].append({"error": "duplicate_rendered_group"})
    if set(rendered_by_id) != set(group_map):
        findings["errors"].append({"error": "render_group_mismatch",
                                   "absent": list(set(group_map)-set(rendered_by_id))[:20],
                                   "extra": list(set(rendered_by_id)-set(group_map))[:20]})
    for gid, entry in rendered_by_id.items():
        if gid not in group_map:
            continue
        expected_forms = {f["id"] for m in group_map[gid]["meanings"]
                          for f in m["formulations"]}
        actual_forms = {f["key"] for f in entry["formulations"]}
        if actual_forms != expected_forms:
            findings["errors"].append({"error": "render_form_mismatch", "group": gid})
        if entry.get("body") != entry["formulations"][0]["body"]:
            findings["errors"].append({"error": "render_first_body_mismatch", "group": gid})
        for form in entry["formulations"]:
            fid = form["key"]
            if fid not in form_map:
                continue
            expected_deps = Counter((r["target_meaning"], r.get("span_start", -1),
                                     r.get("span_end", -1))
                                    for r in by_source.get(fid, []))
            actual_deps = Counter((d["target_meaning"], d["start"], d["end"])
                                  for d in form.get("dependencies", []))
            if expected_deps != actual_deps:
                findings["errors"].append({"error": "render_dependencies_mismatch", "form": fid,
                                          "missing": list((expected_deps-actual_deps).elements())[:8],
                                          "extra": list((actual_deps-expected_deps).elements())[:8]})
            for dep in form.get("dependencies", []):
                target = dep.get("id")
                if target not in rendered_by_id or meaning_group.get(dep["target_meaning"]) != target:
                    findings["errors"].append({"error": "render_target_mismatch", "form": fid,
                                                "target": target,
                                                "meaning": dep["target_meaning"]})
                if dep["start"] >= 0:
                    body = form["body"]
                    if not (dep["start"] < dep["end"] <= len(body)):
                        findings["errors"].append({"error": "render_invalid_span", "form": fid})
        for target in entry.get("related", []):
            if target not in rendered_by_id:
                findings["errors"].append({"error": "render_dangling_related", "group": gid,
                                            "target": target})
    # Independent, corpus-wide scan for links to *already existing* headings.
    # This is NOT a candidate-collection scan; no unknown vocabulary captured.
    idx = name_index(catalog)
    unlinked = Counter()
    unlinked_examples = defaultdict(list)
    covered = 0
    specialized_context_anchors = 0
    suppressed_known_false_positives = 0
    matched = 0
    for fid, form in form_map.items():
        body = form["text"]
        hidden = masked_prose(body)
        tokens = [(m.group(0).casefold(), m.start(), m.end())
                  for m in WORD_RE.finditer(hidden)]
        anchors = [(r["span_start"], r["span_end"], meaning_group[r["target_meaning"]])
                   for r in by_source.get(fid, [])
                   if isinstance(r.get("span_start"), int) and r["span_start"] >= 0]
        i = 0
        while i < len(tokens):
            current = None
            for parts, gids in idx.get(tokens[i][0], []):
                n = len(parts)
                if i+n > len(tokens) or tuple(x[0] for x in tokens[i:i+n]) != parts:
                    continue
                if any(not _safe_gap(body[tokens[k][2]:tokens[k+1][1]])
                       for k in range(i,i+n-1)):
                    continue
                current = (parts, gids, i+n)
                break
            if not current:
                i += 1
                continue
            parts, gids, last = current
            start, end = tokens[i][1], tokens[last-1][2]
            i = last
            if len(gids) != 1 or gids[0] == form_group[fid]:
                continue
            matched += 1
            gid = gids[0]
            if any(start == lo and end == hi and gid == target for lo, hi, target in anchors):
                covered += 1
                continue
            # A CW complex's "weak topology" is correctly linked to the
            # researched CW-topology meaning, not the unrelated weak
            # topologies of functional analysis. Do not misreport that
            # explicit source-specific match as a missing generic link.
            if (target_form[fid] == "meaning.mathdef.original.alg-topology.cell-complex"
                and label_matches_weak_topology(group_map[gid]["title"])
                and any(
                    meaning_group[r["target_meaning"]] != gid
                    and r["target_meaning"] ==
                        "meaning.mathdef.postwave.scan-weak-topology-cw-complex-20261026"
                    and r.get("span_start", -1) >= 0
                    for r in by_source[fid]
                )):
                specialized_context_anchors += 1
                continue
            # Two source definitions are deliberately about distinct
            # *directional quasi-metric balls*, not ordinary open metric
            # balls, so adding a generic link here would be incorrect.
            if (target_form[fid] in {
                    "meaning.mathdef.original.quasimetric.forward-ball",
                    "meaning.mathdef.original.quasimetric.backward-ball",
                } and group_map[gid]["title"].casefold() == "open ball"):
                suppressed_known_false_positives += 1
                continue
            # Earlier term-use in the same definition may be anchored already;
            # subsequent mentions need not be individually annotated. Count
            # only formulation/group pairs with *no* positioned reference.
            if any(gid == target for _, _, target in anchors):
                continue
            label = group_map[gid]["title"]
            unlinked[label] += 1
            if len(unlinked_examples[label]) < 3:
                unlinked_examples[label].append({
                    "formulation": fid, "from_term": group_map[form_group[fid]]["title"],
                    "phrase": body[start:end],
                    "excerpt": body[max(0,start-70):min(len(body),end+70)],
                })
    totals["matched_existing_term_occurrences"] = matched
    totals["specialized_context_anchors"] = specialized_context_anchors
    totals["suppressed_known_false_positives"] = suppressed_known_false_positives
    totals["exact_anchor_matches"] = covered
    totals["unlinked_existing_term_occurrences"] = sum(unlinked.values())
    stats = {"groups": len(groups), "meanings": len(meaning_group),
             "formulations": len(form_map), "relations": len(relations),
             "rendered_groups": len(rendered_by_id),
             "rendered_formulations": sum(len(e["formulations"]) for e in rendered)}
    anomalies = {k: len(v) for k,v in findings.items()}
    return {
        "schema_version": 1,
        "scope": "entire_merged_corpus_cross_cohort_existing_links_only",
        "no_candidate_discovery": True,
        "stats": stats,
        "relation_totals": dict(sorted(totals.items())),
        "anomaly_counts": anomalies,
        "anomalies": {k:v[:150] for k,v in findings.items() if v},
        "known_existing_term_unlinked": {
            "total_occurrences": sum(unlinked.values()),
            "distinct_target_labels": len(unlinked),
            "top": [{"target_term": term, "occurrences": n,
                     "examples": unlinked_examples[term]}
                    for term,n in unlinked.most_common(100)]
        },
        "notes": [
            "Unlinked existing-term mentions are audit signals, not proposed new terminology.",
            "Some missing anchors reflect source-sensitive mathematical ambiguity, self-definitions, deliberate suppression, or earlier duplicate mentions.",
            "Automatic lexical links are tentative, not human-verified mathematics.",
        ],
    }


def label_matches_weak_topology(label: str) -> bool:
    return label.casefold() == "weak topology"


def _safe_gap(gap: str) -> bool:
    import re
    return bool(re.fullmatch(r"\s+|\s*[-–]\s*", gap))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--catalog", type=Path, required=True)
    p.add_argument("--index", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    result = audit(json.loads(args.catalog.read_text(encoding="utf-8")),
                   json.loads(args.index.read_text(encoding="utf-8")))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n",
                           encoding="utf-8")
    print("GLOBAL_LINK_AUDIT_SUMMARY_JSON=" + json.dumps({
        "stats": result["stats"], "relation_totals": result["relation_totals"],
        "anomaly_counts": result["anomaly_counts"],
        "unlinked_existing_term_occurrences":
            result["known_existing_term_unlinked"]["total_occurrences"],
        "top_unlinked": result["known_existing_term_unlinked"]["top"][:18],
        "anomaly_examples": {k:v[:12] for k,v in result["anomalies"].items()},
    }, ensure_ascii=False, separators=(",",":")))
    if result["anomaly_counts"].get("errors"):
        raise SystemExit("Failed strict whole-graph index/endpoint consistency audit")


if __name__ == "__main__":
    main()
