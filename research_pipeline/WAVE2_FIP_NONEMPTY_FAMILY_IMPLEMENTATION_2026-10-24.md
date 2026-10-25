# Approved independent Wave 2 FIP compactness wording — integration checkpoint

**Status: source wording edited on isolated branch only; NOT READY TO MERGE until the versioned graph scan is safely re-anchored and tested.**

## Explicit mathematical approval and exact change

The user accepted the nonempty-family qualification to repair the empty-space/empty-family counterexample. This branch changes exactly the `text` field of `form.wave2.broad67.compact-closed-fip` in the authoritative independent-only `records/meanings.jsonl`, under `meaning.wave2.broad67.compact-topological-space`.

Previous text:

> Equivalently, X is compact if every family of closed subsets of X that has the finite intersection property has nonempty total intersection.

Approved revised text:

> Equivalently, X is compact if every **nonempty** family of closed subsets of X that has the finite intersection property has nonempty total intersection.

The old evidence observation, which is a historical paraphrase, is **not** rewritten or passed off as a verified external quote. Its observation ID is `obs.wave2.broad66.compact-space.02`, and its source metadata is `src.proofwiki`. Source verification remains an independent later task. No production or frozen Wave1 mathematical content was accessed.

The existing missing FIP candidate `missing.ded806b239b007c8af8c` retains the original explicit **nonempty finite subfamily** interpretation; the independent compactness theorem alone is qualified. No candidate identity, meaning label or topological hypothesis was changed.

Proof of the precise mathematical equivalence (including the empty topological space) is in `research_pipeline/WAVE2_PASS2_CONVENTION_ADJUDICATION_PROPOSAL_2026-10-24.md`.

## Exact version audit

The version computation was reproduced using `research_pipeline.engine.core.digest` semantics: canonical sorted-key UTF-8 JSON SHA256 of `{"formulation": form, "context": meaning.context, "source_snapshot_sha256": digest({"observations": [observation], "sources": [source]})}`.

- Previous active formulation version: `e6a0aa44634543ff92c50272643e6d7a42152bc50827bbbd925d745849f036bb`.
- **New formulation version:** `844fa46b00ce7ef7960240f19be908bf46ae0985f5f45de1195b8137d61ed213`.
- Unchanged source-provenance snapshot: `bf47fb7b275dbc285237b1465610976b3d3555a86ca1dbd952b82572aae2994c`.
- Historical original base node and existing 3 reviewed amendments remain tied to the old version. They must **not** be deleted or rewritten to forge history.
- Historical amendment IDs: `amend.pass2.foundations_topology.20261022.04`, `amend.global_audit.cycle.20261023.06`, `amend.round178.compact_closed_subset.20261023.01`.
- No existing candidate-resolution or seed-override event directly targets this modified formulation/meaning in the examined ledgers. Nevertheless independently validate all version-bound edges after updating the inventory.

## Important blocker: source edit requires a fresh scan

`dependency_graph.live_nodes` discards a node whose `version_sha256` no longer matches the inventory. After `inventory_sync`, the old compactness FIP node is **not a current complete scan**, and its historical same-version amendments are correctly inactive for the changed formulation. This is expected version protection, **not** an excuse to bypass integrity checks.

The effective old-version formulation adjacency, from the last approved amendment, contains five references to carry through a fresh full-formulation semantic review:

1. `occ.97765f07f6424c30d4f7` — open-cover alternative: `external` defining/equivalence condition (never a self-edge).
2. `occ.2fb4cd2d7de4fa4994e4` — closed-subset predicate: `missing.622459998fd4b876125d`, which currently aliases to canonical `missing.c4ed408b10943e9c0f8e` (not the ambient topological-space meaning).
3. `occ.28173daad7376ce1805d` — FIP family property: `missing.ded806b239b007c8af8c` (the separately preserved nonempty finite subfamily convention).
4. `occ.f55220b0d16dc1524f92` — nonempty total intersection: `external` defining criterion, not a distinct newly researched term.
5. `occ.6a4bd77e2974b5d6fbac` — equivalence to open-cover compactness: `external` criterion.

The source phrase `nonempty family` is a quantifier/restriction on the indexed family in this theorem, not a new mathematical concept, and does **not** automatically require new candidates or a different family-identity merge.

**Offline scan packet prepared:** `research_pipeline/WAVE2_FIP_NONEMPTY_FAMILY_OFFLINE_RESCAN_PROPOSAL.json` contains the complete five-reference proposed `ingest` payload, the checked new version hash, source-free rationale and retained contextual missing identities. It is deliberately **outside** the live graph inbox and contains `proposal_only: true`; it must not be treated as an applied receipt. The engine's `make_snapshot` derives new occurrence IDs from the revised source version and reference details. Thus the five occurrence IDs listed above anchor the **historical** scan only; fresh IDs are expected after re-ingestion. Preserve those old IDs in immutable prior history and verify candidate identity/provenance through the new effective graph rather than insisting that occurrence IDs remain unchanged.

**Branch CI currently expected to fail until graph re-anchoring:** [isolated research pipeline run #40148083600](https://github.com/Zengez/mathDef/actions/runs/40148083600) passed the isolated unit tests and global audit steps but failed `resume_checkpoint --check` with `ResumeError: Stale formulation meaning context or catalog digest`. This is a real staleness condition caused by source-only modification, not a harmless warning or a reason to bypass the validator. Do not merge while it persists. A reviewer should verify that all five effective references remain valid and determine whether the preexisting FIP reference `matching_note` about the now-resolved empty-family concern needs updating for accuracy. Preserve the precise original occurrence provenance wherever that representation is supported.

### Required integration sequence, not yet executed

1. On an isolated copy of the **independent Wave 2 only**, run the normal `inventory_sync` and verify exactly one changed formulation version. Inspect for version-sensitive resolutions/seed overrides; never silently drop valid mathematical work.
2. Recreate one `complete` **version-anchored reviewed scan for the new formulation version**, based on a full review of all five current effective references; use the engine's supported ingestion workflow, not direct edits to the old immutable node or amendment ledger. Keep original prior-version amendments as history.
3. Before proposing any merge, run the relevant synthetic and independent graph tests in a disposable workspace. Verify that the revised source and rebuilt graph indexes agree, the five effective references and existing canonical candidate relationships are preserved, and no unrelated mathematical records or count changes occur.
4. Only after that, submit the properly reviewed new-version ingest package through the established graph inbox path with explicit authorization for the graph update; validate the actual resulting `STATE.json`, `CHECKPOINT.json`, `INVENTORY.json`, candidate registry, seed/review ledgers, and 19-check readiness assessment.
5. Update the current handoff once the applied hashes and new state are verified. The old inventory SHA256 `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492` and unresolved fingerprint `61246db4cb0897ac3bfdb43f8a8e6be361e2f05bf905367bfbda0b388a541113` become **stale** after the source-version migration. Do not use them in any consolidation packet.

**No consolidate event, consolidation gate, Pass3 research, external source lookup, production definition changes, broad mathematical retargeting or unreviewed automated correction is authorized.**

This is a precisely bounded implementation checkpoint: the approved source-text edit is present on the feature branch, but main's graph remains valid and untouched until a new-version scan has been reviewed and safely applied.