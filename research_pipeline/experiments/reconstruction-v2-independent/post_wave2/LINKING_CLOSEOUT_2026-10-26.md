# Post-Wave2 merged-reference linking closeout — 2026-10-26

## Status: initial existing-term linking wave COMPLETE

**The original terminology backlog remains fully finished: 2,019 / 2,019
frozen quick-scan candidates dispositioned. No new candidates were gathered
during linking.** All 2,197 existing contextual meanings remain in the merged
corpus (958 independently reconstructed Wave2 + 1,014 original mathDef + 225
subsequent post-Wave2 merged-only meanings), displayed under 2,048 term groups
with 2,246 actual definition formulations.

The separate original mathDef production source, historically frozen independent
Wave2 corpus, frozen Wave1, and 2,019-lead scan are unchanged. This report
closes the **first existing-term linking/website integration wave**, not a claim
that all human editorial review or mathematical verification is complete.

## Tested implementation

The earlier linking PR #62 added an anchored matcher in
`research_pipeline/adapters/mathdef/merged_linking.py`, combining existing
term names/aliases and definitions on the merged site only, with explicit
provenance. Automatically matched links have
`review_state=lexical_candidate` and `human_verified=false` and are displayed
as **Suggested**, not editorially certified. Existing screened relations
preserve their review states. The linking report is generated as
`/reconstruction/merged/link-report.json`.

This follow-up links refinement:

- Prevents made-up multiword matches across hidden LaTeX expressions,
  paragraph boundaries, and TeX-formatting commands, preserving exact
  source-text offsets in any remaining accepted link.
- Retains retrievable source-meaning IDs, formulations, excerpts, and
  eligible variant meanings for ambiguous existing terms (only existing
  terminology: no vocabulary discovery).
- Adds conservative, explicitly documented broad representatives for
  equivalent/compatible ordinary term labels, e.g. topological space,
  abelian group, subspace topology, open set, homeomorphism. It does **not**
  merge or erase alternative formulations. Ring homomorphisms in scheme and
  commutative-algebra contexts favor the identity-preserving meaning.
  Supremum and infimum use context-specific real/order-theoretic preferences;
  a martingale transform is recognized as a discrete-time setting.
- Preserves genuine distinct variant meanings: e.g. random variables with
  real versus arbitrary measurable codomains, discrete versus continuous
  martingales, different open balls in metric/normed/quasi-metric settings.
  A CW-complex's weak topology remains distinct from weak operator/functional
  analytic topologies.
- Corrects recursive expansion to block **only ancestor terms on the active
  path**, so if A cites both B and C, B may still cite C without looping to A.
  Both nested and in-line expansion remain available, with **In-Line**
  the default for new visitors (an existing stored user choice is respected).
- Adds actual Chromium browser checks of both independent search inputs,
  link click/expand, two-level nested recursion, sibling reuse, ancestor
  cycle blocking, mobile layout, and runtime JavaScript errors.
- Adds normal Python tests for literal offsets, plural matches,
  expression-boundary false positives, candidate provenance and
  variant-specific selection; CI also tests frozen scanner coverage,
  generated merged index consistency, unchanged independent baseline,
  JavaScript syntax, and source-exact anchors.

## Final successful CI snapshot

Successful combined-preview build and independent preview preserve:

| Measure | Result |
|---|---:|
| Combined existing contextual meanings | **2,197** |
| Definition formulations scanned for links | **2,246** |
| Term headings | **2,048** |
| New tentative anchored link relationships | **2,836** |
| Previously screened relationships newly positioned inline | **259** |
| Formulations with positioned definition links | **1,706 (about 76%)** |
| Ambiguous existing-term occurrences deliberately left unresolved | **117** |
| Frozen quick-scan terminology candidates processed | **2,019 / 2,019** |

The totals are generated from the actual merged-site builder, not hand-counted.
Source-to-target anchored relationships are checked against unmodified
definition strings, and the website's browser smoke has no page-level errors.

## Remaining work is quality refinement, NOT a wave completion gate

The 117 ambiguous-context **occurrences** are preserved with examples in the
generated report. They often represent substantively distinct conventions:
random variable (real/general), supremum and infimum (real/order-theoretic),
discrete/continuous martingale, normed-vector-space scalar conventions,
and metric versus quasi-metric or normed-ball terminology. **Do not force an
arbitrary target or count them as verified links.** An unlinked formulation
may be self-contained or use mathematical expressions rather than literal
term-name prose; no requirement that every formulation have a guessed link.

Future optional work, when requested, is targeted source-context review of
remaining ambiguities and user-submitted corrections, then a separate,
explicitly authorized terminology discovery phase. Do not restart bulk
candidate collection, dependency-graph gates, research packets or old
historical Wave2 reconstruction workflows.

This closeout is the durable checkpoint. No user action is needed to close the
current linking pass.
