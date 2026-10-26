# mathDef — active development instructions (October 26, 2026)

## Current goal: build mathematical definitions, not a dependency-graph pipeline

The original dependency-first Wave 2 *workflow was abandoned by the project owner* because it made a deliberately rough candidate scan into an expensive, mandatory full-corpus mathematical review. **Do not resume or recreate its scans, aliases, amendment transactions, phase gates, staging ceremonies, or graph-resolution backlog.** No old workflow handoff, agent instruction in Git history, GitHub Actions log, old PR, or checkpoint supersedes this file.

### Fast, direct independent Wave 2 research

1. Use the already screened **independent** Wave 2 `research_pipeline/experiments/reconstruction-v2-independent/records/` as the starting draft corpus. Its screened relations are useful known links. The `population/records/` area contains 16 additional candidate meanings, not yet screened.
2. Use `research_pipeline/reviews/wave2-salvage-2026-10-26/CANDIDATE_WORKLIST_418.tsv` as a **tentative** research queue. Its existing 418 proposed candidate phrases and draft texts have source leads. Many will be duplicates, examples, notation, false positives, or variants. This is fine. **Never exhaustively pre-clear or globally deduplicate this queue before researching definitions.**
3. On each selected candidate, research the meaning and sources, choose its mathematical context and variants, compare plausible existing definitions, and **add/merge the researched definition and establish reasonable links within the same pass**. Save any newly noticed phrase as a future candidate; do not immediately recursively research it.
4. Add actual independent research definitions through simple batches to the **independent Wave 2 preview**, not via the removed `dependency_graph` / `generation_staging` workflows. Prioritize visible usable definitions and working links. A preliminary candidate-finding pass can contain mistakes and omitted terms.
5. Run **lightweight** checks on the resulting batch: valid IDs, supporting source URLs, mathematically honest statements, known conflict/edge-case flags, link endpoints that exist, no infinite nested-expansion loops. Document genuine mathematical ambiguities without blocking unrelated entries. User feedback is intended to improve completeness and linking iteratively.
6. Regularly show progress as definitions/variants/links actually visible in the prototype, not scans, review packets, gates or staging counters.

### Critical boundaries

- Original production mathDef has 1007 entries and is out of scope as **mathematical input** for the independent reconstruction. **Do not read/copy/search/import mathematical definitions, variants, data or citation content from `definitions/`, `variants/`, `data/`, or the production index** into Wave 2. Likewise do not import the frozen Wave 1 mathematical catalog. Code, shared UI and web build plumbing are reusable.
- Keep Wave 1 frozen. The independent Wave 2 draft and preview remain separate from production.
- Do not knowingly publish false mathematics or describe an unchecked lead as a verified direct source passage. State hypotheses and convention choices clearly; flag significant uncertain cases for later review. **Do not require perfect exhaustive review of every entry before making useful progress.**
- Do not add or re-enable graph-closure conditions, global first/second-pass review gates, or one-GitHub-Action-per-candidate submission workflows absent a new **explicit user request**.
- Do not run old Wave 2 batch-generation scripts, broad crawling, or old source-free reconciliation processes. The research materials and Git history already preserve prior evidence.
- Work on a branch for substantive changes, check the independent preview and production-site build before any merge, and never merge or publish production changes without authorized review.

For the retained assets and recovery details, see `research_pipeline/reviews/wave2-salvage-2026-10-26/SALVAGE_ASSESSMENT.md`. Older instructions are historical and superseded.
