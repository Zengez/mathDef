# Independent mathDef Reconstruction — Execution Runbook

**Status:** Software preparation for both waves is implemented and covered by isolated tests. **No real reconstruction has been initiated**. This document is an execution protocol, not evidence of recovered definitions.

## Non-negotiable experiment boundary

- Start only with Stage 0 **generic project description**, then independently discover suitable sources. The source registry MUST NOT be seeded from production \`definitions/\`, \`variants/\`, citation/audit files, or other production mathDef content.
- Engine and preview read only a specified \`research_pipeline/experiments/reconstruction-vN\` workspace. No original-repo reads are permitted before both waves finish and their publications are frozen.
- Evaluation runs from \`research_pipeline/evaluation/compare.py\` **only after** Wave 1 and Wave 2 are published. The evaluation may read the existing \`definitions/\` and \`variants/\` as the (imperfect) reference set.
- Neither a shared chat's prior knowledge nor general researcher experience can be perfectly blinded. Record the limitation in the evaluation report.
- Python scripts do not independently reason like ChatGPT. Stage 1 authority judgments and Stage 4–5 semantic reasoning remain interactive, source-grounded chat tasks; the scripts prepare queues, enforce structure, and preserve evidence and progress.
- **Never spend money by default.** Record reputable paid sources, but do not fetch/pay for their contents. Respect reuse rights, crawl restrictions, robots and source-specific rate limits.
- The proof-of-concept preview is NOT deployed over the existing production Pages site.

## Before first live run: verify software

From the mathDef repository root:

    python -m unittest discover -s research_pipeline/tests -v
    node --check research_pipeline/adapters/mathdef/preview.js

Also check the newest "Research pipeline isolated tests" workflow is green. Existing mathDef production tests are separate.

## First-wave initialization — mostly linear

### Stage 0 (High only when revising conceptual contract; otherwise Medium)

Discuss or confirm term identity, content type, mathematical contexts, grouping, aliases, relation types, source standards, publication gate, access rights, and prototype scope. The existing profile is \`research_pipeline/project_profiles/mathdef_reconstruction.json\`, which names **no inherited source URLs**.

Initialize a fresh, independent workspace:

    python -m research_pipeline.engine.cli --workspace research_pipeline/experiments/reconstruction-v1 init --config research_pipeline/project_profiles/mathdef_reconstruction.json

### Stage 1: discover reliable *source collections* (Medium recommended)

    python -m research_pipeline.engine.cli --workspace research_pipeline/experiments/reconstruction-v1 queue sources

In chat, research scholarly indexes, textbooks, encyclopedias, university sources, and other relevant directories. Create JSONL source records with authority rationale, rights/access flags, candidate index page URLs, and any reuse license. Do NOT look up or enumerate math terms during Stage 1. Source records need \`id,title,url,authority_reviewed,rights,access\`. Optional \`index_pages\` is a list of \`{"url":"...","profile":"glossary|headings|linked-list","html_path":"..."}\`. \`index_urls\` and \`index_profile\` are alternatives. Paid sources can be catalogued but cannot be automatically read.

    python -m research_pipeline.engine.cli --workspace WORKSPACE ingest sources --input reviewed_sources.jsonl --batch-size 5
    python -m research_pipeline.engine.cli --workspace WORKSPACE seal sources

Checkpoint the reviewed sources and stage state in GitHub at each research batch; local files alone are insufficient across ephemeral chat executions.

### Stage 2: discover raw term names/locators (Instant or Medium)

    python -m research_pipeline.engine.source_manifest --workspace WORKSPACE --output source_pages.jsonl
    python -m research_pipeline.engine.batch_intake --workspace WORKSPACE --manifest source_pages.jsonl --stage terms --output raw_terms.jsonl --checkpoint state/terms_intake.json

The manifest is reviewed and bounded. Batch intake runs **offline by default** using manifest \`html_path\`; add \`--network\` only for an approved, robots-permitted HTTPS index and permitted host. Each invocation processes up to **five** pages by default and can be repeated from the checkpoint. Optional \`--batch-pages N\`, \`--limit-pages N\`.

A locally saved sitemap can add approved index targets without querying the live sitemap automatically:

    python -m research_pipeline.engine.source_manifest --workspace WORKSPACE --sitemap-xml approved_sitemap.xml --sitemap-source-id SOURCE_ID --output source_pages.jsonl

Indexes are not guaranteed to expose all terms. Keep uncertain candidates, and do not claim complete coverage.

    python -m research_pipeline.engine.cli --workspace WORKSPACE ingest terms --input raw_terms.jsonl --batch-size 25
    python -m research_pipeline.engine.cli --workspace WORKSPACE seal terms

### Stage 3: acquire content candidates and precise locators (Medium)

    python -m research_pipeline.engine.batch_intake --workspace WORKSPACE --manifest source_pages.jsonl --stage observations --output raw_observations.jsonl --checkpoint state/observations_intake.json

By default the collector records only source locators. To persist licensed passages, the source must explicitly record permitted reuse rights and \`license_url\`, AND the researcher must opt in with \`--licensed-excerpts\`. Otherwise human/assistant research supplies **independently authored paraphrases** as additional observation records, retaining the original URL/locator and evidence role. It is not a goal to copy unlicensed scholarly text.

    python -m research_pipeline.engine.cli --workspace WORKSPACE ingest observations --input raw_observations.jsonl --batch-size 10
    python -m research_pipeline.engine.cli --workspace WORKSPACE seal observations

### Stage 4: group terms, contextual meanings, and formulations (High)

    python -m research_pipeline.engine.cli --workspace WORKSPACE queue meanings --batch-size 10

Research and classify into \`meanings\` rows: stable \`id\`, \`term_group_id\`, \`display_term\`, explicit \`context\`, \`term_ids\`, and \`formulations\` (each needs \`id,text,evidence_ids,review_state\`). Distinguish identical terminology with different objects from equivalent formulations; retain source evidence after consolidation. Semantic reasoning is performed in chat, not asserted by the script. A \`screened\` formulation meets the specified automated publication gate, not human verification.

    python -m research_pipeline.engine.cli --workspace WORKSPACE ingest meanings --input meanings.jsonl --batch-size 10
    python -m research_pipeline.engine.cli --workspace WORKSPACE seal meanings

### Stage 5: relate entries (High)

    python -m research_pipeline.engine.cli --workspace WORKSPACE queue relations --batch-size 10

For each formulation, research relevant links and dependencies, resolving or holding ambiguities. A proposed relation needs \`id,from_formulation,target_meaning,relation_type,review_state\`.

    python -m research_pipeline.engine.cli --workspace WORKSPACE ingest relations --input relations.jsonl --batch-size 10
    python -m research_pipeline.engine.cli --workspace WORKSPACE seal relations

### Stage 6: publish the separate prototype (High for review)

    python -m research_pipeline.engine.cli --workspace WORKSPACE publish
    python -m research_pipeline.adapters.mathdef.preview --workspace WORKSPACE

This is an **experimental** website at \`WORKSPACE/preview/index.html\`, with its own sources, search, context groups and link expansion, not a GitHub Pages overwrite. The source modal retains supporting and other encountered references. A GitHub issue can propose verification of one or more specified formulation revisions; the maintainer must approve.

Inspect visually and test representative difficult cases. Confirm the prototype's project-specific structure before moving to Wave 2. Record stable first-wave commit and catalog digest.

## Rigorous Wave 2 — after prototype inspection

1. Freeze the first-wave snapshot; never overwrite it.

       python -m research_pipeline.engine.cli --workspace WAVE1 wave2-plan
       python -m research_pipeline.engine.cli --workspace WAVE1 fork-wave2 --destination WAVE2

2. Use Wave 1 terminology to research additional authoritative sources, synonym contexts and definition variants. Re-run the Stage 1 source assessment for all newcomers, and revisit **old as well as new** source indexes. Review automatically generated Wave 2 tasks, and select high-yield work rather than assuming the whole source×term Cartesian product must be queried.
3. Add new records by regular \`ingest\` and preserve inherited stable IDs; modify an existing item ONLY through the audited revision CLI, using a JSON proposal with \`event_id,stage,record_id,before_digest,editor,reason,operation,replacement\`. \`retire\` leaves a traceable held record. Substantively changed formulations must return to candidate status and pass screening again.

       python -m research_pipeline.engine.revision_cli --workspace WAVE2 --proposal reviewed_change.json
       python -m research_pipeline.engine.revision_cli --workspace WAVE2 --recover

4. Complete/seal the stages in order; revalidate and republish a second independent snapshot.

       python -m research_pipeline.engine.cli --workspace WAVE2 publish
       python -m research_pipeline.adapters.mathdef.preview --workspace WAVE2

5. Record provenance and effort only when measured, with per-batch \`id,stage,thinking,minutes,research_calls,records_examined\`:

       python -m research_pipeline.engine.effort --workspace WAVE2 --event-file measured_batch.json

## After both waves are frozen: compare to existing mathDef

This is the ONLY step permitted to read the original production definitions.

    python -m research_pipeline.evaluation.compare --baseline-root . --wave1 WAVE1 --wave2 WAVE2 --output comparison.json

Report the original source and term candidate recovery, ambiguous lexical matches, candidate link overlap, novel leads, and recorded effort. **The lexical matching and relation overlap are preliminary candidates**, not mathematical equivalence judgments. The evaluator writes a semantic-review queue; use High thinking for resolving uncertain matches and judging mathematical accuracy.

## Standard restart message / stage handoff

Read \`research_pipeline/IMPLEMENTATION_CHECKPOINT.md\`, then the active \`WORKSPACE/state/checkpoint.json\`, stage summary, candidate files, and git commit. Continue the next incomplete unit. The status report must give **which task is complete, what remains, exact next command, and the recommended Instant/Medium/High setting**. Scripts cannot themselves change ChatGPT's thinking effort.

Commit reviewed source lists, output manifests and progress after practical batches (typically 5–10 records for reasoning-heavy stages; title extraction may be larger). Do not claim a batch is persisted to GitHub merely because it was written to local storage.
