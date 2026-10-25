# Historical staging inputs — both Stage 1 transactions now APPLIED

These files were staged for **offline review before submission**; the folder name reflects their historical state when created. **Neither file is an outstanding unapplied request now. DO NOT RESUBMIT.**

- `alias.chat-postcoverage.20261025.shifted-operator.json` was validated and applied in the independent graph through commit `91f72555c759680c4229b3d6cb5b6958d1fbaa66`; receipt `dependency_graph/applied/alias.chat-postcoverage.20261025.shifted-operator.json`, digest `b3574ca780c053c6df1392a414df7eb86e5be1dab124dbf25f6fafe606883c11`.
- `filtration_prepare_manifest.json` was run through the real offline package engine. Its generated complete amendment packet `chat-postcoverage-realtime-filtration-edge-20261025-001.json` was applied via commit `a5e73476f35eca928e1f4b0966c6fed4fac2cf0f`; receipt `dependency_graph/applied/chat-postcoverage-realtime-filtration-edge-20261025-001.json`, digest `1517ea4b426f4dcf0fdec00dfc385b9d84fe125768c21b955526537c7cfa215f`. The preparer manifest is a **historical snapshot** and its prior unresolved fingerprint is stale after the alias; the live source node has also changed.

The graph is now at 420 unresolved canonical identities, 301 aliases and 771 amendment events. Original audit **421/421 reviewed** remains historically valid and immutable. Consolidation gate closed, Pass 3 unauthorized.

Verified exact graph receipts and all 19 mechanical readiness checks in [Stage 1 applied results](../STAGE1_APPLIED_GRAPH_RESULTS_2026-10-25.md). For **new corrections**, create fresh ID/version-bound manifests from `live_nodes` and current fingerprints. The updated generic preparer permits omitting `reference_index` entirely when exact `expected_occurrence_id` is supplied, preventing mixed seed/effective reference indexing errors. Do not use this historical path as a new transaction queue.
