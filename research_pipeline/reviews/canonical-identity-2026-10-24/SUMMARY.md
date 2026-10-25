# Canonical identity audit — tranche 1

Base `cd1c774b`; post-FIP and adopted unitality adjudication respected.

421 inventoried; **4 complete, 2 partial, 415 untouched**. 62 distinct source formulations reviewed. COMPLETE denotes parent-context coverage, not resolution of all mathematical questions. Two complete reviews retain explicit object/compound-reference ambiguity.

| Rank | Candidate | Coverage | Disposition | Parents reviewed / total |
|---|---|---|---|---|
| 1 | `missing.fcb5ab865c6d9dbb3d79` | PARTIAL | retain_distinct_missing | 6/42 |
| 2 | `missing.c5104821c3c70afa1f63` | PARTIAL | retain_distinct_missing | 6/36 |
| 3 | `missing.50fc57153b93520a247a` | COMPLETE | contextual_ambiguity_or_variant | 16/16 |
| 4 | `missing.b86257b3cce62907e97e` | COMPLETE | retain_distinct_missing | 15/15 |
| 5 | `missing.9db64b2f9cdb8258e3d8` | COMPLETE | contextual_ambiguity_or_variant | 14/14 |
| 6 | `missing.38969d113c4ee1db6e98` | COMPLETE | retain_distinct_missing | 11/11 |

Confident retain-distinct missing: 2 complete (preimage, residue field); provisional retain/nonmerge on 2 partial high-fanout candidates. Candidate aliases proposed: 0; existing-meaning resolutions proposed: 0; source-convention-deferral dispositions: 0 (the already-adopted nine-case policy is preserved separately); contextual ambiguity: 2 complete; needs-recheck disposition: 0. Residual uncertainties are retained in every record.

## 1. category (size-unrestricted)

The six reviewed parents use an ambient ordinary category, not a category with a set of all objects. Initial/final objects and pushout universal properties place conditions on arrows but do not bound object cardinality. A monoidal structure adds tensor/coherence, not smallness. The representable and compact-object formulas use set-valued Hom and therefore need local-smallness/universe attention separately; local smallness does not imply a set of all objects. The existing small-category definition has the additional object-set restriction. The category of sets (relative to a universe convention) supplies the standard separating pattern: set-valued homs but not a small object collection in the same universe. This is a nonmerge judgment for the reviewed contexts, not complete verification of all 42 parents.

Remaining: 36 parents remain; no homogeneity argument has been substituted for reading them.; Hom set/universe scope in compact and representable cases remains a distinct source-scope question.

## 2. functor F:C→D

The reviewed sources use ordinary identity/composition-preserving maps of categories. A bifunctor is an ordinary functor on a product category; a projection p:E→C and functors over C still have underlying ordinary functor data. Strong monoidal and over-base conditions remain additional parent structure and are not erased by using the generic prerequisite. The existing covariant-functor meaning explicitly restricts both categories to be small; the current contexts do not supply those bounds. The contravariant meaning reverses arrows or is covariant on C^op and is not automatically identical with a covariant functor on C. The iso-comma source uses two covariant functors into a common C; it retains an invertible comparison arrow, unlike the unrestricted comma construction.

Remaining: 30 parents remain, including presheaf/opposite-source and exact/tensor functor cases.; The product-category domain and relative-to-base equations must be retained, not inferred from an untyped word functor.

## 3. quotient ring R/I

All 16 parents were read. Ideal-power quotients, prime quotients, polynomial-presentation quotients, square-zero quotients, and S_q/pS_q share the additive-coset construction with induced multiplication. Well-definedness follows because changing representatives by elements of an ideal changes sums/products by elements of that ideal. This is not an additive/module quotient alone: Z/2 as an additive quotient carries no general recipe for multiplying arbitrary quotient modules; the ring construction needs multiplication on the parent and an ideal. Quotients can be nonfields (Z/4), so the existing special field k[t]/(f) for irreducible f cannot resolve this general identity. Localization inverts a multiplicative set instead of killing an ideal. However occ.39767a08c003da7e344c in formally-smooth-ring-map has a compound context: an R-algebra, square-zero ideal, quotient algebra AND canonical quotient map, described as an extension. The underlying ring quotient is a justified shared prerequisite, but a whole square-zero extension datum is not identical to a quotient-ring object. Existing aliasing is not certified as equality of those compound objects by this review.

Remaining: Adjudicate segmentation of the compound formally-smooth occurrence: underlying quotient prerequisite versus extension/map datum. No split or alias change applied.; Several paraphrases omit ambient commutative-unital hypotheses; preserve the recorded commutative-algebra scope and adopted source-convention policy, without asserting those hypotheses for arbitrary noncommutative variants.

## 4. inverse image

All 15 parents were read: open/quasi-compact/measurable preimages, contractions of ideals, kernel singletons, and the contracted prime in a local fibre all use {x:f(x)∈B}. For a constant map from a two-element set to a singleton this operation is defined for every subset, while an inverse function does not exist. For a ring map, preimage of a prime is prime by multiplicativity and preservation of 1, but generic set preimage does not assert any ideal or prime property. For an inclusion, phi^-1(q)=q∩R; this is not an assumed equality for maps not represented as inclusions. Kernel structure is a consequence of linearity, not part of the generic set operation. Continuity/measurability constrain which B have open/measurable preimages; they do not change the underlying operation. The recorded bare/typed mapping and image meanings define functions or direct images, not this inverse-image-of-a-subset operation.

Remaining: This verifies identity use across these parents, not every parent theorem. The existing module-kernel unitality link and submersive wording are source-scope matters, not new preimage identities.; Related contracted-prime candidate is compared by full context only; its own parent audit remains UNREVIEWED.

## 5. polynomial ring R[x_1,…,x_n]

All 14 parents were read. Formal polynomial algebras occur with one, finite, or arbitrary set-indexed variables, including S-indexed variables in the naive cotangent complex. Finite support of each polynomial does not force the whole variable family to be finite; a finite-variable specialization is not a reason to restrict the generic missing algebra to finite rank. A polynomial ring is not a degree predicate, a quotient by equations, or an evaluated element. In particular occ.aa7d5dd9a4e322c869e6 (strongly-transcendental-subring-element) has context explicitly allowing an indeterminate OR its evaluation at x∈S. Evaluation can lose information: T and 0 in R[T] have the same value at x=0 but are different formal polynomials. A polynomial-algebra prerequisite is justified for coefficient expressions, but the current mixed context must not be treated as a proof that a polynomial and its value, or a ring and one element, are the identical object. The nonzero-polynomial qualifier in the algebraic-extension source remains a source restriction, not an exclusion of zero from the polynomial algebra itself.

Remaining: Adjudicate whether the strong-transcendence occurrence means a formal-polynomial prerequisite or an evaluation construction; do not silently declare the existing alias an object equality.; Characteristic-polynomial source uses an identity matrix while the general ring seed permits no identity: preserve source scope rather than changing candidates here.; Comparison candidate contexts were read, but their parent coverage is not claimed complete; no new alias is proposed.

## 6. residue field of a local ring

All 11 parents were read: local/Tor/regularity criteria, fibre constructions, Henselian lifting, fibrewise maps, relative assassin, syntomic fibres and coefficient rings. They use A/m for the specified commutative local ring, including A=R_p and scheme local rings. For a proper maximal ideal m in a unital commutative A, a∉m gives (a)+m=A, so ra+b=1 for some b∈m; [r] inverts [a]. Thus A/m is a field, but a bare field definition does not specify its quotient construction, map or relation to (A,m). Generic quotient rings need not be fields, and Frac(D) preserves an embedded domain instead of killing a maximal ideal. For A=Z_(p), its residue field has characteristic p while Frac(A)=Q has characteristic zero, disproving a general residue/fraction-field identification. In coefficient-ring contexts an induced residue-field isomorphism is a map between such fields, not the residue field itself.

Remaining: Retain current commutative-unital local-ring scope; source conventions and the assertions of the host criteria are not independently certified.; No exact existing generic residue-field construction was found in the checked inventory descriptors and plausible definitions; related candidate parents remain unreviewed.

## Resume and boundaries

Resume the first partial category candidate at `form.34c38bc0b482f182.binary-coproduct-category`; exact remaining IDs are in reviews.jsonl. After both partial high-fanout candidates, rank 7 is the first untouched identity. No blanket homogeneity argument substitutes for unread sources. Full reviewed sources, effective references, observation/locator metadata and source records are preserved in source-contexts.jsonl; comparison-only candidate contexts do not count as their own deep reviews.

The three existing read-only audit CLIs passed on the active snapshot; graph/index/source files are unchanged. No engine review ledger, alias, resolution, source, gate or phase was modified. This is not a global consolidation rationale.
