# Canonical identity review — tranche 4

Source-free review under CHAT_ADJUDICATION_TRANCHE3.md; no graph changes. COMPLETE denotes contextual parent coverage, not identity resolution or external-source certification.

**10 additional COMPLETE; cumulative 98 COMPLETE, 0 PARTIAL, 323 untouched.**

## 89. isomorphism class — `missing.6bb87052ec8a81464ddd`

**retain_distinct_missing**, 2/2 parents. The two parents quotient modules by invertible R-linear maps, then impose different additive relations on the resulting symbols. An object M is not its class [M], nor is [M] an individual isomorphism; different labelled copies represent the same class. Restricting representatives to finite projectives is legitimate within finitely generated modules, but does not identify K_0 with K′_0: the latter uses all finite-module exact sequences, the former direct sums/split sequences. In a fixed universe the collection of all labelled copies may be a proper class. A group presentation must use a set of representatives of isomorphism types, obtainable for finite modules as quotients of finite free objects in the adopted module convention; it must not form the set of every labelled copy.

Remaining: Use a universe/skeleton of isomorphism types, and reconcile ring/module conventions later; the raw class of all copies need not be a set.

## 90. structure sheaf — `missing.6cf140295eca581eb7ae`

**retain_distinct_missing**, 2/2 parents. Both sources require the canonical ring sheaf on Spec(R), with O(D(f))=R_f and localization restriction maps, not just a topology or an arbitrary sheaf. A locally ringed space packages an ambient sheaf but does not construct this particular one. The same one-point topology supports Spec(k) and Spec(k[ε]/(ε²)) with different local section rings, so topology alone does not recover O. Affine charts in a general scheme use this same construction locally without making the whole scheme affine.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 91. minimal prime ideal — `missing.6e8236437269027131a5`

**retain_distinct_missing**, 2/2 parents. Minimality is inclusion-minimality among prime ideals: no strictly smaller prime exists. It differs from maximality, minimal nonzero ideal, and merely being prime. In Z, (0) is minimal prime while (2) is maximal but has (0) below it. Height zero characterizes this prime-minimality under the stored strict-chain convention, but the existing height meaning assigns an ordinal/numerical invariant, not the predicate or the ideal. The geometric parent counts these primes after scalar extension; a unique minimal prime does not imply reducedness or domain: k[ε]/(ε²) has unique prime (ε) and a nonzero nilpotent.

Remaining: Bare-ring/k-algebra unit conventions remain under prior deferrals; no additional unit assumption certified.

## 92. reflexivity x~x — `missing.7176b5fd74d3e3e5dc95`

**retain_distinct_missing**, 2/2 parents. Reflexivity is Δ_S⊆R, equivalently every xRx; it is one axiom, not the entire preorder or equivalence relation. On a nonempty set the empty relation is transitive and symmetric but not reflexive. On {0,1}, the relation Δ∪{(0,1)} is reflexive but not symmetric, so reflexivity does not supply equivalence. The empty set satisfies reflexivity vacuously. Both occurrences use the identical property despite notation ≤ versus ∼.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 93. natural isomorphism F(Y)≅Hom_C(X,Y) — `missing.718fa3e492d42c0ced8e`

**retain_distinct_missing**, 2/2 parents. A natural isomorphism η:F⇒G is a natural family of bijections with inverse natural: from G(u)η_X=η_YF(u), multiply by inverse components to get F(u)η_X^−1=η_Y^−1G(u). Component bijections without this square are insufficient. For a one-object group C_2, the trivial action on a two-element set and the swapping action have underlying sets in bijection but no equivariant bijection, hence no natural isomorphism. Covariant C→Sets and presheaves D^op→Sets both use this construction on their actual domains, with precomposition for Hom(−,X). This does not identify a covariant Hom(X,−) with Hom(−,X), or natural isomorphism with the Yoneda correspondence.

Remaining: Stored scheme sentence calls F:Sch^op→Sets contravariant; its Hom(T,X) context fixes the intended presheaf direction, but literal notation should be reconciled later. Universe/local-smallness remains explicit source scope.

## 94. indexed measurable-event family A_i — `missing.729d8675c7fcafa797ef`

**retain_distinct_missing**, 2/2 parents. Both parents need a map I→Σ with fixed ambient probability space, not an indexed family of random-variable functions Ω→E. Events may repeat and I may be empty or uncountable. Independence adds product equations, not part of the family datum. If the same nontrivial event A occurs at two distinct indices, pairwise independence forces P(A)=P(A)^2, impossible for 0<P(A)<1; the family itself is nevertheless valid. Thus neither measurability nor indexing implies independence. The pairwise distinct-index source issue stays logged, and no common null event for an entire uncountable family is assumed.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 95. direct sum decomposition M=⊕_j M_j — `missing.72b9f9bc4ac0e952e202`

**contextual_ambiguity_or_variant**, 2/2 parents. The common additive construction is an internal direct sum: each element has a unique finitely supported decomposition in the chosen subgroups. It is not an unrestricted product, and the pieces of a graded S-module need not be S-submodules: multiplication can change degree. Existing external direct-sum module candidate includes a common scalar action, while here the construction is additive-group decomposition. Literal scope differs: the canonical context specifies all j∈Z, the ring source only n≥0. Zero-extending a nonnegative grading to negative zero pieces embeds those data into Z-gradings, but a general Z-grading with nonzero negative pieces cannot be recovered as a nonnegative grading. The historical alias shares only the additive finite-support prerequisite, not equality of index conventions or compatibility axioms.

Remaining: Later identify a generic index-set additive decomposition prerequisite or qualify the source-specific index scope; no candidate/alias rewrite applied.

## 96. stalk O_{X,x} — `missing.7413d0506040cdeb60af`

**retain_distinct_missing**, 2/2 parents. A stalk is a germ construction: (U,s) and (V,t) agree iff their restrictions coincide on some neighborhood W⊆U∩V of x. Neighborhoods form a filtered restriction system using intersection. It is not global sections or a categorical fibre. For schemes it gives a local ring, but an arbitrary sheaf of rings need not have local stalks: the constant sheaf Z on a point has stalk Z with multiple maximal ideals. Thus the locally-ringed-space axiom is extra; reducedness of every such local ring is another condition. The set-colimit definition describes underlying germs; ring operations are induced locally, not forgotten.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 97. isomorphism over base category C — `missing.77eacb7314c513d85c72`

**retain_distinct_missing**, 2/2 parents. An isomorphism over C is an invertible functor H commuting strictly with the projections. If H is an isomorphism and p′H=p, its strict inverse K satisfies pK=p′ by composing with K. An equivalence with inverse only up to natural isomorphism is weaker: the two-object category with exactly one arrow between any ordered pair is equivalent to the terminal category but cannot be isomorphic to it. Over a terminal base this already separates the notions. Isomorphisms of fibred categories transport cartesian universal properties; general Cat fibres and groupoid fibres remain separate restrictions. No strictification theorem or source convention is inferred merely from the word split.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 98. multiplication x↦αx — `missing.85c65a55076fda1a7e63`

**retain_distinct_missing**, 2/2 parents. Both parents use exactly m_α:L→L, x↦αx over the fixed subfield K. Commutativity in L gives m_α(cx+dy)=c m_α(x)+d m_α(y), hence K-linearity. This is a selected endomorphism with α as data, not an arbitrary linear endomorphism, nor its scalar norm or trace. The map α↦m_α is injective since m_α(1)=α. For L=K, m_2(x)=2x is linear but is not a unital field endomorphism in characteristic zero. Determinant and trace applied to the same map are different operations; finite dimension belongs to these source parents.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

Next: `missing.8d23b7ba80f9f5e74420`, first parent `form.wave2.analysis.antiderivative-on-interval`. Full source/node hashes, provenance, effective references and occurrence-specific assessments are in the JSONL evidence.
