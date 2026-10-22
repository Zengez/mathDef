# Wave 2 Pass 2 — second source-free consolidation chunk (2026-10-22)

## Verified result

The independent corpus remains **611 meanings / 659 formulations, 659 scan-complete, 659 structurally Open, zero Closed**, with no external source research, new meanings, population changes, publication or freeze. The source inventory SHA remains `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`. `STATE.json.summary.phase` remains `consolidate_occurrences`; **no consolidation gate** has been written.

| State | Before this chunk | After |
| --- | ---: | ---: |
| Unassigned references | 1,166 | **1,101** |
| Missing occurrences (incl. older) | 35 | **66** |
| Distinct missing candidate records | 15 | **21** |
| Ambiguous occurrences | 0 | **0** |
| Append-only amendment events | 38 | **83** |
| Existing meanings | 611 | **611** |

The 45 new version-pinned appendix amendments were committed as five immutable reviewed packages; all have `applied_in_independent_graph_only` receipts and their graph Actions passed, including run `39833427684`. The pipeline isolated tests also passed, including run `39833427792`.

## Reviewed classification clusters

1. `semantic-pass2-category-size-consolidation-001` (**12 source formulations**): 10 unrestricted-category references grouped as one missing ordinary category concept; 2 *finite* indexing categories linked to the existing `small category` meaning, preserving the additional finiteness assumption. Do not confuse arbitrary/base categories with a small category, functor or slice category.
2. `semantic-pass2-residue-fields-consolidation-001` (**10**): one typed residue-field-of-local-ring missing candidate covers R/m, R_p/pR_p, and scheme-stalk κ(s)=O_(S,s)/m_s. Compound descriptions such as *lifting roots* or *isomorphism of residue fields* remain ungrouped.
3. `semantic-pass2-field-algebras-consolidation-001` (**5**): plain commutative unital k-algebras over a field k grouped as one candidate; scalar-extension *constructions* remain separate.
4. `semantic-pass2-repeated-typed-prerequisites-001` (**6**): three shared missing concepts, with two occurrences each: indexed diagram functor F:I→C, multiplicatively closed ring subset, and countably generated R-module. Existing covariant-functor notion is scoped to small source *and target* categories and is not silently used for arbitrary target C.
5. `semantic-pass2-defining-axiom-clauses-001` (**12 formulations / 32 clauses**): explicitly reviewed module/scalar-action distributivities and unit axioms, linear-operator bound inequalities, contraction axioms, ring-map preservation conditions, and division-ring scalar-norm axioms. Those selected clauses are **internal defining predicates and data of the concept being defined** rather than separate prerequisite meanings, so they received explanatory `external` dispositions. Actual named prerequisite concepts not in the reviewed list were left unchanged, including the general group's identity and inverse element.

## Generic efficiency upgrade

Added:
- `research_pipeline/engine/dependency_context_worklist.py`
- `research_pipeline/tests/test_dependency_context_worklist.py`

Read-only usage:
```bash
python -m research_pipeline.engine.dependency_context_worklist \
  --workspace research_pipeline/experiments/reconstruction-v2-independent \
  --contains "residue field" --limit 20
```

The bundle joins original full source definitions and mathematical contexts with current live effective node hashes, all adjacent reference dispositions, existing target names, and a review-friendly reference template without generated occurrence IDs. It can filter surface groups by substring **for navigation only** and never asserts synonyms or edits the graph. The engine is subject-agnostic; mathDef-specific terminology review stays in the adapter/reviewer layer. New isolated regression tests verify hash accuracy and read-only behavior; `Research pipeline isolated tests` passed on commits `266be6e9b` and `d779f7fe7`.

The general execution contract `research_pipeline/DEPENDENCY_FIRST_WORKFLOW.md` now documents the helper and the key distinction between **independent prerequisite concepts** and **defining axioms/quantified conditions**. This reduces needless missing-candidate inflation while preserving explanatory content.

## Next

Resume from the *live* `STATE.json` and these notes, inspect unresolved-occurrence groups in complete mathematical context (not simple shared labels), reuse existing meanings where exact, and submit small append-only effective-node-hash amendments. Priorities: appropriately distinguish polynomial rings, module quotient/powers, category constructions (slice/comma), topological constructions and genuine missing notions. Do not bulk-convert all remaining unassigned strings to missing; test whether some are logically internal conditions. Continue to preserve the original 659 formulation texts and prevent false circular links.

**Pass 3 remains forbidden until the complete global Pass-2 review produces zero unassigned/ambiguous references and a valid explicitly reviewed consolidation gate.**
