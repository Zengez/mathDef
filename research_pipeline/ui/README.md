# Portable reference interface (display-only)

This directory contains a **presentation component** extracted from the original mathDef GUI. It does not read the original `definitions/`, `variants/`, citation records, or generated production `definitions-index.json` to assemble the independent reconstruction.

## What is shared

- `template.html`: two independent search boxes, split/focused result panes, recursive exploration controls, suggestion form, and the familiar masthead. Brand-specific text is substituted as escaped literals.
- `styles.css`: a visually identical copy of the original mathDef stylesheet, with a small nonintrusive research-stage notice added.
- `app.js`: original reference UI interaction patterns, with a portable configuration and independent source-aware display links. The source-linked contextual variant is prioritized when opening an independently constructed dependency.
- `feedback.js`: GitHub issue draft interface. The issue destination is supplied by the project configuration; submitting an issue cannot mutate research data.
- `renderer.py`: reusable, display-only conversion from a **supplied** groups/meanings/formulations/relations display catalog into a static web search index, HTML, CSS and JavaScript.

## Domain adapter boundary

The mathDef adapter supplies `research_pipeline/adapters/mathdef/ui_branding.json` and independently generated `preview/catalog.json`. The adapter chooses an output location, a stage name, and the stage description. The portable renderer never searches mathematical definitions or infers that two independently researched concepts are equivalent.

To reuse for another subject, provide an equivalent independent display catalog, a replacement branding JSON with name/logo/description/terminology/repository URL, and a separate stage output directory. For theorem or math-education projects, **do not import mathDef production data or its source-discovery heuristics**; instead, implement a domain adapter that explicitly maps independently researched records to this display contract.

## Commands and testing

From repository root, the mathDef Pages build is:

```bash
python -m research_pipeline.adapters.mathdef.preview_site --site-root /tmp/independent-reconstruction-preview
python -m unittest research_pipeline.tests.test_reference_ui -v
node --check research_pipeline/ui/app.js
node --check research_pipeline/ui/feedback.js
```

The `preview_site` command reads the frozen independent Wave 1 published catalog and screened independent Wave 2 records. It checks structural integrity of the displayed meanings, source evidence and link endpoints, but **does not require or execute any retired dependency-graph scan, consolidation gate, or global reconstruction checkpoint**. It builds experiment-only catalogs and renders both using the portable UI. It neither seals Wave 2 nor changes either source workspace, and it is separate from the original production Pages index generation.

## Limitations and further verification

The current preview is derived from already **screened** research records, not a source-completeness or human-peer-reviewed certification. The independent stage catalog does not always contain exact word-offset information for definition links: nested expansion is supported and the In-Line view places controls after the relevant formulation when offsets are absent. The source-linked contextual meaning is displayed first in recursive expansion. Full cross-browser/visual screenshot comparison against the original interface, mobile testing and feedback-form end-to-end QA remain useful before relying on identical behavior.

For now, production `web/` is deliberately unchanged. The reusable UI was extracted from that design rather than redirecting production users to an unproven new code path. Once the reconstruction preview has been visually approved, production can optionally switch to the common interface without changing its mathematical corpus.
