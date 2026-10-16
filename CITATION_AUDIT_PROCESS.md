# Citation verification ledger

This file describes the controlled **citation-specific** second-stage audit of mathDef. The [CSV ledger](CITATION_AUDIT.csv) contains exactly one row per existing definition file.

## Status semantics
- `pending`: no complete evidence-based citation review recorded for this phase. **Previous first-pass definition audits or source URL replacements do not imply verified status.**
- `verified`: the cited page/tag/section has been visited, the source actually defines or supports the displayed mathematical concept, and the key ambient hypotheses/conventions agree. Verification is **citation suitability**, not mathematical peer review.
- `corrected`: same as verified after updating an entry's citation or its mathematical wording to match an authoritative checked source. A commit trail should identify the change.
- `needs_followup`: citation unavailable, mismatched, incomplete or insufficiently specific, or an assertion in the definition remains unsupported; not counted as verified.
The `review_note` should identify the evidence (concept, page section, issue, or limitation); `checked_source` is the actual URL reviewed. CSV quoting rules apply for notes that contain commas.

## Rules
- A valid HTTPS URL and successful site build are only structural checks.
- Check the cited source itself. For arXiv, compare the precise locator against the **specified article version** and relevant statements.
- Retain stable definition IDs and subject-folder conventions. Do not change `status: draft` to `reviewed`: peer review is a separate process.
- Work in bounded batches, saving a tested Git commit and updating [WORK_CHECKPOINT.md](WORK_CHECKPOINT.md). Record objectively what was checked; do not infer progress from a topic-level sweep.
- Each batch may reveal new inconsistency, which can be fixed; unrelated term discovery, UI features and systematic rendering checks remain deferred.
- Ledger paths are the stable primary keys. When adding definitions only because they are invoked by existing definitions, add their rows with `pending`. Reconcile count against the current `definitions/` tree.

## Baseline
Created October 16, 2026. **1007 pending definitions initially**; prior exploratory citation improvements from the consistency/first-pass phases are recorded in `WORK_CHECKPOINT.md` and can inform priorities but are not blindly backfilled as verified.
