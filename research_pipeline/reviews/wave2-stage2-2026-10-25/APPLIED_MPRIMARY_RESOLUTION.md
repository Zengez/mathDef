# Wave 2 applied noncircular m-primary / ideal-of-definition reconciliation

**Checkpoint:** 2026-10-25; independent Wave 2 graph on `main` only.
The historical 421/421 canonical identity review remains immutable in draft PR #10.
No new definitions, external research, source edits, consolidation decision or
Pass 3 transition.

## Mathematically reviewed identity and circularity

Candidate `missing.b963edbe734f35266d3a` is the predicate "I is m-primary"
in a **commutative unital Noetherian local ring (R,m)**. The existing
`meaning.b9defeff446a0526.ideal-of-definition-local-ring` is defined in
that context by `sqrt(I)=m`, equivalently m-primary. If `ab∈I`, `a∉I`
and `sqrt(I)=m`, then b cannot be outside m (otherwise b is a unit and
a∈I); so b∈sqrt(I) and some power of b lies in I. The ideal is proper
since m is proper. Thus I is m-primary; the reverse radical condition is
part of the m-primary predicate. Local/Noetherian evidence was examined in
the independent source and meaning variants. No general adic,
noncommutative, nonunital or zero-ring equivalence is claimed.

The first attempted read-only simulation identified a **real graph
provenance dependency**: the defining source was the sole active owner of
the canonical candidate, while the system-of-parameters source retained
only an observed pre-alias candidate ID. Retiring the defining self-edge
before resolving therefore temporarily removed the canonical ID, causing
the real resolution dispatcher to reject it. This unsuccessful simulation
was confined to a disposable workspace; it was NOT submitted.

The revised, successful transaction groups **two** complete-node
amendments before one resolution:

1. In `form.22c049b8eee93897.system-of-parameters`, re-anchor only
   its observed `m-primary` reference to the mathematically reviewed
   canonical candidate (explicit reusable-candidate rationale).
   Preserve the source phrase, its separate existing ideal-of-definition
   prerequisite, all other references and the original raw node and
   alias ledger history.
2. In `form.b9defeff446a0526.ideal-of-definition-local-ring`, reclassify
   the `m-primary ideal` self-reference to an external/provenance
   equivalent-characterization occurrence. The raw screened formulation
   still states the equivalence and `sqrt(I)=m`; the definition no longer
   depends on a meaning resolved to itself.
3. Resolve the now genuinely live `missing.b963edbe734f35266d3a` in
   the *other* source to the existing ideal-of-definition meaning. Do not
   identify the entire system-of-parameters construction (which also
   chooses dimension-many generators) with that predicate.

The prior alias event
`alias.global-audit.20261023.051` remains immutable in its ledger.
The originally observed source occurrence is preserved in original
node/amendment history. Its distinct observed alias no longer needs an
active registry entry after explicit canonical re-anchoring, so **active
aliases decrease from 301 to 300**; this is not deletion of historical
alias events. Missing-candidate registry decreases from 728 to 727.

## Exact executed transaction and receipts

- Disposable complete-workspace Python trial on branch
  `codex/wave2-mprimary-self-reference-trial-2026-10-25`:
  [GitHub Actions run 40239123991](https://github.com/Zengez/mathDef/actions/runs/40239123991)
  **SUCCESS**, 208 tests with two expected skips. The actual
  `build_review_packages`, `review_preflight`, `apply_inbox` and
  **19/19 exhaustive mechanical readiness checks** passed. No file in
  `main` was changed during the trial.
- Grouped exact inbox submission commit
  [`a0dde72`](https://github.com/Zengez/mathDef/commit/a0dde72afac374bb80b231b82d1c4d10c6d97442).
  Both packets entered in one commit; lexical dispatcher order puts
  `amend` before `resolve`.
- Amendment packet
  `amend-mprimary-selfreference-20261025-001`,
  SHA256 `8c9ba8c6e6b67c397c08c6950c5a0b998106ea892643b87a4e052bf80d677da4`.
- Resolution packet
  `resolve-wave2-mprimary-noetherianlocal-20261025-001`,
  SHA256 `a6e41ea7f038971cdb00fa40487da2054820f864b3ddf963658f7e435e258eef`.
- Actual independent graph
  [Action 40239363403](https://github.com/Zengez/mathDef/actions/runs/40239363403)
  **SUCCESS**. Both committed receipts match their respective package ID,
  mode, exact SHA256, and status `applied_in_independent_graph_only`;
  `human_certified=false`. Graph checkpoint
  [`3e8d94c`](https://github.com/Zengez/mathDef/commit/3e8d94cb664262647e7333751b0bfea304de1303).
- Independent read-only postapplication verification on branch
  `codex/wave2-mprimary-postapplication-verification-2026-10-25`:
  [GitHub Actions run 40239511795](https://github.com/Zengez/mathDef/actions/runs/40239511795)
  **SUCCESS**, 208 tests (two expected skips), **19/19** exhaustive
  mechanical checks, preserved old raw source/provenance, absence of
  defining self-edge, exact resolved source occurrence and matching
  receipts. Consistency scanner returned 20 contextual review leads with
  zero mechanical integrity findings; global scanner returned 9 review
  leads, neither automatically a mathematical defect.

## Current live checkpoint

- Source inventory SHA256: `34f61b6cf7fd1e80bda932dc8eeac473a729b11dfa0ba849c6db424b7a8f8113`.
- Unresolved fingerprint: `7b69e2fdcb30a4536883df44308d386219b7621533886d65276b8992959f4773`.
- **611 meanings**, **659/659 complete formulation scans**,
  **418 unresolved canonical missing identities**, **841 missing
  occurrences**, **727 registry candidates**, **300 active aliases**
  (historical alias ledger events preserved), **9 candidate resolutions**
  and **775 amendment events**.
- 2,638 reviewed existing-dependency edges at postcheck.
- `phase=consolidate_occurrences`,
  `consolidation_gate_valid=false`, **Pass 3 unauthorized**.

The earlier applied shifted-operator alias, real-time filtration correction,
Ext/Hom and local-connectedness edge amendments, and order-zero S-linearity
resolution remain separate immutable applied transactions. Never resubmit them.

Engineering draft PRs #11 and stacked #12 remain **unmerged**. Their
reference-ID-safe preparer and receipt-backed status need integration
against updated `main` without changing the protected graph; PR #10 is
historical and should not reset it. This review and its valid receipts do
not replace independent source certification or authorize consolidation.
