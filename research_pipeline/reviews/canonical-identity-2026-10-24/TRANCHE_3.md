# Canonical identity review — tranche 3

Source-free review under CHAT_ADJUDICATION_TRANCHE2.md; no graph changes. COMPLETE denotes contextual parent coverage, not identity resolution or external-source certification.

**20 additional COMPLETE; cumulative 58 COMPLETE, 0 PARTIAL, 363 untouched.**

## 39. closed subset of a topological space — `missing.c4ed408b10943e9c0f8e`

**retain_distinct_missing**, 4/4 parents. All four parents use F⊆X with X\F open in the specified topology, including the product topology in the diagonal test. Closedness is relative: {0} is closed in itself but need not be closed in a larger indiscrete space. It is a property of a subset, not the closure operator, a closed-map property or a scheme with a sheaf. Spec(Z/2) and Spec(Z/4) have the same underlying closed support in Spec(Z) but different quotient rings, separating closed subsets from closed subschemes. The current FIP parent explicitly says NONEMPTY family; that approved repair remains intact, including X=∅. Historical topology seeds supply legitimate ambient structure but not a standalone closed-subset definition.

Remaining: No external citation or complete host-theorem certification; no semantic change proposed.

## 40. roots of a polynomial in a field — `missing.fa5932b42daa1a3e0307`

**contextual_ambiguity_or_variant**, 4/4 parents. All four parents use f(α)=0 in a specified extension field; the quotient-field parent correctly assumes irreducible f, so the residue class of x is a root. Roots are elements, not evaluation homomorphisms, whole splitting fields, or root multiplicities. A root need not be a root of unity (0 roots T), and T² has one distinct root despite degree two. A canonical-context defect remains: it says K=F[x]/(f) for nonconstant f without requiring irreducibility. F[T]/(T²) has a nonzero nilpotent T-class and is not a field, although that class satisfies the equation. The generic field-root prerequisite is sound in these sources; the abbreviated quotient example needs the irreducibility qualification. Proposed clarification NOT APPLIED.

Remaining: Adjudicate qualification of the canonical quotient example; actual parent sources do not exhibit this error.

## 41. groupoid — `missing.1ebe938ec77d5606093e`

**retain_distinct_missing**, 3/3 parents. All three contexts need invertible-arrow categories without an object-set restriction. A large discrete category on all sets has only identity arrows and is a groupoid but is not small in the same universe, separating the existing explicitly small groupoid. In a strict (2,1)-category this applies to arrows in each hom-category, hence to VERTICAL inverses of 2-cells, not inverses of 1-arrows. Cartesian lifting over identity arrows in a fibred groupoid forces vertical arrows invertible by unique factorization. The setoid parent imposes trivial automorphism groups in addition: if u,v:x→y then v^−1u is an automorphism, so u=v. None of these restrictions makes the general groupoid small or a single group.

Remaining: A set-theoretic equivalence relation on a possibly proper object collection needs a universe/class convention in the setoid parent; it does not justify silently imposing smallness.

## 42. quotient topology on Y for f — `missing.0c5a27f2980fc722cbb5`

**retain_distinct_missing**, 3/3 parents. The three sources use τ_Q={U⊆Q:q^−1(U) open in X} for the specified surjective target Q. Inverse images preserve unions and finite intersections, proving these sets form a topology. It is final for q and need not equal an externally supplied subspace topology; strictness asks exactly for that agreement on f(X), not surjectivity onto Y. A quotient set supplies no topology by itself. The known submersive biconditional does not imply surjectivity: include a singleton into a discrete two-point space; every preimage is open and every subset of the target is open, yet one point is missed. Keep its separate surjectivity clause and existing source-wording deferral.

Remaining: The already-adjudicated submersive wording issue remains unchanged; no new source correction.

## 43. multiplicative subset of commutative ring — `missing.0c99be984399f9134720`

**source_convention_deferral**, 3/3 parents. All three denominator occurrences invoke multiplication-closed S. The recorded candidate additionally contains 1_R. In a unital ring the nonzerodivisors contain 1 and are closed: if abx=0 and a,b are regular, first bx=0 then x=0. But all three stored formulations omit an explicit unit axiom, and the effective generic ring targets allow no identity. Multiplicative closure alone does not produce a unit: {0} is closed in Z but does not contain 1. Neither does a bare subset define a localization or require denominators be regular; the canonical context does not exclude 0, so no such exclusion is invented. Retain the unital multiplicative-set type while deferring the exact source conventions rather than certifying narrower hypotheses.

Remaining: Later check multiplicative-set/unit and zero-denominator conventions separately for the three source versions; no external lookup now.

## 44. S⊗_R R′ — `missing.2d82e7722cfbce9eca14`

**retain_distinct_missing**, 3/3 parents. All three occurrences form the commutative algebra S⊗_R R′ with product (s⊗a)(t⊗b)=st⊗ab and unit 1⊗1. The balanced tensor relations respect multiplication because coefficient images commute; this extends the module tensor to an algebra. Existing module tensor lacks that multiplication; existing base-change ring-map defines the arrow R′→S⊗_R R′ rather than the whole algebra object. The earlier scalar-extension candidate assumes a FIELD base and field extension, while here R,R′ are arbitrary rings (e.g. R=Z,R′=Z/2); no alias erases that restriction. Fibre products reverse the affine ring direction and are additional scheme constructions, not tensor modules or the induced map.

Remaining: No external citation or complete host-theorem certification; no semantic change proposed.

## 45. natural transformations lying over identity arrows — `missing.5a53cd2d53ef5891adcb`

**retain_distinct_missing**, 3/3 parents. The three sources use α_x:H(x)→K(x) natural in x with q(α_x)=id_{p(x)} and qH=qK=p. These equations preserve base objects/arrows, not identity of the total transformation: over the terminal category every natural transformation is over the base, including nonidentity ones in a one-object group category. An identity 2-cell is more restrictive. Vertical composition stays over identities because q(βα)=q(β)q(α)=id. Setoids or fibred sets impose additional fibre constraints but do not change this definition. Existing strict 2-category packages arbitrary 2-cells; presheaf natural-transformation candidate has a different domain and set-valued codomain and no such projection condition.

Remaining: No external citation or complete host-theorem certification; no semantic change proposed.

## 46. subfield of E — `missing.631bb780e939ffa2b71f`

**retain_distinct_missing**, 3/3 parents. All three sources use an embedded field with inherited operations and the SAME zero/one as its ambient field. Nonzero inverses are essential: Z⊆Q is a unital subring but not a subfield because 2 has no inverse in Z. Generic field definition does not specify an embedding, and prime subfield is the smallest such field, not every subfield. Generated k(B) is least for a chosen generator set; arbitrary subfields need not be generated by a preselected B or finite over a preselected base. An extension E/F encodes the inclusion in the opposite naming direction but is a pair, not the isolated embedded-subfield predicate. Intermediate k⊆L⊆K adds lower containment without changing inherited operations.

Remaining: No external citation or complete host-theorem certification; no semantic change proposed.

## 47. sends closed subsets to closed subsets — `missing.751471447065f0d756cd`

**retain_distinct_missing**, 3/3 parents. All three parents test a SPECIFIED continuous map on every closed subset of its source. Closedness is distinct from continuity, which tests inverse images of closed subsets, and from universal closedness, which repeats the image test after all stated base changes. For example R→{*} is closed, whereas its product with id_R is a projection R²→R that sends the closed hyperbola xy=1 to R\{0}, not closed. Thus merely closed does not imply Bourbaki-proper or universally closed. Product vs fibre-product and topological vs scheme base-change quantifiers remain distinct; the candidate says general topology and only describes scheme base change as one instance.

Remaining: No external citation or complete host-theorem certification; no semantic change proposed.

## 48. coefficient sequence (a_n) — `missing.80fe89921faf5393a2c5`

**retain_distinct_missing**, 3/3 parents. The three contexts all start with a function N_0→R. The index includes 0, and the coefficients themselves need not converge; a_n=1 for every n is a valid sequence even though Σa_n diverges. A sequence differs from its range: the two alternating sequences 0,1,0,1,... and 1,0,1,0,... have the same range but different values at index 0. Existing typed function supplies underlying map data, but an arbitrary function does not fix this domain and codomain. Existing rational-sequence meaning has Q codomain, excluding a constant irrational sequence. A power-series expression, its partial sums and an evaluated generating function have different object types and additional convergence requirements.

Remaining: No external citation or complete host-theorem certification; no semantic change proposed.

## 49. lift S→A/I to S→A — `missing.9b77bf68dde01674ecf2`

**retain_distinct_missing**, 3/3 parents. All three parents use a map g:S→A with qg=f for the specified R-algebra maps and square-zero quotient q. A lift is neither q nor its target ring A/I; it includes the source S and the chosen f. Existence and uniqueness are independent conditions on the set of solutions: at-most-one permits an empty solution set, whereas formally smooth requests nonempty. For R=k,S=k[T],A=k[ε]/(ε²),f(T)=0 in k, maps T↦cε give distinct lifts, showing existence need not imply uniqueness. The square-zero hypothesis is common to these parents but does not itself force lifting. Field K/k is a specialization R=k,S=K, not a different direction or a mere polynomial root.

Remaining: No external citation or complete host-theorem certification; no semantic change proposed.

## 50. arbitrary direct product ∏_j Q_j of R-modules — `missing.a2b8dbc04d465756c102`

**retain_distinct_missing**, 3/3 parents. All three uses are products of R-modules with unrestricted coordinate support. For maps h_i:N→Q_i the tuple map n↦(h_i(n)) is the unique R-linear map with all prescribed coordinates, proving the product universal property. For Q_i=Z indexed by positive integers, (1,1,...) lies in the product but not the finite-support direct sum. In a finite family the constructions agree canonically; that fact does not extend to arbitrary families. The countable inverse limit is a SUBMODULE of the product cut out by transition equations, not the entire product. Empty product is the zero/terminal module, distinct from declaring the product an empty set. Tensor comparison injectivity is additional.

Remaining: The generic categorical product supplies a universal specification; concrete module operations and the particular family are retained rather than identifying the whole parent with that specification.

## 51. cone arrows L→F(i) compatible with all arrows of I — `missing.ab1dee70553ea0ff2c1c`

**retain_distinct_missing**, 3/3 parents. For each arrow a:i→j in I, a cone has legs λ_i:L→F(i) with F(a)λ_i=λ_j. This is a natural transformation const_L⇒F and contains no universal factorization axiom. Over a single-object identity diagram in Sets, any map L→X is a cone, while a limit leg must be a bijection to X; a singleton mapping into a two-element set separates them. For a cospan X→S←Y, the leg to S is determined by the common composite of the two displayed legs, so fp=gq supplies exactly the specialized cone. Reversing the legs gives a cocone; replacing equality with invertible 2-cells gives pseudocone data, neither the same prerequisite. Existing limit and fibre-product meanings impose universality.

Remaining: No external citation or complete host-theorem certification; no semantic change proposed.

## 52. local ring homomorphisms — `missing.b05a1814a9da0d01922a`

**retain_distinct_missing**, 3/3 parents. For a unital map of commutative local rings φ:(R,m)→(S,n), local means φ^−1(n)=m. The equivalent condition φ(m)⊆n uses that units in R map to units in S: every r∉m is a unit and cannot land in n. Unitality is essential to this argument. Merely mapping local rings is insufficient: Z_(p)→Q is unital between local rings, but the inverse image of maximal ideal 0 is 0 rather than pZ_(p). The existing local-ring meaning describes objects, while unital ring-map meaning does not enforce localness. Stalk maps reverse the continuous-space direction and require the same ideal condition, not a homeomorphism or sheaf-surjectivity condition.

Remaining: Previously adopted local-ring unit source-scope deferral remains; this verifies the map condition under its stated unital interpretation.

## 53. cover of Spec(R) by standard opens D(f_i) — `missing.b3329d7bb30dc66927f6`

**retain_distinct_missing**, 3/3 parents. All three parents use a family of principal opens with union Spec(R). One distinguished open is not a cover: D(2) in Spec(Z) misses (2); D(2),D(3) cover because no prime contains both 2 and 3. Generally the family covers iff no prime contains all f_i, equivalently the generated ideal is R under standard maximal-ideal existence. Finiteness of the particular cover is extra: finite generation of the unit ideal may supply a finite subcover but does not make the original indexing family finite. Module finite rank, local freeness and gluing transition isomorphisms are not properties of an arbitrary cover. Generic open-cover candidate has arbitrary topology and opens, whereas this construction fixes Spec(R) and distinguished opens.

Remaining: No external citation or complete host-theorem certification; no semantic change proposed.

## 54. R-linear span of generators m_1,…,m_n — `missing.beea674f8fcd201a1af5`

**contextual_ambiguity_or_variant**, 3/3 parents. Under unital module action, finite R-linear combinations of S form a submodule containing S (s=1s), and every submodule containing S contains those combinations, proving leastness. Arbitrary S still uses finite sums; a finite S does not imply the ambient module is generated unless the span equals M. However the canonical context only says left R-module without a unit condition; its displayed formula can fail for the stored identity-optional module convention. Over R=F₂ with M=C₂ and zero scalar action, S={m≠0}, all finite R-linear combinations are zero, while the least submodule containing S is M. Thus a unit-action qualification or a broader additive-generation formula is needed. The finite-generation parent retains both general historical and unital effective targets; no automatic conclusion about the nine previously adjudicated cases is changed.

Remaining: Adjudicate the canonical span formula scope for nonunital actions; no source, candidate-context or alias correction applied.

## 55. sheaf homomorphism O_Y→f_*O_X — `missing.bf9f155d15473da985d2`

**retain_distinct_missing**, 3/3 parents. The three sources use compatible unital ring homomorphisms on sections O_Y(V)→O_X(f^−1(V)), commuting with all restriction maps. The direction is opposite f:X→Y; the same maps can be expressed by the inverse-image/direct-image adjunction, not by identifying f_* with f^−1. Individual ring maps do not supply restriction compatibility, and a locally ringed-space morphism additionally requires local stalk maps. The closed-immersion phrase combines the direct-image sheaf, a sheaf homomorphism and surjectivity; only its map component is shared. Sheaf surjectivity is a stalk/local-lifting condition, not an automatic statement of surjectivity on all open-section rings. No exact existing ring-sheaf-homomorphism definition was found among checked sheaf/ringed-space meanings.

Remaining: Future segmentation should preserve the pushforward object and sheaf-surjectivity content of occ.43b37334a3e5e3c5f7ea; no identity of that whole phrase with a bare sheaf map is certified.

## 56. I^n M — `missing.d066de85583ac1b1a7d4`

**source_convention_deferral**, 3/3 parents. Finite sums Σi_jm_j form a submodule: addition concatenates sums, negatives can be absorbed in the ideal, and r(i_jm_j)=(ri_j)m_j remains of the same form. This differs from ideal multiplication, whose outputs lie in R, and from M/IM, whose elements are cosets. Taking I^n specializes the same ideal action. For unital M, RM=M; a ring identity alone does not force this for broad actions (the zero-action C₂ module over F₂ has RM=0). The canonical type restricts R to commutative unital, while the three paraphrases leave ambient conventions implicit; current module targets use the unital specialization. Positive ideal powers are meaningful more generally, but that does not authorize broadening this canonical type or applying I^0M=M universally.

Remaining: Later source-specific reconciliation must establish ring commutativity/unit and module action convention in all three parent formulas; no general/specialized identities are merged.

## 57. factors completely into linear factors over E — `missing.d0ca7fa93046fab7ab04`

**retain_distinct_missing**, 3/3 parents. The three contexts require the nonzero polynomial to factor as c∏(T−α_j) in the stated extension field, with leading scalar and multiplicities retained. One root is insufficient: (T−1)(T²+1) has a rational root but does not split over Q. Repeated factors are allowed, so T² splits though it is not separable. Having a splitting over E does not make E the splitting field: T²−1 splits over Q(t), but that larger field is not generated by its roots. Normal-extension parents add universal quantifiers over their stated irreducibles or minimal polynomials; those quantifiers are not part of splitting a single polynomial. Existing splitting-field and normal-extension meanings therefore require extra data and cannot resolve the general factorization predicate.

Remaining: No external citation or complete host-theorem certification; no semantic change proposed.

## 58. precomposition — `missing.de1b7a5e3717e67b42a7`

**retain_distinct_missing**, 3/3 parents. Every parent sends h:T→X to hα:T′→X for α:T′→T. Associativity gives (αβ)^*(h)=hαβ=β^*(α^*(h)), and identity arrows induce identity maps, establishing contravariance in the variable source. Postcomposition instead changes the target; it is not this operation with arrows reversed silently. Module transitions u_ij:M_i→M_j produce Hom(M_j,N)→Hom(M_i,N), preserving linearity by composition, hence an inverse system. This does not force stabilization of images, which is the Mittag-Leffler requirement. Existing contravariant-functor meaning is a whole functor and its axioms, not the particular Hom operation; internal Hom is an object with extra algebraic structure.

Remaining: No external citation or complete host-theorem certification; no semantic change proposed.

Next: `missing.de3c256ab9b24566d9a4`, first parent `form.wave2.research81.martingale-continuous-index.01`. Full source/node hashes, provenance, effective references and occurrence-specific assessments are in the JSONL evidence.
