# Codex engineering handoff — reviewed generic missing-candidate contexts

**Purpose:** implement robust engineering **support** for a reviewer-approved
canonical missing-candidate context clarification without changing any
mathematical content in this task. **This request is not blanket approval
to adopt the six mathematical edits.**

## Verified scope and sources

- Read `APPROVED_DEPENDENCY_GRANULARITY_POLICY.md`,
  `GENERIC_SCOPE_CORRECTION_DESIGN.md`,
  `REANCHORING_OPTIONS.json`,
  `EXACT_EFFECTIVE_OCCURRENCE_REVIEW.json`,
  `EXACT_EFFECTIVE_OCCURRENCE_FINDINGS.md`
  and `POST_POLICY_CHECKPOINT.md` within this directory.
- Use current engineering integration PR #13 as the code base,
  with the **latest** main graph snapshot (verify heads and receipts).
- Historical ranks 36/38 are **two generic concept scopes**
  whose narrow canonical representatives are shared by a total
  of **six** mismatched parent-occurrence usages:
  **L¹ integrability of one real random variable** versus
  **real-indexed martingale entire quantified condition**,
  and **clopen subset of any topological space** versus
  **clopen subset of a spectrum**.
- The original five alias events explicitly justified generic
  component reuse; their historical event, raw observed context
  and provenance must remain intact.
- All 13 source-convention identities remain separate from
  this feature (see `PRIMARY_SOURCE_STATUS.json`).

## Engineering task

Review the existing engine support for canonical missing candidates,
immutable alias replay and guarded offline review export.
Implement the **smallest generic, reusable, domain-neutral feature**
that allows a **version-bound, explicitly reviewer-authored**
canonical candidate interpretation/context overlay while retaining
both the immutable observed reference/candidate records and all
legacy alias events. If a different design better preserves the
existing architecture and transactions, document the tradeoff
before implementation; **never overwrite the protected corpus
or alter a canonical candidate's meaning by silently editing
the derived registry.**

Requirements:

1. Authoritative append-only review events, each with unique ID,
   reviewed author, exact canonical candidate ID, the prior
   canonical description, the proposed interpretation,
   explicit alias/parent/occurrence coverage, source and
   effective-node version anchors, complete alias and
   resolution ledger fingerprints, mathematical rationale
   and provenance.
2. Correct deterministic replay, fail closed on stale
   source versions, changed aliases, changed resolution
   map, duplicate/reused event IDs, incompatible
   definitions, unknown or cyclic aliases, unapproved
   replacement, missing or changed occurrence.
   No historical event deletion/reordering.
3. Separate raw observed context from the **reviewed
   canonical interpretation** in all reader/auditor views.
   Never present a generic component as identical to
   its specialized parent whole definition.
4. Support read-only **preflight** on a disposable
   byte-identical workspace copy, with strict before/
   after file hashes and exact receipt-shaped validation
   evidence. Implement *no automated submit/apply*
   from a mere source-free research report.
5. Regression tests for: valid one-variable L¹ reuse
   at integer and real indices; valid generic clopen
   under arbitrary X and Spec(R); rejection of a
   homogeneous source whose quantified property is
   incorrectly generalized; safe specialized-parent
   retention; alias cycles/history; stale pins and
   deliberate malicious or malformed events; zero
   effects on existing graph if the overlay is absent.
6. No hidden assumptions of ring unitality, nonzero
   field, category smallness, index set, or source
   author convention. Mathematics remains a separate
   review layer, not a heuristic aliasing engine.
7. The new overlay is an engineering capability,
   not authorization to alter protected Wave 2
   mathematical graph content or gate state.

## Do not do

- No frozen Wave 1 reads/writes, production deployment,
  candidate discovery, source crawling, new math definitions,
  math-candidate context changes or live graph transactions.
- No Pass 3, consolidation acceptance or gate reopening.
- No loss of exact historical missing IDs/alias rationales.
- No unreviewed alias, inferred identity or automatic
  rewriting to "external" to satisfy gate counts.

## Deliverables

- Standalone integration feature branch **based on the
  current verified engineering branch** (check stacked PRs).
- Unit/integration tests and synthetic negative controls,
  read-only smoke and exhaustive readiness/consistency/
  provenance checks where available; report *actual*
  executed checks, not planned checks.
- Architecture/design record, exact changed paths,
  raw-byte protected-file manifest comparison,
  branch/commit SHA, durable checkpoint, and draft PR.
  If Codex's PR API denies permission, provide
  comparison URL for ChatGPT to create draft PR.
- The canonical scope proposals from
  `REANCHORING_OPTIONS.json` must remain **unapplied
  demonstration data** (or synthetic examples in
  tests) unless **separately authorized** in a
  later reviewed transaction.

If a safe solution requires changing the workflow
contract substantially, stop at a detailed design +
tests for non-mutating primitives, and explain the
specific decision needed. This task must never
silently create an applied mathematical correction.
