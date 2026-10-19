# Stage 6: independent Wave 1 prototype — editorial and browser review

**Date:** 2026-10-19 (America/New_York)
**Repository/workspace:** `Zengez/mathDef` / `research_pipeline/experiments/reconstruction-v1-recovery`.

## Decision: technical Stage 6 review passed; mathematical and external visual review remain explicitly unverified

This is a **standalone reconstructed experimental preview**, not a replacement for `https://zengez.github.io/mathDef/`. The prototype does not read the existing mathematical definitions, citation corpus, or variant data to populate its terms.

### Frozen precursor

- Stage 5 is sealed: **431 of 431 formulations individually reviewed**.
- Outcomes: **338 linked**, **89 individually justified missing compatible targets in the current collection**, and **4 held context ambiguities**.
- **445 screened relationships:** 428 definition uses, 5 logical implications, and 12 equivalent/contextual characterizations.
- Stage 5 records digest: `a01dfe2c2823c57a60bb9f9b6ca89b11aeb833fcda987a3431afba7e2629364b`.
- No duplicate formulation IDs, broken relation endpoints or directed definitional cycles were detected. Stage 5 machine evidence: `state/stage5_seal_evidence.json`.

### Stage 6 content and presentation

- Published independent content: **419 meaning records**, **431 formulations**, **445 relations**, and **431 direct Stacks section source locators**.
- **415 term-name search groups** after presenting four repeated titles as two contextual meaning entries under one common heading: *Galois field extension*, *normal algebraic extension*, *separable algebraic extension*, *purely inseparable extension*.
- Fixed source grouping: source-section identifiers are not mathematical term identifiers. Different names from the same Stacks page now appear separately, while identical names from different pages can appear together.
- Source dialogs link to **specific Stacks tag URLs**, never silently to the general Stacks homepage, and every nested recursive formulation has its own source/correction controls.
- Separate term-name and definition-text real-time search; alphabetically ordered results, initially 40 entries with an incremental “Show 40 more” control. In-Line, Nested and Standard exploration modes are retained.
- Mathematical relationships are not all recursively expandable: `logical_implication` and `equivalent_characterization` are navigable references, not proof that one definition is a prerequisite for the other.
- Scope correction: equivalent characterizations explicitly say **subject to hypotheses** and reveal their individual editorial rationales. This particularly matters for projectivity characterizations restricted to countably generated modules and Serre's criterion under Noetherianity.
- General **Suggest a new definition**, root verification proposals, per-formulation **Suggest correction**, and per-link correction/priority reporting open reviewed GitHub issue proposals only; they do not modify the source corpus.

### Targeted mathematical/source editorial spot-check

Independently inspected these exact source sections and compared selected reconstructed formulations to the underlying mathematics:

| Reconstructed topic | Source | Spot-check result |
| --- | --- | --- |
| Standard étale ring maps | [Stacks 0G1A](https://stacks.math.columbia.edu/tag/0G1A) | Monic derivative criterion matched; standard étale ⇒ étale correctly tagged as implication |
| Smooth ring maps | [Stacks 00T1](https://stacks.math.columbia.edu/tag/00T1) | Finite presentation and naive cotangent quasi-isomorphic to finite projective degree-zero condition matched |
| Geometrically normal algebras | [Stacks 037Y](https://stacks.math.columbia.edu/tag/037Y) | All field extensions and perfect-closure characterizations agreed under stated general setting |
| Purely inseparable extension | [Stacks 09HD](https://stacks.math.columbia.edu/tag/09HD) | Positive characteristic p-power test verified; **trivial extensions in characteristic zero must remain visible**, which is why both source contexts are retained |
| Algebraic field extension review | [Stacks 037H](https://stacks.math.columbia.edu/tag/037H) | Review section confirms algebraic, separable, purely inseparable, normal and Galois conditions, with the positive-characteristic caveat |
| Stone–Čech compactification | [Stacks 0908](https://stacks.math.columbia.edu/tag/0908) | Universal map into quasi-compact Hausdorff space verified; compact is used in the Hausdorff sense |
| Constructible subsets with retrocompact opens | [Stacks 04ZC](https://stacks.math.columbia.edu/tag/04ZC) | Finite union of locally closed-type pieces of retrocompact opens verified |
| Kummer extensions | [Stacks 09I6](https://stacks.math.columbia.edu/tag/09I6) | Correct prime-to-characteristic and roots-of-unity hypotheses, and cyclic Galois conclusion in the indicated setting |
| Separable algebraic field extensions | [Stacks 09GZ](https://stacks.math.columbia.edu/tag/09GZ) | Polynomial separability context confirmed; do not conflate separability of arbitrary transcendental extensions |

These are **spot checks, not a proof of correctness for every definition, not a verification of every citation on the internet, and not external human peer review**. They do not change the sealed independent formulations; they inform Wave 2 contextual research priorities.

### Browser regression and visual limitations

Automated Chromium tests exercise:
- term and definition queries separately, including that unrelated terms drawn from one source page do not coappear;
- consolidated duplicate headings and retention of the two distinct meanings;
- exact source hyperlink target, nested per-formulation sources, root and nested recursive expansion, and collapse;
- nonrecursive implication links, general contribution and correction controls, and verification modal;
- 40-item pagination and reset on filtering;
- a 375px viewport horizontal-overflow bound;
- no uncaught JavaScript exceptions.

Full Python regression suite, JS syntax tests and published catalog provenance are in the Stage 6 builder's Actions evidence. Automated screenshots are retained as artifacts in browser-test runs for human inspection.

**Known limitations deferred rather than hidden:**
1. Source coverage is still intentionally first-wave sparse: the 27 PlanetMath blocked leads and other missing foundations explain many of the 89 missing-target dispositions. New sources belong in Wave 2 and must not be silently invented for Wave 1.
2. **None of the 431 first-wave mathematical formulations are currently marked with KaTeX delimiters** despite KaTeX support in the preview adapter. Most render as readable plain text/Unicode (and informal sub/superscript notation); high-quality structured LaTeX conversion requires mathematical checking in Wave 2.
3. Four ambiguous cross-context relationship reviews remain held: vector space/abelian group, general regular ring, generic versus strict 2-category, pseudofunctor versus strict functor.
4. Some equivalence and implication labels depend on hypotheses not expressed by the target title. The preview now displays the source's qualifying formulation plus an editorial rationale, but an audited relation-scope metadata schema would improve the next wave.
5. Responsive browser checks are automated. **A person has not yet independently reviewed the screenshot for visual design or legibility**, and `human_verified` remains false. Human editorial approval and community corrections are future steps.

## Stage 6 approval scope / next phase gate

After full Python, JavaScript, browser and digest-fingerprint validation, the independent **Wave 1 publication can be reproducibly frozen as a technical research artifact**, even while mathematical peer review is pending. A freeze is **not** a claim that all terms or sources were recovered or that any formulation was academically refereed.

**Do not perform any comparison with the production mathDef corpus until Wave 2 also finishes and freezes.** Any Wave 2 expansion starts only from the frozen independent Wave 1 workspace, with a fresh source-discovery review, explicit unresolved mathematical contexts, and source-level provenance.
