# Research Pipeline — Implementation Checkpoint

**Updated:** 2026-10-18.  
**Phase:** Pre-reconstruction engine build COMPLETE for a supervised two-wave trial; **the actual reconstruction has NOT been started**.  
**Guide:** [RECONSTRUCTION_RUNBOOK.md](RECONSTRUCTION_RUNBOOK.md).  
**Design:** [../RESEARCH_PIPELINE_ENGINE_DESIGN.md](../RESEARCH_PIPELINE_ENGINE_DESIGN.md).

## Implemented functionality (GitHub-tracked)

- Reusable model and CLI: \`engine/core.py\`, \`engine/cli.py\`. Project profile, stage-specific records (sources, raw terms, observations, meanings/formulations, relationships), strict cross-record validations, stable IDs, idempotent batch ingestion, atomic checkpoint manifests, stage sealing and digests, eligible-draft screening and isolated publication.
- Stage work and thinking effort: \`engine/queues.py\`, CLI \`queue\` and \`status\`. Separately prepares source discovery, title collection, content gathering, semantic classification and linking research. Handoffs recommend **Instant, Medium or High**; software does not set the ChatGPT model/effort.
- Approved-source intake: \`engine/source_manifest.py\`, \`engine/source_intake.py\`, \`engine/batch_intake.py\`. Build approved index-page manifests (optionally using downloaded/saved sitemaps), extract conservative candidates from glossary/headings/list links, record source-specific locators and rights-permitted excerpts, process bounded page batches with resumable durable checkpoints. Offline HTML default; opt-in network is same-host HTTPS only with robots policy checks. No paid retrieval by default.
- Separate bulk waves: \`wave2-plan\` queues additional source/variant/relationship research, \`fork-wave2\` creates a new workspace without altering frozen Wave 1, and \`engine/revisions.py\` + \`revision_cli.py\` implement explicit predecessor-hash corrections/retirements with an append-only audit log and recovery. Substantive changes to formulations must return to candidate review.
- Independent mathDef prototype: \`adapters/mathdef/preview.py\`, \`preview.js\` and \`preview.css\`. Separate term and definition searches, grouped mathematical meanings, multiple formulations, source evidence dialog (supporting plus other encountered), basic KaTeX rendering with online asset fallback, three exploration modes, context-prioritized target meaning, branch-limited recursive links, proposed link-context correction, and multi-formulation GitHub verification issue drafts. None of these reports auto-approve content.
- Evaluation: \`evaluation/compare.py\`. Only **post-freeze**, read-only comparison against production mathDef. Outputs source URL/domain overlap, term identity candidates, link candidates, ambiguous semantic-review queue and changes from Wave 1 to Wave 2. \`engine/effort.py\` accepts explicit user-recorded effort metrics, never invents cost/time.
- Tests/workflow: \`research_pipeline/tests/\` covers full artificial acquisition→publication→preview→wave2→evaluation, source rights, batch restart, source index manifests, staged revisions, link/term group behavior and work-effort records. \`.github/workflows/research-pipeline-ci.yml\` checks all independent Python tests, the CLI, and viewer JavaScript syntax. Existing mathDef production Pages workflow remains separate and previously passed after the Closure test regression fix.

## Strict research isolation and publication policy

- **No real source search or independent mathDef reconstruction has yet been performed.** Stage 1 authoritative-source selection and Stage 4/5 mathematical semantic analysis are performed with source-grounded reasoning in ordinary ChatGPT conversations; these scripts manage batches, provenance, validation and checklists, rather than calling an AI model autonomously.
- Start from a generic subject contract in \`project_profiles/mathdef_reconstruction.json\`. That profile must NOT contain production citations or seed definitions. During both acquisition waves, do not read existing production \`definitions/\`, \`variants/\`, citation ledger or related reference files to seed results.
- Publication is screened-draft only, with **"Not yet manually verified"** notice. GitHub verification proposals remain queued for explicit editorial approval. Neither tests nor source links prove mathematical correctness.
- Both waves publish into their **separate experiment** folders, never replace the live mathDef website. Only \`evaluation/compare.py\` can subsequently inspect production data, and only when Wave 1 and Wave 2 have both been frozen and published.
- No source-text capture unless specific reuse rights are recorded; ordinary indexes yield term names and locators. Advanced index formats may need subject/source-specific readers during the trial.
- GitHub Actions CI is not a browser UI test. Exact word-offset In-Line linking and automatic semantic relevance ranking are not yet at full production feature parity; the experimental viewer uses after-formulation expansion and explicit screened relation targets. These are acceptable known limitations for this first reconstruction benchmark, not claims of finished general website software.
- Workspace checkpoints are durable on disk, but must also be **committed to GitHub after practical batch boundaries** when running in ephemeral chat runtimes. Never claim a local checkpoint is already pushed.

## Exact next action: START RECONSTRUCTION WAVE 1 — Stage 1 (Medium thinking)

1. Confirm latest [Research pipeline CI](https://github.com/Zengez/mathDef/actions/workflows/research-pipeline-ci.yml) and normal Pages checks pass.
2. Open \`RECONSTRUCTION_RUNBOOK.md\`; initialize a fresh \`reconstruction-v1\` workspace with the generic project profile.
3. Generate the Stage 1 source-discovery queue; independently research authoritative source collections without consulting the existing mathDef source/definition inventory.
4. Record reviewed, permitted source collection URLs and access/rights evidence in batches; checkpoint source registry to GitHub frequently.
5. Complete and seal Stage 1. **Next stage after that: Stage 2 term-title inventory, recommended effort Instant** (or Medium for difficult index sites).
6. Do not begin Wave 2 until Wave 1 has produced an inspected, functional prototype. Do not compare either wave to production content until both waves are frozen.

**No further feature coding is a prerequisite to BEGINNING the controlled reconstruction trial.** The experiment can reveal opportunities for refining parsers, context scoring and preview semantics without postponing the first wave indefinitely. Record discoveries in this checkpoint if modifications are needed.

## Resume after timeouts

Read this file, the runbook, the current project profile and the active experiment's \`state/checkpoint.json\`. Check \`git log -1\` and latest CI. Run \`python -m research_pipeline.engine.cli --workspace WORKSPACE status\`. Continue the next incomplete task at the recorded Instant/Medium/High effort; never restart previously sealed stages or import production citation seeds. Update the checkpoint after each completed stage.

## Reconstruction live progress — 2026-10-18

- **Wave 1 Stage 1 source discovery: 9 independently selected source collections committed and Stage 1 state sealed** at `research_pipeline/experiments/reconstruction-v1/`. Source registry: `records/sources.jsonl`; queue: `tasks/sources.jsonl`; seal and digest: `state/sources.json`; handoff: `state/checkpoint.json`.
- Stage 1 digest (canonical engine-style SHA-256 of ordered source records): `eefb63f653c727bdda4caba61e32f271a71869c1b6e41d7c0c4c3c80e16d3356`. Nine records: EOM, PlanetMath, Stacks Project, OpenStax Calculus Vol 1, ProofWiki, MIT OCW, NIST DLMF, Wolfram MathWorld, AMS MathSciNet. The sources were independently researched using public external materials; **no terms or definitions were collected**, and no production mathDef corpora/source catalog/citation records were inspected.
- Access/rights caution: EOM mixes copyrighted Springer articles and later open contributions, so use locators only; DLMF and MathWorld prohibit bulk copying; OpenStax and MIT OCW use noncommercial share-alike licenses, so use locators only until compatibility is reviewed; AMS MathSciNet is a paid/subscription source, not eligible for ingestion. PlanetMath and ProofWiki have CC BY-SA rights but attribution and site crawl restrictions still apply.
- Stage 1 records/schema and sealing digest were checked against the `engine/core.py` source contracts and independently calculated; **the actual Python CLI and test suite were NOT run in this chat runtime** because a full repository checkout was unavailable. GitHub commit status API returned no reported statuses for the checked commit; do not claim CI passed or that the seal was executable-CLI verified. Before Stage 2, run the tests and `python -m research_pipeline.engine.cli --workspace research_pipeline/experiments/reconstruction-v1 status` on a repository checkout and verify the seal. This is a validation follow-up, not a request to reopen source selection.
- **Next stage: Wave 1 Stage 2 raw term-title inventory**, recommended effort **Instant** (switch to Medium if source index structures prove difficult). Exact next command after CI/status checks: `python -m research_pipeline.engine.source_manifest --workspace research_pipeline/experiments/reconstruction-v1 --output source_pages.jsonl`. Do not harvest terms before beginning Stage 2. Do not start Wave 2 or production comparison.

## Stage 2 execution workflow repair — 2026-10-18

- Implemented `.github/workflows/mathdef-stage2-intake.yml`, a read-only GitHub-hosted Stage 2 intake workflow with an explicit source allowlist. Triggered on appropriate engine/manifest changes or manual `workflow_dispatch`; no GitHub write token, ingestion, sealing, baseline definitions access, or production deployment.
- Implemented `research_pipeline/engine/stage2_actions.py`: bounded pages, HTTPS/robots checks via `source_intake`, source restrictions, page-level restart/checkpoint/report, deterministic raw candidate IDs, and artifact upload even on failures. Review instructions: `research_pipeline/STAGE2_ACTIONS.md`.
- Updated `source_intake.py`: explicit PlanetMath www/apex alias without allowing other hosts, alphabetical-index anchor support, and a dedicated Stacks section-title parser that tolerates omitted `</li>` tags.
- Added/revised regression tests; final isolated CI completed **22 tests successfully** at commit `f96edde0`.
- Last verified Stage 2 workflow: https://github.com/Zengez/mathDef/actions/runs/39169887545 (green but **partial**). Six Stacks Project chapters successfully yielded **306 raw term-title candidates** in uploaded artifact `stage2-title-candidates-39169887545-1`; PlanetMath remains blocked due to missing robots policy and was not bypassed. Removed navigation-only Stacks browse-page headings from the manifest and disabled temporary diagnostic output.
- Durable pointer: `research_pipeline/experiments/reconstruction-v1/state/stage2_execution_status.json`. The **existing 30 manually recorded candidates** still need reconciliation with extracted candidates; the 306 raw automated candidates are **not** yet ingested into the GitHub term registry. GitHub artifacts expire after 30 days. Stage 2 remains unsealed, Stage 3 not started, and no original production definitions were inspected.
- Next action: retrieve artifact, validate source title/locator accuracy and stable IDs, merge verified candidates using the existing engine ingest, expand safe source coverage, perform Medium review, then seal Stage 2. Instant remains suitable for collection, Medium for final technical audit.
