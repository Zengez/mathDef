# Reusable Research and Publication Pipeline — Design Checkpoint

**Status:** Discussion specification, NOT an implemented engine.  
**Recorded:** 2026-10-18.  
**First adapter:** mathDef (mathematical definitions); engine intentionally independent of this subject.
**Next action:** Review unresolved decisions with the user BEFORE implementing scripts. Do not mistake candidate schemas or defaults for agreed implementation.

## 1. Purpose and agreed approach

Build a reusable, chat-executable system for acquiring, organizing, cross-linking, validating, publishing, and maintaining a body of structured scholarly material. It should work both with a new/empty repository and with subsequent single-entry suggestions, and eventually be reusable in other repositories with different meanings of "term" and "content".

**Two separate bulk phases are an explicit requirement:**

1. **Bulk initialization / prototype wave.** Follow a relatively linear, simple Stage 0 → 1 → 2 → 3 → 4 → 5 → 6 sequence. Its purpose is to acquire a substantial first corpus and publish a usable prototype, not to exhaust every synonym, source, variant, or relationship. Apply structural and automated checks before publication; mark all unapproved formulations as not manually verified. Avoid automatic recursive discovery loops during this initial wave.
2. **Bulk acquisition / rigorous second wave.** After examining the first website/corpus and adapting the subject-specific presentation and schema, undertake source-list expansion using acquired terminology; search old AND new sources again for synonyms, missed contexts, alternative formulations, and missing links; improve verification and cross-links. This later wave is iterative and may revisit any earlier stage; record measurable yield and use stopping criteria.

**Targeted acquisition mode** later uses the same underlying stages with a narrow scope around a proposed missing term, correction, or variant. A requested term should trigger a search for other relevant contexts and variants, not merely a single pasted definition, but expansion should be bounded and resumable. Incoming community reports form a review queue, not unreviewed automatic changes.

The stages are logically independent and can run in different chat turns or at different reasoning-effort settings. The first prototype wave is deliberately mostly linear even though the final engine supports feedback loops.

## 2. Stage 0: Project-specific concept contract (human discussion required)

Before starting a new repo, the user and assistant discuss and explicitly record:

- Subject/scope, intended readership, inclusion/exclusion rules and licensing constraints.
- What counts as a **term/search key** (name? statement? concept? theorem title?); whether it may be unnamed or have aliases.
- What counts as **content** (definition, theorem statement, proof, educational explanation, etc.), required and optional content types.
- What counts as the same underlying **meaning/object**, a distinct context, a variant/formulation, and a synonym; identity and stable-ID policy.
- How terms are grouped for display, and whether several mathematically different meanings belong under one searchable heading.
- Recognized relationship types; what constitutes an acceptable cross-link and whether context-sensitive prioritization is needed.
- Source standards, disciplinary-specific citation conventions, and minimum evidence/quality requirements.
- Automated publication gate, human verification scope, handling of revisions, feedback workflow, and safety of public claims.
- Website adapter and required project quirks; data format and rendering constraints; desired prototype size.
- Source access budget: **zero by default**; paid sources may be catalogued but not acquired without explicit authorization.
- Resumption/batching parameters and per-stage limits.

**Important:** A future theorem project need not define its term as a theorem name and its content as a single statement; these are choices to make interactively in Stage 0. The pipeline must never hardcode "definition" or "proof" as universal content types. Capture unresolved choices as open decisions and prompt the user; do not silently assume.

## 3. Data model and information preservation

Use a general-purpose intermediate schema, with a project-specific adapter translating approved records into its own files.

Suggested conceptual layers (working names, subject to Stage 0):
- **Source:** bibliographic identity, domain, scope, discovered URL(s), source type, reputation evidence, licensing/reuse rights, accessibility, paid/free/unknown category, restrictions, date evaluated, and evaluator/notes. Store canonical source IDs so updates do not require editing each definition.
- **Observation / source evidence:** a source-specific occurrence of a name and/or proposed content, exact URL and locator (section, equation, page, theorem number, etc.), retrieval/access notes, permitted excerpt or original paraphrase, evidence type and processing history. A source observed during research is not automatically a source that SUPPORTS the final definition.
- **Term / search group:** a displayed name, aliases, normalized search aliases, and references to its meanings. Multiple distinct meanings can belong under one term heading (not merely equivalent formulations).
- **Meaning / context:** a stable identity describing what object is being defined, ambient structures, hypotheses and contextual distinctions. E.g. topological closure of a subset versus algebraic closure of a field.
- **Formulation / content item:** a specific mathematical expression or characterization, content type, scope, optional pedagogical order, and its parent meaning. Equivalent formulations and restricted-case characterizations remain distinguishable. A source observation might support multiple formulations and a formulation can have multiple supporting sources.
- **Relation / link:** source and target stable IDs, relation type (depends-on, synonym, equivalent meaning, special case, generalization, etc.), the originating formulation/context, evidence, confidence, decision state, and possibly preferred destination meaning for a contextual link.
- **Verification / editorial event:** immutable provenance of who/what was reviewed, exact content revision(s), result, scope, date and explanation.

**Never destructively prune evidence:** store all relevant source observations and merge/reject/consolidate decisions, including apparently redundant observations; the published material can be compact, while the research provenance remains intact. Do not automatically equate same spelling with same mathematical meaning, nor multiple names with different meanings.

Keep verification dimensions distinct: (a) structural validation, (b) source located, (c) source suitability/support, (d) semantic grouping/equivalence, (e) mathematical/content correctness, and (f) editorial approval. Automated structural success never implies human mathematical verification.

**Proposed serialization:** interoperable, schema-versioned JSONL for large appendable batches and JSON/YAML for small config/manifests; stable record identifiers and content hashes; no dependence on mathDef LaTeX conventions within the engine itself. This format is a proposal to review, not yet implemented.

## 4. Seven stages and suggested effort

### Stage 0 — Project configuration (High, interactive once per repo and on major schema changes)
Write a human-readable project contract plus machine-readable adapter config. Explicitly define "term", "content", identity, variants, context, relationships, gates, sources, and UI. Output: reviewed project profile and outstanding questions.

### Stage 1 — Source discovery and trust catalogue (Medium–High)
Search for reference websites, catalogs, authoritative texts, journals, archives, repositories, and stable URL patterns relevant to the project; **do not discover/acquire terms yet**. Record authority rationale and per-source caveats, coverage, access mechanism and legal/technical permissions.

Keep source reputation, access price, and reuse rights as SEPARATE fields:
- Approved/openly accessible sources suitable for permitted collection.
- Reliable but free-to-read with restricted copying/processing rights.
- Potentially reliable paid/subscription sources: **catalog only**, no paid acquisition by default.
- Unknown/unreliable/disallowed sources: hold for review or exclude.

"Free" does not mean unrestricted reuse; "reputable" does not imply permission to scrape or copy. Observe site terms, robots/access limits, rate limits, privacy, and copyright; use locators/metadata instead of unlicensed bulk copying. arXiv content/source access is generally free, but individual reuse rights still matter.

### Stage 2 — Raw term/title discovery (Low–Medium)
Walk source indexes, TOCs, glossaries, category trees, search APIs or other permitted discoverability features. Record likely term strings, spelling and sources where observed; do NOT decide mathematical identity, extract full definitions or aggressively merge synonyms. Preserve a term-to-source inverted index (and source-to-terms), source record IDs, discovery paths and timestamps. De-duplicate purely mechanical duplicate observations without discarding evidence.

**Prototype-wave discipline:** broadly collect headings and relevant candidate titles; do not attempt expensive per-term synonym searches across every source.

### Stage 3 — Raw content acquisition (Low–Medium)
For each raw term, inspect the sources known from Stage 2 to contain it, and capture each found content candidate with its source ID and exact locator. Light mechanical duplicate detection is permitted; do not erase semantically distinct or not-obviously-identical candidate formulations. Do not require all sources to be re-queried for every term; use indexed material or supported targeted access, avoiding wasteful cross-products.

Retain the source language only when license/quotation limits permit. Otherwise preserve a reference/locator and independently authored provisional paraphrase with an explicit provenance label. Source existence is not proof of mathematical validity.

**First-wave deliberate simplification:** no separate exhaustive synonyms/variant discovery Pass B here; those will emerge partly as separate titles and later in Stages 4/5. A stronger source-spanning Pass A/B is for the second wave.

### Stage 4 — Semantic grouping and categorization (High)
Review the raw candidates; group synonyms and aliases into search terms, distinguish different meanings/contexts, equivalent or restricted formulations, and truly redundant content. Decide parent meaning/term membership and retain all linked provenance. Do just enough outside lookups to resolve classification where required; defer comprehensive mathematical link research to Stage 5 and final verification to Stage 6. Mark uncertain equivalence as needing review rather than force-merge.

### Stage 5 — Relationship mapping and contextual linking (High)
Research links among meanings, formulations and other terms, including definitions occurring within definitions and per-context specialization. Track supported relation type, origin passage, target meaning and reason. Detect cycles and resolve/hold ambiguous links. In mathematical definitions, a link activated inside a particular context should prioritize the relevant meaning/formulation while keeping all other legitimate meanings discoverable; reportable link corrections must allow a contributor to propose which meaning should rank first. Links are provisional until checked and should not silently claim mathematical implication.

### Stage 6 — Validation, editorial normalization, publication (High/Extra High)
Finish original paraphrasing and precise assumptions, sources and citations; run all feasible automated checks (schema, references, missing context, traceability, consistency flags, math rendering, link integrity, duplicates, CI/deployment). Individual manual verification is NOT a blocking requirement for publishing an otherwise eligible draft, but no raw Stage 3 observations should be published directly. Publish only after all pipeline stages and automated publication gates are complete. Visibly mark material without accepted human review **"Not yet manually verified"**. Actual mathematical peer review remains distinct.

**Draft publication gate:** at minimum: valid IDs/schema, context and formulation clearly labeled, permitted and identifiable support, no known blocking contradiction/unresolved attribution issue, acceptable provisional prose, all links conform to policy, and automated tests passed. Exact thresholds are project-configurable and should be confirmed in Stage 0. If a candidate fails, place it in a hold/review queue instead of pretending validation succeeded.

## 5. Execution strategy, progress persistence and recovery

- Each stage is a small, independently invocable command/process reading a common input schema and writing a versioned output manifest. No global full-corpus rerun should be necessary merely to resume.
- **Checkpoint frequently and durably**, using configurable count/time limits. Initial heuristic: after 5–10 sources (Stage 1), 25–100 titles (Stage 2), 5–20 terms (Stage 3), and 5–10 records for Stages 4/5; Stage 6 after each reviewed item or small batch. The numbers are tunable.
- Write idempotent records with stable IDs, source and input revisions, stage/version, processed IDs, accepted/rejected/held counts, current cursor, remaining work, exceptions and the next safe action. Persist/commit at agreed batch boundaries so losing a chat or tool execution discards at most an unfinished batch.
- Prefer transactional/atomic output and append-only decisions where practical. Rerunning any batch must not duplicate data or overwrite prior reviewed decisions without a clear conflict signal.
- A concise top-level handoff checkpoint points to per-stage manifests, committed artifacts, known failures and the exact next step. Never rely solely on a chat transcript for resume.
- Keep each stage usable interactively in chat; no requirement to use Work or Codex. A future script can be run in supported environments, and GitHub-based operation may need smaller commits where filesystem state is ephemeral.
- Record costs, wall time, batch sizes, tokens/API calls where accessible, and yield per stage; not all measurements are available in every execution environment.

## 6. Three modes and phase boundaries

**Mode: Initial bulk prototype** — Stage 0 setup, source search, broad title collection, known-source content collection, clustering, minimal sufficient linking, automated validation, publish coherent draft website. **Stop to inspect the prototype** for repo-/subject-specific quirks BEFORE running wave two. Do not attempt endless second-order discovery during this first pass.

**Mode: Second-wave rigorous expansion** — use the existing term/alias/context dictionary to search the wider web for previously missed trustworthy sources (each newly found source must pass Stage 1 review); crawl accepted new sources; revisit existing sources for alternate terms, synonyms, hidden or additional formulations and contexts. Permit term-specific Pass A (known source hits) and Pass B (cross-source searches, synonyms/context), identify new candidate relationships, and revise prior records without losing evidence. Measure novel credible sources, new contexts and distinct formulations per unit cost/time to support a rational stopping decision.

**Mode: Targeted new/suggested term** — search published and candidate corpus first; distinguish genuinely missing meaning from synonym, duplicate or missing formulation; invoke the same stage logic on a scoped set; discover credible contexts/variants as practical; map local inbound/outbound links; publish if gates pass; retain any longer-tail context search as an explicit follow-up task. A community suggestion alone never automatically publishes content.

The three modes are configurations of shared machinery, not three unrelated research algorithms.

## 7. Public website and evidence interface

- Each term search result may display multiple distinct meanings and, within them, multiple formulations, each specifying the mathematical object, ambient context and assumptions. A single term heading should not imply those meanings are equivalent.
- "View sources" opens an accessible **modal dialog** over the page (dismissible without a new tab), listing *all retained source records relevant to the displayed term*, grouped by meaning/formulation and distinguishing verified supporting evidence, additional sources, merely considered sources, and unsupported/rejected candidates as appropriate. All used-source provenance should be retained, including sources of consolidated/redundant formulations.
- Keep the source registry separate from individual definition bodies and use source/evidence IDs. Changes to an underlying bibliography should not require editing every published definition.
- For nested/in-line linked definitions, rank relevant meanings first using originating meaning, formulation, context and explicit curated overrides where available; never hide other legitimate meanings or imply confidence unsupported by evidence.
- The "fix this link" report should allow not only wrong/missing links, but also "correct term, wrong meaning prioritized" and a specific proposed target meaning.
- mathDef will need an adapter/migration design: current canonical definition IDs and variants were initially modeled as equivalent formulations; the broader term → meaning → formulation hierarchy and source modal are **not yet implemented**. Preserve stable historical IDs and links where feasible. Do not claim the existing site has these features now.

## 8. Community verification and editorial decision queue

- All eligible published drafts can carry a "Not yet manually verified" notice and a "Propose verification" action.
- The verification form lets a person check one, multiple, or all formulations within a term/meaning. The submitted issue records the **exact formulation IDs and content revisions/hashes** verified, evidence/rationale, and which aspects (mathematics, sources, context, etc.) they assert.
- Require an **authenticated GitHub identity**. Merely typing a GitHub username is not proof. Reuse the existing GitHub Issues prefilled-new-issue approach where feasible: the visitor selects items, the site builds the draft issue, GitHub signs them in, and the user presses Submit. Direct API submission must never expose write credentials or bypass explicit consent.
- Suggestions/verification claims are queued, NOT automatically approved. An authorized editor reviews the submission, the person's asserted credentials and supporting evidence, and accepts, rejects or asks for clarification. Contributor identity and optional claims about credentials are separate; don't imply credentials were verified merely because GitHub authenticated a username.
- Acceptance records precise scope, reviewer decision, date and content revision; accepted community verification is not automatically equivalent to formal scholarly peer review.
- A later substantive edit may invalidate/reopen a prior verification for the changed formulation. Proposed future convenience: if fewer than about 20 accepted verified items change at once, show side-by-side old/new text and offer the editor a manual reconfirmation decision without forcing a new crowd submission. Exact UX/automation deferred until verification actually starts.
- The community feedback flows (missing definition, correction, wrong link/ranking, verification) share an auditable review queue and can reference the same records, source evidence and content revisions.

## 9. Engine versus repository-specific adapter

**Engine (portable):** project contract/schema version, source registry, term and content observation capture, indexing, provenance, semantic decisions, relation graph, review status, mode selection, checkpoint/retry logic, export/validation interfaces, reporting and test harness. It must never assume all projects are math, all terms have a single meaning, or content is one text definition.

**Adapter (per repo):** source/site-specific reader integrations where authorized, vocabulary normalization and mathematical domain rules, representation/rendering (e.g. mathDef LaTeX/KaTeX), paths and metadata, search behavior, matching and recursive link display, repo CI, publication and GitHub issue templates, presentation preferences and known quirks. Version the adapter and pin it in each batch manifest.

Proposed eventual directory layout, **illustrative only**:
- research_pipeline/engine/ — importable core modules and stage commands
- research_pipeline/schemas/ — record and manifest schemas
- research_pipeline/adapters/mathdef/ — translation to existing mathDef
- research_pipeline/project_profiles/ — Stage 0 contract and configuration
- research_pipeline/state/ — stage progress and resumable work queues
- research_pipeline/records/ — source registry, observations, meanings, formulations, links and evidence
- research_pipeline/tests/ — deterministic fixture-based tests
- docs/ — usage guide, source permissions, review policy, acquisition case studies

Exact paths, serialization and any package structure must be agreed BEFORE implementation. An engine may eventually be extracted into its own reusable repo, but the current request is to document its design, not decide that deployment structure now.

## 10. Verification and testing plan for the eventual implementation

- Small, artificial fixtures containing synonyms, same-name distinct meanings, special-case formulations, corroborating sources, rejected sources, and ambiguous relationships.
- Stage-by-stage schema and provenance integrity tests; merging must preserve all observations.
- Retry/idempotency tests: deliberately interrupt between batches and resume, verifying no duplicate or lost committed records.
- Paid/disallowed source guardrails; query throttling and rights metadata; no accidental paid access or unlicensed bulk copying.
- Versioned verification tests: a material edit marks prior verification stale while a mere formatting change can be manually retained.
- GitHub prefill/report tests for multi-select verification, authenticated authorship at GitHub, erroneous-link ranking correction and source attribution.
- mathDef adapter tests for canonical ID stability, contextual relevance, nested/inline modes, source modal and site build. Browser-level interaction QA is separate from CI.
- Publication tests that reject raw/untraceable/blocked candidate material and display the human-verification disclaimer correctly.

## 11. Settled decisions versus unresolved discussion

**Agreed in conversation:** seven stages (0–6); first linear prototype wave; separate deeper second wave; targeted suggestion mode; source registry with evidence retained after consolidation; no irreversible pruning; stage checkpoints and idempotency; zero-default paid-source budget; independent engine plus adapters; modal "View sources"; grouped context-aware meanings under a search term; link relevance corrections; automated publication before mandatory human verification; multi-select community verification through authenticated GitHub Issue submissions; editor approval; version-aware review.

**Questions explicitly deferred by user (previous item 9):**

1. **Breadth of automatic variant discovery for a targeted suggestion.** Search all mathematically legitimate meanings of an ambiguous term immediately, or begin with requested context and expand to near neighbors? Proposed compromise: search broadly for candidates, but bound the initial editorial work, record additional senses for later. The user has not yet answered this.
2. **Acceptance threshold for community verification.** Is one authorized editor approval initially sufficient, with potential specialist/multiple review later? Suggested default: yes, but the user has not yet answered this.

**Additional small decisions to discuss before coding:**
- Whether the engine should initially reside inside mathDef or its own separate reusable repository, and how adapters get versioned.
- What initial prototype scale/crawl limits are acceptable, since "significant enough to expose quirks" is a subjective goal; Stage 0 should explicitly choose the range.
- Final names/ID policies for term-group, meaning and formulation, and migration from existing mathDef canonical IDs.
- Required minimum source-evidence/reuse criteria for automatically published drafts, and whether all discovered but weakly sourced materials are held privately.
- Frequency and git/storage approach for durable checkpoint writes in chat-driven executions.

## 12. Current stopping point and next safe action

**No pipeline engine or new scripts have been created as part of this design discussion.** This file is solely the requirements/design checkpoint and may be revised freely. Before implementing scripts, resume the discussion at Section 11 (especially the user's outstanding answers to item 9), finalize the Stage 0 template and the minimum viable prototype, then implement a small vertical slice using fixtures and the mathDef adapter. Do not start a second-wave expansion or resume the Closure case study until the design is confirmed by the user.
