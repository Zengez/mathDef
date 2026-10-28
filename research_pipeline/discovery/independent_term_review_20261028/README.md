# Pass 5 — independent mathematical terminology screening (28 October 2026)

**All 7,240 unresolved leads from the prior contextual review have received a new, reversible disposition.** The active pool for *this tranche* is now **3,109**, comprising 934 plausible mathematical-term leads and 2,175 targeted-review cases. Another 4,131 have been excluded from *independent-term research* for the reasons below. **This is not a removal from the historical high-recall discovery registry or from mathematical source material.**

| Disposition | Number | Meaning |
| --- | ---: | --- |
| `candidate_lead` | **934** | Plausible independent mathematical terminology; needs mathematical/source verification |
| `needs_targeted_review` | **2,175** | Potentially technical terminology; do not reject without human mathematical assessment |
| `remove_description` | 2,166 | Mathematical or ordinary descriptive phrase, not established as an independently named concept in available evidence |
| `remove_false_positive` | 1,719 | Grammatical fragment, sentence boundary, or mathematics-removal artifact |
| `remove_fragment` | 245 | Truncated prefix of a larger mathematical expression |
| `existing_definition` | 1 | Already covered by a published definition/synonym (clopen/open-and-closed) |
| **Total** | **7,240** | All recorded, no missing or duplicate IDs |

The **4,131 suppressed leads are never permanently deleted**. A description of a mathematical object may be valid and even deserve its own definition once researched. `remove_description` means *not independently established as a new term*, **not** mathematically false. `candidate_lead` is also provisional and is not a verified missing definition.

## Why this pass is more decisive than earlier passes

1. Reads source formulation text and measures whether the candidate was artificially assembled across punctuation or removed LaTeX mathematics. Such artifacts were a major origin of false positives.
2. Compares all terms/aliases in the exact published 2,104-formulation v2 snapshot, including lightweight singular inflections. The historical candidate IDs and original sources remain unchanged.
3. Distinguishes grammatical fragments, incomplete term prefixes, ordinary descriptive qualifiers, and terms that could reasonably have independent definitions.
4. Preserves unfamiliar mathematical noun phrases for targeted review instead of treating unfamiliarity as evidence of falsehood. Auditing found that over-aggressive rules wrongly suppressed **Koszul formula**, **Hamel basis**, **specialization preorder**, **extension of scalars**, and other genuine concepts; safety exceptions now protect them.
5. Includes selected context-based/definitional-subject evidence as an **indicator**, not proof of mathematical independence; even strong-looking leads still require verification.

## Reproducibility and recovery

`batches/*.tsv` contains every decision, rationale, prior source IDs, source-text excerpts, and boundary evidence. `survivor_batches/*.tsv` contains only the 3,109 retained leads for efficient continuation. `manifest.json` records original feed SHA-256, exact counts, source review, and per-file SHA-256 digests. Verify every byte, candidate ID, and queue count with:

```
python -m scripts.validate_independent_term_review
```

To reproduce the classification from the **same historical feed and checkpoint**, assemble the canonical site and use the durable `discovery-checkpoints` branch from the original scan:

```
python -m scripts.mathdef_independent_term_filter \
  --snapshot _site/api/definitions/v2/snapshot.json \
  --checkpoint _discovery/checkpoint.next.json \
  --source-review-dir research_pipeline/discovery/contextual_review_20261028 \
  --output /tmp/mathdef-pass5-replay
```

The scanner intentionally asserts the original feed hash so a later changed corpus does not silently alter these historical decisions. For genuinely newly published terms or source changes, make a **new dated review** instead of rewriting this audit.

No definitions, original source discoveries, mathDef public Pages contents, or mathThm feed were modified in this process. Prior user-approved definition overrides continue to take precedence over heuristic review labels.