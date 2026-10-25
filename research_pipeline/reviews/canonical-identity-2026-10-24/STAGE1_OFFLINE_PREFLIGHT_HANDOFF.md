# Stage 1 — offline semantic reconciliation preflight handoff

**Review anchor:** original 421/421 coverage commit `6616d53ac5449bd8ea81b8e804631709fac74459`, active inventory digest `34f61b6cf7fd1e80bda932dc8eeac473a729b11dfa0ba849c6db424b7a8f8113`, unresolved-pool fingerprint `eb9beb4199a99b1dc3fc18b57daa1f1d4cc9c66051caa558acb7a48396242cee`. Work remains on [draft PR #10](https://github.com/Zengez/mathDef/pull/10). **Not in the active dependency_graph inbox. Nothing has been applied.**

Stage 1 contains **exactly two independent, reviewer-authored, unapplied proposed changes**; it does not attempt to resolve all 51 postcoverage questions:

1. `staged-not-applied/filtration_prepare_manifest.json`: a read-only preparer manifest for a **complete-formulation semantic amendment** to the real-time adapted process, changing the incorrect existing discrete-filtration occurrence `occ.4dc2044654482ca4b966` into an explained external/provenance-only reference. This edit specifically **retains** the correct real-time missing occurrence `occ.3cee100f060f105c219b` → `missing.65d334caa51c845ea335`, plus the other five effective source references. The manifest uses the **minimal delta** `updates` and `remove_fields=["target_meaning_id"]` rather than a full replacement object, so unrelated metadata is retained. It is anchored to `form.wave2.found85.adapted-continuous`, exact effective node SHA `c9620ad31916c4847819ce84edae793209445401fb29d81e794d52ba1f37e678`, and reference index **2** in the reviewed current effective reference order.
2. `staged-not-applied/alias.chat-postcoverage.20261025.shifted-operator.json`: a correctly **ID/filename-matched** `mode=alias` packet for `missing.bc0a34bcacc0fd814981` → `missing.99d02928227cf7d5004d`, the precisely same typed K-linear shifted endomorphism `A−λI_V:V→V`. Parent eigenvalue/eigenvector conditions are not aliased. No source or term identity is silently deleted.

Both proposals have been mathematically reviewed in `CHAT_POSTCOVERAGE_ADJUDICATION.md`. The first retires a known wrong existing edge but deliberately does not delete its historical provenance. The second is an exact typed candidate equivalence and does not identify whole source formulations.

## Checks possible without a local Git checkout (performed)

Using live GitHub objects and the immutable anchored `POSTCOVERAGE_RECONCILIATION.json`, checked **13 conditions**, all passing before the final minimal-delta adjustment: manifest format; current inventory and unresolved digests; exact formulation and effective-node hashes; reference index and occurrence ID; incorrect existing target; presence of separately valid real-time candidate occurrence; justified nonexisting-reference disposition; alias schema/ID shape, two distinct valid unresolved candidate IDs, and a substantive mathematical reason. After the minimal-delta adjustment, the intended updated fields are `state=external`, `disposition` and removal of `target_meaning_id`; the source/index/node anchors did not change. This is **static GitHub evidence checking**, not execution of `dependency_global_audit prepare`, `dependency_review_preflight`, tests, or a production graph validation. Any stale future hash requires re-review/re-anchoring, not forced acceptance.

## Required next preflight commands on a checkout of the PR branch

From repo root, with the current independent Wave2 workspace:

```bash
set -euo pipefail
W=research_pipeline/experiments/reconstruction-v2-independent
D=research_pipeline/reviews/canonical-identity-2026-10-24
STAGE="$D/staged-not-applied"

# Step A: revalidate frozen 421/421 coverage evidence and current graph fingerprints.
python "$D/validate.py"

# Step B: build full node-replacement amendment OFFLINE.
# This internally calls dependency_review_preflight on the generated package(s).
python -m research_pipeline.engine.dependency_global_audit \
  --workspace "$W" prepare \
  --manifest "$STAGE/filtration_prepare_manifest.json" \
  --output-dir /tmp/mathdef-wave2-stage1-filtration --max-per-batch 5

# Step C: preflight the independent exact-type alias WITHOUT submitting it.
# The filename stem equals the packet id as the preflight engine requires.
python -m research_pipeline.engine.dependency_review_preflight \
  --workspace "$W" \
  --batch "$STAGE/alias.chat-postcoverage.20261025.shifted-operator.json"
```

**Expected:** two offline, mathematically reviewed, mechanically checked transaction candidates. Their actual emitted amendment filenames, proposed full reference snapshots, derived occurrence metadata, and preflight results must be inspected and archived in this dated audit directory **before** anything goes to `$W/dependency_graph/inbox/`. The original source formulation and all unchanged effective references must appear unchanged in the generated replacement, except the one exact reviewed reference-state correction.

**If the preparer rejects the proposed `external` disposition or finds a shifted index/source hash:** DO NOT bypass validation or invent a new target. Read its exact error, inspect `make_snapshot` and the source/target in the current independent workspace, and revise only through another documented contextual adjudication. The right alternative, if external is semantically inappropriate under the scan classifier, is a well-justified deferred occurrence or correct typed missing candidate reuse—NOT a duplicate unreviewed missing identity nor a rewritten original mathematical source.

**If the alias preflight rejects an old event ID or new alias graph cycle:** stop and inspect current aliases, exact candidate contexts and receipts; do not resubmit a conflicting ID blindly.

## Gate and application policy

- There is **no staging here in the live inbox**. Creating these review-only JSON files on a draft PR does not apply them.
- Do not run an inbox action, merge PR #10, change the 421-review counts retroactively, open the consolidation gate, or begin Pass 3 on the strength of this preparatory work.
- After successful **offline** preflight and human/assistant inspection, a separate authorized controlled transaction can submit the two mode-separated packets using their correct filenames, record immutable receipts, verify hashes/rebuilt graph, rerun the 60 regression tests, all 19 mechanical readiness checks, the global scan and cycle/consistency checks, and reconcile the changed unresolved count against the preserved 421/421 **historical audit**.
- Next unresolved scope issue after stage 1: the Ext/internal-Hom coefficient assumption. Its options require explicit source-scope evidence or a new correctly typed general Hom prerequisite, not a blind graph rewrite.
- **No user decision is needed to finish these offline preflights.** If an application of the graph transactions or a source convention is contested, record the exact mathematical alternative for adjudication instead of guessing.

This file captures a reproducible handoff, without claiming that Codex usage or an external CI runner has performed the commands.
