# Wave2: bounded first-generation staging and routine gate automation

**Proposal / engineering branch, 2026-10-26.** Independent Wave2 only. No production mathDef data, frozen Wave1, or other experimental corpora used. This change does not certify any mathematical statements or source citations.

## Owner-approved workflow improvements

1. **Bound each generation.** After an exact reviewed consolidation gate opens, freeze the current unresolved canonical candidate registry into `generation_staging/MANIFEST.json`. Record each one-generation source-backed candidate disposition under `generation_staging/records/` with original query/identity, actual mathematical sources and locators, accepted and provisional independent-corpus version anchors, an explicit comparison, any distinct variants and deferred newly discovered dependencies. Do not import any of those records into live meanings/graph until the complete original generation has been reviewed and integrated. New prerequisites are recorded for a subsequent generation, not researched recursively during the current milestone.
2. **Guard but automate routine gates.** A GitHub Action on `main` runs a version-checked gate runner after the existing inbox application. It uses a pinned substantive initial Phase 2 review (documented in separate draft PR #17) and the owner's standing policy for later routine generations. It opens the gate only when every current formulation has a complete scan, no reference remains unassigned/ambiguous, no graph inbox packet remains unapplied, no explicit substantive gate hold exists, and the current inventory/fingerprint match. A later-generation gate also requires an attested, fully staged and integrated prior generation, with recorded mathematical/global/source review. **Mechanical readiness is never source certification.**
3. **No repetitive user JSON copy/paste.** The current exact gate event lives in `research_pipeline/adapters/mathdef/phase_gate_policy.json`, and the approved GitHub Action invokes the runner. On merge of the reviewed engineering PR, GitHub Actions handles the protected write transaction on `main`; the assistant doesn't need a direct write to `dependency_graph/inbox/`. Subsequent routine transitions likewise use the standing policy when prerequisites are met.

## Engineering files

- `research_pipeline/engine/dependency_phase_gate.py`: pure check by default; `--apply` uses the existing `seal_consolidation` implementation and never bypasses its exact hash and completeness guards.
- `research_pipeline/engine/dependency_generation.py`: frozen milestone, strict per-candidate staging and nonrecursive source research requirements, progress check and archival of completed prior generation.
- `research_pipeline/adapters/mathdef/phase_gate_policy.json`: exact initial inventory/fingerprint and owner-approved routine-policy metadata.
- `.github/workflows/research-dependency-graph.yml`: guarded gate after inbound reviewed packets, freezes a milestone only once gate is genuinely valid, commits only graph/index/independent staging; additional triggers on independent mathematical inventory intake.
- `research_pipeline/tests/test_dependency_generation.py`: synthetic fixture tests, no real mathematical dataset read.

## Current, exact pinned initial review

- Inventory SHA256: `34f61b6cf7fd1e80bda932dc8eeac473a729b11dfa0ba849c6db424b7a8f8113`
- Missing-occurrence fingerprint: `7b69e2fdcb30a4536883df44308d386219b7621533886d65276b8992959f4773`
- At review: 659/659 scanned, 0 unassigned, 0 ambiguous, 418 unresolved canonical candidates, 841 missing reference occurrences.

**Never say this PR opens the gate until the actual GitHub Action runs on merged `main`, records a valid `CONSOLIDATION.json` and produces a state with `phase=research_missing_dependencies`.** The two changes are proposed via an isolated PR; neither a branch commit nor a PR creates an applied main-branch graph gate.

## Safety/integration boundaries

- The staged first pass is deliberately **not** the existing `population/records/`; that existing population is part of the graph's current source inventory. Writing new meanings into it in the middle of the first generation would immediately stale the active gate. Integration must be a separate, post-milestone reviewed event.
- The generation manifest is immutable during its research pass. Incoming new candidates do not enlarge its list.
- A rejected, deferred, or unresolved result still requires a contextual written reason and remains provisional; source-backed decisions require actual source URL + section.
- Research compares against both the current screened independent meanings and the entire independent provisional population; additionally every earlier staged generation draft must be considered before the next candidate can be written.
- The current gate's exact review rationale acknowledges separate version-pinned holds (e.g. source text counterexamples), but opening a research phase is **not** permission to promote those formulations.
- Future stage archival requires reviewed integration, with explicit source-verification/global-audit evidence and a receipt keyed to the original gate fingerprint. The source and mathematical review itself is not automated by a mechanical CI check.
- `GATE_HOLDS.json` with `{"block_gate":true,"reason":"..."}` remains an emergency substantive blocker. This is an explicit opt-out of routine gating, not permission for CI to resolve mathematics automatically.

## Operator commands (for maintainers, not repetitive owner chores)

Read-only eligibility check:

```bash
W=research_pipeline/experiments/reconstruction-v2-independent
python -m research_pipeline.engine.dependency_phase_gate \
    --workspace "$W" --policy research_pipeline/adapters/mathdef/phase_gate_policy.json
```

Apply only via approved workflow on `main`, then inspect actual state and receipts:

```bash
python -m research_pipeline.engine.dependency_phase_gate \
    --workspace "$W" --policy research_pipeline/adapters/mathdef/phase_gate_policy.json --apply
python -m research_pipeline.engine.dependency_generation --workspace "$W" --mode create
python -m research_pipeline.engine.dependency_generation --workspace "$W" --mode status
```

For a researched candidate, `--mode stage --submission path/to/researched-candidate.json` writes only a version-pinned, evidence-bearing provisional staging record. Future generation integration must be independently attested.

## Review and deployment requirements

- CI must pass isolated `test_dependency_generation.py` plus existing `test_dependency_graph.py`, full pipeline suite and read-only global independent graph audit.
- No direct writes to `main` from ChatGPT; changes are reviewable on an isolated PR.
- Before merging, confirm the main branch still matches initial hashes. If it changed, **do not loosen the checks**: prepare another reviewed Phase 2 decision or source-specific hold.
- After merging, verify the GitHub Action successfully persisted the phase gate and initial bounded manifest; do not assume automatic publication or begin source acquisition without that verification.

No Codex credits are needed for these narrowly scoped engineering changes.
