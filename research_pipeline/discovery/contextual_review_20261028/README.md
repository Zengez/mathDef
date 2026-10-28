# mathDef contextual candidate review — 2026-10-28

This is a **source-referenced research worklist**, not a new published
definition corpus. It continues the prior Pass 3 review, in which 9,071
phrases required deeper mathematical/contextual judgment.

**Exact input:** the cleaned corpus at v2 SHA-256
`0441b9c5fc2f7a515c3210a7471a3a3e8f9ca0b8dc63f570dcc8e1cb38a08fe2`.
Review records are stored as the 20 versioned TSV partitions in `batches/`.
Their row counts and byte-level SHA-256 checksums are in `manifest.json`.
Run `python -m scripts.validate_contextual_review` to verify completeness.

## Review outcomes for all 9,071 candidates

| Disposition | Count | Treatment |
| --- | ---: | --- |
| `clear_false_positive` | 109 | Clear grammatical non-terms; reversible exclusion |
| `contextual_fragment` | 27 | Phrase truncated in the original definition; reversible exclusion |
| `contextual_description` | 1,011 | Mathematical prose/composition, not established as a separate named term; retain audit trail |
| `existing_variant` | 6 | Apparent existing heading/alias/inflection; check any contextual distinction before merging |
| `legitimate_lead` | 678 | Mathematical concept plausibly worth definition research, not yet verified absent |
| `deeper_research` | 7,240 | Ambiguous; preserve and escalate to mathematical/citation review |

The 1,011 contextual descriptions should **not** be counted as disproven
mathematical terminology. For example, a phrase such as “closure of the
convex hull” can be mathematically meaningful without representing a
separate term whose definition is missing. Similarly, the 678 legitimate
leads are *candidates*, not verified definitions.

## Method

- Reused **exactly 9,071** unresolved phrases from the preceding Pass 3
  checkpoint, rather than reextracting previously scanned formulations.
- Compared against the current published v2 headings and aliases, with
  conservative spelling/plural matching.
- Inspected source formulation headings and adjacent token windows from the
  durable `discovery-checkpoints` scan cache.
- Identified candidate strings that end partway through an existing named
  notion (e.g. “real vector” before “space”), and clear sentence fragments.
- Applied mathematical-terminology recognition to technical noun phrases;
  ambiguous mathematical descriptions were *not* rejected.
- Performed targeted contextual adjudications of higher-frequency and
  demonstrably ambiguous cases.
- Consulted established reference sources for selected cases:
  [Encyclopedia of Mathematics: Germ](https://encyclopediaofmath.org/wiki/Germ),
  [Abscissa of convergence](https://encyclopediaofmath.org/wiki/Abscissa_of_convergence),
  [Local homology](https://encyclopediaofmath.org/wiki/Local_homology),
  [Analytic number theory](https://encyclopediaofmath.org/wiki/Analytic_number_theory),
  [MathWorld: Bergman space](https://mathworld.wolfram.com/BergmanSpace.html),
  and [Identity map](https://mathworld.wolfram.com/IdentityMap.html).

This was a **moderate automated/contextual mathematical screening**, not
9,071 independently source-verified mathematical adjudications.
External sources corroborate selected named notions, not the entire
classification set. The category `deeper_research` remains unresolved.

## Next pass and recovery

The durable source references, reason codes, and distinctions are recorded
in each TSV. Resume mathematical validation from rows with
`review_class=deeper_research`, then investigate
`review_class=legitimate_lead` for proper conventions, duplicate contexts,
citations, and precise formulations. Preserve prior classifications and
source attribution, including all reversible false-positive exclusions.

The compact `matrix.json` is an independent 16,043-candidate accounting
checksum recording prior and current classification categories. It is
not a replacement for human-readable detailed decisions.

No production definition source, published link, or external API snapshot
is changed by this review.
