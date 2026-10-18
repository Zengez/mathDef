# Closure discovery, classification, and verification case study

Date: 2026-10-18. Scope: targeted, non-exhaustive acquisition pass for the word **closure**, as a reusable protocol for future definition-variant research.

## Decision principle

**Do not equate shared names with equivalent definitions.** The variant system in FORMULATIONS.md is for genuinely equivalent descriptions *of the same mathematical object under explicitly stated assumptions*. Thus the smallest closed superset and neighborhood characterization describe the same topological closure, whereas field algebraic closure, integral closure and closed linear span are different constructions with different types of input and output. These must retain their own stable concept IDs, even though they belong in a navigable thematic family. A second distinction: a *special-case equivalence*, such as the sequential characterization in first-countable spaces, is a variant only if the restriction is conspicuous.

## Reproducible workflow

1. **Inventory the existing repository first.** Enumerate all paths matching closure, closed, hull, completion, span and related words, then inspect existing definition IDs and the policy and parser in FORMULATIONS.md / scripts/build_index.py. In this pass existing `topology.closure`, `geometry.convex-hull`, `linear.span` and `measure.completion-of-measure` were found; avoid duplicating them.
2. **Expand the search across meanings, not just spellings.** Query reference sources for topological, metric, sequential, Kuratowski, algebraic-field, relative algebraic, integral, convex, linear, operator, Zariski, weak and analytic closure, then follow contextual references. Search terms are candidates, never sufficient evidence.
3. **Classify each candidate** as (A) equivalent characterization, (B) restricted-context characterization with hypotheses, (C) different concept needing an ID, (D) existing concept needing only cross-reference, or (E) unresolved/ambiguous. Record cases separately rather than forcing all into `variants/topology`.
4. **Read a concept-specific reference** and compare its input object, ambient space, quantifiers and output type with the proposed formulation. Prefer formal specialist references (Stacks Project, Encyclopedia of Mathematics), with general articles as supplementary support. Check equivalence mathematically rather than inferring it from a shared term.
5. **Write an original short definition** with named ambient assumptions and differences from neighboring notions. Include HTTPS concept-specific source, initial `status: draft`, related IDs that exist and a stable term/ID. Add actual variants under `variants/` with their original parent ID, unique key, label and optional pedagogical order.
6. **QA and checkpoint.** Run repository Python unit tests (including formulations/dependencies), JavaScript checks, full index build and GitHub Pages deployment. Check concept count and stable original IDs, source links, definition-search results and Standard/Nested/In-Line rendering where possible. Record any manual/browser checks still outstanding; a CI pass is not a mathematical peer review.
7. **Maintain a candidate backlog and review notes**, including rejected equivalents and necessary hypotheses. Repeat by mathematical family. Discovery is not comprehensive simply because all first-page search results were reviewed.

## Examined references and disposition

| Candidate | Classification | Evidence | Decision |
| --- | --- | --- | --- |
| Topological closure as closed hull | Existing canonical | https://encyclopediaofmath.org/wiki/Closure_of_a_set | Preserve `topology.closure` |
| Neighborhood/adherent-point test | A | https://encyclopediaofmath.org/wiki/Closure_of_a_set | Variant `neighborhood` |
| Metric distance-zero test | B: metric spaces | https://en.wikipedia.org/wiki/Closure_(topology) | Variant `metric` with metric hypothesis |
| Sequential-limit test | B: first-countable spaces | https://en.wikipedia.org/wiki/Sequential_space | Variant `sequences` with explicit caveat |
| Kuratowski closure axioms | A: equivalent representation of topology | https://encyclopediaofmath.org/wiki/Closure_of_a_set | Variant `kuratowski` |
| Algebraic closure of field | C | https://stacks.math.columbia.edu/tag/09GS | Separate `field.algebraic-closure` |
| Relative algebraic closure within extension | C | https://stacks.math.columbia.edu/tag/037I | Separate `field.relative-algebraic-closure`; relative closure need not be algebraically closed |
| Integral closure of ring in extension | C | https://encyclopediaofmath.org/wiki/Integral_closure | Separate `commalg.integral-closure` |
| Closed convex hull | C | https://encyclopediaofmath.org/index.php?title=Convex_hull | Separate `geometry.closed-convex-hull` |
| Closed linear span | C | https://encyclopediaofmath.org/wiki/Linear_span | Separate `linear.linear-closure` |
| Abstract closure operator (Moore) | C | https://encyclopediaofmath.org/index.php?title=Closure_relation | Separate `order.closure-operator` |
| Sequential closure as an operator | C | https://en.wikipedia.org/wiki/Sequential_space | Separate `topology.sequential-closure`; not always idempotent |
| Zariski closure | D: instance of topological closure using Zariski topology | https://encyclopediaofmath.org/wiki/Zariski_topology | Candidate for dedicated contextual entry after checking algebraic-set formulations |
| Operator closure | E | https://encyclopediaofmath.org/wiki/Operator | Defer: closure of graph only defines an operator when the graph closure remains single-valued (closability) |
| Weak / weak-star closure | D/C depending on ambient topology | https://encyclopediaofmath.org/wiki/Topological_vector_space | Defer explicit dual-pair conventions to next pass |
| Holomorphic / polynomial hull | D: existing different constructions | `definitions/scv/holomorphic-hull.tex` and `definitions/scv/polynomial-hull.tex` | Do not duplicate under closure |
| Completion of a measure | D: distinct operation already represented | `definitions/measure/completion-of-measure.tex` | Do not confuse with topological closure |
| Analytic closure | E: ambiguous term across contexts | Multiple specialized uses; no single verified universal definition | Do not add a generic unsupported entry |

## Checks and limitations

- First wave: four sourced variants of `topology.closure`, seven new context-specific concept IDs. Original closure definition unchanged. New entries remain drafts.
- **Not an exhaustive literature review.** Sources support terminology/formulation suitability; independent peer review, thorough proof-level equivalence checking and browser-level rendering QA remain separate steps.
- Important mathematical distinction: an arbitrary abstract closure operator on a powerset need not satisfy the Kuratowski finite-union and empty-set axioms; sequential closure may fail idempotence.
- For later interface design: consider a dedicated **Closure family** or disambiguation panel of related distinct concepts rather than displaying incomparable meanings as alternative definitions of one object. Variant cards should continue to mean mathematical equivalence.

## Next acquisition queues

Zariski closure (including affine vanishing ideal characterization); closure of an unbounded closable linear operator; norm versus weak and weak-star closures; real versus complex algebraic-geometric notions; closure under finitary operations/universal algebra and generated substructures; Galois closure of extensions; radical/ideal saturation where terminology requires precision; and other specialized analytic uses. Do not auto-add these without separately checking types, assumptions and references.
