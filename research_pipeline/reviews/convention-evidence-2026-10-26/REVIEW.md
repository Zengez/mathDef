# Wave 2 source-free contextual evidence — 2026-10-26

**Status: prepared for ChatGPT/user adjudication; no decision or graph action applied.**

Base: engineering `51696c08b1e5e8b7964ad4f1599e61acc9301ff9`, current main mathematical checkpoint `a7ce2ba3cdd07e6d0b9809d4e39014fb8533228c`. Historical evidence is pinned to `978db08b2fe736638237c6967f934dbfe96894a3`; its graph snapshot was not read or imported.

All 40 historical candidates remain unresolved: 13 convention deferrals and 27 contextual ambiguities. Across 104 parent visits / 93 distinct formulations, all original source versions remain the same. Thirty-nine cases also have unchanged effective nodes. Rank 399 has a receipt-backed changed node: the old global-basis link is external provenance, while the pointwise connected-neighborhood candidate remains missing. Resolution/alias effects are not inferred from node hashes alone.

Read [the decision index](ADJUDICATION_QUEUE.md) first. `EVIDENCE.json` is the comprehensive machine inventory: exact historical review and occurrence IDs, all historical and current hashes, full source observations and provider records, live nodes and effective edges including seeds/overrides/resolutions, existing target variants, and current comparison candidates. `CONTEXTS.md` contains every captured full current formulation, not excerpts. Shared context keys deduplicate texts; all variants of every implicated source/linked/compared meaning are included. Captured targets are one-level evidence for these cases, not a new global proof audit of every target theorem.

The complete historical mathematical justification and residual uncertainty are preserved per case in the inventory. The arguments below are the current preparation conclusions, not source certification. Recommended dispositions and possible wording/segmentation changes are **not applied**. A current unresolved candidate is not automatically a Pass 2 blocker. Any later bounded deferral, consolidation decision or graph change requires separate adjudication.

Applied real-time filtration, Ext/Hom, local-connectedness, order-zero S-linearity and m-primary corrections are reconciled in [SOURCE_DEFERRALS.md](SOURCE_DEFERRALS.md) with actual receipt evidence. The four provisional source issues and topological inverse-continuity gap remain separately documented; none is silently promoted to a gate blocker.

## 01 Ring and algebra conventions

<a id="case-007"></a>
### Rank 7 — commutative unital ring

Canonical candidate: `missing.5645554e6bee6b40edda`. Historical `canonical-review.2026-10-24.009`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** Associative, commutative, specified unit are separate conditions. Zero ring is not excluded by the bare candidate; field/domain parents explicitly require 0≠1. Eleven sources: five explicit-unit, six bare commutative-ring formulations.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.003cb1cc70cf5a2c.locally-nilpotent-ideal`](CONTEXTS.md#context-001): An ideal I in a commutative ring R is locally nilpotent (in the Stacks Project terminology) when each element x of I is nilpotent, with the exponent allowed to depend on x.
- [`form.03b55b8ca41abb20.jacobson-ring`](CONTEXTS.md#context-003): A commutative ring R is a Jacobson ring when every radical ideal I of R equals the intersection of the maximal ideals of R containing I.
- [`form.03b55b8ca41abb20.jacobson-ring-prime-characterization`](CONTEXTS.md#context-004): Equivalently, a commutative ring R is Jacobson if each prime ideal p is the intersection of all maximal ideals containing p.
- [`form.097db25e2f156689.clopen-subset-of-spectrum`](CONTEXTS.md#context-007): For a commutative ring R, a subset U of Spec(R) is simultaneously open and closed exactly when there is an idempotent e of R (so e²=e) such that U=D(e)={p in Spec(R):e is not in p}; this e is unique.
- [`form.363d711d668364b7.normal-ring`](CONTEXTS.md#context-028): A commutative ring R is normal if each localization R_p at a prime ideal p is an integrally closed domain in its own fraction field.
- [`form.ed035ec300dc4ceb.irreducible-component-spectrum`](CONTEXTS.md#context-124): For a commutative ring R, the irreducible components of Spec(R) are exactly the subsets V(p) where p ranges over prime ideals minimal under inclusion.
- [`form.wave2.foundation.commutative-maximal-ideal`](CONTEXTS.md#context-159): Let R be a commutative ring with identity. An ideal m of R is maximal if m is properly contained in R and every ideal J with m⊆J⊆R satisfies J=m or J=R.
- [`form.wave2.foundation.commutative-prime-ideal`](CONTEXTS.md#context-160): Let R be a commutative ring with identity. An ideal P⊊R is prime if, for all a,b∈R, ab∈P implies a∈P or b∈P.
- [`form.wave2.foundation.field-commutative-unital`](CONTEXTS.md#context-161): A field is a commutative ring k with identity 1_k, with 0≠1_k, such that for every a∈k with a≠0 there exists b∈k satisfying ab=1_k (and hence ba=1_k).
- [`form.wave2.foundation.integral-domain`](CONTEXTS.md#context-162): An integral domain in the Stacks commutative-unital convention is a nonzero commutative ring R with identity 1_R in which ab=0 implies a=0 or b=0 for every a,b in R.
- [`form.wave2.foundation76.noetherian-module.01`](CONTEXTS.md#context-184): A module M over a commutative ring A with identity is Noetherian when every A-submodule of M is finitely generated.

**Mathematical argument:** The zero-product ring on C2 is commutative but has no identity; M2(Q) has an identity but is noncommutative. Z/4 is commutative unital but neither a field nor a domain. Thus none of the existing general ring, field or domain meanings equals this candidate. The six bare-ring paraphrases cannot acquire a unit axiom solely from their provider label. The three Noetherian-module variants must retain their explicit unital coefficient scope; the prime/maximal properness predicates do not exclude the zero ring from the generic coefficient type.

**Interpretations:**

- commutative unital type: Valid distinct structured type, not general identity-optional ring.

- bare source ring: Unit and zero-ring convention not independently established by the text.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** Distinct types and exact explicit/implicit source partition can be decided. No blanket existing-meaning resolution follows.

**Further evidence or judgment:** Later verify source conventions for the six listed bare sources, including 1=0; user may choose a documented deferral policy without claiming source verification.

**Compared existing targets, all stored variants retained:** `meaning.86b5d488b98c612f.noetherian-commutative-ring`; `meaning.wave2.foundation.associative-ring-identity-optional`; `meaning.wave2.foundation.field-commutative-unital`; `meaning.wave2.foundation.integral-domain`.

**Historical candidate occurrence anchors:** `occ.7f61ca79f1d97c770d8e`, `occ.79e76d1d0b4edf155f8b`, `occ.28b8e4cdf8149afbb555`, `occ.503af4f588926b6b3c02`, `occ.dde392eb5024a329e6bc`, `occ.a72d23a710b9bad93be7`, `occ.f3d1c03462a078238f4b`, `occ.300fe64a3e587b160c5a`, `occ.9b28c848da1a3d59ad24`, `occ.f0091a2c435aa7fb43a9`, `occ.09559617b0c116793abe`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-023"></a>
### Rank 23 — commutative unital algebra over a field

Canonical candidate: `missing.3b37131115a06556c3e4`. Historical `canonical-review.2026-10-24.025`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** Five k-algebra sources over a nonzero commutative field k. Candidate: commutative unital A plus a specified unital structure map k→A; zero algebra convention unstated.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.2a93c6a662a51d67.geometrically-normal-algebra`](CONTEXTS.md#context-021): A k-algebra A is geometrically normal over a field k if for every extension of fields K/k the base-changed algebra K⊗_k A is a normal ring.
- [`form.2a93c6a662a51d67.geometrically-normal-perfect-closure-test`](CONTEXTS.md#context-022): Equivalently, a k-algebra A is geometrically normal if its scalar extension k^perf⊗_k A to the perfect closure of k is a normal ring; this also tests normality over all finite purely inseparable field extensions.
- [`form.2c5739452921ea24.geometrically-irreducible-algebra`](CONTEXTS.md#context-023): A k-algebra A is geometrically irreducible over the field k when, for every field extension K/k, the ring A⊗_k K has exactly one minimal prime ideal, equivalently its prime spectrum is irreducible.
- [`form.6c51aeb904a0fe74.geometrically-reduced-algebra`](CONTEXTS.md#context-058): A k-algebra A is geometrically reduced if for every field extension K/k the tensor-product K-algebra A⊗_k K is a reduced ring.
- [`form.c236facceae1dd0f.geometrically-regular-noetherian-algebra`](CONTEXTS.md#context-105): A Noetherian k-algebra R is geometrically regular over a field k if R⊗_k K is a regular ring for every finite field extension K/k; equivalently this holds for all field extensions K/k under the hypotheses of the Stacks criterion.

**Mathematical argument:** The map determines c·a=φ(c)a, so a bare ring forgets base-field structure. k[T] is an algebra without being a field; k[ε]/(ε²) is an algebra without being a domain or reduced. A ring homomorphism is the structure arrow, not the whole algebra datum. Each parent states k-algebra without independently spelling out commutativity/unit, so geometric spectrum context is evidence of intended specialization, not external convention certification.

**Interpretations:**

- algebra object: Preserve the chosen scalar structure.

- field or ring map: Not an identity with either stricter object or structure arrow alone.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** Base field, algebra object, scalar-extension arrow and geometric predicate are distinct.

**Further evidence or judgment:** Verify commutativity, unitality and zero-algebra allowance in all five source versions. Do not silently narrow their universes.

**Compared existing targets, all stored variants retained:** `meaning.415a1503ae7ed97d.finitely-presented-algebra`; `meaning.7210832bc589f307.field-extension`; `meaning.wave2.foundation.field-commutative-unital`; `meaning.wave2.foundation.ring-map-unital`.

**Historical candidate occurrence anchors:** `occ.8c97f35eb2b710452001`, `occ.ead6baaa69e2d6d331c4`, `occ.51e6889eab309227c012`, `occ.3c8a1a79c5bbd89954f8`, `occ.29dc6ffd5341ec86cd59`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-043"></a>
### Rank 43 — multiplicative subset of commutative ring

Canonical candidate: `missing.0c99be984399f9134720`. Historical `canonical-review.2026-10-24.045`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** Localization denominators in three sources. Canonical S⊆R contains 1 and is multiplicatively closed; R commutative unital. No canonical exclusion of 0 is recorded.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.559efcb6f15ddc96.total-quotient-ring`](CONTEXTS.md#context-049): The total quotient ring Q(R) of a commutative ring R is the localization S^{-1}R at the multiplicative set S of all nonzerodivisors of R, allowing fractions with any regular denominator.
- [`form.70f44988651b76b5.module-localization-at-multiplicative-set`](CONTEXTS.md#context-061): For an R-module M and multiplicative subset S⊆R, the module S^{-1}M consists of fractions m/s modulo (m,s)∼(m′,s′) when t(s′m−sm′)=0 for some t∈S, with its natural S^{-1}R-module structure.
- [`form.70f44988651b76b5.ring-localization-at-multiplicative-set`](CONTEXTS.md#context-062): Given a commutative ring R and multiplicative subset S⊆R, the localization S^{-1}R is the ring of fractions r/s modulo (r,s)∼(r′,s′) if t(rs′−r′s)=0 for some t∈S.

**Mathematical argument:** Multiplicative closure alone does not imply 1∈S: {0}⊆Z is closed. In a unital ring the regular elements contain 1 and are closed, since abx=0 implies bx=0 then x=0. Allowing 0 gives a degenerate localization under the usual unital construction; it is a convention question rather than permission to discard that input. A multiplicative subset is not the fraction ring or localized module. Existing generic ring targets do not settle the missing unit hypothesis.

**Interpretations:**

- unital denominator subset: Valid prerequisite under recorded candidate scope.

- any closed subset: Broader convention; not identical without adding 1 or choosing a construction.

**Recommended disposition:** convention clarification — **not applied**.

**Decidable now:** Closure, presence of 1, regularity and exclusion of 0 are different properties.

**Further evidence or judgment:** Check source denominator/unit/zero conventions separately for total quotient ring, ring localization and module localization.

**Compared existing targets, all stored variants retained:** `meaning.70f44988651b76b5.ring-localization-at-multiplicative-set`; `meaning.wave2.foundation.associative-ring-identity-optional`; `meaning.wave2.foundation.subset-nonstrict`.

**Historical candidate occurrence anchors:** `occ.46d13d28b26bdd10a412`, `occ.6de9d42ab81ed6b58f63`, `occ.bc87759779f39ba996c6`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-133"></a>
### Rank 133 — commutative unital ring and common identity

Canonical candidate: `missing.0113342523b02aece2fb`. Historical `canonical-review.2026-10-24.135`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** Strong transcendence: R⊆S commutative rings with identity; candidate additionally requires common identity. x∈S, all n≥0, a_i∈R and u∈S.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.wave2.foundation.strongly-transcendental-subring-element`](CONTEXTS.md#context-174): Let R⊆S be an inclusion of commutative rings with identity, and let x∈S. The element x is strongly transcendental over R if for every integer n≥0, coefficients a_0,…,a_n∈R, and u∈S, the equation u(a_0+a_1x+⋯+a_nx^n)=0 implies ua_i=0 for every i=0,…,n.

**Mathematical argument:** R=k×{0}⊂S=k×k consists of individually unital commutative rings with identities (1,0) and (1,1), so common identity does not follow from individually having identities. The historical unital-map seed supports an intended reading but does not establish the cited source convention. Under common identity, taking u=1 in the strong-transcendence implication proves injectivity of evaluation; that consequence must not be used to assume the predicate before defining it.

**Interpretations:**

- common identity inclusion: The canonical structured type.

- individually unital inclusion: Strictly broader; example separates them.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** The two inclusion conventions are different even for commutative rings.

**Further evidence or judgment:** Verify whether this source means identity-preserving subring. Coordinate with ranks 5 and 298, without inferring conventions from the seed.

**Compared existing targets, all stored variants retained:** `meaning.wave2.foundation.associative-ring-identity-optional`; `meaning.wave2.foundation.ring-map-unital`.

**Historical candidate occurrence anchors:** `occ.9c759e556ba18cc2058e`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-252"></a>
### Rank 252 — subring of S

Canonical candidate: `missing.6761326c179c108a8d73`. Historical `canonical-review.2026-10-24.257`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** Integral closure of R in S via a ring homomorphism R→S; candidate subring has commutative, inherited-unit scope. The map need not be injective.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.8594a432b165bcda.integral-closure-relative`](CONTEXTS.md#context-072): For a ring homomorphism R→S, the integral closure of R in S is the subring of S consisting of all elements integral over the image of R.

**Mathematical argument:** For Z→Z/2 the coefficient image is F2, not an embedded copy of Z. Integral elements form a particular selected subring under the commutative convention, but a subring containing coefficients need not be the integral closure. A bare subset loses addition/multiplication, while a bare inclusion does not select the integral elements. The stored source sentence does not itself state all unit/commutativity conventions in the candidate.

**Interpretations:**

- coefficient image subring: Valid component prerequisite, with image rather than domain inclusion.

- integral closure: Extra integrality selection, not any subring.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** Do not rewrite a noninjective structure map as R⊆S.

**Further evidence or judgment:** Check source commutativity and inherited-identity convention; retain integrality selection and map image in any future segmentation.

**Compared existing targets, all stored variants retained:** `meaning.8594a432b165bcda.integral-closure-relative`; `meaning.wave2.foundation.ring-map-unital`.

**Historical candidate occurrence anchors:** `occ.104c85e61c6f21eef305`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-281"></a>
### Rank 281 — local subring inclusion A⊆B

Canonical candidate: `missing.8270eec9d7801be60879`. Historical `canonical-review.2026-10-24.286`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** A⊆B local subrings of one field; domination additionally requires contraction m_B∩A=m_A. Nonzero conventional unital rings share the field identity.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.f72779e263dd3e51.domination-local-rings`](CONTEXTS.md#context-129): For local subrings A⊆B of a common field, B dominates A if the maximal ideal of B contracts to the maximal ideal of A.

**Mathematical argument:** A nonzero idempotent of a field is 1, so the identity of any nonzero unital subring equals that of the field. This is a mathematical conditional result, not evidence that an unstated subring convention is adopted. Inclusion alone does not imply domination: Z_(p)⊂Q has m_Q=0 with contraction 0, not pZ_(p). Both stored local-ring variants need to retain their common nonzero/local hypotheses.

**Interpretations:**

- unital local subring inclusion: Common identity follows conditionally.

- domination: Strictly stronger maximal-ideal contraction datum.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** Shared field identity and failure of automatic domination are established under the stated conventional hypotheses.

**Further evidence or judgment:** Verify local-ring/subring conventions of this exact source; no new generic alias to domination.

**Compared existing targets, all stored variants retained:** `meaning.4f7edb6d32334f67.local-ring-unique-maximal`; `meaning.f72779e263dd3e51.domination-local-rings`.

**Historical candidate occurrence anchors:** `occ.197229d2d272838f7f9b`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

## 02 Ideal action and module grading

<a id="case-018"></a>
### Rank 18 — ideal product IJ

Canonical candidate: `missing.e43d4f1922e210cc373a`. Historical `canonical-review.2026-10-24.020`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Positive products of two-sided ideals make sense in associative rings without unit/commutativity. Canonical product uses commutative unital R and I^0=R when n≥0.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.003cb1cc70cf5a2c.nilpotent-ideal`](CONTEXTS.md#context-002): An ideal I of a ring R is nilpotent when there is a single positive integer n for which the product ideal I^n is the zero ideal.
- [`form.05531f966e3a206f.dedekind-domain`](CONTEXTS.md#context-005): An integral domain R is a Dedekind domain in this factorization characterization if every nonzero ideal factors as a finite product of nonzero prime ideals and this decomposition is unique up to permuting the factors.
- [`form.3fe40ac4fb74bff2.pure-ideal-intersection-test`](CONTEXTS.md#context-035): Equivalently, an ideal I⊆R is pure when I∩J=IJ for every ideal J of R; it is enough to test finitely generated ideals J.
- [`form.a38f1da0bc017afe.noetherian-i-adic-completion`](CONTEXTS.md#context-089): For a Noetherian commutative ring R and ideal I, the I-adic completion R^ is the inverse-limit ring lim_n R/I^n, with structure homomorphism R→R^ induced by the quotient maps.
- [`form.a4bbabe606a10067.rees-blowup-algebra`](CONTEXTS.md#context-090): Given an ideal I of a commutative ring R, the Rees algebra of I is the nonnegatively graded R-algebra ⊕_{n≥0}I^n, with I^0=R and multiplication induced by the products I^m I^n⊆I^{m+n}.
- [`form.f3421024042fb45b.symbolic-power-prime-ideal`](CONTEXTS.md#context-127): For a prime ideal p of a commutative ring R and n≥0, the nth symbolic power p^(n) is the contraction to R of p^n R_p, equivalently the kernel of R→R_p/p^nR_p.

**Mathematical argument:** Finite sums of ij define IJ; two-sided absorption proves closure. In Z, (2)(2)=(4) differs from (2)∩(2). In the nonzero zero-product C2 ring, I=R has I²=0 despite no multiplicative identity, so the broad nilpotent-ideal source is mathematically meaningful beyond the canonical scope. Symbolic powers use localization/contraction and must not be read as ordinary powers. Source-specific purity equalities and positive/nonnegative exponent choices remain separate.

**Interpretations:**

- positive ideal product: Valid reusable operation in broader rng scope.

- canonical unital specialization: Covers the commutative-unital parents but not every broad-ring reading.

**Recommended disposition:** genuine policy decision — **not applied**.

**Decidable now:** General versus specialized operations and the scope mismatch are demonstrable.

**Further evidence or judgment:** User must decide whether underlying prerequisites may be recorded polymorphically or need distinct scoped identities; alternatively exact source verification may establish a narrower parent intent. No old alias is reversed.

**Compared existing targets, all stored variants retained:** `meaning.003cb1cc70cf5a2c.nilpotent-ideal`; `meaning.f3421024042fb45b.symbolic-power-prime-ideal`; `meaning.wave2.foundation.associative-ring-identity-optional`; `meaning.wave2.foundation.two-sided-ideal`.

**Historical candidate occurrence anchors:** `occ.6382ae14011d622d9352`, `occ.c1efd20ad644d724ea9b`, `occ.007b04e9d94f6ea51946`, `occ.0f9f25f54aa0dd5b9fc4`, `occ.11b529bbb6518e3584b0`, `occ.ef81e693551e30a4d7b5`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-054"></a>
### Rank 54 — R-linear span of generators m_1,…,m_n

Canonical candidate: `missing.beea674f8fcd201a1af5`. Historical `canonical-review.2026-10-24.056`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Span of a subset S of a left module; finite combinations, not infinite sums. Unit action is needed for the usual formula to contain S.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.91ebb3796458d5bb.finite-generated-module`](CONTEXTS.md#context-084): An R-module M is finitely generated if there exist m_1,…,m_n∈M such that M=Rm_1+⋯+Rm_n; equivalently there is a surjective homomorphism R^n→M for some finite n.
- [`form.cbe7158b0742af88.colimit-modules`](CONTEXTS.md#context-108): The colimit of a diagram (M_i,μ_ij) of R-modules is the quotient of the direct sum ⊕_i M_i by the submodule generated by all elements ι_i(m)−ι_j(μ_ij(m)) for i≤j.
- [`form.db846ebeca42b9ee.finitely-generated-module-stacks`](CONTEXTS.md#context-114): An R-module M is finitely generated if a finite list m_1,…,m_n generates all of M by R-linear combinations; equivalently there is an R-linear surjection R^n→M.

**Mathematical argument:** In a unital module, s=1s and closure proves the finite-combination set is the least submodule containing S. For the zero action of F2 on C2 and S={m≠0}, all R-linear combinations vanish while the least submodule containing S is C2. For the general nonunital convention the generated submodule must also include additive integer combinations of S. Thus the candidate formula cannot be certified over every stored left-module type. The finite-generation source retains a broad historical seed and a unital effective module prerequisite, not two proved equivalent conventions.

**Interpretations:**

- unital span: Formula valid.

- general generated submodule: Formula without additive closure of original generators can fail.

**Recommended disposition:** convention clarification — **not applied**.

**Decidable now:** The missing unit-action qualification has a concrete counterexample.

**Further evidence or judgment:** Adjudicate candidate scope versus a broader generation formula and document historical seed specialization; no automatic source correction.

**Compared existing targets, all stored variants retained:** `meaning.91ebb3796458d5bb.finite-generated-module`; `meaning.wave2.foundation.left-module-nonunital`; `meaning.wave2.foundation76.submodule`; `meaning.wave2.module94.unital-left-module`.

**Historical candidate occurrence anchors:** `occ.03e7f2690d2d1f77a190`, `occ.144e8bd61f46a88e0d0f`, `occ.810460027f5255964f2d`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-056"></a>
### Rank 56 — I^n M

Canonical candidate: `missing.d066de85583ac1b1a7d4`. Historical `canonical-review.2026-10-24.058`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** IM or I^nM is a submodule of M, not an ideal power in R or a quotient. Canonical R commutative unital; three parents leave ring/action conventions implicit.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.1be2fa074ef447b0.i-adic-completeness`](CONTEXTS.md#context-012): An R-module M is I-adically complete when its canonical map M→lim_n M/I^n M is an isomorphism; a ring R is I-adically complete when it has this property as its own module.
- [`form.1be2fa074ef447b0.i-adic-module-completion`](CONTEXTS.md#context-013): For an R-module M and ideal I⊆R, the I-adic completion of M is lim_n M/I^n M; its elements can be viewed as mutually compatible residue classes modulo powers of I.
- [`form.951ae8411d8a974b.depth-module-ideal`](CONTEXTS.md#context-086): For a finite R-module M and ideal I⊆R, depth_I(M) is the supremum of lengths of M-regular sequences whose entries lie in I when IM≠M, and is defined to be infinite when IM=M.

**Mathematical argument:** Finite sums i_jm_j are closed under negatives, sums and scalar action, since r(i_jm_j)=(ri_j)m_j. For a unital action RM=M; for the zero F2-action on nonzero C2, RM=0 instead. Thus I^0M=M when I^0=R depends on unital action, even if the ring itself has a unit. The quotient M/I^nM and its inverse limit require separate constructions and indices.

**Interpretations:**

- ideal action: Valid component distinct from ideal multiplication and quotient.

- zero power identity: Conditional on unital action; not a general left-module theorem.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** The operation and conditional unit identity are proved; no equivalence with ideal multiplication.

**Further evidence or judgment:** Check coefficient commutativity/unit, module unit action and index starting value in all three sources.

**Compared existing targets, all stored variants retained:** `meaning.wave2.foundation.left-module-nonunital`; `meaning.wave2.foundation76.submodule`; `meaning.wave2.module94.unital-left-module`.

**Historical candidate occurrence anchors:** `occ.e772e8b976e03adf5a87`, `occ.b5152a551116c69d072a`, `occ.c2710fc6cf7687827f9d`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-095"></a>
### Rank 95 — direct sum decomposition M=⊕_j M_j

Canonical candidate: `missing.72b9f9bc4ac0e952e202`. Historical `canonical-review.2026-10-24.097`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Internal direct sum of additive subgroups; module uses j∈Z, ring uses n≥0. Scalar multiplication may shift degree.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.fa3b484c09596cfd.graded-module`](CONTEXTS.md#context-131): A graded module M over S=⊕_{n≥0}S_n is an S-module with a direct-sum decomposition M=⊕_{j∈Z}M_j and S_nM_j⊆M_{n+j}.
- [`form.fa3b484c09596cfd.nonnegatively-graded-ring`](CONTEXTS.md#context-132): A nonnegatively graded ring S is a direct sum S=⊕_{n≥0}S_n of additive groups satisfying S_nS_m⊆S_{n+m} for every n,m≥0.

**Mathematical argument:** For S=k[t], each homogeneous subgroup kt^j is generally not an S-submodule, because multiplication by t changes degree. Direct sum means each element has finitely many nonzero components; product permits infinitely many. A nonnegative grading can be extended by zero in negative degrees, but Z-gradings with nonzero negative pieces are not nonnegative gradings. The common additive decomposition is a valid prerequisite; equality of whole indexed graded structures is not established.

**Interpretations:**

- additive direct sum: Shared finite-support construction.

- module direct sum or same grading: Adds scalar or index conditions absent from the common operation.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** Group/module distinction and embedding versus equivalence of index conventions are settled.

**Further evidence or judgment:** Choose a generic index-set additive prerequisite or explicitly scoped variants; preserve each source grading and compatibility.

**Compared existing targets, all stored variants retained:** `meaning.fa3b484c09596cfd.graded-module`; `meaning.fa3b484c09596cfd.nonnegatively-graded-ring`; `meaning.wave2.foundation.abelian-group`.

**Historical candidate occurrence anchors:** `occ.9088747c6557b7874011`, `occ.3c4dbdc9d83b9ed70713`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-175"></a>
### Rank 175 — induced exterior-power map ∧^rφ

Canonical candidate: `missing.25dac0c185025e52a26a`. Historical `canonical-review.2026-10-24.178`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** Finite free R-modules R^m→R^n; ordinary exterior powers over commutative unital R. r≥0; ∧^0φ=id_R, ∧^1φ=φ.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.41e3aea7f356bae3.rank-of-map-finite-free`](CONTEXTS.md#context-037): For a homomorphism φ:R^m→R^n of finite free modules, its rank is the largest integer r for which the induced exterior-power map ∧^rφ is nonzero (and is zero when φ itself is zero).

**Mathematical argument:** The alternating map (v_1,…,v_r)↦φ(v_1)∧…∧φ(v_r) descends to a linear induced map by the exterior-power universal construction. It is not the exterior module itself. Over Z/4, multiplication by 2 has nonzero ∧^1 but becomes zero after reduction modulo 2; the stored nonzero-exterior-map rank criterion therefore must not be silently replaced by constant fibre rank or an invertibility test. Zero rings require care at r=0, where id_R is the zero map.

**Interpretations:**

- ordinary exterior map: Valid under the commutative coefficient framework.

- arbitrary left modules: No ordinary noncommutative construction follows without extra data.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** Induced-map formula and distinction from fibrewise rank are established conditionally.

**Further evidence or judgment:** Verify coefficient commutativity/unit, r=0 and zero-ring conventions. No new noncommutative exterior construction or rank theorem proposed.

**Compared existing targets, all stored variants retained:** `meaning.41e3aea7f356bae3.rank-of-map-finite-free`; `meaning.wave2.module94.unital-left-module`.

**Historical candidate occurrence anchors:** `occ.36b73d7bd2a48315f0c7`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-358"></a>
### Rank 358 — graded associative R-algebra

Canonical candidate: `missing.c5a7afab433a3e7d30ed`. Historical `canonical-review.2026-10-24.363`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** Tensor algebra T_R(M)=⊕_{n≥0}M^{⊗n}, degree zero R, concatenation. Ordinary module tensor typing needs commutative coefficients or appropriate right-left/bimodule data.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.445e8dc5147c408d.tensor-algebra`](CONTEXTS.md#context-038): For an R-module M, its tensor algebra is the graded associative R-algebra obtained by taking the direct sum over n at least zero of the n-fold tensor powers of M, with the degree-zero summand R and multiplication by concatenation of tensors.

**Mathematical argument:** For free rank-two M over a field, ef and fe are distinct tensor words, so this algebra need not be commutative even though the scalar ring is. The generic tensor-product formulation says two R-modules and an R-module-valued bilinear universal property without stating the scalar convention. Arbitrary left modules over a noncommutative ring are not automatically composable tensor inputs of that type. A graded additive module or commutative graded ring cannot resolve the whole associative algebra datum.

**Interpretations:**

- commutative base associative algebra: Standard typed interpretation, still noncommutative multiplication allowed.

- noncommutative base: Requires bimodule or other explicit tensor data, not supplied here.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** Base commutativity and algebra commutativity are different; module versus algebra data are different.

**Further evidence or judgment:** Verify intended scalar/action framework and degree-zero unit. Do not repair the generic tensor definition implicitly.

**Compared existing targets, all stored variants retained:** `meaning.445e8dc5147c408d.tensor-algebra`; `meaning.74e36635b2776fe8.tensor-product-modules`; `meaning.fa3b484c09596cfd.graded-module`; `meaning.fa3b484c09596cfd.nonnegatively-graded-ring`.

**Historical candidate occurrence anchors:** `occ.9c4dc9f50f4a8f4893c7`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-400"></a>
### Rank 400 — graded differential complex Ω^•

Canonical candidate: `missing.ebf92c196007c438f394`. Historical `canonical-review.2026-10-24.406`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** A→B, Ω^p=∧^p_BΩ^1, Ω^0=B; d increases degree, d²=0. Components B-modules, differential A-linear in the ordinary commutative setting.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.711d6a9a3f5a61ca.relative-de-rham-complex`](CONTEXTS.md#context-063): For a ring homomorphism A→B, the relative de Rham complex Ω^•_{B/A} is the graded complex with Ω^p_{B/A}=∧^p_B Ω^1_{B/A}, Ω^0=B, and differentials d:Ω^p→Ω^{p+1} uniquely extending the universal derivation and satisfying d(b_0 db_1∧⋯∧db_p)=db_0∧db_1∧⋯∧db_p.

**Mathematical argument:** For A=k, B=k[t], d(t)=dt while t·d(1)=0; hence d is not B-linear. Restricting scalars gives a complex of A-modules or abelian groups. Wedge multiplication supplies differential graded algebra structure beyond a bare cochain complex. A chain complex with differential lowering degree is not the displayed cohomological grading. The existing derivation and Kähler meanings explain these types but do not license erasing the base ring.

**Interpretations:**

- A linear cochain complex: Mathematically supported underlying prerequisite.

- B linear complex: Rejected in general by k[t] counterexample.

**Recommended disposition:** convention clarification — **not applied**.

**Decidable now:** Correct scalar scope and variance of d can be decided without fetching a source.

**Further evidence or judgment:** User should confirm intended prerequisite granularity and later source convention for commutative coefficients; no B-linear interpretation accepted.

**Compared existing targets, all stored variants retained:** `meaning.711d6a9a3f5a61ca.relative-de-rham-complex`; `meaning.7ca4fb934b2f076c.kahler-differentials`; `meaning.7ca4fb934b2f076c.r-derivation`.

**Historical candidate occurrence anchors:** `occ.2a3dca729eb03dce129c`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

## 03 Algebraic objects and component prerequisites

<a id="case-003"></a>
### Rank 3 — quotient ring R/I

Canonical candidate: `missing.50fc57153b93520a247a`. Historical `canonical-review.2026-10-24.003`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** A commutative unital ring, ideal I; quotient A/I with induced operations. Formal-smoothness parent additionally has R→A, I²=0, quotient arrow q and lifting maps.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.1be2fa074ef447b0.i-adic-ring-completion`](CONTEXTS.md#context-014): For a commutative ring R and ideal I, its I-adic completion R^ is the inverse limit of the quotient rings R/I^n over positive integers n, with transition maps given by reduction modulo smaller powers.
- [`form.1fd51873f9f0afbd.field-from-irreducible-polynomial`](CONTEXTS.md#context-015): For a field k and irreducible polynomial f in k[x], the quotient k[x]/(f) is a field extending k, obtained by adjoining the class of x as a root of f.
- [`form.1fd51873f9f0afbd.prime-field-finite`](CONTEXTS.md#context-016): For a prime integer p, the finite prime field F_p is the quotient field Z/(p), whose elements are integer residue classes modulo p with operations inherited from integers.
- [`form.2cde0248ffe81c00.tor-flatness-criterion`](CONTEXTS.md#context-024): An R-module M is flat if and only if Tor_1^R(M,R/I)=0 for every finitely generated ideal I⊆R; equivalently, Tor_i^R(M,N)=0 for all R-modules N and every i>0.
- [`form.3f6cdddd076e5ca0.nagata-ring`](CONTEXTS.md#context-033): A commutative ring R is Nagata if it is Noetherian and R/p is Japanese (N-2) for each prime ideal p of R.
- [`form.44fae2299dfd2f0a.formally-unramified-map`](CONTEXTS.md#context-040): A ring homomorphism R→S is formally unramified if, for every R-algebra A and square-zero ideal I⊆A, any R-algebra map S→A/I admits at most one lift to an R-algebra map S→A.
- [`form.6676171d9e5698af.affine-closed-subscheme`](CONTEXTS.md#context-055): A closed subscheme of the affine scheme Spec(R) is a scheme isomorphic over Spec(R) to Spec(R/I) for some ideal I⊆R, equipped with the closed immersion induced by the quotient map R→R/I.
- [`form.8a5f1888f076f50d.formally-etale-ring-map`](CONTEXTS.md#context-075): A ring map R→S is formally étale if for every R-algebra A and ideal I⊆A with I²=0, every R-algebra map S→A/I lifts to exactly one R-algebra map S→A.
- [`form.8dbafc093b30c2a3.global-complete-intersection-algebra`](CONTEXTS.md#context-079): A finite-type algebra S over a field k is a global complete intersection if some presentation S≅k[x_1,…,x_n]/(f_1,…,f_c) satisfies dim(S)=n−c.
- [`form.a38f1da0bc017afe.noetherian-i-adic-completion`](CONTEXTS.md#context-089): For a Noetherian commutative ring R and ideal I, the I-adic completion R^ is the inverse-limit ring lim_n R/I^n, with structure homomorphism R→R^ induced by the quotient maps.
- [`form.aacbc297769cc94a.formally-smooth-ring-map`](CONTEXTS.md#context-096): A commutative ring homomorphism R→S is formally smooth if every R-algebra map S→A/I lifts to an R-algebra map S→A whenever A is an R-algebra and I⊆A satisfies I²=0.
- [`form.c50e4715a45d9236.relative-global-complete-intersection`](CONTEXTS.md#context-106): A ring map R→S is a relative global complete intersection if S admits a presentation R[x_1,…,x_n]/(f_1,…,f_c) for which every nonempty fibre of Spec(S)→Spec(R) has dimension n−c.
- [`form.d2b85c43cfbc6c05.finite-presentation-ring-map`](CONTEXTS.md#context-112): A ring map R→S is of finite presentation if S is R-isomorphic to R[x_1,…,x_n]/(f_1,…,f_m) for finite families of polynomial generators and relations.
- [`form.e39c701ba05418fb.formal-smoothness-field-extension`](CONTEXTS.md#context-119): A field extension K/k is formally smooth over k when every k-algebra map K→A/I across a square-zero quotient lifts to A. In positive characteristic this is equivalent to separability of K/k; in characteristic zero every field extension satisfies it.
- [`form.f3d1c8c59cda279e.complete-local-ring`](CONTEXTS.md#context-128): A local ring (R,m) is complete if the canonical homomorphism R→lim_n R/m^n is an isomorphism; equivalently, its m-adic completion introduces no new elements.
- [`form.wave2.foundation.local-ring-fibre-at-prime`](CONTEXTS.md#context-164): Let R→S be a homomorphism of commutative rings. For a prime ideal q⊆S with contraction p=q∩R, the local ring of the fibre at q is S_q/pS_q. Equivalently, it is the localization of the fibre ring S⊗_Rκ(p) at the prime corresponding to q.

**Mathematical argument:** Changing representatives changes products by elements of I, so the quotient ring prerequisite is legitimate in all 16 parents. But k[ε]/(ε²)→k and k→k have the same target quotient k with different square-zero kernels. The extension datum is not recoverable from the target ring. Z/4 is a quotient ring without being a field. Thus neither the existing irreducible-polynomial field nor a module quotient identifies the generic ring construction or whole extension.

**Interpretations:**

- underlying quotient: Justified common prerequisite.

- whole extension equals quotient: Rejected; source-specific map, action and kernel are extra data.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** The component relation is defensible; whole-object equivalence is false.

**Further evidence or judgment:** Adjudicate whether prerequisite-only historical alias rationales suffice or explicit occurrence segmentation is required; preserve all 16 hypotheses.

**Compared existing targets, all stored variants retained:** `meaning.1fd51873f9f0afbd.field-from-irreducible-polynomial`; `meaning.70f44988651b76b5.ring-localization-at-multiplicative-set`; `meaning.wave2.quot119.quotient-group`; `meaning.wave2.set63.set-of-equivalence-classes`.

**Historical candidate occurrence anchors:** `occ.2c5cacbc9d3860bb753e`, `occ.57ae070de7ce8a63fba7`, `occ.7a4955efd8491df01c30`, `occ.1ccc1447911cc48498ed`, `occ.32a4e0fbf677311cfa24`, `occ.f585c5feabcb062d11de`, `occ.87dd540c2994aa2f0859`, `occ.87b9becb9f6c94643c0f`, `occ.075fba056157644b27f2`, `occ.fe395fbd598e8f849a52`, `occ.39767a08c003da7e344c`, `occ.d0a2518401b81c11869a`, `occ.b75e8e0c5256fbc42b32`, `occ.3c5fc86c6a360ec62604`, `occ.125e77739bdab976cb85`, `occ.d2d4e2195a4c9ef69ac0`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-005"></a>
### Rank 5 — polynomial ring R[x_1,…,x_n]

Canonical candidate: `missing.9db64b2f9cdb8258e3d8`. Historical `canonical-review.2026-10-24.005`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Formal polynomial algebra over commutative unital coefficients, arbitrary set-indexed variables with finite monomial support. Evaluation at x∈S has different domain/codomain.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.0c4c23579959165d.algebraic-independence`](CONTEXTS.md#context-008): A family (x_i) of elements of a field extension K/k is algebraically independent over k when the evaluation homomorphism k[X_i:i∈I]→K, sending each indeterminate X_i to x_i, is injective.
- [`form.138b13bf27c037c1.naive-cotangent-complex`](CONTEXTS.md#context-010): For a ring map R→S, let P=R[X_s:s∈S] map canonically onto S and put I=ker(P→S). The naive cotangent complex NL_{S/R} is the two-term complex I/I²→Ω_{P/R}⊗_P S, with I/I² in homological degree 1 and the induced differential from universal derivation.
- [`form.30083611f9483a64.characteristic-polynomial-matrix`](CONTEXTS.md#context-026): The characteristic polynomial of an n×n matrix A over a commutative ring R is the polynomial χ_A(t)=det(t I_n−A) in R[t], where I_n denotes the identity matrix.
- [`form.50d335de00e5f11d.algebraic-extension`](CONTEXTS.md#context-046): An extension K/k of fields is algebraic if every element α∈K satisfies a nonzero polynomial with coefficients in k.
- [`form.82307b7a25fdc9fd.quasiregular-sequence-module`](CONTEXTS.md#context-071): For an R-module M and elements f_1,…,f_c generating J⊆R, the sequence is M-quasi-regular if the graded map (M/JM)⊗_{R/J}(R/J)[X_1,…,X_c]→⊕_{n≥0}J^nM/J^{n+1}M, sending X_i to the class of f_i, is an isomorphism.
- [`form.8dbafc093b30c2a3.global-complete-intersection-algebra`](CONTEXTS.md#context-079): A finite-type algebra S over a field k is a global complete intersection if some presentation S≅k[x_1,…,x_n]/(f_1,…,f_c) satisfies dim(S)=n−c.
- [`form.c50e4715a45d9236.relative-global-complete-intersection`](CONTEXTS.md#context-106): A ring map R→S is a relative global complete intersection if S admits a presentation R[x_1,…,x_n]/(f_1,…,f_c) for which every nonempty fibre of Spec(S)→Spec(R) has dimension n−c.
- [`form.d0a078e59e1495da.algebraic-element-extension`](CONTEXTS.md#context-110): An element α of a field extension E/F is algebraic over F if some nonzero polynomial f∈F[x] satisfies f(α)=0.
- [`form.d0a078e59e1495da.algebraic-field-extension`](CONTEXTS.md#context-111): A field extension E/F is algebraic if every element of E satisfies at least one nonzero polynomial with coefficients in F.
- [`form.d2b85c43cfbc6c05.finite-presentation-ring-map`](CONTEXTS.md#context-112): A ring map R→S is of finite presentation if S is R-isomorphic to R[x_1,…,x_n]/(f_1,…,f_m) for finite families of polynomial generators and relations.
- [`form.d2b85c43cfbc6c05.finite-type-ring-map`](CONTEXTS.md#context-113): A ring map R→S is of finite type if S can be generated as an R-algebra by finitely many elements, equivalently S is a quotient of R[x_1,…,x_n] for some finite n.
- [`form.e606496d592fe305.relatively-prime-polynomials`](CONTEXTS.md#context-120): Polynomials f,g∈k[x] over a field k are relatively prime when the ideal (f,g) they generate is the entire polynomial ring k[x].
- [`form.wave2.foundation.nonzero-polynomial-degree`](CONTEXTS.md#context-167): Let R be a commutative ring with multiplicative identity and let P=∑_{k=0}^n a_kX^k∈R[X] be nonzero. Its degree deg(P) is the greatest integer k≥0 for which a_k≠0_R. This definition does not assign a finite degree to the zero polynomial.
- [`form.wave2.foundation.strongly-transcendental-subring-element`](CONTEXTS.md#context-174): Let R⊆S be an inclusion of commutative rings with identity, and let x∈S. The element x is strongly transcendental over R if for every integer n≥0, coefficients a_0,…,a_n∈R, and u∈S, the equation u(a_0+a_1x+⋯+a_nx^n)=0 implies ua_i=0 for every i=0,…,n.

**Mathematical argument:** T≠0 in R[T] for nonzero R although ev_0(T)=ev_0(0). Finite support of each polynomial does not make the entire variable set finite, especially P=R[X_s:s∈S]. The strong-transcendence source uses P(x), an element of S, whereas formal P(T) is in R[T]. Under common identity and the defining strong-transcendence condition, u=1 implies injective evaluation; even then ring, polynomial and image value are different typed data. The characteristic-polynomial source also needs the identity matrix, so its broad-ring seed cannot certify nonunital scope.

**Interpretations:**

- polynomial algebra prerequisite: Valid shared operation.

- algebra expression evaluation value: Not one mathematical object even when evaluation happens to be injective.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** Formal/value distinction and arbitrary-index scope are clear.

**Further evidence or judgment:** Clarify prerequisite-only alias semantics at the strong-transcendence occurrence; verify identity convention separately. No narrowing to finitely many variables.

**Compared existing targets, all stored variants retained:** `meaning.50d335de00e5f11d.algebraic-extension`; `meaning.d0a078e59e1495da.algebraic-element-extension`; `meaning.d2b85c43cfbc6c05.finite-type-ring-map`; `meaning.wave2.foundation.nonzero-polynomial-degree`.

**Historical candidate occurrence anchors:** `occ.7baaa7f00bd06670e1a2`, `occ.cde28c9026dd9ebf3bf1`, `occ.cc2d8d837c94d986dc3b`, `occ.8a610b801f1afe26a528`, `occ.52511e9d622c088f8b18`, `occ.721c15f7de0ceaaa4efa`, `occ.555f92d6a5311adc5e37`, `occ.08596e566fe3ee29f4b4`, `occ.fec879f2b5b6da83067b`, `occ.9723973c6978063662cf`, `occ.50749c0d1402386c1b51`, `occ.4698890269e07848615d`, `occ.52659d4daedd3f18cae8`, `occ.aa7d5dd9a4e322c869e6`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-040"></a>
### Rank 40 — roots of a polynomial in a field

Canonical candidate: `missing.fa5932b42daa1a3e0307`. Historical `canonical-review.2026-10-24.042`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Root α in a specified extension field with f(α)=0. The actual quotient-field parent requires irreducible f; canonical example only says nonconstant.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.1fd51873f9f0afbd.field-from-irreducible-polynomial`](CONTEXTS.md#context-015): For a field k and irreducible polynomial f in k[x], the quotient k[x]/(f) is a field extending k, obtained by adjoining the class of x as a root of f.
- [`form.39488f3e396a1c77.algebraically-closed`](CONTEXTS.md#context-030): A field K is algebraically closed precisely when it has no proper algebraic field extension; equivalently, each nonconstant one-variable polynomial with coefficients in K admits a root in K.
- [`form.471f985f2fbe7b49.splitting-field`](CONTEXTS.md#context-041): For a nonconstant polynomial P over a field F, a splitting field is a field extension E/F in which P factors into linear terms and which is generated over F by all its roots.
- [`form.720eaae9156f6f4e.separable-degree-polynomial`](CONTEXTS.md#context-064): The separable degree of an irreducible polynomial f over F is the number of its distinct roots in an algebraic closure of F, counted without multiplicities.

**Mathematical argument:** For a field F, F[T]/(T²) contains nonzero nilpotent class T and is not a field. Its T-class solves the equation, but does not establish the canonical description as a field extension. The actual irreducible-polynomial source has the missing hypothesis and is not shown erroneous. A root is an element, not its evaluation map, root count, splitting field or root of unity; zero is a root of T and not a root of unity.

**Interpretations:**

- generic field root: Valid prerequisite for the four parents.

- arbitrary nonconstant quotient is field: False without irreducibility.

**Recommended disposition:** convention clarification — **not applied**.

**Decidable now:** The qualification error in the candidate example is mathematically demonstrable.

**Further evidence or judgment:** Approve an eventual qualification of the candidate example, not a correction to the already-qualified parent. No edit applied.

**Compared existing targets, all stored variants retained:** `meaning.1fd51873f9f0afbd.field-from-irreducible-polynomial`; `meaning.e0849711d61cd26f.nth-root-of-unity`.

**Historical candidate occurrence anchors:** `occ.29b820e470569d95f584`, `occ.9f3dda1841b64dd9f533`, `occ.4f0a00da35a6a75dc313`, `occ.5e8b4356a3bb977ed5c0`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-250"></a>
### Rank 250 — n prime to characteristic

Canonical candidate: `missing.659b5d5ed37a38428987`. Historical `canonical-review.2026-10-24.255`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Kummer n≥2, field K, nth roots of unity in K. Intended scalar n·1_K invertible; characteristic p>0 or 0.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.b3aefc22ee361c53.kummer-extension`](CONTEXTS.md#context-099): In the Kummer setting, an extension L/K is obtained by adjoining an element α satisfying α^n=a∈K, where n≥2 is prime to char(K) and K contains the nth roots of unity; when [L:K] is finite, L/K is a cyclic Galois extension of degree dividing n.

**Mathematical argument:** If char K=p>0, invertibility is equivalent to p∤n. In characteristic zero every positive n is invertible in K, whereas gcd(n,0)=n would exclude n≥2. Thus literal integer coprimality at zero is the wrong reading. This condition says nothing about n itself being prime. If a=0 then T^n has a repeated root even when p∤n, so separability of that polynomial cannot be inferred without a≠0; the full parent extension statement is not globally certified here.

**Interpretations:**

- n invertible in K: Correct field-theoretic reading of candidate qualifiers.

- literal gcd in char zero: Rejected.

**Recommended disposition:** convention clarification — **not applied**.

**Decidable now:** The arithmetic interpretation and its limitation at a=0 are settled.

**Further evidence or judgment:** Use explicit invertibility wording in a later authorized record; retain the parent hypotheses and do not certify every Kummer formulation by this local review.

**Compared existing targets, all stored variants retained:** `meaning.b3aefc22ee361c53.kummer-extension`; `meaning.dbce785fa0c96b0a.field-characteristic`; `meaning.wave2.foundation.field-commutative-unital`.

**Historical candidate occurrence anchors:** `occ.9dba5fb8c426cc4e73a3`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-268"></a>
### Rank 268 — presentation S≅R[x_1,…,x_n]/(f_1,…,f_m)

Canonical candidate: `missing.76cef49793a8851de7db`. Historical `canonical-review.2026-10-24.273`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Finite lists of variables and relations plus an R-algebra isomorphism R[X]/(f)→S. Finite presentability quantifies existence of such data.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.415a1503ae7ed97d.finitely-presented-algebra`](CONTEXTS.md#context-036): An R-algebra S is finitely presented if it admits a presentation S≅R[x_1,…,x_n]/(f_1,…,f_m) with finitely many generators x_i and finitely many polynomial relations f_j.

**Mathematical argument:** R has a presentation with no variables and another as R[T]/(T), demonstrating that chosen presentation is not the mere property. A polynomial algebra or quotient alone omits the relations and chosen isomorphism; an abstract ring isomorphism may omit scalar compatibility. Zero variables and an empty relation list should not be excluded without source evidence.

**Interpretations:**

- chosen presentation: Compound datum; preserve maps and finite lists.

- finite presentability: Existential property, not the selected data.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** Chosen data versus existence is a real distinction.

**Further evidence or judgment:** Choose whether later identity modeling isolates constituent constructions or keeps a typed presentation datum. No self-resolution to the parent property.

**Compared existing targets, all stored variants retained:** `meaning.415a1503ae7ed97d.finitely-presented-algebra`; `meaning.d2b85c43cfbc6c05.finite-presentation-ring-map`.

**Historical candidate occurrence anchors:** `occ.cd654a2d09261d8a5f1d`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-294"></a>
### Rank 294 — quotient ring R/J and quotient module M/JM

Canonical candidate: `missing.8d90dbc484b53274e726`. Historical `canonical-review.2026-10-24.299`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** R/J a ring, M/JM an R/J-module, graded quasi-regular comparison additionally uses polynomial algebra and ideal powers.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.82307b7a25fdc9fd.quasiregular-sequence-module`](CONTEXTS.md#context-071): For an R-module M and elements f_1,…,f_c generating J⊆R, the sequence is M-quasi-regular if the graded map (M/JM)⊗_{R/J}(R/J)[X_1,…,X_c]→⊕_{n≥0}J^nM/J^{n+1}M, sending X_i to the class of f_i, is an isomorphism.

**Mathematical argument:** The scalar action (r+J)(m+JM)=rm+JM is well-defined since J kills the quotient. With M=R² and J=0 the quotient module has no specified multiplication, so it is not the ring quotient as a structured object. Separating components must retain ideal action JM, both quotient constructions and the induced scalar structure, rather than deleting an apparently redundant dependency.

**Interpretations:**

- ring and module quotients: Both legitimate prerequisite components.

- single quotient identity: Not an identity of the entire compound phrase.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** The two object types and descent of scalar action are proved.

**Further evidence or judgment:** Adjudicate compound granularity and any later segmentation without losing links or inventing a new meaning now.

**Compared existing targets, all stored variants retained:** `meaning.82307b7a25fdc9fd.quasiregular-sequence-module`.

**Historical candidate occurrence anchors:** `occ.9028c4bc4186bfc8f868`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-298"></a>
### Rank 298 — zero-divisor phenomena in S

Canonical candidate: `missing.8f2dea7e2bd1211c0cf6`. Historical `canonical-review.2026-10-24.303`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Strong-transcendence implication allows arbitrary u∈S, including 0. Candidate zero divisor requires a nonzero element; existing predicate only requires a nonzero annihilator.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.wave2.foundation.strongly-transcendental-subring-element`](CONTEXTS.md#context-174): Let R⊆S be an inclusion of commutative rings with identity, and let x∈S. The element x is strongly transcendental over R if for every integer n≥0, coefficients a_0,…,a_n∈R, and u∈S, the equation u(a_0+a_1x+⋯+a_nx^n)=0 implies ua_i=0 for every i=0,…,n.

**Mathematical argument:** In a nonzero ring the existing annihilator-based predicate includes 0, since 0·s=0 for nonzero s; the canonical candidate excludes it. Moreover uP(x)=0 need not exhibit nonzero factors: u=0 always satisfies it. The scan phrase zero-divisor phenomena is explanatory and not a literal source definition, so the displayed formula does not select either named convention or prove that a separate zero-divisor prerequisite is necessary.

**Interpretations:**

- nonzero zero divisor: Distinct from the stored zero-inclusive predicate.

- explanatory annihilation warning: Possible source-local caution rather than named prerequisite.

**Recommended disposition:** genuine policy decision — **not applied**.

**Decidable now:** Nonidentity of the variants is proved; the formula does not force nonzero factors.

**Further evidence or judgment:** Decide named-prerequisite versus explanatory reference policy and zero inclusion, preserving the annihilator equation and historical evidence.

**Compared existing targets, all stored variants retained:** `meaning.559efcb6f15ddc96.zerodivisor-of-ring`; `meaning.wave2.foundation.strongly-transcendental-subring-element`.

**Historical candidate occurrence anchors:** `occ.6414b479b47d231c54a8`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

## 04 Ringed-space conventions

<a id="case-202"></a>
### Rank 202 — sheaf of rings O_X

Canonical candidate: `missing.42dd118d20d40e57e2b9`. Historical `canonical-review.2026-10-24.206`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** O_X sheaf of rings on opens; candidate uses unital rings and restriction maps. Locally ringed parent additionally requires local stalks.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.52683cac2ccf3bad.locally-ringed-space`](CONTEXTS.md#context-048): A locally ringed space is a topological space X together with a sheaf of rings O_X whose stalk at every point of X is a local ring.

**Mathematical argument:** A one-point space with ring of sections Z is a ringed space but not locally ringed, because its sole stalk Z has distinct maximal ideals (2),(3). Stalk, section ring and whole sheaf are different objects. Sheaf gluing supplies neither a source convention on identities nor localness by itself. The two existing local-ring formulations leave the already-recorded unit question to source reconciliation.

**Interpretations:**

- unital ring sheaf: Candidate scoped type.

- locally ringed space: Adds local stalks, not a generic sheaf resolution.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** Sheaf, stalk, section ring and local-stalk restriction are separated.

**Further evidence or judgment:** Verify ring-sheaf unit/restriction conventions together with local-ring conventions; do not infer them from provider attribution.

**Compared existing targets, all stored variants retained:** `meaning.52683cac2ccf3bad.locally-ringed-space`.

**Historical candidate occurrence anchors:** `occ.fb409fc3e895f8b17b77`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-222"></a>
### Rank 222 — quotient sheaf O_X/I and direct image under inclusion

Canonical candidate: `missing.4fff53dd962546ca64ba`. Historical `canonical-review.2026-10-24.226`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** I ideal subsheaf on locally ringed X, quotient sheaf O_X/I, support inclusion i:Z↪X and comparison i_*O_Z≅O_X/I.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.8f376cdea16a26da.closed-subspace-from-ideal-sheaf`](CONTEXTS.md#context-081): Given a locally ringed space X and a locally section-generated sheaf of ideals I⊆O_X, the associated closed subspace is the support Z of O_X/I with the quotient structure sheaf O_Z whose direct image under Z↪X equals O_X/I.

**Mathematical argument:** A ring-sheaf quotient has stalks O_x/I_x; a sectionwise quotient presheaf can require sheafification. Pushforward is an operation between spaces, (i_*F)(U)=F(i^{-1}U), not quotienting one ring. The support, quotient sheaf, sheaf on Z and comparison are different typed ingredients. A single generic ring quotient cannot encode this entire package; local-generation requirements must not be silently strengthened to finite generation or quasi-coherence.

**Interpretations:**

- quotient sheaf and pushforward: Legitimate distinct components.

- one ring or entire closed subspace: Not an equivalent replacement for the compound datum.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** The constructions and their spaces are clear; sectionwise quotient is not a general shortcut.

**Further evidence or judgment:** Adjudicate segmentation while retaining comparison map and local-generation quantifiers; verify sheaf/local-ring conventions later.

**Compared existing targets, all stored variants retained:** `meaning.8f376cdea16a26da.closed-subspace-from-ideal-sheaf`.

**Historical candidate occurrence anchors:** `occ.678bfa1765e66f84cf84`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-323"></a>
### Rank 323 — maximal ideal mR^h and residue field R/m

Canonical candidate: `missing.a115a0258bce647cea2b`. Historical `canonical-review.2026-10-24.328`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Local R-map R→R^h, target maximal ideal mR^h and induced residue isomorphism R/m→R^h/mR^h; henselian and initial/colimit clauses are additional.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.a87b0cc83bb541e4.henselization-local-ring`](CONTEXTS.md#context-094): For a local ring (R,m), its henselization R^h is a Henselian local R-algebra initial among local R-homomorphisms from R into Henselian local rings, with maximal ideal mR^h and residue field canonically R/m; it may be constructed as a filtered colimit of suitable étale R-algebras.

**Mathematical argument:** The local map k→k[t]_(t) induces residue isomorphism k→k, but 0·k[t]_(t)=0 is not its maximal ideal (t). Thus localness plus residue isomorphism does not imply the extension-ideal equality. A residue field alone cannot represent this datum or the whole henselization universal object. The exact source-selected maps and residue identification must survive any decomposition.

**Interpretations:**

- local map ideal and residue data: Compound component package.

- residue field or generic local map: Insufficient by counterexample.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** The three conditions are not redundant under generic local-map hypotheses.

**Further evidence or judgment:** Choose granularity while retaining all conditions; later verify local-ring/unit and universal-property source conventions. No henselization self-resolution.

**Compared existing targets, all stored variants retained:** `meaning.a87b0cc83bb541e4.henselization-local-ring`.

**Historical candidate occurrence anchors:** `occ.e0ee42722fb119a46552`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

## 05 Category-theoretic assumptions

<a id="case-062"></a>
### Rank 62 — natural transformation a:F→G

Canonical candidate: `missing.a8c70a2a13320680c54c`. Historical `canonical-review.2026-10-24.064`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Set-valued presheaves on C, η:F⇒G with components functions and contravariant naturality. Yoneda instance has h_U(X)=Hom_C(X,U).

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.a570f5bed277bd8b.presheaf-fibre-product`](CONTEXTS.md#context-091): For natural transformations F→G and H→G of set-valued presheaves on C, their fibre product is the presheaf sending X to the set-theoretic fibre product F(X)×_{G(X)}H(X), with restriction maps inherited componentwise.
- [`form.a570f5bed277bd8b.representable-presheaf-morphism`](CONTEXTS.md#context-092): For presheaves F,G:C^op→Sets, a natural transformation a:F→G is representable when for every object U in C and element ξ∈G(U), the fibre-product presheaf h_U×_G F formed using ξ:h_U→G is representable.

**Mathematical argument:** For ξ∈G(U), define η_X(h)=G(h)(ξ); composition proves naturality. Conversely η_U(id_U) recovers ξ and naturality recovers all components. This constructs the Yoneda correspondence, a whole bijection involving an element and a family, not the definition of an arbitrary natural transformation. Components need not be bijective. Set-valued represented presheaves require the relevant Hom collections to be sets in an adopted universe, connecting rank 393.

**Interpretations:**

- natural transformation: Valid prerequisite component.

- whole Yoneda bijection: More data/proposition than one arbitrary transformation.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** The formula and nonidentity of whole correspondence with a component are established.

**Further evidence or judgment:** Clarify prerequisite-only alias at the exact Yoneda occurrence and source size conventions; no automatic natural-isomorphism alias.

**Compared existing targets, all stored variants retained:** `meaning.a570f5bed277bd8b.presheaf-fibre-product`; `meaning.a570f5bed277bd8b.representable-presheaf-morphism`; `meaning.fef4e69e96c25bfa.contravariant-functor`.

**Historical candidate occurrence anchors:** `occ.fec3a03198f7fee73ecf`, `occ.294c2ee49c6e374c14f7`, `occ.099ea4270d9cbdccf52b`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-393"></a>
### Rank 393 — bijections between the morphisms L(X) to Y in D and X to R(Y) in C

Canonical candidate: `missing.e834133a2cdc7390f1de`. Historical `canonical-review.2026-10-24.399`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** L:C→D, R:D→C; Hom_D(LX,Y)≅Hom_C(X,RY), contravariant X and covariant Y, natural in both. Candidate additionally describes sets.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.5b6d4a7f88629b12.left-adjoint`](CONTEXTS.md#context-052): For functors L:C to D and R:D to C, L is left adjoint to R when there are bijections between the morphisms L(X) to Y in D and X to R(Y) in C, natural in both X and Y.

**Mathematical argument:** Bijections are between morphism collections, not LX and RY, which live in different categories. Equal cardinalities alone do not choose a natural family. Smallness of the collection of all objects is stronger than local-smallness; a discrete category with a proper class of objects still has empty or singleton Hom collections. Conversely the bare source does not specify any universe or local-smallness rule. Thus neither a small-category restriction nor a Set-valued Hom convention may be inferred merely from the word category.

**Interpretations:**

- locally small or fixed universe: Set-valued Hom interpretation is meaningful.

- arbitrary categories: Set-valued Hom is additional scope, requiring convention verification.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** Arrow types, variance and naturality requirement are settled.

**Further evidence or judgment:** Later verify local-smallness/universe or class-valued adjunction convention. User policy must not silently replace all categories with small ones.

**Compared existing targets, all stored variants retained:** `meaning.5b6d4a7f88629b12.left-adjoint`.

**Historical candidate occurrence anchors:** `occ.cdce74c80bf00e7432d2`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-420"></a>
### Rank 420 — multiplication map S⊗_R S→S is ring isomorphism

Canonical candidate: `missing.fe199606757d4b449fee`. Historical `canonical-review.2026-10-24.426`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Category of commutative unital rings, unital f:R→S. μ:S⊗_R S→S, s⊗t↦st, is a ring map; categorical epi is right-cancellation.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.988d26ef7c849694.epimorphism-commutative-rings`](CONTEXTS.md#context-087): A ring homomorphism f:R→S is an epimorphism in the category of commutative rings if every pair of ring maps g,h:S→T satisfying g∘f=h∘f are equal; equivalently the multiplication map S⊗_R S→S is an isomorphism.

**Mathematical argument:** If f is epi, the two maps i1,i2:S→S⊗_R S agree on R and hence agree. Then s⊗t=i1(s)i2(t)=i1(st), so μ and i1 are inverse. Conversely μ invertible gives i1=i2; for g,h:S→T agreeing on R, commutativity gives the balanced map s⊗t↦g(s)h(t), forcing g=h. Z→Q is epi but not surjective: images of fractions are uniquely determined by images of integers and inverses. The proof does not establish the same tensor criterion in arbitrary noncommutative ring categories.

**Interpretations:**

- canonical multiplication map: Valid typed component.

- its invertibility: Equivalent epi criterion under the commutative category; not an arbitrary ring isomorphism.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** The stated equivalence and distinction from surjectivity can be proved.

**Further evidence or judgment:** Choose whether the candidate represents a map or its predicate; retain commutative/unital category and do not resolve it to the whole parent.

**Compared existing targets, all stored variants retained:** `meaning.74e36635b2776fe8.tensor-product-modules`; `meaning.988d26ef7c849694.epimorphism-commutative-rings`; `meaning.eed0c34725956bb5.categorical-epimorphism`.

**Historical candidate occurrence anchors:** `occ.f0134a4982504bbae736`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

## 06 Topology and local versus global predicates

<a id="case-038"></a>
### Rank 38 — simultaneously open and closed

Canonical candidate: `missing.b599bdc9343a25050226`. Historical `canonical-review.2026-10-24.040`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Clopen U in an arbitrary X versus canonical context U⊆Spec(R). Connected meanings include both empty-allowed and nonempty conventions.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.097db25e2f156689.clopen-subset-of-spectrum`](CONTEXTS.md#context-007): For a commutative ring R, a subset U of Spec(R) is simultaneously open and closed exactly when there is an idempotent e of R (so e²=e) such that U=D(e)={p in Spec(R):e is not in p}; this e is unique.
- [`form.ab260940ea9c523d.connected-topological-space`](CONTEXTS.md#context-097): A nonempty topological space X is connected if it cannot be expressed as a disjoint union of two nonempty open subsets; equivalently its only clopen subsets are ∅ and X.
- [`form.wave2.pop141.connected-clopen`](CONTEXTS.md#context-199): A topological space (X,τ) is connected if every subset C⊆X that is both open and closed in X satisfies C=∅ or C=X.
- [`form.wave2.variant71.connected.02`](CONTEXTS.md#context-218): A topological space X is connected precisely when its only subsets that are both open and closed are ∅ and X.

**Mathematical argument:** U is clopen iff U and X\U are open. A nontrivial clopen gives a separation and conversely, including the vacuous empty-allowed case. This does not impose nonemptiness on X. In Spec(R), idempotents give D(e)=V(1−e), but a general space has no chosen ring/idempotent datum. Generic clopen is a valid shared predicate; its specialization to a spectrum is not the whole idempotent correspondence and does not turn every X into a spectrum.

**Interpretations:**

- generic clopen: Justified shared prerequisite.

- spectrum with idempotent: Specialized context plus additional algebraic correspondence.

**Recommended disposition:** valid specialization — **not applied**.

**Decidable now:** The shared topological predicate and separation equivalence are established.

**Further evidence or judgment:** Adjudicate canonical ambient scope versus polymorphic prerequisite modeling; preserve all connectedness conventions and sources.

**Compared existing targets, all stored variants retained:** `meaning.097db25e2f156689.clopen-subset-of-spectrum`; `meaning.ab260940ea9c523d.connected-topological-space`; `meaning.wave2.foundation.topological-space`.

**Historical candidate occurrence anchors:** `occ.982109ad4faf2e20b72d`, `occ.417c86f577e85affc4cb`, `occ.00775f87f3c5601a0719`, `occ.1612dec2b099f44c923b`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-399"></a>
### Rank 399 — fundamental system of connected neighborhoods

Canonical candidate: `missing.eb8e1a62d06acf7c487c`. Historical `canonical-review.2026-10-24.405`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** At each x, connected neighborhoods cofinal in all neighborhoods; individual members not necessarily open. Global topology basis consists of open sets.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.ab260940ea9c523d.locally-connected-space`](CONTEXTS.md#context-098): A topological space X is locally connected if each point x possesses a fundamental system of connected neighbourhoods.

**Mathematical argument:** Fix open U and a connected component C of U. For each x∈C, choose connected neighborhood V_x⊆U; since it meets C it lies in C and contains an open neighborhood of x. Hence C is open. Such components give a connected-open basis. This derived characterization does not identify an arbitrary selected pointwise system with a global open basis. The offending historical global-basis occurrence was corrected by a receipt-verified amendment; the pointwise candidate remains missing and is not an unapplied repeat correction.

**Interpretations:**

- pointwise connected system: Valid remaining prerequisite.

- derived global basis: Equivalent space property under all-point quantification, not identity of the systems.

**Recommended disposition:** preserve distinct — **not applied**.

**Decidable now:** The theorem and distinction of data are proved; old target warning is superseded.

**Further evidence or judgment:** No repeat amendment requested. User may later document a derived characterization; keep the unresolved pointwise type separate from global basis.

**Compared existing targets, all stored variants retained:** `meaning.6a3376e5ecb82bfb.topology-basis`; `meaning.ab260940ea9c523d.connected-topological-space`; `meaning.ab260940ea9c523d.locally-connected-space`.

**Historical candidate occurrence anchors:** `occ.466d90b0de4bc627c881`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

The missing occurrence `occ.466d90b0de4bc627c881` remains. Historical wrong-target `occ.cdc96f16a3e31332ec7d` is superseded by external occurrence `occ.37c025a95505dc305dad`; do not resubmit it.

## 07 Measure and indexing conventions

<a id="case-036"></a>
### Rank 36 — integrability E|X_t|<infinity

Canonical candidate: `missing.826fb5c503bdaf25ce7f`. Historical `canonical-review.2026-10-24.038`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Finite absolute expectation of a real random variable on one probability space; four parents quantify two individual variables, integer sequences, or all real t≥0.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.wave2.found85.conditional-expectation`](CONTEXTS.md#context-154): For an integrable real random variable X on (Ω,F,P) and a sub-σ-algebra G⊆F, a version of E[X|G] is an integrable G-measurable random variable Z satisfying ∫_A Z dP = ∫_A X dP for every A∈G.
- [`form.wave2.research81.martingale-continuous-index.01`](CONTEXTS.md#context-211): A real-valued process (X_t)_{t≥0} adapted to a filtration (F_t)_{t≥0}, with E|X_t|<∞ for every t≥0, is a martingale if E[X_t|F_s]=X_s almost surely whenever 0≤s≤t.
- [`form.wave2.research81.martingale-discrete.01`](CONTEXTS.md#context-212): A real-valued discrete-time process (X_n)_{n≥0}, adapted to a filtration (F_n)_{n≥0} and satisfying E|X_n|<∞ for every n, is a martingale if E[X_{n+1}|F_n]=X_n almost surely for each n≥0.
- [`form.wave2.research81.martingale-discrete.02`](CONTEXTS.md#context-213): An integrable adapted real-valued discrete-time process (X_n,F_n)_{n≥0} is a martingale if E[X_m|F_n]=X_n almost surely whenever 0≤n≤m are integers.

**Mathematical argument:** On N_{>0} with P{k}=2^{-k}, Z(k)=2^k is measurable but E|Z|=∞. Set X_t=0 at integer times and Z otherwise: integer-time integrability does not imply all-real-time integrability. Deterministic X_n=n also shows pointwise finiteness is not a uniform expectation bound. The real-time filtration correction fixes a distinct reference and does not settle this integrability candidate quantifier scope.

**Interpretations:**

- single variable L1: Legitimate common predicate instantiated at each source variable.

- all real time process condition: Strictly different quantified statement from integer or individual cases.

**Recommended disposition:** convention clarification — **not applied**.

**Decidable now:** The local predicate is shared, but whole quantified requirements are not equivalent.

**Further evidence or judgment:** Adjudicate generic L1 prerequisite versus indexed requirement in the canonical context; preserve each parent index set. No source edit or quantifier weakening.

**Compared existing targets, all stored variants retained:** `meaning.wave2.found85.conditional-expectation`; `meaning.wave2.foundation.tagged-riemann-integral`; `meaning.wave2.prob90.random-variable-real`.

**Historical candidate occurrence anchors:** `occ.3eda46790ce1c2aed5c5`, `occ.2cf87f7b73f5c5a33bb4`, `occ.b8df608b462159d8948d`, `occ.98619b3d2a58ee9006e9`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-166"></a>
### Rank 166 — Lebesgue–Stieltjes measure from nondecreasing function

Canonical candidate: `missing.2216f1dfe187a7af152c`. Historical `canonical-review.2026-10-24.169`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** Nonnegative Borel/Stieltjes measure from bounded nondecreasing admissible α; source does not define admissible or endpoint normalization.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.wave2.analysis.orthogonal-polynomials-measure`](CONTEXTS.md#context-137): Let μ be a nonnegative Lebesgue–Stieltjes measure arising from an admissible bounded nondecreasing function with infinitely many points of increase and finite moments ∫|x|^k dμ(x)<∞ for all integers k≥0. A polynomial family p_n of degree n is orthogonal with respect to μ when ∫p_n(x)p_m(x)dμ(x)=0 for n≠m.

**Mathematical argument:** For right-continuous α the usual interval assignment is μ((a,b])=α(b)−α(a). If α(t)=0 for t≤0 and 1 for t>0, that raw assignment gives μ((0,1/n])=1 although these sets decrease to ∅, violating finite-measure continuity from above. Thus bare monotonicity cannot justify that interval formula. Atoms also exclude aliasing the construction with a density w(x)dx. A different one-sided normalization can be legitimate; no convention is selected here.

**Interpretations:**

- normalized Stieltjes construction: Requires an explicit sided/endpoint convention.

- bare monotone interval formula: Not valid in every sided convention.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** Need for a normalization and distinction from density measures are proved.

**Further evidence or judgment:** Later source verification must determine admissible, one-sided limits, endpoint atoms and integration domain. Current evidence cannot choose right versus left.

**Compared existing targets, all stored variants retained:** `meaning.wave2.analysis.orthogonal-polynomials-measure`; `meaning.wave2.foundation.nonnegative-measure`.

**Historical candidate occurrence anchors:** `occ.a948cb2f41a2dba805f9`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-291"></a>
### Rank 291 — Lebesgue–Stieltjes integral of x^n

Canonical candidate: `missing.8b4a695691c7d8e62f73`. Historical `canonical-review.2026-10-24.296`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Integrand x^n, n≥0, μ-integrability, interval (a,b) in the stored context, displayed ∫_a^b endpoint notation. Parent defines the nth raw moment.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.wave2.foundation.orthogonality-measure-raw-moment`](CONTEXTS.md#context-169): Let μ be a nonnegative Borel or Lebesgue–Stieltjes measure on a real interval (a,b) and let n be a nonnegative integer such that x↦x^n is μ-integrable. The nth raw moment of μ is μ_n=∫_a^b x^n dμ(x). It is finite only when the integral is finite.

**Mathematical argument:** For μ=δ_a and n=0, including a gives integral 1 and excluding it gives 0. Thus unspecified endpoints are material for atomic measures. Once μ, interval, n and integrability are fixed, ∫x^n dμ is exactly the raw-moment value already defined by the parent. Generic integration as an operation is a prerequisite, not an identity of every integral with this moment or with a Riemann construction.

**Interpretations:**

- generic Lebesgue integral: Reusable operation.

- specified raw moment value: Exactly the parent construction after parameters fixed; self-resolution risk.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** The specialization and possible endpoint discrepancy are concrete.

**Further evidence or judgment:** Adjudicate operation versus value granularity, and obtain endpoint convention through rank 166 source verification; no moment self-resolution.

**Compared existing targets, all stored variants retained:** `meaning.wave2.foundation.orthogonality-measure-raw-moment`; `meaning.wave2.foundation.tagged-riemann-integral`.

**Historical candidate occurrence anchors:** `occ.a0c3f77092abf2cd4daf`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-364"></a>
### Rank 364 — infinitely many points of increase

Canonical candidate: `missing.ca3087282d7220fbe8f5`. Historical `canonical-review.2026-10-24.370`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Bounded nondecreasing generator with infinitely many points of increase, plus all absolute moments finite; source does not define point of increase.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.wave2.analysis.orthogonal-polynomials-measure`](CONTEXTS.md#context-137): Let μ be a nonnegative Lebesgue–Stieltjes measure arising from an admissible bounded nondecreasing function with infinitely many points of increase and finite moments ∫|x|^k dμ(x)<∞ for all integers k≥0. A polynomial family p_n of degree n is orthogonal with respect to μ when ∫p_n(x)p_m(x)dμ(x)=0 for n≠m.

**Mathematical argument:** An atomic distribution with weights 2^{-n} at positive integers has infinitely many jumps but is constant between them; strict increase everywhere is therefore a different condition. If a measure is supported on finitely many a_i, the nonzero polynomial ∏(X−a_i) has zero L2 norm. This explains why infinite support is relevant to positive-norm orthogonal systems in unbounded degree, but does not establish which local/sided generator definition the source intends. Orthogonality alone in the short formulation must not be silently upgraded to a normalization theorem.

**Interpretations:**

- support nondegeneracy intent: Mathematically motivated conditional explanation.

- strict monotonicity or derivative positive: Not equivalent to infinitely many jumps or increase points.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** Finite-support degeneracy and failure of strict-increase interpretation are established.

**Further evidence or judgment:** Verify point-of-increase definition and its relation to normalized Stieltjes support; no derivative or normalization axiom invented.

**Compared existing targets, all stored variants retained:** `meaning.wave2.analysis.orthogonal-polynomials-measure`.

**Historical candidate occurrence anchors:** `occ.b8a1d1f5d00273fb043b`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

## 08 Compound constructions and self-reference

<a id="case-172"></a>
### Rank 172 — degree-zero subring

Canonical candidate: `missing.244d6cfceb0dd22abbca`. Historical `canonical-review.2026-10-24.175`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Positive grading, homogeneous f with deg f>0; S_f graded localization and its degree-zero part S_(f). Homogeneous numerator degree n deg f.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.29b2c34cc33d4b62.degree-zero-localization`](CONTEXTS.md#context-020): For a positively graded ring S and homogeneous element f of positive degree, S_(f) denotes the degree-zero subring of the graded localization S_f, consisting of fractions a/f^n with deg(a)=n·deg(f).

**Mathematical argument:** In S=k[x], f=x, S_f=k[x,x^{-1}] while (S_f)_0=k, so full localization is not its zero-degree subring. Degree-zero extraction is a reusable operation, but in the exact positive-degree setting it is already the defining construction of the existing S_(f) parent. A candidate with more general denominator or grading scope cannot be identified with that parent without qualification. Graded zero elements belong to all components, so degree notation must not assign them a unique degree accidentally.

**Interpretations:**

- degree zero extraction: Valid operation prerequisite.

- same specific S (f): Overlaps the parent definition and risks self-reference if resolved naively.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** Full localization versus degree-zero extraction and exact-specialization overlap are clear.

**Further evidence or judgment:** Decide whether to retain a generic operation or a more specific datum; preserve deg f>0 and no self-resolution.

**Compared existing targets, all stored variants retained:** `meaning.29b2c34cc33d4b62.degree-zero-localization`; `meaning.70f44988651b76b5.ring-localization-at-multiplicative-set`; `meaning.fa3b484c09596cfd.nonnegatively-graded-ring`.

**Historical candidate occurrence anchors:** `occ.e0d877766eb0e3095cab`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-223"></a>
### Rank 223 — abelian group presentation by direct sums

Canonical candidate: `missing.50540c0ba5822a8df022`. Historical `canonical-review.2026-10-24.227`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Finite projective modules up to isomorphism, direct-sum monoid, abelian group presentation [P⊕Q]=[P]+[Q]. K′_0 uses finite modules and short exact sequences instead.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.b85b64499f3fb523.grothendieck-group-finite-projectives`](CONTEXTS.md#context-101): For a ring R, K_0(R) is the abelian group generated by finite projective R-modules up to isomorphism, modulo [P⊕Q]=[P]+[Q], equivalently modulo split short exact sequence relations among these modules.

**Mathematical argument:** Group completion supplies formal differences without assuming monoid cancellation; distinct monoid elements can acquire the same group image. Once the monoid is fixed as finite projective isomorphism types, this is precisely the stored K_0 construction. A generic abelian presentation/group-completion operation is a legitimate prerequisite, not the whole chosen K_0 datum. In a fixed universe, representatives of isomorphism types rather than all labeled copies are needed; finite unital modules can be represented as quotients of finite free modules.

**Interpretations:**

- generic group completion: Reusable operation.

- specified K0 presentation: Same specific construction as parent, not an automatic independent resolution.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** K0 versus K′0 inputs/relations and operation versus selected presentation are separated.

**Further evidence or judgment:** Adjudicate generic prerequisite granularity and universe/skeleton convention; do not assume cancellation or identify K0 with K′0.

**Compared existing targets, all stored variants retained:** `meaning.b85b64499f3fb523.grothendieck-group-finite-modules`; `meaning.b85b64499f3fb523.grothendieck-group-finite-projectives`.

**Historical candidate occurrence anchors:** `occ.01238cbe880164b64d91`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-245"></a>
### Rank 245 — inverse limit of the quotient rings

Canonical candidate: `missing.6149b958a6aa818d4806`. Historical `canonical-review.2026-10-24.249`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Compatible tuples in ∏_{n≥1} R/I^n, reduction maps, componentwise ring operations and unit under the unital convention.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.1be2fa074ef447b0.i-adic-ring-completion`](CONTEXTS.md#context-014): For a commutative ring R and ideal I, its I-adic completion R^ is the inverse limit of the quotient rings R/I^n over positive integers n, with transition maps given by reduction modulo smaller powers.

**Mathematical argument:** Reduction maps preserve ring operations, so compatible tuples form a ring with the inverse-limit universal property. Forgetting multiplication gives a module/group limit, not the same structured object. For precisely this ideal-power system the limit is already the stored I-adic completion, so a candidate fixing the whole system cannot be resolved naively to its defining parent without checking self-reference. A degree-zero R/I^0=0 term, if used, is forced and does not change the positive-tail limit; it still must be recorded rather than silently changing indices.

**Interpretations:**

- generic ring inverse limit: Reusable prerequisite.

- this specific limit: The completion construction already named by the parent.

**Recommended disposition:** component prerequisite — **not applied**.

**Decidable now:** Compatible-tuple construction, structured forgetfulness and exact specialization are proved.

**Further evidence or judgment:** Choose generic operation versus whole completion identity; retain units, transition maps and original indices. No self-resolution.

**Compared existing targets, all stored variants retained:** `meaning.1be2fa074ef447b0.i-adic-ring-completion`; `meaning.8d61300dcabf30c0.inverse-limit-sequence-modules`; `meaning.8f7683667fac9d28.category-limit`.

**Historical candidate occurrence anchors:** `occ.7c2b770ad48fcc42b04d`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-405"></a>
### Rank 405 — localization at complement R\p

Canonical candidate: `missing.f179e2d20985ef5e88d5`. Historical `canonical-review.2026-10-24.411`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Prime proper ideal p of commutative unital R, S=R\p containing 1 and closed under multiplication, M_p=S^{-1}M an R_p-module.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.a9ca2e716ceffd36.support-module`](CONTEXTS.md#context-095): For an R-module M, its support Supp_R(M) is the subset {p∈Spec(R):M_p≠0} of the prime spectrum, where M_p denotes localization at p.

**Mathematical argument:** If a,b∉p then ab∉p by primality, and 1∉p. Thus the denominator-set construction is valid. A generic multiplicative set need not be a prime complement: {1}⊆Z has complement Z\{1}, not an ideal. Localization of a module is not localization of a ring alone, and the support predicate additionally tests M_p≠0. Retain these distinct operations instead of equating the entire compound phrase with S.

**Interpretations:**

- prime complement subset: Valid component.

- specialized module localization: Uses that subset and module fractions; richer than a multiplicative set.

**Recommended disposition:** valid specialization — **not applied**.

**Decidable now:** The specialization and nonidentity of subset, ring and module objects are proved.

**Further evidence or judgment:** Choose candidate granularity; existing module-localization meaning is a possible construction target only with exact parameter/scalar scope, not automatic resolution.

**Compared existing targets, all stored variants retained:** `meaning.70f44988651b76b5.module-localization-at-multiplicative-set`; `meaning.a9ca2e716ceffd36.support-module`.

**Historical candidate occurrence anchors:** `occ.0fa8a4b36ea641c54e56`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

## 09 Set, order and graph conventions

<a id="case-154"></a>
### Rank 154 — edge multiplicity

Canonical candidate: `missing.17fcbd3c3e67f2b21f6b`. Historical `canonical-review.2026-10-24.156`; `source_convention_deferral`. Current: **unresolved canonical**.

**Hypotheses and types:** Loopless undirected multigraph: multiset E of two-element subsets of vertex set V. Candidate multiplicity is a nonnegative integer for each unordered pair.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.wave2.graph42.loopless-undirected-multigraph`](CONTEXTS.md#context-188): A loopless undirected multigraph is a pair G=(V,E), where V is a set of vertices and E is a multiset of two-element subsets of V. Two copies of {u,v} represent parallel edges joining u and v; the graph is simple exactly when each edge multiplicity is at most one.

**Mathematical argument:** Two vertices with three parallel copies have pair multiplicity 3; the simple-graph predicate keeps only 0/1. An infinite vertex set does not force infinite multiplicity per pair, while a cardinal-valued multiset with infinitely many copies of one pair need not have integer multiplicity. Loops are excluded by the two-element edge condition independently of multiplicity. The source has not specified which multiset convention it uses.

**Interpretations:**

- finite per pair multiset: Integer-valued multiplicity fits.

- cardinal valued multiset: Broader convention not identified with N-valued counts.

**Recommended disposition:** source-verification required — **not applied**.

**Decidable now:** Parallel-edge count, degree, edge pair and whole multiset are different.

**Further evidence or judgment:** Verify finite-per-pair convention without imposing finite V or finite E; preserve loopless scope.

**Compared existing targets, all stored variants retained:** `meaning.wave2.graph42.loopless-undirected-multigraph`; `meaning.wave2.graph42.simple-undirected`.

**Historical candidate occurrence anchors:** `occ.744c033d856601736101`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-181"></a>
### Rank 181 — singleton {a} and unordered pair {a,b}

Canonical candidate: `missing.2d4e4af6f3b83da929a6`. Historical `canonical-review.2026-10-24.184`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Arbitrary sets a,b in Kuratowski (a,b)={{a},{a,b}}; no a≠b hypothesis.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.wave2.foundation.ordered-pair-kuratowski`](CONTEXTS.md#context-168): For arbitrary sets a and b, the Kuratowski ordered pair is (a,b):={{a},{a,b}}. This set-theoretic construction has the defining property (a,b)=(c,d) if and only if a=c and b=d.

**Mathematical argument:** When a=b, {a,b}={a} and the outer pair is {{a}}, still a valid ordered pair. Thus unordered pair has at most two members, while doubleton has exactly two. The graph two-vertex edge prerequisite requires distinct arguments and is narrower. A singleton constructor alone does not provide the whole nested two-constructor datum.

**Interpretations:**

- unordered pair possibly singleton: Fits the actual arbitrary-coordinate source.

- literal doubleton: Overrestrictive without a≠b.

**Recommended disposition:** convention clarification — **not applied**.

**Decidable now:** The equal-coordinate counterexample settles the wording issue.

**Further evidence or judgment:** Approve later wording/constructor segmentation if desired, retaining arbitrary coordinates. No candidate alias or source edit applied.

**Compared existing targets, all stored variants retained:** `meaning.wave2.foundation.ordered-pair-kuratowski`.

**Historical candidate occurrence anchors:** `occ.af14da7f06b8c83e1cb0`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-259"></a>
### Rank 259 — no largest element

Canonical candidate: `missing.6e286e5d25f8e80fa9f6`. Historical `canonical-review.2026-10-24.264`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Dedekind lower cut A⊂Q: nonempty, proper, downward closed, no largest element. Q is totally ordered.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.wave2.real50.dedekind-rational-lower-cut`](CONTEXTS.md#context-210): A (lower) Dedekind cut of the rational numbers is a subset A of Q such that A is nonempty, A is not all of Q, if a belongs to A then every rational q<a also belongs to A, and A has no largest element.

**Mathematical argument:** In a total order, absence of greatest element implies for each a∈A some b∈A satisfies b>a; otherwise a would be greatest. In a two-point antichain there is no greatest element but each point is maximal, so the same equivalence fails in arbitrary partial orders. The actual rational-cut parent is correctly in the total-order setting. Properness and no largest element are separate; neither should be deleted or confused with ambient greatest elements.

**Interpretations:**

- total order no largest: Equivalent to no maximal element in the actual context.

- partial order generalization: False as an unqualified equivalence.

**Recommended disposition:** convention clarification — **not applied**.

**Decidable now:** The candidate-context qualification can be decided mathematically.

**Further evidence or judgment:** Later qualify total-order scope; do not change approved rational cut endpoints, nonemptiness or properness.

**Compared existing targets, all stored variants retained:** `meaning.709d3d2f82950c5b.partially-ordered-set`; `meaning.wave2.real50.dedekind-rational-lower-cut`.

**Historical candidate occurrence anchors:** `occ.5c59b3261c91e60cc9b8`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

<a id="case-324"></a>
### Rank 324 — set family P

Canonical candidate: `missing.a128ec6b5c7fae2074c2`. Historical `canonical-review.2026-10-24.329`; `contextual_ambiguity_or_variant`. Current: **unresolved canonical**.

**Hypotheses and types:** Partition P is an unindexed collection of nonempty disjoint blocks covering S. Arbitrary indexed families retain indexing and multiplicities.

**Full original source formulations** (their exact source versions are unchanged; IDs link to complete reference/provenance records):

- [`form.wave2.group116.set-partition.2`](CONTEXTS.md#context-191): Equivalently, a partition P of S is a collection of nonempty subsets of S such that for each s∈S there exists exactly one B∈P with s∈B.

**Mathematical argument:** Two equal subsets at two distinct indices become one member on forgetting indices, so indexed family and set of subsets are different data. P can be indexed by itself, but that encoding does not equate all indexed families to collections. For S=∅, P=∅ is the valid partition; {∅} violates nonempty blocks. Both stored partition variants preserve exactly these conditions.

**Interpretations:**

- collection of blocks: Fits the parent.

- arbitrary indexed family: Adds index data not present in P.

**Recommended disposition:** convention clarification — **not applied**.

**Decidable now:** Collection/indexed-family distinction and empty case are settled.

**Further evidence or judgment:** Choose canonical scope or explicit encoding policy without aliases to unrelated event or map families.

**Compared existing targets, all stored variants retained:** `meaning.wave2.group116.set-partition`.

**Historical candidate occurrence anchors:** `occ.c53e9755c2a9b738c722`. Exact observed candidate IDs and source/node SHA256 pairs are in this case’s `parents` entries in `EVIDENCE.json`.

## Decision boundary

No lexical match authorizes an identity. The clearest mathematical qualifications are rank 40’s irreducibility, rank 54’s unit-action span formula, rank 181’s possibly singleton pair, rank 250’s characteristic-zero reading, rank 259’s total-order scope, rank 298’s zero-divisor variants, and rank 400’s scalar base. Their mathematical arguments can be assessed now; whether and how to represent them in candidate records is still a separate user decision.

The 13 source-convention cases remain bounded verification deferrals. Generic/component granularity is a shared modeling question rather than 27 automatically invalid edges. The applied corrections must not be counted as outstanding transactions. No report here opens the consolidation gate, declares Pass 2 complete or authorizes Pass 3.
