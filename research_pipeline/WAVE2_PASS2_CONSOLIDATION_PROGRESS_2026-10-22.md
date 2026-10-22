# Wave 2 Pass 2 consolidation checkpoint — 2026-10-22

Pass 1 remains complete: 659/659 scans, 611 meanings. All 659 remain structurally Open and none certified. Current phase: `consolidate_occurrences`; no external research, added definitions or consolidation gate.

## Verified progress

| Metric | Before | After |
| --- | ---: | ---: |
| Unassigned occurrences | 1192 | 1166 |
| Missing occurrences | 17 | 35 |
| Missing candidate records | 13 | 15 |
| Append-only amendments | 13 | 38 |
| Ambiguous occurrences | 0 | 0 |

Five applied packages, all with successful graph checks:

- `semantic-pass2-eigen-operator-amend-001`: 3 formulations; existing linear-map links and eigenvalue self-link correction.
- `semantic-pass2-powerset-consolidation-001`: 5 formulations; one power-set candidate, `missing.dd36779bc0facafd958e`.
- `semantic-pass2-commutative-ring-unital-001`: 5 formulations; reuse historical commutative-unital ring candidate `missing.466fc74fa077cb173f05`, now 8 incoming formulations.
- `semantic-pass2-subgroup-and-module-scope-001`: 4 formulations; 3 subgroup links and a unitality-scope correction.
- `semantic-pass2-injective-map-consolidation-001`: 8 formulations; one injective-map candidate `missing.4ba0cfe171bbe93d0c9a`. Categorical coproduct arrows are excluded.

## Next steps

Review unresolved occurrences globally, starting with general/possibly-large categories, residue fields, k-algebras, and mathematical synonyms. Keep general categories distinct from the existing small-category definition; avoid identifying supremum with Dedekind completeness. Read the full source formulation and compare existing meaning targets before any classification.

For each correction, submit a version-anchored append-only full-reference `amend` package, using the latest *effective* snapshot digest from the amendment ledger. Verify receipt, graph Action and live `STATE.json`. Do not alter applied packages or open the research gate with unresolved occurrences. See `research_pipeline/DEPENDENCY_FIRST_WORKFLOW.md` and `research_pipeline/WAVE2_PASS2_INITIAL_TRIAGE_2026-10-22.md`.
