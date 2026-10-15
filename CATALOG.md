# Definition catalog

Snapshot: 2026-10-15. Counts below are generated from the repository tree; the deployed site is the source for the most current total.

**760 definitions across 31 subject folders.**

| Subject | Folder | Entries |
|---|---|---:|
| Abstract algebra | [`definitions/algebra/`](definitions/algebra/) | 29 |
| Algebraic and analytic number theory | [`definitions/arithmetic/`](definitions/arithmetic/) | 36 |
| Algebraic topology | [`definitions/alg-topology/`](definitions/alg-topology/) | 36 |
| Category theory | [`definitions/category/`](definitions/category/) | 36 |
| Combinatorics | [`definitions/combin/`](definitions/combin/) | 14 |
| Commutative algebra | [`definitions/commalg/`](definitions/commalg/) | 21 |
| Complex analysis | [`definitions/complex/`](definitions/complex/) | 19 |
| Computability and complexity theory | [`definitions/computability/`](definitions/computability/) | 27 |
| Convex analysis and optimization | [`definitions/optimization/`](definitions/optimization/) | 36 |
| Distributions, Sobolev spaces and PDEs | [`definitions/pde/`](definitions/pde/) | 35 |
| Dynamical systems and ODEs | [`definitions/dynamics/`](definitions/dynamics/) | 15 |
| Elementary number theory | [`definitions/number/`](definitions/number/) | 19 |
| Foundational analysis | [`definitions/analysis/`](definitions/analysis/) | 3 |
| Functional analysis and operator theory | [`definitions/functional/`](definitions/functional/) | 36 |
| Functions and mappings | [`definitions/functions/`](definitions/functions/) | 4 |
| General topology | [`definitions/topology/`](definitions/topology/) | 32 |
| Geometry | [`definitions/geometry/`](definitions/geometry/) | 20 |
| Graph theory | [`definitions/graph/`](definitions/graph/) | 19 |
| Holomorphic dynamics | [`definitions/holodynamics/`](definitions/holodynamics/) | 28 |
| Linear algebra | [`definitions/linear/`](definitions/linear/) | 28 |
| Mathematical logic | [`definitions/logic/`](definitions/logic/) | 15 |
| Measure theory | [`definitions/measure/`](definitions/measure/) | 15 |
| Metric spaces | [`definitions/metric/`](definitions/metric/) | 3 |
| Numerical analysis | [`definitions/numerical/`](definitions/numerical/) | 35 |
| Probability and statistics | [`definitions/prob/`](definitions/prob/) | 31 |
| Real analysis | [`definitions/real/`](definitions/real/) | 22 |
| Relations | [`definitions/relations/`](definitions/relations/) | 24 |
| Schemes and sheaf theory | [`definitions/schemes/`](definitions/schemes/) | 20 |
| Set theory | [`definitions/sets/`](definitions/sets/) | 31 |
| Smooth manifolds and differential geometry | [`definitions/manifold/`](definitions/manifold/) | 36 |
| Stochastic processes | [`definitions/stochastic/`](definitions/stochastic/) | 35 |

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
