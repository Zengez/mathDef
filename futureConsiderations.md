# Future considerations (deferred)

Recorded 2026-10-16. This file preserves agreed website feature requirements for later chats. **Do not implement yet.** Current priority: source-citation audit and cross-definition mathematical consistency. Defer systematic rendering verification and unrelated term discovery. Only add a missing definition when its term is found inside an existing definition.

## Recursive definition exploration

Three compact settings near the term search bar: **Standard**, **Nested**, **In-Line**. Default **Nested**; retain the user's selection across navigation. No explanatory labels necessary.

**Standard:** display the chosen definition normally.

**Nested:** inside the selected definition's own container, show collapsed boxes for matching terms in the definition, below its text. Clicking the whole header, e.g., “Definition: Monoid”, expands its text and recursively shows its own collapsed dependency boxes. Collapse hides descendants. Multiple siblings can remain open. Prefer remembering descendant expansion state if a parent is collapsed/reopened.

**In-Line:** show a specific clickable cue by a recognized term, e.g., “(definition: monoid)”. Clicking inserts its definition on a **new line or lines, indented by approximately 2–3 character widths per recursive level**. It does not navigate away or replace the original definition. The inserted definition offers the same recursive expansion. Further nesting adds incremental indentation. Collapsing hides child definitions. Despite the mode's name, the expansion itself uses line breaks for readability.

**Detection:** match actual repo entries mentioned **in the formal definition text only** (not commentary, notes, related-terms metadata, or sources). Recognize mathematical expressions and LaTeX correctly. Prefer exact complete terms and explicit aliases, accounting for subject-specific ambiguities; avoid substring confusion such as “normal subgroup” versus “normal operator”. Related-term metadata can inform detection but must not be the sole source. The details of term matching and ambiguity handling can be designed later.

**Branch-local deduplication and cycle protection:** suppress a dependency if its term is already accessible at any level legitimately above the current expansion, including *collapsed sibling entries at an ancestor level*. Do NOT suppress terms simply because they appear in a separate branch. Example: A mentions B,C,D; B mentions C,E,F; C mentions E,F,G; D mentions A,B,G. Opening B, then C, then D yields A(B(E,F), C(E,F,G), D(G)). C is omitted under B since C is already an available child of A; A and B are omitted under D; E and F may appear independently under B and C because neither branch is an ancestor of the other. This is ancestor-level visibility exclusion, not a global already-expanded set.

Use a shared dependency/branch filtering engine in both recursive modes, differing only in presentation. Construct deeper children lazily. Maintain cycle protection and sensible performance; very deep indent is not a priority.

## Other deferred features

The user has additional features to describe; do not invent details. Term-matching/disambiguation may intersect with their next idea.

Read alongside `WORK_CHECKPOINT.md`. Feature design discussion is **not** authorization to start coding.