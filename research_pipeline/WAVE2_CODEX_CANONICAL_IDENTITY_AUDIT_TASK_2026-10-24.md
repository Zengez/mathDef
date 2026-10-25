# Codex task — independent Wave 2 canonical missing-identity audit (after Chat unitality adjudication)

**Prepared:** 2026-10-24, America/New_York.  
**Execution authority:** bounded **source-free mathematical/contextual REVIEW AND REPORTING ONLY**. Do not apply graph amendments, identities/aliases/resolutions, change mathematical source records, open phase gate, research outside sources, edit production or frozen Wave1, or expand breadth. Existing mathDef workflow contracts remain controlling. This task authorizes creating **audit reports, resumable progress indexes, scripts/tests strictly needed for reproducible read-only review** within the independent research pipeline; it does not authorize semantic graph changes.

## Mandatory first reads (from newest main, never trust hardcoded snapshot blindly)

1. `research_pipeline/DEPENDENCY_FIRST_WORKFLOW.md` — current execution contract.
2. `research_pipeline/WAVE2_PASS2_POST_FIP_HANDOFF_2026-10-24.md` — completed FIP repair / active digests.
3. `research_pipeline/WAVE2_PASS2_UNITALITY_ADJUDICATION_2026-10-24.md` — current Chat mathematical decisions for nine source-convention cases; no need to rediscover these as term-identity problems.
4. `research_pipeline/WAVE2_CODEX_CONTEXTUAL_CONSOLIDATION_REVIEW.md` — exact 20 historical leads, and `research_pipeline/WAVE2_PASS2_CONVENTION_ADJUDICATION_PROPOSAL_2026-10-24.md` — historical proposal (the FIP paragraph and source-inventory hashes there are superseded).
5. Live `research_pipeline/experiments/reconstruction-v2-independent/dependency_graph/{STATE.json,CHECKPOINT.json,INVENTORY.json,missing_candidates.jsonl,candidate_aliases.jsonl,resolutions.jsonl}` and up-to-date effective nodes/amendments/seed overrides. Read `research_pipeline/adapters/mathdef/resume_plan.json` for historical workflow context; some prose there is older than the above handoff.

As of the preparing checkpoint: inventory `34f61b6cf7fd1e80bda932dc8eeac473a729b11dfa0ba849c6db424b7a8f8113`, unresolved fingerprint `eb9beb4199a99b1dc3fc18b57daa1f1d4cc9c66051caa558acb7a48396242cee`, 611 meanings, 659/659 scans, **421 unresolved canonical candidates, 300 aliases, seven candidate-to-meaning resolutions, 844 missing occurrences**, 770 amendments, 0 unassigned/ambiguous, gate FALSE. Recompute from current committed data; if drifted, record exact changes before acting and never present old hashes as current.

## Core mission

Provide a **reproducible, auditable contextual classification of the 421 unresolved canonical missing-candidate identities**, distinguishing genuinely missing definitions from plausible existing-meaning matches, reviewed identity aliases, context-dependent ambiguities/variants, known justified nonmerges and source-scope questions. Every claim of “reviewed” must be supported by complete mathematical context and explicit per-candidate coverage, NOT inferred from a programmatically generated inventory or similarity score.

Do **not** optimize to reduce 421 artificially. A canonical missing prerequisite is allowed and is likely often truly missing; resolving it requires future source-supported research in Pass 3, not invented source-free content. The goal is to judge whether the **identity partition** in Pass 2 is sufficiently understood for a truthful global consolidation rationale, without conflating that with having populated every missing definition.

## Efficient, staged execution

**Stage A — read-only universe manifest:** Build an exact ordered list of all currently canonical unresolved candidate IDs from live `missing_candidates.jsonl` (status=unresearched and no alias_of or resolved_target_meaning_id). Capture candidate query, complete stored mathematical context, occurrence count, all associated observed alias IDs, incoming formulation count, and current inventory/unresolved hashes. Mark every row `UNREVIEWED` initially. Programmatic enumeration and ranking DO NOT count as mathematical review. Do not modify the registry. Prefer a compact JSONL review worklist and small summary MD under `research_pipeline/` so the review can resume without repeating work.

**Stage B — deep contextual review in incremental batches:** Start with **up to 30** highest-impact canonical identities, ordered by incoming occurrences and upstream formulation breadth, then prioritize high-risk size/variance, ring/module assumptions, quotient/object-type conflicts, and other likely false-target pairs. For each:

- Read each relevant *complete original source formulation*, its context, full effective current reference list, known source provenance metadata, and each apparently related **existing meaning** or potential aliased candidate's full recorded context. Use `dependency_global_audit focus` with `--candidate-id` and `--max-formulations 1000` if needed; never confuse the default three-formulation preview with exhaustive source review.
- If a candidate has more parents than can be evaluated in the active bounded batch, record exact `parent_formulations_reviewed` and `parent_formulations_remaining` and classify `PARTIAL`, not `COMPLETE`. High-fanout candidates (e.g. 42 source formulations for a category notion) require explicit complete coverage or explicitly bounded homogeneity argument grounded in enumerated sources, not an unchecked inference.
- Specify exact candidate ID; every source formulation reviewed; source-version hashes; implicated occurrence IDs and effective-node digests; original phrase and contextual meaning; compared existing meaning/candidate IDs; explicit mathematical proof or counterexample for proposed equivalences/contrasts; reviewer judgment; residual uncertainty.
- Assign one *review* disposition: `retain_distinct_missing`, `potential_existing_meaning_resolution`, `potential_candidate_alias`, `contextual_ambiguity_or_variant`, `source_convention_deferral`, `needs_mathematical_recheck`. If no other identity needs comparison, explicitly justify `retain_distinct_missing` via the expected object type/context and checked present inventory. Never label a candidate `resolved` solely because its English name matches another.
- For a proposed alias, show the identical mathematical object, domain, quantifiers, conditions and conventions under all included source contexts; disprove plausible near-matches where relevant. For an existing-meaning resolution, cite that exact current meaning and demonstrate prerequisites/scope match. Record *proposals only*; no inbox writes and no amendments/resolutions/aliases.
- Preserve nonmerges: unrestricted category vs small category; general functor vs smallness-constrained functor; inverse image of a set vs inverse function; module over nonunital vs unital ring/module; quotient ring vs quotient module; ring ideal vs ideal powers; general vs commutative/specialized ring assumptions; arrow/covariance and comma-versus-iso-comma; ordinary vs symbolic powers; pairwise vs mutual independence.
- Record every meaningful uncertainty rather than guessing a mathematical decision. For external source-scope cases, record an exact later-source verification question; do not use new internet/source research in this pass.

**Stage C — reporting and reproducibility:** Write per-candidate reviewed records to a distinct dated audit JSONL ledger under `research_pipeline/` or a dedicated `research_pipeline/reviews/` directory, not the engine's `dependency_graph` semantic ledgers. Maintain a checkpoint JSON with the exact reviewed IDs, not simply a reviewed counter, plus original active snapshot hashes. Write a succinct summary MD with accurate counts: total canonical, inventoried, deep-reviewed complete, partial, untouched, confidently distinct, candidate aliases proposed, existing-meaning resolutions proposed, deferred, needs recheck, and all proposed nonmerges. On each bounded chunk commit the **report and checkpoint together**; verify there are no mathematical/graph data diffs. Keep review runs within ~12–16 minutes so Chat/Codex timeouts can resume. Subsequent continuation starts at exact first unfinished candidate.

## First-priority live candidates (illustrative, not permanently hardcoded ordering)

As observed on 2026-10-24:
- `missing.fcb5ab865c6d9dbb3d79`: category (size-unrestricted), 60 missing occurrences, 42 upstream formulations. Special concern: not the same as a **small** category.
- `missing.c5104821c3c70afa1f63`: general functor F:C→D, 39 occurrences, 36 upstream formulations. Do not silently add object smallness.
- `missing.50fc57153b93520a247a`: quotient ring R/I, 16 occurrences, 16 parents. Check ring vs additive/module quotient.
- `missing.b86257b3cce62907e97e`: inverse image/preimage, 15 occurrences, 15 parents; never require inverse function.
- `missing.9db64b2f9cdb8258e3d8`: polynomial ring, 14 occurrences; finite versus arbitrary indeterminate families and unital coefficients.
- `missing.7462fa5f90275b34779a`: free R-module, 11 occurrences; arbitrary rank versus finite rank. Free-resolution #3 is mathematically justified under its recorded unital free-module construction.

These are workload priorities, **not** proposals to merge or populate those records.

## Reuse existing read-only engine helpers

From repo root:

```bash
W=research_pipeline/experiments/reconstruction-v2-independent
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" focus --limit 30 --max-formulations 1000 > /tmp/wave2-top30-candidates.json
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" scan --limit 80 --candidate-limit 80 > /tmp/wave2-current-audit.json
python -m research_pipeline.engine.dependency_consolidation_readiness --workspace "$W" --exhaustive > /tmp/wave2-readiness-current.json
```

Prefer one underlying parsed effective snapshot per audit batch. Large full-source bundles can be memory-heavy; split the 30 candidates into batches of 5–10 in the semantic-review process while tracking complete coverage. The CLI source text is the recorded independent formulation; it is not necessarily a verified verbatim external citation. The readiness tool evaluates 19 mechanical conditions and independently highlights limited mathematical leads; **passing it does not certify contextual identity consolidation**. Temporary outputs belong under `/tmp`, while only deliberately curated review/checkpoint files belong in Git.

For each chunk, run relevant tests and read-only audit commands, report actual success/failure; inspect git changed paths; commit to a dedicated `codex/wave2-canonical-identity-coverage-*` feature branch and prepare PR for review. Do not edit production or frozen Wave1. Do not write `CONSOLIDATION.json` or start external missing-definition research. Do not mark work complete or open the gate merely because 421 candidates were enumerated.

## Output / stopping condition for first Codex turn

Aim to complete Stage A manifest **for all 421** and Stage B's **first well-supported bounded batch of up to 30**, reporting how many candidates achieved *complete source-context review* versus partial. If the high-fanout candidates consume the full work budget, finish fewer **honestly**; do not reduce verification quality. Commit checkpoint and initial findings, validate report-versus-state hashes, and return links to branch/PR, exact reviewed/partial counts, noteworthy identities or errors, and next unreviewed ID(s). Subsequent Codex runs should continue until the coverage target is genuinely reached or mathematical issues require Chat adjudication.

**After the first substantial Codex tranche:** return to Chat with the review file/PR and exact state to adjudicate mathematically difficult identity cases; no need for user intervention merely to pick a batch size or navigate the workflow. Human user decisions are required only when competing substantive mathematical conventions remain genuinely indeterminate after analysis, or when authorizing a materially different research phase.
