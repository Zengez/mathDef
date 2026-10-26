# Source-free correction design: generic prerequisite scopes and alias provenance

**Decision class:** exact-live-snapshot **proposal only**, not an accepted
mathematical graph correction. This document and its companion
`REANCHORING_OPTIONS.json` use source, graph and registry evidence pinned
by `EVIDENCE.json` and `EXACT_EFFECTIVE_OCCURRENCE_REVIEW.json`.
The project owner approved *typed component-prerequisite semantics*,
**not** any particular alias reversal, candidate-context modification,
new missing identity, or packet application. The current graph,
Pass 2 gate, all mathematical sources, and all alias histories are unchanged.

## Central distinction: the aliases' rationales were mostly correct

The six rank-36/38 cases are **not** proof that the historical alias
reviewers conflated mathematically different full martingale or
connectedness definitions. In fact the original recorded rationale
for alias `alias.global-audit.20261023.128` expressly says the
shared term is **single-variable L¹ integrability** and *the
index set remains part of its original parent*.
`alias.global-audit.20261023.141` likewise treats integrability
of X and Z as individual-variable instances; alias
`alias.global-audit.20261023.217` explicitly excludes a
uniform-in-n expectation bound. Thus the current canonical
`missing.826fb5c503bdaf25ce7f` is **too specifically
described** as the whole statement
`∀t∈[0,∞), E|X_t|<∞`, despite the intended
common prerequisite being **E|Y|<∞ for one real-valued
random variable Y**.

Similarly, `alias.global-audit.20261023.013` originally
identifies the generic clopen predicate in X, and alias
`alias.global-audit.20261023.121` explicitly preserves
connectedness's empty/nonempty convention separately.
The surviving representative
`missing.b599bdc9343a25050226` is instead
narrowly described as **U⊆Spec(R) clopen**. That is
a *valid specialization*, but not an appropriate general
description for three arbitrary-space parent occurrences.

**Correct semantic interpretation:** two common **generic**
prerequisites with specialized parent instances.
No source formulation or historical alias rationale must
be declared mathematically false just because the chosen
representative context is too narrow.

## Mathematically preferred representative meanings

### Integrability — historical rank 36

**Generic candidate meaning desired:** Let
`Y:Ω→R` be a measurable real-valued random variable
on a probability space. `Y` is **integrable**
(`Y∈L¹`) iff
`E|Y|=∫_Ω |Y|dP<∞`.

- Conditional expectation requires this separately for
  input X and the chosen integrable output Z.
- Discrete-time martingales require it for each
  `n∈N_0`, **not** uniformly bounded expectations.
- Real-index martingales require it for every
  `t∈[0,∞)`; their time index and filtration remain
  in the parent, not in the generic prerequisite.
- None of these cases equates conditional expectation,
  discrete martingales or real-index martingales.

Keep the existing canonical and alias history as
**provenance**; do not silently mutate
`missing_candidates.jsonl` to change its meaning or
rewrite the old aliases to suggest their contexts were equal
as fully quantified process properties.

### Clopen — historical rank 38

**Generic candidate meaning desired:** For a topological
space X, a subset U⊆X is **clopen in X** iff U is
both open and closed in X. Equivalently, U and
X\U are open.

- All three generic connectedness source formulations
  use this predicate in an arbitrary topological space.
- The affine-spectrum parent uses the instance X=Spec(R).
  Its additional idempotent characterization is **not**
  the definition of generic clopen.
- Empty-space connectedness variants and nonempty-space
  connectedness variants remain separately recorded.

The alias rationale only supports a **generic clopen
prerequisite**. The narrower spectral canonical text cannot
be used as proof that an arbitrary topological space is
the spectrum of a ring.

## Exact affected occurrences

The following effective references were verified against
the pinned current graph: source SHA256 and effective-node
SHA256 are specified **in full** in
`REANCHORING_OPTIONS.json`.

| Rank | Formulation | Occurrence ID | Intended generic predicate |
| --- | --- | --- | --- |
| 36 | `form.wave2.found85.conditional-expectation` | `occ.3eda46790ce1c2aed5c5` | L¹ integrability of X and Z |
| 36 | `form.wave2.research81.martingale-discrete.01` | `occ.b8df608b462159d8948d` | Each real-valued X_n is integrable |
| 36 | `form.wave2.research81.martingale-discrete.02` | `occ.98619b3d2a58ee9006e9` | Each real-valued X_n is integrable |
| 38 | `form.ab260940ea9c523d.connected-topological-space` | `occ.417c86f577e85affc4cb` | Clopen in arbitrary X |
| 38 | `form.wave2.pop141.connected-clopen` | `occ.00775f87f3c5601a0719` | Clopen in arbitrary X |
| 38 | `form.wave2.variant71.connected.02` | `occ.1612dec2b099f44c923b` | Clopen in arbitrary X |

The two specialized representative uses, which remain
mathematically coherent, are:

- Rank 36: `form.wave2.research81.martingale-continuous-index.01`,
  `occ.2cf87f7b73f5c5a33bb4`.
- Rank 38: `form.097db25e2f156689.clopen-subset-of-spectrum`,
  `occ.982109ad4faf2e20b72d`.

**No proposed fix may rewrite or delete these parents'
original defining quantifiers, spectral setting or citations.**

## Technical constraints proven from current engineering code

Reviewed `research_pipeline/engine/dependency_global_audit.py`,
`dependency_review_export.py`, `dependency_review_preflight.py`
and `dependency_graph.py` on the current integration branch.

1. The missing-candidate registry is a **derived index** of
   original observed reference phrases and contexts plus
   historical alias events; it is not an editable source of
   mathematical truth. Its active representative context
   can be narrower than its aliased dependents.
2. The ordinary reviewed manifest `build_review_packages()`
   explicitly rejects *new missing-candidate identities*
   and requires source inventory + unresolved fingerprint,
   exact effective node SHA256 and stable occurrence ID.
3. Its delta-edit path forbids assigning/removing a
   `missing_candidate_id`. Its full-reference
   replacement path also requires the replacement missing
   candidate to be **already registered**, or else
   construction fails. The original generic observed IDs
   in all six cases remain **aliased** and are not
   unresearched reusable canonical identities.
4. Existing alias ledger replay is **append-only** and
   flattens chains; there is no approved inverse
   alias/unalias action. Do not delete the two historical
   clopen aliases, three historical integrability aliases,
   or their old reviewer rationales.
5. Demoting a still-valid needed prerequisite to
   `external`, `unassigned`, or `deferred` solely
   to make an error count drop would conceal the intended
   dependency, possibly upset Phase 2 completeness, and
   is **not recommended**.
6. No existing graph meaning for **general clopen**
   or **single-variable L¹ integrability** was found
   in the checked current `INVENTORY.json` meaning
   descriptor catalog. Therefore a supposed direct
   `existing` correction has **no supported target**
   in this evidence snapshot.

### Preferred future engineering capability (not implemented)

Implement a **guarded, append-only, versioned reviewer-context
adjudication** for canonical missing identities, permitting
an approved *semantic-scope clarification* to coexist with
immutable original observed contexts and immutable aliases.

A minimal viable design could use a new **adjudicated
interpretation metadata** overlay keyed by canonical
candidate ID and pinned to:

- current source inventory and candidate/alias
  fingerprints;
- canonical candidate ID, exact observed alias set
  and full incoming occurrence IDs;
- the old canonical context, verified source text,
  proposed generic meaning and a mathematical proof;
- explicit scoping rules: specialization in the
  real-time/spectral parent, generic prerequisite in
  other parents;
- reviewer, applied-receipt ID and append-only history.

Requirements before approving that engineering addition:
replay must fail closed on changed alias history, missing
source versions, conflicting adjudications or stale
candidate usage; the UI/audit API must distinguish
reviewed contextual meaning from the immutable
historical representative text; existing source/graph
files and original alias observations must remain
inspectable and byte-identical until an **explicit**
newly approved transaction; tests must cover positive
and negative index/universe cases and duplicate/stale
events. The metadata **must not** disguise actual
non-equivalent candidates as synonyms.

**Alternative** if the project explicitly wants scoped
missing identities instead: a new strictly controlled
reviewed-missing-candidate creation/split workflow,
preserving old canonical and alias history with
versioned supersession and per-occurrence reanchoring.
This is substantially more invasive. Do not simply
append a reverse alias or invent an unregistered key;
existing alias replay and current preparer would reject
or flatten it.

**Status:** neither pathway was implemented here.
Whether to create a new metadata capability or wait
until subsequent missing-definition research is a
software/phase decision, not a mathematical theorem.
The scientific result (two generic prerequisites
are shared) is already clear under the approved policy.

## Independent rank-298 caveat

`missing.8f2dea7e2bd1211c0cf6` calls a
zero-divisor concept a needed prerequisite of
strong transcendence. The parent statement has no
"zero divisor" term and quantifies over all u,
including u=0. Its implication does not posit
two nonzero annihilating elements. Consequently the
new scan phrase "zero-divisor phenomena in S" is at
most an *explanatory analogy*, not a prerequisite
forced by the source's wording. Do not resolve it
to the existing zero-inclusive annihilator predicate.
An **optional future** reviewed full-reference
replacement could reclassify this *single* occurrence
as `external` with a qualified explanatory
disposition, after mathematical reviewer authorization
and standard full-node, version-bound preflight.
Its exact live anchor is in
`EXACT_EFFECTIVE_OCCURRENCE_REVIEW.json`.
This is not an accepted amendment.

## Next safe work

- Keep these **six** occurrences visible as
  unresolved scope mismatches until a validated
  correction mechanism exists. Do not let them
  disappear under a phase-gate declaration.
- Maintain the other 20/26 reviewed cases'
  mathematical context conclusions and the
  separately pending 13 provider convention cases.
- Audit remaining specialized candidate overlaps
  (ranks **172, 223, 245**) against all effective
  meaning-level paths before any attempted resolution.
  Avoid cycle/self-reference introduced by resolving
  a missing candidate to its own parent meaning.
- Prepare Codex engineering handoff only if/when
  implementation is authorized; no protected graph,
  frozen Wave 1 or production changes are authorized
  by this design.
