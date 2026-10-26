# mathDef — active development instructions (October 26, 2026)

## Current status: independent Wave 2 COMPLETE; post-Wave2 combined research underway

**As of 2026-10-26, the original 418-lead research pass is finished.**
The independent research preview contains **958 meanings**, with **1,511**
contextual relations (including **115 screened-to-direct incoming links**).
The original leads have dispositions: **350 incorporated** and **68 not
promoted**. The completed-pass record is
[`WAVE2_INITIAL_RECONSTRUCTION_COMPLETE_2026-10-26.md`](research_pipeline/experiments/reconstruction-v2-independent/WAVE2_INITIAL_RECONSTRUCTION_COMPLETE_2026-10-26.md).

**Do not restart the original 418-lead queue or revive dependency graphs,
stages, gates, and old audits.** The quick post-Wave2 terminology scan has
ALREADY COMPLETED across all 363 direct Wave 2 definitions and 1,014 original
mathDef definitions (+5 variants). The merged site has 1,972 original-plus-Wave2
baseline meanings, and the initial scan yielded 2,019 intentionally rough
phrase leads plus 473 known-term mention patterns.

**ACTIVE OWNER DIRECTIVE (2026-10-26): Process the ACTUAL 2,019
quick-scan terminology candidates now. Do NOT independently hunt for new terms
while this existing candidate collection is pending.** New-term discovery is a
different, separately authorized phase. Review the existing candidate's source
examples; compare against the independent + original + post-Wave2 catalog;
record a quick disposition (new meaning, existing/duplicate/synonym,
mathematically distinct variant, context ambiguity or lexical false positive).
Incorporate useful mathematical content DIRECTLY. Do not reintroduce
mandatory dependency graphs, slow gates, arbitrary verification packet stages,
or a new external vocabulary hunt.

The original frozen-scan incorporation now processed ranked candidates
**1–340 of 2,019** in
`research_pipeline/experiments/reconstruction-v2-independent/post_wave2/scan_candidate_dispositions.json`.
These yielded **34 source-attributed mathematical meanings** (new headings
and legitimate contextual variants), bringing the merged-only post-Wave2
overlay from its 118 pre-scan meanings to **152**. The latest **120**
ranks 221–340 produced **7 researched new meanings**, 33 existing
matches, 78 lexical nonterms, 1 contextual ambiguity, and 1 phrase already
covered by existing alternative conventions.
**Next candidate rank: 341.** The original scan is frozen and no new candidate
discovery is authorized while this collection is pending.

Keep per-candidate source examples, concise outcome and target mapping in this
same lightweight ledger; it is a resumption log, not a mathematical
admission gate. The original report is `/reconstruction/merged/scan-report.json`
and its lexical leads may include false positives.

For new meanings, use
`research_pipeline/experiments/reconstruction-v2-independent/post_wave2/terms.json`
and render them ONLY in `/reconstruction/merged/`, not the completed 958-meaning
independent Wave 2 or original production source. The preceding nine general
research batches added 118 meanings; the current scan-driven batch is a
DIFFERENT focus, not a restart of those unrelated expansions.
See `research_pipeline/experiments/reconstruction-v2-independent/post_wave2/README.md`.

## New explicit authorization: original-content merger and rapid scan (2026-10-26)

**After completing the independent Wave 2 reconstruction, the user explicitly
authorized scanning the 363 new definitions AND the original mathDef term
list/definition contents, and incorporating the original content into the new
searchable reference.** That changes the source-access rule *for the new
post-Wave2 merged view only*.

- Keep `/reconstruction/wave1/` frozen and `/reconstruction/wave2/` independently
  reconstructed at **958 meanings**; do not silently import the original corpus
  into that historical snapshot.
- The explicitly authorized `/reconstruction/merged/` view combines all original
  `definitions/*.tex`, `variants/*.tex` with independent Wave 2, preserving
  source IDs, citations, contexts and text. Production source files remain
  read-only. Match exact term labels under common search headings without
  asserting that their definitions are automatically equivalent.
- A fast lexical scan of new Wave 2 definitions and all original definition
  bodies yields **rough possible terminology** and existing-term mentions.
  These are error-tolerant starting leads only. **Do not turn the scan into
  another prerequisite-completion gate, graph closure or global approval audit.**
- See [post-Wave2 merge and scan record](research_pipeline/experiments/reconstruction-v2-independent/POST_WAVE2_ORIGINAL_MERGE_AND_SCAN_2026-10-26.md).

## Completed research method: build definitions, not a dependency-graph pipeline

The original dependency-first Wave 2 *workflow was abandoned by the project owner* because it made a deliberately rough candidate scan into an expensive, mandatory full-corpus mathematical review. **Do not resume or recreate its scans, aliases, amendment transactions, phase gates, staging ceremonies, or graph-resolution backlog.** No old workflow handoff, agent instruction in Git history, GitHub Actions log, old PR, or checkpoint supersedes this file.

### Fast, direct independent Wave 2 research

1. Use the already screened **independent** Wave 2 `research_pipeline/experiments/reconstruction-v2-independent/records/` as the starting draft corpus. Its screened relations are useful known links. The `population/records/` area contains 16 additional candidate meanings, not yet screened.
2. Use `research_pipeline/reviews/wave2-salvage-2026-10-26/CANDIDATE_WORKLIST_418.tsv` as a **tentative** research queue. Its existing 418 proposed candidate phrases and draft texts have source leads. Many will be duplicates, examples, notation, false positives, or variants. This is fine. **Never exhaustively pre-clear or globally deduplicate this queue before researching definitions.**
3. On each selected candidate, research the meaning and sources, choose its mathematical context and variants, compare plausible existing definitions, and **add/merge the researched definition and establish reasonable links within the same pass**. Save any newly noticed phrase as a future candidate; do not immediately recursively research it.
4. Add actual independent research definitions through simple batches to the **independent Wave 2 preview**, not via the removed `dependency_graph` / `generation_staging` workflows. Prioritize visible usable definitions and working links. A preliminary candidate-finding pass can contain mistakes and omitted terms.
5. Run **lightweight** checks on the resulting batch: valid IDs, supporting source URLs, mathematically honest statements, known conflict/edge-case flags, link endpoints that exist, no infinite nested-expansion loops. Document genuine mathematical ambiguities without blocking unrelated entries. User feedback is intended to improve completeness and linking iteratively.
6. Regularly show progress as definitions/variants/links actually visible in the prototype, not scans, review packets, gates or staging counters.

### Critical boundaries

- Original production mathDef was excluded as **mathematical input** for the historically independent reconstruction. It is NOW explicitly authorized as input to the separate **post-Wave2 merged view**, but must never be retrospectively counted as independently reconstructed. **Do not read/copy/search/import mathematical definitions, variants, data or citation content from `definitions/`, `variants/`, `data/`, or the production index** into Wave 2. Likewise do not import the frozen Wave 1 mathematical catalog. Code, shared UI and web build plumbing are reusable.
- Keep Wave 1 frozen. The independent Wave 2 draft and preview remain separate from production.
- Do not knowingly publish false mathematics or describe an unchecked lead as a verified direct source passage. State hypotheses and convention choices clearly; flag significant uncertain cases for later review. **Do not require perfect exhaustive review of every entry before making useful progress.**
- Do not add or re-enable graph-closure conditions, global first/second-pass review gates, or one-GitHub-Action-per-candidate submission workflows absent a new **explicit user request**.
- Do not run old Wave 2 batch-generation scripts, broad crawling, or old source-free reconciliation processes. The research materials and Git history already preserve prior evidence.
- Work on a branch for substantive changes, check the independent preview and production-site build before any merge, and never merge or publish production changes without authorized review.

For the retained assets and recovery details, see `research_pipeline/reviews/wave2-salvage-2026-10-26/SALVAGE_ASSESSMENT.md`. Older instructions are historical and superseded.
