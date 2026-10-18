"""Post-freeze evaluation of independent reconstructed corpora against mathDef.

ONLY THIS evaluation adapter may read the original definitions/ tree. Do not
import this module from acquisition, source intake, stage execution or adapters.
A name match is a CANDIDATE for equivalence, not a mathematical verification.
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.parse
from collections import defaultdict
from pathlib import Path

from research_pipeline.engine.core import PipelineError, Workspace, atomic_json, digest


def normalize(text):
    return " ".join(re.findall(r"[a-z0-9]+", str(text).casefold()))


def clean_url(value):
    if not value:
        return ""
    u = urllib.parse.urlparse(value)
    if not u.hostname:
        return ""
    path = urllib.parse.unquote(u.path).rstrip("/")
    return u.hostname.casefold().removeprefix("www.") + path.casefold()


def parse_tex_header(path):
    meta = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("%"):
            if line.strip():
                break
            continue
        match = re.match(r"^%\s*([a-z_]+):\s*(.*)$", line)
        if match:
            meta[match.group(1)] = match.group(2).strip()
    return meta


def original_mathdef(root):
    """Read-only baseline. Only invoked AFTER both experimental waves freeze."""
    root = Path(root).resolve()
    directory = root / "definitions"
    if not directory.is_dir():
        raise PipelineError("Explicit baseline path must contain definitions/")
    original = {}
    for path in sorted(directory.rglob("*.tex")):
        meta = parse_tex_header(path)
        if not meta.get("id") or not meta.get("term"):
            raise PipelineError(f"Malformed existing definition: {path}")
        if meta["id"] in original:
            raise PipelineError("Duplicate original definition IDs")
        original[meta["id"]] = {
            "id": meta["id"], "name": meta["term"],
            "aliases": [x.strip() for x in meta.get("aliases", "").split("|") if x.strip()],
            "source": meta.get("source", ""),
            "related": [x.strip() for x in meta.get("related", "").split(",") if x.strip()],
            "variants": [],
        }
    for path in sorted((root / "variants").rglob("*.tex")):
        meta = parse_tex_header(path)
        parent = meta.get("parent")
        if parent in original:
            original[parent]["variants"].append({
                "key": meta.get("key", ""), "label": meta.get("label", ""),
                "source": meta.get("source", ""),
            })
    return original


def frozen_catalog(workspace):
    w = Workspace(workspace)
    expected = w.root / "state" / "publication.json"
    file = w.root / "published" / "catalog.json"
    if not expected.is_file() or not file.is_file():
        raise PipelineError("Both reconstruction waves must be published before comparison")
    manifest = json.loads(expected.read_text(encoding="utf-8"))
    catalog = json.loads(file.read_text(encoding="utf-8"))
    if digest(catalog) != manifest["sha256"]:
        raise PipelineError("Experiment publication hash has changed since freezing")
    # A sealed published catalog must also match the current sealed records.
    w.publication()
    return catalog


def candidates(baseline, catalog):
    meanings = catalog["meanings"]
    terms = {t["id"]: t for t in catalog.get("terms", [])}
    indexed = defaultdict(set)
    for m in meanings:
        labels = [m["display_term"]]
        labels += [terms[t]["label"] for t in m.get("term_ids", []) if t in terms]
        for label in labels:
            if normalize(label):
                indexed[normalize(label)].add(m["id"])
    result = {}
    for original in baseline.values():
        possibilities = set()
        for label in [original["name"]] + original["aliases"]:
            possibilities.update(indexed.get(normalize(label), set()))
        result[original["id"]] = sorted(possibilities)
    return result


def collect_links(baseline, catalog, matches):
    meaning_by_form = {
        f["id"]: m["id"] for m in catalog["meanings"] for f in m["formulations"]
    }
    reconstructed_edges = set()
    for rel in catalog["relations"]:
        frm = meaning_by_form.get(rel["from_formulation"])
        if frm:
            reconstructed_edges.add((frm, rel["target_meaning"]))
    found = []
    unclear = []
    total = 0
    for original in baseline.values():
        for target in original["related"]:
            if target not in baseline:
                continue
            total += 1
            start = matches.get(original["id"], [])
            end = matches.get(target, [])
            if len(start) != 1 or len(end) != 1:
                unclear.append({"from_original": original["id"], "to_original": target,
                                "reason": "Unmatched or ambiguous concept identity"})
            elif (start[0], end[0]) in reconstructed_edges:
                found.append({"from_original": original["id"], "to_original": target,
                              "from_reconstructed": start[0], "to_reconstructed": end[0]})
    return {"original_links": total, "confirmed_name_mapped_link_candidates": len(found),
            "ambiguous_or_unmatched_links": len(unclear),
            "unresolved_cases": unclear[:500]}


def wave_score(baseline, catalog):
    match = candidates(baseline, catalog)
    recovered = {key: ids for key, ids in match.items() if len(ids) == 1}
    ambiguous = {key: ids for key, ids in match.items() if len(ids) > 1}
    source_old = {clean_url(x["source"]) for x in baseline.values() if clean_url(x["source"])}
    source_old.update(clean_url(v["source"]) for x in baseline.values() for v in x["variants"] if clean_url(v["source"]))
    source_new = {clean_url(s["url"]) for s in catalog["sources"] if clean_url(s["url"])}
    hosts_old = {x.split("/")[0] for x in source_old}
    hosts_new = {x.split("/")[0] for x in source_new}
    unmatched = sorted(set(baseline) - set(recovered) - set(ambiguous))
    return {
        "baseline_concepts": len(baseline),
        "experiment_meanings": len(catalog["meanings"]),
        "experiment_formulations": sum(len(m["formulations"]) for m in catalog["meanings"]),
        "experiment_sources": len(catalog["sources"]),
        "source_url_overlap": len(source_old & source_new),
        "baseline_source_urls": len(source_old),
        "source_domain_overlap": len(hosts_old & hosts_new),
        "baseline_source_domains": len(hosts_old),
        "unique_name_match_candidates": len(recovered),
        "ambiguous_name_matches": len(ambiguous),
        "unmatched_baseline_concepts": len(unmatched),
        "unmatched_examples": unmatched[:100],
        "links": collect_links(baseline, catalog, match),
        "review_queue": [
            {"baseline_id": key, "original_name": baseline[key]["name"],
             "candidate_meaning_ids": ids, "review_required": True,
             "reason": "Name agreement does not establish mathematical equivalence"}
            for key, ids in sorted(match.items()) if ids
        ],
        "caveat": "These are automatic lexical/source/link candidate matches, NOT verified mathematical recovery or correctness."
    }


def compare(baseline_root, first_workspace, second_workspace, output):
    first = frozen_catalog(first_workspace)
    second = frozen_catalog(second_workspace)
    if Path(first_workspace).resolve() == Path(second_workspace).resolve():
        raise PipelineError("The two waves must be distinct workspaces")
    baseline = original_mathdef(baseline_root)
    first_result = wave_score(baseline, first)
    second_result = wave_score(baseline, second)
    report = {
        "schema_version": 1, "design": "post-freeze-independent-reconstruction",
        "wave1": first_result, "wave2": second_result,
        "improvement": {
            "unique_name_match_candidates_delta":
                second_result["unique_name_match_candidates"] - first_result["unique_name_match_candidates"],
            "source_url_overlap_delta":
                second_result["source_url_overlap"] - first_result["source_url_overlap"],
            "link_candidate_delta":
                second_result["links"]["confirmed_name_mapped_link_candidates"] -
                first_result["links"]["confirmed_name_mapped_link_candidates"],
        },
        "human_semantic_review_required": True,
        "limitations": [
            "Baseline may have its own missing or erroneous entries.",
            "Match counts are lexical heuristics, not claims that definitions are equivalent.",
            "Original related links and reconstructed relations may represent different link types.",
            "Recorded execution time/API usage must be imported separately from stage manifests.",
        ],
    }
    atomic_json(output, report)
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--baseline-root", type=Path, required=True,
                   help="Explicit mathDef repository root; evaluation only, never used by acquisition")
    p.add_argument("--wave1", type=Path, required=True)
    p.add_argument("--wave2", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = compare(args.baseline_root, args.wave1, args.wave2, args.output)
    print(json.dumps({"wave1_candidates": result["wave1"]["unique_name_match_candidates"],
                      "wave2_candidates": result["wave2"]["unique_name_match_candidates"],
                      "report": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
