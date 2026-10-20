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
from research_pipeline.engine.resume_checkpoint import snapshot

WAVE1 = Path("research_pipeline/experiments/reconstruction-v1-recovery")
WAVE2 = Path("research_pipeline/experiments/reconstruction-v2-independent")
CONFIG = Path("research_pipeline/adapters/mathdef/resume.json")


def render(repo: Path, site: Path) -> dict:
    repo = repo.resolve()
    site = site.resolve()
    # Validation verifies frozen independent Wave 1 lineage, all individual
    # mathematical review records and the unsealed Wave 2 graph. No production
    # mathDef definitions, sources, or variants are ever consulted.
    verification = snapshot(repo / CONFIG, repo)
    valid = verification["domain_validation"]
    if not (valid["frozen_wave1_digest_recomputed_and_matched"]
            and valid["editable_wave2_unsealed"]
            and not valid["dependency_graph_has_cycles"]):
        raise ValueError("Independent reconstruction validation failed")

    wave1 = build(repo / WAVE1, output=site / "wave1")
    wave2 = build(repo / WAVE2, draft=True, output=site / "wave2")

    def card(href, title, description, count):
        return ('<a class="stage" href="' + href + '/"><h2>' +
                html.escape(title) + '</h2><p>' + html.escape(description) +
                '</p><span>' + html.escape(count) + '</span></a>')

    cards = card(
        "wave1", "Wave 1 · Frozen baseline",
        "The initial independent reconstruction, preserved as our baseline.",
        str(wave1["meanings"]) + " contextual meanings"
    ) + card(
        "wave2", "Wave 2 · Living research draft",
        "New independently sourced and screened work, unsealed and incomplete. "
        "Updated when research is committed and the site rebuilds.",
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
<p class="small"><a href="../../">Original mathDef site</a> · Independent research experiment</p>
<h1>Independent mathematical definitions reconstruction</h1>
<p>Explore the second, independently researched version of mathDef at two stages.
The original mathDef content is <strong>not</strong> used to construct these previews.</p>
<div class="stages">___CARDS___</div>
<div class="notice"><strong>Research previews, not a certified reference.</strong>
Definitions, citations, and relationships are research-screened drafts,
not human-refereed mathematical facts. Wave 2 is still undergoing research.</div>
<p class="small">Wave 1 is frozen. Wave 2 is a working snapshot built directly from
its independent research records, without sealing or publishing its research stages.
Both are presented separately from the original mathDef content.</p>
</body></html>""".replace("___CARDS___", cards)
    site.mkdir(parents=True, exist_ok=True)
    (site / "index.html").write_text(page, encoding="utf-8")
    return {"wave1": wave1, "wave2": wave2,
            "validation": {"frozen_wave1": True, "wave2_unsealed": True},
            "site": str(site)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--site-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(render(args.repo_root, args.site_root), indent=2))


if __name__ == "__main__":
    main()
