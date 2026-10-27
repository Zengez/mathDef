# TEMPORARY EXECUTION PLAN — mathDef definition deduplication, Subjects/Contexts, and source registry

**Planning checkpoint:** October 27, 2026. **Status: approved approach, NOT started.**
**Delete/archive this temporary plan when the cleanup is complete and the lasting implementation documentation has been updated.**

## 0. Authoritative scope, baseline, and non-goals

- The canonical public mathDef library is the merged collection at https://zengez.github.io/mathDef/; its cross-project feed is the merged v2 snapshot. Baseline before this cleanup: **2,048 term headings, 2,197 meanings, 2,246 formulations**, and 6,825 links/relations. Baseline figures are checkpoints, not quotas or permanent invariants.
- The purpose of the next pass is to **remove linguistically redundant mathematical definitions while preserving mathematical ideas, justified variants, and source URLs**. The earlier requirement to preserve literally every old mathDef formulation is superseded.
- **Start by comparing original mathDef versus newly researched formulations** wherever their terms have been grouped, then examine duplicates across all remaining source cohorts, variants, and batches.
- **NO NEW terminology candidate discovery, broad reference crawling, or additions of unrelated mathematical concepts.** References may be consulted as needed for comparison or correctness, but do not create a new term candidate queue.
- **Do NOT begin the cleanup in the conversation that created this plan.** The user requested only this durable plan and a handoff prompt for a new chat.
- **Do NOT rebuild the complete linking graph, perform the final link audit, or publish the deduplicated corpus until the user has had the offered chance to resolve uncertain cases.** Interim narrow checks and reports are allowed.
- **Defer user-facing UI redesign.** In particular, establish Subject/Context data first; later the user will discuss how these appear on the website, including the proposed 'Sources' link.

## 1. What counts as duplicate versus variant

Think in **mathematical language**, not English surface-string similarity.

1. **Clear duplicate — consolidate:** two formulations express substantively the same defining mathematical predicate on the same class of objects, with the same assumptions/conventions and no genuinely distinct presentation or construction. Notation, variable names, sentence structure, and trivial ordering do not justify separate displayed definitions. Keep a single excellent formulation and preserve every independently useful source reference.
2. **Clear variant — retain:** a formulation uses different defining mathematical objects, equivalent-but-informative characterizations, constructions, prerequisite frameworks, subject branches, assumptions, conventions, scope, or genuinely pedagogically useful mathematical perspectives. Logical equivalence *alone* does not imply deletion.
3. **Uncertain — do NOT silently merge:** if it is unclear whether two formulations are mathematically redundant versus pedagogically/mathematically distinct, put them on the temporary decision list and leave both active pending the user's decision.
4. **Non-equivalent meanings sharing one term — retain distinctly:** do not collapse context-dependent definitions (e.g., commutative versus unrestricted rings, unital versus nonunital conventions, real versus complex cases). If one assumption changes the class of objects, do not treat that as mere wording.
5. **Example (Artinian ring):** the screenshot shows two nearly identical *commutative* descending-chain-of-ideals formulations. Consolidate these (likely prefer the externally precise Stacks-supported formulation) but preserve independent references. Do NOT inadvertently discard a broader, possibly noncommutative Artinian-ring meaning if it exists.

Prefer better precision/rigor and credible primary references, not the source cohort ('Original mathDef' versus 'Wave 2'). Source choice and retained URLs must be recorded with the decision. Do not mistake an editorial GitHub source-file URL for an independent mathematical authority.

## 2. Source registry: collect now, UI display later

- Implement a **term/group-level source registry**, associating each mathematical heading with all distinct URLs/locators where a definition for a meaning of that term was actually encountered. Prefer additionally associating each source with the precise meaning/context it supports, so a source for a specialized meaning is not silently described as endorsing every variant under the heading.
- Preserve references from duplicate formulations even after consolidating their text. Accumulate source title, URL, optional section/tag/locator, supported meaning/formulation IDs, role (actual definition evidence / cross-reference / supplemental source), evidence verification state where available, and **which source was selected as primary for each surviving meaning/formulation**. If multiple formulations differ, their primary sources may differ.
- Keep URL deduplication conservative: normalize trivial redirects/tracking differences where demonstrably equivalent, but do NOT destroy meaningful section fragments, Stacks tags, source locators, separate versions, or sources supporting different assumptions.
- The future user-facing behavior should be a compact **'Sources' link/action for the term**, opening its collected source list. Do not dump every reference inline inside each definition. Exactly how the link/list renders is **deferred** until the planned interface conversation.
- Do **not** build original-mathDef cohort metadata into the new user-facing identity or public source list. The old corpus and Git history suffice for historical comparisons. A retained external citation is relevant; 'original mathDef' as a historical source cohort is not itself mathematical evidence.
- Preserve and report whatever legitimate collected source URLs are currently available. Do not claim comprehensive web-source coverage of a term if the underlying collection is not exhaustive.

### Future source-reliability metric — RECORD DESIGN ONLY; DO NOT IMPLEMENT NOW

- Later, correction submissions could be associated with a **canonical source URL / source ID** and with the definition/meaning that cited that source, in an **internal-only correction-event ledger** distinct from the user-visible Sources list. Capture enough stable identifiers now so this is straightforward later.
- Source reliability should ultimately be judged using a **normalized rate**, such as reviewed/substantiated corrections per eligible source-attributed definition or exposure, not raw correction counts. Compare '500 Stacks corrections versus 5 Wikipedia corrections' only alongside denominator, type/severity, legitimacy, repeat submissions, and opportunity for feedback. Do not automatically label a source unreliable based on unverified reports.
- **No correction counts, source scoring, reputation ranking, or automatic primary-source reselection are required in this pass.** Do not falsely initialize historical correction counts to zero where reporting was never tracked; represent historical absence as unknown/untracked.

## 3. Subject and optional Context: structured metadata, no provenance labels

- Every **surviving mathematical meaning/formulation** must have a **required primary `subject`** identifying its mathematical branch (e.g., Algebra, Commutative Algebra, Topology, Analysis, Category Theory); use specific accurate labels where useful.
- Add an optional `context` for salient mathematical conventions, object classes, grounding frameworks, or finer restrictions (e.g., Unital associative rings, Real inner-product spaces, Functional analysis). A context must not be automatically invented when none is justified.
- Subject and Context have different purposes. 'Original mathDef', 'Wave 2', 'post-wave', 'research', draft status, and citation type are **not** mathematical subjects or contexts; put provenance/review status in separate internal metadata if needed.
- Create **two separate, human-readable internal registry files** (suggested locations: `data/math_subjects.json` and `data/math_contexts.json`; filenames may be improved during implementation), listing all approved/encountered values, including relevant planned values even if their present usage count is zero.
- Optional but useful if cheap in this pass: generate **assignment counts** for each subject/context in these registries, with an explicit denominator/granularity (prefer count of surviving meanings, perhaps counts of formulations as secondary). Ensure counts are recalculated from the canonical data, not maintained by hand. If counts complicate work, defer them.
- Normalize abbreviations and inconsistent spelling/levels (`Commalg` → `Commutative Algebra`, etc.); enforce registry consistency, and record aliases if useful rather than proliferating near-synonyms. Avoid mechanically guessing math subject from a repository directory when term context contradicts it.
- **Do the underlying metadata in this pass**, including for single-definition entries, but postpone changing how Subject and Context are visually displayed. The user will return to the interface afterward.

## 4. Practical work sequence and durable checkpoints

**Phase A — Inventory and audit setup (no corpus mutations initially).**
- Read this temporary plan, `AGENTS.md`, and the current merged-corpus publisher, renderer, reference export, and global link audit. Inventory existing meanings/formulations, titles, citations, source cohorts, and current subject/context labels.
- Produce baseline counts and a checkpoint with exact pending work. Build a deterministic comparison plan that starts with **original-versus-new grouped definitions**; optionally use normalized mathematical text/token similarity to prioritize promising duplicate pairs, but **never use similarity alone to discard an entry**.
- Choose internal source registry and subject/context schema that survive publication rebuilds and will feed the later public Sources action. Prefer a maintainable canonical layer/overlay rather than editing frozen historical research inputs or relying on ad-hoc UI filters.

**Phase B — First targeted pass: original versus new.**
- Inspect every grouped term with original and newer meanings/formulations. Consolidate obvious duplicate mathematical statements and collect their source URLs into the term/meaning source registry. Keep obvious variants, including differing mathematical objects and genuine alternative characterizations.
- Normalize required Subject and optional Context fields for each reviewed surviving definition. Maintain committed running progress/counters so interruption or chat timeout does not restart the work.

**Phase C — Whole-corpus pass.**
- Compare remaining formulations across *all* cohorts, including duplicates among independent Wave 2, post-Wave 2, and previous alternatives. Recheck that a clear duplicate was not missed simply because of source provenance or title normalization.
- Never remove a term/concept just because a formulation was redundant. Preserve searchable headings/aliases, meaning distinctions, actual references, and necessary relational information. No target-count quotas.

**Phase D — Ambiguity queue for the USER: stop before global link rebuild.**
- Collect a **bounded, finite list of genuinely uncertain consolidation choices** in a persistent temporary review file (suggested `post_wave2/TEMP_DEDUP_DECISIONS.md` or JSON+Markdown), with status and exact source/formulation identifiers.
- For **each term requiring a decision**, present **ALL formulations currently shown for that term**, not merely the uncertain pair, verbatim as mathematical statements with enough context and source info. Use:
  - `Definition of [term]`
  - `Def A: [full definition]`, `Def B: [full definition]`, `Def C: [full definition]` ...
  - `Decision needed: [explicit subset, e.g. whether A and B should be combined]`
  - `Clearly retained: [others, if any]`
  - `Preliminary recommendation and precise mathematical reason for uncertainty`.
- Mark clear decisions completed; avoid flooding the user with obvious duplicates or noncontroversial variants. **Then offer the user the chance to adjudicate** all unresolved cases. Do not infer consent from silence and do not repeatedly reopen already resolved cases.

**Phase E — Resolve user's decisions; one final structural/link/export pass.**
- Apply the user's decisions. Update all source-registry cross-references and chosen primary source identifications consistently; ensure every surviving definition has a valid subject and optional registry-approved context.
- **Adjust old publication invariants** that currently insist on preserving every one of 1,014 original formulations and exact original IDs. Replace them with correctness invariants: every intended mathematical term/meaning survives, retained forms have appropriate citations, explicit consolidated-ID mappings exist where essential for link correctness, and no dangling relation or feed target remains. The older v1 feed can remain historical if convenient but is not an authoritative constraint.
- Once duplicate/uncertain decisions are final, do the requested **ONE full combined linking rebuild and exhaustive cross-chunk audit**, repairing dangling/misdirected anchors and cross-meaning relations caused by consolidation. Revalidate recursive linking, feedback actions, search and rendering.
- Rebuild the canonical **v2 cross-project feed** from the cleaned published corpus, including sources and subject/context metadata; update its schema/doc contract carefully where needed (if incompatible, explicitly version), preserve a content-addressed update signal, and run full tests before publishing.
- Report before/after group/meaning/formulation/relation counts; duplicate removals; retained variants; all references preserved; registry coverage; anomalies fixed; and any genuinely unresolved limitations.
- Publish only after correctness checks and the user-review checkpoint are satisfied. No second linking rebuild if ordinary stage-local verification will suffice.

## 5. Guidance and constraints for future continuation chats

- This plan records *decisions*, not instructions to start a new candidate-collection wave. There are **no pending terminology candidates** from the earlier 2,019-item quick scan.
- Do not revive obsolete Wave 2 dependency-graph gates, retrospective candidate investigations, or requirements to preserve every original formulation verbatim in the new public collection.
- Do not conflate mathematical equivalence of meanings with near-identical natural-language wording; inspect assumptions and mathematical objects before deduplicating.
- Preserve actual source URLs and primary-source choices; user-facing 'Sources' view and internal correction-by-source analytics are **future UI/features**, not mandatory features of the first cleanup pass.
- Keep the community feedback system functional. Corrections against an authoritative source are not a verified indictment of that source; the reliability concept needs denominators and moderation later.
- User requested work in a **new chat**. The assistant writing this plan must **not begin data cleanup**, must commit this checkpoint to GitHub, and must supply a ready-to-paste chat handoff prompt.

## 6. Success / handoff criteria

- This temporary plan exists on main and is readable to a new chat.
- First pass reviews original-vs-new, then full corpus; certain duplicates consolidated, meaningful variants retained, ambiguous pairs fully presented to user before final link rebuild.
- A term-level source list and explicit primary references survive deduplication; normalized subject and optional context exist with inspectable separate registries.
- No original-source-provenance badge pollution, no UI presentation decisions prematurely implemented, and no new term discovery.
- On completion, exactly one final complete linking/build/export validation is performed *after* user review, with normal CI and real browser checks.

---

**Planning-only checkpoint created by ChatGPT at user request; no deduplication, subject/context migration, UI edits, correction tracking, or link rebuild has begun.**
