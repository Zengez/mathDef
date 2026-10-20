# Independent mathDef Wave 2 — verified checkpoint W (2026-10-20)

**Fast restart authority:** [compact RESUME_STATE.json](experiments/reconstruction-v2-independent/state/RESUME_STATE.json) and [adapter resume_plan.json](adapters/mathdef/resume_plan.json). Supersedes checkpoint V's current totals/next task without overwriting its historical source evidence.

## Batches 118–120 — normal subgroup, quotient group, graph isomorphism, analytic generating function

All three gated independent workflows completed successfully in GitHub Actions:

- **Batch 118 source-only** [successful run 39513931720](https://github.com/Zengez/mathDef/actions/runs/39513931720): Four directly read approved ProofWiki source definition headings and **seven** individually attributed source observations, one explicitly **quarantined** for mathematical inadequacy. Source pages: [Normal Subgroup](https://proofwiki.org/wiki/Definition:Normal_Subgroup), [Quotient Group](https://proofwiki.org/wiki/Definition:Quotient_Group), [Graph Isomorphism](https://proofwiki.org/wiki/Definition:Graph_Isomorphism), [Generating Function](https://proofwiki.org/wiki/Definition:Generating_Function). No meanings or links advanced in source-only stage. Source dossier: wave2/quotient_graph_generating_source_batch118_2026-10-20.jsonl.
- **Batch 119 mathematical screening** [successful run 39514135617](https://github.com/Zengez/mathDef/actions/runs/39514135617): Four mathematically screened contextual meanings, **six** individual formulations. The three normal-subgroup criteria are equivalent and share **one** meaning: gN=Ng, gNg⁻¹=N, and gNg⁻¹⊆N for *every* g∈G, with N already a subgroup. Quotient group G/N is defined for **normal** N with well-defined product (aN)(bN)=(ab)N, not a group structure on an arbitrary quotient set. Simple undirected graph isomorphism is vertex bijection **preserving and reflecting** adjacency. The ordinary real generating function is the real analytic sum of its coefficient series on its **real convergence domain**, not an unrestricted formal power series. All 600 historic formulation dispositions and 803 prior links retained.
- **Batch 120 individual source-to-prerequisite screening** [successful run 39514370092](https://github.com/Zengez/mathDef/actions/runs/39514370092): Eight exact independently screened mathematical prerequisites. Each of three normal-subgroup formulations → group; quotient group → normal subgroup; graph isomorphism → simple undirected graph and mapping; real ordinary generating function → real-number system and mapping. All six new formulations have individual completed decisions; all **803 earlier reviewed edges and 600 unrelated formulation decisions preserved**, graph remains **acyclic**. Three missing prerequisite-target candidates were explicitly recorded rather than fabricated: standalone subgroup definition, left group coset / coset product, and convergence of real power series. The source and mathematical context reviews are reproducible and leave unrelated engine code untouched.

## Independent mathematical source-quality discovery

**ProofWiki Graph Isomorphism page gives an insufficient one-way clause**: it states that for each edge of G there is an image edge in H under a vertex bijection, then calls this equivalent to both F and F⁻¹ being graph homomorphisms. That is not generally equivalent. Counterexample: V={1,2,3}, graph G has just edge {1,2}, H has edges {1,2} and {2,3}, and F is the identity bijection. Every edge of G is an edge of H but the inverse does not preserve H's extra edge, so the graphs are not isomorphic. **Held/quarantined** the source's one-way presentation as an observation, and admitted only the correct bidirectional edge-and-nonedge preservation condition. Distinct from earlier source-held ProofWiki directional derivative gradient-only expression, which remains excluded.

**Normality requires N already be a subgroup**, not merely a conjugation-invariant subset. The condition gNg⁻¹⊆N for all g implies equality by applying the condition with g⁻¹; does not require finite G. **Quotient group is not quotient set.** The coset product requires representative independence, ensured by N normal.

**Analytic versus formal ordinary generating functions:** the source explicitly defines the generating function where the real series converges; a formal power series with arbitrary real coefficients is a different contextual object and must be sourced independently before it is listed as an additional correct definition.

## Latest committed independent Wave 2 inventory

| Research registry | Count |
| --- | ---: |
| Approved independently accessible source collections | **14** |
| Attributed independent term/source headings | **461** |
| Individual source observations | **919**, including 2 separately held/questionable source observations |
| Mathematically screened contextual meanings | **572** |
| Individually reviewed formulations | **606** |
| Source-scoped mathematical prerequisite links | **811** |
| Formulation dispositions | **600 linked, 6 justified no-supported-target, 0 pending** |
| Dependency graph cycles | **0** |
| Sealed Wave 2 stages | **0** |

Frozen independent Wave 1 digest unchanged: \`7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801\`. Original production mathDef definitions, variants and citations **never consulted or compared**. This is mathematically screened source research, not human expert peer validation.

### Detailed new records

Relative to \`research_pipeline/experiments/reconstruction-v2-independent/\`:

- \`wave2/quotient_graph_generating_source_batch118_2026-10-20.jsonl\`
- \`wave2/quot118_quarantined_source_claims.jsonl\`
- \`state/wave2_quot118_source_intake.json\`
- \`wave2/quot119_individual_mathematical_reviews.jsonl\`
- \`state/wave2_quot119_meaning_screen.json\`
- \`wave2/quot120_individually_source_screened_links.jsonl\`
- \`wave2/quot120_missing_prerequisite_target_candidates.jsonl\`
- \`state/wave2_quot120_link_review.json\`
- Historic 600/606 formulation review snapshots, individually sourced stage intake files, and unchanged earlier directional-derivative held-source records.

### Next bounded research: Batch 121

Continue independent source-rich **breadth** beyond recently studied normality/quotients/graphs/generating functions. Three concrete missing prerequisite target candidates are logged, but avoid following them all as an unbounded foundational recursion. Candidate next branches: Fourier series/convergence notions with explicit analytic hypotheses; combinatorial recurrence and exponential generating functions (source-specific distinction from ordinary); graph connectivity via paths; uniform convergence versus pointwise convergence. Collision-check existing reconstructed meanings before ingesting anything. Review direct source provenance and mathematical definitions *before* promoting their variants/links.

Earlier unresolved external access remains: eight inaccessible Encyclopedia of Mathematics locators and 27 blocked original PlanetMath pages. The original 192 priority term records have first-pass evidence, **not** comprehensive definition coverage. The earlier ProofWiki boundary/exterior and normed-division-ring bibliography warnings also persist.

**Engineering protocol:** generic engine remains subject-neutral for future math theorems/math-education terminology; mathematical policy stays in mathDef adapters. Keep all five independent Wave 2 stages **UNSEALED**, do not access or compare production original corpus until appropriately independently frozen, and stop after approximately 12–14 active minutes with a verified commit and portable checkpoint.
