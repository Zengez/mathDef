# Canonical identity audit — first substantial tranche

Base `cd1c774b4a44f25416890513dcfe98030c948091`; post-FIP repair and adopted unitality adjudication respected. The active graph matches both preparing hashes; no drift.

**421 inventoried; 8 complete parent-context reviews; 0 partial; 413 untouched.** 134 distinct original source formulations reviewed, across 156 candidate/parent visits and 177 candidate occurrences. COMPLETE is coverage, not mathematical resolution or source certification.

Manifest rows remain initially UNREVIEWED permanently. The append-only review event ledger supplies current status; two initial partial events are retained and superseded explicitly by complete events. Checkpoint lists exact IDs and latest events, not just counts.

| Rank | Candidate | Parents | Current disposition |
|---|---|---|---|
| 1 | `missing.fcb5ab865c6d9dbb3d79` | 42/42 | retain_distinct_missing |
| 2 | `missing.c5104821c3c70afa1f63` | 36/36 | retain_distinct_missing |
| 3 | `missing.50fc57153b93520a247a` | 16/16 | contextual_ambiguity_or_variant |
| 4 | `missing.b86257b3cce62907e97e` | 15/15 | retain_distinct_missing |
| 5 | `missing.9db64b2f9cdb8258e3d8` | 14/14 | contextual_ambiguity_or_variant |
| 6 | `missing.38969d113c4ee1db6e98` | 11/11 | retain_distinct_missing |
| 7 | `missing.5645554e6bee6b40edda` | 11/11 | source_convention_deferral |
| 8 | `missing.7462fa5f90275b34779a` | 11/11 | retain_distinct_missing |

Counts: confidently retain-distinct missing **5** (category, functor, preimage, residue field, free module); contextual ambiguities **2** (quotient, polynomial); source-convention deferral **1** (commutative-unital ring); needs-recheck disposition **0**; new candidate aliases proposed **0**; new existing-meaning resolutions proposed **0**. Mathematical questions remain in complete records. No reduction of the canonical registry is attempted.

## 1. category (size-unrestricted)

All 42 parent formulations have now been read, including their complete reference lists and provenance metadata. Initial/final objects, limits/colimits, filtered/cofiltered and connected categories, fibred/inertia constructions, localization, strict 2-category hom-categories, presheaves, opposite categories and preadditive categories all invoke an underlying ordinary category. None of the universal properties or extra tensor/additive/fibre structure forces the object collection to be a set. In the set-valued Hom parents, a local-smallness/universe condition is needed for the displayed Hom sets; it still does not imply a small object collection. The existing small-category meaning explicitly requires an object set, and the specialized discrete, monoidal, fibred and preadditive meanings impose additional structure. The category of sets relative to a universe is the standard separating pattern for object smallness versus local smallness. A historical seed whose phrase says diagram or functor is understood only as a prerequisite for its ambient categories, not an assertion that a functor object is itself a category. Thus retain the distinct generic missing identity; no existing meaning checked covers it without additional size/structure restrictions.

Residual uncertainty: Local Hom set/universe questions in compact and representable formulas remain source-scope questions, not proof of global smallness.; The coproduct word injections is not certified to mean monomorphisms in every category; that source-wording issue does not alter this ambient category identity.; Complete here means review of all 42 parent contexts for this identity, not a full correctness certification of every parent theorem.

## 2. functor F:C→D

All 36 parents were read. Ordinary diagrams, projections and over-base functors, tensor bifunctors on product categories, exact functors, adjoint pairs, localizations and Hom/tensor functors all use ordinary covariant functor data in their correctly typed domains. A diagram I→C with small/finite I does not make C small, so it is not covered by the existing small-to-small functor definition. An inverse system is covariant on I^op; a represented presheaf is covariant C^op→Sets. In category/groupoid-valued presheaves the current source explicitly uses C^op→Cat/Groupoids with strict composition, not another contravariance on C^op. Opposite directions of the two functors in an adjunction do not make either contravariant. Tensoring maps sends g to g⊗id, and Hom_R(P,−) sends g to postcomposition, both covariantly; these actions are not merely tensor/Hom objects. Extra exactness, monoidal structure, over-base equations and pseudofunctor comparison cells remain separate. The generic strict-functor prerequisite is missing under the checked inventory; no alias to a contravariant or smallness-constrained meaning is justified.

Residual uncertainty: Tensor functor parents retain their commutative-ring or appropriate bimodule hypotheses; ordinary functoriality does not validate an ill-typed left-left tensor product over an arbitrary noncommutative ring.; Size conventions for the target categories Cat and Groupoids remain separately recorded; no new universe convention is inferred.; No source re-verification or automatic alias/resolution follows from full parent-context coverage.

## 3. quotient ring R/I

All 16 parents were read. Ideal-power quotients, prime quotients, polynomial-presentation quotients, square-zero quotients, and S_q/pS_q share the additive-coset construction with induced multiplication. Well-definedness follows because changing representatives by elements of an ideal changes sums/products by elements of that ideal. This is not an additive/module quotient alone: Z/2 as an additive quotient carries no general recipe for multiplying arbitrary quotient modules; the ring construction needs multiplication on the parent and an ideal. Quotients can be nonfields (Z/4), so the existing special field k[t]/(f) for irreducible f cannot resolve this general identity. Localization inverts a multiplicative set instead of killing an ideal. However occ.39767a08c003da7e344c in formally-smooth-ring-map has a compound context: an R-algebra, square-zero ideal, quotient algebra AND canonical quotient map, described as an extension. The underlying ring quotient is a justified shared prerequisite, but a whole square-zero extension datum is not identical to a quotient-ring object. Existing aliasing is not certified as equality of those compound objects by this review.

Residual uncertainty: Adjudicate segmentation of the compound formally-smooth occurrence: underlying quotient prerequisite versus extension/map datum. No split or alias change applied.; Several paraphrases omit ambient commutative-unital hypotheses; preserve the recorded commutative-algebra scope and adopted source-convention policy, without asserting those hypotheses for arbitrary noncommutative variants.

## 4. inverse image

All 15 parents were read: open/quasi-compact/measurable preimages, contractions of ideals, kernel singletons, and the contracted prime in a local fibre all use {x:f(x)∈B}. For a constant map from a two-element set to a singleton this operation is defined for every subset, while an inverse function does not exist. For a ring map, preimage of a prime is prime by multiplicativity and preservation of 1, but generic set preimage does not assert any ideal or prime property. For an inclusion, phi^-1(q)=q∩R; this is not an assumed equality for maps not represented as inclusions. Kernel structure is a consequence of linearity, not part of the generic set operation. Continuity/measurability constrain which B have open/measurable preimages; they do not change the underlying operation. The recorded bare/typed mapping and image meanings define functions or direct images, not this inverse-image-of-a-subset operation.

Residual uncertainty: This verifies identity use across these parents, not every parent theorem. The existing module-kernel unitality link and submersive wording are source-scope matters, not new preimage identities.; Related contracted-prime candidate is compared by full context only; its own parent audit remains UNREVIEWED.

## 5. polynomial ring R[x_1,…,x_n]

All 14 parents were read. Formal polynomial algebras occur with one, finite, or arbitrary set-indexed variables, including S-indexed variables in the naive cotangent complex. Finite support of each polynomial does not force the whole variable family to be finite; a finite-variable specialization is not a reason to restrict the generic missing algebra to finite rank. A polynomial ring is not a degree predicate, a quotient by equations, or an evaluated element. In particular occ.aa7d5dd9a4e322c869e6 (strongly-transcendental-subring-element) has context explicitly allowing an indeterminate OR its evaluation at x∈S. Over a nonzero coefficient ring, evaluation can lose information: T and 0 in R[T] have the same value at x=0 but are different formal polynomials. A polynomial-algebra prerequisite is justified for coefficient expressions, but the current mixed context must not be treated as a proof that a polynomial and its value, or a ring and one element, are the identical object. The nonzero-polynomial qualifier in the algebraic-extension source remains a source restriction, not an exclusion of zero from the polynomial algebra itself.

Residual uncertainty: Adjudicate whether the strong-transcendence occurrence means a formal-polynomial prerequisite or an evaluation construction; do not silently declare the existing alias an object equality.; Characteristic-polynomial source uses an identity matrix while the general ring seed permits no identity: preserve source scope rather than changing candidates here.; Comparison candidate contexts were read, but their parent coverage is not claimed complete; no new alias is proposed.

## 6. residue field of a local ring

All 11 parents were read: local/Tor/regularity criteria, fibre constructions, Henselian lifting, fibrewise maps, relative assassin, syntomic fibres and coefficient rings. They use A/m for the specified commutative local ring, including A=R_p and scheme local rings. For a proper maximal ideal m in a unital commutative A, a∉m gives (a)+m=A, so ra+b=1 for some b∈m; [r] inverts [a]. Thus A/m is a field, but a bare field definition does not specify its quotient construction, map or relation to (A,m). Generic quotient rings need not be fields, and Frac(D) preserves an embedded domain instead of killing a maximal ideal. For A=Z_(p), its residue field has characteristic p while Frac(A)=Q has characteristic zero, disproving a general residue/fraction-field identification. In coefficient-ring contexts an induced residue-field isomorphism is a map between such fields, not the residue field itself.

Residual uncertainty: Retain current commutative-unital local-ring scope; source conventions and the assertions of the host criteria are not independently certified.; No exact existing generic residue-field construction was found in the checked inventory descriptors and plausible definitions; related candidate parents remain unreviewed.

## 7. commutative unital ring

All 11 parents were read. Five explicitly require an identity: commutative prime/maximal ideals, field, integral domain, and Noetherian module over a commutative ring with identity. Their additional properness, nonzeroness, invertibility or Noetherianity belongs to the parent, not to the bare ring candidate. Six Stacks-attributed paraphrases (nil ideal, both Jacobson-ring criteria, clopen spectrum, normal ring and irreducible spectrum components) say commutative ring without spelling out 1. As in the adopted adjudication policy, source attribution is not independent evidence of an ambient convention. Retain the recorded commutative-unital missing type, but defer exact source scope of those six uses; do not equate it with the existing identity-optional associative ring or certify the omitted unit hypothesis. Noncommutative 2x2 matrices show that having an identity does not force commutativity; the zero-product C2 rng shows commutativity alone need not give an identity. Z/4 is commutative unital but not an integral domain or field, so those stricter existing meanings are not generic resolutions. The zero ring question (whether 1=0 is permitted) must not inherit the field/domain parents nonzero condition accidentally.

Residual uncertainty: For the six bare-ring paraphrases, later source reconciliation must establish the actual multiplicative-identity and zero-ring conventions; no new external research here.; This documents additional parents under the adopted general source-convention policy; it does not reopen the nine already adjudicated cases as new identity defects.

## 8. free R-module F_i

All 11 parents were read. Finite free R^n in presentations and Lazard diagrams, arbitrary R^(I) in resolutions/direct-summand characterizations, and free modules over localized rings instantiate the same basis/direct-sum construction while preserving rank and coefficient-ring restrictions in the parent. Finite support of each vector in a direct sum does not imply the index set is finite: over a nonzero field the infinitely many standard basis vectors cannot be spanned by a finite list, whose union of supports is finite. Existing finitely generated modules need not be free (Z/2 as a Z-module has torsion), and locally free/projective modules need not be globally free: for R=k×k, eR with e=(1,0) is a finite direct summand of R and locally free with component ranks (1,0), whereas any globally free R^n has ranks (n,n). The already-adjudicated free-resolution augmentation forces its terminal module to be unital under its recorded free-module construction. No rank-finiteness, projectivity-only, or local-free meaning can resolve the missing general free module.

Residual uncertainty: Rank zero and zero-ring conventions must remain explicit in future population; the separating infinite-rank argument uses a nonzero field.; This review checks the free-module prerequisite, not all claims about global rank of maps or finite locally free/projective equivalences in the host formulations.

## Resume

First unfinished rank **9**, `missing.6baca7285e379e18e82b` (quotient R-module), beginning with `form.138b13bf27c037c1.naive-cotangent-complex`. Ranks 9–30 remain inventory priorities, not reviewed records. Compared candidate contexts (e.g. contraction, polynomial evaluation and generic direct sums) do not count as deep reviews of those identities. Re-run the validator before continuing; invalidate or re-anchor the tranche if the active inventory/pool or a reviewed source/node differs.

## Evidence and boundaries

Full original source texts, contexts, full effective reference records, source versions/node hashes, observed aliases and original provenance/locator metadata are retained in the two evidence JSONL files. No automatic similarity score generated these semantic dispositions. The proofs are for contextual identity use; they do not certify all host theorems. In particular underlying-structure use is not proof that an entire compound phrase is that underlying object.

The three existing read-only audit CLIs succeeded with 19 mechanical readiness checks; the FIP issue is repaired and the nine unitality cases retain their adopted deferral policy. No external mathematical source was fetched. Source/graph hashes and changed paths were checked. No source, graph, semantic ledger, alias, resolution, gate or phase changes were made. This tranche is not a global consolidation rationale.

## Validation at this checkpoint

Run from the repository root:

```bash
python research_pipeline/reviews/canonical-identity-2026-10-24/validate.py
python -m unittest research_pipeline.tests.test_dependency_global_audit research_pipeline.tests.test_dependency_cycle_analysis research_pipeline.tests.test_dependency_consistency_worklist research_pipeline.tests.test_dependency_consolidation_readiness
```

Actual results: coverage/anchor validator **PASS**; **60 tests passed**. The validator compares every manifest identity/context, all reviewed source versions and effective references, event digests, supersession and exact parent coverage with the current independent snapshot. It does not certify mathematical judgments. The existing focus (`--limit 30 --max-formulations 1000`), scan (`--limit 80 --candidate-limit 80`) and readiness (`--exhaustive`) commands all exited successfully; readiness returned `mechanical_checks_passed_review_decision_required`, with 19 checks and no mechanical integrity failures.

All **2,281** independent-workspace files have identical before/after SHA-256 values. The branch-to-base changed paths are confined to this audit directory: `SUMMARY.md`, `manifest.jsonl`, `reviews.jsonl`, `source-contexts.jsonl`, `checkpoint.json`, `validate.py`. No engine behavior changed. Earlier checkpoints preserve the inventory and partial coverage; later review events supersede rather than erase those judgments.
