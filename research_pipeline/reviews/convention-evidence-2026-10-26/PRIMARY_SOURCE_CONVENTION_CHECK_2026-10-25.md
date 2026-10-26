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
