# Codex engineering report: Pass 2 consolidation readiness evidence

Base: `c56ab1f8d45dfa4b2bca81d9d6f4c209f5b1a5e6` (latest main, PRs #4/#5 merged).
Branch: `codex/wave2-consolidation-readiness`.

**Assessment: mechanical checks pass; the contextual consolidation decision is
still required. Pass 2 is not declared complete. No gate was written, packet
prepared, phase changed or Pass 3 research started.**

## Implementation and use

```bash
python -m research_pipeline.engine.dependency_consolidation_readiness \
  --workspace research_pipeline/experiments/reconstruction-v2-independent
# All review leads and all candidate/source contexts:
python -m research_pipeline.engine.dependency_consolidation_readiness \
  --workspace research_pipeline/experiments/reconstruction-v2-independent --exhaustive
```

Default: 12 consistency leads, 12 candidate-context leads if any, and 12
recurrence-ranked missing-candidate examples with at most three parent contexts
per example. Candidate and parent-context omissions are explicit. `--limit N`
changes the page size; exhaustive output removes these limits. Results include
full relevant original formulations, source versions, effective-node/occurrence
IDs, target definitions, observation/source records and existing alias rationales.
Malformed inputs and failed mechanical checks produce a nonzero CLI exit status;
mathematical review leads alone do not.

The new module composes existing `collect`, effective amendment/alias/resolution/
seed replay, consistency worklist, formulation-choice cycle analysis, candidate
focus, provenance summarizer, review ranking and review-ledger validators. It
checks current sources against inventory and derived records against replay,
without running `rebuild`, `inventory_sync` or `seal_consolidation` on live data.
It does not implement another cycle detector, alias resolver or semantic matcher.

New checks compare occurrence/edge/unresolved/reverse indexes, registry identity
sets/status/counts/incoming sources, STATE/checkpoint/fingerprints, reference
dispositions and source-record links. Candidate review flags are limited to
missing contextual traceability or explicit opposing qualifier uses on shared
object words. Cross-domain/context variation alone does not imply an alias error.
Candidate flags reuse evidence-bound review-ledger acceptance; all are leads,
never automatically established identity errors or added gate requirements.

Evidence binds current source contents, effective graph, amendment-ledger digest,
alias/resolution/seed ledgers, derived indexes, review records and source issues.
Page limits do not change the assessment evidence ID. Source or graph changes
invalidate the result. The engineering commit identifies the diagnostic version.

Exact changed files, all under `research_pipeline/`:

- `engine/dependency_consolidation_readiness.py`
- `tests/test_dependency_consolidation_readiness.py`
- `WAVE2_CODEX_CONSOLIDATION_READINESS.md`

## Actual gate contract and current mechanical results

`dependency_graph.seal_consolidation` requires full semantic scans, zero
unassigned/ambiguous references, exact inventory/unresolved fingerprints, schema
1, a named reviewer and a substantive global rationale (40+ characters). A
conflicting same-scope existing record cannot be silently rewritten. The
assessment does not call this writer or emit a gate event.

The executable contract does **not** require zero missing candidates, zero open
formulations, zero cycles, zero heuristic warnings or zero explicitly deferred
occurrences. Deferred references still need their required reason and an explicit
contextual disposition; they do not automatically become missing meanings.

Current independent snapshot passes **19 mechanical checks**, with **zero
integrity failures and zero unmet scan/classification prerequisites**:

- 611 meanings; 659/659 complete scans; 0 unassigned, ambiguous or deferred.
- 728 raw identities = 421 canonical missing + 300 aliases + 7 resolved.
- 844 effective missing occurrences; all canonical missing candidates have
  nonempty registry context and live incoming occurrences.
- All 300 alias events, seven version-valid resolutions and 20 seed overrides
  replay consistently; no inactive resolution events.
- 770 amendments; current source inventory matches freshly collected source
  versions and seeds; occurrence, edge, unresolved and reverse indexes match.
- All 659 formulations have observation/source records and locators. There are
  659 paraphrase evidence links; their verification status is **unspecified**.
  Structural traceability is not external verification or citation certification.
- Existing consistency worklist: 20 mathematical leads, no integrity findings.
  The metric-space/open-ball effective SCC is avoidable under stored formulation
  choice; it is not an automatic mathematical defect or a gate blocker.
- No consolidation record exists; gate false and phase `consolidate_occurrences`.
  There are 300 reviewed alias events, 20 provisional population reviews, and
  zero audit-ledger rows. This does not prove that candidates were never reviewed,
  or that global review is complete: individual reviews do not certify coverage.

Inventory: `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`.
Recomputed unresolved pool:
`61246db4cb0897ac3bfdb43f8a8e6be361e2f05bf905367bfbda0b388a541113`.
Run the CLI for the complete current `assessment_evidence_sha256`.

## Prioritized decisions for ChatGPT review

1. **Record a global contextual-consolidation rationale at the exact scope.**
   Decide whether the existing scan classifications, identity reviews and
   documented nonmerges sufficiently address the missing-occurrence pool, and
   record exceptions/deferrals. Counts cannot decide this. No requirement to
   reduce 421 to zero or mechanically accept every warning is introduced.
2. **Triage the highest-ranked consistency lead: compactness historical seed.**
   `form.wave2.broad67.compact-closed-fip`, seed
   `seed.00a94ab09cd5a879d962`, relation `rel.wave2.broad68.02` still links
   “closed subsets of X” to ambient topology, while the corrected scan preserves
   missing closed-subset identity `missing.c4ed408b10943e9c0f8e`. The source says
   every family of closed subsets with FIP has nonempty total intersection.
   Decide whether the seed intentionally represents ambient topology or needs
   a separately authorized correction. Neither conclusion is inferred here.
3. **Preserve contextual distinctions in the other consistency leads.**
   Internal Hom (`form.3a0545450d7a5285.internal-hom-module`,
   `occ.a1e476731c4866e84c7d`) retains both general optionally nonunital and
   explicitly unital module targets. A legitimate specialization may explain it.
   Lower Dedekind cuts (`form.wave2.real50.dedekind-rational-lower-cut`,
   `occ.85b8e6f623ea12a5b553`) retain subset/proper-subset targets, while their
   source explicitly requires A not equal Q. Both may be warranted. Full target
   definitions and source contexts are joined by the reused worklist.
4. **Adopt an explicit later-reconciliation disposition for source issues, if
   appropriate, rather than silently treating them as repaired.** Round183's
   topological ring/module issue remains: the current texts require continuous
   addition and multiplication/scalar multiplication, but permit nonunital
   prerequisites and do not state inverse continuity. Decide the eventual source
   convention (unital context versus explicit additive-topological-group
   requirement) in the separately authorized source/formulation review phase.
   Related current source IDs are `form.646e4dcbd9b6f1e1.topological-ring` (version
   `03f497391324c755234793649bde87ad83ea94dc581a2ee3637168e25e5fa14d`) and
   `form.646e4dcbd9b6f1e1.topological-module` (version
   `0760928492e0ac3367e6d3c68783c325a204a8da9f76c4d167973eb79934ba7d`).
   The prior counterexample is in `WAVE2_SOURCE_FREE_AUDIT_ROUND183_2026-10-24.md`;
   this assignment did not reread external sources or apply a correction.

Four open population source issues are also returned, with original records,
full related formulation contexts and record hashes: pairwise-independence
index quantifier, outer-measure domain/axiom convention, bounded-map uniform
quantifier and operator-norm codomain notation. Their existing drafts preserve
corrected variants or quarantine discrepancies. Later source/citation
reconciliation is a proposed disposition, not an automatically adopted deferral.
Likewise retain the documented submersive-map, perfect-closure characteristic
scope and provisional-reconciliation caveats. None is a newly invented engine
gate condition. If a correction changes identity consolidation, reassess first.

## Missing meanings versus incomplete classification

All 421 canonical entries are structurally classified missing prerequisites,
not unassigned references. The bounded focus starts with size-unrestricted
category `missing.fcb5ab865c6d9dbb3d79` (60 occurrences) and covariant functor
`missing.c5104821c3c70afa1f63` (39). Their size/variance distinctions must survive;
missing unrestricted categories cannot be replaced by existing small categories
solely to improve counts. Source recurrence prioritizes review, not equivalence.

Another concrete classified example is polynomial relations
`missing.00f05f23cf310f438561`, occurrence `occ.c79911a56462df60950d`, in
`form.415a1503ae7ed97d.finitely-presented-algebra`: the source presents
`S≅R[x_1,…,x_n]/(f_1,…,f_m)`. The registry distinguishes the relations from their
relation ideal. Such entries can be considered as research inputs **only after**
a separate authorized consolidation decision. Their mathematical legitimacy,
possible primitive dispositions or further contextual duplication cannot be
certified automatically. The controlled candidate diagnostic returned zero
new explicit context contrasts; this is not a proof that every alias is correct.

## Validation and boundaries

- **101 focused Python tests passed**, including 16 new readiness regressions,
  plus **eight selected seed-override tests passed**. One historical test,
  `test_live_round177_packet_full_copy_replay_and_invariants`, was not run
  because it reads mathematical proposal material outside the authorized dataset.
- Tests cover mechanically eligible but undecided review, real registry/index/
  provenance failures, valid unassigned versus deferred references, classified
  missing meanings, alias/resolution/seed provenance, stale sources and graph
  evidence, source-issue deferral questions, ledger acceptance, truncation,
  exhaustive output and deterministic read-only behavior.
- Default and exhaustive live assessments were generated outside the checkout
  at `/tmp/wave2-consolidation-readiness*.json`. All **2,277 independent dataset
  files** retained identical hashes. `git diff --check` and final protected-path
  inspection pass.
- No production, frozen Wave1 or other mathematical dataset was consulted.
  No graph, definition, evidence, alias, resolution, index, state, receipt or gate
  changed. No consolidate packet, source rewrite, research phase or mathematical
  correction was performed. The next action is review of this evidence, not
  automatic gate activation.
