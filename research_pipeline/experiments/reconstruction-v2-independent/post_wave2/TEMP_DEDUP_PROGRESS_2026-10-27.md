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

## Resume checkpoint — convention policy integrated (2026-10-27)

- Merged main's updated `AGENTS.md` and new permanent `DEFINITION_CONVENTIONS.md` into this branch via two-parent commit `3ef44734d597b2969fe8301f066af8dd77334944`. The cleanup branch now includes the policy **in Git history**, not only in conversation context.
- Source-scoped convention catalog: `data/math_definition_conventions.json`; actual evidence ledger: `data/math_source_convention_assessments.json`; Python resolver: `research_pipeline/adapters/mathdef/conventions.py`.
- Status logic: `verified_applies` enforces a verified source restriction at its scope. `checked_inconclusive`, `verified_opposite`, and `not_checked` inherit the **latest canonical mathDef meaning** as working editorial interpretation; evidence statuses remain distinct and no source endorsement is invented. No scores/reputation or correction event counts.
- Connected-space canonical meaning is the broad no-separation predicate; the Stacks-specific nonempty version is now consolidated into it with a citation and verified per-section restriction. Exact source evidence: Stacks Section 5.7, Definition 5.7.1(1), directly checked. The borrowed `connected component` formulation now explicitly says **nonempty connected subset** in a merged-only editorial text override; historical source text is unchanged, and its translation/evidence are recorded.
- Source ID granularity fixed: an independent Wave 2 citation may use a whole-work URL but its observation locator points to an exact Stacks tag. The registry uses the actual cited HTTPS locator as stable source identity, retains the parent work URL separately, and does not overextend a tag/section convention to all of Stacks.
- `research_pipeline/adapters/mathdef/stage_cleanup.py` produces unlinked structural snapshots directly from existing historical input and curated overlay, not from a new terminology scan. `.github/workflows/cleanup-stage-only.yml` checks this branch only, with no publishing or final relink.
- **Successful GitHub Actions stage-only run:** https://github.com/Zengez/mathDef/actions/runs/40529028568 — 8 Python tests passed. Baseline 2,197 meanings / 2,246 formulations / 2,048 term headings; after first 28 decisions: 2,169 meanings / 2,218 formulations, all term headings retained and 2,662 distinct precise source identities collected. (The 3,873 starting relations are the **pre-lexical stage-only graph**, not the already published 6,825-relation link graph; do not conflate.)
- Additional mathematically reviewed original/new consolidations subsequently recorded: **bijection, affine combination, measurable space, outer measure, prime number, probability space, real-valued random variable, sigma-algebra**. Total explicit decisions now **36**; a fresh stage-only test run is required to confirm latest results.
- Newly revisited distinctions **not** silently collapsed: rational number as a real fraction vs fraction-field construction; arbitrary vs nonempty metric space pending convention/source check; general vs real-valued random variables (real versions consolidated only); finite/nonempty chromatic number vs unrestricted including empty graph; zero-divisor inclusion of zero vs nonzero-only convention; algebraic-categorical versus module-only exactness.

### Remaining steps

1. Continue original/new shared-heading comparisons; new terms/candidate queues remain prohibited.
2. Log genuine uncertain cases with **all** current definitions for each heading in `TEMP_DEDUP_DECISIONS.md`.
3. Complete whole-corpus comparison and mathematical Subject coverage (first passed stage-only check covered 38/2169 subjects; most are still unassigned).
4. User review of uncertainty queue, **then and only then** run one global linking rebuild + audit/export/browser validation and publication review.

## Recovery checkpoint after conversation timeout — 2026-10-27 (AUTHORITATIVE LATEST)

**Do not resume from the obsolete 36-merge figure above.** A subsequent run
continued after that older checkpoint and committed 91 meaning decisions and 3
within-meaning form decisions before the conversation timed out. Those writes
are durable on the same branch.

**Current verified branch state:**
- Branch: `work/dedup-subject-context-sources-20261027`, not merged into main.
- Latest recovery integrity commit: `7c0d492c7d78d5b71b16e073687055800f6975bf`.
- **Successful stage-only CI:** https://github.com/Zengez/mathDef/actions/runs/40536084973 (includes post-timeout safeguards for historical original-ID coverage, relation endpoints, and source-registry IDs). Its immediate predecessor at the 91-decision checkpoint also passed: https://github.com/Zengez/mathDef/actions/runs/40534939034.
- Verified 8 Python tests pass. No final global linking rebuild, publication export, final link audit or website deployment from the cleanup branch.
- Initial pre-linking data: **2,048 groups, 2,197 meanings, 2,246 formulations**, 3,873 original/curated relations. The public previous fully linked site had 6,825 relations; the two counts refer to different pipeline stages.
- Staged survivors: **2,048 groups, 2,106 meanings, 2,152 formulations**, 3,798 stage-only relations, subject coverage **2,106/2,106**, zero missing.
- **91** explicit cross-meaning semantic consolidations; **3** reviewed trivial within-meaning formulation consolidations; **94** formulations removed overall. All 1,014 original definition IDs remain accessible as direct or explicit historical aliases; all surviving stage-only relation endpoints are valid.
- **41** explicitly reviewed retained multi-formulation groups in `data/merged_cleanup_retained_variants.json`; this is not a claim to have reviewed every group or every mathematical variant.
- Source registry compile yields **2,662** distinct precise source identities across all 2,048 term headings; sources use exact HTTPS locator/tag when available, preserving work URL and provenance distinction. The current source registry is generated by stage-only code, not yet wired to production or the v2 public feed.
- Subject and Context controlled registries are distinct; 100% mechanically/individually classified Subject coverage means schema completeness, **not** complete human certification of every mathematical classification.
- Canonical convention catalog records connectedness and subspace-topology boundary families. Actual evidence ledger has **one** verified Stacks §5.7 nonempty restriction, carefully scoped, plus tests for `checked_inconclusive` and `verified_opposite` dynamically inheriting the latest canonical meaning. Tests do not imply that those additional evidence assessments were collected from real sources.
- The connected-component nonempty wording translation is recorded in a merged-only override; original historical source input remains untouched.
- Genuine pending user decisions currently recorded with **all existing term formulations** in `TEMP_DEDUP_DECISIONS.md`: **Zero divisor** and **Metric space**. Additional uncertain cases may emerge from the unfinished whole-corpus pass.

**Safe next step, deliberately deferred to the next bounded research batch:** continue reviewing **unprocessed original/new shared headings first** and then research-only alternatives; do not restart the 91 approved explicit decisions, the 41 retained-variant checks, historical Wave2 work or old candidate discovery. Maintain both the pending user queue and the meaning/formulation ID alias ledger. Do not claim that the full corpus comparison is done.

**Phase gate remains unchanged:** obtain the user's opportunity to adjudicate *all* genuinely uncertain cases before the **one final** complete linking rebuild, full publication/feed consistency audit and website/browser validation. Neither source-scoring analytics nor public Sources UI has been implemented.

## Continued bounded original/new review — October 27, 2026

- Reconstructed original-versus-research inventory from verified stage-only CI: **101** shared headings. Before this batch, 97 had explicit merge/retained dispositions and 4 were untouched by decisions; of those four, two were already placed in `TEMP_DEDUP_DECISIONS.md` (metric space and zero divisor).
- Reviewed **Abelian category**: original statement already covers normal mono/epi criteria plus the Stacks coimage/image criterion; merge the redundant independent meaning into the original meaning, preserving its precise Stacks evidence and historical aliases.
- Reviewed **Filtration of sigma-algebras**: retain unrestricted ordered-index and discrete n≥0 variants; distinguish explicit Contexts `General ordered index sets` and `Discrete-time filtrations`, with Probability Theory as primary Subject.
- Added 6 further previously implicit retained-variant decisions for multi-meaning cross-cohort headings (binary operation, binary relation, Lipschitz continuity, open ball, random variable, ring homomorphism), in addition to filtration; no new candidate terminology.
- Following these changes, **99 of 101 original/new shared headings** have recorded clear deduplication or retained-variant dispositions; **2 remain intentionally uncertain** in the user queue. This figure refers to the shared-heading first pass only, **not** a completed full-corpus cross-title duplicate audit.
- Expected cumulative explicit meaning mergers **92** and same-meaning form mergers **3**, with 2,105 surviving meanings and 2,151 formulations, subject to stage-only CI. No global link rebuild or production deployment.
- Next batch: compare definitions under different existing searchable headings/aliases and check surviving multi-form meanings for semantically redundant duplicates, using a read-only prioritization audit. Do not reprocess the 99 adjudicated headings or revisit discarded Wave2 dependency graph work.
