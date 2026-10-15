# Definition catalog

Snapshot: 2026-10-15. Counts below are generated from the repository tree; the deployed site is the source for the most current total.

**934 definitions across 40 subject folders.**

| Subject | Folder | Entries |
|---|---|---:|
| Abstract algebra | [`definitions/algebra/`](definitions/algebra/) | 29 |
| Algebraic and analytic number theory | [`definitions/arithmetic/`](definitions/arithmetic/) | 36 |
| Algebraic topology | [`definitions/alg-topology/`](definitions/alg-topology/) | 36 |
| Asymmetric quasi-metric spaces | [`definitions/quasimetric/`](definitions/quasimetric/) | 6 |
| Category theory | [`definitions/category/`](definitions/category/) | 46 |
| Chromatic metric geometry and TDA | [`definitions/tda/`](definitions/tda/) | 5 |
| Combinatorics | [`definitions/combin/`](definitions/combin/) | 18 |
| Commutative algebra | [`definitions/commalg/`](definitions/commalg/) | 21 |
| Complex analysis | [`definitions/complex/`](definitions/complex/) | 38 |
| Computability and complexity theory | [`definitions/computability/`](definitions/computability/) | 27 |
| Convex analysis and optimization | [`definitions/optimization/`](definitions/optimization/) | 36 |
| Distributions, Sobolev spaces and PDEs | [`definitions/pde/`](definitions/pde/) | 36 |
| Dynamical systems and ODEs | [`definitions/dynamics/`](definitions/dynamics/) | 15 |
| Elementary number theory | [`definitions/number/`](definitions/number/) | 19 |
| Foundational analysis | [`definitions/analysis/`](definitions/analysis/) | 3 |
| Functional analysis and operator theory | [`definitions/functional/`](definitions/functional/) | 41 |
| Functions and mappings | [`definitions/functions/`](definitions/functions/) | 4 |
| General topology | [`definitions/topology/`](definitions/topology/) | 32 |
| Geometry | [`definitions/geometry/`](definitions/geometry/) | 20 |
| Graph theory | [`definitions/graph/`](definitions/graph/) | 19 |
| Holomorphic dynamics | [`definitions/holodynamics/`](definitions/holodynamics/) | 28 |
| Holomorphic function spaces and reproducing kernels | [`definitions/functionspaces/`](definitions/functionspaces/) | 31 |
| Linear algebra | [`definitions/linear/`](definitions/linear/) | 28 |
| Mathematical logic | [`definitions/logic/`](definitions/logic/) | 15 |
| Measure theory | [`definitions/measure/`](definitions/measure/) | 39 |
| Measured group actions | [`definitions/measured-actions/`](definitions/measured-actions/) | 5 |
| Metric spaces | [`definitions/metric/`](definitions/metric/) | 3 |
| Numerical analysis | [`definitions/numerical/`](definitions/numerical/) | 35 |
| Probability and statistics | [`definitions/prob/`](definitions/prob/) | 31 |
| Real analysis | [`definitions/real/`](definitions/real/) | 22 |
| Relations | [`definitions/relations/`](definitions/relations/) | 24 |
| Schemes and sheaf theory | [`definitions/schemes/`](definitions/schemes/) | 20 |
| Set theory | [`definitions/sets/`](definitions/sets/) | 31 |
| Several complex variables and complex geometry | [`definitions/scv/`](definitions/scv/) | 41 |
| Smooth manifolds and differential geometry | [`definitions/manifold/`](definitions/manifold/) | 40 |
| Solenoidal manifolds and odometer groups | [`definitions/solenoids/`](definitions/solenoids/) | 6 |
| Stochastic processes | [`definitions/stochastic/`](definitions/stochastic/) | 39 |
| Walk metrics and proximities | [`definitions/graphwalks/`](definitions/graphwalks/) | 1 |
| Weighted and Bergman analysis | [`definitions/weighted-analysis/`](definitions/weighted-analysis/) | 5 |

| Classical special functions | [`definitions/special/`](definitions/special/) | 3 |

## Provenance

Each LaTeX definition file may contain:

- `id`: stable unique identifier; never rely on the human-readable term as the ID
- `term`: displayed term, which may include LaTeX math
- `aliases`: optional pipe-separated synonyms
- `related`: optional comma-separated existing definition IDs
- `source`: optional HTTPS academic reference or topic-index link
- `status`: `draft`, `reviewed`, or `example`

The source URL gives **reference context**, often a broad subject page, and is **not necessarily a direct citation for each specific formulation**. Entries were independently written in concise mathematical language. The presence of a URL does not establish that the referenced article supports every clause of an entry. The new corpus is tagged `draft` and is not mathematically peer-reviewed.

## Editorial review checklist

1. Confirm the ambient objects, quantifiers, and hypotheses are precise (field, topology, completeness, measurability, domains, etc.).
2. Check the formulation against an individual reputable mathematical reference, preferably with page/section-level citation; update the source URL when appropriate.
3. Explicitly identify convention-dependent variants, especially in algebra, topology, dynamical systems, and numerical analysis.
4. Verify LaTeX rendering and whether the definition is actually equivalent to accepted variants; separate properties and theorems from definitions.
5. Check term collisions and alternative meanings, preserve the stable ID, and audit `related` links for genuine mathematical relationships.
6. Promote from `draft` to `reviewed` only following individual mathematical review.

## Reference families used for discovery and contextual validation

- [Encyclopedia of Mathematics](https://encyclopediaofmath.org/wiki/Functional_analysis): advanced mathematical definitions and background across analysis, dynamics, number theory, and numerical analysis
- [nLab](https://ncatlab.org/nlab/show/category%2Btheory): category theory, homotopy, and manifold terminology
- [The Stacks Project](https://stacks.math.columbia.edu/tag/0ELP): commutative algebra, sheaves, and schemes
- [Boyd and Vandenberghe's Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/): convex analysis and optimization
- [Wikipedia's index of mathematics topics](https://en.wikipedia.org/wiki/Lists_of_mathematics_topics): discovery map for the initial subject expansion

## Verification

The GitHub Actions site build checks every file's ID, nonempty definition body, review status, source URL form, and related references. A passing build **does not** verify mathematical truth, citation specificity, or full LaTeX compilation. GitHub Pages builds a static client-side searchable index from the validated files.

## arXiv paper-defined entries (October 2026)

The first curated and scan-verified batches added **28** independently worded mathematical definitions from **six actual arXiv research papers**. Unlike subject-list references, each of these stores the paper identifier and version (when known), title, and exact numbered definition with printed page. All remain in draft status until individually checked.

A cautious LaTeX candidate scanner and GitHub Actions workflow are documented in [ARXIV_HARVEST.md](ARXIV_HARVEST.md). Candidate discovery is separate from accepting mathematical definitions. The code does not automatically import copyrighted paper text into the website.

### Live candidate scan confirmation

A rate-limited GitHub Actions trial of 12 current math.DS papers identified **30 definition-environment candidates in 7 papers**. The CSV is a *locator-only* review queue, not published definitions. Six new entries were then individually checked in arXiv:2610.20131 (Hurder and Lukina, *Mapping class groups of solenoidal manifolds*), and saved with explicit numbered locators. See [the successful live scan](https://github.com/Zengez/mathDef/actions/runs/38797055015).

## October 2026 source and category coverage audit

The [coverage and source-review report](COVERAGE_REVIEW.md) records the audits, prioritized reference sources, and the Wikipedia category workflow. In the current expansion, **91 additional draft definitions** were written from individual mathematical sources, notably Bergman kernels and spaces, analytic function spaces, standard complex analysis, and several complex variables. The initial coverage audit revealed several hundred nonmatching Wikipedia titles, not hundreds of confirmed mathematical omissions; biographies and theorems require triage. 

## Expanded systematic mathematics audit — 15 October 2026

The database now contains **908 draft/example definitions** across **40 folders**. A targeted inspection and repair covered all 36 original functional-analysis entries, followed by 29 independently formulated advanced definitions chosen from a completed depth-two Wikipedia mathematics category scan. None of these entries was indiscriminately reclassified as peer-reviewed.

The [broad discovery report](WIKIPEDIA_BROAD_SCAN_2026-10-15.md) summarizes four independent scans totaling 220 visited Wikipedia categories and 10,233 distinct candidate article titles; a large fraction of unmatched titles are not appropriate mathematical definitions. See also [WORK_CHECKPOINT.md](WORK_CHECKPOINT.md) for the remaining per-entry mathematical QA backlog.

## Measure theory and algebra audit, continued (October 15, 2026)

- **934 definitions** are present as individual LaTeX files; structural and mathematical review status are separate.
- Repaired **21 existing commutative algebra entries**, replacing a shared general Stacks tag with direct Stacks sections or individual mathematical topic pages and tightening definitions of tensor products, integrality, local rings, and zero divisors.
- Repaired **20 existing scheme/sheaf entries**, replacing a shared affine-scheme Stacks tag with relevant permanent references to the spectrum, presheaves, sheaves, stalks, locally ringed spaces and properties of schemes. Qualified the closed-subscheme and scheme-fiber formulations.
- Added **26 new advanced measure and stochastic definitions**, using the prior multi-category Wikipedia title inventory and individual concept pages. New topics include Radon regularity, signed measures, Hahn/Jordan decompositions, Radon–Nikodym derivatives, product and completed measures, Pettis/Bochner integration, standard Borel spaces, local martingales and semimartingales.
- All new definitions remain `status: draft`. Source URLs are direct concept references, but full mathematical peer review and per-definition renderer review remain to be completed.

[Checkpoint with commit IDs and remaining work](WORK_CHECKPOINT.md).
