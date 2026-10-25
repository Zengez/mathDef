# Canonical identity review — tranche 4

Source-free review under CHAT_ADJUDICATION_TRANCHE3.md; no graph changes. COMPLETE denotes contextual parent coverage, not identity resolution or external-source certification.

**90 additional COMPLETE; cumulative 178 COMPLETE, 0 PARTIAL, 243 untouched.**

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

## 119. isomorphic over Spec(R) — `missing.cf55f62008d08ce2df84`

**retain_distinct_missing**, 2/2 parents. An S-scheme isomorphism h:X→Y is an invertible scheme morphism with s_Y h=s_X; its inverse automatically commutes with the base by composing this equation. Ordinary isomorphism of abstract schemes is weaker. Over S=Spec(k[t]), the two k-valued points t↦0 and t↦1 have isomorphic underlying Spec(k), but no S-isomorphism: the only possible commuting identity would equate the two t-values. Both parents fix their affine base and preserve the scheme sheaves; neither is merely a ring isomorphism without A/R-algebra compatibility or an isomorphism of categories over a base.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 120. every element idempotent x²=x — `missing.cf59d9cb388b3999576d`

**retain_distinct_missing**, 2/2 parents. The canonical context explicitly distinguishes an element satisfying e²=e from the universal condition ∀x x²=x used by Boolean-ring parents. A single idempotent does not make a ring Boolean: 0 and 1 in Z are idempotent but 2 is not. Universal idempotence does not supply identity: finite subsets of an infinite set, with symmetric difference and intersection, form a Boolean ring whose multiplicative identity would have to be the unavailable entire infinite set. The same element predicate is a legitimate component of both parent conditions; no identity of an individual element with the whole Boolean ring or its all-element property is claimed.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 121. topological fibre product with subspace topology — `missing.cf69ce1240520995df04`

**retain_distinct_missing**, 2/2 parents. The subset P={(x,z):f(x)=g(z)} of X×Z, with its product-subspace topology, is a pullback in Top: a compatible pair of continuous maps from T gives the continuous product map T→X×Z with image in P, which factors uniquely and continuously through the subspace. The generic categorical pullback meaning specifies universality but not this concrete topology; the scheme fibre product adds sheaf data and its underlying space need not be the pointwise set pullback. The self-pullback Z=X uses the same topological construction. No Hausdorff assumption is needed for formation; diagonal-image closedness and universal closedness are extra.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 122. usual total order on Q — `missing.d2189c6f07c197ca9bcb`

**retain_distinct_missing**, 2/2 parents. The usual order on Q is a specific compatible total relation, not the rational field object alone, a generic partial order, or the positive subset. Normalize fractions p/q,r/s to q,s>0; then p/q≤r/s iff ps≤rq. Replacing a fraction by an equal one preserves this cross-product comparison, so it is well-defined independently of any real embedding. The comparison supplies the cases in rational absolute value and q>0 in epsilon positivity. Reversing a total order still gives an abstract total order but is not this usual ordered-field structure (1>0 must hold). Strict >0 excludes 0; ≥0 permits it.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 123. cocone morphisms F(i)→Q compatible with the diagram — `missing.ddc9befb080e8d7146db`

**retain_distinct_missing**, 2/2 parents. A cocone is a family λ_i:F(i)→Q satisfying λ_j F(u)=λ_i for u:i→j, equivalently F⇒ΔQ. It is not a cone ΔL⇒F, nor necessarily universal. For a one-object identity diagram at singleton in Sets, its map into a two-element set is a cocone but not a colimit (the colimit is singleton). A filtered domain in the ind-parent specializes the same compatibility equations. Eventual agreement and a selected splitting are extra and are not inferred from the existence of a cocone. Historical category seed on a diagram phrase supplies ambient categories only.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 124. countable union of members A_n — `missing.dfb06f7328573e269bb5`

**retain_distinct_missing**, 2/2 parents. Countable union of A_n consists of elements belonging to at least one n≥1; repeating or empty terms changes no result. It is the countable-index specialization of arbitrary union, not a disjoint tagged coproduct. Pairwise disjointness adds a condition on inputs, not a different operation. In the alternative sigma axioms, finite unions follow from complements and differences; disjointify A_n as B_n=A_n\(A_1∪…∪A_{n−1}), giving pairwise disjoint B_n with the same union. Thus the restricted closure axiom implies general countable-union closure without changing the candidate operation. Arbitrary-union closure is stronger: countable/cocountable sets on an uncountable X form a sigma-algebra but need not contain an arbitrary union of singletons.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 125. equivalence relation generated by x∼F(u)(x) — `missing.eeaf8a205d5ed2ed6eeb`

**retain_distinct_missing**, 2/2 parents. For P⊆S×S, intersect all equivalence relations containing P (a nonempty collection since S×S qualifies), or use finite zigzags in P and P^op with length-zero paths. This is reflexive, symmetric, transitive and least. It is not merely transitive closure: P={(a,b)} lacks (b,a) under transitive closure alone. A generated relation is not the quotient set or its quotient topology. For set-colimits pairs relate tagged (i,x) to (j,F(u)x), so accidental equality of untagged elements cannot identify components prematurely; for topological coequalizers pairs are (f(x),g(x)) in Y. The same abstract construction handles both inputs without identifying their outputs or topologies.

Remaining: The explicit set-colimit construction requires a set-sized disjoint union (small diagram or adequate universe); the unrestricted functor prerequisite alone does not guarantee that size condition.

## 126. convergence domain D⊆R — `missing.eeb1ff5cf448091c3d57`

**retain_distinct_missing**, 2/2 parents. D is a set of inputs for which a specified real power series converges to a finite real value, not the series expression, its sum function or a radius number. Since n starts at zero, 0∈D always. Changing a_n to a_n/n! changes the series: for a_n=n!, the EGF is Σz^n with D=(−1,1), whereas its OGF diverges at every nonzero z since n!|z|^n fails to tend to zero, giving D={0}. Thus both sources use the same construction but not identical resulting domains for the same a_n. A radius alone does not decide boundary endpoints: Σz^n/n² converges at ±1 while Σz^n does not. Formal generating functions do not require D.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 127. strict finite chain of irreducible closed subsets — `missing.ef28497e9dc38c5b82e5`

**retain_distinct_missing**, 2/2 parents. The underlying chain has strict inclusions between irreducible CLOSED subsets, with length n for n+1 terms; n=0 is allowed for a single irreducible closed subset. Catenarity further fixes endpoints and maximality under insertion, not necessarily greatest cardinality among chains. In a poset with two branches a<b<d and a<c<e<d, both saturated endpoint chains are maximal but lengths differ, illustrating the equal-length condition rather than deriving it from maximality. On Spec(R), p⊊q gives V(q)⊊V(p), reversing orientation; prime-ideal chains are related algebraic instances, not identical topological input data. Supremum in dimension need not be attained and the empty-space −∞ convention remains separate.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 128. finite intersections of open subsets — `missing.f112efe448973069bae2`

**retain_distinct_missing**, 2/2 parents. Finite indexed intersection means simultaneous membership in every U_i, with empty-index intersection the ambient X. It is a set operation; openness and subbasis generation are additional topology statements. Binary A∩B is the two-index instance but does not on its own encode the nullary X convention; arbitrary intersections may be infinite and need not be open (∩_n(−1/n,1/n)={0} in R). Both sources agree exactly on empty and nonempty finite families, including X=∅, preserving the repaired NONEMPTY-family convention of the earlier compactness/FIP audit rather than importing it into all intersections.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 129. conjugate subset gNg^{-1} — `missing.fbd11071cfe5ca8ef6e2`

**retain_distinct_missing**, 2/2 parents. Conjugate subset is the IMAGE of N under the automorphism c_g(n)=gng^−1, not one conjugated element or the conjugacy class varying g. For subgroup N it is a subgroup: products and inverses are conjugates of products and inverses in N. In S_3, conjugating N={1,(12)} by (123) gives {1,(23)}, so subgroup status alone does not imply invariance. If gNg^−1⊆N for every g, apply it to g^−1 and conjugate to get N⊆gNg^−1; equality follows. A fixed single g does not supply normality.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 130. integer divisibility of a-b by m — `missing.9f6f3ee9e141231a54d4`

**retain_distinct_missing**, 1/1 parents. Integer divisibility is the existential integer-multiple predicate m|(a−b) iff ∃k∈Z a−b=km; it is not real division, a chosen quotient k, or a least remainder. For m>0 it defines the stored congruence relation, but the candidate allows nonzero m more generally and the existing congruence meaning fixes positive modulus and two-argument relation. Replacing m by −m negates k and preserves divisibility, without identifying signed parameter conventions. Congruence is an equivalence: witnesses 0, −k and k+ℓ prove reflexivity, symmetry and transitivity. The seed and scan occurrences in this same parent use exactly the same predicate, not two separately reviewed source parents.

Remaining: The historical alias reason mentions a nonzero-modulus variant, but the current single parent explicitly requires positive m; do not invent an extra parent or zero-modulus convention.

## 131. Square matrix of finite order over a field — `missing.c84405a9f915b0897178`

**retain_distinct_missing**, 1/1 parents. A square matrix over K is an array/function {1,…,n}²→K for finite n≥1, distinct from its diagonal, trace, associated linear endomorphism or characteristic polynomial. A linear map acquires a matrix only after bases are chosen. General commutative-ring matrices include coefficients such as Z/4 and therefore have broader coefficient scope; adjacency matrices impose 0/1 values and graph constraints, so they are narrower in a different direction. Matrix [[0,1],[0,0]] and the zero matrix both have trace zero but differ, proving the trace cannot recover the matrix. Both seed and scan identify the same square-array prerequisite of the one source.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 132. polynomial relations f_j — `missing.00f05f23cf310f438561`

**retain_distinct_missing**, 1/1 parents. The f_j are a finite chosen family of polynomial elements mapped to zero by a presentation, not the generated ideal as a set, the equality predicate alone, or the entire presented algebra. (T)=(T,T²) in R[T] supplies two different relation lists yielding the same ideal/quotient; generators need not be independent, minimal, nonzero, or a regular sequence. The finite-presentation property asserts existence of some such finite family and a finite generator list, not a canonical choice. Empty relation family gives the polynomial algebra itself. The polynomial-ring and quotient prerequisites in the compound presentation remain additional; no relation-list/ideal/presentation alias is inferred.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 133. commutative unital ring and common identity — `missing.0113342523b02aece2fb`

**source_convention_deferral**, 1/1 parents. The candidate specifies a commutative unital inclusion with COMMON identity, strictly more than two individually unital rings related by a multiplicative additive inclusion. For example R=k×{0}⊂S=k×k has identities (1,0) and (1,1); both rings are commutative unital but the inclusion is not unital. The source says inclusion of commutative rings with identity without spelling 1_R=1_S; the historical ring-map-unital seed supports an intended convention but is not independent proof of it. Thus retain a source-scope deferral for common identity rather than weakening the candidate or certifying the seed. Strong transcendence and the prior formal-polynomial/evaluated-value granularity caution remain separate; one cannot infer an inclusion convention from the displayed annihilator implication alone.

Remaining: Later verify whether this exact source uses common-identity subrings; no external lookup, source edit or seed override authorized. This is separate from the nine already adopted convention deferrals.

## 134. zero element 0_B — `missing.01941cf7d698abe9cfcc`

**retain_distinct_missing**, 1/1 parents. 0_B is the additive identity of the specified abelian group B. Its uniqueness follows from 0+0′=0′ and 0+0′=0. It is an element, not the zero object B=0, a zero morphism, or the entire kernel subset. Every additive group homomorphism preserves it: f(0)=f(0)+f(0), then cancel. The generic two-sided identity candidate abstracts the same law for arbitrary operations, while this typed additive abelian-group context and specified codomain identify which element the kernel equation uses; do not equate identity of an arbitrary multiplication with additive zero. For a nonzero ring, 0 and 1 separate those operations.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 135. factorial n! of nonnegative integer — `missing.03b976f9393f9c4191f4`

**retain_distinct_missing**, 1/1 parents. Factorial is the integer-valued finite product of all positive integers up to n, with 0!=1. It differs from falling factorial x-underlined-n as a function of two parameters: only specialization x=n gives n!, whereas e.g. 5-underlined-2=20 and 2!=2. In characteristic zero n! embeds as a nonzero real, so a_n/n! in this real EGF is defined for all n≥0. The same division in characteristic p need not exist once n≥p, a scope not allowed to leak into this real construction. Factorial does not encode the infinite-series convergence condition.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 136. disjoint union of sets X_i — `missing.03f1f6a4d6b405f4f3e3`

**retain_distinct_missing**, 1/1 parents. The tagged disjoint union is {(i,x):i∈I,x∈X_i}; component injections have disjoint images even when the original X_i overlap. If X_1=X_2={a}, ordinary union has one element but tagged union has two. It is the coproduct in Sets with its canonical injections, but the generic coproduct meaning ranges over categories and does not define this set construction. The topological parent adds U open iff every injection preimage is open; U∩X_i is shorthand after identifying each component with its tagged image. Empty index gives ∅. A set-sized I and set components are needed to form a set; no proper-class coproduct is asserted.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 137. singleton {x} — `missing.0423a519b1e84ca6d41c`

**retain_distinct_missing**, 1/1 parents. A singleton {x} has exactly one element and exists for each specified x, whereas its member x need not itself be a one-element set. The compound Kuratowski-constructor candidate includes a singleton AND an unordered pair, so the singleton component does not identify that whole construction. Components are maximal connected subsets, not automatically open sets. The rationals with their usual topology have singleton connected components (an irrational between two rational points separates any purported two-point connected subset) but are not discrete, since every neighborhood contains other rationals. Empty space has no components and satisfies the displayed condition vacuously; no phantom singleton is created.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 138. eventual uniform lower bound a_n>=delta — `missing.06d3b29d2fa8ad998a3d`

**retain_distinct_missing**, 1/1 parents. The predicate is ∃δ∈Q_{>0}∃N∀n≥N a_n≥δ, a UNIFORM positive margin in the tail, not ∃N∀n≥N a_n>0. Sequence a_n=1/(n+1) is positive termwise but tends to zero and has no such margin. If b∼a and a_n≥δ eventually, choose the difference threshold δ/2; eventually b_n>a_n−δ/2≥δ/2. Hence the predicate is representative-invariant on rational Cauchy classes. It requires no previously constructed real limit, and it is not merely a lower bound (negative/zero bound would not characterize positive classes) or a property of δ alone.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 139. chosen ordering V={v_1,…,v_n} — `missing.07e25eec2547df68421c`

**retain_distinct_missing**, 1/1 parents. Choosing an enumeration is choosing a bijection {1,…,n}→V, more than finiteness or a surjective list allowing repeats. It is not adjacency, an intrinsic order on an abstract graph, or the matrix itself. A new enumeration permutes rows and columns simultaneously: if v′_i=v_{π(i)}, then A′_ij=A_{π(i),π(j)}. The same graph can therefore have different displayed arrays, e.g. moving the centre of a three-vertex path from index 2 to index 1 changes its entries. No infinite enumeration is supplied by this finite source.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 140. morphisms A to P and C to P agreeing on B — `missing.087c8c78478b26335f01`

**retain_distinct_missing**, 1/1 parents. For a span B→A,B→C, a compatible pair i:A→P,j:C→P satisfies i f=j g. This is the span-shaped cocone, whose B-component is forced by that equality. It is an instance of a generic cocone but retains a specific input diagram and pair of arrows, not an arbitrary diagram shape, and is not automatically a pushout. In Sets with B=∅ and A=C={*}, two maps to a singleton form such a pair while the pushout is a two-element set; universality fails for that chosen vertex. Do not reverse it into a cone over a cospan or infer that the structure arrows are injective in every category.

Remaining: Generic cocone is a reusable construction covering this span instance; any future identity compression must explicitly retain the diagram-shape data rather than claim arbitrary cocones are just pairs. No alias proposed.

## 141. zero R-module — `missing.08ca647ed43622178944`

**retain_distinct_missing**, 1/1 parents. The zero R-module is the singleton additive group with its forced zero action. There is exactly one R-linear map to and from it in either general or unital module conventions, making it a zero object of the corresponding module category. This does not identify it with a chosen zero submodule inside M or with the zero element of an arbitrary M. The final quotient in a regular sequence must not be this object; otherwise injectivity on zero successive terms would make trivial sequences misleading. Rank-9 source convention deferrals remain: an empty sequence need not force 1m=m, and no unital R is inferred from this zero object.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 142. field automorphism σ:E→E — `missing.08fcaa9f26323a9c3d56`

**retain_distinct_missing**, 1/1 parents. A field automorphism is a bijective unital ring map E→E; its inverse preserves operations by applying the forward bijection to sums/products. An injective endomorphism is not enough: k(t)→k(t), t↦t², is injective but not onto. Fixing F pointwise is an additional condition defining the subgroup Aut(E/F); a general E-automorphism need not fix a chosen subfield pointwise. On Q(t), t↦−t does not fix Q(t) pointwise if that whole field is chosen as F. An automorphism group is a set/group of such arrows, not one automorphism. No finite or Galois hypothesis is required for Aut(E/F).

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 143. circuit as nontrivial closed edge-trail — `missing.0b7317d52bc5113b3520`

**retain_distinct_missing**, 1/1 parents. A circuit here is a positive-length finite closed TRAIL, no undirected edge repeated, whereas a simple cycle forbids repeated vertices except its closing one. Traversing two triangles sharing one vertex in succession is a circuit with that shared vertex repeated, not a simple cycle. Every finite closed trail contains a simple cycle: take a shortest closed subwalk between repeated vertices, whose interior vertices cannot repeat. Thus absence of circuits and cycles agrees in simple undirected graphs even when the ambient vertex set is infinite. This is equality of existence/absence predicates, not identity of the individual circuit and cycle objects, nor a rooted-tree or directed/matroid convention.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 144. two-term complex I/I²→Ω_{P/R}⊗_P S — `missing.0cef0a8e358745284bfe`

**retain_distinct_missing**, 1/1 parents. A two-term homological complex C_1→C_0 has zeros elsewhere, so consecutive differentials compose to zero automatically. The specified arrow is data; its kernel and cokernel are H_1 and H_0 and need not vanish. It is not an exact sequence, a cochain complex in degrees 0,1 with the same numeric degree placement, or the full cotangent object with chosen polynomial presentation. Here d(i mod I²)=di⊗1 is well-defined: d(ab)=a db+b da maps to zero after tensoring with S for a,b∈I, so I² is killed. The general two-term prerequisite and its source-specific I/I², differential-module and scalar-extension terms stay separate.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 145. set of all rational lower cuts R_D — `missing.0f9ce4837c92ff02c397`

**retain_distinct_missing**, 1/1 parents. The carrier R_D is a subset of P(Q), consisting of all NONEMPTY PROPER downward closed subsets without greatest rational. It is not a single cut, a pair (cut,complement), Q itself, or already a field with operations. Separation from P(Q) is strict: ∅ and Q are subsets but not cuts. The rational example A_q={r:r<q} is nonempty/proper and has no greatest member by rational density. Abstract complete ordered fields are isomorphic to an eventual cut field but not literally the same sets. The source explicitly treats arithmetic and completeness as proof obligations; merely collecting cuts supplies none of them.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 146. cyclic group of order p — `missing.11eb8dbe559b544a000a`

**retain_distinct_missing**, 1/1 parents. Cyclic order p means a generator g with exact least positive period p; g^p=e alone is insufficient since the identity also satisfies it. Its elements are e,g,…,g^(p−1), distinct by minimality. The source p is prime characteristic, and a nontrivial Artin–Schreier extension has the additional Galois interpretation: roots differ by c∈F_p and translations compose by addition; a nontrivial subgroup of the order-p translation group is the whole group. This does not turn field characteristic into a group-order definition. The Kummer candidate allows degree merely dividing n, hence may have order 1 or a proper divisor; not an exact-order-p identity.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 147. zero composite of consecutive maps — `missing.12cbff3823a07d544a1e`

**retain_distinct_missing**, 1/1 parents. A chain complex requires d_n d_(n+1)=0 for all adjacent maps, not just a sequence of composable arrows and not exactness. The complex 0→Z --0→ Z→0 has zero composites but nonzero homology at both Z terms. Thus existing exact-sequence meaning, although its opening sentence describes complexes, cannot replace the whole generic complex prerequisite without imposing extra image=kernel conditions. In an additive category zero arrows exist independently of a zero OBJECT choice. Two-term complexes automatically meet this condition because the neighboring terms are zero, whereas a three-term arbitrary sequence need not.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 148. structure morphism X→Spec(Z) — `missing.131212604e1e2155bd93`

**retain_distinct_missing**, 1/1 parents. Every scheme has a canonical morphism to Spec(Z), unlike an arbitrary chosen base map X→S. On an affine Spec(A), the unique unital ring map Z→A sends n↦n1_A; these maps agree under restrictions and glue. Uniqueness on affine charts proves Spec(Z) is terminal in schemes, dual to Z being initial in unital commutative rings. Merely having the prime-spectrum space Spec(Z) does not specify this arrow. Separatedness and quasi-separatedness of this canonical map are the absolute properties; their distinction remains and no chosen S-structure is substituted.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 149. evaluated polynomial phi(P)(g)=0 — `missing.137cc84619d0fc68bf3b`

**retain_distinct_missing**, 1/1 parents. For φ:R→S define φ_*(Σa_jT^j)=Σφ(a_j)T^j and ev_g(φ_*P)=Σφ(a_j)g^j. The source requires this evaluated ELEMENT to equal zero; neither the formal P, coefficient map, evaluation homomorphism nor zero equation alone is the whole datum. A nonzero polynomial may evaluate to zero (P=T at g=0), and a noninjective coefficient map may already kill nonzero coefficients. The earlier evaluation-map candidate supplies the underlying map construction but does not impose the vanishing condition; the roots-in-a-FIELD candidate is too narrow because S may have zero divisors. Ideal-power coefficient restrictions and monicity belong separately to integrality over I.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 150. finite partial sum s_N — `missing.14fb2e2c8ee691a830d3`

**retain_distinct_missing**, 1/1 parents. s_N is a FINITE sum with N+1 real terms and exists for every real sequence even if no infinite sum exists. Recurrence s_0=a_0 and s_(N+1)=s_N+a_(N+1) fixes the indexing. For a_n=1, s_N=N+1 is defined for all N but has no finite limit; thus the partial-sum operation is not series convergence or its limit. The original sequence and the partial-sum sequence are different (recover a_n by differences, not equality). Order and multiplicity are retained; this is not an unordered sum of the set of distinct coefficient values.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 151. support Z of quotient sheaf O_X/I — `missing.16dd13db42779fad9a84`

**retain_distinct_missing**, 1/1 parents. Support here is {x:(O_X/I)_x≠0}, a subset of the given locally ringed space, not the quotient sheaf or its closed-space structure. For a sheaf ideal in a unital ring sheaf, outside support means I_x=O_x, so germ 1 lies in I_x; it is represented by an ideal section equal to 1 on a smaller neighborhood. The quotient vanishes throughout that neighborhood, proving support is closed. The finite-module support on Spec(R) is a related affine special case, not an arbitrary-sheaf definition. Different quotient rings k[ε]/(ε²) and k on the same point have the same support but different structure sheaves, so support cannot recover the closed subspace datum.

Remaining: The exact locally section-generated hypothesis remains under the rank-86 source-scope question; no finite-generation/coherence assumption inferred.

## 152. left and right cancellation — `missing.16eb7002116042616e29`

**retain_distinct_missing**, 1/1 parents. This is cancellation AFTER an allowed denominator composition, not ordinary monic/epic cancellation. In a two-sided calculus one typical direction says if s f=s g with s∈S then some t∈S on the other side satisfies f t=g t; the dual exchanges sides. It does not demand f=g before such a composition. For a one-object category from a commutative monoid with absorbing zero, S={1,0} illustrates the distinction: 0f=0g always, and choosing t=0 equalizes on the other side without making 0 monic or epic. The full multiplicative system also includes identities, composition and Ore squares, so cannot replace this component axiom. The stored parent abbreviates rather than writes the exact arrow variables/quantifiers.

Remaining: Before future population/source certification, recover the exact two directional cancellation formulas and S-placement from this source; current shorthand identifies the calculus component but is not a full axiom statement.

## 153. local restriction E∩V_i — `missing.16fdb955076446c83a6f`

**retain_distinct_missing**, 1/1 parents. E∩V_i is the binary restriction of a subset to the open subspace V_i; its topology is relative to V_i. It is not a section restriction map, a locally closed set predicate, or the open-cover datum. Underlying membership is the general binary-intersection operation, but the contextual construction additionally records the open ambient subspace in which constructibility is tested. Constructible here means finite unions of U\V with retrocompact opens; a locally constructible cover need not supply a single globally finite presentation. The local finite presentations and their potential global gluing require their own argument; no counterexample to global constructibility is asserted by this prerequisite review.

Remaining: Generic binary intersection covers the underlying set component; any future identity compression must retain the specified relative-topology/constructibility context.

## 154. edge multiplicity — `missing.17fcbd3c3e67f2b21f6b`

**source_convention_deferral**, 1/1 parents. An edge multiplicity counts copies of a fixed unordered doubleton; it is not the doubleton, the whole edge multiset, or vertex degree (which sums incident multiplicities). Two vertices joined by three copies have pair multiplicity 3, whereas simple-graph existence only records present/absent. The candidate explicitly makes multiplicity a NONNEGATIVE INTEGER; the source merely calls E a multiset without specifying whether each pair has finitely many copies. Infinitely many vertices do not by themselves force infinite pair multiplicity, but neither do they settle the multiset convention. Retain a bounded source-convention deferral rather than silently equating cardinal-valued infinite multiplicity with N-valued multiplicity.

Remaining: Later verify whether this exact multiset source restricts multiplicity per pair to finite integers; preserve its loopless and parallel-edge conventions.

## 155. two-sided inverse element b for each a — `missing.18f9db0195dad8f9cb4e`

**retain_distinct_missing**, 1/1 parents. For an associative operation with identity e, b is a two-sided inverse of a when ab=e=ba. If b and c are both inverses, b=b(ac)=(ba)c=c. A one-sided inverse need not be two-sided: on N, shift s(n)=n+1 and p(0)=0,p(n+1)=n satisfy p∘s=id but s∘p≠id. The group parent requires such inverse for EVERY a, stronger than a monoid having one invertible element. An inverse element is not an inverse function of a set map; a ring unit is the analogous multiplication predicate in a richer ambient ring and does not force all ring elements invertible.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 156. canonical summand inclusions ι_i:M_i→⊕_i M_i — `missing.1a60248259f8ac73fd6f`

**retain_distinct_missing**, 1/1 parents. ι_i sends m to the finitely supported family with its i-coordinate m and all others zero, hence is R-linear and injective since projection π_iι_i=id. It is not a generic module injection, an inclusion into the colimit, or the direct-sum object. After quotienting by transition relations its composite need NOT be injective: the directed diagram M_0=Z→M_1=0 has zero colimit and kills M_0, although its direct-sum injection was injective. Thus the displayed relations use the genuine summand maps before quotienting; neither transition injectivity nor colimit injectivity follows.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 157. ith cohomology of a cochain complex — `missing.1bd554e6f230b14c5f9b`

**retain_distinct_missing**, 1/1 parents. For cochains d^i:C^i→C^(i+1), H^i=ker d^i/im d^(i−1) is defined because d^i d^(i−1)=0. A Hom applied to a homological resolution reverses arrows: δ^i(f)=f∘d_(i+1); δ^(i+1)δ^i=0. For the unaugmented F_•, H^0 Hom(F_•,N) identifies Hom(M,N) via augmentation, rather than including Hom(M,N) as a preceding term that would change the computation. Chain homology has opposite degree direction and is not literally cohomology with indices erased. There is an additional existing-edge scope question: the stored internal-Hom MODULE target requires commutative R, while this parent says only R-modules. Over arbitrary associative R, Hom_R is naturally an abelian group; output scalar multiplication need not preserve R-linearity (for M=N=R and noncentral r, r·id fails). This does not invalidate the generic cohomology prerequisite.

Remaining: Later exact source reconciliation should state commutative R if internal Hom is an R-module, or use abelian-group Hom for general R. Existing edge occ.321952d7b781466d1856 remains untouched; prior unit-action deferrals remain distinct.

## 158. finite direct sums or biproducts — `missing.1bf45a51e32fe839d4c5`

**retain_distinct_missing**, 1/1 parents. In a preadditive category a finite biproduct has p_iι_j=δ_ij and Σι_i p_i=id, simultaneously realizing product and coproduct. From a finite product, define ι_j by projection components δ_ij; the sum equation follows by testing every projection, and for arrows f_i:X_i→Y the universal coproduct map is Σ f_i p_i. This proof uses bilinear composition, not a general identity of products and coproducts in arbitrary categories (Sets has |A×B|=1 and |A⊔B|=2 for two singletons). Nullary biproduct is a zero object. Arbitrary module direct sums use finite SUPPORT of elements, but need not be products for infinite families.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 159. graded quotients m^nM/m^{n+1}M — `missing.1c3a3131528cfb0d72af`

**potential_candidate_alias**, 1/1 parents. This degree-n object is exactly the module quotient N/L with N=m^nM and L=m^(n+1)M. Its induced residue-field action is determined by the R-action since mN⊆L, hence it adds no independently chosen scalar datum or multiplication. The previously fully reviewed generic quotient-module candidate explicitly includes successive filtration factors and the same induced-scalar-action construction (review canonical-review.2026-10-24.011). This supports a POTENTIAL candidate alias for the quotient prerequisite only, with m,n,M and associated-graded role retained in the source; it is not an alias of a whole graded module. In R=k[t]_(t), M=R, each m^n/m^(n+1) has length 1 while R/m^(n+1) has length n+1, so graded-piece and cumulative Hilbert–Samuel functions remain distinct. No alias is applied.

Remaining: Proposal only, anchored to prior complete generic quotient review and unchanged source snapshots. Later authorization must preserve the exact associated-graded source role, residue action and n=0 unitality convention.

## 160. map X→M_i splitting M_i→X — `missing.1c6af723b751472f1aba`

**retain_distinct_missing**, 1/1 parents. A splitting here has r:M_i→X and s:X→M_i with r s=id_X. It makes X a retract, r a split epimorphism and s a split monomorphism, but does not require s r=id_(M_i). The projection X⊕Y→X with the standard inclusion splits and is not an isomorphism for nonzero Y. It differs from the dual pro-object orientation, and having this one splitting does not by itself establish all eventual-agreement conditions of essential constancy. Generic injectivity/surjectivity are set notions and cannot substitute for these universal arrow equations in an arbitrary category.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 161. Minkowski set sum tC+(1−t)C — `missing.1d1e6d6708183b231518`

**retain_distinct_missing**, 1/1 parents. tC+(1−t)C is a SET of all tx+(1−t)y with independent x,y∈C. It is not one pointwise convex combination or merely scalar multiplication of C. For C={0,2}⊆R and t=1/2, this set is {0,1,2}, larger than C; allowing only x=y would falsely yield C for every subset. At t=0 or 1 it equals C for nonempty C, and for C=∅ it is ∅ because there are no input pairs (the image 0∅ is also ∅, not {0}). Inclusion for every t∈[0,1] exactly matches the two-point convexity predicate, with no norm, dimension, closedness or arbitrary-real-scalar stability.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 162. prime ideals minimal over its annihilator Ann_R(m) — `missing.1d331e8d364b026c50d5`

**retain_distinct_missing**, 1/1 parents. Minimal over I means minimal in the poset of primes CONTAINING I, not among all primes of R. With R=Z and I=(6), primes (2) and (3) are minimal over I but neither is a minimal prime of Z, whose (0) does not contain (6). Weak association existentially chooses m and a minimal-over-Ann(m) prime, whereas association requires equality p=Ann(m); the predicates must not be merged by replacing minimality with equality. It corresponds to minimal primes of R/I via inverse image, but the quotient-ring/base-change data are necessary for that translation. Unit/module source conventions remain independently deferred.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 163. Cat as category of small categories — `missing.1e57f82e00af556806fa`

**retain_distinct_missing**, 1/1 parents. For a fixed universe U, Cat_U has U-small categories as objects and functors as arrows; functor composition/identities define the ordinary category. It is generally larger than a U-small category itself. A presheaf F:C^op→Cat_U need not have U-small DOMAIN C merely because each value is small. A category object, the category OF such objects and a Cat-valued functor are different types. Groupoids_U is the subcategory with all value-category arrows invertible, not all of Cat_U. The source strictness is equality of pullback functors, not extra 2-cells of a pseudofunctor; the ordinary Cat role suffices here.

Remaining: The stored source does not spell out its universe for Cat. Keep this a later size-convention obligation, without shrinking the already reviewed unrestricted-domain category candidate.

## 164. kernel of automorphism mapping F on an object — `missing.1f1fd9a269f9c46bb515`

**retain_distinct_missing**, 1/1 parents. F induces a group homomorphism Aut_S(x)→Aut_(S′)(Fx): it preserves composition, identity and inverses. Its kernel consists exactly of α with Fα=id. If F is strictly over C, verticality is AUTOMATIC for kernel elements: pα=p′Fα=p′id=id_(p x). Thus no extra verticality gap remains under the recorded over-base hypothesis. In contrast, merely preserving automorphisms does not put them in the kernel; for F=id the kernel is trivial, while for the map of a group category to terminal every automorphism is killed. The kernel group at x is not the entire relative-inertia category of pairs and intertwining arrows.

Remaining: If a later variant uses commuting projections only up to isomorphism, transport data must be specified separately; current strict over-base reading supplies the proof.

## 165. restriction of functions to U_x — `missing.1faaa3731208d18704c8`

**retain_distinct_missing**, 1/1 parents. Restricting f:X→M to U⊆X keeps each value f(u) and changes its domain to U; it is f composed with inclusion U→X. It is neither inverse image of a subset, a sheaf-restriction map as extra sheaf data, nor a new choice of values. Restrictions to the same U preserve pairwise metric errors; uniform convergence there means one N for every y∈U, possibly depending on ε and the chosen neighborhood, not on y. For f_n(x)=x/n on R, every bounded neighborhood has uniform convergence to zero but the whole line does not. The restriction construction itself requires no continuity or neighborhood hypothesis; those belong to the parent.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 166. Lebesgue–Stieltjes measure from nondecreasing function — `missing.2216f1dfe187a7af152c`

**source_convention_deferral**, 1/1 parents. A Lebesgue–Stieltjes measure is not just an arbitrary nonnegative measure or a weight-density measure: bounded monotone functions may have jumps giving atoms, whereas w(x)dx assigns every singleton zero. For the common right-continuous convention μ((a,b])=α(b)−α(a), one-sided continuity matters. The monotone α(t)=0 for t≤0, 1 for t>0 would give μ((0,1/n])=1 although those intervals decrease to ∅, contradicting finite-measure continuity from above. Thus the word admissible must include a normalization/one-sided convention or a construction using one-sided limits. The stored source does not specify which. Preserve a source-convention deferral, not an invented right-continuity hypothesis or an alias to density integration.

Remaining: Later verify the source meaning of admissible, endpoint atom assignment, one-sided normalization and integration interval; no formula or source correction applied.

## 167. automorphism α of x over identity of p(x) — `missing.229af74a7a716a68dd9e`

**retain_distinct_missing**, 1/1 parents. A vertical automorphism is an invertible x→x with pα=id_(p x), not merely an arbitrary endomorphism or an automorphism over a nonidentity base loop. For p=id on a nontrivial one-object group category, every group element is an automorphism, but only identity is vertical; this separates the predicates. A fibration does not force verticality of all total automorphisms. The inertia object additionally pairs x with α, and an arrow β between two pairs must satisfy βα=α′β; that whole category is not one automorphism or its group. Relative-inertia kernel elements are vertical for the separate reason F is over C.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 168. μ-integrability of power function — `missing.22e38bfed03405a51af2`

**retain_distinct_missing**, 1/1 parents. For nonnegative integer n, conventional μ-integrability of x^n means measurability and finite ∫|x|^n dμ. The moment value is then a finite scalar; the source sentence finite only when integral finite is redundant under this assumption, not a second extended-integrability convention. At n=0 the condition is finite mass using the constant polynomial 1, including at x=0. For odd n, a symmetric principal-value cancellation does not supply absolute integrability. This single-power predicate is an instance of the all-absolute-moments prerequisite, but does not assert all orders at once, nor probability normalization or stochastic-time quantifiers. On density x^−2 over [1,∞), n=0 is integrable and n=1 is not.

Remaining: Conventional finite-L1 reading is explicit in the candidate; later verify any source alternative using extended moments rather than silently broadening it.

## 169. metric-induced topology tau_d — `missing.23c297a4a1c27fe4ec73`

**retain_distinct_missing**, 1/1 parents. τ_d consists of unions of positive-radius d-balls, not just the ball collection. If z belongs to B(x,r)∩B(y,s), a radius smaller than both r−d(x,z) and s−d(y,z) gives a ball about z contained in the intersection, proving the basis property. The topology is uniquely determined by d, but not conversely: d and 2d on a nontrivial metric space give the same opens and different distances. The parent retains the specified metric in its compatible triple and excludes empty X under its source convention. The candidate-resolved ball edge legitimately creates a structural effective cycle through this alternative metric formulation; no mathematical link is removed to break it.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 170. boundedness of real-valued f — `missing.23f5062d098be96c786a`

**retain_distinct_missing**, 1/1 parents. Boundedness is one M≥0 working for every x in the fixed interval. Pointwise finite values or compactness of the domain alone do not imply it: define f(a)=0 and f(x)=1/(x−a) for x>a. Conversely the Dirichlet indicator of rational inputs is bounded by 1 but not Riemann integrable on a nondegenerate interval: arbitrary tags allow all-rational and all-irrational sums of b−a and 0. Thus boundedness is not integrability, continuity, or bounded-linearity of an operator. A bounded-above range alone is weaker than a two-sided absolute bound; f(x)=−1/(x−a) with f(a)=0 is bounded above but not bounded.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 171. Hermitian sesquilinear form V×V→C — `missing.23ff9207e591fcd879d9`

**retain_distinct_missing**, 1/1 parents. Hermitian first-linear means h(αv+βw,z)=αh(v,z)+βh(w,z), h(v,αw)=conjugate(α)h(v,w), and h(v,w)=conjugate(h(w,v)). Consequently h(v,v) is real, but need not be positive: h(z,w)=z_1 conjugate(w_1)−z_2 conjugate(w_2) is Hermitian indefinite. A zero form is degenerate. Positive definiteness is the extra inner-product axiom, not part of the general Hermitian-form identity. A real symmetric bilinear form has another scalar field and no nontrivial conjugation. Switching which slot is linear is a labelled convention related by conjugation/transposition, not equality of the same function under unchanged arguments.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 172. degree-zero subring — `missing.244d6cfceb0dd22abbca`

**contextual_ambiguity_or_variant**, 1/1 parents. The zero-degree part consists of homogeneous fractions with degree(a)−n degree(f)=0; addition is closed by taking common denominator and multiplication adds zero degrees. For S=k[x], deg x=1,f=x, the whole S_f=k[x,x^−1] has many degrees while its degree-zero subring is k. Thus it is not full localization or a homogeneous component chosen as a scalar element. A granularity overlap remains: the existing parent meaning degree-zero homogeneous localization DEFINES S_(f) as this exact subring for positive-degree f. The candidate wording can also describe the degree-zero component for degree-zero denominators or more general localized gradings, whereas that existing meaning explicitly fixes positive degree. Do not assert an unrestricted existing-target resolution or silently keep a redundant self-definition as an independently justified prerequisite.

Remaining: Later adjudicate component-operation versus full existing S_(f) construction, positive-degree scope and zero homogeneous elements; no resolution/removal or source edit applied.

## 173. naturally identified representing module — `missing.24b750917f64c00ee6ee`

**potential_candidate_alias**, 1/1 parents. The canonical candidate explicitly denotes a natural isomorphism of COVARIANT set-valued functors in N, not the module P itself. This is the generic natural-isomorphism prerequisite missing.718fa3e492d42c0ced8e (complete review rank 93), instantiated at Hom_S(P,−) and Diff^k(M,−). For an S-linear h:N→N′, Hom sends u to h u and Diff sends D to hD. The latter preserves order by induction because [hD,s]=h[D,s]. Naturality requires η_(N′)(h u)=hη_N(u) for every h, stronger than unrelated bijections for each N. A chosen P and representing correspondence remain additional whole data; no alias of a module with a transformation is proposed. Unit/commutative coefficient source conventions remain under existing deferrals.

Remaining: Proposal only for the natural-isomorphism prerequisite, not a representing-module identity or certified principal-parts existence theorem. Preserve prior source module-convention cautions.

## 174. radical ideal I — `missing.2592ffd1f6be0b4d46bf`

**retain_distinct_missing**, 1/1 parents. A radical ideal satisfies x^n∈I⇒x∈I for every positive n, equivalently sqrt(I)=I. The radical OPERATION takes any ideal to a new ideal, whereas this is a property of an ideal already given. For example (4) in Z is not radical since 2²∈(4) but 2∉(4), and sqrt((4))=(2). The Jacobson radical is the intersection of maximal ideals of a ring; a Jacobson R requires a relation between all radical ideals and containing maximal ideals, not equality of the predicate radical with that distinguished ideal. In k[t]_(t), (0) is radical and Jac(R)=(t), separating them. I=R is allowed as a radical ideal unless properness is separately imposed; empty intersection then gives R.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 175. induced exterior-power map ∧^rφ — `missing.25dac0c185025e52a26a`

**source_convention_deferral**, 1/1 parents. For commutative unital R, apply φ to each wedge factor: v_1∧…∧v_r↦φv_1∧…∧φv_r. The multilinear map is alternating, hence descends through the exterior-power quotient and is R-linear. Exterior MODULE and induced MAP are different; r=0 gives id_R, r=1 gives φ. Nonzero wedge is not invertible wedge or constant fibre rank: over Z/4, φ=multiplication by 2 has nonzero ∧¹φ but becomes zero over the residue field Z/2. The parent merely says finite free modules over R, while this ordinary exterior-power construction needs the commutative coefficient convention (or additional bimodule machinery in other contexts). No such generalization is invented. Keep a precise source-convention deferral instead of certifying coefficient commutativity from the unital-module scan target.

Remaining: Later verify commutative/unital coefficient convention and exterior indexing (especially r=0 and zero ring) in this exact source; no rank-theorem or ring-scope correction applied.

## 176. finite moments Σ|x|^k w_x — `missing.265e6df46207937dc94a`

**retain_distinct_missing**, 1/1 parents. The discrete all-moment condition is Σ_(x∈X)|x|^k w_x<∞ for every k≥0, so k=0 includes total weight finiteness. With atomic measure μ=Σ w_xδ_x it equals all absolute μ-moments, but the stored discrete prerequisite retains support and weights whereas general Stieltjes measures need not be atomic. Positive summability alone does not imply higher moments: X={1,2,…},w_n=1/n² has finite total mass and infinite first moment. Conversely n^k2^−n sums finitely for each fixed k, showing a valid infinite-support example. Different k may have different finite bounds; no single bound uniformly over all k is required.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

## 177. pro-object — `missing.278d73133c80cdd539f3`

**retain_distinct_missing**, 1/1 parents. A pro-object is a formal cofiltered inverse diagram, with its formal morphism structure, not an actual limit object in C or a single inverse-sequence arrow. Actual limits need not exist in C: finite sets Z/2^n with reduction maps give a pro-finite-set object, but their inverse limit has arbitrarily many distinct compatible residues and is not finite. Ind-objects reverse the formal direction; saying Pro(C) is related to Ind(C^op)^op does not identify objects of the two completions of C without opposites. Essential constancy adds a condition making the formal object isomorphic to a constant one; a cone alone does not establish it.

Remaining: Formal completion morphism sets require small-index/universe conventions not specified in this abbreviated source; no unrestricted proper-class limit formed.

## 178. restriction of ambient group operation — `missing.293cecfee8aa9184332d`

**retain_distinct_missing**, 1/1 parents. Restricting ⋆:G×G→G to H×H first gives values in G; closure is needed to corestrict the codomain to H. Thus an arbitrary subset does not carry an INTERNAL operation by mere restriction. For H={1}⊂(Z,+), 1+1=2∉H. Even a closed nonempty subset such as nonnegative integers under addition need not be a subgroup because inverses can fail. The subgroup definition requires the inherited law to form a group, not an unrelated chosen group law on H. Generic function restriction keeps the codomain G, whereas this construction includes closure and codomain corestriction; do not erase that distinction.

Remaining: No external citation verification or whole-parent theorem certification; no semantic correction applied.

Next: `missing.2b4bf1ddae7c8d62e393`, first parent `form.wave2.cross110.finite-image-rank`. Full source/node hashes, provenance, effective references and occurrence-specific assessments are in the JSONL evidence.
