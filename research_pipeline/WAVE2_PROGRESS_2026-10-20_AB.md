# Independent mathDef Wave 2 — verified checkpoint AB (2026-10-20)

**Fast restart:** [portable RESUME_STATE.json](experiments/reconstruction-v2-independent/state/RESUME_STATE.json), [adapter resume plan](adapters/mathdef/resume_plan.json). Supersedes checkpoint AA for the latest counts/next action; prior source reviews and mathematical decisions are preserved.

## Verified Batches 135–138 — convexity, falling factorial, numeric Kronecker delta, bipartite graphs

All four sequential workflows completed successfully with independent frozen Wave1 checks, historical formulation review preservation, regression tests, source-specific mathematical verification and noncircular dependency checks.

- **Batch135 — source intake:** [success run 39529138225](https://github.com/Zengez/mathDef/actions/runs/39529138225). Four directly read ProofWiki source headings and **seven individual source observations** covering [Convex Set (Vector Space)](https://proofwiki.org/wiki/Definition:Convex_Set_(Vector_Space)), [Falling Factorial](https://proofwiki.org/wiki/Definition:Falling_Factorial), [Kronecker Delta](https://proofwiki.org/wiki/Definition:Kronecker_Delta), and [Bipartite Graph](https://proofwiki.org/wiki/Definition:Bipartite_Graph). Important independent corroboration: ProofWiki Falling Factorial states its definition for positive integer n only; [Binomial Coefficient with Zero](https://proofwiki.org/wiki/Binomial_Coefficient_with_Zero) separately explicitly establishes the vacuous product x^{underline 0}=1, so extending to n=0 is not falsely attributed to the restricted source.
- **Batch136 — mathematical screening:** [success run 39529315377](https://github.com/Zengez/mathDef/actions/runs/39529315377). Four screened contextual meanings and **seven mathematical formulations**. Pairwise and Minkowski-set convexity are equivalent within one real-vector-space meaning. Piecewise numerical equality indicator and Iverson equality bracket are equivalent within one Kronecker-delta meaning. Cross-part-edge and proper two-coloring with **non-surjective** coloring allowed are equivalent within one simple-graph bipartiteness meaning. The falling factorial is one nonnegative-index real polynomial product with the separately sourced zero convention. All 632 historic formulation reviews and 869 links were preserved.
- **Batch137 — individual mathematical links:** [success run 39529548233](https://github.com/Zengez/mathDef/actions/runs/39529548233). **Fourteen** directly screened and attributed mathematical prerequisites, linking seven new forms to independently sourced vector-space structure, subset inclusion, real field, zero-inclusive natural numbers, typed mappings and simple undirected graph as appropriate. All 869 older links and 632 unrelated individual review decisions preserved. Zero cycles; all 639 forms dispositioned.
- **Batch138 — retroactive prerequisite recovery:** [success run 39529729911](https://github.com/Zengez/mathDef/actions/runs/39529729911). **Four** separate links from previously screened Stirling and convex-hull definitions to the newly source-screened prerequisites: Stirling recurrence → numeric Kronecker delta; Stirling falling-factorial coefficient characterization → falling factorial with n=0; convex-hull intersection-of-convex-supersets and least-convex-superset definitions → convex subset of real vector space. All **883 prior links and 639 individual reviews and rationales preserved**. Only four new relation IDs appended to the four specific older formulations. No cycles.

## Current independently committed totals

| Registry | Count |
| --- | ---: |
| Approved independent source collections | **14** |
| Independently attributed source headings | **481** |
| Individual external source observations | **953** |
| Mathematically screened contextual meanings | **595** |
| Individually reviewed mathematical formulations | **639** |
| Individually sourced screened prerequisite relationships | **887** |
| Formulation reviews | **633 linked / 6 justified no-supported-target / 0 pending** |
| Directed dependency cycles | **0** |
| Sealed Wave2 stages | **0** |

Frozen independently reconstructed Wave1 publication digest: **7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801**. **Original production mathDef mathematical definitions, variants and citations never accessed or compared.** Mathematically reviewed against directly read sources and automated checks, not independent expert human peer review.

### Important mathematical/sourcing distinctions preserved

- A convex subset of a real vector space may be empty; topological closedness and finite dimensionality are not assumed. Convex hull need not be a *closed* convex hull.
- Falling factorial uses the real product x(x−1)…(x−n+1) for n>0 and separately sourced **empty-product x^{underline 0}=1**, essential for the k=0 Stirling term. This is not a rising factorial or an unqualified factorial quotient.
- Numeric Kronecker delta δ(a,b) is {0,1}-valued equality indicator, not the more general ring-valued symbol without a codomain convention, nor Dirac delta.
- A bipartite simple graph may have an empty color class (edgeless graphs and the empty graph included); two-colorability does not require both colors to be used and does not imply complete bipartiteness.
- Source-quality issue: incident-edge and unique-neighbor degree counts are equivalent only in simple loopless graphs, not arbitrary multigraphs.
- All **three previous suspect source observations stay held and excluded** from screened mathematical meanings: gradient-existence-only directional derivative, forward-edge-only graph isomorphism, and incorrectly indexed uniform-convergence series partial sum.
- Other inherited warnings: ProofWiki boundary/exterior source defect excluded, uncited division-ring pair source, inaccessible 8 Encyclopedia of Mathematics locators and 27 PlanetMath original pages, and original first-pass 192 prioritized terms are not exhaustive coverage.

### Detailed new evidence

Relative to research_pipeline/experiments/reconstruction-v2-independent:

- wave2/convex_falling_delta_bipartite_source_batch135_2026-10-20.jsonl
- state/wave2_bridge135_source_intake.json
- wave2/bridge136_individual_mathematical_reviews.jsonl
- state/wave2_bridge136_meaning_screen.json
- wave2/bridge137_individual_source_screened_links.jsonl
- state/wave2_bridge137_link_review.json
- wave2/bridge138_individual_backfill_links.jsonl
- state/wave2_bridge138_retroactive_links.json
- Immutable 632/639 review snapshots and exact stage input files. Previous [checkpoint AA](WAVE2_PROGRESS_2026-10-20_AA.md) documents Batches132–134.

## Next bounded work — Batch139

Resume **independent mathematical breadth** beyond convexity, Stirling numbers, Bell numbers and bipartite graphs. Candidate directly sourced areas: affine geometry (differentiate affine from convex hull), probability independence, linear-algebra matrix trace, graph cycles, or number theory congruences. Check current independently screened mathematical meanings and source locators for collisions first. Only mathDef adapters encode mathematical policy; generic research engine remains topic-neutral and portable to future theorem and math-education terminology projects.

Keep the reconstructed Wave1 frozen, all five Wave2 stages **UNSEALED**, and avoid production-original comparison until the independent reconstruction is independently frozen. Keep the source-only → mathematical-context → individual-direct-prerequisite workflow and a bounded 12–14-minute session followed by a verified portable checkpoint.
