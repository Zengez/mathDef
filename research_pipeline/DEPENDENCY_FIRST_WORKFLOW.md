# Dependency-first Wave 2: operating protocol

**Experimental only.** The authoritative design is TEMP_DEPENDENCY_FIRST_WAVE2_PLAN.md, especially section 8. Automated closure is not mathematical certification, manual approval, promotion, publication, or a Wave 2 freeze. Frozen independent Wave 1 and historically screened independent Wave 2 remain read-only; original production mathDef definitions are forbidden inputs.

## Start here after interruption

Read this file, TEMP_DEPENDENCY_FIRST_WAVE2_PLAN.md, then independent dependency_graph/CHECKPOINT.json, STATE.json and INVENTORY.json. Inspect the shared missing candidate registry and the research queue. Never reparse an unchanged, complete, version-valid node. Source population records and Batches 139–142 remain separate, unchanged inputs.

## Stored schema

Workspace: research_pipeline/experiments/reconstruction-v2-independent/dependency_graph/

- INVENTORY.json: independently screened and separately provisional contextual meanings and every individual formulation, context and source-content hashes. Existing relations are imported as seeds and do NOT prove exhaustive scanning.
- nodes/FORMULATION_ID.json: complete atomic per-formulation adjacency snapshots, version hash, individual occurrences and scan status.
- occurrences.jsonl, edges.jsonl: reproducible exact occurrence and edge ledger.
- missing_candidates.jsonl: shared contextual missing candidates, with incoming dependent forms and occurrence counts.
- reverse_index.json: reverse dependents for meaning nodes and missing candidates.
- resolutions.jsonl: append-only, version-anchored editorial mappings to newly admitted or pre-existing meanings.
- STATE.json and CHECKPOINT.json: derived Open/Closed and scan/completion states, hashes, counts, and restart instructions.
- inbox/: review-authored semantic scan and missing-candidate resolution inputs.

An unscanned formulation is not a completed scan even if it has screened pre-existing links. Algorithmically suggested lexical matches are explicitly scan_incomplete. Only a separate exhaustive contextual review can supply a complete scan snapshot. The review does not certify mathematical correctness.

## CLI

From repository root, where WORKSPACE means research_pipeline/experiments/reconstruction-v2-independent:

    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode inventory
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode propose --limit 40
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode status
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode queue --limit 20
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode tree --root-formulation FORMULATION_ID
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode ingest --batch "$WORKSPACE/dependency_graph/inbox/SCAN.json"
    python -m research_pipeline.engine.dependency_graph --workspace "$WORKSPACE" --mode resolve --batch "$WORKSPACE/dependency_graph/inbox/RESOLUTIONS.json"
    python -m unittest research_pipeline.tests.test_dependency_graph -v

The independent dependency graph GitHub Action performs bounded pilot proposals on push to its own code/tests or workflow_dispatch, sharing the existing population write concurrency group. It retries branch push collisions by recomputing from fresh main. A GitHub commit of the full graph folder is the only durable checkpoint across Chats or runners.

## Semantic intake contracts

A committed scan JSON batch contains schema_version=1 and items. Each item supplies formulation_id, exact INVENTORY version_sha256, references array, complete flag, and for complete scans a substantive review_rationale (40+ chars). Each occurrence must have phrase and state of existing, missing, ambiguous, external or deferred. Existing needs exact target_meaning_id; missing needs context to stabilize a shared missing_candidate_id; ambiguous/deferred needs an explanatory reason; external needs a justified disposition. Optional span offsets are checked against original formulation text.

Resolution batches contain schema_version=1 and resolutions array. Each resolution needs missing_candidate_id, target_meaning_id, target_version_sha256 (digest of the target INVENTORY meaning descriptor), and substantial contextual review_rationale. Resolution never creates a new definition. Add source-supported new meanings through the existing provisional population ledger, then sync the inventory and resolve the stable candidate. All previously screened reviews remain untouched.

## Crash-safe operation and closure

A node snapshot is a single atomically written file containing the entire occurrence list, digest, and completion marker. A missing, truncated, corrupted, mismatched or older-version file does not count as scanned. Rebuild derives reverse indexes, missing candidates, Open status, and checkpoint from valid committed snapshots; replay never needs in-memory stacks.

A rooted tree is expanded from stored immediate edges with a current-path visited set; the closing edge of a cycle is still shown, but its subtree terminates. Closure uses reverse propagation of blockers to a fixed point. Existing closed cycles are mechanically allowed; truly circular mathematical definitions remain a later mathematical audit problem.

Research queue prioritizes shared missing dependencies after contextual scans are reviewed. New dependency-driven provisional research may enlarge the graph and create more missing dependencies. Unrelated broad topic Batch 143 remains suspended until structural stabilization. Do not silently reinterpret old population/QUEUE.json recommendations as current priorities.

## Explicit limitations (follow-up implementation)

Automatic exact-display-name proposals are not mathematically exhaustive and do not close scans. Exact normalized phrase+context deduplication is deliberately cautious; aliases, homonyms, and source-specific synonym equivalence require mathematical review. Current append-only resolution snapshots and complete scans cannot be editorially changed in place without a new formulation version; a dedicated correction-event ledger for same-version semantic corrections is a next engineering task. No automatic independent mathematical source investigation, review certification, promotion, public-site change, or Wave 2 freeze occurs.

Retain the temporary design note until outstanding requirements and pilot reviews are incorporated into durable machinery.
