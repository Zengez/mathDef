"""Stage-specific GitHub Pages views of independent mathDef reconstruction.

The original production site is built by the pre-existing frontend pipeline.
This module reads ONLY independent experiment records and adapter files and
writes to a separate subdirectory of the Pages artifact.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

from research_pipeline.adapters.mathdef.preview import build
from research_pipeline.adapters.mathdef.direct_additions import add_direct_research
from research_pipeline.adapters.mathdef.original_merge import (
    read_original, merge_original, fast_scan, scan_report_html,
)
from research_pipeline.ui.renderer import render as render_reference_ui

WAVE1 = Path("research_pipeline/experiments/reconstruction-v1-recovery")
WAVE2 = Path("research_pipeline/experiments/reconstruction-v2-independent")


def render(repo: Path, site: Path) -> dict:
    repo = repo.resolve()
    site = site.resolve()
    # Only the independent research records and the frozen independent Wave 1
    # catalog are required to display this research preview. The retired
    # dependency graph and consolidation gates must never block rendering.
    for path in (
        repo / WAVE1 / "published" / "catalog.json",
        repo / WAVE2 / "records" / "meanings.jsonl",
    ):
        if not path.is_file():
            raise FileNotFoundError(f"Missing independent preview input: {path}")

    wave1 = build(repo / WAVE1, output=site / "wave1")
    wave2 = build(repo / WAVE2, draft=True, output=site / "wave2")

    # The legacy experiment viewer remains available in its own workspace.
    # Here, only the generated *independent preview catalogs* are converted
    # to the shared reference UI. No production site index is consulted.
    brand = repo / "research_pipeline/adapters/mathdef/ui_branding.json"
    ui1 = render_reference_ui(
        site / "wave1/catalog.json", brand, site / "wave1",
        "Wave 1 — frozen baseline",
        "An independently reconstructed, frozen first wave. Research-screened, not human verified."
    )
    ui2 = render_reference_ui(
        site / "wave2/catalog.json", brand, site / "wave2",
        "Wave 2 — initial reconstruction complete",
        "Initial independently reconstructed research corpus complete; mathematical drafts and citations are not human certified."
    )

    # New explicit post-reconstruction comparison: the original .tex corpus
    # is merged into a SEPARATE browsing view; neither frozen Wave 1 nor the
    # independently completed 958-meaning Wave 2 is modified.
    originals = read_original(repo)
    direct_file = repo / WAVE2 / "direct_research" / "terms.json"
    direct_entries = json.loads(direct_file.read_text(encoding="utf-8"))["entries"]
    independent = json.loads((site / "wave2" / "catalog.json").read_text(encoding="utf-8"))
    merged, merge_counts = merge_original(independent, originals)
    # Preserve the original fast scan's exact historical input scope: 363
    # independent direct texts and original mathDef texts, before admitting
    # any further post-Wave2 research. It is a discovery report, not a gate.
    scan = fast_scan(direct_entries, originals, merged)
    merged_baseline_meanings = merge_counts["combined_meanings"]
    post_wave2_added = add_direct_research(
        merged["groups"], merged["relations"],
        repo / WAVE2 / "post_wave2" / "terms.json",
    )
    merge_counts["original_plus_independent_meanings"] = merged_baseline_meanings
    merge_counts["post_wave2_meanings"] = post_wave2_added
    merge_counts["combined_meanings"] += post_wave2_added
    merge_counts["combined_term_groups"] = len(merged["groups"])
    combined_folder = site / "merged"
    combined_folder.mkdir(parents=True, exist_ok=True)
    (combined_folder / "catalog.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    ui_combined = render_reference_ui(
        combined_folder / "catalog.json", brand, combined_folder,
        "mathDef · Original, Wave 2, and subsequent research",
        "All completed independent Wave 2 meanings, original mathDef source definitions, "
        "and subsequent source-attributed research in one collection. "
        "Exact term-name matches do not assert mathematical equivalence; drafts are not peer certified.",
    )
    (combined_folder / "scan-report.json").write_text(
        json.dumps(scan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (combined_folder / "scan-report.html").write_text(
        scan_report_html(scan, merge_counts), encoding="utf-8"
    )
    print(json.dumps({"combined_merge": merge_counts, "rapid_scan": scan["counts"]}))

    def card(href, title, description, count):
        return ('<a class="stage" href="' + href + '/"><h2>' +
                html.escape(title) + '</h2><p>' + html.escape(description) +
                '</p><span>' + html.escape(count) + '</span></a>')

    cards = card(
        "wave1", "Wave 1 · Frozen baseline",
        "The initial independent reconstruction, preserved as our baseline.",
        str(wave1["meanings"]) + " contextual meanings"
    ) + card(
        "wave2", "Wave 2 · Independent reconstruction",
        "Initial research pass complete: original 418 leads considered and new meanings integrated. "
        "New terminology discovery and further source verification remain future work.",
        str(wave2["meanings"]) + " contextual meanings"
    ) + card(
        "merged", "Combined mathDef · Original + Wave 2",
        "Original mathDef definitions, independent Wave 2 meanings and new research "
        "in one searchable view. Includes the original rough terminology scan.",
        str(merge_counts["combined_meanings"]) + " source-provenanced meanings"
    )
    page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Independent mathDef reconstruction · Research previews</title>
<style>
:root{font-family:system-ui,-apple-system,sans-serif;color:#182336;
background:#f6f8fb}body{max-width:900px;margin:0 auto;padding:35px 20px 70px}
h1{font-size:2rem;line-height:1.15}p{line-height:1.6}
.small{font-size:.9rem;color:#506077}
.stages{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-top:25px}
.stage{display:block;text-decoration:none;color:inherit;border:1px solid #d1d9e4;
border-radius:13px;background:white;padding:24px}
.stage:hover,.stage:focus{outline:2px solid #4866aa}
.stage h2{margin-top:0}.stage span{color:#304e86;font-weight:600}
.notice{margin-top:26px;padding:14px 18px;border-left:4px solid #576e96;background:#eaf0f8}
</style></head><body>
<p class="small"><a href="../">Original mathDef site</a> · Independent research experiment</p>
<h1>Independent mathematical definitions reconstruction</h1>
<p>Compare the frozen independent Wave 1, completed independent Wave 2, and an explicitly original-inclusive merged reference.
Wave 1 and the completed independent Wave 2 remain source-independent and frozen for comparison.\nThe new combined view explicitly includes the original mathDef content, as authorized for this expansion.</p>
<div class="stages">___CARDS___</div>
<div class="notice"><strong>Research previews, not a certified reference.</strong>
Definitions, citations, and relationships remain assistant-screened research drafts,
not formally peer-reviewed mathematical facts. Initial Wave 2 reconstruction is complete;
The completed fast terminology scan is available in the combined view, which can now grow through subsequent direct research without changing the Wave 2 checkpoint.</div>
<p class="small">Wave 1 is frozen. Wave 2 is the completed initial reconstruction snapshot built directly from
its independent research records, without relying on the abandoned research stage gates.
Both are presented separately from the original mathDef content.</p>
</body></html>""".replace("___CARDS___", cards)
    site.mkdir(parents=True, exist_ok=True)
    (site / "index.html").write_text(page, encoding="utf-8")
    return {"wave1": wave1, "wave2": wave2, "merged": merge_counts, "rapid_scan": scan["counts"],
            "reference_ui": {"wave1": ui1, "wave2": ui2, "merged": ui_combined},
            "validation": {"independent_research_inputs_only": True,
                           "no_dependency_graph_gate": True},
            "site": str(site)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--site-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(render(args.repo_root, args.site_root), indent=2))


if __name__ == "__main__":
    main()
