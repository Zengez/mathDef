# Deduplication, Subject/Context and sources — working checkpoint

Date: 2026-10-27
Branch: `work/dedup-subject-context-sources-20261027`
Authoritative execution plan: `TEMP_DEDUPLICATION_SUBJECT_CONTEXT_SOURCES_PLAN_2026-10-27.md`.

## Contract and gate

- Active work is **merged-corpus cleanup only**. Do not alter original `definitions/`, `variants/`, historical independent Wave 2 records, candidate scan, or historical preview snapshots.
- No new terminology discovery. Do not revive dependency-graph review.
- **Do not run final global linking rebuild, change production publication, or deploy deduplicated corpus until user reviews uncertain decisions**. This branch is preparation, reviewable data/logic, and stage-local tests only.
- User-facing Sources UI, source correction analytics, and automatic source ranking are deferred.
- Semantic deduplication is never driven solely by lexical similarity.

## Baseline inventory

- Current public combined snapshot: **2,048 headings, 2,197 meanings, 2,246 formulations, 6,825 relations** (pre-cleanup published baseline).
- Historical originals: **1,014** .tex definition files. Existing merge source is `research_pipeline/adapters/mathdef/original_merge.py`.
- Initial independent Wave2: **595 screened record meanings** plus **363 direct-research meanings** = **958**; historical immutable.
- Post-Wave2 overlay: **225** meanings; immutable historical research input.
- Fast deterministic filename/normalized-heading intersection between original filenames and newly researched term titles: **91 original .tex paths** match, before reading and normalizing actual TeX term declarations. This is a **lower-bound priority worklist**, not a complete count of original/new shared headings. Full mathematical comparison must follow actual rendered titles and all cohorts.
- Relevant existing code: `preview_site.py` combines source cohorts and calls `merged_linking.py`; `publish_root.py` still enforces preservation of every original formulation verbatim; `renderer.py` builds the UI search index; `merged_definition_export.py` builds v2 feed; `audit_merged_links.py` checks relations. These must be upgraded together in Phase E, **not** partially pushed to production.
- Existing original source-file GitHub links are **editorial provenance**, *not* independent mathematical authorities. Sources registry must separate them from external citations.

## Immediate work

1. Inspect and adjudicate initial original/new overlapping formulations, recording exact ID mappings and preserved references in a merged-only overlay.
2. Extend to other shared headings and within-cohort alternatives; produce temporary **full-term** unresolved decision packets.
3. Establish registries and data compiler for surviving Subject, optional Context, sources/primary links; run stage-local validation only.
4. Stop before Phase E and present every unresolved definition under each term for user review.

## Progress

- [x] Read execution plan and `AGENTS.md`.
- [x] Trace entry points for merge, publication, UI, linker, source export, global link audit.
- [x] Baseline and lower-bound original/new overlap inventoried.
- [x] Dedicated work branch created at main commit `a5762f78a67b2c0f4260399d8d5d2ce8f0d83e7f`.
- [ ] Original/new semantic comparison and approved duplicate decisions.
- [ ] Whole-corpus pass.
- [ ] Subject/context and term source registry compiled and audited.
- [ ] User adjudication of genuinely uncertain decisions.
- [ ] Post-adjudication single full linking/build/export/browser validation.

This checkpoint is deliberately incremental and should be updated after each meaningful batch. Counts of reviewed vs. undecided are not asserted until source statements are actually examined.
