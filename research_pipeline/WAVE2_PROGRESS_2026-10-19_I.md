# mathDef independent reconstruction — Wave 2 checkpoint I (2026-10-19)

**Latest verified committed Wave 2 milestone** (check main and exact Actions run results when resuming): source-to-review checkpoint `51a25b7b90c90192626b589c09441f46260e85e5`. This supersedes H for current counts; H remains a historical source and mathematical provenance record.

## Current independently verified status

| Component | Verified |
| --- | ---: |
| Approved source registrations | 9 |
| Source term/heading records | **366** (318 frozen Wave 1 + 48 Wave 2) |
| Individual source observations | **789** (749 Wave 1 + 40 Wave 2) |
| Screened contextual meanings | **469** (419 Wave 1 + 50 Wave 2) |
| Individually reviewed formulations | **481** (431 Wave 1 + 50 Wave 2) |
| Source-anchored screened definition-uses links | **623** (445 frozen Wave 1 + 178 Wave 2) |
| Current link dispositions | **471 linked, 10 no suitable screened target, 0 held, 0 pending** |
| Wave 2 stages sealed | **none** |

The ten no-target reviews are mathematically accounted for, not evidence that the source research is completed. Their missing prerequisites are explicit; six new ones involve calculus and orthogonal-polynomial concepts. A linked formulation can still need other cross-definition links. No human peer verification or comparison against the original production corpus is claimed.

## New verified workflows and mathematical work

1. [DLMF/OpenStax direct-source intake 39320835714](https://github.com/Zengez/mathDef/actions/runs/39320835714): **success**, 363→366 source terms and 786→789 observations, versioned preservation of all 363 prior source decisions. Only original brief mathematical paraphrases were added; source rights remain locator-only.
2. [Seven mathematical meaning screens 39321425178](https://github.com/Zengez/mathDef/actions/runs/39321425178): **success**, 462→469 meanings and 474→481 reviews, immutable snapshot of all 474 historical reviews, 622 existing links unchanged. Four distinct DLMF orthogonal-polynomial contexts (weighted interval, countably infinite discrete, finite discrete, admissible Lebesgue–Stieltjes measure); real antiderivative and indefinite-integral contexts; and epsilon-delta punctured-neighborhood real limit. The disconnected-domain antiderivative constants and domain-relative limit source gap remain explicit.
3. [Indefinite-integral prerequisite 39321749946](https://github.com/Zengez/mathDef/actions/runs/39321749946): **success**, one exact-source-anchored `indefinite integral → antiderivative` link, 622→623 total, with no cycles.
4. [Six independent missing-foundation reviews 39322085753](https://github.com/Zengez/mathDef/actions/runs/39322085753): **success**, six formulation-specific no-supported-target decisions with missing prerequisites; original 481-review snapshot and all 623 links preserved. Result **471 linked + 10 no target + 0 pending**.

Evidence is individually preserved in:
- `experiments/reconstruction-v2-independent/wave2/direct_source_research_dlmf_openstax_definition_variants_2026-10-19.jsonl`
- `intake/foundations_batch_19_{terms,observations}.jsonl`; `wave2/foundation_source_discovery_batch_19.jsonl`
- `wave2/foundation_meaning_review_batch_20.jsonl`; `state/wave2_analysis20_meaning_screen.json`
- `intake/wave2_curated_relations_batch_19.jsonl`; `state/wave2_link_review_batch_19.json`
- `wave2/analysis20_remaining_mathematical_dependency_decisions.jsonl`; `events/wave2_analysis20_no_target_reviews.jsonl`
- `state/wave2_analysis20_dependency_reviews_complete.json`
- Historical snapshots `state/wave2_term_coverage_snapshot_363.jsonl`, `state/wave2_formulation_reviews_snapshot_474_before_analysis20.jsonl` and `state/wave2_formulation_reviews_snapshot_481_before_analysis20_dependency_reviews.jsonl`.

## Updated original priority backlog

The original fixed 192-item priority list remains immutable. All **93/93 original missing-target or ambiguity relationship cases** have at least one screened link, but this does **not** imply exhaustive prerequisites. The other **99 original source/variant/collection research cases** are **not fully demonstrated complete**.

A new individually grounded assessment of these 99, without false completion claims, is committed at `state/wave2_original_source_priority_progress_2026-10-19.jsonl` plus summary JSON:
- **4** original field-theory cross-source variants have source/math comparisons; one required a prior independently audited Stacks characteristic-specific correction. These are not automatically merged.
- **9** original source-collection entry routes were individually assessed: 6 have at least partial usable indexes/entry routes, while 3 have access, JavaScript or content-observation limits. **None of the nine collections is exhaustively surveyed.**
- **27** original access-blocked acquisitions and **59** unproductive-definition-section tasks remain without demonstrated resolution.

Collection-route evidence:
- `wave2/source_collection_partial_resurveys_2026-10-19.jsonl`: Stacks, ProofWiki, PlanetMath;
- `wave2/source_collection_remaining_route_assessments_2026-10-19.jsonl`: NIST DLMF, OpenStax, MathWorld, MIT OCW, AMS MathSciNet, EoM.
- EoM direct fetches still fail with HTTP 502. Do not bypass access limits or copy restricted content. MathSciNet frontend is JavaScript-dependent and its source rights remain unknown.

The generic 3,599 exploratory leads are unexhausted opportunities, **not** a count of missing definitions.

## High-thinking next tasks

1. Independently research source-grounded foundations needed by the new reviewed no-target cases: **derivative, polynomial degree, weighted sums and integrals, Lebesgue–Stieltjes measure and finite moments, real absolute-value metric, punctured neighborhoods and mapping/function formalization**.
2. Preserve source-specific mathematical variants: DLMF interval/countable/finite/measure orthogonality are *different source conventions and support hypotheses*; OpenStax F+C uniqueness uses a connected interval, not arbitrary disconnected domains; relative-domain limit must be sourced separately before screening.
3. Reconsider the original 27 blocked and 59 unproductive source cases using **independent accessible sources only**, logging each attempt and why a page is or is not a definition. Do not relabel a different source as an inaccessible original.
4. Keep the per-source evidence and individual mathematical ledger snapshots, test all workflows and commits, and update fixed-denominator coverage without treating partial checks as full completion.
5. **No stage seals and no production comparison** until independent Wave 2 source and contextual-review coverage have been appropriately assessed.

Frozen Wave 1 directory `research_pipeline/experiments/reconstruction-v1-recovery/`, publication digest `7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801`, is unchanged. The original live mathDef definition/variant/citation corpus has not been consulted in this Wave 2 continuation. No user action is needed.
