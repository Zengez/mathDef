# Exact effective occurrence audit — 26 prioritized cases

**Review status:** completed as a **source-free, read-only** mathematical
judgment against the existing Wave 2 live-graph evidence checkpoint.
No candidate/source/meaning/graph/alias/receipt changes applied.
The default typed component-prerequisite policy is already
owner-approved; this report does not treat that approval as authority
to make individual edits, resolve candidates or open the gate.

**Input / exact evidence:** the complete, previous live-graph
`EVIDENCE.json` capture, checked against
`POST_POLICY_TRIAGE.json`,
`ADJUDICATION_QUEUE.json`,
`CHAT_ADJUDICATION_A01_A05.md`,
`CHAT_ADJUDICATION_A06_A09.md`, and
`CHAT_ADJUDICATION_A10_A13.md`.
The new [exact-reference ledger](EXACT_EFFECTIVE_OCCURRENCE_REVIEW.json)
records each observed/canonical candidate identity, phrase, effective
occurrence ID, parent meaning/source, exact source-version SHA256,
effective-node SHA256 and scoped mathematical disposition.

## Validated coverage and integrity

- **26 historical cases**: 20 contextual component cases plus the
  six mathematical qualification cases (historical ranks
  **40, 54, 181, 250, 259, 400**).
- **72 historical parent visits**, containing **73** effective
  missing-candidate occurrences. Rank 62 contains two distinct
  occurrences in one of its parents.
- **73/73** recorded current missing-candidate occurrences
  agree with the corresponding effective references in the complete
  Codex evidence capture, including observed aliases and canonical IDs.
- **72/72** captured source-version SHA256 and effective-node
  SHA256 pairs match the containing authoritative live-context
  evidence objects. No source versions or effective nodes changed
  since the historical review for these 26 cases in that capture.
- **Zero** directly resolved self-links to the parent meaning
  in this 26-case effective-reference subset; a *potential
  future self-reference* still has to be avoided when proposing
  new resolutions or aliases.
- The GitHub evidence branch differs from the engineering base
  only by review-directory files, so this source-free pass
  **did not import an older graph snapshot**.
  Spot-checked current raw parent nodes are consistent with
  the recorded historical scan. These checks validate the
  **pinned evidence checkpoint**, not a newly rerun full graph
  reconstruction or external source certification.

## Six specifically identified candidate-scope mismatches

All six are instances of the **candidate description being too
specialized for an otherwise valid generic prerequisite**.

### Rank 36 — integrability, three occurrences

Canonical `missing.826fb5c503bdaf25ce7f` currently means
`E|X_t|<∞` **for every real t≥0**. That quantified process
property is not what the following parents are referring to:

| Parent | Effective occurrence | Valid required predicate |
| --- | --- | --- |
| `form.wave2.found85.conditional-expectation` | `occ.3eda46790ce1c2aed5c5` | `E|X|<∞` and integrability of Z, with no process |
| `form.wave2.research81.martingale-discrete.01` | `occ.b8df608b462159d8948d` | `E|X_n|<∞` **for every integer n≥0** |
| `form.wave2.research81.martingale-discrete.02` | `occ.98619b3d2a58ee9006e9` | Discrete-time componentwise integrability |

The real-time martingale parent
`form.wave2.research81.martingale-continuous-index.01`
does instantiate the narrower canonical real-time condition.
Neither a discrete-time family nor an isolated random variable
has the all-real-time property as written. **Proposed non-applying
remedy:** preserve both the generic single-variable
`L^1`-integrability predicate and each quantified
discrete/real-time specialization in the future dependency
model. Do not merge martingale definitions or repeat the
already-applied real-time *filtration* correction.

### Rank 38 — clopen predicates, three occurrences

Canonical `missing.b599bdc9343a25050226` currently means
a subset `U⊆Spec(R)` that is simultaneously open and closed
in the Zariski topology. The following parents instead use
arbitrary topological spaces:

| Parent | Effective occurrence | Valid required predicate |
| --- | --- | --- |
| `form.ab260940ea9c523d.connected-topological-space` | `occ.417c86f577e85affc4cb` | Generic clopen subset of X |
| `form.wave2.pop141.connected-clopen` | `occ.00775f87f3c5601a0719` | Generic clopen subset of X |
| `form.wave2.variant71.connected.02` | `occ.1612dec2b099f44c923b` | Generic clopen subset of X |

The spectral parent
`form.097db25e2f156689.clopen-subset-of-spectrum`
legitimately instantiates the specialized candidate.
**Proposed non-applying remedy:** use a generic clopen
subset predicate, with a separate specialization or contextual
instantiation for the spectrum/idempotent correspondence.
Do not rewrite all topological spaces as spectra, or identify
the idempotent correspondence with the mere clopen predicate.

**Important:** The six cases above are mathematical *scope*
mismatches to prepare for a separately authorized
candidate recontextualization or occurrence reanchoring.
They are not six newly applied graph errors or permission
to edit `missing_candidates.jsonl` directly.

## Other consequential findings from the 73 exact links

### The clear wording qualifications still have live consequences

- **Rank 40, four occurrences:** the generic root prerequisite is
  valid; the canonical example's phrase "residue class in
  `k[x]/(f)` for nonconstant f" wrongly treats an arbitrary
  nonconstant quotient as a *field*. Each source parent that
  actually needs the field construction already states
  irreducibility. Correct **candidate/example wording** rather
  than accusing those source parents of the same error.
- **Rank 54, three occurrences:** all three parent effective
  reference sets include the intended **unital module** meaning,
  making the usual finite-linear-span prerequisite justified
  under that assumption. The first finite-generation parent
  also has a separate broader historical seed to the
  identity-optional module: this is a **scope/seed
  consistency issue to document**, not grounds to assume
  the unital span formula holds under zero action.
- **Rank 181, one occurrence:** canonical research context says
  "unordered doubleton {a,b}", which is false if a=b; its
  **parent Kuratowski construction is correctly stated for
  arbitrary a,b**. The eventual wording should be "unordered
  pair, possibly a singleton".
- **Rank 250, one occurrence:** canonical context already
  notes characteristic zero is automatic, but "coprime to
  characteristic" benefits from an explicit interpretation
  `n·1_K` invertible. Do not use `gcd(n,0)=1`.
- **Rank 259, one occurrence:** the canonical context contains
  two logically different claims in general partial orders:
  "no greatest element" and `∀a∈A ∃b∈A : a<b`.
  The latter is **no maximal element**; it implies no greatest
  in nonempty A but not conversely. They coincide when A
  is a subset of a total order, as in the **correctly scoped**
  Dedekind rational-cut source. Qualify the candidate,
  not the already valid Q-cut parent.
- **Rank 400, one occurrence:** the parent/source description
  does **not** actually assert B-linearity of the de Rham
  differential. The present generic cochain candidate is
  a plausible underlying dependency, but its scalar ring
  should explicitly be A: `d` is A-linear and
  generally not B-linear. Preserve B-module graded
  terms and wedge/Leibniz structure; this is an
  **incomplete typing note**, not a demonstrated false
  B-linearity assertion in the source.

### Compound/component links and explanatory overlink

- **Ranks 172, 223, 245:** source and candidate already
  describe respectively the **same specialized** degree-zero
  localization, specific K_0 group completion, and specific
  I-adic inverse limit. A general operation is a legitimate
  prerequisite, but resolving those candidates back to
  their *own* parent meaning would create a conceptual
  or direct defining self-edge. Generalize the prerequisite
  only under reviewed scope; do not naively auto-resolve.
- **Ranks 222, 294, 323, 420:** candidate phrases bundle
  multiple typed components—quotient sheaf/pushforward,
  ring quotient/module quotient, ideal/residue data,
  and multiplication map/isomorphism predicate. Under the
  approved policy each component can be a prerequisite,
  but no one component should replace the whole datum.
  Segmentation remains a potential later action.
- **Rank 298, one occurrence:** `zero-divisor phenomena in S`
  was added as an explanatory dependency; the actual
  strong-transcendence formula allows `u=0`, and does
  not assume two nonzero annihilating elements. The
  current canonical nonzero zero-divisor concept is
  **not entailed** by the source phrase. This is a
  **possible unnecessary link**, suitable for an exact
  occurrence-level proposal to classify as external
  explanation after separate review, rather than a
  speculative alias to a zero-inclusive definition.
- **Rank 18, six occurrences:** the nilpotent-ideal
  parent uses an identity-optional ring and only positive
  ideal powers, whereas the current shared canonical
  context requires commutative unital coefficients.
  That particular parent requires **source convention or
  broader typed-operation review**, not a blanket claim
  that the shared canonical satisfies every general ring.
- **Rank 364, one occurrence:** the precise point of
  increase convention remains unverified from source
  and cannot be repaired by appealing to strict
  monotonicity or positive derivative.
- **Ranks 3, 5, 62, 95, 268, 405:** generic quotient,
  polynomial, natural-transformation, additive direct-sum,
  finite-presentation datum and localization
  prerequisites are mathematically appropriate as typed
  components with their source qualifications intact;
  no blanket graph reanchoring follows. The one
  rank-5 strong-transcendence evaluated-polynomial
  occurrence still warrants a separate form/value
  instantiation check.
- **Rank 324:** the partition is an **unindexed
  collection of blocks**. Calling it an indexed
  family only works after deliberately forgetting the
  indexing and multiplicity; preserve the empty
  partition's permitted case.
- **Rank 291:** generic integration is a reusable
  prerequisite, but the specified `∫x^n dμ` is the
  source's raw moment itself. Source-specific endpoint
  and atomic-measure convention remain undecided.
- **Rank 38/399 cross-note:** already corrected
  locally-connectedness edge at historical rank 399
  is a **separate event**, not one of these six
  clopen candidate-scope mismatches. Do not resubmit.

## Next carefully bounded work

1. Prepare **non-applying, version-bound correction options**
   for the rank 36 and rank 38 candidate-scope conflicts,
   keeping all observed aliases, original source texts and
   discrete/real-time + generic/spectral variants.
2. Investigate rank 298's possible extraneous reference and
   ranks 172, 223 and 245 for future self-links before
   recommending any graph transaction.
3. Prepare a separate **candidate-context clarification**
   plan for ranks 40, 181, 250, 259, 400; rank 54 additionally
   needs the historically broad module seed recorded.
4. Independently verify the original-provider assumptions
   of the 13 bounded source-convention deferrals and
   secondary ranks 18/291/364 in a later research phase.
5. Apply changes only with exact live source/node/occurrence
   anchors and separate approval, disposable preflight,
   immutable receipts, exhaustive readiness and consistency
   checks. Any unavailable supported registry-edit mechanism
   means documenting a proposal, not mutating a derived
   candidate file directly.

**No gate opening, Pass 3 transition, external-source
certification, or graph mutation is authorized by this report.**
The prior **254 tests passed + 2 expected skips,
19/19 mechanical checks and 2,293 protected-file identity**
are results of the preceding Codex read-only evidence pass,
not newly executed tests during this report-writing round.
