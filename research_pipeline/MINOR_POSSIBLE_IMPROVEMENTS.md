# Minor possible improvements — deferred ideas

**Purpose:** During the first dependency-first Wave 2 experiment, record possible
workflow optimizations that do **not** appear likely to make enough difference
to justify changing the pipeline mid-pass. Reconsider as a group near the end
of Pass 2 / during the post-pass consistency audit. This is a backlog, **not**
an authorization to alter the independence boundary, mathematical review,
source corpus, or applied graph data.

## 2026-10-22 — Pass 2 contextual consolidation

| Idea | Potential benefit | Why deferred / safety constraints |
| --- | --- | --- |
| Persist a short-lived inventory/occurrence view for the current topical review cluster rather than rereading every registry in each connector invocation | Fewer repetitive repository reads and less local orchestration code | The existing multi-filter read-only context helper and small-batch workflow already address the largest cost. Any cache must be tied to an exact inventory/version/fingerprint, automatically invalidated after graph amendments, and never be treated as authoritative over live GitHub data. |
| Show reviewed candidate aliases next to each new raw missing-candidate record in a one-page read-only worklist | Less manual navigation between the missing registry and aliases when building a consolidation packet | Existing two-step amendment then contextual alias procedure is rigorous and functioning. Display-only convenience probably has modest impact compared with reviewing full mathematical source text. A lexical similarity result is **never** sufficient to assert mathematical identity. |
| Package small reusable local checksum/serialization diagnostics for reviewers operating through a remote connector | Reduce repeated implementation of canonical JSON SHA checks in connector scripts | The existing `dependency_review_preflight.py` validates mechanically when a local workspace is available, and the graph CI validates applied packets. A connector-side helper may save only marginal effort unless we see repeated digest errors; any helper must be tested against authoritative `digest` and read-only. |

### Revisit criteria

Group these with later minor ideas when the remaining occurrence backlog is
much smaller. Promote an idea into an implementation task only if the estimated
time saved across future research projects or the reduction in actual
correctness risk is substantial. Do not optimize by automatically conflating
distinct concepts, removing provenance, or relaxing the review-first gate.
