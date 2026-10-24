# Wave2 independent source-free dependency audit — Round 179 (2026-10-24)

## State and method

Resumed from `WAVE2_CURRENT_HANDOFF.md` and the authoritative independent graph `STATE.json`, after the October 24 code-efficiency review. Rechecked source inventory (SHA256 `3759cab60c5fce7287492724fc2ed433ac6001c8a242b66f9bbc887e92294492`), immutable full source statements, latest **effective** append-only amendments rather than stale original node files, and the preexisting unresolved candidate registry. Starting fingerprint `b40bf721311cef8d66971984c799bb8f5833e0447475ab766a97a4a3b9d0cf0b`; 611 meanings, 659/659 formulation scans, 420 unresolved canonical prerequisite identities, 839 effective missing occurrences, 766 amendments, 298 aliases, 0 ambiguous/unassigned.

This is an independent, source-free **dependency/reference** audit; no mathematical meaning was added and no original formulation source was rewritten. No external definition research, original mathDef production data, frozen Wave1, breadth Batch143, unreviewed consolidation gate, or certification was used.

## Corrected three unsupported small-groupoid dependencies

The only populated groupoid meaning `meaning.wave2.foundation.small-groupoid` has original text stating **small category** G whose arrows are invertible. Its smallness hypothesis is not entailed by invertibility. The separate generic category and functor scope errors had already been corrected in Round 177 and were not repeated.

The following complete source formulations were independently examined with all their latest effective reference classifications:

| Parent source formulation | Before | Mathematically correct prerequisite |
| --- | --- | --- |
| `form.74cd6dc48e0606fc.setoid-category` | `groupoid C` → small groupoid | A groupoid with only identity automorphisms; no **smallness** stated; invertible arrows and induced equivalence relation retained |
| `form.0bf601085c1029d4.two-one-category` | `groupoid` → small groupoid | All 2-cells invertible vertically, hence each hom-category a groupoid; source strict 2-category makes no small hom-category assumption |
| `form.5e4b8f6efeda6522.category-fibred-in-groupoids` | `groupoids` → small groupoid | The fibred-in-groupoids condition has no stated size restriction on fibre groupoids; its functor/cartesian-lift references remain intact |

Each currently effective reference imposing the extra smallness condition was changed from `existing:meaning.wave2.foundation.small-groupoid` to a source-context-specific *missing* ordinary-groupoid prerequisite, not to the too-weak unrestricted **category** concept. This is a link correction, **not** a proposal that the independent source should define its groupoids differently.

Full, same-version amendment packet: `dependency_graph/inbox/wave2-sourcefree-round179-groupoid-size-scope.json`; [Git commit `0516764f4fef`](https://github.com/Zengez/mathDef/commit/0516764f4fef84fc7524d5d26466b29d64a231cf). Exact applied receipt `dependency_graph/applied/wave2-sourcefree-round179-groupoid-size-scope.json`, SHA256 `81e4bca693755a4b0bd3a48666c471b06c1983cfdb73ab5b7e4d80fcf96b7684`; `human_certified=false`.

This application first indexed three raw candidate records from their retained source phrases and shared contextual definition:

- `missing.1ebe938ec77d5606093e` — *groupoid*
- `missing.467c799601bb5d539a8f` — *groupoid C*
- `missing.6dd26585ccd4e8c7b6ce` — *groupoids*

They refer to **one contextual mathematical prerequisite**, so two explicit source-reviewed alias decisions (without changing the occurrence identities, phrase strings or raw record history) now map the latter two to canonical `missing.1ebe938ec77d5606093e`. Alias packet `dependency_graph/inbox/wave2-sourcefree-round179-unrestricted-groupoid-aliases.json`, [commit `745846b2d6bb`](https://github.com/Zengez/mathDef/commit/745846b2d6bbcc2407e3f4d8ccba4da411081ef5), exact applied receipt SHA256 `824c9a671225b4abb76334622e6eea26af0c9b2e08ffe7c12662cd50c82ad905`; `human_certified=false`.

The consolidated *effective* missing candidate now has exactly **three incoming parent formulations**, one for each phrase. This was confirmed independently against `missing_candidates.jsonl` and `unresolved_occurrences.jsonl` after application.

## Mathematically important nonmerge and downstream checks

The following independent source variants were read for type/size compatibility and deliberately **not** merged with the generic groupoid:

- `form.f0d993a60533fc99.groupoid-valued-presheaf` explicitly defines a strict `F:C^op→Groupoids`; its target category `Groupoids` is separately contextualized as the category of **small** groupoids. Retain the populated **small-groupoid** dependency for `F(U)`; do not reclassify this source as unrestricted.
- `form.wave2.foundation.small-groupoid` legitimately presupposes a **small** category, and its source text remains unchanged.
- `form.ec5e3a0d13f85f3a.strict-two-category` expresses general hom-category composition with no new set-size hypothesis. Its existing independent category/functor scope adjustments were retained without resubmission.
- `form.3653fa0ad844d187.category-fibred-in-sets` and `form.74cd6dc48e0606fc.category-fibred-in-setoids` inherit the corrected broad fibred-in-groupoids parent and define further *discrete* or *setoid* fibre conditions respectively; they are not independently small-groupoid claims.

Additional high-impact lead check compared representative current effective references for topology-vs-algebra, homomorphism and module-vs-ring object typing across the amended corpus; the sampled apparent mismatches were ordinary contextually valid prerequisites (e.g. modules over rings and localizations), not reason for new edits. No aliases were invented to meet a numerical target.

## Authoritative post-application state (verified)

| Metric | Value |
| --- | ---: |
| Distinct meanings | **611** |
| Complete / total formulations | **659 / 659** |
| Raw missing candidates (historical aliases included) | **728** |
| Reviewed aliases | **300** |
| Resolutions to existing meanings | **7** |
| **Unresolved canonical candidates** | **421** |
| Effective missing occurrences | **842** |
| Complete scan amendments | **769** |
| Historical seed overrides | **19** |
| Ambiguous and unassigned occurrences | **0 / 0** |
| Structurally open / closed | **651 / 8** |
| Consolidation gate | **FALSE** |

Unresolved fingerprint `5ce283b1e53f511a472b9913440f36a3f40a827378823afddd33200c2af7a96a`; inventory hash unchanged. The canonical count rose **by one** solely because a genuinely separate size-unrestricted groupoid prerequisite has been recorded rather than falsely identified with a small groupoid. The three source uses are now one canonical class, **not three new meanings**.

## Resume instructions

Start with current handoff + live STATE. Continue targeted *effective* source-context checks for remaining genuine object/scope mismatches, supported candidate equivalences and high-impact mathematical source leads. Distinguish generic category, ordinary groupoid, small groupoid, and target category `Groupoids`. Do **not** repeat the Round 177 category/functor corrections or Round 179 groupoid corrections, add new mathematical meanings, rewrite source text, open the gate, or conflate source-free graph review with verified citations or human certification.
