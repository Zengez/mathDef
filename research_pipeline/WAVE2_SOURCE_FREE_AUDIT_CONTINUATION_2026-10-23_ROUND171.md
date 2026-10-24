# Wave2 source-free audit — Round 171 (October 23, 2026)

## Disposition: contextual intersection target was an intentional common primitive

This round prioritized the previously flagged three-way intersection candidate `missing.fbe845b2e6ab78c9890f`. Instead of submitting a speculative graph amendment, the actual **effective occurrence index**, the immutable source-formulation texts, the two alias event rationales, the original immutable base snapshots, and the versioned Pass2 amendment packages were cross-checked.

The three mathematical parents are:

| Source formulation | Original effective reference phrase | Distinct mathematical family |
| --- | --- | --- |
| `form.wave2.cross107.topological-closure.1` | `intersection of all closed supersets of A` | Topologically closed supersets of `A` in `X` |
| `form.wave2.cross133.convex-hull-real.2` | `intersection of convex supersets` | Convex supersets of `U` in `V` |
| `form.wave2.pop140.affine-hull-intersection` | `intersection of all affine-closed supersets` | Subsets of `ℝ^d` stable under finite affine combinations containing `S` |

Two prior append-only aliases were explicitly justified as the **arbitrary indexed intersection operation**, **not** as identifying closure, convex hull and affine hull:
- `alias.global-audit.20261023.045`, `missing.babcda8464728aa791fe` → `missing.fbe845b2e6ab78c9890f`.
- `alias.global-audit.20261023.074`, `missing.d9c11dd3187956dd9ee3` → `missing.fbe845b2e6ab78c9890f`.

Thus the abstract identity merge is mathematically defensible: the *underlying set-theoretic intersection* is the same operation with different input families, and the original predicates survive in the parent texts and effective source references. **Do not break those identities or rewrite the source formulations simply because their results differ.**

**Actual remaining concern:** the canonical candidate's inherited query string “intersection of all closed supersets of A” is too narrow for a generic arbitrary-intersection prerequisite; its longer registered context already describes an arbitrary indexed intersection. A downstream missing-candidate viewer must not substitute that narrow canonical query for the precise convex/affine source expression. Example `A={0,1}⊆ℝ`: closure `{0,1}`, convex hull `[0,1]`, affine hull `ℝ`. This demonstrates why the **families** matter; it does not invalidate sharing the general intersection operation.

**Safe completed software remedy:** `candidate_review_bundle` now emits `matching_source_references` for each source formulation, including original source `phrase`, source `context`, observed pre-alias candidate ID, occurrence ID, and reference index, while still retaining `all_effective_references`. It handles canonical candidates' `alias_ids` without changing any graph identities or prior reasons. Regression test reproduces the topological-closure canonical label with an aliased convex-hull source phrase, checks exact observed identity and phrase, and verifies no mutation of the snapshot.

Future UI/presentation work may introduce a provenance-preserving **neutral display label** for this canonical candidate (“intersection of an indexed family of sets”), but must never overwrite its hashed ID/query/immutable aliases without a designed migration contract. The actual current graph is not mathematically wrong solely because a candidate's canonical query includes an unnecessary specialized phrase.

## Concrete audit defect repaired: groupoid-size heuristic regex escaping

The existing read-only global auditor checks whether a source explicitly says **small groupoid / small groupoids**, or refers to the category named `Groupoids`, before warning that a reference to the only existing *small-groupoid* definition might impose unintended size restrictions.

The two original raw regex patterns were accidentally double-escaped:
- `r"\\b(small|finite)\\s+groupoids?\\b"`
- `r"\\bGroupoids\\b"`

They were corrected to the proper word-boundary regexes:
- `r"\b(small|finite)\s+groupoids?\b"`
- `r"\bGroupoids\b"`

The first is matched on case-normalized source content; the second recognizes the exact named `Groupoids` category without treating an embedded token such as `preGroupoids` as the actual category. A new regression test verifies that **unqualified groupoid** triggers a heuristic review lead, while **small groupoid** and explicitly typed **Groupoids** do not. This is a detector-only correction: the three previously noted effective groupoid-size links remain untouched and require human mathematical context assessment. Passing the detector does not mathematically certify a source.

Changes:
- `a17ff8c4af1d954e1bd218e0f7dd916948882b27` — groupoid detector fix.
- `c4bf6cfbf18ae0c3fd4acd34b8e5dbb396406288` — groupoid detector regression.
- `e122446cd484fff4bb80289a85ece9aedaccd809` — contextual observed-phrase focus output.
- `3ef1f63783eee068ea43143db5f5ac466ae9b952` — contextual phrase regression.

## Live graph and phase guardrails

**No new aliases, resolutions, new meanings, graph amendments, scan rewrites, source edits, candidate deletions or gate changes** were submitted in Round 171. Authoritative live counts (unchanged from verified packet 170): **611 meanings; 659/659 scans; 724 raw missing IDs; 294 applied aliases; 7 existing-target resolutions; 423 unresolved canonical identities; 819 missing occurrences; 765 amendment events; zero ambiguous/unassigned; 651 open/8 closed; gate FALSE**.

Current inventory hash `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`. Canonical unresolved fingerprint remains `aeb62c80b7cf0f95c9d944309bc4888acd97daa2c58e148bf2ffdb13b06642a7`.

Avoid external research, breadth Batch143, human/source certification, promotion, frozen Wave1 or production corpus edits and opening/fixing the consolidation gate.

### Next focus

1. Verify the latest isolated CI tests for the source-phrase enhancement; differentiate code-test success from mathematical certification.
2. Reevaluate groupoid-size warnings with correctly functioning explicit-size word boundaries, using the **effective** amended references.
3. Continue investigating source-scoped quasi-finite / local-fibre-dimension, submersive surjectivity and non-Noetherian constructibility terminology. Prefer full mathematical context and counterexamples over candidate-count reduction.
4. For remaining shared canonical candidates, read `matching_source_references` before declaring their differing specialized phrases equivalent as full constructions; only underlying reusable primitives may be merged when rigorously supported.
