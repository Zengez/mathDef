# Future considerations and feature history

Recorded 2026-10-16. This file preserves the user's future website feature requirements and design decisions. **The recursive definition explorer was authorized and its initial implementation completed later on 2026-10-16.** See [DEPENDENCY_LINKING.md](DEPENDENCY_LINKING.md) for its current behavior and correction process. The first GitHub-authenticated community suggestion interface has since been implemented; account-free intake and the process retrospective remain deferred. Existing mathematical citations and definitions should not be modified solely to implement recursive links.

## Recursive definition exploration (first version implemented)

The following is the original design specification. The first iteration derives dependencies automatically from definition text during the site build and implements all three modes. Its In-Line expansion appears after the containing paragraph rather than between text words, and some ambiguous expressions are intentionally skipped for later review. For the implementation and override format, read [DEPENDENCY_LINKING.md](DEPENDENCY_LINKING.md).

Three compact settings near the term search bar: **Standard**, **Nested**, **In-Line**. Default **Nested**; retain the user's selection across navigation. No explanatory labels necessary.

**Standard:** display the chosen definition normally.

**Nested:** inside the selected definition's own container, show collapsed boxes for matching terms in the definition, below its text. Clicking the whole header, e.g., “Definition: Monoid”, expands its text and recursively shows its own collapsed dependency boxes. Collapse hides descendants. Multiple siblings can remain open. Prefer remembering descendant expansion state if a parent is collapsed/reopened.

**In-Line:** show a specific clickable cue by a recognized term, e.g., “(definition: monoid)”. Clicking inserts its definition on a **new line or lines, indented by approximately 2–3 character widths per recursive level**. It does not navigate away or replace the original definition. The inserted definition offers the same recursive expansion. Further nesting adds incremental indentation. Collapsing hides child definitions. Despite the mode's name, the expansion itself uses line breaks for readability.

**Detection:** match actual repo entries mentioned **in the formal definition text only** (not commentary, notes, related-terms metadata, or sources). Recognize mathematical expressions and LaTeX correctly. Prefer exact complete terms and explicit aliases, accounting for subject-specific ambiguities; avoid substring confusion such as “normal subgroup” versus “normal operator”. Related-term metadata can inform detection but must not be the sole source. The details of term matching and ambiguity handling can be designed later.

**Branch-local deduplication and cycle protection:** suppress a dependency if its term is already accessible at any level legitimately above the current expansion, including *collapsed sibling entries at an ancestor level*. Do NOT suppress terms simply because they appear in a separate branch. Example: A mentions B,C,D; B mentions C,E,F; C mentions E,F,G; D mentions A,B,G. Opening B, then C, then D yields A(B(E,F), C(E,F,G), D(G)). C is omitted under B since C is already an available child of A; A and B are omitted under D; E and F may appear independently under B and C because neither branch is an ancestor of the other. This is ancestor-level visibility exclusion, not a global already-expanded set.

Use a shared dependency/branch filtering engine in both recursive modes, differing only in presentation. Construct deeper children lazily. Maintain cycle protection and sensible performance; very deep indent is not a priority.

## Other deferred features

The user has additional features to describe; do not invent details. Term-matching/disambiguation may intersect with their next idea.

Read alongside `WORK_CHECKPOINT.md`. The user explicitly authorized the first implementation and automatic linking population after the original discussion; the separate community-feedback feature remains unimplemented.

## Community suggestions / review queue (initial GitHub Issues version implemented)

Provide an obvious website GUI action such as “Suggest an improvement” so visitors can propose mathematical corrections, report mistakes or bad term/dependency links, request missing definitions, or offer other suggestions. Exact placement and form design are deferred.

**Suggestions are proposals only.** No visitor submission directly edits definitions or other published mathematical content. Store submitted text in a persistent review queue accessible for discussion and auditing by the project maintainers and ChatGPT. A Markdown document or collection of plain-text/Markdown records in the GitHub repository is the desired long-term review artifact. Capture, where available: an identifier, relevant definition ID, category, submitted explanation, proposed replacement, timestamp, optional contributor information, and later review disposition/rationale.

**Contributor identity:** Prefer using a visitor's GitHub identity **with their permission** when available, because this can support future recognition and contribution tracking. Ideally also accept suggestions without a GitHub account, using an optional supplied name or anonymous submission. However, unauthenticated submission is a **nice-to-have, not a hard requirement**: if supporting it adds substantial infrastructure, security, spam-prevention, or maintenance complexity, a GitHub-authenticated initial version is acceptable. Investigate the actual costs and constraints before deciding. Do not silently infer or publish someone’s identity; ask for consent to associate it with their suggestion.

**Architecture:** GitHub Pages cannot itself receive and append arbitrary submissions to the repository. Explore GitHub Issues as a simpler authenticated intake path versus a small secured submission endpoint for account-free input. Whichever is chosen, preserve a durable reviewable queue and keep suggestions isolated from accepted edits. Review actions may mark accepted, revised, deferred, or rejected, with reasons.

User reports of wrongly linked/recognized mathematical terms should feed future refinements to automatic dependency detection; they do not automatically change linking rules.

**Status update (October 16, 2026):** The user authorized the first GitHub-Issues-based intake implementation. A public site form now requests new definitions and captures corrections on main and recursive definitions, including incorrect dependency pairs. The visitor must still sign in and submit the GitHub Issue; no automatic edits are performed. The optional public attribution name requires opt-in. Anonymous/account-free intake, moderation infrastructure beyond GitHub Issues, and future Markdown exports remain deferred. See [FEEDBACK_WORKFLOW.md](FEEDBACK_WORKFLOW.md).


## Post-audit process retrospective and reusable corpus-building workflow (deferred)

**When:** After completing mathDef's current citation/source-quality and cross-definition mathematical-consistency audits; do not launch this new workflow effort yet.

**Why:** The initial mathDef population, source attribution, audits, fixes, and checkpoint/resumption process evolved somewhat experimentally. The user wants to examine what worked, what failed, where repeated corrective passes could have been avoided, and how to make future related projects much faster, more systematic, more reliable, and reproducible **from the first population and attribution pass**.

**Future exemplar projects:** (1) a catalog of mathematical-education theory/model concepts and terminology, and (2) a catalog of mathematical theorems instead of definitions. They are examples of future applications, not authorization to start gathering their contents.

**Review goals:**
- Reconstruct the actual mathDef workflow and its recurring failure modes using repository history, scripts, checkpoints, validation results, and firsthand experience.
- Define a staged intake pipeline: scope/taxonomy and candidate acquisition; source discovery and precise citation attribution; content drafting/extraction and provenance; normalization and mathematical/domain-specific rigor checks; intra-corpus relationship resolution; duplicate/ambiguity checks; automated validation; bounded editorial review; release and maintenance.
- Distinguish reusable infrastructure (ingestion manifests, stable IDs, review-state tracking, source metadata, citation-validation checks, checkpointing, commit-sized batches, regression tests) from domain-specific requirements (definitions versus theorems versus math-education theories/models).
- Capture clear acceptance criteria and auditable progress metrics so an initial corpus is internally consistent and source-grounded before expansion, minimizing remedial rework.
- Consider how to record uncertainty, disagreements, and provenance without presenting machine-audited material as independently peer reviewed.
- Produce a durable playbook/checklist and, if useful, reusable scripts or project template **after discussing design**. Do not presume that the existing mathDef code or schema transfers unchanged to other corpora.

This retrospective and workflow redesign is a **future initiative**, not part of the current definition audit. Continue the current audit first; defer related new-project population and implementation.

## Public cross-project definitions export — implemented 2026-10-23

A read-only, content-hashed production definition snapshot and change manifest are generated by the ordinary Pages build. See [DEFINITION_EXPORT.md](DEFINITION_EXPORT.md). The feed is intended for mathThm and future consumers; it does not modify independent reconstruction data or current Wave 2 workflow.

**Remaining possible improvements:** independent Wave 2 or future promoted-corpus feeds; pushed update events rather than consumer polling; changed-term/delta manifests; a shared canonical term-matching API; and a mathDef-owned scanner/queue for terminology missing from external collections such as mathThm. Do not auto-create definitions from an external project without normal mathDef review.
