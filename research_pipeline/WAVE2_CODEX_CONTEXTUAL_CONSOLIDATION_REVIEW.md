# Wave 2 contextual consolidation review — proposed dispositions

Base: `0866fcaeaa06a4119992813a935cdba2c5f1a446` (latest main, PRs #4–#6).
Branch: `codex/wave2-contextual-consolidation-review`.

This report reviews exactly the 20 exhaustive consistency leads. It proposes
mathematical dispositions for ChatGPT adjudication; **none is entered into a
ledger or applied to the graph**. “Original” below means the stored independent
formulation/paraphrase, not a newly verified external source quotation. I read
each full formulation/context, its full effective adjacency and implicated
stored target definitions; source metadata for convention questions does not
contain the missing ambient convention. No external mathematical sources or
excluded corpora were consulted.

## 1. Scope and result

The existing exhaustive consistency and readiness CLIs both completed. The
snapshot still has 611 meanings, 659 complete scans, 421 canonical missing
identities and 844 missing occurrences; 19 mechanical checks pass, with no
integrity failures or unclassified/ambiguous/deferred references. There is one
formulation-avoidable metric/open-ball SCC, not an automatic defect. These
checks do not certify mathematics or finish Pass 2.

Inventory: `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`.
Unresolved pool: `61246db4cb0897ac3bfdb43f8a8e6be361e2f05bf905367bfbda0b388a541113`.
Readiness evidence: `8cfe7beca88081fe49f8458f2c952e4c3509cdb56467188b516d1d95b07e63fc`.

**Main distinction:** no unambiguous wrong-target replacement is established
merely by these 20 differing links. Many are valid dependencies at different
levels of structure. A concrete empty-family/FIP convention mismatch does need
adjudication (#1). Seven module cases and two ring/ideal cases leave an ambient
unitality question that the stored sentences alone do not decide. They may be
explicitly deferred as source/variant questions while retaining the separate
identities; they must not be silently declared equivalent or fully verified.

## 2. Shared module and ring reasoning

The general target `meaning.wave2.foundation.left-module-nonunital` requires an
abelian additive group and the two distributive laws and associative scalar
law, with unitality a separate condition. The specialized target
`meaning.wave2.module94.unital-left-module` additionally requires a ring with
identity and `1m=m`. Every specialized module is general; the converse is false.
For R=F₂ and M=C₂, define rm=0 for every r,m. All general axioms hold but
1·1_M=0≠1_M. This is a separating model derived from those axioms, not an admitted
new mathematical record. Its identity endomorphism is linear; its only
submodules are 0 and M; its annihilator is all R. It prevents several false
inferences of unitality from the source predicates below.

All eight module source observations are stored Stacks-attributed paraphrases.
That attribution and scan matching notes support an intended ordinary-module
reading but are not independent evidence of the external ambient conventions.
The preserved general seeds are valid under that reading. Conversely, one
must not infer module unitality just because the coefficient ring has 1.
The free-resolution case supplies an additional mathematical argument (#3).

The analogous ring issue in #12–#13 is separated by the additive group C₂ with
zero multiplication. This is a commutative associative rng with no identity;
its only ideals are 0 and R, hence it has a unique maximal proper ideal. Thus
“nonzero local” or “maximal ideal” does not itself prove a multiplicative unit.
The general two-sided-ideal target is still a correct forgotten-structure
prerequisite for the specialized commutative-unital maximal-ideal target.

## 3. The twenty findings

Numbers follow the exhaustive priority order. Every proposed correction or
annotation below is **not applied**. “No Pass 2 obstacle” is limited to that
specific target pair, not a proof that the whole formulation or corpus is correct.

### 1. `form.wave2.broad67.compact-closed-fip`

Context: General topology: compactness by finite open subcovers or closed-set finite intersection property; no Hausdorff assumption.

> Equivalently, X is compact if every family of closed subsets of X that has the finite intersection property has nonempty total intersection.

- `seed.00a94ab09cd5a879d962` → `meaning.wave2.foundation.topological-space` (preexisting_relation; relation `rel.wave2.broad68.02`).

**Disposition:** Justified ambient relationship; unresolved FIP convention (probable source/variant defect under the recorded convention).

A closed subset requires an ambient topology; the seed does not assert that a topological space IS a closed subset. The corrected scan separately preserves the predicate as missing.c4ed408b10943e9c0f8e (occ.2fb4cd2d7de4fa4994e4). Thus there is no demonstrated wrong target to remove. However the FIP candidate missing.ded806b239b007c8af8c (occ.28173daad7376ce1805d) explicitly tests only nonempty finite index sets. For X=∅ and the empty family, that test is vacuous, while the total intersection is X=∅. The stored open-cover alternative makes ∅ compact, so the displayed equivalence fails under that combination of conventions. No Hausdorff assumption fixes this.

**Pass 2:** Material: settle or explicitly quarantine the empty-family/FIP convention before endorsing this candidate interpretation in a global consolidation rationale.

**Proposal:** NOT APPLIED: keep both the ambient dependency and distinct closed-subset candidate. Choose either a nonempty-family qualification for this criterion, or an FIP convention including the empty finite intersection relative to X; alternatively state and separate a nonempty-space variant. These are not interchangeable silent edits.

**Further evidence/decision:** A convention decision using the stored FIP context and open-cover alternative; no new definition research is needed to exhibit the counterexample.

### 2. `form.3a0545450d7a5285.internal-hom-module`

Context: Module theory: internal Hom module of two R-modules.

> For modules M,N over a commutative ring R, the internal Hom Hom_R(M,N) is the R-module of R-linear homomorphisms M→N, with pointwise addition and scalar multiplication (r·f)(m)=r·f(m).

- `seed.52210d46da16614042f6` → `meaning.wave2.foundation.left-module-nonunital` (preexisting_relation; relation `rel.wave2.batch04.internal-hom-module.to.left-module-nonunital`).
- `occ.a1e476731c4866e84c7d` → `meaning.wave2.module94.unital-left-module` (scan).

**Disposition:** Unresolved mathematical/source-convention question; compatible general/specialized targets under the recorded unital reading.

For unital M,N the displayed Hom action is unital: (1·f)(m)=1·f(m)=f(m); forgetting that extra axiom gives the general module target. The seed and scan are then simultaneously legitimate. But the original sentence alone also describes Hom between general modules: for the zero-action C₂ modules in §2, the nonzero identity homomorphism has zero scalar action. The scan matching note “ordinary unital R-modules” records an interpretation, not a proof from the paraphrase.

**Pass 2:** No merger or new missing identity follows. A common unital-source convention or an explicit later-variant deferral is needed for unconditional source-scope acceptance.

**Proposal:** NOT APPLIED: retain both targets as distinct; later annotate a justified unital convention, or review a broader variant and its scan separately.

**Further evidence/decision:** Stored evidence has the same paraphrase, not an independent statement of the ambient module convention.

### 3. `form.788671763be693df.free-module-resolution`

Context: Homological algebra: free resolution.

> A free resolution of an R-module M is an exact augmented chain complex ⋯→F_2→F_1→F_0→M→0 with every F_i a free R-module.

- `seed.91685df62b437f79b8f9` → `meaning.wave2.foundation.left-module-nonunital` (preexisting_relation; relation `rel.wave2.batch04.free-module-resolution.to.left-module-nonunital`).
- `occ.d36f1fe57ea9143cf5c1` → `meaning.wave2.module94.unital-left-module` (scan).

**Disposition:** Justified general/specialized relationship.

The effective free-module prerequisite explicitly means a free module over a unital ring, a direct sum of copies of R; it does not require finite rank. Exactness at M makes the augmentation ε:F₀→M surjective. If m=ε(x), then 1m=1ε(x)=ε(1x)=ε(x)=m. Hence the recorded free-resolution context itself forces M to be unital, and the general-module seed is a valid forgotten-structure prerequisite.

**Pass 2:** No additional identity-consolidation decision for this target pair.

**Proposal:** None. Preserve both links, the free-module candidate missing.7462fa5f90275b34779a and its possibly infinite-rank context.

**Further evidence/decision:** No additional evidence for the pair under that explicitly recorded free-module convention; this is not a certification of the missing candidate definition.

### 4. `form.7ca4fb934b2f076c.r-derivation`

Context: Commutative algebra: derivation relative to a base ring.

> For a ring map R→S and an S-module M, an R-derivation D:S→M is an additive map vanishing on the image of R and satisfying Leibniz's law D(ab)=aD(b)+bD(a).

- `seed.63750086b2c653af6205` → `meaning.wave2.foundation.left-module-nonunital` (preexisting_relation; relation `rel.wave2.batch04.r-derivation.to.left-module-nonunital`).
- `occ.6a34f7aadb3cde3da64c` → `meaning.wave2.module94.unital-left-module` (scan).

**Disposition:** Unresolved module-convention question; not a demonstrated wrong target.

A unital S-module is also a general S-module, so both targets are legitimate in that domain. A unital ring map does not force its separate coefficient module to be unital. With R=S=F₂, the identity ring map, a nonzero zero-action C₂ module and D=0, all displayed derivation conditions hold but 1m=m fails. The additive-group target is only a prerequisite, not an identification of derivations with arbitrary additive maps.

**Pass 2:** Same common convention/deferral decision as #2; preserve both module identities.

**Proposal:** NOT APPLIED: make an eventual unital-context annotation explicit if adopted; do not automatically drop the general seed or declare the two module notions equivalent.

**Further evidence/decision:** Ambient coefficient-module convention, absent from the original paraphrase.

### 5. `form.a81a0fbec29f2186.finite-order-differential-operator`

Context: Commutative algebra: differential operator of finite order.

> For a ring map R→S and S-modules M,N, an R-linear map D:M→N is a differential operator of order at most k if k=0 and D is S-linear, or if k>0 and for every s∈S the commutator m↦D(sm)−sD(m) has order at most k−1.

- `seed.9f39fe8ba9eba9166d56` → `meaning.wave2.foundation.left-module-nonunital` (preexisting_relation; relation `rel.wave2.batch04.finite-order-differential-operator.to.left-module-nonunital`).
- `occ.dd3e9c3724ba10511f62` → `meaning.wave2.module94.unital-left-module` (scan).

**Disposition:** Unresolved module-convention question; resolved linear-map edge justified.

Over R=S=F₂ with zero-action M=N=C₂, the identity additive map is S-linear, hence an order-zero operator satisfying the source without unital modules. Under the recorded ordinary unital interpretation both module targets are correct. Separately, effective occ.880bb8e220b0d634d37f resolves candidate missing.61801675cc783a243555 to meaning.wave2.cross110.module-linear: restriction of scalars makes its general R-linearity definition exactly applicable. It does not claim S-linearity at positive order.

**Pass 2:** Common module-convention decision, not a new ambiguity in the resolved map identity.

**Proposal:** NOT APPLIED: retain the resolution, S-linear order-zero prerequisite and commutator distinction; address source convention only through an authorized annotation/variant review.

**Further evidence/decision:** Ambient module convention; the existing ring-map hypothesis alone does not supply it.

### 6. `form.a95feee56dc057ee.module-composition-length`

Context: Module theory: length of an R-module.

> The length of an R-module M is the supremum of integers n for which M has a strictly increasing chain of R-submodules 0=M_0⊊M_1⊊⋯⊊M_n=M, with infinity if the possible lengths are unbounded.

- `seed.0a6539c2cf972c80bd4f` → `meaning.wave2.foundation.left-module-nonunital` (preexisting_relation; relation `rel.wave2.batch04.module-composition-length.to.left-module-nonunital`).
- `occ.3c415c1dcd2223a932a2` → `meaning.wave2.module94.unital-left-module` (scan).

**Disposition:** Unresolved module-convention question; source predicate meaningful in either domain.

Strict submodule-chain length is defined for general modules as well as unital ones. A nonzero zero-action C₂ over F₂ has exactly the submodules 0 and M, so the displayed supremum is 1 without unitality. Therefore length does not force the scan’s narrower domain. Under an ordinary unital source convention both dependencies are correct. Strict chain length must not be conflated with number of generators or with a separately specified composition series.

**Pass 2:** Common convention/deferral decision only; no candidate identity merger.

**Proposal:** NOT APPLIED: document the intended domain rather than deleting a legitimate general prerequisite.

**Further evidence/decision:** Ambient module convention; no proof of it is present in the chain-length formula.

### 7. `form.a95feee56dc057ee.simple-module`

Context: Module theory: simple module.

> An R-module M is simple when M is nonzero and its only submodules are zero and M itself.

- `seed.d6dd03b6ee44a0637c24` → `meaning.wave2.foundation.left-module-nonunital` (preexisting_relation; relation `rel.wave2.batch04.simple-module.to.left-module-nonunital`).
- `occ.60680af4bd5b36bce5b7` → `meaning.wave2.module94.unital-left-module` (scan).

**Disposition:** Unresolved module-convention question with an explicit separating example.

The zero-action C₂ module is nonzero and has only submodules 0 and M, so it is simple by the displayed sentence but is not unital. Thus simplicity does not imply 1m=m. General and unital simplicity agree when evaluated inside the unital-module domain; that conditional agreement does not justify merging the module meanings or silently extending the source’s domain.

**Pass 2:** Common convention/deferral decision; preserve the nonzero condition and distinct module contexts.

**Proposal:** NOT APPLIED: make the eventual unital restriction explicit if chosen; otherwise review a general-module variant separately.

**Further evidence/decision:** The source’s coefficient-module domain, not another comparison of similar names.

### 8. `form.a9ca2e716ceffd36.annihilator-module`

Context: Module theory: annihilator ideal of a module.

> For an R-module M, its annihilator Ann_R(M) is the ideal consisting of r∈R for which r·m=0 for every m∈M.

- `seed.5220ded3fe72827abe0f` → `meaning.wave2.foundation.left-module-nonunital` (preexisting_relation; relation `rel.wave2.batch04.annihilator-module.to.left-module-nonunital`).
- `occ.0981932eff23bc1c6dd0` → `meaning.wave2.module94.unital-left-module` (scan).

**Disposition:** Unresolved module-convention question; general ideal dependency justified.

For any left module, if r annihilates M then (ar)m=a(rm)=0 and (ra)m=r(am)=0; Ann_R(M) is a two-sided ideal. No unital axiom was used. The zero-action C₂ module has Ann_R(M)=R, which is allowed by “ideal”; the source does not demand a proper ideal. Both module targets are legitimate if the unital domain is intended, but that narrower domain is not forced by the annihilator formula.

**Pass 2:** Common convention/deferral decision; no need to create a new annihilator or ideal identity.

**Proposal:** NOT APPLIED: retain the two-sided-ideal links and universal quantifier; annotate scope only after adjudication.

**Further evidence/decision:** Ambient module convention; no inference of unitality from the word “ideal”.

### 9. `form.f17ea18ebee0660f.module-regular-sequence`

Context: Commutative algebra: regular sequence on a module.

> A finite sequence f_1,…,f_r in a ring R is M-regular for an R-module M if f_i acts injectively on M/(f_1,…,f_{i-1})M for every i and the final quotient M/(f_1,…,f_r)M is nonzero.

- `seed.ce4ec6fb544194eab2d9` → `meaning.wave2.foundation.left-module-nonunital` (preexisting_relation; relation `rel.wave2.batch04.module-regular-sequence.to.left-module-nonunital`).
- `occ.a6fbba788de2ebfb517a` → `meaning.wave2.module94.unital-left-module` (scan).

**Disposition:** Unresolved boundary convention; conditional justification is stronger than lexical similarity.

If R has an identity and the sequence has positive length, injectivity of f₁ on M forces m=1m, because f₁(m−1m)=0. That supports the unital target under those hypotheses. The source does not itself state an identity or exclude the empty sequence. A genuine nonunital example is R=2ℤ acting by multiplication on M=ℤ: (2) is regular, since multiplication by 2 is injective and ℤ/2ℤ≠0. Thus the unital-ring/module domain cannot be inferred from the literal general-ring statement alone.

**Pass 2:** Document the ring and length conventions or explicitly defer their source-variant repair. Do not conflate injectivity, quotient module, zero module or ideal action candidates.

**Proposal:** NOT APPLIED: specify the chosen unital/positive-length context if warranted; do not silently exclude other source readings.

**Further evidence/decision:** The ambient ring convention and whether r=0 is permitted.

### 10. `form.wave2.real50.dedekind-rational-lower-cut`

Context: Real construction from Q: nonempty proper lower set without greatest element.

> A (lower) Dedekind cut of the rational numbers is a subset A of Q such that A is nonempty, A is not all of Q, if a belongs to A then every rational q<a also belongs to A, and A has no largest element.

- `seed.1bc4d429daa76d1d5238` → `meaning.wave2.foundation.subset-proper` (preexisting_relation; relation `rel.wave2.real53.01`).
- `occ.85b8e6f623ea12a5b553` → `meaning.wave2.foundation.subset-nonstrict` (scan).

**Disposition:** Justified general/specialized relationship.

The source explicitly asserts A⊆Q and A≠Q. These are exactly the stored proper-subset definition, which implies the nonstrict-subset definition. Nonemptiness and absence of a greatest element remain additional cut conditions, not part of either generic inclusion relation.

**Pass 2:** No remaining identity ambiguity in this pair; strict and nonstrict inclusion must remain distinct.

**Proposal:** None. Both links are warranted, although redundant for expansion.

**Further evidence/decision:** None for this pair; no claim that every downset is a Dedekind cut.

### 11. `form.5b29c5555567bd3d.cohen-macaulay-locus`

Context: Commutative algebra: Cohen–Macaulay locus of the spectrum.

> For a Noetherian ring S, the Cohen–Macaulay locus of Spec(S) is the set of prime ideals q for which the local ring S_q is Cohen–Macaulay.

- `occ.a74b6ebfa462a21e5b04` → `meaning.4f7edb6d32334f67.local-ring-unique-maximal` (scan).
- `occ.8d34bb1f21102ece5f48` → `meaning.70f44988651b76b5.ring-localization-at-multiplicative-set` (scan).

**Disposition:** Justified construction/property dependencies.

S_q means localization at the multiplicative set S∖q. The resulting ring is local, with maximal ideal qS_q: an element with numerator outside q is invertible, and the others form that ideal. Hence both the localization construction and local-ring property are used. The effective Noetherian-ring and prime-ideal meanings supply the recorded commutative-unital setting; Cohen–Macaulayness is tested on this local ring. The source does not assert the locus is automatically open.

**Pass 2:** No consolidation obstacle; localization is not being declared equivalent to locality for arbitrary multiplicative sets.

**Proposal:** None. Keep both targets and the separate Cohen–Macaulay predicate.

**Further evidence/decision:** None for the flagged pair; the locus’s other mathematical properties are outside this bounded review.

### 12. `form.90b0d1ecfa394230.jacobson-radical-ring`

Context: Commutative algebra: Jacobson radical.

> For a commutative ring R, its Jacobson radical Jac(R) is the intersection of all maximal ideals of R.

- `seed.1d736ae604b5cce7e231` → `meaning.wave2.foundation.two-sided-ideal` (preexisting_relation; relation `rel.wave2.batch04.jacobson-radical-ring.to.two-sided-ideal`).
- `seed.8c53137dbe461ec02892` → `meaning.wave2.foundation.commutative-maximal-ideal` (preexisting_relation; relation `rel.wave2.batch05.jacobson-radical-ring.to.commutative-maximal-ideal`).

Additional effective references: `occ.bc158c586425f2f6670f` → `meaning.wave2.foundation.commutative-maximal-ideal`; `occ.b3a50714a8d66ba81682` → `meaning.wave2.foundation.associative-ring-identity-optional`.

**Disposition:** Justified general/specialized ideal pair, with unresolved ambient ring convention.

Every maximal ideal of a commutative unital ring is a two-sided ideal, so retaining both historical seeds is correct in that setting. Maximality/properness is supplied by the specialized target, not by the general ideal definition. However the source merely says commutative ring and its effective ring reference explicitly permits no identity. The zero-product rng C₂ in §2 is nonzero, commutative and has maximal ideal 0 without an identity. Thus the unital setting of the specialized target is not logically forced by the source’s ring reference.

**Pass 2:** No evidence for merging the ideal notions. The shared ring-convention issue needs an explicit scope/deferral disposition, not automatic rejection of the generic seed.

**Proposal:** NOT APPLIED: annotate commutative-unital scope if adopted, or separately review a rng variant. Do not confuse Jacobson and nil radicals or change the empty-family-intersection convention.

**Further evidence/decision:** Ambient ring convention; a source locator alone does not settle it.

### 13. `form.4f7edb6d32334f67.local-ring-unique-maximal`

Context: Commutative algebra: local ring.

> A nonzero commutative ring R is local if it possesses exactly one maximal ideal.

- `seed.ccd4fd6c2b216322b95a` → `meaning.wave2.foundation.two-sided-ideal` (preexisting_relation; relation `rel.wave2.batch04.local-ring-unique-maximal.to.two-sided-ideal`).
- `seed.ba44141a846c25049d90` → `meaning.wave2.foundation.commutative-maximal-ideal` (preexisting_relation; relation `rel.wave2.batch05.local-ring-unique-maximal.to.commutative-maximal-ideal`).
- `occ.275dd8176f384c525f41` → `meaning.wave2.foundation.commutative-maximal-ideal` (scan).

Additional effective reference: `occ.2f50943b9d900a46bbce` → `meaning.wave2.foundation.associative-ring-identity-optional`.

**Disposition:** Justified ideal specialization, with unresolved ambient ring convention.

In a commutative unital local ring the unique maximal ideal is also a two-sided ideal, so all three implicated edges are legitimate. But “nonzero, commutative, exactly one maximal ideal” alone does not prove existence of a ring identity: the zero-product rng C₂ has only ideals 0 and R and hence exactly one maximal ideal. The effective optional-identity ring link makes this a real scope question, not a lexical discrepancy.

**Pass 2:** Same convention/deferral class as #12. Preserve distinct maximal and general ideals.

**Proposal:** NOT APPLIED: state a unital local-ring convention if adopted; do not automatically remove a correct forgotten-structure edge.

**Further evidence/decision:** An explicit ambient convention is needed before accepting the specialized target as covering every literal reading.

### 14. `form.39488f3e396a1c77.algebraically-closed`

Context: algebraically closed.

> A field K is algebraically closed precisely when it has no proper algebraic field extension; equivalently, each nonconstant one-variable polynomial with coefficients in K admits a root in K.

- `seed.b62ac2743761d11f12a4` → `meaning.d0a078e59e1495da.algebraic-field-extension` (preexisting_relation; relation `rel.stage5.algebraically-closed.to.algebraic-field-extension`).
- `occ.cdda6422e12484d1673a` → `meaning.50d335de00e5f11d.algebraic-extension` (scan).

**Disposition:** Justified coextensive definitions, without authorizing an identity merge.

The two actual target definitions both quantify over every element of a field extension and require a nonzero base-field polynomial vanishing on it; changing E/F to K/k changes no condition. Neither requires finiteness of the extension. Therefore the prohibited proper algebraic extensions in the source can use either prerequisite. “Proper” is supplied separately; the claim does not prohibit arbitrary transcendental extensions.

**Pass 2:** No further resolution of the flagged link pair is needed; any source-preserving meaning reconciliation is a separate task.

**Proposal:** None. Keep both source identities and provenance.

**Further evidence/decision:** None for the equivalence of these stored mathematical predicates.

### 15. `form.1be2fa074ef447b0.i-adic-completeness`

Context: Commutative algebra: I-adically complete module or ring.

> An R-module M is I-adically complete when its canonical map M→lim_n M/I^n M is an isomorphism; a ring R is I-adically complete when it has this property as its own module.

- `seed.23e06201e7e86b2a62fb` → `meaning.1be2fa074ef447b0.i-adic-module-completion` (preexisting_relation; relation `rel.stage5.i-adic-completeness.to.i-adic-module-completion`).
- `occ.7589fdbee7d57352762e` → `meaning.8d61300dcabf30c0.inverse-limit-sequence-modules` (scan).

**Disposition:** Justified general construction and its specialization.

The completion target is explicitly the inverse limit of the quotient tower M/IⁿM; the other target defines compatible tuples in an arbitrary countable inverse system of modules. The natural quotient maps supply the transition maps here. Completeness is the canonical map being an isomorphism to that object, not a claim that every module equals its completion. The seed and scan therefore name different levels of the same construction legitimately.

**Pass 2:** No identity-consolidation obstacle; ideal powers, ideal action IⁿM and quotient M/IⁿM remain distinct prerequisites.

**Proposal:** None. Do not merge general inverse limits with I-adic completions or erase either dependency.

**Further evidence/decision:** None for this pair under the recorded unital module context.

### 16. `form.50d335de00e5f11d.galois-extension-review`

Context: Field theory: Galois field extension.

> An algebraic extension K/k is Galois precisely when it is both separable and normal over k.

- `seed.de25075296fd1732f045` → `meaning.720eaae9156f6f4e.separable-algebraic-field-extension` (preexisting_relation; relation `rel.stage5.galois-extension-review.to.separable-algebraic-field-extension`).
- `occ.7685c282e79846365e74` → `meaning.50d335de00e5f11d.separable-algebraic-extension` (scan).

**Disposition:** Justified coextensive separability prerequisites.

One target says every element of an algebraic extension is separable; the other says each minimal polynomial has no repeated root. The stored separable-element definition reduces to separability of the minimal polynomial, and the stored separable-irreducible-polynomial definition explicitly gives the no-repeated-root equivalence. Thus this is definitional expansion, not a name-based merge. Normality is a separate required conjunct; no finite-extension assumption is introduced.

**Pass 2:** No additional consolidation question for the flagged pair.

**Proposal:** None. Preserve both provenance identities and the separate normality links.

**Further evidence/decision:** None for these stored definitions; this does not certify the original external sources.

### 17. `form.5a7f5216e916198b.separably-generated-extension`

Context: Field theory: separably generated extension.

> A field extension K/k is separably generated if there exists a transcendence basis B⊆K over k such that K is a separable algebraic extension of the rational-function field k(B).

- `seed.e3a1b4fc9017f56e7fd1` → `meaning.720eaae9156f6f4e.separable-algebraic-field-extension` (preexisting_relation; relation `rel.stage5.separably-generated-extension.to.separable-algebraic-field-extension`).
- `occ.4ccc5f0a5037fdd04e80` → `meaning.50d335de00e5f11d.separable-algebraic-extension` (scan).

**Disposition:** Justified same separability criterion over the specified base field.

The comparison in #16 applies with base field k(B), not with k indiscriminately. The source requires existence of a suitable transcendence basis and K algebraic separable over k(B). Both target definitions express that same algebraic separability test. The rational-function-field candidate remains distinct from a transcendence basis or a general field-generation operation.

**Pass 2:** No further resolution of this target pair; do not infer a statement about every transcendence basis or merge candidate identities.

**Proposal:** None. Retain the existential qualifier and both separability references.

**Further evidence/decision:** None for the target pair in its actual k(B) context.

### 18. `form.3718becace9c852d.quasifinite-at-prime`

Context: Commutative algebra: quasi-finite ring map at a prime.

> Let R→S be a finite-type ring homomorphism and q∈Spec(S) lying over p∈Spec(R). The map is quasi-finite at q if q is an isolated point of the fibre Spec(S⊗_R κ(p)); equivalently its local fibre has dimension zero.

- `seed.0b9830e59753a4875337` → `meaning.3fcd082413a6b2eb.relative-dimension-at-prime` (preexisting_relation; relation `rel.stage5.quasifinite-at-prime.to.relative-dimension-at-prime`).
- `occ.b6871a1b24a78a9908d9` → `meaning.bd90654fb341045a.local-krull-dimension-point` (scan).

**Disposition:** Justified specialized/generic local topological dimension targets.

The relative-dimension target explicitly means local TOPOLOGICAL dimension at q in Spec(S⊗_Rκ(p)); the generic target defines the same local topological invariant as min dim(U) over open neighbourhoods. Thus both apply. Neither is the dimension of the local fibre RING. For example at the generic point of the affine line over ℚ the local ring ℚ(t) has dimension 0, but every open neighbourhood contains a closed point specializing from the generic point and has topological dimension 1; that point is not isolated.

**Pass 2:** No consolidation obstacle in this pair. Preserve the whole scheme fibre, its point and local-topological dimension distinctions.

**Proposal:** None. Never replace these by local-ring dimension merely because the word “local” matches.

**Further evidence/decision:** None for the flagged target relation; the example explains the forbidden substitution, not a new claim of source certification.

### 19. `form.wave2.foundation.group`

Context: Abstract group, with a two-sided identity and inverses; arbitrary binary operation.

> A group is a set G with a binary operation *: G×G→G such that (a*b)*c = a*(b*c) for all a,b,c∈G, an element e∈G satisfies e*a = a = a*e for each a∈G, and every a∈G has b∈G with a*b = e = b*a.

- `seed.12c128de075b6a5cf827` → `meaning.wave2.foundation.monoid` (preexisting_relation; relation `rel.wave2.batch07.06`).
- `seed.f8ecf5102f92847392a9` → `meaning.wave2.foundation.binary-operation-internal` (preexisting_relation; relation `rel.wave2.batch07.07`).

**Disposition:** Justified structured prerequisite; imprecise edge caption is not a false mathematical target.

The complete source provides an internal operation, associativity and a two-sided identity before requiring inverses. Forgetting inverses therefore gives precisely a monoid. The internal-operation target supplies the operation alone. A generic binary operation is not a monoid, but this parent defines a group, not an arbitrary operation: the implication uses its full axioms. The separate associativity/identity/inverse candidates do not make the monoid dependency invalid.

**Pass 2:** No identity-consolidation obstacle. Do not identify monoids with internal binary operations.

**Proposal:** NOT APPLIED: optional later caption clarification (“underlying monoid structure”) could improve precision; no target replacement or deletion is mathematically compelled.

**Further evidence/decision:** None for the structured dependency; exact phrase matching is not the semantics of definition_uses.

### 20. `form.83a528850cdf6a59.submersive-continuous-map`

Context: Topology: submersive map.

> A continuous map f:X→Y is submersive if it is surjective and Y has the quotient topology for f; equivalently, U⊆Y is open exactly when f^{-1}(U) is open in X.

Source-level finding: occurrence ID is null. Implicated effective references:

- `seed.21f009ae19271df58e41` → `meaning.wave2.foundation.topological-space` (preexisting_relation).
- `occ.0ec9501754d125839f1b` → `meaning.wave2.foundation76.continuous-topological-map` (scan).
- `occ.979df121e1ebce753534` → `meaning.wave2.foundation.subset-nonstrict` (scan).
- `occ.43968d7dad348d26b30a` → `missing.c8a3e68d130a4f68d108` (scan).
- `occ.7c831677fac9d2e6a690` → `missing.0c5a27f2980fc722cbb5` (scan).
- `occ.9579906f9d75f0731487` → `missing.b86257b3cce62907e97e` (scan).
- `occ.f782a69df2d320b3e145` → `external defining condition` (scan).

**Disposition:** Later-phase wording/source-scope issue; no demonstrated wrong target.

The preimage-open biconditional does not imply surjectivity. The inclusion of a one-point discrete space into a two-point discrete space satisfies it for every subset of Y and is continuous, but is not onto. The source’s first clause separately requires surjectivity, and effective references preserve both that identity and a quotient-topology candidate explicitly defined for a surjection. Read with surjectivity retained, the characterization is correct; read as a replacement of the whole preceding clause, “equivalently” drops a necessary condition.

**Pass 2:** No new candidate-identity ambiguity: retain missing.c8a3e68d130a4f68d108 (surjectivity) separately from missing.0c5a27f2980fc722cbb5 (quotient topology). Record a later wording disposition.

**Proposal:** NOT APPLIED: clarify “equivalently, f is surjective and U is open iff f⁻¹(U) is open.” Do not silently discharge surjectivity from the biconditional.

**Further evidence/decision:** Source-scope adjudication of the ellipsis; no external lookup was performed.

## 4. Target-definition checks and exact anchors

The target readings used above are the stored definitions, not just their
labels. The common module pair is detailed in §2. Other flagged targets are:

- `meaning.1be2fa074ef447b0.i-adic-module-completion` (Commutative algebra: I-adic completion of a module): For an R-module M and ideal I⊆R, the I-adic completion of M is lim_n M/I^n M; its elements can be viewed as mutually compatible residue classes modulo powers of I.
- `meaning.3fcd082413a6b2eb.relative-dimension-at-prime` (Commutative algebra: relative dimension of a finite-type ring map at a prime): For a finite-type ring map R→S and prime q of S lying over p in R, the relative dimension at q is the local topological dimension at the corresponding point of the fibre Spec(S⊗_R κ(p)).
- `meaning.4f7edb6d32334f67.local-ring-unique-maximal` (Commutative algebra: local ring): A nonzero commutative ring R is local if it possesses exactly one maximal ideal. Equivalently, a nonzero commutative ring R is local if the set of its nonunits is an ideal; this ideal is necessarily the ring's unique maximal ideal.
- `meaning.50d335de00e5f11d.algebraic-extension` (Field theory: algebraic field extension): An extension K/k of fields is algebraic if every element α∈K satisfies a nonzero polynomial with coefficients in k.
- `meaning.50d335de00e5f11d.separable-algebraic-extension` (Field theory: separable algebraic extension): An algebraic extension K/k is separable if the minimal polynomial of each α∈K has no repeated roots over an algebraic closure of k.
- `meaning.70f44988651b76b5.ring-localization-at-multiplicative-set` (Commutative algebra: ring localization at a multiplicative subset): Given a commutative ring R and multiplicative subset S⊆R, the localization S^{-1}R is the ring of fractions r/s modulo (r,s)∼(r′,s′) if t(rs′−r′s)=0 for some t∈S.
- `meaning.720eaae9156f6f4e.separable-algebraic-field-extension` (Field theory: separable algebraic extension): An algebraic extension E/F is separable if every element of E is separable over F.
- `meaning.8d61300dcabf30c0.inverse-limit-sequence-modules` (Module theory: inverse limit of a countable module system): The inverse limit of an inverse system ⋯→M_3→M_2→M_1 is the submodule of ∏_{n≥1}M_n consisting of compatible tuples (m_n), so φ_n(m_n)=m_{n−1} for every n≥2.
- `meaning.bd90654fb341045a.local-krull-dimension-point` (Topology: local Krull dimension at a point): For a point x in a topological space X, the local Krull dimension dim_x(X) is the minimum of dim(U) over all open neighbourhoods U of x.
- `meaning.d0a078e59e1495da.algebraic-field-extension` (Field theory: algebraic extension): A field extension E/F is algebraic if every element of E satisfies at least one nonzero polynomial with coefficients in F.
- `meaning.wave2.foundation.binary-operation-internal` (Internal binary operation closed on a set): An internal binary operation on a set S is a function ⋆:S×S→S, assigning to each pair (a,b)∈S×S a uniquely determined element a⋆b∈S.
- `meaning.wave2.foundation.commutative-maximal-ideal` (Commutative algebra: proper maximal ring ideal, not a general noncommutative maximal left or right ideal): Let R be a commutative ring with identity. An ideal m of R is maximal if m is properly contained in R and every ideal J with m⊆J⊆R satisfies J=m or J=R.
- `meaning.wave2.foundation.monoid` (Algebra: associative internally closed operation with two-sided identity): A monoid is a pair (M,⋆) consisting of a set M and an operation ⋆:M×M→M for which (a⋆b)⋆c=a⋆(b⋆c) for all a,b,c∈M and some e∈M satisfies e⋆a=a=a⋆e for every a∈M.
- `meaning.wave2.foundation.subset-nonstrict` (Set theory: non-strict subset relation for sets): For sets A and B, A is a subset of B, written A⊆B, if and only if for every x, x∈A implies x∈B. Equality A=B is allowed in this non-strict inclusion relation.
- `meaning.wave2.foundation.subset-proper` (Set theory: strict set inclusion requiring inequality): For sets A and B, A is a proper subset of B, written A⊊B, if and only if A⊆B and A≠B. Equivalently, every member of A belongs to B and at least one member of B does not belong to A.
- `meaning.wave2.foundation.topological-space` (Open-set axioms for arbitrary topological spaces, including the empty space): A topological space is a pair (X,τ) with τ⊆P(X) such that ∅∈τ and X∈τ, any union of members of τ is in τ, and intersections of finitely many members of τ are in τ. Members of τ are the open subsets of X.
- `meaning.wave2.foundation.two-sided-ideal` (Two-sided ring ideal; multiplication need not be commutative): Let R be a ring. A subset I⊆R is a two-sided ideal if (I,+) is an additive subgroup of (R,+) and, for every r∈R and i∈I, both ri and ir belong to I.

For #16–#17 I also read `form.720eaae9156f6f4e.separable-algebraic-element`
and `form.720eaae9156f6f4e.separable-irreducible-polynomial`: the former uses
separability of the minimal polynomial; the latter explicitly equates that
with no repeated root. For #1 the other stored compactness formulation,
`form.wave2.broad67.compact-open-cover`, quantifies over all open covers without
a nonempty-space restriction. No implicated seed override removes a link
listed above. Effective aliases and candidate resolutions were inspected;
notably the resolved linear-map edge in #5 and the closed-subset alias in #1
are retained in this reasoning. A stale original node was never used as the
current adjacency.

The following exact hashes anchor each entry to its full original source,
effective node and worklist evidence (not merely the selected phrase):

| # | Source version SHA256 | Effective node SHA256 | Worklist evidence SHA256 |
|---|---|---|---|
| 1 | `e6a0aa44634543ff92c50272643e6d7a42152bc50827bbbd925d745849f036bb` | `101ea433c98c87cacaaa5ed473300ed2484699fa8134b14fc57185df57c6f8d8` | `41eb31e3b57ed67f1b3ccf267d65f486c9ac82e8851064f899f5bd1eb025e0df` |
| 2 | `f5b90dc34ea1acc534f01c7bf3695afc7b6766ad777d10676407d9dab5ea9d68` | `0d9e50ced317d0a66a419ce17ffbc24ec46de14a35de3e5ecb5952aca3fe5be7` | `7a1ac45f36d4ecc8d46d5af0e4d460f184734831669b101ac27e106f6da68022` |
| 3 | `88a708c984d789bedcc946d7acbcd0a03e0006ca5257c33843a19c4507b44e59` | `ba40832d3a57e2e5ee013410fc417ed2dfbafd1c2c058a9155351b2462525fac` | `805a7ed34a7f436f53f50cf801398c83071dc780c51be1370dffc8b3c7d4a748` |
| 4 | `2dbf3b841e56c8eb839114478d1bd4a3cdeaf0fd39103a3eadc9acc82449812b` | `227984c66fd4f5c8aa488616bd9dba4c4f514c34e85803a21c741c055da7c375` | `a9bbdefa6c305bbf4498c4a95d4dd46f352676165a811509520a3d1ce9789433` |
| 5 | `ee0ba0c53bc6f2a9a0b4b138ef37f6ae28530ccd1a66c12d473aae9864f781c1` | `62a1d2d291857eb5318cf5f24f3389eded858689c9ff04aa1e5d8a4de622261f` | `bc83f600d8df00ae739f946cafbcec9c3bd79bb595f30c98e7d8e1915957e1eb` |
| 6 | `d95787bfb25535f991348f4ad229fb7b3ad4190b4dd00ea24ef705a34df03fda` | `9b3627702a8ebb009bf9da622c826aa47dfbc48f007625efe35db87d469a394e` | `76bee95272cdf207aea50cc579e6ec88a50de5fde7de2b63ddaf2968b9ce0ebc` |
| 7 | `fad21109abfb5ea66a1e726ca6a9d9b24c639ed5d3ac766bb1117846013e4987` | `c51bb69847756b2989b57ca6d98969c7fd7783624a8b271d4f8b3e7da8fbd89c` | `c1765245a48c23b01b067cb7937b77586ba5466d7524ec603a62c787d8c505a9` |
| 8 | `184188a161e5cd675e3d697cfd8efe2d0a32244fa26cf33bf2e648345c441010` | `f8c513ece709f4242383ec83e86cbcb4415e6a9a652e6c9a3dcbcdefee2306b8` | `40f99ee113019b6f5a17c04b314ee221901a88f2f75d77b16658963b4b52455c` |
| 9 | `e5ee3c048684bccf3ddd2ccfe9982d2294c38ce17661140d1d3a175b31be531b` | `4a8e9cf64f080591322f0a405408d023e995e147948fd00c7f94d463bbff58d5` | `fa45186671d5a2ca1f3e80f1dec851b38ea4222368f192cef75c60537c46d1da` |
| 10 | `dea9312905342edf7bc6492d5e007ed6b0938225ca9f3378e7f886288507a90b` | `2825da4364ac63fd18bfe8bfaa19d4eb02895981f3a7fbbe4466dd110cfa5b01` | `bab623b4ca751919c505d3e8892c9d84cec51af918425c844f84928b266ad4b2` |
| 11 | `6480d0c86963c9861b36567623119e4f23403e011eae6812a55eeb235358444f` | `3a4f645d351fc41f372acc8717d7bf1a0dddfbf25d2c73ac5cc72c7218e8741e` | `b1599bebe09a455f6d400aca298c9ffdef16b710533c8db16a98dc7d432f3efa` |
| 12 | `b981170a4c32a8676a3efc4d4967e668e1dda45a749f12c23fa26e67b6d3ce9a` | `ebfa00fb65b6b054f0f53f0cdd2322db23bbade63a13e1f48f115a1615e7ee3d` | `3708fdacd805b814f28ffb484581c6c104ec6aaf513ba8023e5dd7f8aac9238e` |
| 13 | `5d0331628a7d0eaeb1ccd61f659b5d67c4820babc4782765fc29fb7e9c4214e9` | `b6f42df90467cda76bc35ee0fcd84c190464234bc446a192131c3f3bbe941a23` | `13d41782903ccb85e7de62565f582b29e6adab11a09899a98a6a7ce931b80e78` |
| 14 | `f2868734ceed08ebd1ed168fad5f16308608bc30f190a14eba73afbce9630a34` | `46e672bd63d6866c2661d6c777b9f6f78c6b8a92f94cc854ce63e99eb7bb2979` | `4c93a413d1830342df3b942a6e3afc59c53c57985ce119823a2e1b7b84de6fed` |
| 15 | `a374648a4acf14117a98135079658cf2a521bdbb5abd3c37b954b406e92cc73f` | `b42fbed7ca21a724195bd74953e78f1a756e1a1148801b0f8225cb83874990fc` | `d113053cdc4acd5cbda33de9661dcaeabea046b8785968717c8a5f1cb7e4f3a6` |
| 16 | `604ba90f6ca5e1c829eb9e157356a93dfce56848ce704f714ff567ea6504fd22` | `c327689a04499e86821db13f6d2b42a0734b605d6b734a525c3b4fa97621e19a` | `f940448c3117a9ba098893cf6d25fc7c22a2afc6ac0d7feb473edd9fe3427b06` |
| 17 | `0d16ca5bf92c50d07ef6675419ff7061dfa37401cd4b45aafb3d2c9f5a12a565` | `1a7d4bc5e1737ab137f232cc9b6bad35bc7d3721857f76fd398d4473d180ab89` | `96a6044e7bea9d1c76641ebc77163d9bee8962914fad9e83fb4d17ce0f8b37d2` |
| 18 | `bb42d9415ad7e72f4f29336e25f35d9c66ee68c9dad870e2a7bf6f40fedecf60` | `969a6beb2e4987cf703233c0b755af0744c9dea3ea47c3dda7ce0bd28eaec7e0` | `6c688c7fee7afa4b87d7d4099ad431059794295c70e17cf871ce46b655c6460b` |
| 19 | `7ed1ebeed29d21b555cca7e8560b35487bd97989be7129aa366469a58d9ea6c6` | `7c4b8a312b2db86ac03f84c966b121f92a7ea6b18f42dd7c6f7ab0b3f66a4eef` | `0c6486af3cdb7a4e732ce313076b92b81766f4dab6c9f0acdb0437cded69e251` |
| 20 | `1620373fbacadf98c746265b93e795858111ec79dac3aeb43f8185ec7dab2be1` | `cb15bafec225b3b7911725dc83d18c943304ba7fe58f97e21be114e1deda8dec` | `9dbf690e010ddb20ccf4f46660431889f933d794d424941110eeaa77d4a50041` |

## 5. Four provisional source issues and topological algebra

These are proposals for later source reconciliation, not adopted deferrals or
new automatic gate requirements. External webpages were not fetched: the issue
records report source discrepancies that remain unverified here.

### `issue.wave2.pop140.pairwise-proofwiki-quantifier`

`form.wave2.pop140.pairwise-independent` — context: Probability theory: pairwise but not necessarily jointly independent indexed measurable events.

> Let (Aᵢ)_{i∈I} be measurable events on one probability space. The family is pairwise independent if for every i,j∈I with i≠j, P(Aᵢ∩Aⱼ)=P(Aᵢ)P(Aⱼ). This does not in general imply joint independence for three or more events.

Source version: `186ea4d23a63592d582889dea31ec8ccfab4faff2a4253eb4ea7584600a045e1`.

The stored draft correctly restricts to i≠j. Allowing i=j would force p=p² and exclude events with probability 1/2, so the index restriction is substantive. Preserve pairwise versus joint independence; later verify the reported source typo. No current identity correction is demonstrated. **Pass 2:** later-source/variant disposition is defensible if recorded explicitly; no promotion or source correction is authorized. Issue-record SHA256: `d8e11834c5d81a95bc30ebfb4e4ccc6bdddddfeb00ad88027550889d5753592f`.

### `issue.wave2.pop141.eom-outer-measure-convention`

`form.wave2.pop141.outer-measure-full` — context: Measure theory: extended nonnegative outer measure on the full power set of an arbitrary set X.

> Let X be a set. A function μ*:𝒫(X)→[0,+∞] is an outer measure on X when μ*(∅)=0, A⊆B implies μ*(A)≤μ*(B), and μ*(⋃_{n=1}^∞ Aₙ)≤∑_{n=1}^∞ μ*(Aₙ) for every sequence (Aₙ) of subsets of X.

Source version: `3b05f7d3ee653a69a010d9fe6d918cec433b804acde6c0195373b73077407196`.

The draft explicitly uses the full power set, monotonicity and countable subadditivity. A hereditary-σ-ring domain is a different scope; the issue record does not prove that its other axioms recover exactly this definition. Retain both convention questions and do not alias them by name. Later reconcile source axioms and domains; no current draft repair is justified here. **Pass 2:** later-source/variant disposition is defensible if recorded explicitly; no promotion or source correction is authorized. Issue-record SHA256: `7ef60c4411734a5d0ce9c111b7327f56b292b7d6d16a287fb4c8ae407b7ff1d6`.

### `issue.wave2.pop142.bounded-quantifier`

`form.wave2.pop142.bounded-linear` — context: Functional analysis: linear map X→Y between real or complex normed spaces with one global bound.

> Let X,Y be normed vector spaces over the same field F∈{ℝ,ℂ} and T:X→Y a linear map. T is bounded if there exists a real M≥0 such that ||Tx||_Y≤M||x||_X for every x∈X.

Source version: `a2e01a69301a8da098747643fd6374876c013749c73d4103d671b2daba43c154`.

The draft correctly chooses one global M before quantifying x. Pointwise ∀x∃M_x would hold for every linear map (choose a norm ratio at each nonzero x), so it cannot express boundedness. Explicit model: on finite-support sequences with sum-absolute-value norm, T(x)_n=n x_n is linear, yet ||Te_n||=n. Preserve the corrected global quantifier and defer verification of the reported source discrepancy. **Pass 2:** later-source/variant disposition is defensible if recorded explicitly; no promotion or source correction is authorized. Issue-record SHA256: `460155feeea600160eeda62bd22f39ff5b10861edc36c648ecec0432b4551eda`.

### `issue.wave2.pop142.operator-norm-codomain`

`form.wave2.pop142.operator-norm-inf` — context: Functional analysis: operator norm on real/complex bounded linear maps between normed spaces.

> For bounded linear T:X→Y between real or complex normed spaces, equivalently ||T||=inf{M>0 : ||Tx||_Y≤M||x||_X for all x∈X}, with infimum taken in [0,+∞].

Source version: `0bbcff1d4d64e47568f6c145d0366b82fecc348f13c4ceb849475ffd77f8b0e0`.

The draft correctly measures Tx in Y. For T:X→Y, Tx need not belong to X at all (take X=ℝ and Y=ℝ²), so a general ||Tx||_X expression is ill-typed. This does not invalidate the stored infimum formula: for the zero map inf over positive bounds is still 0. Keep the quarantined source variant for later verification. **Pass 2:** later-source/variant disposition is defensible if recorded explicitly; no promotion or source correction is authorized. Issue-record SHA256: `2ddcb37b919934b307733b286bbf48cbe1959ed117638749a6e9b8ec5c01de5d`.

### Topological ring/module convention (Round183 retained)

`form.646e4dcbd9b6f1e1.topological-ring`:

> A topological ring is a ring R with a topology for which its addition R×R→R and multiplication R×R→R are continuous maps.

Version `03f497391324c755234793649bde87ad83ea94dc581a2ee3637168e25e5fa14d`; effective node `19a9859a9ad8569712edaf656a2950c3aefc09f46aebb1b9f0f52fa1a70a9df8`.

`form.646e4dcbd9b6f1e1.topological-module`:

> Given a topological ring R, a topological R-module is an R-module M endowed with a topology such that addition M×M→M and scalar multiplication R×M→M are continuous.

Version `0760928492e0ac3367e6d3c68783c325a204a8da9f76c4d167973eb79934ba7d`; effective node `fe08819042c9d6879af14becfd4de6853429f6b9766e6ce13fd9d44ed84f414f`.

The ring occurrence `occ.833660ecb99c1dd64abd` targets
`meaning.wave2.foundation.associative-ring-identity-optional`; the module
occurrence `occ.a6cd56d6fd9f20b4c8ec` targets the general nonunital module
meaning. Their continuity/topology/product dependencies are legitimate; these
texts do not ensure continuity of negation in that general scope. Round183's
zero-product ℤ with upper-set topology makes addition and multiplication
continuous but negation discontinuous; the analogous zero scalar action gives
the module example. Under a unital convention, multiplication by −1 supplies
continuous negation. The external source conventions were not independently
verified here, so no assertion about a false external source is warranted.

**Disposition:** later-phase source/variant issue with a genuine scope consequence.
**Not applied:** either explicitly adopt justified unital assumptions or require
additive topological-group structure for the general variant. Do not silently
retarget the current broad definitions. **Pass 2:** this can be explicitly
deferred while preserving the distinct ring/module identities; if adjudication
changes which identity a reference means, revalidate that affected consolidation
scope before relying on it.

## 6. Consolidated decision boundary and validation

- **First resolve/explicitly quarantine #1's FIP empty-family convention.** It
  changes the contextual prerequisite to be interpreted/populated and defeats
  the literal compactness equivalence under the currently recorded nonempty-
  finite-subfamily convention. The historical ambient seed itself need not be
  removed to address this issue.
- **Adjudicate one shared convention/deferral policy** for #2, #4–#9 and #12–#13.
  The general/specialized relationships are mathematically valid in a unital
  domain, but the stored source sentences and locators do not prove that domain.
  This is not nine independent alias errors. A documented later source/variant
  deferral preserves identity consolidation; blanket “all links verified” does
  not. #3 has the additional free-augmentation argument and is separated out.
- **No further resolution of the flagged relationship is indicated** for #3,
  #10–#11 and #14–#19. Keep the source records and identities distinct; this is
  not permission to merge coextensive field-theory meanings or delete redundant
  dependencies.
- **Record later-phase wording/source dispositions** for #20, the four
  provisional issues and topological algebra. If any later decision changes
  source scope, occurrence interpretation or candidate identity, reassess the
  exact affected snapshot. Mere persistence of these warnings is not a hard
  consolidation prerequisite.

This is a bounded review of 20 leads, not exhaustive mathematical review of all
659 formulations or all 421 canonical identities. It supplies proposed rationale
for the subsequent ChatGPT decision, not a consolidation declaration. Nothing
here authorizes a packet, gate, source edit, alias, promotion or Pass 3.

Read-only commands executed successfully:

```bash
python -m research_pipeline.engine.dependency_consistency_worklist --workspace research_pipeline/experiments/reconstruction-v2-independent --exhaustive
python -m research_pipeline.engine.dependency_consolidation_readiness --workspace research_pipeline/experiments/reconstruction-v2-independent --exhaustive
```

Both JSON outputs were kept in `/tmp/wave2-task4-*.json`, outside the checkout.
Finite direct checks confirmed the discrete nonsurjective map counterexample,
the zero-action module axioms, the zero-product rng's ideal lattice and the
empty-family FIP counterexample. These are checks of countermodels, not a new
auditor or a substitute for the mathematical arguments above. No application
code changed, so no broad regression suites were run. Dataset SHA256 comparison
before/after covered all 2,277 files; `git diff --check` and final branch-to-base
path inspection passed. Only this report changed; source records, definitions,
graph links, aliases, ledgers, indexes, state and consolidation gate are unchanged.
