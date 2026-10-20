# Portable research resume and work-session protocol

This infrastructure is intended for **math definitions, theorems, mathematics-education terms, and unrelated research domains**. It does not itself decide the correctness of any definition, theorem, citation, or relationship.

## Contract and extension points

- **Generic engine:** `research_pipeline/engine/resume_checkpoint.py`. No mathematical vocabulary, subject-specific stage names, or hardcoded record counts. It reads and hashes JSON/JSONL research inventories, checks stable IDs, compares changed inventory hashes, and emits an atomic, deterministic short checkpoint.
- **Project adapter config:** e.g. `research_pipeline/adapters/mathdef/resume.json`. Defines record locations, ID fields, review-decision fields, domain-validation plugin, and output path.
- **Optional policy plugin:** e.g. `research_pipeline/adapters/mathdef/resume_validation.py`. Only the adapter understands frozen independent Wave 1, Wave 2, link-cycle logic, and source-specific review integrity. A theorem project can supply its own proof/dependency adapter; an education terminology project can implement its own vocabulary/context rules.
- **Human-maintained plan:** e.g. `research_pipeline/adapters/mathdef/resume_plan.json`. Contains *only* next work, small work budget, known blockers, and workflow IDs requiring live checks. Keep this file short and update it at a completed research boundary.
- **Generated checkpoint:** `.../state/RESUME_STATE.json`. The computer-generated summary carries current inventory counts, hashes, supporting-input-group attestation, review distributions, adapter validations and human-plan instructions. It never claims a queued workflow has completed. Its saved bytes do not depend on the Git commit which subsequently commits the checkpoint itself.

To use this in another repository, copy the generic engine and tests, supply a new `resume.json` and `resume_plan.json`, optionally implement a domain-validation plugin, and install a scoped CI workflow. **Do not copy mathDef-specific validation rules into the generic engine.** If a project uses CSV or database records, implement a new generic-format parser without adding domain vocabulary.

## Checkpoint commands

From the repository root:

```bash
python -m research_pipeline.engine.resume_checkpoint \
  --config research_pipeline/adapters/mathdef/resume.json --check
python -m research_pipeline.engine.resume_checkpoint \
  --config research_pipeline/adapters/mathdef/resume.json --write
python -m research_pipeline.engine.resume_checkpoint \
  --config research_pipeline/adapters/mathdef/resume.json --verify
python -m unittest research_pipeline.tests.test_resume_checkpoint -v
```

`--check` is read-only and reports whether the saved checkpoint matches the current inputs; it does not fail solely because the saved file is stale. `--verify` is also read-only but fails closed if the saved checkpoint is stale or missing. All modes validate records. `--write` updates **only** the configured short checkpoint, atomically, without modifying the research corpus. Unchanged inputs produce identical persisted bytes even after the checkpoint's own Git commit. Live Git HEAD is displayed at runtime but excluded from the saved snapshot. No stopwatch, recurring process, server access or network connection is needed for the CLI.

For mathDef, `.github/workflows/mathdef-resume-checkpoint.yml` refreshes the checkpoint after *relevant research-data changes on main*. The mathDef adapter also hashes frozen lineage records, research queues, revision events and other supporting-input groups without embedding the entire historical files in the short checkpoint. It explicitly excludes the generated checkpoint from its push filters to avoid an infinite commit loop. On a push collision it **fetches and recomputes** from newest main rather than rebasing a stale snapshot. It never seals Wave 2, publishes definitions, or changes frozen Wave 1.

## Short-session operating procedure

**Target 12–14 minutes of active work** as a practical work budget, not a guaranteed execution limit or timer. Checkpoint at task boundaries, and prefer returning to the user over beginning a substantial new step near the budget.

1. **Fast restart:** read `RESUME_STATE.json` and `resume_plan.json`. Check the current commit and the *listed relevant GitHub Actions conclusions*, plus new runs that changed authoritative records. Do not start by re-reading the entire research history.
2. **Validate changed work only:** use `--check` and the adapter checks; if a current inventory hash differs, identify the changed file and inspect its new reviews/results. Trust prior completed mathematical reviews unless new evidence or a failed invariant warrants reopening them.
3. **Execute one bounded batch:** make domain-specific decisions using appropriate mathematical/research effort; preserve individual source evidence and variant distinctions. Commit after independent validation rather than accumulating a long uncommitted session.
4. **Record next action:** update `resume_plan.json` with the exact next safe step and workflow IDs. Refresh/commit the short checkpoint. Return to the user cleanly instead of relying on a timeout.
5. **On failed or queued CI:** never mark it as successful from a submitted workflow or local check. Store its ID as requiring live verification; resume from the last actually committed, verified state.
6. **On uncertain domain correctness:** record a hold/ambiguity instead of forcing a link or claiming human peer review.

## Trust boundaries

The generic engine verifies *syntactic and recorded evidence state*. The project adapter verifies *domain-specific invariants*. A green Actions run verifies the operation ran with its assertions; it is not a mathematical proof or third-party peer approval. Source-citation verification and mathematical source equivalence need independent individual reviews. Neither checkpoint system nor GitHub CI may silently rewrite review dispositions, remove protected research records, or infer that the collection of all relevant concepts has been exhausted.

For mathDef, **never read the production definitions, variants, or citations to build independent Wave 2**. The frozen independent Wave 1 is read only to recompute its attested publication digest; it is not edited. All five Wave 2 stages remain unsealed until separate rigorous approval.

## Limitations

A persisted checkpoint is not an asynchronous agent, cannot infer which GitHub workflows succeeded without checking live results, and cannot prevent a chat timeout. It is a compact recovery index. Per-response time limits are outside these scripts, so the suggested 12–14-minute session window must be observed conversationally rather than enforced by a persistent in-chat timer.
