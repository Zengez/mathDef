# Wave 2 independent reconstruction — execution recovery checkpoint F (2026-10-19)

**Read first, then inspect the latest main SHA and GitHub Actions; this report is a point-in-time checkpoint, not an assertion that queued jobs succeeded.**

Supersedes execution status in `research_pipeline/WAVE2_PROGRESS_2026-10-19_E.md`, which still contains detailed sources, rationale and fixed-baseline research progress. Nothing from the original production mathDef definitions/variants/citations has been used or compared.

## Last fully verified persisted state

- 9 independently approved sources, **343** source headings, **766** observations.
- **435** screened contextual meanings, **447** individually dispositioned formulations.
- **545** screened definition-use relationships: 445 immutable Wave 1 + 100 new Wave 2.
- Current formulation reviews: **419 linked**, **22 no-supported-target**, **2 held ambiguity**, **4 new needs_review**.
- All five Wave 2 stages **UNSEALED**.
- Frozen Wave 1 at `research_pipeline/experiments/reconstruction-v1-recovery`, publication digest `7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801`.

Corrected four-Stacks-meaning screen (field, functor, groupoid, pseudofunctor) was committed `10bd29c1a2493a` with `state/wave2_new_foundations_batch_06_screened.json`. A failed first screening run exposed a pseudofunctor ID key mismatch; it was corrected without relabeling its separately observed source. The final code and 435-meaning corpus are committed.

## Fixed-backlog progress, before new links

The original 192-priority task queue is immutable. **72/93 (77.4%)** initial prerequisite/ambiguity cases now have at least one independently screened link; 21 lack one. In addition 99 initial source/variant/collection tasks are not proved complete. **120/192** original priority tasks therefore lack demonstrated full completion by this conservative metric. This does not assume complete discovery of all mathematical definitions; 3,599 generic discovery leads are neither 3,599 verified missing definitions nor automatically complete.

`research_pipeline/engine/wave2_priority_progress.py` computes the fixed-baseline overlay from audited formulation/relation ledgers, without changing any original queue rows.

## Important execution correction: GitHub workflow_run chain depth

GitHub Actions cannot reliably trigger more than **three chained** `workflow_run` levels. The previously designed A→B→C→D→E→F dependency chain was too deep. Moreover the older post-screening link workflows [39283843058](https://github.com/Zengez/mathDef/actions/runs/39283843058) and [39282739306](https://github.com/Zengez/mathDef/actions/runs/39282739306) were **skipped**, not successful. No 18-link report or 563-link state was committed by them.

**New authoritative execution path:** `.github/workflows/mathdef-wave2-sequential-foundation-reviews.yml` created by `48e32b4088bd63193eb2150e4e6e807557be5e13`, automatically queued as [GitHub Actions 39285610846](https://github.com/Zengez/mathDef/actions/runs/39285610846). It runs in `mathdef-independent-wave2-writes` concurrency group and performs six strictly ordered stages with independent per-stage checks and **GitHub commits after every stage**:

| Stage | Guarded task | Expected if all prior stages pass |
| --- | --- | --- |
| A | 18 individual Stacks context/source links in `intake/wave2_curated_relations_batch_06.jsonl`; all four newly screened meanings are prerequisite to processing | 435 meanings, 447 formulations, **563 links** |
| B | Four ProofWiki source-only observations for monoid/binary operation/binary relation/Cartesian product; archive 343-term reviews | **347 terms, 770 observations** |
| C | Six individually screened mathematical contexts (including two operation conventions and two relation conventions), version 447 historical formulation decisions | **441 meanings, 453 formulation reviews**, 563 links |
| D | 11 exact-phrase reviewed elementary mathematical links; graph-cycle checks and historical source review preservation | **574 links**, one Cartesian-product formulation may still need no-target research |
| E | Three independent set/mapping observations from ProofWiki: ordered pairs, subset, total map versus typed/bare graph; archive 347-term reviews | **350 source terms, 773 observations**, meanings/links unchanged |
| F | Rebuild conservative priority backlog reconciliation; verify frozen Wave 1 digest and all prior reviewed links | **192** original priority overlay rows; all Wave 2 stages remain unsealed |

**These counts are future conditional outcomes only.** As of this checkpoint, run [39285610846](https://github.com/Zengez/mathDef/actions/runs/39285610846) was **queued**, and the last committed screened link count remained **545**. Do not count 563/574 links or 347/350 sources until their exact on-main committed reports and workflow stage logs verify success.

The sixth-stage execution plan uses a single workflow job and per-stage commit checks, avoiding the GitHub `workflow_run` chaining limit. The old dependent workflow files remain as historical evidence, but their triggers are not a reliable substitute for the new sequenced orchestration.

## Another edge case fixed

Previously, a newly constructed (not inherited Wave 1) foundation formulation could be individually reviewed as `no_supported_target`, but the link-ingest engine would reject *any* later justified link because `original_wave1_disposition` was null. Patch `a77853a8289f052483c4d714122458a21f01c27d` now permits such an override **only** if its Wave 2 foundation-specific mathematical no-target review and original reason are explicitly present, there are no old links, and each incoming link is independently source-anchored. Inherited old-review constraints and historical override events remain mandatory.

## Research ready for post-execution

- ProofWiki direct article and source provenance: `wave2/direct_source_research_foundational_algebra_sets_batch_2026-10-19.jsonl` and `wave2/foundational_meaning_proposals_batch_07.jsonl`.
- ProofWiki set and function variants `wave2/direct_source_research_ordered_pairs_subsets_and_mapping_variants_2026-10-19.jsonl` with exact distinctions:
  - Kuratowski versus alternative ordered-pair encodings are equivalent coordinate representations, not literally identical sets;
  - `A⊆B` is non-strict;
  - `f:X→Y` as a total single-valued assignment versus typed graph `(X,Y,G)` with `G⊆X×Y`, versus bare graph `G` that does not independently specify its codomain.
- New source-intake engine `research_pipeline/engine/wave2_foundations_batch8_mapping.py`; source coverage handles `batch_08` and 350 terms. After it is executed, mathematically screen the mapping/ordered-pair variants **individually**, not by text matching.
- EoM's eight inaccessible pages remain unverified; 27 inherited source blocks, 59 original no-definition source outcomes remain pending.

## Resume procedure

1. Check exact run [39285610846](https://github.com/Zengez/mathDef/actions/runs/39285610846) and GitHub main recent commits. If workflow failed, fetch its **failed job logs and step**, fix the precise failure, and rerun using a changed workflow trigger or allowed rerun. Do not assume queued or submitted means successful.
2. Compare each expected stage report in `state/wave2_link_review_batch_06.json`, `state/wave2_foundations_batch_06.json`, `state/wave2_foundations_batch_07_screened.json`, `state/wave2_link_review_batch_07.json`, `state/wave2_foundations_batch_08.json`, and `state/wave2_priority_progress_current.json` to the exact committed record counts, source links, preserved snapshots, and frozen first-wave digest.
3. Once the last stage succeeds, continue independent source acquisition and mathematician-level context/variant work for mappings and ordered pairs, finite/infinite Cartesian products, remaining 21 original link gaps and source constraints.
4. Do **not** inspect or compare the original production corpus; only after Wave 2 is independently complete, rigorously freeze it and then compare.

**High thinking** recommended for source and mathematical decisions. No user input required for routine checkpoints.
