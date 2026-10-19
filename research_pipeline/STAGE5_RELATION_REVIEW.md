# Corrected Wave 1 — Stage 5 independent formulation relationship audit

**Live handoff (2026-10-18, America/New_York):** Stage 5 is **in progress, NOT sealed**. The authoritative machine checkpoint is `experiments/reconstruction-v1-recovery/state/checkpoint.json`. Stage 5 always works exclusively within the corrected independent reconstruction workspace; the original production mathDef corpus, variants and citations must NOT be consulted until both Wave 1 and Wave 2 have been frozen and published.

## Verified progress after two link batches and one disposition batch

| Editorial status | Count |
| --- | ---: |
| Stage 4 context-specific meaning records, sealed | 419 |
| Stage 4 individually screened formulations, sealed | 431 |
| Stage 5 formulations given individual dispositions | **55** |
| Formulations with one or more screened relationships | **39** |
| Source-screened `definition_uses` edges | **47** |
| Explicit, reasoned `no_supported_target` dispositions | **15** |
| Explicit `held_ambiguity` (missing/blocked target) | **1** |
| Formulations requiring Stage 5 mathematical relationship review | **376** |

**The review ratio is 55/431, not 47/431:** one formulation may legitimately have several dependencies; a no-link or held disposition counts only when individually reviewed, not by missing edges. The relationship dataset and the review ledger are separate on purpose.

### Verified sources, inputs, and committed state

- Sealed source content/meaning registries: `records/observations.jsonl`, `records/meanings.jsonl`, and `state/meanings.json` in `experiments/reconstruction-v1-recovery/`. Stage 4 SHA-256 meaning digest: `25c62402079c814c6bfe8d3fc391039df9a6c6fa6d8806d3fe6c1ed18b260ea6`.
- Curated screened link batches: `intake/stage5-curated-batch-01.jsonl` (16 links) and `intake/stage5-curated-batch-02.jsonl` (31 links). Each record points from a precise formulation ID to a precise target meaning ID, includes a phrase that appears in the formulation, individually authored mathematical rationale and independent Stacks source URLs for both ends.
- Curated disposition batch: `intake/stage5-disposition-batch-01.jsonl` (15 no-suitable-target decisions, one held ambiguity). The held item is the vector-space formulation referencing an abelian-group structure when the only Stage 2 abelian-group lead was access blocked. These decisions should NOT be misrepresented as having mathematical links.
- Machine review ledger: `state/stage5_formulation_reviews.jsonl` contains exactly one audit row for each of the 431 Stage 4 formulations, currently 55 terminal decisions and 376 explicit `needs_review` entries.
- Actual screened edges: `records/relations.jsonl`; most recent verified `state/relations.json`: 47 relations and `sealed:false`.
- Independent Stage 5 review gate: `engine/stage5_review_gate.py`; all CLI entry points below use the corrected workspace. Core `Workspace.seal('relations')` now requires completion of the per-formulation ledger in addition to previously mandated source and Stage 3 editorial coverage.
- Isolated regression cases: `tests/test_stage5_review_gate.py`; existing pipeline tests are executed again by the Stage 5 workflows.
- Tested GitHub-hosted workflows: `.github/workflows/mathdef-stage5-start.yml`, `mathdef-stage5-batches.yml`, and `mathdef-stage5-dispositions.yml`. Their completed jobs committed `46cc6a4c3fed`, `bd1a91ee20`, and `e62a4d780f` respectively; the last is the initial 55/431 checkpoint.
- The Stacks Project is the independently acquired source for the supported definitions. These are editor-screened candidates, `human_verified:false`; links are **not formal peer review**.

## Stage 5 workflow and commands

Work through the remaining 376 `needs_review` formulation IDs in bounded, meaningful groups (e.g. 10–25). Do not silently classify uninspected items. For each formulation, compare its actual mathematical prerequisites and context to *existing* screened meaning IDs, including possible cross-source synonyms. A link may be proposed only if its target meaning was actually reconstructed; do not create synthetic meanings for the 59 no-suitable and 27 blocked headings. Distinguish definitional dependencies from theorems, implications, narrower special cases, and lexical coincidence. Record ambiguous cases rather than guessing. Guard the source phrase, exact formulation ID, target meaning, source citation, and independently written reason. Existing source-grounded screened links may themselves need later semantic corrections in Wave 2.

Check the current coverage:

```bash
python -m research_pipeline.engine.stage5_review_gate \
  --workspace research_pipeline/experiments/reconstruction-v1-recovery --audit
```

New screened link batches go into `intake/stage5-curated-batch-03.jsonl` and subsequent files. For locally checked intake:

```bash
python -m research_pipeline.engine.stage5_review_gate \
  --workspace research_pipeline/experiments/reconstruction-v1-recovery \
  --apply-batch research_pipeline/experiments/reconstruction-v1-recovery/intake/stage5-curated-batch-03.jsonl
```

New **individually researched** no-link or unresolved-ambiguity decisions go into `intake/stage5-disposition-batch-02.jsonl` and subsequent files. Every row needs `formulation_id`, `decision` (`no_supported_target` or `held_ambiguity`), `editorial_reason` (at least 50 chars and mathematically specific), `reviewed_by`, `human_verified:false`, plus an exact `source_text` (or programmatically computed `source_text_digest`):

```bash
python -m research_pipeline.engine.stage5_review_gate \
  --workspace research_pipeline/experiments/reconstruction-v1-recovery \
  --apply-dispositions research_pipeline/experiments/reconstruction-v1-recovery/intake/stage5-disposition-batch-02.jsonl
```

GitHub Actions workflows run the same commands on committed batch files and commit the renewed ledger/checkpoint. A submitted batch is **not complete** until its workflow-generated records and checkpoint are visible in GitHub.

**Stage 5 cannot seal while any of the 431 formulation reviews has `needs_review`.** When all are genuinely dispositioned, run `--audit`, then `--seal` and inspect the resulting digest. Only then proceed to Stage 6: publication of an isolated prototype (not the production Pages site), inspection, and a second-wave research/freeze before any comparison against the original corpus.

**Next task: Stage 5 further semantic linking and explicit coverage reviews — recommended thinking effort High.** Preserve short batch checkpoints and resume from the exact set of pending formulation IDs rather than rerunning the sealed source or meaning stages.
