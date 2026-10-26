# Chat mathematical adjudication: A06–A09 (14 historical cases)

**Status:** source-free mathematical scope review, **not user policy
ratification**, graph correction, proof of original citations, consolidation
decision or permission to begin Pass 3. Evaluated against Codex's read-only
live-graph evidence at `9d4aa90260ed51d5e387aeede8a6683c9cbff20f`.
Earlier cards A01–A05 are documented separately in
`CHAT_ADJUDICATION_A01_A05.md`.
No protected graph or frozen corpus file was touched.

## A06: polynomial, quotient and selected-map prerequisites (five)

**Rank 3 — `missing.50fc57153b93520a247a`, quotient ring R/I.**
The quotient's ring operations descend exactly when I is an ideal.
This generic construction is a valid constituent of the 16 listed sources;
the quotient ring alone does **not** encode a specified ring map,
square-zero kernel, R-algebra structure, flatness criterion, local
completion, or lifting problem. The maps
`k[ε]/(ε²)→k` and `k→k` have isomorphic quotient targets
but different kernels. **Adjudication:** shared typed
*component prerequisite* is justified; replacing compound extension
data by the quotient is false. No segmentation or alias change yet.

**Rank 5 — `missing.9db64b2f9cdb8258e3d8`, polynomial ring.**
A formal polynomial `P(T)` and its evaluation `P(x)`
belong to different objects; e.g. `T≠0` in `k[T]` but
`P(0)=0` for `P=T`. The universal polynomial
ring over an arbitrary set of variables permits each polynomial
to have finite support without the variable set being finite.
A finite presentation source adds chosen evaluation/quotient
data, and the strong-transcendence source uses a value in S.
**Adjudication:** preserve a generic formal-polynomial
prerequisite with explicit evaluation/component typing. Do not
equate evaluated expression or an injective map with the polynomial
object. Reconcile identity-preserving inclusion at rank 133 separately.

**Rank 268 — `missing.76cef49793a8851de7db`, presentation.**
A chosen tuple of finite generators, finite relations and an
R-algebra isomorphism is **data**; finite presentability asserts
existence of such a tuple. A ring may have distinct presentations,
e.g. `R ≅ R` and `R ≅ R[T]/(T)`. Either zero generators
or zero relations may be legitimate; no source-based exclusion
established. **Adjudication:** no self-resolution to the
finitely-presented property. Keep the chosen isomorphism, list
lengths and scalar compatibility explicit.

**Rank 294 — `missing.8d90dbc484b53274e726`,
ring quotient versus module quotient.**
The ring `R/J` and module `M/JM` differ in type:
`M/JM` is an `R/J`-module via
`(r+J)(m+JM)=rm+JM`. The quasi-regularity
comparison additionally involves a tensor product, graded
ideal-action quotients and a specific map. **Adjudication:**
valid distinct component prerequisites; no single "quotient"
candidate can replace their compound data.

**Rank 298 — `missing.8f2dea7e2bd1211c0cf6`,
zero-divisor explanatory phrase.**
The universal implication of strong transcendence quantifies
over arbitrary `u`, including `u=0`, and does not require
nonzero factors in an annihilation equation. The currently stored
annihilator-based zero-divisor predicate allows zero in a nonzero
ring, while the missing canonical phrase presupposes nonzero
zero divisors; they are **not** an exact match. The phrase is
explanatory, not necessarily a named theorem dependency.
**Recommendation (not approved):** retain the source's
annihilator equation; consider an external/provenance disposition
for an explanatory phrase if a whole-node review justifies it.
Never equate distinct zero-divisor conventions merely to close a
candidate.

**Shared A06 recommendation:** prerequisite-typed links can
stand alongside compound source formulas; do not forcibly split
every formula, but do not label the *whole* formula as identical
to one component. Any later split is a separate source-anchored
transaction, not automatically implied by this adjudication.

## A07: naturality, Hom universes, categorical epi (three)

**Rank 62 — `missing.a8c70a2a13320680c54c`,
natural transformation.**
A natural transformation between presheaves is a family of
component functions satisfying a naturality condition.
The Yoneda correspondence and a particular Yoneda component
are not this transformation as whole data, and
presheaf fibre products use two transformations to a common
codomain. **Adjudication:** generic Set-valued natural
transformation may serve as a constituent when source and
target functors/variance are instantiated; do not identify
the entire Yoneda bijection or fibre-product object with one
component map.

**Rank 393 — `missing.e834133a2cdc7390f1de`,
adjunction Hom bijections.**
For `L:C→D` and `R:D→C`, the datum is
a family `Hom_D(LX,Y)≅Hom_C(X,RY)`
*natural contravariantly in X and covariantly in Y*.
A category with a proper class of objects can be locally small,
so local smallness cannot be replaced by category smallness.
Set-valued Hom requires locally small or explicitly chosen
universe conventions. **Adjudication:** retain source-convention
deferral (local smallness/universe); no restriction to small
categories or claim of provider verification.

**Rank 420 — `missing.fe199606757d4b449fee`,
multiplication isomorphism criterion.**
In the category of commutative unital rings, a map
`R→S` is an epimorphism precisely when
`μ:S⊗_R S→S` is an isomorphism. The map
`μ(s⊗t)=st` is not interchangeable with the
*assertion* of invertibility or the categorical epi property;
the latter is whole-parent content. `Z→Q` is a
categorical ring epimorphism but not a surjective set map.
**Adjudication:** distinguish the canonical multiplication
map, its isomorphism predicate and category-specific
epimorphism. Preserve commutative/unital conditions; no
automatic surjectivity alias.

## A08: clopen generality and corrected local connectedness (two)

**Rank 38 — `missing.b599bdc9343a25050226`,
clopen subset.**
The underlying condition `U⊆X` open and closed is
a generic topological predicate. In a spectrum,
the extra ring and idempotent correspondence is a
specialized characterization, *not* a universal property of
clopen subsets of arbitrary spaces. A space can be connected
on the empty-allowed convention even when another stored
connectedness formulation insists on nonemptiness.
**Adjudication:** generic clopen predicate is a valid
instantiated prerequisite; do not rewrite the canonical
spectrum-specific wording as a general theorem by alias
alone. Preserve both connectedness source conventions.

**Rank 399 — `missing.eb8e1a62d06acf7c487c`,
connected neighborhood systems.**
For each `x`, a cofinal system of connected neighborhoods
implies each component of each open U is open: choose a
connected neighborhood contained in U, then an open
neighborhood within it; connectedness forces the former
to lie in the component. Applying at all x gives a connected-open
basis. **The equivalence is of space properties, not of
individual systems with a global basis**. The old wrong direct
basis edge was already repaired by an earlier
receipt-verified transaction, and the pointwise missing
candidate remains live.
**Adjudication:** historical flag *already corrected*;
no repeat amendment, no automatic resolution of this
remaining pointwise candidate to the topology-basis meaning.

## A09: L1 index scope and Stieltjes conventions (four)

**Rank 36 — `missing.826fb5c503bdaf25ce7f`,
integrability.**
A real variable's predicate `E|X|<∞` can be
instantiated for each time index, but statements
`∀n∈N E|X_n|<∞` and
`∀t≥0 E|X_t|<∞` are different requirements.
Choose a nonintegrable Z and let `X_n=0` at integer
n but `X_t=Z` at other real t to witness the difference.
Pointwise finiteness also does not imply a uniform
bound on expectations. **Adjudication:** a single-variable
L1 condition can be the shared prerequisite, provided
each parent's whole quantified index set remains visible.
Do not conflate discrete and continuous martingales.
The corrected historical filtration edge is separate.

**Rank 166 — `missing.2216f1dfe187a7af152c`,
Stieltjes measure.**
For a suitable *right-continuous* nondecreasing function
`α`, assigning `μ((a,b])=α(b)−α(a)`
is conventional. Bare monotonicity with the wrong sidedness
fails countable additivity: `α(t)=1_{(0,∞)}(t)`
would assign measure 1 to `(0,1/n]` for every
n, although those sets decrease to empty and would
lie in a finite-measure interval. A left-continuous
normalization might use alternative half-open sides.
**Adjudication:** cannot select normalization or interpret
"admissible" without checking the original provider.
Never equate every Stieltjes measure with one having a
Lebesgue density.

**Rank 291 — `missing.8b4a695691c7d8e62f73`,
Stieltjes monomial integral/raw moment.**
A general `∫f dμ` operation is a reusable
prerequisite, whereas `∫x^n dμ` for specified n
and interval is the already-stored raw-moment value.
If `μ=δ_a`, whether the left endpoint is included
changes `∫x^0dμ` by 1.
**Adjudication:** do not resolve the candidate to the
whole moment meaning (self-reference risk); retain
parameterized integration and the pending endpoint
convention from rank 166.

**Rank 364 — `missing.ca3087282d7220fbe8f5`,
points of increase.**
A measure with atoms at infinitely many integer points
can have infinitely many jumps while its distribution
function is constant between jumps, so infinite increase
points must not be replaced by strict increase at every
point, or by `α'>0` almost everywhere. A finite
support `{a_i}` forces the nonzero polynomial
`∏(x−a_i)` to have squared norm zero, explaining
why infinite support matters for nondegenerate
orthogonal polynomials of arbitrary degree; that
motivates but does not certify a source's precise
"point of increase" definition.
**Adjudication:** leave source-specific convention open
and preserve moment/integrability requirements.

## Status / continuation

- This round reviewed **14 cases**: historical ranks
  `3,5,268,294,298,62,393,420,38,399,36,166,291,364`.
- With A01–A05, **30 of 40 historical cases** have
  source-free mathematical adjudication writeups, including
  rank 399's preexisting applied correction.
- None of these determinations is a source verification,
  automatic user policy approval, identity alias, resolution,
  seed override, scan amendment, new mathematical definition,
  or consolidation gate change.
- The remaining ten cases are A10–A13: ranks
  `172,223,245,405,40,250,181,259,324,154`.
