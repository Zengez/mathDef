# Extended Wave2 dependency audit, 2026-10-23 — packets 147–150

**Status:** twenty mathematically source-context-reviewed identity packets staged for independent graph workflow; receipts and both CI statuses must be verified before counting.

## Scope

Verified baseline: 611 meanings, 659/659 formulations scanned, 724 raw candidate IDs, **197 existing aliases / 527 unresolved canonical identities**, 826 missing occurrences, zero ambiguous/unassigned, 765 append-only amendment events, gate FALSE. Original source-formulation inventory SHA `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`.

Reviewed 20 contextual candidate aliases against both full inventoried source formulations, preserving parent-level restrictions while identifying genuinely shared mathematical **prerequisites**. Grouped into four independent-only alias packets 147–150 (five decisions each). Expected totals only if workflow accepts all: 217 cumulative alias identities and 507 unresolved canonical identities. No mathematical meanings, source files or dependency nodes were rewritten.

### Verified distinctions

- **Generic structure and specialized instance:** idempotent predicate versus idempotent-generated ideal or Boolean ring; ring quotient versus square-zero algebra quotient/lifting; finite free R-module versus its localization at R_f; topological pullback versus self-fibre-product and diagonal closedness.
- **Finite sums and products:** Rees and tensor algebras have extra graded multiplication on a finite-support module direct sum. Their full algebra structures are *not* equated.
- **Topological types:** a clopen subset differs from closed map, closed immersion, or closed point; a general neighborhood is not necessarily open.
- **Probability:** integrability E|X_t|<∞ is shared across discrete and continuous indices; martingale equalities and filtration ranges are not.
- **Commutative algebra:** a monic polynomial is not automatically integral over an ideal, and the condition on its coefficients must be retained.
- **Polynomial construction:** univariate polynomial rings and expressions specialize the indexed polynomial algebra; nonzero/evaluation/injectivity do not follow solely from polynomial-algebra existence.
- **Source error flags retained:** (1) quasi-finite-at-prime local fibre dimension-zero versus isolated point; (2) submersive-map open-preimage condition without surjectivity. Neither is touched in this dependency-only phase.

## Audit completion protocol

Check exact receipts `semantic-global-audit-missing-alias-147.json` through `150.json` in `dependency_graph/applied/`; require `status=applied_in_independent_graph_only` and `human_certified=false`, plus green graph and isolated test workflows. Inspect live STATE, CHECKPOINT, version fingerprint and source inventory afterward. This stage does not enable missing-definition research, human certification, original corpus comparison, Wave1 edits, source correction, breadth expansion, or consolidation-gate sealing.
