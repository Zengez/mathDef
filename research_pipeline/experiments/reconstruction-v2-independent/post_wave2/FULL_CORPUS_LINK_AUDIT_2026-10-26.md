# Complete merged mathDef cross-chunk link audit — 2026-10-26

## Audit scope

**Completed against the entire published merged collection, not sample batches.**
The audit checks every existing group, mathematical meaning, formulation,
reference relationship, and displayed dependency, together with a *separate*
read-only scan for mentions of **existing term labels and aliases** that have
no exact positioned link. **It does not find or collect new terminology
candidates, research definitions, or create new lexical links.**

This review was performed on the current root website's catalog (which is
identical to the already-tested `/reconstruction/merged/` catalog). The complete
graph has:

| Unit | Total |
|---|---:|
| Searchable headings | **2,048** |
| Contextual meanings | **2,197** |
| Definition formulations | **2,246** |
| All relationship records | **6,825** |
| `definition_uses` relationships | **4,522** |
| Other relationships (`related`, implication, characterization) | **2,303** |
| Positioned definition-use links | **3,200** |
| Unpositioned screened definition-use links | **1,322** |

The **1,322 unpositioned** relationships are existing screened, semantic/
editorial references whose source text may not contain the target's literal
term. The site intentionally displays them as additional expansion controls
below the appropriate formulation. They are not necessarily missing links,
broken endpoints, or newly collected candidates.

## Full-graph structural verification

Across **all** 6,825 records and all 2,246 formulations, the required
integrity checks found **zero** instances of:

- Dangling or nonexistent source/target definition identifiers.
- Duplicate relation IDs or duplicate links from the same formulation to the
  same target meaning.
- Invalid source positions, source phrase mismatches, or overlapping
  positioned ranges.
- Source positions hidden inside mathematics instead of visible prose.
- Differences between catalog relations and the dependencies that visitors
  actually receive in the rendered search index.
- Missing definition formulations or mismatched rendered targets.
- Broken references among a rendered group's related terms.

The scan crossed original, reconstructed Wave 2, and post-Wave2 cohorts.
Examples of fully validated cross-cohort relationship counts include **912**
links from independent/postwave source meanings to original mathDef meanings,
**307** original-to-Wave2 relationships, and **133** original-to-postwave
relationships. The original-to-original set has **3,114** relationships;
additional cross-cohort links complete the **6,825** graph. These are
directed relationship counts, not distinct terms.

## Existing terminology coverage: only six intentional abstentions

The independent occurrence scan matched **3,484** existing-heading mentions
against the full 2,246-formulation corpus. Of these, **3,199** are exact
positioned links, and many of the remaining matches are repeated mentions of
a target already linked at its first occurrence. Detailed follow-up classified
the only first-target coverage exceptions as:

- **3** `natural numbers`: the source does not determine whether 0 belongs.
- **2** `inner product space`: no real/complex field is specified.
- **1** `ring homomorphism`: the source explicitly contrasts unital and
  non-unital conventions.

Additionally, **2** `open ball` word matches were correctly suppressed
inside definitions of *forward/backward directional quasi-metric balls*:
making those link to the ordinary symmetric metric ball would be incorrect.
**2** occurrences of `weak topology` in a CW complex are correctly
associated with the existing CW-specific topology meaning rather than a
different subject's homonymous weak topology.

**There are no newly discovered unexplained missing links to existing terms
under this lexical-coverage test.** This does not certify that every possible
mathematical dependency is lexically detectable, nor that every provisional
link is mathematically correct; the site's **Suggested** labeling and feedback
mechanism remain essential.

## 11 same-heading relationships — not broken references

When independently researched meanings and original mathDef were grouped
under the same public heading, **five existing related-category edges** and
**six existing definition-use edges** became internal to one search result.
Examples include separately authored contextual `open set`, `Borel measure`,
and `purely inseparable extension` meanings.

The underlying curated relations remain retained for provenance. The
renderer already suppresses same-heading related suggestions, while the
interactive recursive explorer excludes the current heading from its own
ancestor path. All intended meanings and formulations are visible together
under the shared heading; hence these internal references are redundant
for navigation, **not dangling, duplicated or silently lost definitions**.
Do not delete frozen research relationships simply to make this number zero.

## Repeatable safeguard added

The new `research_pipeline/adapters/mathdef/audit_merged_links.py`
operates on the complete catalog and displayed index. It now runs:

1. During the combined merged-preview CI, with the exhaustive
   browser interaction checks.
2. During the **actual main website publication**, before deployment.
   The site publishes the current machine-readable findings as
   `/audits/full-link-graph.json`.

Four additional regressions explicitly exercise a valid complete graph,
existing-term omission reporting, nonexistent endpoints, and corrupt
positioned text. The full test suite now executes **23 Python tests**, plus
independent searches and recursive-expansion Chromium checks.

**Disposition:** Whole-corpus cross-chunk link integrity verified. No
required additional linking review phase or terminology discovery is needed.
Leave the six convention-dependent cases as deliberate abstentions for
the visitor suggestion process.

**Important limitation:** This is an exhaustive computational and
cross-context-structural link audit, not a human theorem-by-theorem proof
that each of ~3,000 provisional lexical link targets is mathematically
semantically correct. Provisional links remain visibly labeled Suggested.
