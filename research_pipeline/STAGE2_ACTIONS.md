# Stage 2: GitHub Actions source-index intake

**Experiment:** `research_pipeline/experiments/reconstruction-v1/`

This execution path solves the chat container's lack of external DNS by
running the *existing isolated research engine* on a GitHub-hosted runner.
It is intentionally **read-only** with respect to the GitHub repository.

## Start or rerun

Open **Actions > Independent mathDef Stage 2 title intake > Run workflow**,
choose `main`, and run. Changes to its workflow, `stage2_actions.py`,
`source_intake.py`, or the isolated `source_pages.jsonl` also trigger a run.
The job checks out the repository, runs all isolated tests, then executes:

```bash
python -m research_pipeline.engine.stage2_actions \
  --workspace research_pipeline/experiments/reconstruction-v1 \
  --manifest research_pipeline/experiments/reconstruction-v1/source_pages.jsonl \
  --output-dir research_pipeline/experiments/reconstruction-v1/stage2_actions_artifacts \
  --max-pages 12
```

The resulting **stage2-title-candidates-RUNID-ATTEMPT** artifact contains:

- `raw_terms.jsonl`: extracted, **unverified** labels and URL locators
  (no definition text).
- `checkpoint.json`: pages successfully processed and the manifest digest.
- `report.json`: page-by-page results, errors, deferred sources, and counts.

Artifacts expire after 30 days. **Do not treat an artifact as a permanently
committed workspace checkpoint.** After reviewing the results, import accepted
records through `python -m research_pipeline.engine.cli --workspace ... ingest terms --input ...`,
commit the updated experiment files, then seal only after Stage 2 is complete.
Manual/provisional term records already in the workspace must be reconciled by
stable ID and exact content; changed IDs require human review, not overwrites.

## Scope and safety

The run is limited to 12 index pages and only the explicitly reviewed
`src.stacks` and `src.planetmath` sources. HTTPS, approved source hosts,
robots rules, bounded byte counts, and request delay are enforced by
`source_intake.py`. The PlanetMath `www`/apex host alias is narrowly pinned
to that registered source; unrelated hostnames remain denied.

**PlanetMath currently reports its robots policy unavailable.** Network intake
is deferred, not bypassed. Do not substitute direct fetches that evade robots.
OpenStax, MathSciNet, MathWorld, NIST DLMF, EOM, MIT OCW, and ProofWiki are
currently **not** on the automated-network allowlist. OpenStax needs explicit
AI-use rights review, and some sources have restrictions on bulk harvesting.
Adding any new automatic source requires reviewing terms, robots, and the
specific index profile. There is no automated search over the existing mathDef
definitions, citations, relationships, or other production corpus material.

The GitHub workflow uses `permissions: contents: read`, disables persistent
checkout credentials, and uploads artifacts even if collection fails. It does
**not** push source-derived data into the repository, merge to main, ingest
unverified candidates, or seal Stage 2. A green workflow with `partial: true`
is **not** evidence that Stage 2 has finished.

## Diagnostic and failure behavior

- A missing robots policy is a `blocked` page; it stays retryable.
- Other network/parser exceptions are `error` pages; the job fails but
  still uploads checkpoints.
- The source manifest is digest-bound; changing it requires a new output
  directory rather than silently resuming a mismatched run.
- The first live workflow run on 2026-10-18 completed 21 isolated tests,
  successfully fetched the Stacks browse index, and produced an artifact.
  This confirms execution access, **not** completeness or correctness of
  all mathematical term candidates.

After Stage 2 acquisition and reconciliation, a separate Medium-effort review
will check provenance, quality, duplicates, and source coverage prior to
sealing. Stage 3 must not start before that review.
