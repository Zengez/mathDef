# Wave 2 fast population and deferred reconciliation

**Status: new experimental execution path.** The existing screened independent
Wave 2 corpus (639 historically reviewed formulations, 887 screened links at
checkpoint AB) and frozen Wave 1 are not migrated or rewritten. The generic
engine is reusable; mathDef-specific mathematical intake policy is an adapter.

## Research modes

**Populate:** Chat reads independent external references and makes source- and
context-specific mathematical judgments about the NEW work. Build a JSON
research package with observations, candidate formulations, version-anchored
individual review states and optional prerequisite links. Missing prerequisites
are recorded with target_query and deferred, not recursively pursued. Never
consult original mathDef definitions, variants or citations. The generic
engine validates record identities, provenance, source access rights, typed
references and append-only integrity, then writes only under
reconstruction-v2-independent/population/. It does not recheck previously
screened mathematical conclusions or make any new claim of human peer review.

**Reconcile:** Build a shared audit report with incomplete review decisions,
unresolved target queries, candidate link reviews, possible context duplicates,
cycle candidates and affected edges following corrections. Consolidate common
missing prerequisites, review mathematical equivalences and source quality,
and resolve source/context discrepancies in topic-appropriate sessions. The
audit is a work queue, not a machine-generated approval of mathematical truth.

**Certify:** A read-only readiness check fails while reconciliation findings
remain. After reconciliation and promotion into the main independent registry,
the existing full integrity, mathematical, citation, dependency and rendering
checks must run and Wave 2 must be frozen. The generic readiness check alone
does NOT promote, seal or publish; it is not an independent expert audit.
Only after the independent freeze can the original production mathDef corpus
be consulted for the planned reconstruction comparison.

## Package protocol

Store each research package as JSON under:

    research_pipeline/experiments/reconstruction-v2-independent/population/inbox/BATCH_ID.json

Required top-level fields are schema_version=1 and a unique id. Optional arrays
are sources, terms, observations, meanings, relations, reviews, issues and
revisions; at least one must be nonempty. Use the ordinary underlying
source/term/observation/meaning schema. Every new meaning has a precise
mathematical context and one or more formulations whose review_state is
"candidate", evidence_ids identify actual source observations, and
mathematical_rationale explains its specific source and mathematical scope
(60+ characters for mathDef).

Add one review per new formulation with id, formulation_id, status (pending,
provisional, screened, held, rejected), reason, and formulation_sha256.
Compute formulation_sha256 as SHA-256 of canonical JSON with keys:
{"formulation": <complete-formulation-object>, "context": <meaning-context>}.
The implementation's digest function can do this. A screened review
additionally needs a substantive reason and reviewed_by; this locally
recorded decision NEVER automatically admits the draft as a screened
publication. New source-driven links must have source_phrase where known,
editorial_reason, and either an existing target_meaning or a deferred
target_query. No unsupported target should be invented.

To correct an existing draft without rewriting its original evidence, submit
a later research package with a revisions array containing id, kind,
target_id, expected_sha256 (digest of the CURRENT draft record), replacement
(the full record with the same ID) and reason. The append-only revision log
retains the old version. The reconciliation audit then identifies potentially
affected links.

## CLI

From repository root:

    python -m research_pipeline.engine.population --workspace research_pipeline/experiments/reconstruction-v2-independent --mode populate --batch research_pipeline/experiments/reconstruction-v2-independent/population/inbox/BATCH_ID.json --policy research_pipeline.adapters.mathdef.population_policy
    python -m research_pipeline.engine.population --workspace research_pipeline/experiments/reconstruction-v2-independent --mode reconcile
    python -m research_pipeline.engine.population --workspace research_pipeline/experiments/reconstruction-v2-independent --mode status
    python -m research_pipeline.engine.population --workspace research_pipeline/experiments/reconstruction-v2-independent --mode certify
    python -m unittest research_pipeline.tests.test_population -v

The consolidated workflow .github/workflows/research-population-batch.yml
takes mode and batch_path; commit the reviewed JSON research package to
main first. The workflow serializes repository writes, checks the new package,
and commits only population records and audit output. It does not read
production mathematical definitions.

## Session operating procedure

1. Read the short independent Wave 2 checkpoint and population audit/status;
   select breadth-oriented new topics, collision-check only likely overlaps.
2. Work on mathematically useful source evidence and new contextual
   formulations; mark ambiguity or missing prerequisites without stopping
   the whole batch. Do not repeatedly audit the earlier screened corpus.
3. Package multiple new concepts if supported by the available Chat response
   window, commit each bounded package, and verify GitHub workflow status.
4. Stop before the Chat response timeout; give a compact durable handoff with
   actual committed package IDs, failed or pending runs, and the next query.
5. After an agreed first-pass coverage milestone, reconcile all provisional
   work, run full certification/preview tests, freeze, and then compare.

This workflow never runs independently of Chat's research decisions and is
not a background Chat agent. A green GitHub Action certifies mechanical
execution and tests, not the mathematical correctness of newly added claims.

## Separation and forward compatibility

The population ledger is intentionally **not included in the totals of the
previously screened main Wave 2 registry**. Until reconciliation/promotion,
count its drafts separately. The frozen Wave 1, original mathDef production
website and every historical batch script remain unchanged.

The generic population engine has no mathematical vocabulary. Other projects
may provide their own adapters for theorem hypotheses/proofs, educational
terminology, or other research domains.

## Explicit reconciliation-to-promotion bridge (implemented 2026-10-21)

The mathDef adapter exposes a separate opt-in gate:

    python -m research_pipeline.adapters.mathdef.population_promotion --workspace research_pipeline/experiments/reconstruction-v2-independent

Preflight blocks on unresolved population audit findings, missing or stale
formulation reviews, missing prerequisite dispositions, unresolved target links,
source and rights failures, cycles, or duplicate meanings. Every individual
mathematical formulation needs a CURRENT version-anchored screened review with
a substantive reason and reviewer attribution. Every formulation either has
screened prerequisite links or an explicit justified no-supported-target
disposition. Each link needs exact source and target locators and independent
review rationale; provisional link candidates cannot be promoted.

To authorize promotion, create a separate explicit approval JSON file inside
the independent population/ directory. Required keys are
approved_for_independent_promotion=true, draft_digest,
preexisting_catalog_digest, preexisting_review_digest, reviewer, and rationale.
The three SHA digests must equal the preflight output. Never supply approval
just because a mechanical audit passed: this requires substantive research
reconciliation.

To apply after independent review:

    python -m research_pipeline.adapters.mathdef.population_promotion --workspace research_pipeline/experiments/reconstruction-v2-independent --approval PATH_TO_APPROVAL_JSON --apply

This moves source-screened material into the unsealed independent Wave2
registries, archives the existing review ledger, then refreshes the
global-catalog references in a single deliberate operation. It does not seal,
publish, compare with original mathDef, or claim human external peer review.
Actual live promotion must run on a Git branch with a single reviewed commit.
It does not run as part of the normal population workflow.

The promotion adapter currently supports one whole-ledger approval/promotion,
not incremental re-promotion of previously promoted draft IDs. Its fixture
tests cover provisional rejection, explicit approval, and stale approval
rejection. An independent mathematical reconciliation remains necessary.

The normal consolidated workflow is now automatically triggered by a committed
JSON research package on main in population/inbox. It processes unapplied
packages idempotently, updates STATUS.json, and builds QUEUE.json.
workflow_dispatch remains available for manual runs.
