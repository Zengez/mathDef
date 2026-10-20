# Reusable UI port checkpoint — 2026-10-20

Scope: **presentation-only** work on independent reconstruction site. No mathematical sources, terms, formulations, relation decisions, original production definitions or citations were edited.

## Implemented in feature branch

- Copied and extracted the original reference UI shell, layout, styles, search behavior and feedback interface into `research_pipeline/ui/`.
- Added a generic, brand-configured static frontend renderer with a display-only data contract. The project-specific name, logo, description, labels and issue URL are configured in `research_pipeline/adapters/mathdef/ui_branding.json`.
- Integrated independent frozen Wave 1 and unsealed Wave 2 into that shared interface via `preview_site.py`, translating only their **own** generated preview catalogs into display indexes.
- Preserved distinct meanings and formulation-level source provenance. Definitions and relations are **not synthesized by the GUI**.
- Preserved expandable links, prioritizing the independently linked contextual meaning without removing other correct contexts. Exact inline word positions are unavailable for some independent links; controls fall back beneath the formulation rather than guessing textual offsets.
- Added a generic synthetic astronomy test for domain independence, context variants, sources, relationships, data isolation and HTML escaping, and JS syntax checks in isolated CI.
- Legacy experimental `preview.py` remains available inside the independent workspaces; production `web/` has not changed.

## Verification gates before merge

1. Confirm latest full research-pipeline isolated tests pass on feature branch (including the two real independent preview builds).
2. Review resulting HTML for both stages and JavaScript/browser interactions; CI syntax/unit assertions are not a full manual visual parity check.
3. Confirm original production Pages build and tests are unchanged.
4. After merging, verify live GitHub Pages deployment and the original mathDef URL.
5. Return to independent Wave 2 research from the existing `RESUME_STATE.json` and `resume_plan.json`; do not use original mathematical content.

The reusable display package is an extraction of the original **GUI only**. It does not authorize looking at original mathematical content during reconstruction.
