# First-generation research checkpoint — 2026-10-26

**Status:** ongoing independent Wave2 source-backed research; research evidence is not mathematical certification, provisional population admission, candidate resolution, publication, or a release freeze.

## Binding project state

- Repository: `Zengez/mathDef`, draft [PR #19](https://github.com/Zengez/mathDef/pull/19), research branch `research/wave2-firstgen-b01-source-evidence-2026-10-26`.
- Live independent graph on `main` previously verified `phase=research_missing_dependencies` and `consolidation_gate_valid=true` following [PR #18](https://github.com/Zengez/mathDef/pull/18) automation.
- Frozen first-generation manifest: `research_pipeline/experiments/reconstruction-v2-independent/generation_staging/MANIFEST.json`.
- The manifest pins inventory `34f61b6cf7fd1e80bda932dc8eeac473a729b11dfa0ba849c6db424b7a8f8113` and unresolved fingerprint `7b69e2fdcb30a4536883df44308d386219b7621533886d65276b8992959f4773`.
- Original cohort: **418 canonical candidates covering 841 effective missing occurrences**; no recursively added prerequisite candidates in this milestone.

## Completed source-research evidence

| Original priority | Review artifact | Candidate count | Original occurrences |
| --- | --- | ---: | ---: |
| 001–007 | `BATCH01_SOURCE_EVIDENCE_001_007.json` | 7 | 166 |
| 008–020 | `BATCH01_SOURCE_EVIDENCE_008_020.json` | 13 | 92 |
| 021–040 | `BATCH02_SOURCE_EVIDENCE_021_040.json` | 20 | 89 |
| 041–060 | `BATCH03_SOURCE_EVIDENCE_041_060.json` | 20 | 61 |
| 061–080 | `BATCH04_SOURCE_EVIDENCE_061_080.json` | 20 | 43 |
| 081–100 | `BATCH05_SOURCE_EVIDENCE_081_100.json` | 20 | 40 |
| 101–120 | `BATCH06_SOURCE_EVIDENCE_101_120.json` | 20 | 40 |
| 121–160 | `BATCH07_SOURCE_EVIDENCE_121_160.json` | 40 | 52 |
| 161–200 | `BATCH08_SOURCE_EVIDENCE_161_200.json` | 40 | 40 |
| **Total** | **9 committed review documents** | **200 / 418** | **623 / 841** |

Checked all nine committed files for stable, unique candidate IDs, matching original counts and nonempty source evidence: exactly **200 distinct IDs** and **623** represented original references. The source evidence ranges from directly supported definitions to explicitly labeled partial or context-dependent source verifications. No claim that all 200 are mathematically certified or that all locators are fully independently checked.

## Important mathematical holds and typing boundaries

- **Unrestricted category/functor/groupoid:** Stacks Project 4.2 explicitly defaults to set-sized categories and detailed groupoids; a context-unrestricted definition still needs a specified class/universe foundation. Do not alias to small category or small groupoid solely on matching words.
- **Quotient ring vs quotient module vs localization:** these are genuinely different constructions; preserve exact objects and additional multiplication assumptions.
- **Quotient topology:** explicit surjectivity of a quotient map into its quotient space is different from a final topology on a larger target that may not be surjected onto.
- **Prime contraction:** `p=R∩q` is notation for inverse image under a ring map even if the map is not injective, according to Stacks section 10.2.
- **Polynomial quotient as a field:** `F[x]/(f)` is a field for an irreducible nonconstant `f`; a general nonconstant reducible `f` yields only a quotient algebra. The root class of `x` still makes sense in the quotient ring. Existing source-free correction proposal remains unapplied.
- **Monic constant polynomial and zero ring:** the statement that constant `1_R` is a *nonzero* degree-zero monic polynomial requires `R≠0`, but generic nonzero-polynomial monicity need not globally disallow the zero ring.
- **Formal unramified:** “at most one” lift differs from formally smooth existence and formally étale existence+uniqueness; not synonyms.
- **Clopen subsets:** generic simultaneously closed-and-open predicate is not the idempotent-classification theorem for `Spec R`. The existing accepted contextual meaning is a theorem/property form rather than automatic candidate identity.
- **Integrability and almost-sure equality:** per-time `E|X_t|<∞` does not imply uniform-in-time moment bounds; almost-sure equality is not literal pointwise equality on all outcomes.

## Precisely what remains

- **218 original candidate identities** have not yet received this first-generation source-evidence pass. They represent **218 effective incoming references** from the original frozen cohort.
- Begin next with original priorities 201–240 from the frozen `MANIFEST.json`. Reuse the concise per-candidate representation, compare source assumptions and context, and defer new dependencies. Do **not** return to broad source-free alias cycles.
- Continue creating immutable evidence files with exact original IDs, full original context, occurrence IDs and provenance, source URLs+sections, proof/counterexample where mathematical relevance depends on edge cases, accepted/provisional comparison outcomes, and uncertainty statuses.
- **Separate next workstream:** translate genuinely source-supported, context-reviewed records into `generation_staging/records/` using `research_pipeline.engine.dependency_generation` and its strict version/previous-staged comparison preflight. The four evidence files **are not themselves stage submissions**. Validate the full accepted and provisional independent corpora and every previously staged candidate before an actual provisional intake.
- After one full 418-candidate source-research generation, do the deeper global variant/equivalence/source audit and reviewed integration; new prerequisites belong to the *next* generation, not this one.
- Avoid original production mathematical corpora and frozen Wave1 entirely. Do not merge unrelated draft PRs or change current graph/production meanings during research.
- Codex cost reserved for verified large engineering efficiency multipliers; none required yet.

## Operational checks at this checkpoint

- Initial source review artifacts: all nine saved to draft PR #19, **200 unique canonical candidate IDs**.
- Graph gate: was previously verified open on main; revalidate state before any intake action.
- Existing mathematical population / resolution applied: **none by these review commits**.
- No claim of continuing to run after this response; resume from this checkpoint in a later conversation.

## Priority 61–80 addendum

The fifth research artifact `BATCH04_SOURCE_EVIDENCE_061_080.json` records 20 further original candidates with 43 incoming references. Stacks Section 10.89 (`https://stacks.math.columbia.edu/tag/059H`) provides the tensor-product/direct-product canonical map and concrete examples where it fails injectivity or surjectivity; injectivity for every family is an additional Mittag-Leffler property. Stacks Section 12.3 (`https://stacks.math.columbia.edu/tag/09SE`) supplies preadditive zero morphisms without requiring a zero object. Distinguish general vs open neighborhoods, arbitrary affine vs strictly positive convex combinations, and nonzero polynomial norms vs merely vanishing mixed integrals.

All five files compared with the frozen first-generation manifest yield **80 unique canonical IDs, exactly the first 80 in order, and 451 original occurrences**. Actual stage admissions remain separate, guarded and as yet unapplied. Next priorities: 81–100.

## Further October 26 continuation: priorities 81–120

Two more exact cohort-anchored source-review documents were committed:

- `BATCH05_SOURCE_EVIDENCE_081_100.json` — 20 candidates, 40 original occurrences. Verified primary references include Stacks Project §12.13 homology (`https://stacks.math.columbia.edu/tag/010V`), Stacks §6.11 stalks (`https://stacks.math.columbia.edu/tag/0078`), Stacks §26.5 affine structure sheaf (`https://stacks.math.columbia.edu/tag/01HR`), Stacks §26.10 local ideal sheaves (`https://stacks.math.columbia.edu/tag/01IN`), and Stacks §4.32 fibre categories (`https://stacks.math.columbia.edu/tag/02XG`). Some other locators and general-to-specialized scope require further checking; source statuses in the JSON distinguish them.
- `BATCH06_SOURCE_EVIDENCE_101_120.json` — 20 candidates, 40 original occurrences. Notable primary references include Stacks §26.21 diagonal (`https://stacks.math.columbia.edu/tag/01KH`), Stacks §12.13 quasi-isomorphism (`https://stacks.math.columbia.edu/tag/010Z`), Stacks §12.3 zero object (`https://stacks.math.columbia.edu/tag/0100`), and precise general measurable-map and topological pullback definitions from the cited sources. Several generic-category and infinite-sum sources are explicitly partial, pending exact scope confirmation.

**Exact aggregate verification:** seven artifacts, the first **120/418** frozen canonical candidate IDs in order, **531/841** original incoming reference occurrences, **298** candidates and **310** occurrences left for first-generation research. All IDs matched the original generation manifest without duplicates. These figures describe *source-evidence research coverage*, not mathematical verification, successful staged record admission, or release readiness.

### Version-anchored mathematical decisions to retain

1. **Indexed products:** nonemptiness of arbitrary products of nonempty factors uses Choice in ZF; the empty product is a singleton. This is a foundation/edge case, not a reason to alter the definition.
2. **Module isomorphism class:** unrestricted isomorphism classes may be proper classes. The original context concerns finitely generated modules, and that scope remains recorded.
3. **Open interval:** interior-point criterion alone does not define an interval; add order-convexity or the standard interval endpoint definition. Existing candidate context unmodified.
4. **Zero objects:** a zero object is initial and terminal. A preadditive category has zero morphisms even when it has no zero object.
5. **Orthogonality, moments:** for infinite weighted sums, ensure convergence. The zeroth moment k=0 requires finite total mass under the usual |x|^0=1 convention.
6. **Grothendieck construction:** strict contravariant functor orientation and variance differ from covariant/pseudofunctor conventions; manual source-context check still needed.
7. **Quasi-isomorphism:** induces isomorphisms on each homology group; this is weaker than a chain homotopy equivalence.

**Next:** continue original priorities 201–240 in the same bounded generation, then complete remaining candidates before the post-pass global mathematical consolidation and source-verification audit. Compare with existing independent accepted/provisional meanings and all newly staged research before a staged provisional entry; none was admitted through these evidence-only commits. No production/frozen Wave1 inspected and no Codex credits used.

## Latest 2026-10-26 continuation: one-reference throughput experiment (authoritative latest totals)

### Frozen queue shape

Of the 298 candidates remaining at the previous checkpoint, 287 had **one** originating reference, ten had **two**, and one had **three**. All 218 candidates remaining **after rank 200 are exactly single-reference**. Initial ranks 1–120 had 531 references among 120 candidates (4.425 references/candidate); the new ranks 121–200 have 92 references among 80 candidates (1.15 references/candidate). The reduction in contextual inspection is real; mathematical source discovery and source scope verification remain candidate-by-candidate.

### Larger-batch pilot

Two 40-candidate source-evidence files have been committed and individually manifest checked:

- `BATCH07_SOURCE_EVIDENCE_121_160.json`: **40 distinct original candidates**, 52 original references; source leads are separately labeled, several exact Stacks/MathWorld passages directly verified.
- `BATCH08_SOURCE_EVIDENCE_161_200.json`: **40 distinct original candidates**, 40 original references; full original context, reference occurrence ID, preliminary meaning, source locator/qualification, assumptions and relation flags retained.

New cumulative tally: **200/418** candidates and **623/841** original missing-reference occurrences have preliminary source-research review records. **218 candidates and 218 references remain, all singletons.** All 200 reviewed canonical IDs were checked in exact order against the frozen `generation_staging/MANIFEST.json` with no duplicates or missing ranks.

**Practical result:** Batches of about 40 are feasible for the initial typed mathematical/contextual-source-lead pass and reduce bookkeeping/interaction overhead, but it would be misleading to call this a doubling of *fully source-verified* research throughput. A verified reference still needs actual passage and scope checking for each candidate; a substantial proportion of the new records are explicitly marked `source_lead`, `exact_locator_pending` or `context_review`. Never silently promote them to source-verified or accepted definitions. Prefer batching **40–60 singletons** for first-pass collection with individual source-grade statuses, and reserve a separate slower direct-source-verification/consolidation pass before stage admission.

### Newly detected mathematical issues to resolve before integration

- **Sheaf support (priority 151):** Support of `O_X/I` means nonzero stalks; arbitrary sheaf support need not be closed. Stacks [Lemma 29.5.3](https://stacks.math.columbia.edu/tag/056J) directly proves closed support for *finite-type quasi-coherent* modules. Review the exact ideal-sheaf hypotheses before claiming support gives a closed subspace.
- **Lebesgue–Stieltjes measure (priority 166):** A bare bounded nondecreasing function need not be right-continuous; the standard assignment `μ((a,b])=F(b)-F(a)` requires appropriate right-continuity, or a different interval convention. Record as substantive convention, not a harmless spelling difference.
- **Residue-field inclusion (priority 191):** An injection `Λ/(Λ∩m)→R/m` need not be surjective. Calling it an isomorphism requires an additional assumption (and `Λ∩m` maximal to ensure source is a field).
- **Braiding (priority 187):** Natural exchange isomorphisms must satisfy hexagon/coherence conditions to make a braiding. Symmetry further requires double exchange to equal the identity.
- **Finite multigraph multiplicity (priority 154):** Pairwise edge-copy multiplicities are finite integers only under local finiteness of parallel edges; unrestricted multigraphs can have infinite multiplicities.
- **Ore/cancellation conventions (priorities 152,193):** Two-sided localization axioms have typed left/right arrow direction conventions, not generic categorical cancellation.
- **Zero-ring/division-ring degenerate case (priority 197):** Retain specified `1≠0` where needed to avoid vacuous field/division-ring characterizations, and append to owner-approved edge-case-assumption review ledger when actual mathematical population is edited.

### Direct source verification spot checks

Directly inspected [Stacks Remark 4.14.5](https://stacks.math.columbia.edu/tag/0G2U) for cocones and span cocones (122, 140); [Definition 5.10.1](https://stacks.math.columbia.edu/tag/0055) for irreducible chains (126); [MathWorld factorial](https://mathworld.wolfram.com/Factorial.html) (135); [Stacks Lemma 29.5.3](https://stacks.math.columbia.edu/tag/056J) for scope-restricted closed support (151); [Stacks Remark 4.22.5](https://stacks.math.columbia.edu/tag/05PT) for pro-objects (177); [Stacks Section 111.18](https://stacks.math.columbia.edu/tag/027N) for catenary/chain context (189); [Stacks Section 5.12](https://stacks.math.columbia.edu/tag/0059) for closed points (200). The corresponding reviewed source entries have been upgraded explicitly; remaining source leads were not implicitly verified.

**Next:** continue first-generation 201–240 with qualified 40–60 candidate batching, preserving source-status precision and no recursive research. In parallel or in a dedicated later pass, validate preliminary source locators and perform complete accepted/provisional/staged-meaning comparison before using the guarded stage intake. No new source records have been committed to `generation_staging/records/`; the gate and original graph are unchanged. No Codex use.
