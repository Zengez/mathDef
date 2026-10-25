# Canonical identity review — tranche 4

Source-free review under CHAT_ADJUDICATION_TRANCHE3.md; no graph changes. COMPLETE denotes contextual parent coverage, not identity resolution or external-source certification.

**30 additional COMPLETE; cumulative 118 COMPLETE, 0 PARTIAL, 303 untouched.**

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

## 109. comma category (j↓H) — `missing.aba129fc5f7d346b2d0f`

**retain_distinct_missing**, 2/2 parents. For F:A→C,G:B→C the comma objects include an arbitrary arrow u:F(a)→G(b), with morphisms (r:a→a′,s:b→b′) satisfying G(s)u=u′F(r). Iso-comma additionally requires u invertible, excluding e.g. the sole nonidentity arrow 0→1 in the ordered category {0<1}. Fixing an object on the left gives j↓H; fixing it on the right gives H↓j. These need not agree: take H selecting 1 in {0<1} and j=0; j↓H is nonempty, H↓j empty. Shared construction does not identify initiality and cofinality. Nonempty finite-zigzag connectedness is an additional test, not part of the comma definition.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 110. finite absolute moments ∫|x|^k dμ — `missing.ad3eb2f701d26ae8c206`

**retain_distinct_missing**, 2/2 parents. With dμ=w(x)1_(a,b)(x)dx, weighted absolute moments become precisely ∫|x|^k dμ. The interval parent separately assumes finite zeroth mass and all positive moments, hence all nonnegative moments as in the measure parent. These are integrability predicates, not the scalar raw moment ∫x^k dμ; for odd k a principal-value cancellation is not Lebesgue absolute integrability. A finite measure can lack a first absolute moment: density x^−2 on [1,∞) has mass 1 and ∫x·x^−2 dx=∞. Each finite polynomial product is bounded by a finite combination of |x|^k, so all absolute moments justify the orthogonality integrals. No density representation is asserted for every Lebesgue–Stieltjes measure.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 111. slice category C/U — `missing.ad87c8a94e71b0501e7a`

**retain_distinct_missing**, 2/2 parents. C/U has objects a:V→U and arrows h:V→W with b h=a. It is id_C↓U, a particular oriented comma category, with projection to V. The identity U→U is terminal in this slice. It is not the coslice: in {0<1}, C/0 has one object whereas 0/C has two, and not iso-comma, which would exclude noninvertible arrows into U. Over the base C, the fibre of C/U at V is the discrete set Hom_C(V,U); this underlies representable fibred groupoids without identifying C/U with a scheme or a single Hom set.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 112. finite set of k color labels — `missing.afee26ad5b8d0d34952a`

**retain_distinct_missing**, 2/2 parents. The palette is the finite initial segment {1,…,k}, not the coloring function, adjacency relation or chromatic minimum. For k≥1 it has k distinct elements, but no surjectivity is required: an edgeless graph may be colored constantly even with k=5. Renaming labels by a bijection preserves properness without making label set, map and graph identical. The provisional parent explicitly requires k≥1; the older parent does not state it literally, so positive-palette scope needs that source annotation rather than a silent theorem about k=0. The empty palette is a distinct boundary: a map V→∅ exists iff V=∅.

Remaining: Later verify whether the older source permits k=0 for the empty graph; current positive-palette identity does not settle that convention.

## 113. (Sigma,Tau)-measurable mapping — `missing.b458f6a3824dab19725b`

**retain_distinct_missing**, 2/2 parents. A measurable map f:(X,Σ)→(Y,Τ) has f^−1(B)∈Σ for every B∈Τ. It needs neither measure nor probability nor real-valued target; those are additional random-variable/pushforward contexts. A set map may fail: the identity from {0,1} with trivial sigma-algebra to the full power-set sigma-algebra has nonmeasurable singleton preimages. It is not the preimage operation itself, which exists for every map. The measurable condition makes μ∘f^−1 well-defined on Τ, with disjoint countable preimages proving pushforward countable additivity. No inverse function or surjectivity is needed.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 114. weighted discrete orthogonality Σp_n(x)p_m(x)w_x=0 — `missing.b86dc7cff186ed11337b`

**retain_distinct_missing**, 2/2 parents. Both parents impose the discrete weighted bilinear equation Σ_x p_n(x)p_m(x)w_x=0. Finite support is countable support and makes convergence automatic; for the infinite source all absolute moments bound every polynomial product and give absolute convergence, so ordering of summation does not matter. Positivity gives a norm on polynomial restrictions, but on N+1 points every polynomial divisible by ∏_(x∈X)(T−x) has zero seminorm; thus infinitely many independent orthogonal degrees cannot be inferred from a finite system. The continuous/measure integral candidate has wider support/integration data and is not literally this discrete-sum construction, though atomic integration represents it.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 115. m-primary ideal — `missing.b963edbe734f35266d3a`

**potential_existing_meaning_resolution**, 2/2 parents. Within the exact stated Noetherian local scope, the existing ideal-of-definition meaning says sqrt(I)=m, equivalently I is m-primary, matching the candidate predicate on the same ideals. For proof, if ab∈I and a∉I, then b cannot lie outside m: b would be a unit in the local ring and force a∈I. Hence b∈m=sqrt(I), so b^n∈I for some n≥1; I is proper since its radical is the proper maximal ideal. Conversely m-primary includes radical m. A system of parameters additionally selects d generators from m and is not identical to the ideal predicate. This supports a potential existing-meaning resolution to meaning.b9defeff446a0526.ideal-of-definition-local-ring, NOT APPLIED. The target currently has the same missing prerequisite edge; its independent radical formulation grounds the comparison, but any later resolution must handle the resulting self-reference deliberately, not suppress a legitimate dependency automatically.

Remaining: Proposal only: later version-bound resolution and target self-reference/formulation handling need explicit authorization; no gate decision follows.

## 116. nilpotent element r — `missing.bb72b275ee79b161d9b8`

**retain_distinct_missing**, 2/2 parents. The positive-power element predicate x^n=0 for some n≥1 works in every associative ring without an identity; it does not require an exponent-zero convention. In the commutative nil-ideal parent, n may depend on x; a uniform ideal power I^n=0 is stronger. In k[x_1,x_2,…]/(x_i²), each element of I=(x_i) involves finitely many generators and is nilpotent, but x_1…x_n≠0 for every n, so I is not nilpotent. The matrix E_12 in M_2(k) is nilpotent although the ring is noncommutative. Reducedness is the exclusion of nonzero instances, not identity with the element predicate or with being a domain.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 117. two-element subset {u,v} — `missing.bffc2ea0e8bb5da1d41b`

**retain_distinct_missing**, 2/2 parents. A doubleton {u,v} has u≠v and forgets order, whereas Kuratowski (u,v) retains order and exists also when u=v. A general subset may have 0,1 or many elements. These two graph parents use identical possible edges; multiplicities distinguish their edge collections, not the individual doubleton. The singleton {u} cannot represent a loop under these conventions. If V has fewer than two elements there are no such edges, but both graph definitions still permit the vertex set; no finite-vertex or nonempty condition is inferred.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 118. associative ring with multiplicative identity 1_R — `missing.ca9ba1e0fc16e5162ef7`

**retain_distinct_missing**, 2/2 parents. An associative unital ring is the ring object with a two-sided multiplicative identity, not a homomorphism preserving identities or a single invertible element. It need not be commutative: M_2(k) separates it from the commutative-unital candidate. The identity-optional ring meaning is broader: 2Z with inherited operations is a ring with no identity. Two-sided identity, if present, is unique, but being a unit of a ring applies to many elements, not just that identity. The Boolean parent adds all-element idempotence; the homomorphism parent needs two such ring objects and the further preservation equation. No rule 1≠0 is invented: the zero-ring convention must remain source-specific.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

Next: `missing.cf55f62008d08ce2df84`, first parent `form.6676171d9e5698af.affine-closed-subscheme`. Full source/node hashes, provenance, effective references and occurrence-specific assessments are in the JSONL evidence.
