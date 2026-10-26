# Primary-source check — Stacks conventions and DLMF (2026-10-25)

**Status:** externally consulted **current official provider pages**.
This is a distinct, bounded source-reconciliation pass,
superseding the historical label "source-free" **only for the
exact primary links and convention claims listed below**.
It does not imply all 13 deferrals are resolved, nor
that external publisher pages have been checked for their
historical versions. No graph, source record, citation,
candidate context, registered meaning, receipt, frozen
workspace or production site was modified.

## What has now been checked directly

### Stacks Project — commutative algebra conventions

**Official source:** [Stacks Project, Algebra, §10.2, tag 00AQ](https://stacks.math.columbia.edu/tag/00AQ).

The present official section states that **ring
means commutative ring with identity**, expressly
**includes the zero ring**, and carefully treats a
general ring homomorphism R→S without assuming
injectivity or identifying R with a literal subring
of S.

**Consequences for the previous deferral inventory:**

- **Rank 7** (`missing.5645554e6bee6b40edda`):
  Current Stacks *Algebra* source convention is
  **verified** for commutative/unital coefficients
  and zero-ring inclusion. The six formulations
  with only "commutative ring" cannot be labeled
  nonunital *on the basis of Stacks provider
  attribution*. Do not remove explicit nonzero
  requirements in *fields/domains*, and do not
  impose Stacks conventions on **unrelated
  independent source variants**.
- **Rank 23** (commutative unital k-algebra):
  the base-ring unitality and commutativity
  convention of this Stacks commutative-algebra
  material is supported. The particular k→A
  structure map and the commutativity of the
  specified target should still be checked at
  the individual algebra definition, especially
  across chapters with broader associative
  algebra conventions.
- **Rank 252** (integral closure relative to
  ring map): Stacks explicitly allows
  **noninjective** ring maps. Writing "closure of R
  in S" in the formal ring-map case does not
  justify replacing the image of R by an
  unverified embedded copy.

This is a **provider-level verified convention**,
not a new approval to retype an identity-optional
ring meaning as unital globally.

### Stacks Project — multiplicative denominator sets

**Official source:** [Stacks Project, Algebra, §10.9, tag 00CM](https://stacks.math.columbia.edu/tag/00CM).

Definition 10.9.1 **requires 1∈S** and
multiplicative closure. It does **not** require
0∉S. Lemma 10.9.4 expressly identifies the
localization with the zero ring when 0 belongs to
S. Example 10.9.8 gives both a prime-complement
denominator set and the nonzerodivisor set.

- **Rank 43** (`missing.0c99be984399f9134720`):
  its **unit-in-denominator** provider convention
  is now directly verified for the
  Stacks localization source. Its **zero
  denominator** policy is also established:
  zero is **permitted** by the generic
  multiplicative-set convention, with zero-ring
  localization. The special nonzerodivisor
  denominator set excludes zero in a nonzero
  ring, which is a **specialization**, not the
  generic definition.
- **Rank 56:** the localizations operate in
  standard Stacks R-module context and depend
  on the same unital coefficient ring; this
  passage does **not by itself** fully certify
  the exact I⁰M=M index/underlying-module
  condition for all three parent formulations.
  Keep that detailed check open.

### Stacks Project — integrality relative to any ring map

**Official source:** [Stacks Project, Algebra,
§10.36, tag 00GH](https://stacks.math.columbia.edu/tag/00GH).

Definition 10.36.1 evaluates a monic
polynomial after applying a possibly noninjective
structure map R→S. Definition 10.36.9 constructs
a subring of S of elements integral over R,
and imposes R⊆S only in the separate case
where an embedded subring is literally
specified.

- **Rank 252** (`missing.6761326c179c108a8d73`):
  the distinction between **image under R→S**
  and an actual **inclusion R⊆S** has been
  source-verified on the directly relevant
  current definition. The underlying
  commutative/unital coefficient convention
  follows Stacks Algebra §10.2. The
  relative integral-closure prerequisite
  remains distinct from a generic subring,
  and does not become an identity with the
  full integral closure object.

### Stacks Project — left adjunction definition

**Official source:** [Stacks Project,
Definition 4.24.1, tag 0037](https://stacks.math.columbia.edu/tag/0037).

The definition uses morphism collections
`Mor_D(u(X),Y)` and `Mor_C(X,v(Y))`,
with bijections functorial in both variables.
This supports the type/variance analysis
of historical **rank 393**, but **does not by
itself settle** which set/universe or
locally-small framework all authors of
the larger category text intend. It is
not evidence that categories must have
a set of objects. Retain the bounded
size-convention question.

### DLMF — Stieltjes measure orthogonality

**Official source:** [DLMF §18.2(i),
orthogonality on general sets](https://dlmf.nist.gov/18.2);
see also [DLMF §1.4(v)](https://dlmf.nist.gov/1.4).

The DLMF statement directly uses a bounded
nondecreasing function α on the interval
closure, infinitely many points of increase,
and finite absolute moments for its
Lebesgue–Stieltjes measure. In §1.4(v) it
also explicitly discusses atomic jump
measures and distinguishes general
Stieltjes measures from measures possessing
a Lebesgue density.

- **Rank 166** (`missing.2216f1dfe187a7af152c`):
  the bounded/nondecreasing/measure and
  moment setting is **verified**. The DLMF
  excerpt does **not** specify the exact
  right-continuous versus left-continuous
  distribution-function normalization, or
  all endpoint atom conventions. Its
  reconstructed source paraphrase's
  adjective **"admissible"** should not
  be treated as a separately defined
  DLMF hypothesis without another actual
  locator. That specific source issue
  remains **partially open**.
- **Secondary rank 364:** DLMF really uses
  infinitely many points of increase;
  this is not a scanner hallucination.
  The passage does not itself equate
  that phrase with strict monotonicity
  everywhere, positive derivative, or
  all other notions of support, so the
  exact characterization remains deferred.
- **Secondary rank 291:** the existence
  of atoms is source-supported. Boundary
  inclusion and the particular interval
  assigned to raw moments still require
  precise contextual verification.

## Not yet source-verified in this pass

The other source-convention cases remain
to be checked at appropriate exact
definitions, rather than inferred solely
from provider title or chapter context:

- Rank **56** (each I-adic module action,
  exponent-zero convention);
- Rank **133** (common identity for the
  specific strong-transcendence ring
  inclusion);
- Rank **154** (ProofWiki's integer versus
  cardinal multigraph edge multiplicity);
- Rank **175** (exterior-power map, r=0,
  zero ring and coefficient choices);
- Rank **202** (sheaf-of-rings restriction
  maps and local stalks);
- Rank **281** (local-subring/common-field
  convention and domination);
- Rank **358** (tensor algebra/module input
  category and degree-zero unit);
- Rank **393** (specific category
  Hom universe beyond the now checked
  adjunction formula).

Ranks 7, 23, 43, 252, 166 above have
**some** directly verified provider-level
questions, but none has been
automatically marked accepted in the
graph. All **13 historically open
source-convention identities remain
unresolved as graph candidates**.
Mathematical/source verification evidence
is not the same thing as an executed
transaction or a gate decision.

## Historical-source/version caution

The independent corpus consists of
screened paraphrases with evidence/source
IDs and source-snapshot hashes. No source
page was fetched or pinned as raw
authoritative content during the original
40-case evidence capture. The URLs above
are **current live official pages**,
read on 2026-10-25; no 2026-10-25
GitHub content source-version/observation
hash was amended.

Before declaring an individual source
record wholly reconciled, confirm the
stored observation's specific locator/tag,
chapter scope, mathematical assumptions,
and whether an older revision could change
the meaning; record any such difference
rather than retroactively replacing the
immutable observation. Keep provider
assertions, current mathematical theorem
verification and reviewed graph changes
separately labeled.

**Action boundary:** This report is a
standalone citation-evidence supplement.
No acceptance, alias, new meaning,
graph amendment, missing-candidate
resolution, source rewrite, consolidation
gate transition or Pass 3 action follows
automatically.


---

## Second source check — exact recorded locators and clarified statuses

This section supersedes the earlier "not yet source-verified" list **for the
specific questions directly answered below**. The earlier section remains a
chronological record of what had been checked at that point. All links below
are **official source pages at their recorded tags/locators**, independently
consulted this round, not authority inferred from the repo's provider metadata.

### Rank 154 — multigraph finite-per-pair multiplicity: convention verified

The exact archived observation points to
[ProofWiki Definition:Multigraph](https://proofwiki.org/wiki/Definition:Multigraph).
Its multigraph `(V,E)` uses a **multiset of two-element subsets** of V
and says loop conventions vary between sources. In the provider's linked
[Definition:Multiset](https://proofwiki.org/wiki/Definition:Multiset),
a multiset is `(S,μ)` with **μ:S→positive integers** and an explicit
exclusion of infinite multiplicity for any *one* element; S may be infinite.
Thus the provider's selected construction allows an infinite number of
vertices or distinct edges but **only finite multiplicity of each edge pair**.
This directly settles the original rank-154 per-pair multiplicity ambiguity
under this provider's own definitions. The multiset page bears an editorial
refactoring notice, so its status as an authoritative general mathematical
convention should **not** be broadened outside this specific ProofWiki chain.
Do not infer that every mathematical definition of multigraph forbids loops
or infinite multiplicities.

### Rank 358 — tensor algebra: coefficient scope and multiplication verified

[Stacks §10.13, tag 00DM](https://stacks.math.columbia.edu/tag/00DM)
defines `T_R(M)=⊕_{n≥0}M^{⊗_R n}`, with **T⁰(M)=R** and
concatenation, explicitly describing it as a
**noncommutative R-algebra**. Combined with the commutative
unital coefficient-ring convention at
[Stacks §10.2, tag 00AQ](https://stacks.math.columbia.edu/tag/00AQ),
this confirms that **R is commutative/unital but the constructed tensor
algebra need not be commutative** in this cited scope.
This settles the parent source's ordinary coefficient-ring/module typing
without inventing noncommutative ring-left-module tensor powers.
No generic assertion about bimodule tensor algebras follows.

### Rank 281 — domination of local subrings: recorded source directly verified

[Stacks §10.50, tag 00I8](https://stacks.math.columbia.edu/tag/00I8),
Definition 10.50.1, explicitly takes local rings A,B **contained
in a common field K** and defines B dominating A by
A⊆B plus maximal-ideal contraction. In a field, a nonzero
unital subring's identity is necessarily the ambient
field's identity, so the common-unit property is supported
in this exact scope. **Inclusion alone does not imply domination**;
the maximal-ideal condition is separate. The stored parent
formulation correctly preserves that condition.

### Rank 202 — locally ringed space: source verified within provider conventions

[Stacks §26.2, tag 01HA](https://stacks.math.columbia.edu/tag/01HA)
recalls that a ringed space is `(X,𝒪_X)` with a **sheaf of rings** and
requires each stalk to be a local ring for a locally ringed space.
Its cited [§6.25](https://stacks.math.columbia.edu/tag/0081) treats
ringed spaces more generally. Read the ring-sheaf restriction
maps in the usual ring-homomorphism sense, coupled with the
provider's explicitly commutative/unital conventions; do
**not** collapse stalks, global sections, quotient sheaves or
the full locally ringed object. The source-specific
ringed-space/local-stalk criterion is checked, while
any editorial decision about how many typed prerequisite
nodes to link remains separate.

### Rank 133 — strong transcendence: defining formula verified, units contextual

The exact archived locator,
[Stacks Definition 10.123.7, tag 00PZ](https://stacks.math.columbia.edu/tag/00PZ),
requires an **inclusion of rings** R⊂S and uses arbitrary
u∈S in the annihilator-sensitive polynomial implication.
With §10.2 provider convention the rings are commutative
and unital; for an inclusion explicitly understood as a
**unital ring map**, the identity is shared. The tag's
one-line definition does not itself assert the source
inclusion is unital, so keep the identity-preservation
justification attributed to the project's ring-map
convention rather than to a textual `1_R=1_S`
assertion at tag 00PZ. Do **not** replace
strong transcendence with ordinary algebraic
independence in arbitrary rings. The formula also does
not require nonzero annihilating factors, corroborating
the rank-298 possible explanatory-overlink caution.

### Rank 393 — category-size convention: provider default verified with exceptions

[Stacks §4.2, tag 0013](https://stacks.math.columbia.edu/tag/0013)
actually **defines a category with a set of objects and sets
of morphisms** and explicitly states that this is its default
unless listed exceptions allow large categories. This is
stronger than the generic condition that Hom collections be
sets while the object collection might be a proper class.
The exact source [§4.24, tag 0036](https://stacks.math.columbia.edu/tag/0036)
and [Definition 4.24.1, tag 0037](https://stacks.math.columbia.edu/tag/0037)
give natural bijections between Hom sets for adjunctions.

**Correction to earlier research deferral:** for a plain
"category" in the Stacks defaults, the set-of-objects
convention **is directly documented**; for its explicitly
named large categories, or general category theory elsewhere,
one must respect the exceptions and any chosen universe.
Do **not** use provider defaults to force all mathDef
category meanings to denote only small categories.

### Rank 175 — exterior-power rank: source verified, zero-ring boundary remains

[Stacks Definition 10.102.5, tag 00MR](https://stacks.math.columbia.edu/tag/00MR)
defines rank φ as the **maximal r for which ∧^rφ is nonzero**
and adds "rank φ=0 iff φ=0". Its coefficient ring inherits
Stacks §10.2's commutative/unital convention, including
the **zero ring**.

**Remaining precise boundary:** when R is the zero ring,
every R-linear map and `id_R` are zero maps, including
`∧⁰φ=id_R`; hence no r necessarily satisfies the
published "∧^rφ nonzero" predicate. Unless a convention
for the empty maximum or a nonzero-ring hypothesis is
made explicit, the literal formula does not alone yield
rank zero for zero maps over the zero ring. This is a
genuine mathematical/source edge case, **not** a license
to edit the published source or declare a universal
counterexample to the usual nonzero-ring theorem.
Retain as a bounded qualification lead pending
source-specific convention reconciliation.

### Rank 56 — completion formula checked; action/index convention not fully closed

[Stacks §10.96, tag 00M9](https://stacks.math.columbia.edu/tag/00M9)
directly gives ring and module I-adic completions as
`lim_n R/I^n` and `lim_n M/I^nM`.
[Stacks §10.72, tag 00LE](https://stacks.math.columbia.edu/tag/00LE)
gives the separate depth-module context.
This confirms the actual quotient/module completion
operations and their ordinary Stacks ring convention,
but a reviewer should still independently check
**whether each parent specifies I⁰M=M or begins at n=1**
and the unital module action in any non-Stacks
variants. No unitality inference should be exported
to the repository's explicitly identity-optional
module formulations.

## Current evidence-versus-graph status

The original 13 historical deferral identities are still
**unresolved in the independent dependency graph**,
even where some particular provider/source convention
questions have now been answered directly from exact
archived locators. In particular, ranks 154, 281, 358
and the Stacks default size component of 393 no longer
need the same provider-convention research repeated,
while 166's measure sidedness and 175's zero-ring
rank edge case require more precise disposition.

No original provider page or GitHub source event was
silently rewritten. This report constitutes review
evidence, **not an applied graph transaction, blanket
source certification, gate transition or Pass 3 approval**.
