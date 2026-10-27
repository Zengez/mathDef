# Existing-heading cross-term review packet — surface screening

This packet covers only already-defined headings. No new terminology, extended source research or publication was performed.

**Scope and coverage:** The staged catalog's 2,013 headings were indexed once. Their 2,548 normalized title/alias keys and short existing definition snippets generated **992** cross-heading candidate pairs; each unordered pair was generated at most once. Candidate pairs include broad subject relationships and should **not** all be interpreted as duplicate mathematical meanings.

**Applied on cleanup branch:** 7 obvious duplicate-meaning mergers and 9 group-only alias migrations that retain substantively different mathematical formulations. 16 searchable headings retired to aliases. Stage-only CI [40565917496](https://github.com/Zengez/mathDef/actions/runs/40565917496) passed, preserving all 2,662 source identities, all historic original IDs, and the final-linking/publication gate.

**Disposition caution:** Title/alias indexing is a *cursory candidate screen*, not a proof that all 2,013 mathematical definitions have no unnamed synonyms. Pairs outside the shortlist were left as independent headings on the evidence of their existing text. This packet intentionally leaves any borderline mathematical question for manual review.

## Manual comparison — unmerged and ungrouped

These 22 pairs have potentially meaningful context, construction or assumption differences. The excerpts below are the first 310 characters of the preexisting staged wording, not new source research. Their inclusion requests a grouping judgment only.

### 1. minimal prime ideal / prime minimal over an ideal

**minimal prime ideal:** A prime ideal 𝔭 of a commutative ring R is a minimal prime if there is no prime ideal 𝔮 satisfying 𝔮⊊𝔭. Minimality is among the prime ideals ordered by inclusion; a minimal prime need not be the unique smallest prime.

**prime minimal over an ideal:** A prime ideal 𝔭 of a commutative ring R is minimal over ideal I if I⊆𝔭 and there is no prime 𝔮 satisfying I⊆𝔮⊊𝔭. Minimality is relative to primes containing I.

### 2. Algebraic closure of a field / Relative algebraic closure

**Algebraic closure of a field:** For a field $F$, an algebraic closure of $F$ is an extension field $\overline F/F$ such that every element of $\overline F$ is algebraic over $F$ and $\overline F$ is algebraically closed (every nonconstant polynomial in $\overline F[t]$ has a root in $\overline F$). Algebraic closures are unique up to $F$-is

**Relative algebraic closure:** Given an extension of fields $K/k$, the relative algebraic closure of $k$ in $K$ is the subfield $\{x\in K:x\text{ is algebraic over }k\}$. It need not be an algebraically closed field; in particular this differs from an algebraic closure of $k$.

### 3. Analytic Hardy space on the disk / Hardy Hilbert space on the disk

**Analytic Hardy space on the disk:** For $0<p<\infty$, the analytic Hardy space $H^p(\mathbb D)$ consists of holomorphic functions $f$ such that $$ \|f\|_{H^p}=\sup_{0<r<1}\left(\frac1{2\pi}\int_0^{2\pi}|f(re^{i\theta})|^p\,d\theta\right)^{1/p}<\infty. $$ For $p\ge1$ this is a norm and for $0<p<1$ it is a quasi-norm. The analogous space $H^\inft

**Hardy Hilbert space on the disk:** The Hardy Hilbert space $H^2(\mathbb D)$ consists of holomorphic $f(z)=\sum_{n=0}^\infty a_nz^n$ satisfying $\sum_n|a_n|^2<\infty$. For $g(z)=\sum_nb_nz^n$ its inner product, linear in the first argument, is $$ \langle f,g\rangle_{H^2}=\sum_{n=0}^\infty a_n\overline{b_n}. $$ Equivalently $\|f\|_{H^2}^2=\sup_{

### 4. Bergman space / Weighted Bergman space

**Bergman space:** For a domain $\Omega\subseteq\mathbb C^n$ and $0<p<\infty$, the Bergman space is $$ A^p(\Omega)=\left\{f\in\mathcal O(\Omega):\int_\Omega|f(z)|^p\,dV(z)<\infty\right\}. $$ Here $dV$ is the unweighted Euclidean volume measure. The functional $(\int|f|^p)^{1/p}$ is a norm for $p\ge1$, and a quasi-norm for $0<p<

**Weighted Bergman space:** Let $\Omega\subseteq\mathbb C^n$ be a domain and $\omega:\Omega\to(0,\infty)$ a continuous weight. For $0<p<\infty$, the weighted Bergman space is $$ A_\omega^p(\Omega)=\left\{f\in\mathcal O(\Omega):\int_\Omega |f(z)|^p\omega(z)\,dV(z)<\infty\right\}. $$ For $p\ge1$ the weighted $L^p$ expression yields a norm

### 5. Bloch space on the disk / Little Bloch space

**Bloch space on the disk:** The Bloch space $\mathcal B(\mathbb D)$ comprises holomorphic functions $f$ on $\mathbb D$ for which $$ \beta(f)=\sup_{z\in\mathbb D}(1-|z|^2)|f'(z)|<\infty. $$ The expression $\beta$ is a seminorm, since constants have seminorm zero. The norm $\|f\|_{\mathcal B}=|f(0)|+\beta(f)$ makes $\mathcal B(\mathbb D)$

**Little Bloch space:** The little Bloch space $\mathcal B_0(\mathbb D)$ is the subspace of Bloch functions $f$ satisfying $$ \lim_{|z|\to1^-}(1-|z|^2)|f'(z)|=0. $$ It is a closed subspace of the Bloch Banach space in the norm $|f(0)|+\sup_{z\in\mathbb D}(1-|z|^2)|f'(z)|$. The limit condition is stronger than merely having finite Bl

### 6. Cohen–Macaulay local ring / Cohen–Macaulay ring

**Cohen–Macaulay local ring:** A Noetherian local ring (R,m) is Cohen–Macaulay if its depth as an R-module equals its Krull dimension, that is, depth_m(R)=dim(R).

**Cohen–Macaulay ring:** A Noetherian commutative ring R is Cohen–Macaulay if for every maximal or prime ideal p, the local ring R_p is Cohen–Macaulay.

### 7. Cohen–Macaulay local module / global Cohen–Macaulay module

**Cohen–Macaulay local module:** A finitely generated module M over a Noetherian local ring R is Cohen–Macaulay if depth_R(M) equals the Krull dimension of the support Supp_R(M).

**global Cohen–Macaulay module:** A finite module M over a Noetherian ring R is Cohen–Macaulay if for each prime p the localized module M_p is Cohen–Macaulay over the local ring R_p.

### 8. I-adic completion of a Noetherian ring / I-adic completion of a ring

**I-adic completion of a Noetherian ring:** For a Noetherian commutative ring R and ideal I, the I-adic completion R^ is the inverse-limit ring lim_n R/I^n, with structure homomorphism R→R^ induced by the quotient maps.

**I-adic completion of a ring:** For a commutative ring R and ideal I, its I-adic completion R^ is the inverse limit of the quotient rings R/I^n over positive integers n, with transition maps given by reduction modulo smaller powers.

### 9. Tor-based local criterion for module flatness / Tor-vanishing criterion for module flatness

**Tor-based local criterion for module flatness:** For a local map of Noetherian local rings R→S with residue field k of R and a finitely generated S-module M, M is flat over R if and only if Tor_1^R(k,M)=0.

**Tor-vanishing criterion for module flatness:** An R-module M is flat if and only if Tor_1^R(M,R/I)=0 for every finitely generated ideal I⊆R; equivalently, Tor_i^R(M,N)=0 for all R-modules N and every i>0.

### 10. G-unramified at a target prime / unramified at a target prime

**G-unramified at a target prime:** For a ring map R→S and prime q of S, the map is G-unramified at q if there exists g outside q such that R→S_g is G-unramified.

**unramified at a target prime:** For a ring map R→S and a prime ideal q in S, the map is unramified at q if some g in S outside q makes the localized map R→S_g unramified.

### 11. Zariski topology on a scheme / Zariski topology on a spectrum

**Zariski topology on a scheme:** The Zariski topology of a scheme X is the topology of its underlying locally ringed space, characterized locally by requiring each affine chart Spec(R)⊆X to carry the prime-spectrum topology whose standard opens are D(f).

**Zariski topology on a spectrum:** The Zariski topology on $\operatorname{Spec}R$ has as closed subsets $V(I)$ for ideals $I\subseteq R$; its standard open subsets are $D(f)=\{\mathfrak p:f\notin\mathfrak p\}$.

### 12. box topology on a product of topological spaces / product topology of a family of topological spaces

**box topology on a product of topological spaces:** Given topological spaces (X_i,τ_i) indexed by I, the box topology on ∏_{i∈I}X_i is the topology with a basis consisting of every product ∏_{i∈I}U_i where U_i∈τ_i for all i. In contrast, the ordinary product topology requires U_i=X_i for all but finitely many i. Thus the box topology is at least as fine, and c

**product topology of a family of topological spaces:** Let {(X_i,τ_i)}_{i∈I} be topological spaces and X=∏_{i∈I}X_i, with projection π_i:X→X_i. The product topology on X is the topology generated by the subbasis {π_i⁻¹(U):i∈I,U∈τ_i}.

### 13. Reproducing kernel of a Hilbert function space / Reproducing-kernel Hilbert space

**Reproducing kernel of a Hilbert function space:** For an RKHS $\mathcal H$ on $X$, the reproducing kernel $K:X\times X\to\mathbb C$ is uniquely characterized by $K(\cdot,y)\in\mathcal H$ and $$ f(y)=\langle f,K(\cdot,y)\rangle_{\mathcal H}\qquad(f\in\mathcal H). $$ The inner product is taken linear in its first argument. Consequently $K(y,x)=\overline{K(x,y)

**Reproducing-kernel Hilbert space:** A reproducing-kernel Hilbert space (RKHS) on a set $X$ is a Hilbert space $\mathcal H$ of actual scalar-valued functions $f:X\to\mathbb C$ for which each evaluation map $\operatorname{ev}_x(f)=f(x)$ is a continuous linear functional. By the Riesz representation theorem, for each $x$ there is a unique kernel s

### 14. Categorical epimorphism / categorical epimorphism of rings

**Categorical epimorphism:** A morphism $f:A\to B$ in a category is an epimorphism if it is right-cancellable: for any object $X$ and any $g,h:B\to X$, the equation $g\circ f=h\circ f$ implies $g=h$. Epimorphisms need not be surjective set maps in concrete categories, and an epimorphism need not be an isomorphism.

**categorical epimorphism of rings:** A ring homomorphism f:R→S is an epimorphism in the category of commutative rings if every pair of ring maps g,h:S→T satisfying g∘f=h∘f are equal; equivalently the multiplication map S⊗_R S→S is an isomorphism.

### 15. Conditional independence of events / Independence of events

**Conditional independence of events:** For events $A,B,C$ with $P(C)>0$, $A$ and $B$ are conditionally independent given the event $C$ if $P(A\cap B\mid C)=P(A\mid C)P(B\mid C)$.

**Independence of events:** Events $A,B$ in a probability space are independent if $P(A\cap B)=P(A)P(B)$. For a family of events, mutual independence means that for every finite subfamily $A_1,\ldots,A_m$, one has $P(\bigcap_{j=1}^m A_j)=\prod_{j=1}^mP(A_j)$. Pairwise independence is a weaker property.

### 16. formally unramified ring homomorphism / unramified ring homomorphism

**formally unramified ring homomorphism:** A ring homomorphism R→S is formally unramified if, for every R-algebra A and square-zero ideal I⊆A, any R-algebra map S→A/I admits at most one lift to an R-algebra map S→A.

**unramified ring homomorphism:** A homomorphism of commutative rings R→S is unramified in the Stacks Project convention when S is finitely generated as an R-algebra and the module of Kähler differentials Ω_{S/R} is zero.

### 17. Lebesgue measure / Lebesgue–Stieltjes measure

**Lebesgue measure:** The $n$-dimensional Lebesgue measure $\lambda_n$ on $\mathbb R^n$ is the completion of the Borel measure assigning an axis-parallel half-open rectangle $\prod_{j=1}^{n}[a_j,b_j)$ the volume $\prod_{j=1}^n(b_j-a_j)$. It is translation invariant, and $\lambda_n(\{x\})=0$ for every point when $n\ge1$. The comple

**Lebesgue–Stieltjes measure:** Let F:ℝ→ℝ be nondecreasing and right-continuous. Its Lebesgue–Stieltjes measure μ_F is the unique locally finite Borel measure on ℝ satisfying μ_F((a,b])=F(b)−F(a) for finite a<b. The right-continuity assumption is needed for this half-open-interval convention.

### 18. pure short exact sequence / Short exact sequence

**pure short exact sequence:** A short exact sequence 0→M_1→M_2→M_3→0 of R-modules is universally exact if the first nonzero arrow M_1→M_2 remains injective after tensoring with any R-module; equivalently the entire sequence remains exact after every such tensor product.

**Short exact sequence:** A short exact sequence of $R$-modules is $0\to A\xrightarrow{f}B\xrightarrow{g}C\to0$ with $f$ injective, $g$ surjective, and $\operatorname{im}f=\ker g$.

### 19. free abelian group / Free module

**free abelian group:** An abelian group A is free abelian if it admits a subset B⊆A such that every a∈A can be written uniquely as a FINITE integer linear combination ∑_{b∈B}n_b b, n_b∈ℤ. Equivalently A≅⊕_{b∈B}ℤ. The empty basis gives the trivial abelian group. A torsion-free abelian group need not be free abelian: the additive gro

**Free module:** Let R be an associative unital ring and F a unital left R-module. The module F is free if it has a basis B such that every element of F has a unique finite expression ∑_{b∈B} r_b b with coefficients r_b∈R. Equivalently F≅⊕_{b∈B}R as a left R-module. The empty basis gives the zero module; no finite-rank assump

### 20. Hausdorff second-countable topological space / Second-countable space

**Hausdorff second-countable topological space:** A topological space (X,τ) is Hausdorff and second-countable if (i) for distinct x,y∈X there are disjoint open neighborhoods of x and y, and (ii) τ has a countable basis ℬ, meaning every open set is a union of members of ℬ. These two properties alone do not require X to be locally Euclidean or a manifold. Empt

**Second-countable space:** A topological space $X$ is second-countable if its topology admits a countable basis: there is a countable family $\mathcal B$ of open sets such that every open subset of $X$ is a union of members of $\mathcal B$. Second countability implies first countability and separability, but their converses need not ho

### 21. Boolean isomorphism of measured actions / Spatial isomorphism of measured actions

**Boolean isomorphism of measured actions:** A Boolean isomorphism between two Boolean measure-preserving $G$-actions is a measure-preserving Borel injection $\Phi:X_0\to Y$ from a conull set, with $\Phi(\alpha_gx)=\beta_g\Phi(x)$ on a possibly $g$-dependent conull subset of $X_0$.

**Spatial isomorphism of measured actions:** A spatial isomorphism between measure-preserving $G$-actions is an equivariant measure-preserving Borel injection $\Phi:X_0\to Y$, with $X_0$ a $G$-invariant conull Borel set; equivariance holds for all $g$ and all $x\in X_0$.

### 22. C-constrained map of chromatic metric pairs / Sigma-constrained map of chromatic metric pairs

**C-constrained map of chromatic metric pairs:** Given $\mathcal C\subseteq\mathcal P(\mathbb N)$, a map between chromatic metric pairs is $\mathcal C$-constrained if it is $\sigma$-constrained for every $\sigma\in\mathcal C$.

**Sigma-constrained map of chromatic metric pairs:** A map $f:A_1\to A_2$ between chromatic pairs is $\sigma$-constrained, for $\sigma\subseteq\mathbb N$, when $f(\chi_1^{-1}(\sigma))\subseteq\chi_2^{-1}(\sigma)$.

## Working rules for the next decision pass

1. Clearly identical predicates: one canonical meaning; retain source citations and all historic IDs.
2. Clearly related but meaningfully different contexts/constructions: one searchable heading with separate attached variants, retaining formulation text and source provenance.
3. Ambiguous relation: do not merge; decide manually. Any deep mathematical source investigation requires express prior authorization for the specific question.

**The 44 previously flagged within-heading cases are a separate, unchanged review packet.** No final global relinking or publication has been authorized.
