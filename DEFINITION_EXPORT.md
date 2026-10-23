# mathDef public definitions snapshot (v1)

**Status: implemented October 23, 2026.** This is the consumer-facing, read-only export for mathThm and subsequent projects. It is generated from mathDef's **production** definitions, not from the separate, independent Wave 1 or Wave 2 research previews. It makes no claims of peer review or correctness.

## Published endpoints

- Manifest: https://zengez.github.io/mathDef/api/definitions/v1/manifest.json
- Snapshot: https://zengez.github.io/mathDef/api/definitions/v1/snapshot.json

The existing site search index (`definitions-index.json`) remains unchanged for the original frontend. The new feed is an intentionally stable, versioned integration contract.

## Update signal and consumer protocol

Each normal Pages build regenerates both files from the same sorted production definition records. The small manifest has `schema`, `snapshot_schema`, `dataset`, `version`, `sha256`, `definition_count`, and `snapshot_path`.

- A consumer GETs the manifest, preferably using HTTP cache bypass or conditional revalidation. No authentication or repository writes are needed.
- If `version` is unchanged from its last successful import, no snapshot download is needed.
- Otherwise GET `snapshot_path` relative to the manifest, preferably with `?v=<sha256>` to avoid a stale CDN response. Verify SHA-256 of the **raw UTF-8 bytes** against manifest `sha256`; only then atomically adopt the new local snapshot.
- If the manifest or snapshot cannot be fetched or verified, retain the last valid snapshot. Polling can happen on the consumer's build/deploy cycle or on a chosen interval; mathDef does **not** push cross-repository events in v1.
- `version` is content-addressed, not a monotonically increasing counter or a Git commit hash. Unchanged definitions across deployments yield the same version. Do not infer version ordering from hashes.

When a mathDef production definition, alias, source, formulation, contextual dependency, or other exported field changes, the snapshot hash changes. Publication occurs through the existing `.github/workflows/pages.yml` build on pushes to `main`. The manifest is a change signal **once Pages has deployed**, not instant notification of a source commit. Depending on CDN caching and deployment timing, consumers may briefly see an older manifest; they should retry rather than combine mismatched files.

## Snapshot schema

The document has `schema: "mathdef.definition-snapshot.v1"` and a `definitions` array sorted by stable `id`. Each record supplies `id`, `term`, `aliases`, `body`, `source`, `status`, `category`, `path`, `related`, `dependencies`, and `formulations`.

Each formulation retains its original label, source, content, and known dependency links with contextual information. Definitions without alternate formulations receive a synthetic `primary` formulation in this export (without modifying mathDef source files). Consumers can index labels/aliases and use body/formulations for local expandable definitions; mathematical term disambiguation and search semantics remain the consumer's responsibility.

This v1 schema is additive and isolated from the original production UI. Any incompatible future changes should publish under `v2` rather than silently altering the contract.

## Build and test

- Build: `python scripts/build_index.py`
- Export outputs: `_site/api/definitions/v1/manifest.json` and `_site/api/definitions/v1/snapshot.json`
- Tests: `python -m unittest tests.test_definition_export -v`
- Normal Pages CI already executes all tests under `tests/` and the builder before publishing.

## Future integration work

- Independent Wave 2 is an experimental research corpus and **is not quietly mixed into the production feed**. Once the independent dataset is intentionally promoted or given its own well-defined feed, discuss whether consumers should subscribe to a separate channel.
- Future projects may eventually benefit from push-style update notifications, a changed-ID delta feed, or a shared mathematical term-linking library. None is necessary for the first mathThm prototype.
- Cross-project missing-definition intake remains owned by mathDef, with no automatic write-back from mathThm.
