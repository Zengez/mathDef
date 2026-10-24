# Codex operating instructions — mathDef independent Wave 2

These are standing instructions for coding agents working in \`Zengez/mathDef\`. **The authorized project is the independent second reconstruction / dependency-first Wave 2 experiment, not the production mathDef website or definition database.** Treat these rules as restrictive defaults; a task request does not implicitly broaden them.

## 1. Hard isolation boundary

**The ONLY authorized live mathematical dataset is:**

\`\`\`text
research_pipeline/experiments/reconstruction-v2-independent/
\`\`\`

Use that directory for experimental mathematical meanings, formulations, contextual sources, dependency records, and state. All other mathematical corpora in this repository are out of scope, even if similarly named or easier to access.

**Do not read, search, copy, compare against, import from, modify, or regenerate the original/production corpus**, including:

- \`definitions/\`, \`variants/\`, \`data/\`, \`web/\`, \`scripts/\`, \`tests/\`;
- root-level production catalogs, exports, content audit files, and \`WORK_CHECKPOINT.md\`;
- the frozen first reconstruction, \`research_pipeline/experiments/reconstruction-v1-recovery/\`;
- any other research experiment or archived population outside \`reconstruction-v2-independent/\`.

Never use production mathDef data as a fallback, test fixture, evaluation reference, or source of “missing” mathematical content. **Independence of the second reconstruction is a research requirement.**

Exceptions to the no-read rule are only the explicitly permitted *software and workflow* files below (plus this \`AGENTS.md\`, Git metadata, and files indispensable to repository setup); such exceptions authorize inspection of code/configuration, **not** use of another mathematical dataset. If a command, test, utility, or import would silently load an excluded corpus, do not run it.

**Instructions alone are not an OS-enforced sandbox.** Work in an isolated branch/worktree, inspect command inputs and changed paths, and stop if isolation cannot be established. Never claim that this file alone technically prevents access to excluded directories.

## 2. What Codex may read and change

**Read-only by default:**

- \`research_pipeline/WAVE2_CURRENT_HANDOFF.md\` — current human handoff;
- \`research_pipeline/DEPENDENCY_FIRST_WORKFLOW.md\` — current execution contract;
- \`research_pipeline/TEMP_DEPENDENCY_FIRST_WAVE2_PLAN.md\` — design rationale, subordinate to the execution contract;
- the latest \`research_pipeline/WAVE2_SOURCE_FREE_AUDIT_*.md\` and other specifically relevant Wave 2 audit reports;
- \`research_pipeline/experiments/reconstruction-v2-independent/**\` — the **only** live experimental mathematical/source/graph data;
- narrowly relevant Python code and tests in \`research_pipeline/engine/\` and \`research_pipeline/tests/\`. You may inspect \`.github/workflows/research-pipeline-ci.yml\` and \`.github/workflows/research-dependency-graph.yml\` when needed to understand CI; these are configuration, not mathematical sources.

**Default writable scope for explicitly assigned engineering tasks:**

- the relevant \`research_pipeline/engine/dependency_*.py\` modules;
- closely related \`research_pipeline/tests/test_dependency_*.py\`, \`test_candidate_reuse.py\`, and \`test_review_preflight_cache.py\`;
- a concise, clearly marked Codex engineering report in \`research_pipeline/\` (e.g. \`WAVE2_CODEX_CYCLE_AUDIT.md\`), if helpful.

Other generic engine modules may be changed **only if required by the specific assigned task**, with a documented reason and narrow regression tests; these modules can be used by other pipelines. No unnecessary refactors or dependency upgrades.

**Do not change without separate, explicit user approval:**

- anything under \`research_pipeline/experiments/reconstruction-v2-independent/\`, including \`records/\`, \`population/\`, \`intake/\`, \`wave2/\`, \`events/\`, \`state/\`, and **all** \`dependency_graph/\` contents;
- any actual meaning/formulation text, citation, source observation, population record, or original/historical relation;
- graph \`inbox/\`, \`applied/\`, event ledgers, candidate aliases, resolutions, overrides, effective indexes, \`INVENTORY.json\`, \`STATE.json\`, or \`CHECKPOINT.json\`;
- the current handoff, execution contract, or phase plan (propose documentation changes separately);
- root-level site assets; production directories; frozen Wave 1; other experimental workspaces; or \`.github/workflows/\`.

When a task genuinely requires a graph or mathematical-content correction, produce an **offline, exact, version-anchored proposal and mathematical rationale for chat/human review** instead of writing it into the live graph. Do not submit it to \`dependency_graph/inbox/\`, promote it, or trigger its application without explicit separate authorization.

## 3. Current mathematical workflow and limits

At the latest verified Round 184 checkpoint (2026-10-24), the independent workspace had **611 contextual meanings**, **659/659 fully scanned formulations**, **zero unassigned/ambiguous references**, and a **closed (false) consolidation gate**. Counts can change; read current \`dependency_graph/STATE.json\` and \`CHECKPOINT.json\` for authoritative numbers rather than hard-coding these historical figures.

We are in **source-free Pass 2**: global graph integrity, contextual dependency audit, and missing-candidate identity consolidation. **Pass 3 has not been authorized.**

- Do **not** begin external research for missing mathematical definitions, admit new meanings, promote provisional meanings, restart breadth Batch 143, or open \`CONSOLIDATION.json\` / the consolidation gate.
- Software documentation can be consulted for coding tasks; mathematical source/citation research remains off unless specifically authorized in a later phase.
- Do **not** silently create, merge, or resolve mathematical meanings or candidate identities from lexical similarity. Equivalent notation is not sufficient.
- Preserve differences in object type, size, variance, hypotheses, and conventions: small vs unrestricted categories/groupoids, unital vs nonunital structures, left vs right modules/actions, nonempty vs empty-allowed spaces, strict vs nonstrict subsets, and positive vs zero-inclusive indices.
- A dependency is not a mathematical theorem of equivalence. Different source formulations of the same meaning can legitimately have different prerequisites.
- A scanned/structurally closed graph node is **not** human mathematical review, externally verified citation, or permission to publish.
- Preserve exact source text, occurrence identity, original evidence, and append-only provenance. Do not edit a stale original \`dependency_graph/nodes/\` snapshot expecting it to update the effective graph. For analysis, use the **effective** replay / current \`edges.jsonl\` and version-valid indexes, and inspect seed overrides and candidate-resolved edges as relevant.
- Findings generated by heuristics or graph algorithms are *review leads*. Include counterexamples, complete original formulation context, and uncertainty before presenting anything as a confirmed mathematical error.

If existing workflow notes conflict, follow the **most recent current handoff + live state + current execution contract**, and stop to request clarification for a change that would violate these isolation rules.

## 4. Engineering workflow: optimize for reusable, reviewable work

1. **Before edits:** state the narrow task, expected files, baseline Git branch/status, relevant authoritative Wave 2 state, test approach, and any suspected cross-workspace data access.
2. Work on a **separate branch** named \`codex/wave2-<short-task>\` (or a similarly descriptive isolated worktree). Never commit directly to \`main\`, merge a pull request, or push changes to production or Pages.
3. Prefer **read-only diagnostics** and deterministic, domain-agnostic algorithms with source-independent tests. Use synthetic fixtures and temporary directories for mutating tests.
4. Never execute a graph apply/rebuild/ingest/population command **against the live independent workspace** merely to test engineering work. If a rebuild is necessary, copy the relevant independent workspace into a disposable location first, confirm what it will read and write, and keep the copy untracked.
5. Respect source hashes, candidate/occurrence IDs, historical seed overrides, reviewed-alias canonical chains, receipt semantics, and failure-atomic/idempotent behavior. Never bypass integrity assertions or broaden exceptions to make CI green.
6. For cycle auditing, distinguish **all effective meaning-level edges** (including candidate-resolved links), individual formulation dependencies, and cycles avoidable by choosing an alternative formulation. Do not automatically delete a valid mathematical edge to eliminate a cycle.
7. Keep changes focused. Do not launch autonomous series of candidate merges, data migrations, batch population, website deployment, or workflow transitions as incidental follow-up work.
8. On completion, review the changed path list with \`git status --short\`, \`git diff --check\`, and a branch-to-base file diff. **If any protected/excluded path was touched, stop; do not submit or commit that change.**

Suggested narrowly scoped tests (select what fits the changed code):

\`\`\`bash
python -m unittest research_pipeline.tests.test_dependency_global_audit
python -m unittest research_pipeline.tests.test_dependency_graph
python -m unittest research_pipeline.tests.test_dependency_review_preflight
python -m unittest research_pipeline.tests.test_dependency_seed_overrides
\`\`\`

Additional \`research_pipeline.tests.test_dependency_*\` tests are appropriate when their fixture access is verified. Do not run broad production/site test suites, crawlers, network intake jobs, global rebuild scripts, or CI workflow dispatches merely as a convenience. If a test writes files, point it to a temporary workspace and check repository cleanliness afterward. Report tests not run and why.

## 5. What to deliver for chat review

Provide a brief pull request (or unmerged branch) handoff stating:

- the task, findings, and exact **files changed**;
- what you read as inputs, and confirmation that no production/frozen-Wave1 mathematical data were used;
- tests/commands run and pass/fail/skip results;
- before/after behavior, risks, and regression coverage;
- mathematical judgments or graph changes **proposed but not applied**;
- whether any source, graph records, alias ledger, consolidation gate, site, or production files changed (**expected: no**).

Do not report “audit complete,” “all definitions correct,” “source certified,” or “dependency closure complete” on the basis of programmatic checks. Stop for human/chat review at a meaningful task boundary rather than undertaking unrelated work merely because execution time or Codex usage remains available.

## 6. Stop and ask rather than improvise

Stop and request an explicit scope decision if you would need to read production definitions, access frozen Wave 1, use a different mathematical dataset, change Wave 2 source/graph records, relax a strict integrity check, resolve a mathematical ambiguity automatically, open a phase gate, or write outside the permitted scope. Preserve safe partial code/test work for review; never mask or silently work around the blocker.
