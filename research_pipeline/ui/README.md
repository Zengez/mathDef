# Portable reference interface (display-only)

This directory contains a **presentation component** extracted from the original mathDef GUI. It does not read the original `definitions/`, `variants/`, citation records, or generated production `definitions-index.json` to assemble the independent reconstruction.

## What is shared

- `template.html`: two independent search boxes, split/focused result panes, recursive exploration controls, suggestion form, and the familiar masthead. Brand-specific text is substituted as escaped literals.
- `styles.css`: a visually identical copy of the original mathDef stylesheet, with a small nonintrusive research-stage notice added.
- `app.js` + `subject_priority.js`: shared reference UI with display-only, source-formulation-aware contextual ordering. In inline and nested definition expansion, an exact official mathematical Subject match from the containing formulation takes priority among a linked term’s existing formulations. Among matches, the previously linked meaning wins ties; without any exact match or source Subject, the previously linked meaning stays first. All formulations remain visible and no relation targets/corpus records are rewritten. Different registered Subjects (e.g. Algebra vs Linear Algebra) are not automatically treated as equivalent without a separately approved subject hierarchy.
- `feedback.js`: GitHub issue draft interface. The issue destination is supplied by the project configuration; submitting an issue cannot mutate research data.
- `renderer.py`: reusable, display-only conversion from a **supplied** groups/meanings/formulations/relations display catalog into a static web search index, HTML, CSS and JavaScript. It can optionally apply a validated, explicitly approved first-display priority registry. Such overrides outrank exact Subject matches, which outrank the original link target preference. The decisions do not rewrite mathematical meaning IDs or sources.

## Domain adapter boundary

The mathDef adapter supplies `research_pipeline/adapters/mathdef/ui_branding.json` and independently generated `preview/catalog.json`. The adapter chooses an output location, a stage name, and the stage description. The portable renderer never searches mathematical definitions or infers that two independently researched concepts are equivalent.

To reuse for another subject, provide an equivalent independent display catalog, a replacement branding JSON with name/logo/description/terminology/repository URL, and a separate stage output directory. For theorem or math-education projects, **do not import mathDef production data or its source-discovery heuristics**; instead, implement a domain adapter that explicitly maps independently researched records to this display contract.

## Commands and testing

From repository root, the mathDef Pages build is:

```bash
python -m research_pipeline.adapters.mathdef.preview_site --site-root /tmp/independent-reconstruction-preview
python -m unittest research_pipeline.tests.test_reference_ui -v
node --check research_pipeline/ui/app.js
node --test research_pipeline/tests/test_subject_priority.cjs
python -m unittest research_pipeline.tests.test_reference_ui -v
node --check research_pipeline/ui/feedback.js
```

The `preview_site` command reads the frozen independent Wave 1 published catalog and screened independent Wave 2 records. It checks structural integrity of the displayed meanings, source evidence and link endpoints, but **does not require or execute any retired dependency-graph scan, consolidation gate, or global reconstruction checkpoint**. It builds experiment-only catalogs and renders both using the portable UI. It neither seals Wave 2 nor changes either source workspace, and it is separate from the original production Pages index generation.

## Limitations and further verification

The current preview is derived from already **screened** research records, not a source-completeness or human-peer-reviewed certification. The independent stage catalog does not always contain exact word-offset information for definition links: nested expansion is supported and the In-Line view places controls after the relevant formulation when offsets are absent. The source-linked meaning is used as fallback and tie-breaker; when both sides expose a matching official Subject ID, its matching target formulation(s) are displayed first. The source formulation controls the comparison, not the heading’s historical cohort label. Full cross-browser/visual screenshot comparison against the original interface, mobile testing and feedback-form end-to-end QA remain useful before relying on identical behavior.

For now, production `web/` is deliberately unchanged. The reusable UI was extracted from that design rather than redirecting production users to an unproven new code path. Once the reconstruction preview has been visually approved, production can optionally switch to the common interface without changing its mathematical corpus.

## Approved per-link priority overrides

The mathDef-specific editorial registry is `data/definition_expansion_priority_overrides.json`. It begins with **zero overrides**; an unreviewed user suggestion is never automatically accepted. Upon approving a correction, an editor explicitly adds an `approved` record with a unique ID, the **source formulation ID**, **target term/group ID**, the desired **target formulation ID**, an approval reference (e.g., a reviewed GitHub Issue), and a mathematical rationale. An optional `source_span: {start, end}` restricts it to one linked occurrence; otherwise it covers all occurrences of that target within the specified source formulation. An exact-span rule takes precedence over a general rule. These are canonical live IDs from the *cleaned* corpus, not display titles.

Example (illustrative placeholders, NOT an active approval):

```json
{
  "id": "accepted-example-001",
  "status": "approved",
  "source_formulation_id": "form.example.source",
  "target_group_id": "preview.term.example-target",
  "preferred_formulation_id": "form.example.target",
  "approval_reference": "https://github.com/Zengez/mathDef/issues/123",
  "reason": "Editor-reviewed contextual priority correction"
}
```

The portable renderer validates every approved rule against the built catalog, rejects duplicate/conflicting selectors, nonexistent source/target IDs, unapproved statuses, and missing actual dependency links. It emits `preferred_formulation` only on matching display dependencies. Inline and nested views respect the preference without changing the definitions, citation statuses, relations, or normal search order. If no approved override exists for a clicked link, the official Subject priority still applies. The root-site publisher explicitly loads this registry when a cleaned release is authorized; independent historical preview views do not load it. The final global relink and production deployment remain separately gated.

## User-facing Sources interface (staged)
The merged mathDef main-site publisher builds source metadata from **exactly the catalog being published**, using `compile_source_registry()`, and the portable renderer exposes it as a separately fetched `sources-index.json`. This avoids transferring merged-cleanup identifiers into the frozen Wave 1/2 preview records. The source registry's selected primary reference is the best *available citation evidence*, not a reliability rating or a claim of independent verification. Every reference preserves its original URL, title, role, verification status, occurrence and source-scoped convention assessment. Definitions continue to be displayed as mathematical statements, not cluttered with source metadata.

The Sources button on each searchable term opens a dialog grouped by meaning and formulation. A corresponding button on multi-formulation cards can open the same dialog focused on that formulation (including recursively expanded terms). Primary references, other cited supporting references, additional encountered works, and original-repository provenance are distinct categories. Verification and convention metadata is described conservatively; provenance-only citations are **never** treated as supporting mathematical authorities. The sources payload is lazily fetched and the dialog allows source-correction suggestions through the existing review-only GitHub feedback form. Any error in the registry (missing group, stale meaning/formulation, unsupported primary citation, invalid source identity) fails CI/build instead of silently hiding source evidence. No source-scores or correction counts are invented.
