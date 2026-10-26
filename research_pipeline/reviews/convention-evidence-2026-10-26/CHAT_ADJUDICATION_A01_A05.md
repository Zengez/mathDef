# Chat mathematical adjudication: A01–A05 (16 historical cases)

**Date:** 2026-10-25 (America/New_York). **Basis:** reviewed preparation
`ADJUDICATION_QUEUE.md`, `REVIEW.md` and case-specific current source and
target evidence from `codex/wave2-convention-evidence-2026-10-26` at
`9d4aa90260ed51d5e387aeede8a6683c9cbff20f`. The review preserves
historical candidate IDs and uses the existing 2026-10-25 independent graph.
**Status:** source-free mathematical adjudication / policy recommendations,
not user ratification, source certification, resolution, amendment, acceptance
of a gate, or Pass 3 authorization. All 2,293 protected workspace files
remain outside this report and were not edited.

## Overall policy recommendation — PROPOSED, NOT APPROVED

Use a **typed, context-preserving dependency model**: the meaning linked as a
prerequisite should match the portion of the parent formulation it actually
supplies. A generic operation can serve as a component prerequisite of a
specialized construction **only with explicit instantiation and hypotheses**.
Never identify a compound object, a definition's truth condition, and an
operation used in constructing it merely because they share notation. Do not
silently add unitality, commutativity, nonzero-ness, finite index sets, or
linearities from the identity of the putative target.

An absent source convention is an evidence gap, not a mathematical
contradiction and not automatically a consolidation blocker. Distinguish:
(1) a proved mathematical implication; (2) current-source textual scope;
(3) the original provider's unverified conventions; (4) a future project
modeling choice. No cited original source was independently fetched or
verified in this pass.

## A01: coefficient types and localization denominators — three cases

### Rank 7 — `missing.5645554e6bee6b40edda` (commutative unital ring)

**Mathematical determination:** associativity, commutativity, possession
of an identity and `1≠0` are logically separate. For example a nonzero
zero-multiplication ring is commutative without identity;
`M_2(Q)` is unital but noncommutative; `Z/4Z` is commutative unital
but not a field or integral domain. A commutative unital coefficient
ring is not a synonym for the repository's identity-optional ring, and
does not imply a nonzero condition. Where a parent explicitly says
"commutative ring with identity" the relevant hypothesis is supported by
that source text. Where the six parent formulations say only "commutative
ring", unitality and zero-ring policy remain **source-convention deferred**.
Do not bulk-rewrite the six parents to assume one.

**Next action:** source-specific verification only; no identity alias or
source correction approved.

### Rank 23 — `missing.3b37131115a06556c3e4` (commutative unital k-algebra)

**Mathematical determination:** the specified `k→A` scalar structure
is part of the algebra data. It cannot be replaced by the underlying
ring, the base field, or the structure map alone. Algebra multiplication
need not inherit the field property; `k[t]` and dual numbers give
immediate witnesses. A commutative unital `k`-algebra with a unital
structure arrow is a coherent scoped target. The five parents, however,
do not individually state every commutative/unital/zero-algebra
convention. Their geometric terminology is not by itself independent
provider-source certification.

**Next action:** verify five original sources' conventions; keep this
algebra identity distinct.

### Rank 43 — `missing.0c99be984399f9134720` (multiplicative S⊆R)

**Mathematical determination:** closure under multiplication does not
imply `1∈S`—even the nonzero subset
`S={2^n:n≥1}⊆Z` is multiplicatively closed without containing 1.
`0∈S` is a *separate* convention: in the ordinary universal
localization it forces the zero ring, but does not make a general
construction syntactically undefined. For a unital ring the set of
regular/non-zero-divisor elements contains 1 and is closed under
multiplication. The denominator set and its localized ring/module
remain different objects.

**Next action:** retain candidate's explicitly unital denominator
convention as a scoped interpretation; verify inclusion of 1 and
allowance of 0 independently in the three original source formulations.
Do not silently impose `0∉S`.

## A02: shared units, subrings, local inclusions — three cases

### Rank 133 — `missing.0113342523b02aece2fb`

**Mathematical determination:** inclusion of individually unital
commutative rings does not imply that their identities coincide:
`k×{0} ⊂ k×k` has respective identities `(1,0)` and `(1,1)`.
The selected source says "an inclusion of commutative rings with
identity" but does not explicitly settle identity-preservation.
A preexisting unital-map seed may support intent, not certify the
author's convention. Moreover, injectivity of a polynomial evaluation
from the strong-transcendence hypothesis is a *consequence* in the
common-unit scope, not grounds to assume the definition.

**Next action:** source-verify whether inclusion preserves 1;
retain the common-identity qualifier in the candidate; no alias.

### Rank 252 — `missing.6761326c179c108a8d73`

**Mathematical determination:** a ring homomorphism `R→S` need not
be injective. The integral closure of `R` *in* `S` is formed over
the image of `R`, not an assumed embedded copy of the domain
(e.g. `Z→F_2`). The subring is a prerequisite, but the
integrality-selected subring is not the same as a generic subring or
generic ring map. Inherited identity and commutativity must be
checked against the source before broad matching.

**Next action:** source-specific convention verification; preserve
image-versus-inclusion and integrality selection.

### Rank 281 — `missing.8270eec9d7801be60879`

**Mathematical determination:** assuming ordinary nonzero unital
subrings of a common field, each subring has the *same* multiplicative
identity: a nonzero idempotent in a field must equal 1. This conclusion
is conditional on the stated unital/nonzero reading, not proof of the
source's unstated convention. Inclusion does not imply domination:
`Z_(p)⊂Q` has maximal ideals `pZ_(p)` and `0`, respectively,
so `m_Q∩Z_(p)=0` differs from `m_{Z_(p)}`.

**Next action:** source-verify the local-subring convention; do not
equate the inclusion with domination.

## A03: ideal products, module spans and I-adic action — three cases

### Rank 18 — `missing.e43d4f1922e210cc373a`

**Mathematical determination:** `IJ` is the additive subgroup of
finite sums of products `ij`. If I,J are two-sided ideals of an
associative ring, this is a two-sided ideal even without a unit or
commutativity. In a noncommutative ring, `IJ` and `JI` cannot
generally be interchanged. The products `I^n`, n≥1, are meaningful
without unity, as the `I^n=0` nilpotence source requires. Writing
`I^0=R` is a useful convention, but the resulting unit property
`RI=I` is not universal for nonunital actions/rings.
Commutative-unital Rees/completion/Dedekind parents give stricter
source-specific assumptions. Symbolic power also uses
localization/contraction and is not just ordinary power.

**Recommendation (policy, not applied):** favor a generic
two-sided-ideal-product prerequisite with separately documented
commutative/unital specialization and exponent 0 conventions.
Do *not* treat an already narrowly scoped canonical candidate as
automatically identical to the broader one; record scoped dependencies
or defer identity splitting until explicitly reviewed.

### Rank 54 — `missing.beea674f8fcd201a1af5`

**Mathematical determination:** for a unital left R-module,
`∑Rm_i` is the least R-submodule containing its generators, because
`1m_i=m_i`. In an arbitrary nonunital action, however, the usual
finite-combination expression can omit the generators: let `R=F_2`
act as zero on nonzero `M=C_2`. Then `Rm=0` for `m≠0`, but
the generated submodule is `M`. In general the least generated
submodule is the additive subgroup generated by
`{m_i}∪{r m_i : r∈R}` (equivalently `∑ Zm_i + ∑ Rm_i`).
Thus `M=∑Rm_i` and a surjective map `R^n→M` encode
a *stronger* finite-generation convention for a nonunital action.

**Recommendation:** retain the stated linear-span candidate in the
**unital-action context**, and keep any broader nonunital
generated-submodule meaning typed separately. Do not claim
the formulas are equivalent without checking the action hypothesis.
No source edits approved.

### Rank 56 — `missing.d066de85583ac1b1a7d4`

**Mathematical determination:** `IM`, finite sums of `i m`,
is a submodule when I is a two-sided ideal and M a left R-module.
It differs from the ideal product in R, the quotient `M/IM`,
and an inverse limit of such quotients. For `n≥1`,
`I^n M` makes sense with no unital-action assumption. If
`I^0=R`, then `I^0M=RM=M` **only** when `RM=M`
(in particular when the action is unital). The zero-action
counterexample already used at rank 54 also refutes a blanket
`I^0M=M`.

**Next action:** verify the three parent sources' ring/action
conventions and starting index; preserve each quotient and completion
operation separately.

## A04: grading, exterior tensor operations, de Rham differential — four cases

### Rank 95 — `missing.72b9f9bc4ac0e952e202`

**Mathematical determination:** the common construction is a
finite-support **additive** direct sum of homogeneous pieces. For
`k[t]` with its standard grading, `k t^j` is not generally
a `k[t]`-submodule because multiplication by `t` shifts degree.
Thus grading `S=⊕_{n≥0}S_n` and grading
`M=⊕_{j∈Z}M_j` can share a generic additive
direct-sum prerequisite without equating the full graded structures.
An `N`-grading embeds into `Z` by zero extension, but a
`Z`-grading need not be nonnegative.

**Recommendation:** use a generic index-set-indexed additive
direct sum as an *instantiated component prerequisite*; preserve each
module/scalar-compatibility axiom separately. No implicit unification
of full gradings.

### Rank 175 — `missing.25dac0c185025e52a26a`

**Mathematical determination:** for finite free modules over an
ordinary commutative unital R, an R-linear map `φ` induces
`∧^r φ` on the corresponding exterior powers. This is a map,
not the exterior-power module itself. Ordinary tensor powers of an
arbitrary left module over a noncommutative ring are not justified
without right-left/bimodule typing. At `r=0` the induced map is
`id_R`: in the zero ring this is the zero map, so the source's
"largest r with nonzero exterior-power map" rank convention needs
separate zero-ring treatment. Do not equate this rank criterion with
fibre rank, which may vary under reduction.

**Next action:** source-verify commutative/unital coefficient and
zero-ring/r=0 conventions; no unconditional rank identity.

### Rank 358 — `missing.c5a7afab433a3e7d30ed`

**Mathematical determination:** the tensor algebra
`T_R(M)=⊕_{n≥0}M^{⊗_R n}` is naturally an associative,
nonnegatively graded algebra when the tensor products are
appropriately typed. Even when R is a commutative field, the
tensor algebra on a two-dimensional vector space is generally
noncommutative (`e⊗f≠f⊗e`). Do not identify an associative
graded R-algebra with a commutative graded ring, an underlying
graded module, or the underlying tensor product. For a
noncommutative coefficient ring, tensor powers require compatible
bimodule/right-left structures; this does not follow from a
bare left R-module.

**Next action:** source-verify coefficient, module and unit
conventions; do not change the tensor algebra definition itself
until those conventions are established.

### Rank 400 — `missing.ebf92c196007c438f394`

**Mathematical determination:** for a commutative ring map
`A→B`, each relative de Rham `Ω^p_{B/A}` is a B-module,
but the differential `d` is generally only A-linear and
is a graded derivation. Over `A=k`, `B=k[t]`,
`d(t)=dt≠0` whereas `t d(1)=0`; hence B-linearity
is false. The underlying object is an A-linear cochain complex
with differential of degree +1 and `d²=0`, enriched by its
wedge/differential-graded-algebra structure. Do not identify it
with a B-linear complex or the entire relative de Rham
construction solely via the cochain prerequisite.

**Recommendation:** the A-linear cochain complex is an
*underlying typed prerequisite*, not the whole meaning.
No amendment or source edit proposed.

## A05: ringed spaces, sheaf quotients, henselization — three cases

### Rank 202 — `missing.42dd118d20d40e57e2b9`

**Mathematical determination:** a sheaf of rings is sheaf-valued
ring data on opens (with coherent restriction maps); it is not
a single ring, its space of global sections, or a stalk.
A locally ringed space requires **every stalk** to be local,
not simply a ringed space: a one-point space with constant
ring Z is a counterexample. The candidate's
identity-preserving restriction convention and the exact
local-ring convention still require external source
verification; their scope cannot be inferred from a sheaf
attribute alone.

**Next action:** verify ring and stalk conventions later;
keep generic ringed-space and locally ringed-space
hypotheses distinct.

### Rank 222 — `missing.4fff53dd962546ca64ba`

**Mathematical determination:** the quotient ring *sheaf*
`O_X/I` is not a ring quotient at one fixed open: taking
sectionwise quotients may require sheafification. For the support
inclusion `i:Z→X`, the direct image `i_*O_Z` is an
additional construction; the comparison
`i_*O_Z ≅ O_X/I` requires the chosen structure sheaf on Z.
Do not identify an arbitrary ring quotient, sheaf quotient,
pushforward, support, or whole closed-subspace datum.
Nor does "locally section-generated" by itself authorize
replacement by a globally finite generating set or
a quasi-coherent ideal sheaf.

**Recommendation:** preserve typed components and the
comparison map; segmentation is only a proposed future
review action, not an applied candidate split.

### Rank 323 — `missing.a115a0258bce647cea2b`

**Mathematical determination:** for henselization the assertions
that `R→R^h` is a local map, that
`m_{R^h}=m_R R^h`, and that
`R/m_R→R^h/m_{R^h}` is an isomorphism
are distinct. A local map inducing a residue-field
isomorphism need not induce maximal ideal by extension:
`k→k[t]_(t)` has the first two stated properties
(local map, residue-field iso), but
`0·k[t]_(t)=0≠(t)`.
The universal property and étale-colimit presentation
are additional structure, not synonyms for the compound
ideal/residue datum.

**Next action:** preserve all typed conditions and map
directions. The local/unit and source universal-property
conventions still await provider verification.

## Status ledger for this round

- Examined **16 historical cases** in cards A01–A05:
  ranks `7,23,43,133,252,281,18,54,56,95,175,358,400,202,222,323`.
- Historical dispositions include source-convention deferrals and
  contextual ambiguities, not 16 identified mathematical errors.
- **Source verification not performed. Mathematical-typing conclusions
  are reviewer judgments; project policy recommendations are proposed
  only.**
- All 16 historical identities remain unresolved under the live graph.
  Existing corrected rank 399 belongs to A08 and was not re-amended.
- No new term, alias, resolution, scan amendment, source edit, existing
  edge change, graph receipt, dataset file modification, or gate change.
- Continue with A06 (polynomial and quotient constructions) before
  A07 (categorical), then A08–A13. Any future implementation should
  be scoped and separately version-bound after explicit adjudication.
