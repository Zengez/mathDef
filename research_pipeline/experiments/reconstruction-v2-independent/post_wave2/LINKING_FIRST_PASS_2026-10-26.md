# Merged-only mathematical linking — fast first pass (2026-10-26)

## Scope and purpose

The fully dispositioned **2,019 original frozen terminology candidates** are finished. This phase links **already existing terms** within the **2,197-meaning merged reference**. There is no new term search, no new definitions, no dependency graph, and no edits to the original mathDef definitions or frozen independent Wave 2/Wave 1 meaning data.

The site generator in `research_pipeline/adapters/mathdef/preview_site.py` builds the unchanged original inclusion and independent meaning catalogs, adds the existing 225 post-Wave2 merged-only meanings, and then calls `link_merged_catalog` from `merged_linking.py`. All changes are display-only additions to the in-memory merged catalog, published as `/reconstruction/merged/catalog.json`, `definitions-index.json`, and `link-report.json`.

## First full-corpus linking pass

In the successful PR smoke build, the linker visited **2,246 formulations** representing **2,197 contextual meanings** under 2,048 search headings, and:

- Added **2,334 tentative, literal-occurrence anchored** `definition_uses` links between already existing meanings.
- Located exact textual positions for **244 pre-existing screened/curated** definition-use links, so these can expand in-line rather than appearing only in an unanchored list.
- Found positioned links in **1,544 formulations** (~68.7%).
- Logged **860 ambiguous-context occurrences** for later contextual review, with no arbitrary winner chosen where meaning-level evidence was insufficient. `link-report.json` records the leading unresolved labels, sample accepted links, per-form counts, and full summary.
- Kept related-link metadata separate from definition-use links; existing explicit and editorial links remain in place.

These are **candidate links** based on actual term or alias text and a conservative disambiguator, *not* mathematical certification. The UI labels automatic links **Suggested** and retains a report-incorrect-link feedback action. Scoped handling makes *weak topology* in a CW complex select the CW notion, not the different functional-analysis weak topology.

## Matching constraints and next refinements

Matching is Unicode-aware, case-insensitive, supports a few ordinary plural forms, takes longest phrases first, suppresses self-links and duplicate source-form/target-meaning pairs, and masks standard LaTeX math delimiters so mathematical code is not misinterpreted as prose. It preserves exact string offsets for placement by the existing nested/inline UI. At most 35 automatic edges are added per formulation to avoid excessive clutter. Where a term heading contains genuinely different mathematical meanings, it selects a target only for strong contextual evidence or an explicit scoped override; otherwise it logs the unresolved occurrence.

The original and independent math definitions are not rewritten, and the historical 2,019-candidate terminology scan is unchanged.

**Next:** targeted review of the highest-frequency ambiguous group labels using source contexts; enhance alias/inflection support where useful (but do not invent terminology); inspect actual browser rendering of links and recursive expansion, check link-report issue reports, and accept community corrections. Future phases can inspect high-value unlinked formulations. Avoid the retired dependency-research gates or requiring an exhaustive per-edge approval process.

## Check commands

```bash
python -m unittest research_pipeline.tests.test_original_merge research_pipeline.tests.test_merged_linking -v
node --check research_pipeline/ui/app.js
python -m research_pipeline.adapters.mathdef.preview_site --site-root /tmp/mathdef-linked-preview
```

CI verifies exact 2,019 frozen-candidate disposition coverage, the unchanged 958-meaning independent baseline and 1,014 original definitions, the 225 post-wave meanings, source-aligned anchor offsets, distinct candidate link counts, and generated searchable pages.
