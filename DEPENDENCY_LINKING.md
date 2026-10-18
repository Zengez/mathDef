# Recursive definition explorer and automatic links

**Status:** First implementation on 2026-10-16. A first community suggestion/review queue using GitHub Issues is now implemented; see [FEEDBACK_WORKFLOW.md](FEEDBACK_WORKFLOW.md). Anonymous intake remains a deferred enhancement.

## User interaction

Under the **term-search** field, choose one of three modes. The choice is retained locally if browser storage is available.

- **Standard:** the original single-definition view; ordinary related-term links are preserved.
- **Nested (default):** recognized dependencies appear in collapsed boxes below the main definition. Several siblings can be open; a collapsed parent remembers its descendants' state.
- **In-Line:** detected terms receive small "(definition: term)" buttons. Clicking inserts the target definition after the **paragraph** containing the cue, with additional indentation at deeper levels. Curated inclusions without body offsets appear after the main body.

Both search panes use the selected mode. Source links, related-term navigation and split/focused layouts are preserved.

## Automatic initial population

The builder calls [scripts/dependency_links.py](scripts/dependency_links.py) to derive dependencies from the **body** of every definition, not from its related metadata or citations. Results are attached to each definition in the generated index as target IDs, source offsets, and matching evidence. No original LaTeX definition file is modified. The build additionally generates a public JSON report named **dependency-review.json**, containing link counts and the first 150 unresolved ambiguities.

- Match complete term names and declared aliases, with simple English plural inflections, not arbitrary word substrings. Prefer longest overlapping phrase.
- Hide LaTeX commands and math expressions from normal prose matching; exact LaTeX-bearing term names and aliases may match the original formula text.
- Resolve competing targets using direct related-ID metadata, reciprocal references and subject-folder context. If evidence is still too close, omit the ambiguous occurrence.
- Never add a dependency solely on the strength of related-term metadata.
- Omit self-references; collapse multiple occurrences of the same target; cap initial display at 30 direct dependencies per entry.
- No language-model API or network access is needed to build or traverse the links.

The resulting link graph is an initial editorial suggestion, not a guarantee that all links are correct or complete.

## Branch-local recursion and cycle protection

At each descendant level, exclude its own ancestors and every dependency already accessible at ancestor levels, including siblings whose boxes are collapsed. Do not globally deduplicate across unrelated branches. Generate deeper children only while expanding that branch.

## Curated corrections

Edit [data/link_overrides.json](data/link_overrides.json). Each top-level key is a **source definition ID**; available instructions are:

- **exclude:** list of target IDs which must not be auto-linked from this source.
- **include:** list of target IDs to add even if automatic matching missed them.
- **resolve:** object mapping an ambiguous visible phrase to the precise target ID.

Example shape (illustrative only; the current manifest starts empty):

    {
      "algebra.example": {
        "exclude": ["algebra.group"],
        "include": ["algebra.ring"],
        "resolve": {"kernel": "linear.kernel"}
      }
    }

The builder checks IDs and override structure. In-Line mode places a forced inclusion at the end of the definition if no literal source-text match exists. Visitor feedback now creates GitHub Issue proposals for maintainers to review; it must not automatically alter this manifest or mathematical content. Incorrect link reports include the source definition ID, target definition ID, and matched phrase.

## Limitations and future work

1. Term matching is heuristic, not semantic parsing. It can miss paraphrases, unusual inflections and implicit concepts and may choose the wrong mathematical sense.
2. Literal mathematics is supported, but equivalent LaTeX notation is not inferred.
3. In-Line expansions appear after their paragraph to preserve readable HTML and KaTeX boundaries.
4. Community feedback intake and approval workflow are deferred; this initial infrastructure supplies a clear, editable correction point.
5. Browser-by-browser visual and accessibility QA remains useful after deployment.

## Validation

The GitHub Pages workflow checks JavaScript syntax, runs Python tests, regenerates the link population for the complete corpus, and publishes the site. [tests/test_dependency_links.py](tests/test_dependency_links.py) covers term boundaries, notation masking, target ambiguity, manual overrides, and stable matching offsets.


## Equivalently defined concepts with multiple formulations

See [FORMULATIONS.md](FORMULATIONS.md). The matcher analyzes each formulation body separately and saves its own source offsets and formulation key, so In-Line links attach to the correct mathematical text. Nested view uses the union of the concept's dependency targets, avoiding duplicate child boxes. Source/target IDs in link overrides still refer to the underlying **concept**, not to a separately indexed formulation. A suggested correction or bad-link report may specify the originating formulation for editorial investigation.
