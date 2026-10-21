# Independent mathDef Wave 2 — verified checkpoint Z (2026-10-20)

**Fast restart:** [generated RESUME_STATE.json](experiments/reconstruction-v2-independent/state/RESUME_STATE.json) and [mathDef adapter resume_plan.json](adapters/mathdef/resume_plan.json). Supersedes checkpoint Y's counts and next research work, not its historical source audit and individual formulations.

## Batches 128–131: product topology, eigenvalues, graph connectedness, exponential generating functions

All FOUR reviewed independent workflows completed successfully, passing portable unit tests, frozen Wave1 digest checks, old-record preservation, comprehensive source-specific disposition checks, and noncircular direct dependency checks.

- **Batch128 — source-only intake:** [success run 39526539812](https://github.com/Zengez/mathDef/actions/runs/39526539812). Added **four source headings, six source-specific observations**, all individually paraphrased and attributed to accessible ProofWiki: [Product Topology](https://proofwiki.org/wiki/Definition:Product_Topology) (finite-support basis also independently sourced to [Natural Basis of Product Topology](https://proofwiki.org/wiki/Natural_Basis_of_Product_Topology)); [Eigenvalue](https://proofwiki.org/wiki/Definition:Eigenvalue) (linear-operator context; real square-matrix specialization distinguished); [Connected (Graph Theory)/Graph](https://proofwiki.org/wiki/Definition:Connected_(Graph_Theory)/Graph) (vertex-pair criterion separately sourced); [Exponential Generating Function](https://proofwiki.org/wiki/Definition:Exponential_Generating_Function) (real convergent domain). No previously reviewed mathematical object or relation modified.
- **Batch129 — mathematical context/variant screening:** [success run 39526737505](https://github.com/Zengez/mathDef/actions/runs/39526737505). Added **four mathematical meanings and six individually source-screened formulations**. One indexed product topology meaning has two equivalent formulations: open projection cylinders as a **SUBBASIS** and finite-support open rectangular products as a **BASIS**. One field-linear-operator eigenvalue meaning has two equivalent formulations: nontrivial kernel ker(A−λI_V)≠{0_V} and existence of a nonzero eigenvector satisfying Av=λv; zero-dimensional V has no eigenvalues. Nonempty simple undirected graph connected by finite walks; the explicit nonempty convention avoids vacuity disagreements for the empty graph. Analytic real exponential generating function ∑a_n z^n/n! evaluated only where the real series converges, distinct from ordinary generating function of the same coefficient sequence or a formal EGF. Prior 618 mathematical formulation decisions/840 relationships preserved.
- **Batch130 — individual direct prerequisite reviews:** [success run 39527010719](https://github.com/Zengez/mathDef/actions/runs/39527010719). Added **12** separate source-screened direct links across all six new formulations, to previously independent topology, typed mappings, K-linear transformations, field-vector-space structure, kernel, simple graphs, real-number field, convergent real series, and real power-series meaning. Preserved all preceding **840** links and all **618** unrelated formulation decisions; 0 cycles.
- **Batch131 — precisely reviewed retroactive links:** [success run 39527211300](https://github.com/Zengez/mathDef/actions/runs/39527211300). Added **three** independently reviewed, source-specific links recovering two previously documented prerequisite gaps: older topological pointwise convergence → newly screened product topology on T^D, and each of the two older linear-operator eigenvector formulations → newly screened eigenvalue scalar meaning. Preserved **all prior 852 links** and the original 624 individual formulation decisions/explanations, appending only new link IDs to the **three affected old formulations**. No cycles, no circular eigenvalue-eigenvector dependencies: eigenvalue uses independent kernel and linear-map sources, not the eigenvector meaning.

### Verified independent inventory

| Registry | Total |
| --- | ---: |
| Approved external source collections | **14** |
| Independently attributed source headings | **473** |
| Individual source observations | **938**, including 3 previously source-held questionable observations |
| Mathematically screened contextual meanings | **587** |
| Individually screened mathematical formulations | **624** |
| Individually source-reviewed mathematical direct prerequisite links | **855** |
| Review decisions | **618 linked / 6 justified no-supported-target / 0 pending** |
| Definition dependency cycles | **0** |
| Sealed independent Wave 2 stages | **0** |

Frozen independent Wave1 publication digest: **7e9df8ae638dd48d8f8a68ec79c44e2ae3e35d40da6cfe8c15c5e6703781e801**. Original production mathDef definitions, variants and citations **never consulted or compared**. Work reviewed against sources and regression tests, not externally human peer-reviewed mathematical verification.

## Mathematical and source-quality safeguards

1. **Product topology ≠ box topology**, generally. Its open cylinder family is a subbasis, not the whole topology. Finite-support restrictions generate the basis. This supplies product topology on the function space T^D (coordinate i in D).
2. **Operator eigenvalue** λ∈K requires nontrivial kernel ker(A−λI_V), equivalently a nonzero vector v with Av=λv; λ is a scalar, not the eigenvector or eigenspace. No finite-dimensional assumption or matrix determinant formula was imported. A:V→V with the same K on both sides required.
3. **Connected graph** uses explicit **nonempty simple undirected graph** scope; every pair joined by finite walk. Source's raw all-pairs statement on V=∅ is vacuous; this research records a nonempty convention as an editorial restriction rather than declaring all conventions equivalent.
4. **Real exponential generating function** ∑a_n z^n/n! evaluated on its real convergence domain. This is not the ordinary generating function ∑a_n z^n for the unchanged coefficient sequence, and not an unevaluated formal series.
5. The THREE earlier source-held errors remain source observations only, excluded from mathematical meanings and accepted link graph: ProofWiki's gradient-existence-only directional-derivative equation; the forward-only graph-isomorphism clause; the uniform-convergence series partial-sum f_n/f_k indexing typo. No new source holds required in Batches128–131.
6. Other preserved source caveats: apparent erroneous ProofWiki topological-boundary alternative excluded; uncited scalar normed-division-ring pair page; eight inaccessible Encyclopedia of Mathematics and 27 PlanetMath original URLs. Original 192 initial priority items have first-pass evidence, not exhaustive independent coverage.

### Provenance files, relative to research_pipeline/experiments/reconstruction-v2-independent

- wave2/product_eigen_graph_egf_source_batch128_2026-10-20.jsonl
- wave2/foundation_source_discovery_batch_128.jsonl
- state/wave2_branch128_source_intake.json
- wave2/branch129_individual_mathematical_reviews.jsonl
- state/wave2_branch129_meaning_screen.json
- wave2/branch130_individual_source_screened_links.jsonl
- state/wave2_branch130_link_review.json
- wave2/branch131_individual_backfill_links.jsonl
- state/wave2_branch131_retroactive_links.json
- Historical 618- and 624-formulation individual review snapshots and stage-specific intake files.

## Suggested next bounded source-rich research: Batch132

Continue **independent mathematical breadth** beyond the just-completed product topology, operator eigenvalue, connected graph, and EGF contexts. Candidates: graph paths/cycles and their directed vs undirected distinctions, affine geometry definitions, combinatorial Stirling numbers, spectral diagonalizability with explicit field and operator assumptions, or real Fourier series. First collision-check current independent screened meanings and source URLs, then read exact external sources and source-specific mathematical variants before promoting meanings/links. Avoid unbounded recursion into only newly identified prerequisites.

**Engineering/independence:** Keep reusable generic engine topic-neutral for subsequent mathematical theorem and math-education terminology pipelines; mathematical screening policies in mathDef adapters. All five independent Wave2 stages remain UNSEALED; do not inspect or compare original production mathDef corpus before independent freeze. Run bounded ~12–14 minute active research intervals and commit/verify a succinct handoff checkpoint.
