# Reusable scholarly acquisition engine — initial implementation

**Status:** Engine core, local batch importer, stage seals, automated publication gate, and an isolated mathDef prototype adapter are implemented. **Live source crawlers, intelligent semantic classification, contextual automatic link ranking, community verification UI, and the full independent reconstruction have NOT been implemented or run.** Do not claim the experiment has been completed.

## Two bulk waves and targeted work

1. A deliberately linear **first wave**, performing Stages 0–6 to get a coherent, inspectable prototype.
2. Freeze first-wave findings and a comparison-independent evaluation snapshot. The **second wave** produces source discovery, synonym/variant and relationship research queues, followed by new acquisition and review in a *new* workspace or version. It must not overwrite the sealed first-wave output.
3. **Targeted acquisition** will invoke the same stage APIs with more detailed context/variant exploration, after the initial infrastructure and adapters are ready.

The scripts execute **mechanical validation**, file operations and work-list generation. They do not independently call ChatGPT or certify mathematical accuracy. Human/assistant reasoning in chat supplies Stage 1 source assessments and Stage 4/5 semantic decisions. Stage-specific recommended effort uses the available **Instant, Medium, High** settings; scripts only REPORT it, not change model settings.

## Initial CLI usage (Python 3.10+, standard library)

From repository root:

    python -m research_pipeline.engine.cli --workspace research_pipeline/experiments/reconstruction-v1 init --config research_pipeline/project_profiles/mathdef_reconstruction.json
    python -m research_pipeline.engine.cli --workspace research_pipeline/experiments/reconstruction-v1 status

Create independent JSONL candidate records for Stage 1, then:

    python -m research_pipeline.engine.cli --workspace research_pipeline/experiments/reconstruction-v1 ingest sources --input /path/to/independent-sources.jsonl --batch-size 5
    python -m research_pipeline.engine.cli --workspace research_pipeline/experiments/reconstruction-v1 seal sources

Repeat with stage names: terms, observations, meanings, relations, **in that order**. Source discovery must NOT import production mathDef source files or browse its definitions. A future crawler will feed the intake contract; until then, ChatGPT research/batches produce the intake files.

After all five stages are sealed:

    python -m research_pipeline.engine.cli --workspace research_pipeline/experiments/reconstruction-v1 publish
    python -m research_pipeline.adapters.mathdef.preview --workspace research_pipeline/experiments/reconstruction-v1
    python -m research_pipeline.engine.cli --workspace research_pipeline/experiments/reconstruction-v1 wave2-plan

The preview is independent, local and **does not deploy to GitHub Pages**. Publication creates an eligible-draft catalog in the experiment directory, not a public production site. Separate staging/approval is needed before making it public.

To test without web access:

    python -m unittest discover -s research_pipeline/tests -v

## Stage intake records (one JSON object per line)

All rows require unique, stable lower-case IDs (letters, digits, dots, hyphens, underscores), except field values such as labels and URLs. The importer refuses content changes under an existing ID: corrections must be represented by a deliberate, versioned editorial update method (not implemented yet).

- **sources:** id, title, https URL, authority_reviewed (bool), rights (permitted/locator_only/unknown/disallowed), access (free/paid/unknown); optional quality and licence notes. Paid sources may be **catalogued**, never silently purchased or copied.
- **terms:** id, label, source_id, locator. One observed title per source occurrence; synonyms may later consolidate.
- **observations:** id, term_id, source_id, locator, record_kind (locator/paraphrase/licensed_excerpt), text for the latter two. Paid/restricted material cannot be acquired as text. When in doubt use locator-only and independent original prose later.
- **meanings:** id, term_group_id, display_term, context, term_ids (array), formulations (array). A formulation requires id, text, evidence_ids (nonempty) and review_state (candidate/screened/blocked). Several meanings can use the same term_group_id; alternative formulations live within each meaning.
- **relations:** id, from_formulation, target_meaning, relation_type, review_state. A relation with review_state candidate is excluded from the published graph until screened.
- **publication:** the engine requires sealed input stages and stable content digests; only screened formulations with reputable, permissible evidence pass the gate. It marks resulting content **Not yet manually verified**. Held candidates remain in the catalog with reasons; none is treated as peer reviewed.

Stage seals prevent accidentally changing first-wave inputs after research decisions are finalized. A second wave should start from a separately versioned workspace/snapshot; migration utilities and merge decisions are future work.

## Durable restart and checkpoints

Each ingest writes append-only JSONL records, flushes/fsyncs every configurable batch (default 10), writes atomic state summaries and a top-level state/checkpoint.json. Replaying an unchanged batch safely skips preexisting records; a changed ID fails rather than silently overwriting work. Stage seals record content digests checked before publication. GitHub commits are still required for durability **across hosted chat sessions**, because generated local filesystem state may be ephemeral. The pipeline scripts do not automatically write GitHub commits.

Stage handoff should state a concrete next command and recommended effort, and link the active workspace and current git commit. Testing interruption/replay is part of the included tests.

## Data isolation, evaluation and safety

The engine and mathDef adapter only read their supplied experiment workspace. They do NOT import production definition files, source catalogs, citation ledgers or link overrides. **Do not give the new source-discovery phase the original mathDef URLs as seeds.** Once a first-wave and second-wave snapshot is frozen, a separate evaluation process may compare recovery with the production corpus using source, term, meaning, variant, link and efficiency metrics. The production corpus is not unquestionable ground truth.

Use public authoritative sources only where permitted, respect website access policies and rate limits, and preserve source locators. A citation alone cannot establish mathematical correctness. The current preview is a prototype and deliberately lacks full KaTeX and production-site recursive navigation.

See [the overarching design](../RESEARCH_PIPELINE_ENGINE_DESIGN.md). The next implementation unit is a safe source index reader and a more complete wave-2 acquisition runner, followed by the comparison harness.
