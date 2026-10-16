# mathDef working checkpoint — 2026-10-15

## Purpose
Durable handoff/checkpoint for interrupted or timed-out mathDef research sessions. Always read this file and the live repository tree before resuming. Commit every bounded batch separately. Never describe an uncommitted batch as completed.

## Verified starting point
- Repository: https://github.com/Zengez/mathDef
- Site: https://zengez.github.io/mathDef/
- Last observed repository: **879 .tex definitions in 39 subject folders**. This is a snapshot, not a fixed target.
- Already present: Bergman space, Bergman kernel, weighted Bergman space and kernel, Bergman metric and projection, reproducing kernel Hilbert space; do not add duplicates.
- October coverage pass already added 91 entries (31 advanced function spaces; 41 several complex variables; 19 complex analysis).
- Source/discovery audit: [COVERAGE_REVIEW.md](COVERAGE_REVIEW.md); scanner: [scripts/wikipedia_candidate_scan.py](scripts/wikipedia_candidate_scan.py); scan docs: [WIKIPEDIA_DISCOVERY.md](WIKIPEDIA_DISCOVERY.md); source metadata auditor: [scripts/audit_corpus.py](scripts/audit_corpus.py).
- Previous 879-entry audit: 257 citations pointing to broad Wikipedia topic lists; 82 definition bodies shorter than 90 characters; 0 reviewed entries; 2 intentionally distinct entries titled Open set. Details in COVERAGE_REVIEW.md.
- Do not start or continue AWS/arXiv bulk download; user explicitly put that on hold.

## Next batch: direct-source audit (NOT YET COMPLETED)
1. Select a **small batch of up to 10** entries with broad Wikipedia topic-list source links (prefer function spaces/complex analysis initially).
2. Retrieve existing definition files. Read each definition and locate a **specific authoritative reference page** (individual EoM/Wikipedia article, textbook or permanent Stacks tag).
3. Verify definition hypotheses, measure/norm conventions, and mathematical correctness. Correct the body only when grounded, explaining significant changes in the commit.
4. If a precise source is verified, update its `source`; otherwise leave unchanged and log an unresolved issue. Do not falsely mark `reviewed` solely for changing the URL.
5. Run GitHub Actions build and tests after the committed batch, and update this checkpoint with actual counts and sample IDs.

## Subsequent batches
- Advance batches of up to 10 citation repairs.
- Then audit definition bodies under 90 characters, followed by full LaTeX/KaTeX rendering checks.
- Run bounded Wikipedia category scans in underrepresented subjects; review titles as *candidates*, not proven missing definitions.
- Priority new source families: Encyclopedia of Mathematics, NIST DLMF, Stacks Project, nLab, Mathlib, rigorous university textbooks, selected Wikipedia mathematical concept pages. Preserve domain and convention qualifiers.

## Process rules
- Make a small GitHub commit per batch, plus a checkpoint update.
- Check the live Git tree before edits; compare existing IDs, terms, and aliases.
- Never claim all entries were mathematically verified: source and build validation are distinct.
- Record completed batches, commit SHAs, unresolved items, and the next specific task here so another chat can resume immediately.
- If no writes or checks were done, label them pending rather than completed.

## Session status
- **Completed this session:** inspected the live 879-entry tree, Bergman examples, existing coverage review and Wikipedia discovery documentation. Created this checkpoint file.
- **Completed first mini-batch:** checked the existing `functional.banach-space` definition against the individual Encyclopedia of Mathematics article `https://encyclopediaofmath.org/wiki/Banach_space`, verified completeness terminology, and replaced the previous subject-level reference with this precise article. Existing `topology.topological-space`, `metric.metric-space`, and `topology.compactness` already have direct article links and were left unchanged.
- **Pending:** further source-repair batches, with the next batch beginning with additional `functional/` entries. The exact post-commit workflow outcome must be verified separately.

## 2026-10-15 continuation — expanded audit

- User approved bounded batches of about 20–30 rather than 5–10; record each commit and build.
- **Completed:** 14 `functional/` citation/convention repairs in commit `4c4a77c9bc3fdfd2cbf6137b31ecf0f5be53bcca`.
- **Completed:** 14 additional `functional/` reference repairs in commit `125db0bf10279f98cb8dc20495292a372f48d957`.
- **Running/pending:** broad category traversal, triggered by a new `.github/workflows/wikipedia-broad-audit.yml` workflow; four independent subject groups with depth 2, max 55 categories and max 5000 title candidates per group. Candidate artifacts are temporary; retain run links and summaries in checkpoint once completed.
- **Next:** retrieve Wikipedia title-only candidate CSVs; triage graduate-level terms using existing `id`, `term`, `aliases`; inspect specific reference pages and add a bounded batch of genuine missing definitions. Update corpus audit and references, and check deployment before declaring success.
- Full rigorous mathematical verification of 879 entries remains **incomplete**. Site build and metadata checks do not prove correctness.

## Completed October 15 broad scan and audit batches — latest checkpoint

- **Live repository inventory:** 908 .tex definitions across 40 subject folders; check live tree before resuming.
- **Detailed audit of old entries:** all 36 original `functional/` entries have had their mathematics checked at the level of explicit conditions and conventions and broad overview citations replaced by more specific links (one Banach-space fix and commits `4c4a77c9`, `125db0bf`, `d12ace87`). This does NOT make all entries peer-reviewed.
- **Expanded Wikipedia discovery:** successful GitHub Actions run [38809181537](https://github.com/Zengez/mathDef/actions/runs/38809181537). Four groups, 55 categories/group; 11,053 raw records; 10,233 unique Wikipedia article titles. See [WIKIPEDIA_BROAD_SCAN_2026-10-15.md](WIKIPEDIA_BROAD_SCAN_2026-10-15.md) and workflow [wikipedia-broad-audit.yml](.github/workflows/wikipedia-broad-audit.yml).
- **Accepted new drafts:** 14 category/matroid definitions in commit `256ad77b`, then 15 operator/geometry/stochastic/PDE/special-function definitions in `8bc6e698`. Both builds completed successfully.
- **Next editorial batch:** inspect 20–30 previously unreviewed definitions in one underaudited area (suggest `schemes/`, `commalg/`, `stochastic/` or `scv/`), replace broad context citations with specific source pages and correct any mathematical weaknesses. Record IDs explicitly in the next commit/checkpoint. Repeat until all 908+ definitions are reviewed. Do not claim full mathematical audit earlier.
- **Next discovery batch:** investigate another 20–30 of the most promising names in the candidate artifacts, cross-check IDs and synonyms, reject biographies/theorem-only pages, cite specific mathematical sources, and add only genuine missing concepts.
- **Important:** AWS/arXiv bulk extraction remains on hold at user's request.

## Full-corpus metadata scan result and last corrections

- Full **908-definition structural and editorial metadata scan** completed successfully in [GitHub Actions run 38810818349](https://github.com/Zengez/mathDef/actions/runs/38810818349), with downloadable issue-level CSV and machine-readable JSON.
- Snapshot: 887 draft, 21 example, 0 formally reviewed; 257 generic Wikipedia topic-index references, 35 general EoM subject-overview references, 82 very short bodies, two intentionally overlapping Open set display names, and one potential LaTeX-environment warning.
- Inspected the LaTeX warning: `combin.stirling-number` used `\begin{smallmatrix}` **inside inline math**. This is valid KaTeX, so it was a *false positive*. Corrected the metadata audit to ignore math-mode TeX environments. Replaced its generic source with a precise Stirling-numbers-of-the-second-kind article and clarified its body in commit `01cc56f4`. The post-change Wikipedia subject-index citation count should thus decrease to 256; verify on the next automated audit.
- GitHub Pages build and unit tests passed after this correction in [run 38811035189](https://github.com/Zengez/mathDef/actions/runs/38811035189).
- Future editor should treat these flags as **review priorities, not mathematical error counts**. 908 entries have NOT undergone comprehensive individual proof-level mathematical review; do not mark `reviewed` en masse.

## Further bounded batches — current session (October 15, 2026)

- Started from **908 entries, 40 folders**, with arXiv bulk work left on hold.
- **Existing definitions checked and revised: 41** total in this session:
  - `definitions/commalg/`: all 21 entries, 10 in commit `b97dcf5d` and 11 in commit `7e1b7acb`. Sources now cite direct Stacks sections or specific relevant Wikipedia concepts, rather than the shared Stacks spectrum tag `00DY`. Mathematical edits: local-ring convention and residue field, zero-divisor conventions (0 is included under the literal definition), tensor-product universal property, ring-map formulation of integrality.
  - `definitions/schemes/`: all 20 entries, 10 in commit `a38bfa9b` and 10 in commit `103378d5`. Replaced the shared affine-scheme reference with specific Stacks sections and a direct EoM irreducibility page; clarified the sheaf condition, closed subscheme and residue field in scheme fibers.
- **New source-informed draft definitions: 26** total:
  - Ten signed/Radon measure concepts in commit `26755a6b`.
  - Sixteen measure/integration/stochastic concepts in commit `96ec55c2`. Related IDs checked before committing.
  - Includes deliberate treatment of conventions for Radon measures and global vs local convergence in measure. Key source pages: Wikipedia articles on `Radon_measure`, `Signed_measure`, `Bochner_integral`, `Pettis_integral`, and the Stacks Project permanent ring/scheme tags.
- **New live inventory**: 934 definition files across 40 folders. Builds succeeded through the new measure/integration commits; verify the final scheme/documentation commit workflow before closing the session.
- **Review-status caution:** these 41 existing entries were individually read and citation/wording checked, but they have NOT been promoted to formally `reviewed`; most of the 934-entry corpus remains mathematically unaudited.
- **Next audits:** prioritize the 35 `stochastic/` original definitions or `scv/` and `linear/`, and separately resolve the 256+ Wikipedia topic-index references from the last metadata audit (freshly compute this figure after editing). Check any convention collisions, especially source-specific paper terminology, before changing stable IDs.
- **Next discovery:** use the locally saved Wikipedia subject-category CSV inventories to identify more graduate-level missing terms; cross-check IDs and aliases, prefer direct EoM/Stacks/DLMF sources, and add in batches no larger than ~20–30. Do not automatically import biography/theorem/article titles.
- **No further user input is necessary** for this work.

## Variance-consistency fix (October 15, 2026)

- Caught and corrected a genuine formal wording error: `schemes.presheaf` and `category.simplicial-set` had each described a functor from an opposite category as `contravariant`. In the standard functorial convention these are **covariant functors from the opposite category**, equivalently contravariant functors from the original category. Both now say “a functor from the opposite category (equivalently contravariant from the original category).”
- This highlights why mathematics-level consistency review is distinct from static syntax validation and why later audits should inspect category-theoretic variance, duals and universal-property orientations.

## 2026-10-15 evening continuation, batch S1

- Resumed from **934 definition files** and the checkpoint. Bulk arXiv remains on hold.
- Examined first ten existing stochastic-process entries, IDs: stochastic.adapted-process, stochastic.almost-sure-convergence, stochastic.brownian-motion, stochastic.characteristic-function-prob, stochastic.conditional-independence, stochastic.convergence-distribution, stochastic.convergence-lp, stochastic.convergence-probability, stochastic.covariance-function, stochastic.discrete-stationary-process.
- Replaced 9 generic Martingale references with more specifically relevant EoM or Wikipedia articles; one martingale-adjacent reference was retained. Improved $L^p$ convergence common-space assumptions, distinguished conditional independence given an **event** from conditional independence given a sigma-field, and clarified index-set conditions in strict stationarity.
- Batch S1 is committed together with this checkpoint; source URLs are context references, not proof of peer review. Entries remain `draft`.
- Next action: audit second group of stochastic entries starting at `ergodic-measure`, inspect for mathematically significant errors, and commit with next checkpoint.

## 2026-10-15 evening continuation, batch S2

- Examined stochastic IDs: stochastic.ergodic-measure, stochastic.essential-supremum, stochastic.feller-process, stochastic.filtration, stochastic.gaussian-process, stochastic.invariant-measure, stochastic.levy-process, stochastic.markov-kernel, stochastic.martingale-transform, stochastic.martingale; checked against EoM articles on martingales, invariant measure, Gaussian processes, transition functions, and direct subject references.
- Fixed a genuine **unbound domain** bug in `stochastic.markov-kernel`: now states both measurable spaces and both measurability conditions.
- Strengthened `stochastic.ergodic-measure` by expressing invariance modulo null sets via symmetric difference, and `stochastic.essential-supremum` by identifying the ambient measure and extended-real convention.
- Remaining stochastic entries for audit start with `median`, `moment-generating-function`, `poisson-process`, etc. S1 and S2 were each independently committed, with this checkpoint for session recovery.

## 2026-10-15 evening continuation, batch S3

- Audited ten additional stochastic entries: median, moment-generating-function, poisson-process, predictable-process, quadratic-variation, quantile, renewal-process, stationary-increment-process, stopped-process, stopping-time. Swapped generic `Martingale` source for individual process, stopping-time, renewal, quantile, and integral-reference articles.
- Mathematically important correction: `stochastic.renewal-process` did not specify $S_0=0$ and had an undefined max for $t<S_1$. It now includes $S_0=0$, $n\ge0$, and almost-sure finiteness.
- Refined quadratic-variation partition mesh and stopped-process time domain. These are editorially audited drafts; review status was not altered.
- Next: audit final preexisting stochastic entries (`strong-markov-property`, `submartingale`, `supermartingale`, `tightness`, `uniform-integrability`, `weak-convergence-measures`, `wiener-process`) and newer `local-martingale`/`semimartingale`; then audit first block of SCV and add missing graduate terms.

## 2026-10-15 evening continuation, batch S4

- Completed audit of all **39 existing `stochastic/` definition files** in four independently committed batches (S1 10, S2 10, S3 10, S4 9); archive revisions committed before moving on.
- S4 reviewed: stochastic.strong-markov-property, stochastic.submartingale, stochastic.supermartingale, stochastic.tightness, stochastic.uniform-integrability, stochastic.weak-convergence-measures, stochastic.wiener-process, stochastic.local-martingale, stochastic.semimartingale. A crucial correction makes the strong Markov property *formal*, with bounded measurable test functions and a conditional-expectation equation at finite stopping times.
- All stochastic definitions remain draft; no automated peer-review promotion. Duplicate terminology `brownian-motion` and `wiener-process` remains intentional cross-reference.
- Next: several complex variables (`scv/`, 41 existing entries), then an independently sourced discovery batch. Inspect math exactness and sources in each batch.

## 2026-10-15 evening continuation, batch C1

- Began several-complex-variables audit: 11 existing IDs checked: scv.defining-function, scv.dolbeault-cohomology, scv.dolbeault-operator, scv.domain-of-holomorphy, scv.exhaustion-function, scv.holomorphic-hull, scv.holomorphic-separability, scv.holomorphically-convex, scv.levi-form, scv.levi-pseudoconvex-boundary, scv.stein-manifold.
- Corrected `scv.stein-manifold` to explicitly include locally defined holomorphic coordinate systems arising from global functions, following the Encyclopedia of Mathematics definition; its former 2-condition statement omitted that item. Replaced generic analytic-function/Levi references with individual EoM articles on domains of holomorphy and Stein manifolds.
- Clarified that an exhaustion function's properness formulation needs a lower bound, and that the domain-of-holomorphy/pseudoconvexity equivalence is specifically a finite-dimensional statement.
- All entries remain draft. Next audit SCV analytic/complex-manifold geometry and pluripotential groups in ~10-entry blocks.

## 2026-10-15 evening continuation, batch C2

- Inspected 10 more SCV/pluripotential entries: scv.pluriharmonic-function, scv.plurisubharmonic-function, scv.polynomial-hull, scv.polynomially-convex-set, scv.pseudoconvex-domain, scv.strictly-plurisubharmonic, scv.strongly-pseudoconvex-boundary, scv.subharmonic-function, scv.upper-semicontinuous, scv.complex-tangent-hyperplane; swapped four broad/less-specific sources for individually relevant Encyclopedia of Mathematics articles.
- Clarified compact **closed sublevel** condition in the pseudoconvex exhaustion definition and its finite-dimensional Levi-problem equivalence, made the $C^2$ convention explicit for strict plurisubharmonicity, and labeled the complex tangent hyperplane precisely.
- Next SCV audit: remaining geometry/Kähler/Kobayashi entries and analytic polyhedra, about 20; then new advanced terms. Follow up on any concept-level convention conflicts rather than promoting to reviewed.

## 2026-10-15 evening continuation, batch C3

- Examined 10 geometric/analytic SCV definitions: scv.analytic-polyhedron, scv.biholomorphic-map, scv.complex-analytic-subset, scv.complex-line, scv.complex-manifold, scv.complex-polydisc, scv.complex-projective-space, scv.complex-torus, scv.complex-unit-ball, scv.fatou-bieberbach-domain.
- Clarified relative closedness of analytic subsets, the compactly-contained analytic-polyhedron convention, the natural quotient operation for complex projective space, and that complex tori need not be algebraic. Biholomorphic maps now explicitly refer to complex manifolds and a direct EoM article.
- Entries were left in draft status and stable IDs preserved. Next final SCV batch: Fubini–Study, automorphism, holomorphic vector bundles, Kähler and Kobayashi geometry, tube domains, $(p,q)$-forms and Hartogs separate holomorphy.

## 2026-10-15 evening continuation, batch C4 — SCV folder audit complete

- Reviewed final 10 existing SCV IDs: scv.fubini-study-form, scv.holomorphic-automorphism, scv.holomorphic-mapping, scv.holomorphic-vector-bundle, scv.kahler-manifold, scv.kobayashi-hyperbolicity, scv.kobayashi-pseudodistance, scv.tube-domain, scv.type-pq-form, scv.several-variable-holomorphic-function.
- Explicitly distinguished equipped Kähler manifolds from those merely admitting a Kähler metric, clarified Fubini–Study normalization, generalized holomorphic automorphisms to complex manifolds, and recorded Hartogs's separate-holomorphy equivalence only on open subsets of $\mathbb C^n$.
- Thus all **41 existing SCV definitions** have now been inspected in four committed batches C1 11, C2 10, C3 10, C4 10. All **39 stochastic definitions** were inspected in S1–S4 earlier in this session.
- Mathematically specialized definitions and citations remain `draft`; this was a focused line-by-line precision/source audit, not full third-party peer review or runtime rendering inspection.
- Next: discover new graduate-level mathematics terms, cross-check existing stable IDs, add a bounded well-cited batch, test website and run corpus-wide metadata audit; update snapshot totals and checkpoint.

## 2026-10-15 evening continuation, discovery D1

- After all 39 stochastic and 41 previous SCV entries were audited, identified **11 new advanced SCV concepts** and independently drafted linked LaTeX definitions with direct subject-specific sources (EoM, PlanetMath, Wikipedia): scv.runge-domain, scv.runge-pair, scv.envelope-of-holomorphy, scv.pluripolar-set, scv.complete-pluripolar-set, scv.pluricomplex-green-function, scv.hyperconvex-domain, scv.complex-monge-ampere-operator, scv.levi-flat-hypersurface, scv.caratheodory-pseudodistance, scv.caratheodory-hyperbolicity.
- Special care: the bounded hyperconvex-domain definition uses **negative level compactness** rather than the contradictory compact-sublevel-for-every-real-threshold formula. The pluripolar concept names its global convention; the complex Monge–Ampère determinant uses an explicit normalization; the holomorphic envelope can be multi-sheeted.
- All IDs and `related` pointers checked against current GitHub tree before committing; new entries remain draft.
- Next: discovery D2 focused on CR structures, Shilov boundaries, analytic discs and function algebra terminology, followed by build validation and updated catalog/checkpoint.

## 2026-10-15 evening continuation, discovery D2

- Added **14** more precise graduate-level definitions in `functional/` and `scv/`: functional.uniform-algebra, functional.shilov-boundary, functional.peak-point, functional.peak-function, scv.bergman-shilov-boundary, scv.cr-structure, scv.cr-function, scv.hartogs-figure, scv.holomorphic-function-germ, scv.analytic-set-germ, scv.weierstrass-polynomial, scv.holomorphic-vanishing-order, scv.meromorphic-function-on-manifold, scv.divisor.
- Context references are individual EoM articles on uniform algebras, Bergman–Shilov boundary, CR manifolds, function germs, Weierstrass preparation, and complex analytic divisors. Hartogs figure is an explicit standard model, not a claim that every Hartogs figure uses this normalization.
- Carefully distinguish the Bergman–Shilov boundary (function-algebra notion) from the Bergman kernel; complex-analytic divisors include integer multiplicities; Weierstrass polynomials have holomorphic coefficients vanishing at the origin.
- D1 had 11 new SCV entries and D2 14 new entries; the whole session started with 934 definitions, so the current expected collection is **959** definitions (check live tree). All entries are drafts, and the source content was independently paraphrased rather than copied.
- NEXT: verify latest GitHub Actions build for D2, rerun full-corpus metadata audit, update `CATALOG.md` and `README.md` counts. Then another audit of 20–30 previously unreviewed entries (priority `linear/` or `pde/`) and repair generic source links. Update this checkpoint after each batch.

## 2026-10-15 evening continuation — linear algebra L1

- Inspected 10 `linear/` IDs: basis, characteristic-polynomial, determinant, diagonalizable-operator, dimension, dual-space, eigenspace, eigenvalue, eigenvector, image; replaced their generic Wikipedia `List_of_linear_algebra_topics` citation with direct EoM/Wikipedia concept pages.
- Clarified basis as a **Hamel basis**, separate from infinite Schauder expansions, fixed the field dependence of diagonalizability and the sign convention for characteristic polynomials, and added a commutative base-ring assumption for the determinant formula. Checked eigenvalue/eigenspace definitions against the EoM operator entries.
- Next: inspect the 18 remaining `linear/` entries in 2 smaller batches, then move to the most important PDE problems and new sources. All definitions remain draft.

## 2026-10-15 evening continuation — linear algebra L2

- Reviewed `linear/`: inner-product, invertible-matrix, kernel, linear-combination, linear-functional, linear-independence, linear-map, matrix-multiplication, matrix, norm. Fixed ambiguous scalar-field, ring, and inner-product linearity conventions and explicitly distinguished algebraic from continuous linear functionals.
- Replaced generic topic-list links with term-specific references. Zero-dimensional matrix shapes remain allowable under the explicit $m,n\ge0$ convention.
- Next linear L3: remaining 8 entries `nullity`, `orthogonal-complement`, `orthogonality`, `rank`, `span`, `subspace`, `transpose`, `vector-space`. Then compile/metadata check and further audits.

## 2026-10-15 evening continuation — linear algebra L3 completed

- Reviewed last 8 existing `linear/` entries: nullity, orthogonal-complement, orthogonality, rank, span, subspace, transpose, vector-space. Replaced broad Wikipedia topic index citations with precise concept pages, corrected the domain of orthogonal complements to subsets, and stated vector-space axioms and zero-span convention explicitly.
- All **28 original linear-algebra entries** have now been examined and committed in L1 10, L2 10, L3 8. Distinguish structural syntax validation from mathematical peer review: entries remain `draft`.
- Current expected total still **959** definitions, with 40 folders (check repository tree). Next target: PDE/domain and numerical approximations or another methodical Wikipedia/EoM-driven batch of genuinely missing mathematical definitions; refresh CATALOG and README.

## October 15, 2026 — PDE batch P1

- Inspected 10 existing PDE entries: pde.characteristic-surface, pde.convolution, pde.dirac-delta, pde.dirichlet-boundary-condition, pde.distribution, pde.distributional-derivative, pde.divergence, pde.elliptic-equation, pde.fourier-transform, pde.fundamental-solution. Replaced generic Sobolev-space reference with concept-level EoM or Wikipedia sources where appropriate (the Fourier transform already had a direct EoM source).
- Fixed substantive mathematical omissions: `characteristic-surface` now requires $d\phi\ne0$; `fundamental-solution` now distinguishes translation-invariant $LE=\delta_0$ from a variable-coefficient fundamental kernel $L_xE(x,y)=\delta_y$; `elliptic-equation` specifies the real nondivergence-form uniform-ellipticity convention.
- Added ambient domains for distributions and Dirac delta, retained original stable IDs, left status draft. Next: PDE P2 (gradient, Green function, Sobolev, wave/heat etc) and continuation of source-specific citations.

## October 15, 2026 — PDE batch P2

- Inspected PDE IDs pde.gradient-vector, pde.green-function, pde.h1-space, pde.h10-space, pde.heat-equation, pde.hyperbolic-equation, pde.initial-value-problem, pde.inverse-fourier-transform, pde.laplace-equation, pde.laplacian. Replaced generic Sobolev references by directly relevant EoM/Wikipedia articles for Green functions, equations, gradients and Laplacians; Sobolev-specific entries retain Sobolev references.
- Substantive clarifications: Green functions depend on a *specified boundary-value problem* and need not exist uniquely; hyperbolicity is defined relative to a time covector with alternate strict-root conventions; inverse Fourier formula requires suitable inversion hypotheses; Laplacian specified Euclidean $C^2$ setting.
- Next: P3 entries mollifier, multi-index, Neumann, parabolic, Poisson, principal symbol, Robin, Schwartz, Sobolev, tempered distributions.

## October 15, 2026 — PDE batch P3

- Examined 10 PDE entries mollifier, multi-index, neumann-boundary-condition, parabolic-equation, poisson-equation, principal-symbol, robin-boundary-condition, schwartz-space, sobolev-space, tempered-distribution and used direct reference pages instead of generic Sobolev sources (except the actual Sobolev-space definition).
- Made regularity/normal assumptions explicit in Neumann conditions, distinguished positive definite from uniformly parabolic operators, specified principal-symbol derivative convention, and made distributional Sobolev derivatives/Schwartz seminorm topology explicit.
- Next: P4 last 6 PDE definitions `test-function`, `viscosity-solution`, `wave-equation`, `weak-derivative`, `weak-solution`, `well-posed-problem`. Confirm full 36-entry PDE audit then final GitHub build.

## October 15, 2026 — PDE batch P4 (resumed after timeout)

- Verified from the repository that P3 (10 PDE definitions) **had already committed** and GitHub Pages run 38828740232 succeeded; no P3 work was repeated.
- Inspected and refined the last 6 preexisting PDE IDs: pde.test-function, pde.viscosity-solution, pde.wave-equation, pde.weak-derivative, pde.weak-solution, pde.well-posed-problem. Added paper-independent per-concept references; formalized test-function domains, viscosity touching condition, time/space domains in wave equations, weak Poisson solution domain, and Hadamard well-posedness relative to specified topological data and solution spaces.
- All **36 existing PDE entries** have now been inspected in four bounded batches: P1 10, P2 10, P3 10, P4 6. Build verification of P4 is still a separate step. Every definition remains `draft` despite source review; individual mathematical peer review is not asserted.
- NEXT: examine further uncited/short graduate-level mathematical concepts and audit older numerical analysis or advanced category/homological entries in separately committed batches. Refresh CATALOG/README snapshots and rerun metadata audit.

## PDE P4 corrective follow-up — source redirect and boundedness

- Checked weak-derivative citation with live sources: EoM `Weak_derivative` **redirects to Gâteaux derivative**, a different definition. Repaired `pde.weak-derivative` source to the genuine [Wikipedia weak derivative entry](https://en.wikipedia.org/wiki/Weak_derivative), which contains exactly the displayed distributional integration-by-parts formula.
- Removed an incorrect caution newly inserted into `pde.weak-solution`: if $f\in L^2(\Omega)$, the functional $v\mapsto\int_\Omega fv$ **is continuous** on $H_0^1(\Omega)$ with the full $H^1$ norm even when $\Omega$ is unbounded; no Poincaré inequality is needed for that fact. A Poincaré inequality may instead matter for coercivity/existence under gradient-only bilinear forms.
- This illustrates why individual URL *resolution* and hypotheses checks matter, even following a passed static build. Remaining definition entries stay draft.

## Numerical analysis audit, batch N1 (October 15, 2026)

- Examined 12 existing numerical definitions: numerical.absolute-error, numerical.backward-error, numerical.backward-stability, numerical.condition-number, numerical.convergence-order, numerical.cubic-spline, numerical.discretization-error, numerical.divided-difference, numerical.euler-method, numerical.finite-difference, numerical.finite-element-method, numerical.fixed-point-iteration.
- Replaced generic `Numerical_analysis` citations with individual mathematical reference articles.
- Important mathematical edits: specified infimum and norms for backward error (the minimizing perturbation might not exist); emphasized distinction between backward stability and problem conditioning; stated domain/norm assumptions for relative condition numbers; restricted “cubic spline” to piecewise polynomial on a specified knot sequence; clarified centered finite-difference $O(h^2)$ smoothness requirements and conforming Galerkin FEM scope.
- Next: numerical N2, 12 files starting at `forward-error`. Keep numerical definitions draft. Build verification pending current commit.

## Numerical analysis audit, batch N2 (October 15, 2026)

- Inspected next 12 numerical entries: numerical.forward-error, numerical.gaussian-elimination, numerical.interpolation, numerical.lagrange-interpolation, numerical.least-squares, numerical.lu-factorization, numerical.machine-epsilon, numerical.matrix-condition-number, numerical.newton-root, numerical.normal-equations, numerical.qr-factorization, numerical.quadrature-rule. Generic EoM Numerical_analysis references replaced by concept-level numerical articles.
- Corrected LU-without-pivoting existence assumptions, clarified normal equations in real versus complex spaces, allowed rank-deficient thin QR, and preserved the machine-epsilon/unit-roundoff convention distinction. The remaining mathematical content is basic numerical linear algebra, not a claim of peer review.
- Next numerical N3: remaining 11 entries `relative-error`, `residual`, `roundoff-error`, `runge-kutta4`, `simpson-rule`, `singular-value-decomposition`, `singular-value`, `spectral-norm`, `spline`, `trapezoidal-rule`, `truncation-error`.

## Numerical analysis audit, batch N3 (October 15, 2026)

- Examined remaining 11 numerical definitions numerical.relative-error, numerical.residual, numerical.roundoff-error, numerical.runge-kutta4, numerical.simpson-rule, numerical.singular-value-decomposition, numerical.singular-value, numerical.spectral-norm, numerical.spline, numerical.trapezoidal-rule, numerical.truncation-error. All references made concept-specific.
- Explained residual sign conventions, how the rectangular dimension affects the **count** of zero singular values, and that spline degree and required smoothness are distinct parameters. Clarified truncation-error versus floating-point roundoff and numerical ODE local-defect conventions.
- Fixed a stray LaTeX spacing macro outside math introduced in N2's machine-epsilon text.
- **All 35 preexisting `numerical/` definitions** have now been inspected over three commits N1 12, N2 12, N3 11. Each remains editorial draft. NEXT: audit metadata and new definition coverage; reconcile catalog snapshot and verify Actions.

## Graduate-level discovery and expansion, batch M1 (October 15, 2026)

- After checking the 36 pre-existing PDE files and 35 numerical definitions, added **12 graduate-level microlocal/PDE definitions** from specific EoM and individual Wikipedia articles: pde.hormander-symbol-class, pde.pseudodifferential-operator, pde.classical-symbol, pde.elliptic-classical-symbol, pde.parametrix, pde.smoothing-operator, pde.singular-support, pde.wave-front-set, pde.pseudolocal-operator, pde.fourier-multiplier, pde.bessel-potential-space, pde.heat-kernel.
- Principal reference: [EoM pseudodifferential operator](https://encyclopediaofmath.org/wiki/Pseudo-differential_operator), with Hörmander symbol estimates, principal symbol ellipticity, parametrix modulo smoothing, and oscillatory-integral operator normalization. Other direct references: [Wave front set](https://en.wikipedia.org/wiki/Wave_front_set), [EoM multiplier theory](https://encyclopediaofmath.org/wiki/Multiplier_theory), [EoM Bessel potential operator](https://encyclopediaofmath.org/wiki/Bessel_potential_operator).
- Each item specifies ambient domain/space and, where needed, Fourier sign/normalization. No full article text was copied; all 12 entries are original concise draft definitions with checked related IDs.
- **Expected total 971 definitions in 40 folders** after M1. Confirm live tree and deploy run before reporting final count. Remaining goals: update catalog/README counts, rerun metadata audit, and continue staged audits of other folders.
