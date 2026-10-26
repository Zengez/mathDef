# Wave 2 convention and contextual evidence packets

Prepared on `codex/wave2-convention-evidence-2026-10-26`, stacked on engineering
branch/PR #13 at `51696c08b1e5e8b7964ad4f1599e61acc9301ff9`. Current `main`
mathematical checkpoint is `a7ce2ba3cdd07e6d0b9809d4e39014fb8533228c`.
Historical audit input is pinned to branch head
`978db08b2fe736638237c6967f934dbfe96894a3`. Only the explicitly named audit
reports/ledgers were read from that historical commit; its graph snapshot was
not read, copied or merged. PR #13's metadata could not be read through the
available GitHub API (`Forbidden`); branch heads were verified through Git.

Start with [the 13-card adjudication index](ADJUDICATION_QUEUE.md), then
[the topic-based mathematical review](REVIEW.md). The owner has **approved the default typed component-prerequisite policy**
([decision record](APPROVED_DEPENDENCY_GRANULARITY_POLICY.md)); the 40 cards
remain individually unmodified by that decision. Their distinct source
conventions, exact graph dispositions and any other choices still require
separate adjudication or verification. No graph packet is authorized.

| File | Role |
| --- | --- |
| `EVIDENCE.json` | Comprehensive machine-readable inventory: all 40 historical reviews, exact original/current anchors, full sources and observations, current links, target variants, alias/resolution/override history and authored mathematical analyses. |
| `REVIEW.md` | Forty mathematical packets organized by convention/topic, including full parent formulations, arguments, counterexamples, recommendations and remaining decisions. |
| `CONTEXTS.md` | All 222 captured current formulations in full, with exact versions and effective reference rows; shared target/variant catalog. |
| `ANALYSES.json` | Human-authored per-case arguments and proposed dispositions, kept separate from captured graph facts. |
| `ADJUDICATION_QUEUE.json`, `.md` | Thirteen manageable discussion cards covering each of the 40 cases exactly once. |
| `SOURCE_DEFERRALS.md`, `SUPPLEMENTARY.json` | Applied historical corrections; four unchanged provisional source issues; topological inverse-continuity question; compactness/FIP qualification. |
| `TRANSACTION_STATUS.json` | Six receipt-verified transactions and two superseded historical review anchors. |
| `PROTECTED_FILE_HASHES.json` | Pre-review raw byte hashes of all 2,293 authorized workspace files. |
| `VALIDATION.json` | Actual tested checks, fingerprints, hashes and exact changed paths. |
| `CHECKPOINT.json` | Durable progress and delivery status; no further mathematical action authorized. |
| `capture.py`, `validate.py` | Task-local reproducibility helpers. No general auditor or engine change; writes are confined to this review directory, or none for validation. |

## Findings and limits

The historical **13 source-convention deferrals + 27 contextual ambiguities**
are all still unresolved canonical candidates. They account for **104 parent
visits, 93 distinct formulations**. Every parent source version, observation
record, provider record and compared target-definition version is unchanged
from its historical anchor. Thirty-nine cases have unchanged effective nodes;
rank 399's node changed through the applied local-connectedness amendment.
Its old global-basis warning is superseded; its pointwise missing prerequisite
remains. Historical source/occurrence IDs are retained alongside current ones.

Applied real-time filtration, Ext/Hom, local-connectedness, order-zero S-linearity
and m-primary transactions are distinguished from remaining scope questions.
The shifted-operator alias is also recorded. Inactive m-primary alias history
is preserved: 301 historical events versus 300 active aliases. A live node hash
alone does not detect alias/resolution effects, so the evidence also records
full effective references and ledger/receipt/version checks.

Several interpretations can be rejected mathematically now: unital span formulas
for arbitrary zero-action modules, B-linear de Rham differentials, quotient
fields without irreducibility, literal coprimality with zero characteristic,
doubletons with equal coordinates, and greatest/maximal equivalence outside
total orders. Whether the registry should encode generic component prerequisites
or entire compound data is a **user policy decision**. Exact source conventions
remain **unverified**; provider names and mechanical checks cannot supply them.
Every recommendation is unapplied, and none automatically blocks or accepts
Pass 2 consolidation.

All 2,293 protected file paths/bytes remain identical. No mathematical source,
graph, candidate, alias, receipt, ledger, production file, deployment artifact,
or frozen Wave 1 data changed. No production/frozen mathematical records or
external subject sources were consulted. Gate remains closed and Pass 3 is
unauthorized. The historical 421/421 ledger is preserved as historical evidence.

## Actual checks and reproduction

From the repository root:

```sh
W=research_pipeline/experiments/reconstruction-v2-independent
python -m research_pipeline.reviews.convention-evidence-2026-10-26.validate
python -m research_pipeline.engine.dependency_consistency_worklist --workspace "$W" --exhaustive
python -m research_pipeline.engine.dependency_consolidation_readiness --workspace "$W" --exhaustive
python -m research_pipeline.engine.dependency_reconciliation_status --workspace "$W" --queue research_pipeline/reviews/canonical-identity-2026-10-24/LIVE_RECONCILIATION_QUEUE.json
python -m research_pipeline.engine.dependency_provenance_audit --workspace "$W"
python -m research_pipeline.engine.dependency_global_audit --workspace "$W" scan --limit 80 --candidate-limit 80 --include-cycle-edges
python -m unittest discover -s research_pipeline/tests -v
git diff --check
git diff --name-only 51696c08b1e5e8b7964ad4f1599e61acc9301ff9
```

All executed successfully. Python: **256 run, 254 passed, two expected stale
historical-proposal skips**, no failures/errors (3.170 s). Readiness: **19/19**
mechanical checks true, zero integrity failures, Pass 2 completion
`not_determined`. Consistency: **20 review leads**, zero integrity findings.
Global audit: nine review leads, one formulation-avoidable effective cycle,
zero unavoidable components and zero integrity findings. Structural provenance
is complete; all 659 formulations remain paraphrases with unspecified
verification state. None of these results certifies the mathematics or sources.

The evidence validator checks all source/context/review/meaning-version hashes,
full target variants, current replay edges, original evidence preservation,
all six receipt statuses, exact predecessor anchors of the three edge
corrections, four unchanged source-issue records, complete queue coverage and
the protected-file manifest. Deterministic recapture and local document links
were also checked. A preliminary document-link scan mistook mathematical
`[D,s](m)` notation for a link; formulas were fenced/quoted and the code-aware
scan passed with 147 links checked. No integrity condition was weakened.

To reproduce machine capture, first fetch the pinned historical branch commit,
then run `python -m research_pipeline.reviews.convention-evidence-2026-10-26.capture`.
This regenerates **only `EVIDENCE.json`**, using committed `ANALYSES.json`; it
refuses a workspace differing from the protected baseline. It neither chooses
dispositions nor regenerates the graph. Human discussion documents remain
review-authored reports. A future graph change makes these anchors stale and
requires a new evidence checkpoint, not quiet rebasing of historical facts.

No apply/rebuild/preflight/submission/export transaction, external source crawl,
workflow dispatch, consolidation acceptance or phase transition was executed.
Frontend builds/tests were not repeated for this documentation-only preparation;
the engineering baseline's results are historical, not claimed as rerun here.

Delivery is recorded in `CHECKPOINT.json`. Review this branch against the
engineering integration branch to see only this evidence directory; comparison
against `main` also includes the still-unmerged engineering work from PR #13.

The branch was pushed successfully through evidence checkpoint `5c87378fa46b75ebb3011c385469c77f1826e21b` and
this final delivery note. Draft PR creation was attempted with `gh pr create
--draft` and a REST POST with `draft: true`; both returned **Forbidden**. No PR
was created or merged. [Open the evidence-only comparison](https://github.com/Zengez/mathDef/compare/codex/wave2-engineering-integration...codex/wave2-convention-evidence-2026-10-26?expand=1).
