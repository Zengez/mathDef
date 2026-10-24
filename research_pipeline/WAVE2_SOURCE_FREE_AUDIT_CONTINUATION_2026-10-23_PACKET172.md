# Wave2 source-free audit continuation — packet 172 (October 23, 2026)

## Applied packet and verification

Packet **semantic-global-audit-missing-alias-172** was committed as c6f4437a139a420cfc948739d6ca77bbd220041c and applied **only** to the independent Wave2 dependency graph. Its receipt confirms mode alias, status applied_in_independent_graph_only, human_certified false, SHA256 442db30f6acec2a0c8cb32ddd1dbf2683fea396d46d95a3f4df35f0e81b8836b.

Both [graph CI 40051019746](https://github.com/Zengez/mathDef/actions/runs/40051019746) and [research-pipeline isolated tests CI 40051019801](https://github.com/Zengez/mathDef/actions/runs/40051019801) completed **SUCCESS**.

| Metric | Before | Verified after |
| --- | ---: | ---: |
| Existing meanings | 611 | **611** |
| Scanned independent formulations | 659/659 | **659/659** (639 screened, 20 provisional) |
| Raw candidate records | 724 | **724** |
| Applied reviewed alias events | 294 | **297** |
| Candidate-to-existing resolutions | 7 | **7** |
| Unresolved canonical candidate identities | 423 | **420** |
| Missing occurrence rows | 819 | **819** |
| Effective amendment events | 765 | **765** |
| Unassigned / ambiguous | 0 / 0 | **0 / 0** |
| Structurally open / closed | 651 / 8 | **651 / 8** |
| Consolidation gate valid | false | **false** |

Original inventory hash: 3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492. Current unresolved fingerprint: f740c264e171ba568241e8925c32efd5e53d8f528f8976fd7e9f9308a7300554.

## Three mathematically reviewed underlying prerequisite identities

Each alias was checked against full independent parent formulations and against the flat alias ledger (no chained aliases). Full mathematical rationales are recorded with the immutable packet.

1. **Coordinatewise integrability of stochastic processes:** missing.85b92abd4a39651a191c → missing.826fb5c503bdaf25ce7f. Both discrete martingale formulations and the continuous-index formulation require that each real-valued coordinate random variable is integrable, meaning finite absolute expectation. Changing the index set from nonnegative real times to nonnegative integers does not change the underlying L1 prerequisite. The process-index sets, adaptation, conditional-expectation equalities and absence of any uniform L1 bound remain distinct in the full parents.
2. **Unital ring isomorphism:** missing.a8be2a7ccf0364ad82c7 → missing.15bb96cb26d587868bbe. The complete-local-ring source requires a canonical unital ring map to its adic completion to have a unital ring-map inverse; this is a categorical isomorphism in the category of commutative unital rings, **not** merely an underlying set bijection. Completion and locality stay parent requirements.
3. **Topological group isomorphism:** missing.a6cf7564e7792b5d1129 → missing.15bb96cb26d587868bbe. The profinite-group source requires a two-sided-invertible continuous group homomorphism, a categorical isomorphism in TopGrp. Neither a group bijection lacking continuity nor a homeomorphism lacking compatibility with multiplication suffices. The inverse-limit condition remains parent-specific.

The latest read-only focus tool preserves actual observed source phrases, so the generic canonical identities should **not** replace structure-sensitive wording in user-visible definitions.

## Mathematical re-evaluation: quasi-finiteness and two meanings of local dimension

An earlier packet raised a possible false equivalence in the independent screened source formulation **form.3718becace9c852d.quasifinite-at-prime**: an isolated point in a finite-type fibre versus dimension-zero local fibre. That warning must now be narrowed.

**Interpretation A — Krull dimension of the local ring.** In X = Spec(k[t]), the generic point q = (0) has local ring O_(X,q) = k(t), a field. Its local ring has Krull dimension zero, although q is not an isolated point of X. Thus “local ring Krull dimension zero” is **not** sufficient for quasi-finiteness.

**Interpretation B — local topological dimension.** The independent source formulation **form.3fcd082413a6b2eb.relative-dimension-at-prime** defines relative dimension at a fibre point using local topological dimension. Specifically, for a point q of a space X, local topological dimension is the minimum of the dimensions of open neighbourhoods of q. For generic q = (0) in Spec(k[t]), every nonempty open neighbourhood has dimension one. Thus the same purported counterexample has **topological local dimension one**, not zero.

Moreover, a finite-type fibre over a field is a Noetherian scheme. There, **q is isolated in the fibre if and only if its local topological dimension is zero**. Forward implication: the singleton {q} is an open neighbourhood of dimension zero. Reverse implication: if q belongs to an open neighbourhood U of dimension zero, then U is a zero-dimensional Noetherian scheme with a finite discrete underlying space, so {q} is open in U, hence open in X. Therefore the quasi-finite equivalence can be mathematically valid under Interpretation B.

**Disposition:** do not edit the screened source or treat the old generic-point example as a refutation of every reading. Retain a terminology/cross-definition consistency question: make clear whether “local fibre dimension” denotes topological local dimension or dimension of the local ring. The distinction is substantive and context-dependent. Source or citation verification remains deferred under the source-free contract.

## Flat-alias structure prevents two superficially tempting merges

The already-canonical candidates for **invertible 2-morphisms** (missing.63d9809ad2eb842deb92) and **isomorphism over base category C** (missing.77eacb7314c513d85c72) both have preexisting incoming aliases. Their operations are special instances of isomorphisms in a hom-category or over-category, but merging either canonical into generic categorical isomorphism directly would create **chained aliases** forbidden by the append-only graph contract. We did not force the merge or rewrite historic events. A separately specified and audited re-canonicalization procedure would be necessary.

## Guardrails and next steps

No original mathDef data, frozen Wave1 data, screened/provisional mathematical texts, source citations, new meanings, or existing effective formulation amendments were changed. No external missing-definition research, breadth Batch143, human certification, premature freeze or gate opening occurred.

Next prefer exact source-sensitive review of (a) groupoid size conventions in three effective links using the corrected detector, (b) the surjectivity assumption in the submersive-map equivalence, and (c) constructible-set terminology over non-Noetherian rings. Further canonical synonym merging should occur only where contextual mathematics warrants it; 420 outstanding identities are **not** 420 verified absent definitions.
