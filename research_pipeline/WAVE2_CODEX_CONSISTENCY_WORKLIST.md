# Codex engineering report: source-free consistency worklist

Base: `ee1958454ebf1df5a0c73c58125036e842110c7e` (latest main, merged PR #4).
Branch: `codex/wave2-consistency-worklist`. No mathematical corrections applied.

## Interface and reuse

From the repository root:

```bash
python -m research_pipeline.engine.dependency_consistency_worklist \
  --workspace research_pipeline/experiments/reconstruction-v2-independent --limit 12
# Complete output, rather than treating a truncated page as an entire audit:
python -m research_pipeline.engine.dependency_consistency_worklist \
  --workspace research_pipeline/experiments/reconstruction-v2-independent --exhaustive
```

Reuses `load_live_snapshot`, global mechanical/scope diagnostics,
`effective_references` (amendments, aliases, version-bound candidate resolutions,
seed overrides), and existing `rank_findings`/review-ledger validation. Reuses
context-worklist's shared-source-table approach without invoking its additional
workspace loader. Provenance auditing remains separate: locator/source coverage
is not evidence of mathematical consistency. The existing cycle analysis is
summarized with its classification and formulation-choice witnesses; no stored
alternative is discarded or selected automatically.

New diagnostics:

- Explicit opposing qualifiers on shared object words: left/right,
  covariant/contravariant, unital/nonunital, small/unrestricted,
  nonempty/empty-allowed. These are contrasts, not certified errors.
- Restricted target heads whose qualifier is absent from reference, full source
  and context. Vocabulary is deliberately bounded; absence is only a lead.
- Open/closed/clopen subset references attached to the ambient topological-space
  meaning. Open-subset leads are omitted when target text explicitly defines
  open subsets. Closed/clopen predicates still require separate review.
- Identical normalized phrases with different effective target identities,
  within one formulation (including seed/scan disagreement) or across stored
  alternatives. No synonyms, duplicate names, or dependency-set differences
  alone establish a conflict.
- Existing strict integrity alerts, extended to unknown historical seed targets.

Broad ideal-vs-module-generation warnings are excluded from this queue: an ideal
can legitimately use a module prerequisite. They remain in the original scanner.
Negative controls also prevent optionally nonunital targets, explicit finite
categories/finitely many objects and morphisms, finite-type hyphenation, and
legitimate open-subset definitions from generating these particular concerns.

Output includes exact occurrence/seed IDs, full source and target definition
context, related effective references, source versions and node hashes. Shared
source/target tables avoid repeating complete definitions in every row. Source-
level leads have null occurrence IDs. Counts disclose omitted findings.

Existing impact/recurrence scores are reused with bounded evidence bonuses
(explicit contrast 120, predicate/ambient 100, missing restriction 40). Mechanical
integrity and high-severity findings stay above mathematical review leads.
Every lead retains uncertainty; none instructs automatic relinking.

## Review persistence and stale evidence

Optional `evidence_sha256` extends the existing audit fingerprint/ledger format.
It binds the detector revision, source references, related formulations, target
texts/versions and target effective-node hashes. An accepted review suppresses
only exactly matching evidence; changes in target definitions, seed IDs or
candidate resolutions cannot silently reuse a source-node-only acceptance.
Legacy fingerprints retain their original behavior in other audit tools.
Legacy reviews without the new evidence anchor do not suppress this worklist's
expanded evidence and are reported stale. The current live review ledger has
zero rows. This command never writes reviews or any ledger.

For separate authorized review recording, use `audit_fingerprint(finding)` from
`dependency_audit_acceleration`, plus `disposition`, `reviewed_by` and substantive
`rationale`. No ledger rows were created during this assignment. Confirmed
mechanical/high-severity alerts remain unsuppressible under existing rules.

## Current-instance demonstration

Live state: 611 meanings, 659 complete scans, 421 unresolved canonical candidates,
770 amendments, 20 seed overrides, gate false. Across 4,489 effective references,
the final worklist has **20 leads, zero mechanical integrity findings**:
15 seed/scan target differences, three same-phrase multiple-target cases,
one subset/ambient lead, and the existing submersive-wording scope lead.
Default output returns 12 and discloses eight omitted. Controlled qualifier and
variant checks produced no live leads; their positive cases are synthetic tests.
These counts measure diagnostics, not mathematical errors or audit completion.

Representative ranked leads (selected distinct review contexts):

1. **Rank 1, score 522: compactness FIP historical seed.**
   `form.wave2.broad67.compact-closed-fip`, occurrence
   `seed.00a94ab09cd5a879d962`, relation `rel.wave2.broad68.02`.
   Source: “Equivalently, X is compact if every family of closed subsets of X
   that has the finite intersection property has nonempty total intersection.”
   The seed phrase “closed subsets of X” still targets
   `meaning.wave2.foundation.topological-space`: a pair `(X,τ)` satisfying the
   empty/full-set, arbitrary-union and finite-intersection open-set axioms.
   The target explicitly defines open subsets, not a closed-subset predicate.
   The corrected scan's separate missing closed-subset prerequisite is retained.
   Review whether the historical seed intentionally supplies ambient topology or
   still confuses the predicate with ambient structure. A definition of closed
   sets via complements could justify a dependency on topology; no error or
   correction is inferred automatically.
   Evidence: `41eb31e3b57ed67f1b3ccf267d65f486c9ac82e8851064f899f5bd1eb025e0df`.

2. **Rank 2, score 450: internal Hom module conventions.**
   `form.3a0545450d7a5285.internal-hom-module`, scan occurrence
   `occ.a1e476731c4866e84c7d`, phrase “modules M,N”. Source: “For modules M,N
   over a commutative ring R, the internal Hom Hom_R(M,N) is the R-module of
   R-linear homomorphisms M→N, with pointwise addition and scalar multiplication
   (r·f)(m)=r·f(m).” The historical target is
   `meaning.wave2.foundation.left-module-nonunital`: an abelian group with a
   distributive associative R-action, unitality a separate optional condition.
   The scan targets `meaning.wave2.module94.unital-left-module`: the same action
   axioms over a ring with identity, plus `1m=m`. Its matching note explicitly
   says ordinary unital modules. Review whether these are intentionally retained
   general and specialized prerequisites; the two identities must not be merged.
   This may be valid specialization, not a defect.
   Evidence: `7a1ac45f36d4ecc8d46d5af0e4d460f184734831669b101ac27e106f6da68022`.

3. **Rank 10, score 450: lower Dedekind cut, subset versus proper subset.**
   `form.wave2.real50.dedekind-rational-lower-cut`, occurrence
   `occ.85b8e6f623ea12a5b553`, seed `seed.1bc4d429daa76d1d5238`.
   Source requires a nonempty subset A of Q, not all of Q, downward closed and
   with no greatest element. The identical phrase “subset A of Q” has historical
   target `meaning.wave2.foundation.subset-proper` and scanned target
   `meaning.wave2.foundation.subset-nonstrict`. The former excludes equality;
   the latter allows equality in its general predicate. Because the source
   explicitly says A is not all of Q, both links can be justified. This is a
   useful negative/control review lead, not a confirmed variant inconsistency.
   Evidence: `bab623b4ca751919c505d3e8892c9d84cec51af918425c844f84928b266ad4b2`.

Full reproducible JSON was generated outside the checkout at
`/tmp/wave2-consistency-all.json`; rerun the CLI to refresh it. Each selected lead
includes full source/target contexts and anchors, not just these report excerpts.

## Verification, efficiency and scope

- **85 tests passed** across `test_dependency_consistency_worklist`,
  `test_dependency_global_audit`, `test_dependency_cycle_analysis`,
  `test_dependency_graph`, `test_dependency_review_preflight`,
  `test_candidate_reuse`, `test_review_preflight_cache`,
  `test_dependency_context_worklist`, and `test_dependency_provenance_audit`.
- **Eight seed-override tests passed.** The historical
  `test_live_round177_packet_full_copy_replay_and_invariants` was not run because
  it reads mathematical proposal material outside the authorized dataset.
- Tests cover positive/negative mathematical contrasts, intact alias/resolution
  provenance, stale resolutions, corrected seed overrides, unknown seed targets,
  unchanged snapshots, deterministic limits/exhaustive output, single CLI
  snapshot load, review suppression and staleness on target/seed changes.
- Current-instance hashes of all **2,277 independent dataset files** matched
  before/after validation. `git diff --check` and protected-path inspection pass.
- Measured locally: snapshot load 0.0877 s; median worklist analysis 0.2433 s
  across three runs reusing that snapshot. This is a current-machine observation,
  not a speedup claim. The global auditor's cycle pass and the worklist each
  project effective references once per batch; no candidate reloads or graph
  reconstruction occur inside the review loop.

Not implemented: arbitrary mathematical implication, general type inference,
parsing binders/arrow direction or variance from formulas, equivalence or synonym
classification, omission-of-inverse-continuity proofs, broad specialization
warnings, and declaring different formulation prerequisites inconsistent. These
need stronger structured semantic evidence or human mathematical assessment.

Changed files only: `engine/dependency_consistency_worklist.py`,
`engine/dependency_audit_acceleration.py`,
`tests/test_dependency_consistency_worklist.py`, and this report, all under
`research_pipeline/`. No source, graph state, aliases, resolutions, indexes,
receipts, gate, production/site/deployment files changed. No production or frozen
Wave 1 mathematical data, external missing-definition research, new audit round,
or mathematical corrections were used/performed.
