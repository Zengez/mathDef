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

## Continuation progress (PR #10)

**Current cumulative coverage: 23 COMPLETE / 0 PARTIAL / 398 untouched; 421 inventoried.** 15 new complete reviews in this continuation. The first-tranche counts and narrative above are historical; the append-only ledger and this current section give current coverage.

Dispositions: contextual_ambiguity_or_variant: **3**, retain_distinct_missing: **18**, source_convention_deferral: **2**. New aliases/resolutions proposed: **0/0**. Complete means all parent contexts considered for identity, not resolution or source certification.

### 9. quotient R-module by a submodule — `missing.6baca7285e379e18e82b`

**retain_distinct_missing; 10 / 10 parents.** All ten contexts use cosets of an R-submodule, with r(m+N)=rm+N well-defined because rN⊆N. I/I² and m/m² also acquire scalar actions through P/I and R/m because the ideal acts trivially on the quotient; that extra action is not a generic quotient ring or vector-space definition. Completion stages, filtration factors, and R/(a) for module length use the same module construction; a colimit additionally chooses a direct sum and relation submodule. A quotient set forgets both addition and scalar action, and the quotient-group meaning supplies no R-action. A generic quotient module has no required multiplication: for example the Z-module Z/2⊕Z/3 has no multiplication specified by its module data. Existing quotient-ring candidate requires an ideal in a parent ring, whereas M and N here need only be modules. The regular-sequence unitality exception remains governed by the adopted Chat policy. No checked existing meaning defines general module cosets with induced scalar action.

Uncertainty: Ambient unitality of bare module/ring sources remains under the existing scoped convention deferral; no theorem of the host formulas is certified.

### 10. injective mapping — `missing.4ba0cfe171bbe93d0c9a`

**retain_distinct_missing; 8 / 8 parents.** The eight occurrences test f(x)=f(y)⇒x=y for specified maps: evaluation, field-tensor multiplication, scalar multiplication, tensor comparisons and fibre maps. For additive maps this is equivalent to zero kernel, since f(x)=f(y) iff f(x−y)=0, but the module-kernel construction is not the general predicate. Ordinary injectivity is weaker than universal tensor injectivity: multiplication by 2 on Z is injective, while tensoring with Z/2 yields the zero map on Z/2. Thus the existing pure-monomorphism meaning is not a resolution. A map can be injective without surjectivity (inclusion {0}→{0,1}); no bijection, inverse function or categorical isomorphism follows. Field embeddings retain their ring axioms separately, and no default algebraic independence is inferred without the appropriate quantified evaluation map. No checked mapping definition supplies the missing predicate.

Uncertainty: Tensor-product module-side and unital conventions belong to the host source; injectivity alone does not settle them.

### 11. surjective R-linear map R^n→M — `missing.c8a3e68d130a4f68d108`

**retain_distinct_missing; 8 / 8 parents.** All eight parents require every element of a fixed codomain to be attained. This is exactly im(f)=Y using the existing image construction, but image as an object is not the predicate equating it with Y. The canonical query mentions R^n→M, yet its stored context explicitly abstracts the onto-condition; free domain, R-linearity, algebra structure, localization, localness and continuity are separately retained. A constant two-element-to-singleton map is surjective without injectivity. Onto f(X) is automatic for any function and cannot replace onto Y: {0}→{0,1} separates them. The finite-generation criterion requires a linear surjection for some finite rank; projectivity quantifies lifting across all linear surjections. The empty space has no surjection onto two points, preserving the stated connectedness convention. None of the checked map/image or specialized locus meanings defines the generic onto-condition.

Uncertainty: The submersive biconditional issue is an adopted source-wording deferral; no source edit is applied. Bare module unitality remains source-scoped.

### 12. categorical isomorphism — `missing.15bb96cb26d587868bbe`

**retain_distinct_missing; 7 / 7 parents.** Each of the seven contexts requires an arrow with a two-sided inverse in its stated category: locally ringed spaces, topological groups, commutative rings, a localization, a small groupoid, or an abelian category. If g and h are both inverses, g=g(fh)=(gf)h=h, so the inverse is unique, but all structure in the ambient morphisms must remain. A bijective continuous map need not be a homeomorphism: the identity from a discrete two-point space to its indiscrete topology has no continuous inverse. Consequently a set bijection, a plain homeomorphism without group/sheaf data, and an isomorphism of graphs cannot resolve generic categorical invertibility. In the abelian-category sentence the phrase isomorphism of categorical morphisms means the comparison arrow Coim(f)→Im(f) is invertible, not an isomorphism between arrows in an arrow category. Specialized aliases are justified only as instances of this predicate with ambient category retained.

Uncertainty: For compound structured isomorphism phrases the category/morphism definition must stay explicit. No claim is made that generic invertibility defines those categories.

### 13. scalar extension of k-algebra — `missing.ad976486b1e3635e60d2`

**retain_distinct_missing; 7 / 7 parents.** The seven sources form the same commutative K-algebra A⊗_kK, with (a⊗u)(b⊗v)=ab⊗uv, unit 1⊗1 and K-map u↦1⊗u. These operations are balanced over k and distribute, so they extend from pure tensors. The existing tensor-module meaning supplies the additive universal object, not multiplication or its chosen K-structure. The existing base-change ring-map meaning instead defines the arrow K→A⊗K; its codomain is a legitimate related construction, not an identity of that arrow with the algebra object. The module base-change meaning presupposes the coefficient algebra, and tensor algebra is a sum of tensor powers with concatenation, not this two-factor scalar extension. Choosing perfect or algebraic closure specializes K without replacing a parent quantifier over all or finite extensions. Connectedness/reducedness/domain/regularity are different tests on the result, not consequences of forming a tensor product. Compound k-algebra A AND extended K-algebra phrases refer only to this component prerequisite; they do not identify the input and output algebras.

Uncertainty: Recorded equivalences of finite/perfect/algebraic-closure tests are not proved by this identity review. Source convention and zero-algebra scope remain source-scoped.

### 14. least upper bound sup(A) — `missing.066b1d1b9032a2e86bdd`

**retain_distinct_missing; 6 / 6 parents.** In all six parents the common operation is least upper bound in a specified order, not its existence for every subset. If u and v both satisfy the upper-bound/least conditions then u≤v and v≤u, so antisymmetry gives u=v. The existing Dedekind completeness meaning is a quantified existence property of an ordered set, not the supremum of an individual subset. In the real-field and operator-norm sources, nonempty bounded real sets are used (the norm ball contains zero and boundedness gives a finite bound); cardinal supremum is taken in cardinal order, not real order. Depth and module dimension use extended nonnegative integers, with infinity for unbounded length sets. A supremum need not be attained: (0,1) in R has supremum 1 without a maximum. Thus maximum, completeness and metric completion are not generic resolutions. The depth convention IM=M⇒∞ is separately stipulated, not derived as a finite maximum.

Uncertainty: Exact empty-support/zero-module dimension conventions and the depth empty-sequence boundary need later source reconciliation; the order operation does not choose them.

### 15. morphism set Hom_C(X,Y) — `missing.6614c6b7c105cc0e6415`

**retain_distinct_missing; 6 / 6 parents.** All six sources collect arrows with fixed endpoints; varying one endpoint then composing defines a Hom functor, which is extra data. Small categories make every such collection a set; preadditivity makes it an abelian group, which also forces a set under the recorded convention, without making the object collection small. The compact-object and representable sources explicitly use set-valued comparisons and therefore need local size/universe scope; a generic unrestricted category alone does not imply every Hom collection is a set. Hom_Sch(T,X) consists of scheme morphisms, not all functions on underlying point sets. Existing internal Hom is the R-module of R-linear maps with pointwise operations, a specialization of a Hom collection and not the general categorical construction. Existing small-category meaning packages objects, composition and identities rather than defining only this collection. A one-object category has one object but its Hom can contain many arrows, separating objects from morphism collections.

Uncertainty: Set-valued Hom in an otherwise unrestricted category still needs an explicit local-smallness/universe convention; no global size assumption is invented.

### 16. monic polynomial — `missing.87eab2bf93382f4b93d6`

**retain_distinct_missing; 6 / 6 parents.** All six sources require leading coefficient 1 in the commutative univariate polynomial algebra. Monicity does not imply irreducibility: T² is monic and reducible over a field; 2T+1 over Q is degree one and irreducible but not monic as written. Degree is a number attached to a nonzero polynomial, while monicity constrains a coefficient. A minimal polynomial additionally generates an evaluation kernel; étale presentation and Henselian lifting add derivative or root conditions; ideal integrality imposes d≥1 and prescribed ideal-power coefficients. For a unital coefficient map with nonzero target, a monic polynomial keeps its leading coefficient after mapping, and finitely many image coefficients may be lifted to coefficients in R; no injectivity of R→S is needed. The generic monic candidate includes constant 1, but a vanishing integrality witness in a nonzero algebra cannot be that constant; its positive-degree restriction must stay visible.

Uncertainty: The canonical nonzero-polynomial leading-coefficient convention needs explicit handling if zero coefficient rings are allowed; no zero-ring convention or source repair is chosen here.

### 17. standard open D(f) inside Spec(R) — `missing.8e961cb57c3f60513be8`

**retain_distinct_missing; 6 / 6 parents.** All six contexts use D(f)={p:f∉p}; D(f) is the complement of V((f)) in the prime spectrum. For a prime p, fg∉p iff f∉p and g∉p, so D(fg)=D(f)∩D(g), explaining localized overlap contexts. An idempotent e gives e(1−e)=0, forcing every prime to contain e or 1−e but not both, hence D(e)=V(1−e) is also closed. This special clopen case does not make arbitrary principal opens clopen: D(2) in Spec(Z) excludes the prime (2), and its complement V(2) is not open (every basic neighborhood D(f) of (2), f odd, contains (0)). Existing Spec defines the ambient topological space, not the distinguished subset indexed by f. The associated affine scheme Spec(R_f), sections M_f, an open covering and constructible Boolean combinations are related additional constructions, not identical needed meanings.

Uncertainty: Commutative-ring source conventions follow the existing scope deferrals; no theorem about source-attributed sheaf equivalences is certified.

### 18. ideal product IJ — `missing.e43d4f1922e210cc373a`

**contextual_ambiguity_or_variant; 6 / 6 parents.** Products are additive finite sums of factors ij with i∈I,j∈J; closure under left/right ring multiplication follows from the two-sided ideal axioms. Iterating gives positive powers, while I^0=R is an extra convention in the unital commutative contexts. IJ need not equal I∩J: in Z, (2)(2)=(4) whereas (2)∩(2)=(2); the purity parent imposes that equality as an extra test. Symbolic p^(n) is localization and contraction and is not ordinary p^n by definition. Five parents explicitly work in commutative-algebra/domain settings. However form.003cb1cc70cf5a2c.nilpotent-ideal, occ.6382ae14011d622d9352, has an identity-optional ring target and former candidate missing.28c2bfd6be87e9099167 with only Ring theory scope, whereas the canonical product requires commutative unital rings. Positive ideal powers also exist for nonunital rings: the nonzero zero-product C2 rng has I=R and I²=0. Thus the broader source reading is meaningful and is not covered as stated by the narrower canonical context. The construction is legitimate, but its alias scope needs adjudication; no generalization or split applied.

Uncertainty: Later source verification may establish a commutative-unital intended scope for the nilpotent source, or a separate review may justify broadening/splitting the candidate. Stored information alone does not choose either correction.; No existing alias is reversed; the exact general-vs-specialized scope question remains open.

### 19. I=ker(P→S) — `missing.fb78af5e23099cc8d59b`

**retain_distinct_missing; 6 / 6 parents.** All six parents take φ^−1({0}) for a commutative unital ring map. If a,b map to zero, so does a−b, and φ(ra)=φ(r)φ(a)=0; hence this subset is an ideal. This specializes generic set preimage, but the ideal structure and ring-map type are additional. A ring map is A-linear when B is viewed by restriction of scalars; its module kernel gives the underlying A-submodule, not a separately stored general kernel-ideal definition. The preadditive categorical-kernel meaning is an arrow with a universal property in an additive setting, not an ideal subset of a ring. Polynomial kernels need not be principal in general; only the minimal-polynomial parent imposes the field/univariate algebraic conditions making it monic-generated. A kernel need not be square-zero: ker(Z→Z/2)=(2), whose square contains 4≠0. Thus neither nilpotence nor a whole extension datum is included. For symbolic powers n=0 the quotient is the zero ring, making the kernel R if that quotient is permitted; it is not automatically proper.

Uncertainty: Commutative-unital source scope and whether zero targets are allowed remain explicit future source questions; no related candidate parents are counted reviewed merely by comparison.

### 20. direct sum ⊕_i M_i of a family of modules — `missing.134e1c9f45dd933fdc36`

**retain_distinct_missing; 5 / 5 parents.** The five sources use finite-support tuples with coordinatewise R-action. Given maps f_i:M_i→N, the formula (m_i)↦Σ_i f_i(m_i) is defined because the support is finite and uniquely extends the summand maps, proving the module-coproduct property. The existing general categorical coproduct gives a universal specification but not this stored concrete module construction; no identity with a whole diagram or graded algebra is inferred. For infinitely many nonzero summands, a tuple of nonzero entries lies in the product but not the direct sum. In a binary family sum and product coincide canonically, which does not justify an arbitrary-family merge. Tensor/Rees multiplications are additional; summands I^n are not required free, nor does countable generation of each summand make the whole index set countable. Free modules are the special case of copies of R; arbitrary modules can have torsion.

Uncertainty: A future population may relate this to the existing generic coproduct via a proven module instance, but that is not an automatic candidate-to-meaning identity resolution. Tensor side/unital conventions remain parent-specific.

### 21. intersection A cap U — `missing.170fcdda487b9180137e`

**retain_distinct_missing; 5 / 5 parents.** Four contexts directly use binary intersection: x∈A∩B iff x∈A and x∈B, independent of topology or probability. The fifth uses finite indexed intersection, obtained by iterating the binary operation; associativity follows from conjunction associativity. Its empty case is separately stipulated to be Ω, not recoverable from a binary operation without a chosen ambient set. Thus historical alias.global-audit.20261023.143 is legitimate only for the shared binary-operation prerequisite, not identity of a whole indexed family (including its empty case) with one binary pair. The stored parent explicitly supplies Ω and finite indexing, so these data need not be invented or dropped. The operation differs from subset relation (a truth value rather than an output set), Cartesian product (ordered pairs), and ideal product ((2)∩(2)=(2) but (2)^2=(4)). Nonempty subspace conventions do not prohibit empty intersections; disjoint nonempty subsets illustrate that distinction. No exact existing intersection construction was found in the checked set-theory meanings.

Uncertainty: Future occurrence-granularity documentation should preserve the explicit finite-index and empty-Ω data if the indexed-intersection alias is used; no mathematical equality of whole input packages is asserted.

### 22. difference A minus B — `missing.189a1049986dd4f651f4`

**retain_distinct_missing; 5 / 5 parents.** All five sources use A\B={x∈A:x∉B}; choosing first argument X gives the ambient complement. Changing X changes that complement, so there is no ambient-free absolute complement here. A\B need not equal B\A or symmetric difference: {0,1}\{1}={0}, while reversing gives ∅. Differences of open sets need not be open; their topology/measurability conditions stay in the constructible or sigma-algebra parents. Boundary uses closure minus interior, not A minus interior: in R, A=Q has closure R and empty interior, so its boundary R is larger than A. The second boundary formula instead takes closure of X\A before intersection; complement and closure are distinct operations. Existing nonstrict subset, interior, closure and sigma-algebra meanings do not define the generic binary difference operation as their needed meaning.

Uncertainty: Recorded excluded boundary source wording is not rehabilitated or externally checked; the stored independent formulas alone are reviewed.

### 23. commutative unital algebra over a field — `missing.3b37131115a06556c3e4`

**source_convention_deferral; 5 / 5 parents.** All five parents need a k-algebra input with a specified structure map, not just an abstract ring or a scalar-extended output. For a commutative unital algebra the chosen map k→A gives scalar multiplication c·a=φ(c)a and compatibility with multiplication; this extra data is not present in a bare commutative ring. A=k[T] is a k-algebra but not a field, and A=k[ε]/(ε²) is a k-algebra but is not reduced or a domain, separating the underlying type from the geometric tests. A field extension is narrower (A must itself be a field), while finite-presentation algebra imposes finite generators and relations. The existing unital ring-map meaning describes the structure arrow rather than the whole algebra object. However all five actual source texts say k-algebra, without independently spelling out commutativity and the unit axiom. Their commutative-algebra/ring-spectrum context supports the intended reading but does not independently certify external conventions. Retain the missing structured type and document precise source verification instead of declaring the specialized assumptions proved.

Uncertainty: Later reconcile for each of these five exact sources whether algebras are commutative and unital and whether zero algebra is allowed; this is a bounded source-scope deferral, not authorization for external lookup now.; The existing base-change-arrow links in geometric-normality parents provide a related construction; object/arrow granularity is not automatically resolved by this review.

Current totals: **199 distinct source formulations**, **252 candidate/parent visits**, **273 candidate occurrences**. Next: `missing.45359d317b7e3aba73da`, beginning with `form.05531f966e3a206f.prime-element`. All per-occurrence component flags are in the new ledger events; no whole-data identity is inferred from a component prerequisite.
