# Same-term internal variants: one-pass manual review packet

**Stage-only branch:** `work/dedup-subject-context-sources-20261027`  
**Scope:** Only formulations that were already attached under the **same current searchable heading**. No term expansion, cross-heading comparison, or deep source research.  
**Input:** 2,013 searchable headings; 1,923 with one formulation; 90 with multiple attached variants (196 variants at the start of this pass).  
**Disposition:** 44 obviously mathematically distinct (retained), 2 obvious duplicate cases merged with source and historic-ID inheritance, 44 for manual review (left unchanged). 

**Important:** These labels are conservative classification results, not claims that every remaining formulation is a separate mathematical meaning. Any distinction that would require more than a cursory reading to settle is in the manual-review section. The full structured records are in `data/merged_cleanup_internal_variant_classification.json`; all citations remain in the stage-only catalog/source registry.

## Two merged obvious duplicates

1. **closure of a subset in a topological space.** The least closed superset is precisely the intersection of closed supersets, a near-verbatim restatement of the same construction. Retained `form.wave2.cross107.topological-closure.1`; retired `form.wave2.cross107.topological-closure.2`.
2. **Set partition.** Both require exactly a pairwise disjoint family of nonempty blocks whose union is the original set. The third, unique-membership characterization is NOT discarded. Retained `form.wave2.group116.set-partition.1`; retired `form.mathdef.original.combin.set-partition.primary`.

## 44 apparently distinct headings (no edits)

1. **accumulation point** — Sequence accumulation is formulated through subsequences/infinitely many indices; set accumulation is by neighborhoods of a subset. The defining input object differs.
2. **Adapted process** — Discrete-time and continuous-time filtrations have genuinely different index domains and measurability requirements. The original general-index notion is retained alongside these narrower index contexts in the now-shared heading.
3. **Basis for a topology** — Base as a generator on a bare underlying set versus base subordinate to an already specified topology.
4. **binary operation** — An internal binary law S×S→S differs in declared type and closure from a general two-input map S×T→U; neither substitutes for the other.
5. **binary relation** — Relations as subsets of S×S and typed relations between potentially different sets are different ambient data; retain the generalized representation.
6. **Boolean ring** — Keep unital versus possibly nonunital idempotent rings distinct; duplicate nonunital wording is already consolidated.
7. **Borel measure** — Basic measure, compact-finite assumptions and outer-measure presentations invoke different hypotheses/objects; do not erase them.
8. **chain complex** — Module/abelian group chain complexes versus complexes in a general additive category use different mathematical frameworks.
9. **closed ball** — Metric and normed-vector-space formulations use different structures; the normed case is a metric specialization but informative.
10. **coset of a subgroup** — Left coset gH and right coset Hg can be different sets when H is not normal.
11. **domination of local rings** — One formulation embeds local subrings in a common field; the other allows general compatible local-ring inclusions. Different ambient hypotheses.
12. **exact sequence** — Specific module exactness versus categorical images and kernels in an abelian category.
13. **filtered category** — A small filtered category is a genuine smallness specialization of filtered categories without that size restriction.
14. **filtration of sigma-algebras** — The original definition permits an increasing family indexed by an arbitrary ordered index set T. The researched instance explicitly fixes n>=0; retain this useful discrete-time specialization and preserve separate sources.
15. **independent sigma-algebras** — Two algebra independence versus mutual independence of a countable family have different quantification.
16. **infimum** — Real lower bounds and infimum in an arbitrary partially ordered set differ in the ambient ordered object and existence assumptions.
17. **inner product space** — Real symmetric bilinear and complex Hermitian forms have different scalar fields and conjugation behavior.
18. **kernel** — Concrete additive subgroup kernel of an abelian group homomorphism versus universal categorical kernel morphism.
19. **kernel of linear transformation** — Linear maps of modules over rings versus of vector spaces over fields require different ambient algebraic objects.
20. **Linear map** — After consolidating the searchable 'linear transformation' heading into 'Linear map', keep the independent general left R-module map and field-vector-space specialization as distinct and pedagogically informative ambient settings. The redundant researched vector-space formula merges into the existing original Linear map meaning.
21. **Lipschitz continuity** — Global Lipschitz inequality for all pairs differs from a point-anchored bound at a fixed base point; one is generally stronger.
22. **locally finite Borel measure** — One version assumes Hausdorff spaces and includes consequences about compact sets; another is defined on arbitrary topological spaces. Preserve scope pending detailed citation review.
23. **locally uniform convergence of functions** — Compact-local complex analytic formulation versus neighborhood-local topological-source/metric-target formulation; equivalent only under additional hypotheses.
24. **mapping (function)** — Input-output assignment, bare graph subset, and typed graph object are distinct mathematical encodings, even when equivalent as functions.
25. **module over a ring** — Nonunital right modules, unital left modules, and unital right modules encode different module actions/conventions.
26. **natural numbers** — Inclusion versus exclusion of zero affects the underlying set and dependent constructions; do not collapse conventions silently.
27. **norm on a vector space** — Normed division-ring scalar systems versus real or complex normed spaces are different ambient frameworks.
28. **normed vector space** — Real/complex scalar field versus general normed division-ring scalar field.
29. **open ball** — Metric-space ball d(x,a)<r and norm-space ball ∥x−a∥<r reflect different given structures; normed-space version is informative specialization.
30. **open cover** — Cover of an arbitrary subset by ambient open sets versus a cover of the entire space; preserve the broader construction.
31. **open interval of real numbers** — Extended-real endpoints include unbounded open intervals while finite endpoints cover only bounded intervals.
32. **Open set** — Metric-ball openness and arbitrary topological openness require different input structures.
33. **orthogonal polynomial system** — Continuous weight on an interval, discrete countable support, finite support and a general Stieltjes measure supply different orthogonality frameworks.
34. **pointwise convergence of functions** — Real-valued pointwise limits and arbitrary topological-target pointwise limits have different codomain frameworks.
35. **polynomial ring** — One formal indeterminate versus an arbitrary family of indeterminates uses different polynomial constructions.
36. **quotient ring** — Quotient of noncommutative unital ring by two-sided ideal versus commutative quotient.
37. **random variable** — General measurable-state-space random elements versus real-valued measurable functions use different codomains and sigma-algebras.
38. **real number system (complete ordered field)** — Axiomatic complete ordered field, Dedekind-cut construction and Cauchy-completion construction describe genuinely different presentations/objects.
39. **reduced ring** — Definition in commutative rings versus possibly noncommutative associative rings.
40. **ring homomorphism** — A ring homomorphism that must preserve identity is not interchangeable with an additive multiplicative map whose preservation of 1 is not required. Keep both conventions explicit.
41. **stochastic process** — A family of random elements potentially with differing state spaces versus an E-valued process with fixed measurable state space.
42. **supremum** — Real least upper bound versus upper bounds in an arbitrary partially ordered set.
43. **trace of a square matrix** — Trace over an arbitrary commutative ring (including 0×0 convention) versus strictly positive-size matrices over a field uses different domains.
44. **uniform convergence of functions** — Real-valued uniform convergence versus general metric-valued uniform convergence has a different target structure.

## 44 manual-review headings (unchanged)

These entries reproduce their **existing wording only**; no source investigations were performed for this packet. Each form identifier is preserved to allow a precise later decision.

### 1. additive category

**Reason for review:** Finite-product definition in a preadditive category versus zero object and finite biproduct construction: separate informative criterion.

**Variant 1:** `form.mathdef.original.category.additive-category.primary` (meaning.mathdef.original.category.additive-category)

```text
An additive category is a preadditive category (its morphism sets are abelian groups and composition is bilinear) having a zero object and every binary biproduct. A biproduct of $X,Y$ is simultaneously their product and coproduct, with canonical injections and projections satisfying the usual matrix identities. In particular, the category has finite products and coproducts.
```

**Variant 2:** `form.wave2.foundation15.additive-category` (meaning.wave2.foundation15.additive-category)

```text
An additive category C is a preadditive category in which all finite products exist, including an empty product. Equivalently in a preadditive category, it has a zero object and finite direct sums.
```

### 2. bipartite simple undirected graph

**Reason for review:** Partition of vertices into two independent parts versus a proper two-coloring function are distinct constructions with the same existence predicate.

**Variant 1:** `form.wave2.bridge136.simple-bipartite.1` (meaning.wave2.bridge136.simple-bipartite)

```text
A simple undirected graph G=(V,E) is bipartite if there are disjoint subsets A,B⊆V with A∪B=V and every edge {u,v}∈E has one endpoint in A and the other in B; either part may be empty.
```

**Variant 2:** `form.wave2.bridge136.simple-bipartite.2` (meaning.wave2.bridge136.simple-bipartite)

```text
A simple undirected graph G=(V,E) is bipartite if there exists a function c:V→{0,1} such that c(u)≠c(v) for every edge {u,v}∈E; surjectivity of c is not required.
```

### 3. boundary of a subset in a topological space

**Reason for review:** Closure minus interior versus intersection of closures of a set and its complement give distinct set-theoretic expressions.

**Variant 1:** `form.wave2.cross107.topological-boundary.1` (meaning.wave2.cross107.topological-boundary)

```text
For a subset A of a topological space X, its boundary is ∂_X A=cl_X(A)\int_X(A), the points in the closure of A that are not interior to A.
```

**Variant 2:** `form.wave2.cross107.topological-boundary.2` (meaning.wave2.cross107.topological-boundary)

```text
Equivalently, for A⊆X in a topological space, the boundary is ∂_X A=cl_X(A)∩cl_X(X\A), where X\A is the complement relative to the given ambient X.
```

### 4. Bounded linear operator

**Reason for review:** Original statement does not explicitly restrict the scalar field, while the researched one restricts to real or complex normed spaces. Although the displayed formula is the same, the unqualified ambient normed-space convention is potentially broader; do not merge without user review.

**Variant 1:** `form.meaning.wave2.pop142.bounded-linear` (meaning.wave2.pop142.bounded-linear)

```text
Let X,Y be normed vector spaces over the same field F∈{ℝ,ℂ} and T:X→Y a linear map. T is bounded if there exists a real M≥0 such that ||Tx||_Y≤M||x||_X for every x∈X.
```

**Variant 2:** `form.mathdef.original.functional.bounded-linear-operator.primary` (meaning.mathdef.original.functional.bounded-linear-operator)

```text
A linear map $T:X\to Y$ between normed spaces is bounded if some $C\ge0$ satisfies $\|Tx\|_Y\le C\|x\|_X$ for all $x\in X$.
```

### 5. chromatic number

**Reason for review:** Finite nonempty graph definition versus unrestricted graph and empty-graph convention. Retain until the precise scope and infinite-color extension are reconciled.

**Variant 1:** `form.wave2.research81.chromatic-proper-coloring.01` (meaning.wave2.research81.chromatic-proper-coloring)

```text
For a finite simple undirected graph G having at least one vertex, the chromatic number χ(G) is the smallest positive integer k for which there exists c:V(G)→{1,…,k} with c(u)≠c(v) for every edge {u,v}∈E(G).
```

**Variant 2:** `form.mathdef.original.graph.chromatic-number.primary` (meaning.mathdef.original.graph.chromatic-number)

```text
The chromatic number $\chi(G)$ of a simple undirected graph $G$ is the least number of colors needed to assign colors to its vertices so that adjacent vertices receive different colors. The empty graph has chromatic number $0$ under this convention; a nonempty edgeless graph has chromatic number $1$.
```

### 6. Closure

**Reason for review:** Original primary already includes smallest closed superset and neighborhood characterization; remove repeated neighborhood card, retain metric distance-to-A=0, first-countable sequential limits, and Kuratowski closure-operator axioms as mathematically different objects/assumptions.

**Variant 1:** `form.mathdef.original.topology.closure.primary` (meaning.mathdef.original.topology.closure)

```text
For a subset $A$ of a topological space $X$, its closure $\overline A$ is the smallest closed set containing $A$, equivalently the intersection of all closed subsets containing $A$. A point $x$ lies in $\overline A$ if and only if every open neighborhood of $x$ intersects $A$. No sequential characterization is valid in complete generality without additional countability assumptions.
```

**Variant 2:** `form.mathdef.original.topology.closure.metric` (meaning.mathdef.original.topology.closure)

```text
If $(X,d)$ is a metric space and $A\subseteq X$, then $\overline A=\{x\in X: d(x,A)=0\}$, where $d(x,A)=\inf\{d(x,a):a\in A\}$ and $\inf\varnothing=+\infty$. Equivalently, every open ball about $x$ meets $A$.
```

**Variant 3:** `form.mathdef.original.topology.closure.sequences` (meaning.mathdef.original.topology.closure)

```text
If $X$ is first-countable (in particular, if $X$ is metrizable) and $A\subseteq X$, then $x\in\overline A$ if and only if there is a sequence $(a_n)$ in $A$ converging to $x$. In a general topological space, sequential limits can fail to exhaust $\overline A$.
```

**Variant 4:** `form.mathdef.original.topology.closure.kuratowski` (meaning.mathdef.original.topology.closure)

```text
A topological closure may equivalently be specified by a map $c:\mathcal P(X)\to\mathcal P(X)$ satisfying $c(\varnothing)=\varnothing$, $A\subseteq c(A)$, $c(A\cup B)=c(A)\cup c(B)$, and $c(c(A))=c(A)$. The closed sets of the corresponding topology are exactly the fixed points $F=c(F)$.
```

### 7. compact topological space

**Reason for review:** Finite subcovers versus finite intersection property of closed sets are mathematically informative dual criteria; the empty-family convention remains explicit.

**Variant 1:** `form.wave2.broad67.compact-open-cover` (meaning.wave2.broad67.compact-topological-space)

```text
A topological space X is compact if every open cover of X contains a finite subfamily whose union is X.
```

**Variant 2:** `form.wave2.broad67.compact-closed-fip` (meaning.wave2.broad67.compact-topological-space)

```text
Equivalently, X is compact if every nonempty family of closed subsets of X that has the finite intersection property has nonempty total intersection.
```

### 8. connected space

**Reason for review:** No separation, absence of nontrivial clopen subsets, and nonexistence of a continuous surjection onto the discrete two-point space are distinct characterizations under mathDef's empty-allowed convention.

**Variant 1:** `form.wave2.variant71.connected.01` (meaning.wave2.variant71.connected-empty-allowed)

```text
A topological space X is connected if it cannot be written as the union of two disjoint nonempty open subsets.
```

**Variant 2:** `form.wave2.variant71.connected.02` (meaning.wave2.variant71.connected-empty-allowed)

```text
A topological space X is connected precisely when its only subsets that are both open and closed are ∅ and X.
```

**Variant 3:** `form.wave2.variant71.connected.03` (meaning.wave2.variant71.connected-empty-allowed)

```text
A topological space X is connected precisely when there is no continuous surjection from X onto the discrete two-element space.
```

### 9. continuous map

**Reason for review:** Preimages of open subsets versus pointwise local-neighborhood behavior are distinct characterizations.

**Variant 1:** `form.wave2.foundation76.continuous-topological-map.01` (meaning.wave2.foundation76.continuous-topological-map)

```text
A map f:X→Y between topological spaces is continuous when, for every open subset V⊆Y, the inverse image f^{-1}(V) is open in X.
```

**Variant 2:** `form.wave2.foundation76.continuous-topological-map.02` (meaning.wave2.foundation76.continuous-topological-map)

```text
A map f:X→Y is continuous when for each x∈X and each open neighborhood V of f(x) in Y there exists an open neighborhood U of x in X such that f(U)⊆V.
```

### 10. convex hull of a subset of a real vector space

**Reason for review:** Finite convex-combination construction versus intersection of all convex supersets are distinct, informative perspectives; trivial least-superset paraphrase consolidated.

**Variant 1:** `form.wave2.cross133.convex-hull-real.1` (meaning.wave2.cross133.convex-hull-real)

```text
For a real vector space V and U⊆V, conv(U) is the set of sums ∑_{j=1}^m λ_j u_j with m≥1, u_j∈U, λ_j>0 for all j, and ∑_{j=1}^m λ_j=1; conv(∅)=∅.
```

**Variant 2:** `form.wave2.cross133.convex-hull-real.2` (meaning.wave2.cross133.convex-hull-real)

```text
For a real vector space V and U⊆V, conv(U)=⋂{C⊆V:C is convex and U⊆C}, the intersection of every convex subset containing U.
```

### 11. coprime polynomials

**Reason for review:** Unit ideal generated by the pair versus no common zero in an algebraic closure uses ideal and algebraic-geometric formulations.

**Variant 1:** `form.e606496d592fe305.relatively-prime-polynomials` (meaning.e606496d592fe305.relatively-prime-polynomials)

```text
Polynomials f,g∈k[x] over a field k are relatively prime when the ideal (f,g) they generate is the entire polynomial ring k[x].
```

**Variant 2:** `form.e606496d592fe305.relatively-prime-polynomials-roots` (meaning.e606496d592fe305.relatively-prime-polynomials)

```text
Two polynomials f,g over a field k are relatively prime if and only if they have no common zero in an algebraic closure of k.
```

### 12. degree of a vertex in a simple undirected graph

**Reason for review:** Cardinality of incident edges versus cardinality of adjacent vertices uses two different sets; equality relies on graph simplicity.

**Variant 1:** `form.wave2.cross133.vertex-degree-simple.1` (meaning.wave2.cross133.vertex-degree-simple)

```text
For a simple undirected graph G=(V,E) and v∈V, deg_G(v) is the cardinality of the set {e∈E:v∈e} of edges incident to v.
```

**Variant 2:** `form.wave2.cross133.vertex-degree-simple.2` (meaning.wave2.cross133.vertex-degree-simple)

```text
For a simple undirected graph G=(V,E) and v∈V, deg_G(v)=|{u∈V:{u,v}∈E}|, the number or cardinality of distinct vertices adjacent to v.
```

### 13. discrete valuation ring

**Reason for review:** Valuation-group characterization versus local-PID/nonfield construction; mathematically informative equivalent characterizations.

**Variant 1:** `form.f72779e263dd3e51.discrete-valuation-ring-value-group` (meaning.f72779e263dd3e51.discrete-valuation-ring-value-group)

```text
A valuation ring is a discrete valuation ring in the Stacks convention if its associated ordered value group is isomorphic to Z, with its usual order.
```

**Variant 2:** `form.mathdef.original.arithmetic.discrete-valuation-ring.primary` (meaning.mathdef.original.arithmetic.discrete-valuation-ring)

```text
A discrete valuation ring is an integral domain $R$ with fraction field $K$ admitting a surjective valuation $v:K^\times\to\mathbb Z$ for which $R=\{0\}\cup\{x\in K^\times:v(x)\ge0\}$. Equivalently, it is a local principal ideal domain that is not a field. Its unique nonzero maximal ideal is generated by an element of valuation $1$, called a uniformizer.
```

### 14. eigenvalue of a field-linear operator

**Reason for review:** Nontrivial kernel versus existence of a nonzero eigenvector use different algebraic presentations.

**Variant 1:** `form.wave2.branch129.operator-eigenvalue.1` (meaning.wave2.branch129.operator-eigenvalue)

```text
For a K-vector space V and K-linear operator A:V→V, λ∈K is an eigenvalue of A if ker(A−λI_V)≠{0_V}, where I_V is the identity map of V.
```

**Variant 2:** `form.wave2.branch129.operator-eigenvalue.2` (meaning.wave2.branch129.operator-eigenvalue)

```text
Equivalently, for such a K-linear endomorphism A, λ∈K is an eigenvalue exactly if some nonzero v∈V satisfies A(v)=λv.
```

### 15. eigenvector of a linear operator

**Reason for review:** Av=λv condition versus nonzero membership in ker(A−λI) introduces the kernel construction.

**Variant 1:** `form.wave2.conv126.eigenvector-linear-operator.1` (meaning.wave2.conv126.eigenvector-linear-operator)

```text
Let K be a field, V a K-vector space, A:V→V a K-linear operator and λ∈K an eigenvalue of A. A vector v∈V is an eigenvector for λ when v≠0 and A(v)=λv.
```

**Variant 2:** `form.wave2.conv126.eigenvector-linear-operator.2` (meaning.wave2.conv126.eigenvector-linear-operator)

```text
Under the same K-linear operator A:V→V and eigenvalue λ∈K, v is a corresponding eigenvector if v≠0 and v∈ker(A−λI_V), where I_V is the identity map of V.
```

### 16. formally unramified ring homomorphism

**Reason for review:** Uniqueness of square-zero liftings versus vanishing of Kähler differentials uses different universal and infinitesimal constructions.

**Variant 1:** `form.44fae2299dfd2f0a.formally-unramified-map` (meaning.44fae2299dfd2f0a.formally-unramified-map)

```text
A ring homomorphism R→S is formally unramified if, for every R-algebra A and square-zero ideal I⊆A, any R-algebra map S→A/I admits at most one lift to an R-algebra map S→A.
```

**Variant 2:** `form.44fae2299dfd2f0a.formally-unramified-differential-test` (meaning.44fae2299dfd2f0a.formally-unramified-map)

```text
A ring homomorphism R→S is formally unramified exactly when its module of Kähler differentials Ω_{S/R} is zero.
```

### 17. fraction field of an integral domain

**Reason for review:** Explicit construction by equivalence classes of fractions versus the universal mapping property are different mathematical perspectives.

**Variant 1:** `form.wave2.integer59.fraction-field-integral-domain` (meaning.wave2.integer59.fraction-field-integral-domain)

```text
For a commutative integral domain D, the fraction field Frac(D) is constructed from pairs (a,b) with a∈D and 0≠b∈D, where (a,b)∼(c,d) iff ad=bc. The class of (a,b) is written a/b; addition and multiplication are defined on such classes so that D embeds into the resulting field.
```

**Variant 2:** `form.wave2.integer59.fraction-field-universal` (meaning.wave2.integer59.fraction-field-integral-domain)

```text
Equivalently, a fraction field of an integral domain D is a field F with an injective ring map i:D→F satisfying: for every field K and injective ring map j:D→K, there exists a unique field homomorphism h:F→K for which h∘i=j.
```

### 18. Free module

**Reason for review:** One definition explicitly assumes unital left modules while the other just says R-module. Retain both for review of the ring/module convention.

**Variant 1:** `form.meaning.wave2.direct.7462fa5f90275b34779a` (meaning.wave2.direct.7462fa5f90275b34779a)

```text
Let R be an associative unital ring and F a unital left R-module. The module F is free if it has a basis B such that every element of F has a unique finite expression ∑_{b∈B} r_b b with coefficients r_b∈R. Equivalently F≅⊕_{b∈B}R as a left R-module. The empty basis gives the zero module; no finite-rank assumption is made.
```

**Variant 2:** `form.mathdef.original.commalg.free-module.primary` (meaning.mathdef.original.commalg.free-module)

```text
An $R$-module is free if it is isomorphic to a direct sum of copies of $R$, equivalently if it admits an $R$-module basis.
```

### 19. Function

**Reason for review:** The assignment X→Y formulation and the graph-as-total-single-valued-relation subset of X×Y are distinct foundational encodings. Preserve both, including typed domain/codomain.

**Variant 1:** `form.mathdef.original.functions.function.primary` (meaning.mathdef.original.functions.function)

```text
A function $f:X\to Y$ assigns to each $x\in X$ exactly one element $f(x)\in Y$. The set $X$ is the domain and $Y$ is the codomain.
```

**Variant 2:** `form.mathdef.original.functions.function.graph` (meaning.mathdef.original.functions.function)

```text
For sets $X$ and $Y$, a function from $X$ to $Y$ is a subset $f\subseteq X\times Y$ of their Cartesian product such that for every $x\in X$ there exists a unique $y\in Y$ satisfying $(x,y)\in f$. The set $X$ is its domain, $Y$ is its specified codomain, and $f(x)$ denotes this unique $y$. Equivalently, the relation $f$ is total and single-valued on $X$.
```

### 20. geometrically integral algebra

**Reason for review:** All field extensions remaining domains versus the algebraic-closure base-change test are informative distinct criteria.

**Variant 1:** `form.831db4eab7a244a4.geometrically-integral-algebra` (meaning.831db4eab7a244a4.geometrically-integral-algebra)

```text
A k-algebra A is geometrically integral when, for every field extension K/k, the tensor-product algebra A⊗_k K is an integral domain.
```

**Variant 2:** `form.831db4eab7a244a4.geometrically-integral-algebra-closure-test` (meaning.831db4eab7a244a4.geometrically-integral-algebra)

```text
Equivalently, a k-algebra A is geometrically integral when A⊗_k k̄ is an integral domain, where k̄ is an algebraic closure of k.
```

### 21. geometrically normal algebra

**Reason for review:** Testing all field extensions versus the single perfect-closure scalar extension is an informative reduction of the verification domain.

**Variant 1:** `form.2a93c6a662a51d67.geometrically-normal-algebra` (meaning.2a93c6a662a51d67.geometrically-normal-algebra)

```text
A k-algebra A is geometrically normal over a field k if for every extension of fields K/k the base-changed algebra K⊗_k A is a normal ring.
```

**Variant 2:** `form.2a93c6a662a51d67.geometrically-normal-perfect-closure-test` (meaning.2a93c6a662a51d67.geometrically-normal-algebra)

```text
Equivalently, a k-algebra A is geometrically normal if its scalar extension k^perf⊗_k A to the perfect closure of k is a normal ring; this also tests normality over all finite purely inseparable field extensions.
```

### 22. geometrically reduced algebra

**Reason for review:** Every field scalar extension versus perfect-closure test gives an informative simplification of the extension quantifier.

**Variant 1:** `form.6c51aeb904a0fe74.geometrically-reduced-algebra` (meaning.6c51aeb904a0fe74.geometrically-reduced-algebra)

```text
A k-algebra A is geometrically reduced if for every field extension K/k the tensor-product K-algebra A⊗_k K is a reduced ring.
```

**Variant 2:** `form.6c51aeb904a0fe74.geometric-reducedness-perfect-test` (meaning.6c51aeb904a0fe74.geometrically-reduced-algebra)

```text
Equivalently, A is geometrically reduced over k if A⊗_k k^perf is reduced, where k^perf denotes the perfect closure of k; this is a field-extension test of the same property.
```

### 23. Hausdorff space

**Reason for review:** Separating distinct points by open neighborhoods versus closedness of the diagonal in X×X are genuinely distinct tests.

**Variant 1:** `form.e62923cd8ef99cd1.hausdorff-space` (meaning.e62923cd8ef99cd1.hausdorff-space)

```text
A topological space X is Hausdorff if every pair of distinct points has disjoint open neighbourhoods.
```

**Variant 2:** `form.e62923cd8ef99cd1.hausdorff-diagonal-characterization` (meaning.e62923cd8ef99cd1.hausdorff-space)

```text
A topological space X is Hausdorff exactly when the diagonal {(x,x):x∈X} is a closed subset of X×X with its product topology.
```

### 24. homeomorphism

**Reason for review:** Continuous bijection with continuous inverse versus preservation and reflection of open sets are distinct useful tests.

**Variant 1:** `form.wave2.directional113.homeomorphism-topological.1` (meaning.wave2.directional113.homeomorphism-topological)

```text
For topological spaces X and Y, a map f:X→Y is a homeomorphism if f is bijective, f is continuous and its inverse map f⁻¹:Y→X is continuous.
```

**Variant 2:** `form.wave2.directional113.homeomorphism-topological.2` (meaning.wave2.directional113.homeomorphism-topological)

```text
Equivalently, a bijection f:X→Y between topological spaces is a homeomorphism if for every U⊆X, U is open in X exactly when f[U] is open in Y.
```

### 25. Jacobson radical

**Reason for review:** Intersection of maximal ideals versus invertibility of 1−xy for all y uses distinct ideal versus unit tests.

**Variant 1:** `form.90b0d1ecfa394230.jacobson-radical-ring` (meaning.90b0d1ecfa394230.jacobson-radical-ring)

```text
For a commutative ring R, its Jacobson radical Jac(R) is the intersection of all maximal ideals of R.
```

**Variant 2:** `form.90b0d1ecfa394230.jacobson-radical-unit-test` (meaning.90b0d1ecfa394230.jacobson-radical-ring)

```text
Equivalently, an element x∈R belongs to Jac(R) exactly when 1−xy is invertible in R for every y∈R.
```

### 26. Jacobson ring

**Reason for review:** Radical-ideal intersection criterion versus the prime-ideal-only criterion is a substantive commutative-algebra equivalence.

**Variant 1:** `form.03b55b8ca41abb20.jacobson-ring` (meaning.03b55b8ca41abb20.jacobson-ring)

```text
A commutative ring R is a Jacobson ring when every radical ideal I of R equals the intersection of the maximal ideals of R containing I.
```

**Variant 2:** `form.03b55b8ca41abb20.jacobson-ring-prime-characterization` (meaning.03b55b8ca41abb20.jacobson-ring)

```text
Equivalently, a commutative ring R is Jacobson if each prime ideal p is the intersection of all maximal ideals containing p.
```

### 27. local ring

**Reason for review:** Unique maximal ideal versus the ideal of nonunits provides a distinct criterion.

**Variant 1:** `form.4f7edb6d32334f67.local-ring-unique-maximal` (meaning.4f7edb6d32334f67.local-ring-unique-maximal)

```text
A nonzero commutative ring R is local if it possesses exactly one maximal ideal.
```

**Variant 2:** `form.4f7edb6d32334f67.local-ring-nonunit-ideal` (meaning.4f7edb6d32334f67.local-ring-unique-maximal)

```text
Equivalently, a nonzero commutative ring R is local if the set of its nonunits is an ideal; this ideal is necessarily the ring's unique maximal ideal.
```

### 28. martingale

**Reason for review:** Discrete indexed conditional-expectation equations and continuous-time martingale filtration structure use different time domains.

**Variant 1:** `form.wave2.research81.martingale-discrete.01` (meaning.wave2.research81.martingale-discrete)

```text
A real-valued discrete-time process (X_n)_{n≥0}, adapted to a filtration (F_n)_{n≥0} and satisfying E|X_n|<∞ for every n, is a martingale if E[X_{n+1}|F_n]=X_n almost surely for each n≥0.
```

**Variant 2:** `form.wave2.research81.martingale-discrete.02` (meaning.wave2.research81.martingale-discrete)

```text
An integrable adapted real-valued discrete-time process (X_n,F_n)_{n≥0} is a martingale if E[X_m|F_n]=X_n almost surely whenever 0≤n≤m are integers.
```

**Variant 3:** `form.wave2.research81.martingale-continuous-index.01` (meaning.wave2.research81.martingale-continuous-index)

```text
A real-valued process (X_t)_{t≥0} adapted to a filtration (F_t)_{t≥0}, with E|X_t|<∞ for every t≥0, is a martingale if E[X_t|F_s]=X_s almost surely whenever 0≤s≤t.
```

### 29. metric space

**Reason for review:** Metric axioms and metric-induced compatible topology are related but not near-verbatim variants; retain for manual editorial decision.

**Variant 1:** `form.wave2.analysis98.metric-space` (meaning.wave2.analysis98.metric-space)

```text
A metric space is a pair (X,d) where X is a nonempty set and d:X×X→ℝ satisfies d(x,x)=0, symmetry d(x,y)=d(y,x), the triangle inequality d(x,z)≤d(x,y)+d(y,z), and d(x,y)>0 whenever x≠y.
```

**Variant 2:** `form.wave2.analysis98.metric-space.compatible` (meaning.wave2.analysis98.metric-space)

```text
For a nonempty set X with a metric d, the balls B_d(x,r)={y in X:d(x,y)<r}, r>0, generate a canonical topology τ_d. The metric-space data (X,d) determine the compatible triple (X,τ_d,d), and conversely a triple (X,τ,d) with τ=τ_d determines (X,d). A metrizable topology alone does not specify a unique metric.
```

### 30. minimal polynomial

**Reason for review:** Least-degree monic annihilating polynomial versus a monic generator of the evaluation kernel use different defining constructions.

**Variant 1:** `form.3aaa8d6f2195bb8e.minimal-polynomial` (meaning.3aaa8d6f2195bb8e.minimal-polynomial)

```text
If an element alpha of an extension E/k is algebraic over k, its minimal polynomial over k is the unique monic polynomial generating the kernel of evaluation k[t] to E at alpha; it is irreducible over k.
```

**Variant 2:** `form.mathdef.original.arithmetic.minimal-polynomial.primary` (meaning.mathdef.original.arithmetic.minimal-polynomial)

```text
If $\alpha$ is algebraic over a field $K$, its minimal polynomial over $K$ is the unique monic polynomial $m_{\alpha,K}\in K[x]$ of smallest positive degree satisfying $m_{\alpha,K}(\alpha)=0$. It is irreducible and divides every polynomial in $K[x]$ that vanishes at $\alpha$.
```

### 31. Noetherian module

**Reason for review:** Finite generation of submodules, ACC, and inclusion-maximal-element conditions are useful alternate tests.

**Variant 1:** `form.wave2.foundation76.noetherian-module.01` (meaning.wave2.foundation76.noetherian-module)

```text
A module M over a commutative ring A with identity is Noetherian when every A-submodule of M is finitely generated.
```

**Variant 2:** `form.wave2.foundation76.noetherian-module.02` (meaning.wave2.foundation76.noetherian-module)

```text
A module M over a commutative unital ring A is Noetherian when every ascending sequence M_1⊆M_2⊆⋯ of A-submodules becomes constant from some index onward.
```

**Variant 3:** `form.wave2.foundation76.noetherian-module.03` (meaning.wave2.foundation76.noetherian-module)

```text
A module M over a commutative unital ring A is Noetherian when every nonempty collection of its A-submodules has an inclusion-maximal member.
```

### 32. Noetherian ring

**Reason for review:** Finitely generated ideals, ACC, maximal condition, and module Noetherianity give useful mathematically different tests.

**Variant 1:** `form.86b5d488b98c612f.noetherian-commutative-ring` (meaning.86b5d488b98c612f.noetherian-commutative-ring)

```text
A commutative ring R with identity is Noetherian if every ideal of R is finitely generated.
```

**Variant 2:** `form.wave2.variant71.noetherian.ascending-chain-condition` (meaning.86b5d488b98c612f.noetherian-commutative-ring)

```text
A commutative ring R is Noetherian if every ascending chain of ideals I_1⊆I_2⊆⋯ stabilizes.
```

**Variant 3:** `form.wave2.variant71.noetherian.maximal-condition` (meaning.86b5d488b98c612f.noetherian-commutative-ring)

```text
A commutative ring R is Noetherian if each nonempty collection of ideals of R has a maximal element under inclusion.
```

**Variant 4:** `form.wave2.variant71.noetherian.noetherian-as-module` (meaning.86b5d488b98c612f.noetherian-commutative-ring)

```text
A commutative ring R is Noetherian if R, regarded as a left R-module over itself, is Noetherian.
```

### 33. normal algebraic extension

**Reason for review:** Splitting of each irreducible polynomial with a root versus splitting of each element's minimal polynomial are informative equivalent characterizations.

**Variant 1:** `form.50d335de00e5f11d.normal-algebraic-extension` (meaning.50d335de00e5f11d.normal-algebraic-extension)

```text
An algebraic extension K/k is normal if every irreducible polynomial over k having one root in K splits completely into linear factors over K.
```

**Variant 2:** `form.ac17dab9530c0b80.normal-algebraic-field-extension` (meaning.ac17dab9530c0b80.normal-algebraic-field-extension)

```text
An algebraic field extension E/F is normal if the minimal polynomial over F of each element α∈E factors completely into linear factors over E.
```

### 34. normal subgroup

**Reason for review:** Coset equality, equality under conjugation, and conjugation inclusion for every group element are distinct useful algebraic tests.

**Variant 1:** `form.wave2.quot119.normal-subgroup.1` (meaning.wave2.quot119.normal-subgroup)

```text
For a group G and a subgroup N≤G, N is normal in G if gN=Ng for every element g∈G, where gN={gn:n∈N} and Ng={ng:n∈N}.
```

**Variant 2:** `form.wave2.quot119.normal-subgroup.2` (meaning.wave2.quot119.normal-subgroup)

```text
For a group G and subgroup N≤G, N is normal precisely when gNg⁻¹=N for every g∈G, with gNg⁻¹={gng⁻¹:n∈N}.
```

**Variant 3:** `form.wave2.quot119.normal-subgroup.3` (meaning.wave2.quot119.normal-subgroup)

```text
For a group G and subgroup N≤G, N is normal if gNg⁻¹⊆N for every g∈G; demanding this inclusion for every g, including its inverse, forces equality.
```

### 35. Operator norm

**Reason for review:** Original statement does not explicitly restrict the scalar field, while the researched one restricts to real or complex normed spaces. Although the displayed formula is the same, the unqualified ambient normed-space convention is potentially broader; do not merge without user review.

**Variant 1:** `form.meaning.wave2.pop142.bounded-operator-norm` (meaning.wave2.pop142.bounded-operator-norm)

```text
For a bounded linear T:X→Y between real or complex normed vector spaces, define ||T||=sup{||Tx||_Y : x∈X, ||x||_X≤1}. This is a finite nonnegative real number.

Equivalent formulation: For bounded linear T:X→Y between real or complex normed spaces, equivalently ||T||=inf{M>0 : ||Tx||_Y≤M||x||_X for all x∈X}, with infimum taken in [0,+∞].
```

**Variant 2:** `form.mathdef.original.functional.operator-norm.primary` (meaning.mathdef.original.functional.operator-norm)

```text
For a bounded linear operator $T:X\to Y$, the operator norm is $\|T\|=\sup_{\|x\|\le1}\|Tx\|$.
```

### 36. orbit of an element under a group action

**Reason for review:** Explicit translate set G·x versus equivalence class under the action-induced equivalence relation are different constructions.

**Variant 1:** `form.wave2.group116.group-orbit.1` (meaning.wave2.group116.group-orbit)

```text
Let G be a group acting on a set X on the left and x∈X. The orbit of x is G·x={g·x:g∈G}={y∈X:there exists g∈G with y=g·x}.
```

**Variant 2:** `form.wave2.group116.group-orbit.2` (meaning.wave2.group116.group-orbit)

```text
For a left G-action on X, define x∼_G y when some g∈G satisfies y=g·x. The orbit of x is its equivalence class [x] under this action-induced equivalence relation.
```

### 37. product topology of a family of topological spaces

**Reason for review:** Projection-inverse-image subbasis versus finite-support box basis uses distinct generating families.

**Variant 1:** `form.wave2.branch129.indexed-product-topology.1` (meaning.wave2.branch129.indexed-product-topology)

```text
Let {(X_i,τ_i)}_{i∈I} be topological spaces and X=∏_{i∈I}X_i, with projection π_i:X→X_i. The product topology on X is the topology generated by the subbasis {π_i⁻¹(U):i∈I,U∈τ_i}.
```

**Variant 2:** `form.wave2.branch129.indexed-product-topology.2` (meaning.wave2.branch129.indexed-product-topology)

```text
For the same indexed topological spaces, the product topology is generated by the basis of all products ∏_{i∈I}U_i with each U_i open in X_i and U_i=X_i for all but finitely many i∈I.
```

### 38. profinite space via finite inverse limits

**Reason for review:** Inverse-limit construction versus compact Hausdorff totally disconnected characterization are substantially different frameworks.

**Variant 1:** `form.7368f71dcc6adfef.profinite-topological-space` (meaning.7368f71dcc6adfef.profinite-topological-space)

```text
A topological space X is profinite when it is homeomorphic to an inverse limit of finite discrete topological spaces.
```

**Variant 2:** `form.7368f71dcc6adfef.profinite-space-compact-characterization` (meaning.7368f71dcc6adfef.profinite-topological-space)

```text
Equivalently, a topological space is profinite exactly when it is quasi-compact, Hausdorff, and totally disconnected.
```

### 39. pure ideal

**Reason for review:** Flatness of R/I versus I∩J=IJ for every ideal J uses different module/ideal conditions.

**Variant 1:** `form.3fe40ac4fb74bff2.pure-ideal` (meaning.3fe40ac4fb74bff2.pure-ideal)

```text
An ideal I in a commutative ring R is pure if the quotient module R/I is flat over R.
```

**Variant 2:** `form.3fe40ac4fb74bff2.pure-ideal-intersection-test` (meaning.3fe40ac4fb74bff2.pure-ideal)

```text
Equivalently, an ideal I⊆R is pure when I∩J=IJ for every ideal J of R; it is enough to test finitely generated ideals J.
```

### 40. rational number

**Reason for review:** Real fraction representation versus formal fraction-field construction of Q.

**Variant 1:** `form.mathdef.original.number.rational-number.primary` (meaning.mathdef.original.number.rational-number)

```text
A rational number is a real number expressible as $a/b$ with $a,b\in\mathbb Z$ and $b\ne0$. Two such fractions $a/b$ and $c/d$ represent the same rational number precisely when $ad=bc$. The rationals form the field $\mathbb Q$.
```

**Variant 2:** `form.wave2.rational55.rational-number` (meaning.wave2.rational55.rational-number)

```text
A rational number is an element of Q, the field of fractions of Z. Concretely, every rational number can be represented as p/q for integers p and nonzero q, with p/q=r/s precisely when ps=rq for nonzero q,s.
```

### 41. reduced scheme

**Reason for review:** Every local ring reduced versus all open-section rings reduced is a different local-to-global formulation.

**Variant 1:** `form.6a21c2d4f3354c8f.reduced-scheme` (meaning.6a21c2d4f3354c8f.reduced-scheme)

```text
A scheme X is reduced if each local ring O_{X,x} is a reduced ring, meaning it contains no nonzero nilpotent element.
```

**Variant 2:** `form.6a21c2d4f3354c8f.reduced-scheme-sections-equivalent` (meaning.6a21c2d4f3354c8f.reduced-scheme)

```text
Equivalently, a scheme X is reduced exactly when the ring O_X(U) has no nonzero nilpotent elements for every open subset U of X.
```

### 42. set difference

**Reason for review:** Relative complement of a specified subset in an ambient set versus unrestricted A\B have different stated inputs; their exact redundancy is not adjudicated.

**Variant 1:** `form.mathdef.original.sets.complement.primary` (meaning.mathdef.original.sets.complement)

```text
Given a set $X$ and a subset $A\subseteq X$, the relative complement of $A$ in $X$ is $X\setminus A=\{x\in X:x\notin A\}$. Without a specified ambient universe, the notation $A^c$ is ambiguous. Relative complementation depends on $X$.
```

**Variant 2:** `form.mathdef.original.sets.difference.primary` (meaning.mathdef.original.sets.difference)

```text
For sets $A,B$, their set difference is $A\setminus B=\{x\in A:x\notin B\}$. Equivalently, it is the relative complement in $A$ of $A\cap B$. In general $A\setminus B$ differs from $B\setminus A$.
```

### 43. sigma-algebra

**Reason for review:** Complement closure plus countable unions versus differences plus disjoint countable unions use different closure axioms.

**Variant 1:** `form.wave2.foundation.sigma-algebra` (meaning.wave2.foundation.sigma-algebra)

```text
Let X be a set. A sigma-algebra on X is a family Σ⊆P(X) containing X, closed under taking complements X\A for A∈Σ, and closed under countable unions ⋃_{n≥1}A_n of members A_n∈Σ.
```

**Variant 2:** `form.wave2.broad67.sigma-difference-disjoint-countable` (meaning.wave2.foundation.sigma-algebra)

```text
Equivalently, a family Σ⊆P(X) is a σ-algebra if X∈Σ, it is closed under differences A\B for A,B∈Σ, and it is closed under countable unions of pairwise disjoint members.
```

### 44. Stirling numbers of the second kind

**Reason for review:** Recurrence and initial conditions versus expansion coefficients in a falling-factorial polynomial basis are mathematically different characterizations.

**Variant 1:** `form.wave2.cross133.stirling-second-kind.1` (meaning.wave2.cross133.stirling-second-kind)

```text
For n,k∈ℕ₀, the Stirling numbers of the second kind S(n,k) satisfy S(n,0)=δ_{n,0}, S(0,k)=δ_{0,k}, and for n,k≥1, S(n,k)=S(n−1,k−1)+k S(n−1,k), where δ is Kronecker's delta.
```

**Variant 2:** `form.wave2.cross133.stirling-second-kind.2` (meaning.wave2.cross133.stirling-second-kind)

```text
For each n∈ℕ₀, the Stirling numbers S(n,k) are the unique coefficients in the polynomial identity x^n=∑_{k=0}^n S(n,k)x^{\underline{k}}, where x^{\underline{0}}=1 and x^{\underline{k}}=x(x−1)⋯(x−k+1) for k≥1.
```


---

No manual-review case has been automatically merged. Permission is required before any deeper mathematical investigation of these cases.
