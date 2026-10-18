> **Update (2026-10-18): CORRECTED FIRST-WAVE STAGE 3 AND STAGE 4 COMPLETE.** The historical narrative below explains the earlier incomplete state. Since then all 291 fetched Stacks section headings have received substantive mathematical decisions (**232 supported, 59 no suitable standalone definition**), 431 independently authored formulation candidates were recorded, and corrected Stage 3 sealed with 749 observations. Corrected Stage 4 also sealed with **419 context-labelled meanings / 431 formulations**, including 12 explicitly checked equivalent-definition groupings. The 27 PlanetMath entries remain blocked by robots-policy verification. See `experiments/reconstruction-v1-recovery/state/stage3_review.json`, `state/stage4_review.json`, and `IMPLEMENTATION_CHECKPOINT.md`. Stage 5 has not started; neither wave has been compared against production mathDef.

# Corrected Stage 3: per-term source acquisition and editorial evidence

**2026-10-18 — acquisition complete; mathematical review remains open.**

The first Wave 1 experiment incorrectly sealed Stage 3 after recording 318
source URLs and writing actual mathematical paraphrases for only 25 terms.
This was a **workflow design error**, not a finding that the other terms had
no definitions. The historical seals and their digests have deliberately been
preserved; the corrected research lives in a **separate versioned workspace**.

## Completed acquisition of all 318 sealed Stage 2 terms

The GitHub workflow `.github/workflows/mathdef-stage3-attempts.yml` actually
performed policy-checked, rate-limited HTTPS attempts against the term-specific
source URLs, not merely the Stage 2 alphabetical/chapter indexes.

- **318/318** terms have durable attempt records.
- **291** Stacks section pages were fetched and inspected for structural
  `Definition x.y.z` markers. **174** had at least one marker; **117** did
  not have an explicit marker detected.
- **27** PlanetMath term requests were denied by unavailable robots-policy
  verification. This is recorded as `policy_blocked`, **not** as a fetched
  article or a successful definition search.
- **Zero** terms are unattempted; **zero** fetching errors remained after
  permitted retries.
- No source definition passages were stored; only source locators, page
  SHA-256 checksums, section headings and definition-marker leads were
  retained. Marker identification **does not verify mathematical relevance**.

The durable acquisition results are:

- `experiments/reconstruction-v1/state/stage3_acquisition_attempts.jsonl`
- `experiments/reconstruction-v1/state/stage3_acquisition_report.json`

The script `research_pipeline.engine.stage3_attempts` enforces one source
record per sealed term ID, confirms source host and source catalog digest,
records whether a real page was fetched, checkpoints every term, and refuses
to pass a full-coverage check with an unattempted or retryable-failure term.
The GitHub workflow commits its ledger in bounded batches, rebases on
unrelated repository updates before pushing, and also uploads an artifact
if the job fails. The page fetcher caches reviewed robots policies only
within the current process and does not bypass missing policies.

To verify the completed acquisition:

```sh
python -m research_pipeline.engine.stage3_attempts \
  --workspace research_pipeline/experiments/reconstruction-v1 \
  --ledger research_pipeline/experiments/reconstruction-v1/state/stage3_acquisition_attempts.jsonl \
  --report research_pipeline/experiments/reconstruction-v1/state/stage3_acquisition_report.json \
  --verify-only
```

## Corrected research workspace (do not overwrite original)

`research_pipeline/experiments/reconstruction-v1-recovery/`

Created by the success-gated `mathdef-stage3-recovery-fork.yml` workflow.
It preserves the independently discovered Stage 1 and Stage 2 registries,
carries forward the 349 previously collected observations as **unsealed
candidates**, and records where they came from. It does **not** copy the
earlier 31 sealed Stage 4 meanings, which reflected prematurely truncated
research.

Relevant files:

- `project.json`: two new mandatory gates,
  `require_full_definition_attempts` and
  `require_reviewed_term_dispositions`.
- `state/stage3_acquisition_attempts.jsonl`: every source attempt.
- `state/stage3_term_reviews.jsonl`: 318 per-term editorial work items.
- `state/stage3_recovery_lineage.json`: historical digests and recovery
  lineage.
- `records/observations.jsonl`: prior evidence, unsealed for expansion.
- **No** `records/meanings.jsonl` has been carried forward.

After the acquisition workflow, **291 fetched-source terms are still marked
`needs_review`**. The 27 source-restricted PlanetMath terms are explicitly
`access_blocked` with their access reason; they remain unresolved.

## Mandatory completion gates

**Gate 1 — acquisition:** Every one of the sealed Stage 2 terms must have
a terminal source-acquisition outcome backed by a fetch or explicit policy/
retrieval restriction. Merely having a URL does not count.

**Gate 2 — mathematical editorial review:** Every fetched term must have an
explicit and documented disposition:

- `supported`: a reviewed, independently authored mathematical
  observation with correctly linked term and source, plus reviewer and
  mathematical rationale.
- `no_suitable_definition`: source read and an adequately reasoned
  editorial finding that no suitable definition was located.
- `access_blocked`: a documented policy or retrieval obstacle, without
  pretending that the mathematical content has been examined.
- `needs_review`: pending. **Prevents sealing Stage 3.**

The code cannot independently perform semantic mathematical verification;
reviewers/ChatGPT must examine the actual pages and develop rigorous
formulations. `research_pipeline.engine.stage3_review_gate` generates the
queue and enforces its completeness. The core `Workspace.seal` function
applies **both gates** for Stage 3 and downstream Stage 4/5 in this corrected
workspace. The corrected `stage3_finalize` removes the former hardcoded
31-paraphrase target, and Stage 4 uses dynamic supported-term counts rather
than expecting exactly 31 meanings and 32 formulations.

The manual-only `mathdef-stage3-seal.yml` and
`mathdef-stage4-meanings.yml` workflows now target **only the recovery
workspace**. They cannot simply rerun the old 25-term batches and declare
success. Old sealed results remain available as a reproducible audit
checkpoint and are not falsely described as complete research.

## Next research step

Continue real mathematical research across the **291 pending fetched-source
term entries** (many contain several definition marker links). Cross-check
source-specific objects/conditions, author paraphrases, identify genuinely
different variants, and record a reviewed disposition for each term. Keep
the 27 robots-blocked PlanetMath cases explicit; do not bypass access
restrictions. Only then run Stage 3 seal, proceed with Stage 4 context
classification, and eventually Stage 5 cross-links.

This completes the **workflow repair and initial acquisition attempts**,
not the mathematical research needed to complete Stage 3 itself.
