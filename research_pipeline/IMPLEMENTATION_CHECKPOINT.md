# Research Pipeline — Implementation Checkpoint

**Updated:** 2026-10-18. **Current phase:** Implementing the reusable engine and mathDef adapter (not running the independent reconstruction). **Keep production definitions, variants and website intact.** Use RESEARCH_PIPELINE_ENGINE_DESIGN.md for the accepted architecture and research_pipeline/README.md for existing commands.

## What is implemented and committed

1. **Portable engine** in `research_pipeline/engine/core.py` with JSONL registries for sources, discovered terms, observations, meanings/formulations, and proposed relations. Uses stable IDs, cross-record validation, source access/rights checks, atomic checkpoint metadata, record-level idempotency, batch fsync, stage seals/content digests, and automated eligibility screening before experimental publication.
2. **CLI** at `python -m research_pipeline.engine.cli` with `init`, `queue`, `ingest`, `seal`, `status`, `publish`, `wave2-plan`, and `fork-wave2`. The command-line entrypoint does not mutate ChatGPT thinking level; work queues recommend only **Instant, Medium or High**, matching available user controls.
3. **Chat work queue generator** in `engine/queues.py`: one source discovery request from the project profile, term index tasks per permitted source, content tasks per observed term/source, clustering batches and meaning-level linking tasks. Saves stage tasks and status summaries.
4. **Isolated mathDef adapter** in `adapters/mathdef/preview.py` creating a separate `preview/index.html` and preview catalog. Displays multiple contextual meanings and formulations grouped under one term, a source-evidence dialog and an unverified disclaimer. This is a minimal preview, **not** the production site: full mathematical rendering, nested/inline interactions and GitHub verification submissions remain future development.
5. **Wave split:** stage seals and publication preserve the initial prototype; `wave2-plan` constructs source/variant/link research queues; `fork-wave2` creates a separate unsealed workspace using only prior experiment records, without touching the first-wave workspace or the original mathDef corpus.
6. **Independent tests** `research_pipeline/tests/test_pipeline.py` and `test_queues.py` exercise the Stage 0–6 flow with synthetic Closure/field examples, term-group variants, sources, browser preview generation, paid-source restrictions, duplicate replay, conflict rejection, integrity tampering, stage ordering and wave2 fork/queue. A dedicated workflow `.github/workflows/research-pipeline-ci.yml` runs tests without depending on production mathDef tests.
7. **Existing repository CI regression fixed:** `scripts/build_index.py` now permits scoped tests to omit unrelated variant parents, but **full-site builds still require every variant parent** via strict validation. The standard Pages and corpus audit workflows subsequently completed successfully (commit `7ce27691`; later changes require their own CI checks).

## Known limitations / not yet implemented

- Stage 1 research is chat-driven; currently no automatic discovery/scoring of authoritative source websites. That is intentional: source reliability requires researched editorial judgment.
- Stage 2/3 are not yet connected to a robust, rights-aware source-index reader/crawler and content-locator extractor. The engine accepts independently gathered JSONL candidate records and generates research work queues.
- Stage 4/5 **do not perform semantic or mathematical reasoning autonomously**; the assistant/user must research, classify and formulate reviewed intake records in chat. Automatic context-based link ranking is not implemented.
- Stage 6 produces an eligible-draft `published/catalog.json` **inside the experiment**, not a publicly deployed second site. No true reconstruction or comparison has yet been conducted.
- The second-wave fork can append new records, but edits to prior IDs require an **explicit audit-tracked revision mechanism** before it is safe to refine previous forms/meanings. Do not work around this by silently rewriting sealed records.
- Raw observations are kept; the source modal currently shows citations used by screened published formulations, not a complete reviewed/rejected/consolidated source-history browser. UI and provenance linkage must be expanded later.
- Workspaces checkpoint to local files after configured batches; if executing in ephemeral chat environments, explicitly commit the workspace/checkpoint to GitHub at regular intervals (the engine does not have GitHub credentials).
- The full independent baseline vs reconstructed Wave 1 vs reconstructed Wave 2 comparison harness is not yet implemented. The existing mathDef corpus must be used only by that **post-freeze evaluator**, never as seed material.
- Tests verify structural, source-policy and replay constraints, not mathematical rigor or provenance truth. Human verification remains distinct.

## Immediate safe next development task — recommended thinking: Medium

**Implement the Stage 2/3 source intake bridge**: a robust, bounded, rights-aware source-index/locator reader that converts permitted external catalog/index material into term observations. Use offline HTML/API fixtures to prove parser reliability and avoid downloading unlicensed source prose. Also complete explicit, versioned second-wave revision handling so previous meaning/formulation records can be corrected with a revision ledger rather than being frozen forever. Test these changes in the isolated CI workflow. Do not yet launch the real corpus reconstruction.

After that, develop a separate post-freeze evaluation harness (source/term/meaning/relationship recovery, ambiguous semantic-match review queue, efficiency tracking), and only then consider running the two reconstruction waves with independently discovered source inputs.

## Resume instructions

1. Read this file and `research_pipeline/README.md` and then the accepted design file.
2. Check HEAD and the dedicated GitHub Actions workflow before continuing. Earlier rapid commits may have caused older runs to be canceled; use the newest successful run.
3. Preserve `research_pipeline/engine/` independence from `research_pipeline/adapters/mathdef/`. Never read production `definitions/`, `variants/`, `CITATION_AUDIT.csv`, `DEPENDENCY_LINKING.md` or other production content while populating reconstruction records.
4. Add tests and small commits. Checkpoint after manageable batches; update this file at each completed development task.
5. Recommended user ChatGPT thinking setting for the **next** task: **Medium** (source intake). High will be recommended when semantic/relationship reasoning begins.
