# Current mathDef checkpoint — 2026-11-03

The original .tex definitions, reviewed variants, independently researched Wave 2 content and post-Wave2 additions are **already published** as one versioned, cleaned v2 definition feed. The authoritative source files remain in `definitions/`, `variants/`, `data/`, and the research records/curated additions under `research_pipeline/experiments/`.

**Production:** `.github/workflows/pages.yml` builds and deploys mathDef. Keep the core `scripts/build_index.py`, `research_pipeline.adapters.mathdef.preview_site`, `publish_root`, `scripts/merged_definition_export.py`, `scripts/validate_published_corpus.py` and the shared UI components. These are required for the current combined site and mathThm's definition feed.

**New content / future discovery:** Edit original `.tex` definitions or curated research records as appropriate; use the release candidate and combined-preview tests before merging. Keep `scripts/current_corpus_discovery.py` and `scripts/discovery_checkpoint.py` for incremental scans, `arxiv-scan.yml` and `wikipedia-discovery.yml` for on-demand intake. The research discovery ledgers and unpromoted candidate dispositions remain preserved so deferred content can be reconsidered without reconstructing history.

**Retired:** one-time October 2026 Stage-only cleanup, contextual review and batch triage Actions; specialized scripts that only validate or regenerate those finished passes. Their completed mathematical and provenance data remain in the repository. Historical audit diaries are recoverable from Git history, rather than maintained as current operating instructions.

See `README.md` for user-facing behavior, `research_pipeline/README.md` and `research_pipeline/WAVE2_SIMPLE_WORKFLOW.md` for curated independent content, and `DEFINITION_EXPORT.md` for public feed generation.
