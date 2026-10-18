# Multiple equivalent formulations of one mathematical definition

**Implemented:** October 18, 2026.

A mathematical concept may have several correct, complementary formulations. mathDef shows them **together under one term heading and one stable definition ID**, not as duplicate search results. **Function** is the first example:

1. Assignment formulation: each domain input has exactly one output.
2. Set-theoretic formulation: a subset of the Cartesian product whose first-coordinate projection is total and single-valued.

Order formulations by likely educational encounter **only when evidence is clear**; otherwise append. This is not a mathematical correctness ranking.

## Files and metadata

The original definition remains under **definitions/** in its original TeX file. The original ID, main body, source and term stay unchanged for backwards compatibility. Optional original-file metadata specifies label and rank:

    % form_label: Assignment formulation
    % form_order: 0

Defaults are **Original formulation**, rank **0**. Existing entries need no migration.

An additional formulation is a separate TeX file under **variants/**, with metadata:

    % parent: functions.function
    % key: graph
    % label: Set-theoretic (relation) formulation
    % order: 20
    % source: https://www.homepages.ucl.ac.uk/~ucahmto/0007/_book/1-3-functions.html
    % status: draft

    For sets $X$ and $Y$, a function may be represented by a
    subset $f\subseteq X\times Y$ satisfying totality and uniqueness.

Required: **parent** (existing concept ID), **key** (unique within that concept), **label**, and individual HTTPS **source**. Optional **order** defaults to 100; **status** defaults to draft. Tie-breaking is stable by key. Uncertain cases can omit order and naturally appear after the original. The source should support the precise formulation, not just mention the topic.

Example: [variants/functions/function-graph.tex](variants/functions/function-graph.tex).

The builder validates alternatives, attaches them to their parent, and adds a **formulations** array to that parent in the published index. It does **not** increment the concept count or create a second "Function" search result. The canonical original body remains separately accessible to older clients.

## UI, search, recursion and feedback

- One result per concept in both search boxes. Definition-content search looks through every formulation body.
- Standard, Nested, and In-Line viewing show all formulations in the specified order, including recursively displayed definitions.
- Each formulation displays its own label, reference and LaTeX file link.
- Dependency detection scans each formulation separately, keeping precise body offsets and the formulation key for accurate In-Line cues and reports. Nested dependencies are deduplicated at the concept level.
- "Correct formulation" reports attach the variant key and file path; link reports can identify the variant in which the link was found.

**Mathematical policy:** Only attach genuinely equivalent formulations. Different objects, distinct meanings or incompatible conventions require distinct concept IDs or explicit qualification, not a misleading list of supposed equivalents. In particular, the function codomain is part of the specified function-from-X-to-Y data, even if the graph alone need not determine it.

## Verification

The new [tests/test_formulations.py](tests/test_formulations.py) checks the Function example, source, order, stable IDs, link offsets, metadata validation and compatibility. GitHub CI also checks the JavaScript, feedback tests, existing dependency tests and full corpus build.
