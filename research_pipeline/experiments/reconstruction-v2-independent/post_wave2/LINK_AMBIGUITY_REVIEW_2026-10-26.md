# Targeted link ambiguity follow-up — 2026-10-26

## Scope

This is a **direct review of the remaining ambiguous links to mathematical meanings already in the merged mathDef corpus**, not another scan for terms or a reopening of the original frozen candidate queue. The 2,019/2,019 terminology candidates remain completely dispositioned. No new mathematical definitions, labels or aliases were discovered or added.

Sources: the exact existing candidate link references, their surrounding original definition passages, the catalog's existing mathematical meaning variants, and existing cited original/mathDef source definitions. Choice rules live in `research_pipeline/adapters/mathdef/merged_linking.py` and affect only the merged-site generated display. The independent Wave2 (958 meanings), original mathDef (1,014), and post-Wave2 overlay (225) remain untouched.

## Results: 117 → 6 intentional ambiguities

| Metric | Prior linked-reference closeout | After scoped review |
|---|---:|---:|
| Combined searchable meanings | 2,197 | **2,197** |
| Definition formulations | 2,246 | **2,246** |
| New tentative links in merged output | 2,836 | **2,952** |
| Existing screened relations newly anchored inline | 259 | **248** |
| Formulations with positioned links | 1,706 | **1,732** |
| Ambiguous-context occurrences | 117 | **6** |
| Frozen terminology candidate dispositions | 2,019/2,019 | **2,019/2,019** |

The 111 no-longer-ambiguous occurrences were addressed through mathematically appropriate matches, source-specific rules, or suppression of false generic matches. They should **not** be described as 111 manually certified or 111 newly published mathematical definitions. The difference in the number of previously-screened relations newly positioned inline reflects the matcher's updated competition/selection behavior; those screened relations have **not** been deleted. The actual merged catalog and UI are built and validated by GitHub CI.

### Review decisions

- **Random variable (formerly 27 ambiguous occurrences):** Use the measurable-space-valued general definition for unspecified state spaces; in source passages explicitly specifying a *real random variable*, prioritize the real-valued version, without removing alternatives.
- **Foundational duplicate contexts:** Select representative formulations for demonstrably compatible meanings such as stochastic processes, discrete topology, successor ordinals, normal subgroups, full subcategories, coequalizers, valuation rings, quotient topology, projective modules, and more. Other variants remain searchable.
- **Mathematical scope-sensitive cases:** Distinguish discrete- and continuous-time martingales when the source fixes the index; distinguish a set's limit point from a sequence accumulation point; use the real/complex normed-space formulation for source passages with those scalars; choose order-theoretic suprema for the lengths of ideal chains and regular sequences; use the nontrivial zero-divisor convention in the zero-polynomial reference; and select the correct metric versus Euclidean norm closed ball.
- **False generic-phrase matches:** The words *open ball* inside *forward open ball* and *backward open ball* of a quasi-metric do **not** imply the usual symmetric-metric open ball. The matcher now suppresses precisely those two contexts, rather than linking incorrectly.
- **Substantive conventions:** Unqualified `ring homomorphism` may or may not include preservation of 1, and the source explicitly compares those conventions. We declined to guess.

### Six deliberately unlinked references

| Existing term | Occurrences | Why no meaning choice is justified |
|---|---:|---|
| Natural numbers | **3** | The source does not specify whether ℕ includes 0 or begins at 1; the existing definitions distinguish them. |
| Inner product space | **2** | The source doesn't fix real versus complex scalar field; both existing definitions are meaningful. |
| Ring homomorphism | **1** | The source explicitly discusses unital and non-unital conventions, rather than committing to one. |

These are **six source occurrences**, not six missing mathematical definitions or new candidates. They remain in `/reconstruction/merged/link-report.json`, with source excerpts and alternative meaning IDs for targeted suggestions. Community corrections are appropriate; no automated choice is required.

## Validation and closure

The complete merged site continued to build with 2,197 meanings, both independent search fields, and nested/inline expansion including ancestor-only cycle suppression. **19 Python regression tests** passed, and real Chromium browser checks passed for recursive expansion, sibling reuse, independent searches, mobile layout, and absence of runtime errors. Exact link source spans, target identities, and full original-frozen candidate dispositions are validated in CI.

**Status:** this follow-up is complete. No further obligatory review gate and no user intervention is required. New terminology discovery is a *separate future phase requiring explicit authorization*, not implied by closing the linking wave.
