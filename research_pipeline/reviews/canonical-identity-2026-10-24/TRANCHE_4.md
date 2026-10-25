# Canonical identity review — tranche 4

Source-free review under CHAT_ADJUDICATION_TRANCHE3.md; no graph changes. COMPLETE denotes contextual parent coverage, not identity resolution or external-source certification.

**20 additional COMPLETE; cumulative 108 COMPLETE, 0 PARTIAL, 313 untouched.**

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

## 99. open real interval I — `missing.8d23b7ba80f9f5e74420`

**retain_distinct_missing**, 2/2 parents. Both parents require an open order-convex subset of R, with endpoints possibly infinite, not an arbitrary open subset or an interval with endpoints included. The local δ condition proves openness, while the word interval separately requires all points between any two members. The disconnected set (0,1)∪(2,3) satisfies that local condition but is not an interval. This matters for the antiderivative constant-difference conclusion; derivative zero permits different constants on different components. The weight parent additionally imposes positive finite total mass and all moments, which exclude an empty domain there; the candidate alone must not silently acquire that positivity condition.

Remaining: The displayed local-neighborhood clause is not by itself a definition of interval; retain order convexity explicitly in future source reconciliation and keep empty-domain conventions source-specific.

## 100. field of rational functions in an arbitrary set of indeterminates over k — `missing.92c051047df5e5a34ba3`

**retain_distinct_missing**, 2/2 parents. For a set I, k[X_i:i∈I] consists of finite sums of monomials, each using finitely many indices and finite exponents. It is a domain: any proposed product of two nonzero polynomials lies in one finite-variable polynomial subring, where the product is nonzero. Its fraction field contains quotients p/q using finitely many indeterminates per element, although the field may have infinitely many generators in total. Algebraic independence of B makes evaluation injective and extends to a k-field isomorphism Frac(k[X_b])→k(B); its image is exactly the least subfield containing k and B. This does not require finite transcendence degree, and neither polynomial algebra alone nor the general fraction-field construction is the specifically generated rational-function field. I=∅ gives k.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 101. fibre category E_U of p — `missing.9583e5aa27671c66640e`

**retain_distinct_missing**, 2/2 parents. The strict fibre has objects p(x)=U and only arrows mapped to id_U. It is not generally the full subcategory on those objects: if p is the identity on a nontrivial one-object group category, the full subcategory has all group arrows, but the strict fibre has only the identity. In the groupoid-fibred parents these fibres are groupoids, and discreteness or trivial automorphisms are further restrictions. A setoid can have two distinct isomorphic objects joined uniquely, hence need not be discrete. Fibres at every U being setoids does not imply the whole total category is a setoid; base arrows need not be invertible.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 102. relative diagonal — `missing.96df95f71d6a919f6c57`

**retain_distinct_missing**, 2/2 parents. Δ_{X/S} is the unique scheme arrow induced by the compatible pair (id_X,id_X), since f id_X=f id_X. This distinguishes a particular arrow from the fibre-product object, a set diagonal or a property such as closed immersion. For an affine S-scheme Spec(A), its coordinate description comes from multiplication A⊗_R A→A, so sheaf/ring data matter as well as points. Separatedness and quasi-separatedness apply different predicates to this identical arrow; neither predicate is included in constructing it. No condition that every diagonal be closed is inferred.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 103. two-sided identity e∈M — `missing.9b25d5ea4962f66e4ade`

**retain_distinct_missing**, 2/2 parents. The common prerequisite is an element e with e*x=x=x*e for every x, without separately requiring associativity or inverses. If e and f are two such elements, e=e*f=f, proving uniqueness. A one-sided identity is insufficient: on a set with x*y=y, every element is a left identity but there is no right identity when at least two elements exist. Both group and monoid parents require two-sided identity; a monoid does not require every element invertible. The historical group→monoid seed is a legitimate consequence, not an identity between arbitrary binary operations and monoids.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 104. norm displacement ∥v−a∥ — `missing.9c6846ccbcf16c917251`

**retain_distinct_missing**, 2/2 parents. For a chosen norm and centre a, v↦∥v−a∥ is norm evaluated on an additive difference, not the norm function v↦∥v∥ with centre erased. The triangle inequality implies the induced d(v,a)=∥v−a∥ is a metric; an arbitrary metric need not arise from any vector norm. The two parents evaluate the identical scalar expression then use ≤r versus <r. No completeness, inner product, or equality between closed ball and closure of open ball is required. In the discrete norm |x|=1 for x≠0 on a field with trivial absolute value, the open radius-one ball is {0} and the closed one is the whole nontrivial space; the provenance warning about closure therefore remains relevant in the permitted normed-division-ring scope.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 105. formal derivative f′ — `missing.a42c73c7effdb6ac0764`

**retain_distinct_missing**, 2/2 parents. Formal differentiation is the coefficientwise algebraic map D(Σa_iX^i)=Σ(i a_i)X^(i−1), with integer multiplication interpreted in the coefficient ring. It needs no limits and is not the real analytic derivative meaning. In characteristic p, D(X^p)=0 although X^p is nonconstant; zero derivative does not mean constant there. For standard étale presentations invertibility is required of the IMAGE of f′ in the localized quotient, not of f′ in R[X]. The separability source instead tests coprimality of f and f′ over a field; irreducibility of f does not require irreducibility of f′.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 106. zero object — `missing.a60aa43eed2b99b5d184`

**retain_distinct_missing**, 2/2 parents. A zero object is one object both initial and terminal. Initial ∅ and terminal singleton in Sets show neither condition alone suffices. Factoring X→0→Y yields a distinguished zero arrow; this works in any pointed category, not only a preadditive one. In a preadditive category a terminal object is also initial: its unique endomorphism is zero and identity, so every arrow out is zero by bilinearity, and each Hom group supplies that arrow. Thus the empty product in the additive-category source supplies a zero object. Object 0, zero morphism, zero composite and exactness are distinct data/conditions.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 107. quasi-isomorphic — `missing.a66bc0c6846ac92c6394`

**retain_distinct_missing**, 2/2 parents. A quasi-isomorphism is a chain map inducing homology isomorphisms in every degree; quasi-isomorphic objects can be compared through zigzags. This is weaker than chain isomorphism or chain-homotopy equivalence. The acyclic complex 0→Z --2→ Z →Z/2→0 is quasi-isomorphic to zero, but not contractible: a contracting homotopy would split Z→Z/2, impossible since every group map Z/2→Z is zero. For the stored two-term NL in degrees 1,0, having H_1=0 and H_0=P gives the canonical quotient chain map NL→H_0[0] as a quasi-isomorphism; choosing H_0≅P then supplies the source comparison. Finite projectivity is additional; homology alone does not select a canonical identification with a named P.

Remaining: The statement uses quasi-isomorphic as a comparison relation rather than naming a map; preserve zigzag allowance and degree placement. No derived-category foundational conventions externally verified.

## 108. Grothendieck construction of a category-valued functor — `missing.a6a017ccc98fac71121d`

**retain_distinct_missing**, 2/2 parents. For strict F:C^op→Cat, objects are (U,x); an arrow (V,y)→(U,x) consists of f:V→U and h:y→F(f)x in F(V). If followed backwards by (g:W→V,k:z→F(g)y), composition is (fg,F(g)(h)∘k); strict F(g)F(f)=F(fg) gives associativity and strict identities. Projection sends this arrow to f. Groupoid-valued F is an instance with invertible fibre arrows, but total arrows over noninvertible base arrows need not be invertible. The functor F, its construction ∫F, its fibre category and over-base isomorphism are different data. Weak pseudofunctors require coherence inserted into composition, absent from this stored strict context.

Remaining: Size/universe for Cat and Groupoids stays explicit source scope; no pseudofunctor strictification theorem certified.

Next: `missing.aba129fc5f7d346b2d0f`, first parent `form.de2c8164874ee4a9.cofinal-category-functor`. Full source/node hashes, provenance, effective references and occurrence-specific assessments are in the JSONL evidence.
