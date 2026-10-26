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

    def card(href, title, description, count):
        return ('<a class="stage" href="' + href + '/"><h2>' +
                html.escape(title) + '</h2><p>' + html.escape(description) +
                '</p><span>' + html.escape(count) + '</span></a>')

    cards = card(
        "wave1", "Wave 1 · Frozen baseline",
        "The initial independent reconstruction, preserved as our baseline.",
        str(wave1["meanings"]) + " contextual meanings"
    ) + card(
        "wave2", "Wave 2 · Initial reconstruction complete",
        "Initial research pass complete: original 418 leads considered and new meanings integrated. "
        "New terminology discovery and further source verification remain future work.",
        str(wave2["meanings"]) + " contextual meanings"
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
<p>Explore the second, independently researched version of mathDef at two stages.
The original mathDef content is <strong>not</strong> used to construct these previews.</p>
<div class="stages">___CARDS___</div>
<div class="notice"><strong>Research previews, not a certified reference.</strong>
Definitions, citations, and relationships remain assistant-screened research drafts,
not formally peer-reviewed mathematical facts. Initial Wave 2 reconstruction is complete;
new-term discovery and further validation have not yet been undertaken.</div>
<p class="small">Wave 1 is frozen. Wave 2 is the completed initial reconstruction snapshot built directly from
its independent research records, without relying on the abandoned research stage gates.
Both are presented separately from the original mathDef content.</p>
</body></html>""".replace("___CARDS___", cards)
    site.mkdir(parents=True, exist_ok=True)
    (site / "index.html").write_text(page, encoding="utf-8")
    return {"wave1": wave1, "wave2": wave2,
            "reference_ui": {"wave1": ui1, "wave2": ui2},
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
