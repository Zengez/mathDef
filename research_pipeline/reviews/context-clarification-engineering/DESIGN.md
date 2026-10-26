# Candidate-context review log: design and boundary

Base engineering commit: `51696c08`; authoritative main graph: `a7ce2ba3`.
Owner policies and six-case proposal inputs are read from evidence commit
`c1882af8`, without merging that branch or its historical graph. The approved
component-prerequisite policy is controlling. The later provider checks and
qualification policy are preserved; none authorizes a live correction here.

Use a separate, explicit **analysis metadata log**, not a graph transaction.
The derived missing registry, observations, aliases, nodes, indexes and graph
dispatcher remain untouched. Reuse existing effective replay and alias/seed
validators. A pure API validates append-only hash-chained proposal/review
events and returns a context view. No command submits, applies or auto-loads
this log from the workspace. This is narrower than a candidate split/creation
workflow and does not change the mathematical graph's semantics.

Every proposal pins the complete current graph inputs, the canonical record,
all incoming effective occurrences (including specialized representative uses
and seed references), exact observed/alias paths, full source/node/reference
hashes, and the prior reviewed interpretation. Each occurrence must specify
its component instantiation and retained parent conditions. A review event
approves/rejects an exact proposal digest; it cannot replace its payload.
Reviewers and substantive rationale/provenance are mandatory. Separate trusted
history checkpoints detect truncation, replacement and reordering. Pure log
extension preserves the entire prior prefix; no log writer or apply dispatcher
is introduced. Version control and reviewer authentication remain external
trust requirements, as with existing graph reviews.

Replay fails closed on stale pins or unsupported input. It never guesses
mathematical implication from prose. Structural role checks reject whole-parent
identity, retargeting and graph-edit fields. A reviewer must still establish
that the claimed component instantiation is mathematically valid; authored
text cannot be mechanically certified. No hidden unitality, size, zero-object
or indexing assumptions are added. Metadata cannot add a self-edge because
it cannot add any edge or resolve a candidate.

Readers opt in explicitly and receive **parallel** original-observed,
recorded-canonical, proposed and reviewed descriptions, with exact occurrence
coverage. No context is overwritten and proposals are never displayed as
approved. Audit counts, closure, cycles and source-integrity hashes continue
to use the original graph. Default readers without a log must produce exactly
their previous output. Existing graph preparation commands do not consume
the metadata. This avoids implicitly making a reviewed interpretation into
an applied mathematical correction.

Preflight copies the explicitly supplied independent workspace into a
disposable directory, verifies all paths/bytes, validates/replays there and
compares both original and copy afterward, even on failure. Evidence is
receipt-shaped but explicitly `not_applied`; it is never written to graph
`applied/`. The input log and history checkpoint are also checked unchanged.

Conservative limitation: all replayed events must match the current graph
snapshot. A changed graph requires new explicit review/revalidation; this
version does not invent automatic migration or stale-event supersession.
Hash chains cannot authenticate an author or resist replacement of both
the log and its trusted checkpoint outside protected Git review.

Basic qualification-ledger validation distinguishes proposed candidates from
claimed applied entries with application evidence. It neither adds an entry
to the owner ledger nor treats metadata review as a qualified source edit.
The real ledger currently has zero applied qualifications, which must remain
zero throughout this task.
