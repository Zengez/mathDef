# Chat mathematical adjudication: A10–A13 (final ten historical cases)

**Status:** source-free, non-applying mathematical review. Mathematical
claims/counterexamples reviewed against the exact historical cases in
`REVIEW.md`; recommendations are **not adopted user policy** and do
not update source records, meanings, nodes, aliases, receipts, missing
candidate statuses, protected graph or the consolidation gate.
Read with `CHAT_ADJUDICATION_A01_A05.md` (16 cases) and
`CHAT_ADJUDICATION_A06_A09.md` (14 cases).

## A10: generic operations versus named constructions (four cases)

**Rank 172 — `missing.244d6cfceb0dd22abbca`,
degree-zero extraction.**
For a graded ring S localized at a homogeneous element f,
the degree-zero component `(S_f)_0` is a subring of
`S_f`, but not generally all of `S_f`. For
`S=k[x]`, `f=x`, the entire localization is
`k[x,x^{-1}]` and its degree-zero part is k.
The stored `S_(f)` definition is this *specific*
degree-zero construction. A generic homogeneous degree-zero
component is a valid reusable operation, but resolving the
specific candidate to the whole S_(f) meaning would make a
self-prerequisite. **Decision:** keep typed general operation
versus specialized whole construction; preserve `deg f>0`,
homogeneous numerator restrictions and zero-component
conventions. No applied resolution.

**Rank 223 — `missing.50540c0ba5822a8df022`,
Grothendieck-group presentation.**
A commutative monoid admits universal group completion without
requiring cancellation: distinct monoid elements can become
equal in its group completion. The monoid of isomorphism types
of finite projective modules under direct sum, once chosen,
gives the parent K_0 construction; the generic operation is
only its reusable prerequisite. The separate K'_0
construction from finite modules and short exact sequences
has distinct generators/relations and must not be merged
without an independent theorem. Size/skeleton conventions
remain source-scoped. **Decision:** use generic group completion
only with explicitly instantiated monoid, and avoid K_0
self-dependency.

**Rank 245 — `missing.6149b958a6aa818d4806`,
ring inverse limits.**
The inverse limit of `R/I^n` with compatible reduction maps
inherits componentwise ring operations in addition to its
underlying additive-group or module limit. That specific
inverse limit *is* the stored I-adic completion, so
unqualified resolution of the parent prerequisite to the
parent meaning would be circular. A generic inverse-limit
of rings is the reusable operation, instantiated with the
chosen system and its maps. Index 0, if admitted with
`I^0=R`, gives a forced `R/R=0` stage but
does not replace the positive-index convention.
**Decision:** preserve generic-versus-specific level, ring
structure and the specified transition maps.

**Rank 405 — `missing.f179e2d20985ef5e88d5`,
localization at a prime complement.**
If p is prime and proper in a commutative unital R,
`R\p` is multiplicatively closed and includes 1.
It is the chosen denominator set, not the ring
`R_p`, not the module `M_p` and not the support
predicate `M_p≠0`. A generic localization of modules can
be instantiated with this set, but changing the candidate
from a denominator-set meaning to whole module localization
requires explicit scoped identity review. **Decision:**
valid specialization/component, not an exact alias of all
construction data.

## A11: demonstrable wording qualifications (two cases)

**Rank 40 — `missing.fa5932b42daa1a3e0307`,
roots and quotient fields.**
A root α satisfies `f(α)=0` in a specified field
extension. `k[t]/(t²)` is *not* a field because
the nonzero class of t is nilpotent. Thus an illustrative
claim that *every* nonconstant polynomial produces a field
by quotienting is false: irreducibility is needed.
The actual stored parent `form.1fd51873f9f0afbd.field-from-irreducible-polynomial`
already states irreducible, so no parent error has been
proved. **Decision:** recommend fixing only the overly
broad missing-candidate example in a separately authorized
wording/identity review; keep the generic field-root concept
distinct from quotient-field construction and splitting field.

**Rank 250 — `missing.659b5d5ed37a38428987`,
n prime to characteristic.**
For a field K, the correct arithmetic hypothesis is that
`n·1_K` is invertible. In positive characteristic p this
means p does not divide n; in characteristic zero every
nonzero integer n is invertible, whereas an unqualified
`gcd(n,0)=1` would reject n≥2. This says nothing
about n being a prime number. The Kummer source also
involves roots of unity and other hypotheses; no blanket
Kummer theorem audit has been carried out.
**Decision:** recommend explicit invertibility phrasing in
the candidate, without changing the parent source or
claiming its full Galois conclusion certified.

## A12: sets, total orders and indexed families (three cases)

**Rank 181 — `missing.2d4e4af6f3b83da929a6`,
unordered pair in Kuratowski's ordered pair.**
`{a,b}` contains one element when `a=b`;
the Kuratowski ordered pair remains valid:
`(a,a)={{a}}`. A doubleton, by contrast, requires
two distinct elements. **Decision:** say "unordered pair
(possibly a singleton)", not "doubleton", while preserving
all arbitrary-coordinate ordered-pair cases. Constructor
nesting does not make the whole ordered pair synonymous
with a singleton or unordered-pair operation.

**Rank 259 — `missing.6e286e5d25f8e80fa9f6`,
no largest element.**
In a *total order*, no greatest element iff no maximal
element, because every element which is not greatest is
strictly below another. In a two-element antichain there
is no greatest element, but both elements are maximal,
so the equivalence fails in a general partially ordered
set. The Dedekind rational lower-cut source is totally
ordered and is not wrong. **Decision:** qualify the candidate
with total-order scope; preserve the parent cut's other
nonempty/proper/downward-closure conditions.

**Rank 324 — `missing.a128ec6b5c7fae2074c2`,
set family versus indexed family.**
A set of blocks P forgets repeated labels. An indexed
family `(B_i)_{i∈I}` additionally remembers I and
the assignment; distinct indices may have identical
sets, whereas a set-of-sets representation cannot
retain duplicate occurrences. For an empty underlying
set, P=∅ is the valid partition into nonempty blocks;
P={∅} is not. **Decision:** keep the set-of-blocks
predicate typed separately from an arbitrary indexed
family, without imposing nonempty underlying sets.

## A13: graph multiplicity (one case)

**Rank 154 — `missing.17fcbd3c3e67f2b21f6b`,
edge multiplicity.**
The ordinary finite-multiset convention assigns a
natural-number multiplicity to each distinct unordered
vertex pair; a broader cardinal-valued multiset convention
may allow infinitely many copies of one pair. Neither
infinite vertex count nor infinitely many distinct edges
forces an individual pair to have infinite multiplicity.
The graph source already excludes loops by requiring
edge endpoints to be distinct in two-element edge sets.
Parallel edges, however, remain possible.
**Decision:** preserve a finite-per-pair multiplicity
meaning as a scoped option; source-verify the author's
multiset convention before asserting it universally.
Do not impose finite V, finite E or simplicity.

## Completion and next decision boundary

The three Chat adjudication reports now cover **all 40
historical cases**, each exactly once, grouped into the
13 cards A01–A13. They record source-free mathematical
scope determinations and **provisional** modeling choices.
No source convention was verified externally; the original
13 convention deferrals are still properly identified as
source-verification work. The historical classifications
do not constitute 40 required graph corrections or
automatic readiness blockers.

Suggested common modeling policy for later *user*
adjudication:

1. **Typed prerequisite semantics:** generic operation
   links are permitted as *component dependencies*
   only with explicit contextual instantiation, not
   claims that the entire parent object is identical
   to the component.
2. **Context discipline:** if assumptions differ
   (unital/nonunital, commutative/noncommutative,
   left/right module, Set/class-valued, degree/index
   range, empty/nonempty), preserve the qualifiers and
   keep genuinely different mathematical meanings
   separately identifiable.
3. **Source evidentiary discipline:** unverified provider
   conventions are bounded deferrals, not endorsed
   conventions; only an independently supported
   source-specific review can remove them.
4. **Transaction discipline:** no alias, source correction,
   missing candidate resolution, graph amendment or
   gate transition follows automatically from these notes.
   Review exact live versions and avoid self-references
   before proposing any later packet.

The earliest low-risk future *proposal* set, conditional
on later approval, is clarification of ranks 40, 54,
181, 250, 259 and 400; these have direct counterexamples
to an overly broad wording/scope. Fixing a candidate
description still requires a supported version-bound
workflow and must not be achieved by editing protected
registries manually.
