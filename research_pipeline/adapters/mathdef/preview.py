"""Build an isolated mathematical reference preview from an experiment catalog.

Acquisition remains independent of production mathDef. Only experiment files
and the adapter's own static JS/CSS are read. Does not deploy to GitHub Pages.
"""
import argparse
import json
import shutil
from collections import defaultdict
from pathlib import Path

from research_pipeline.engine.core import PipelineError, Workspace, STAGES, atomic_json, digest
from research_pipeline.adapters.mathdef.direct_additions import add_direct_research



def read_working_draft(root):
    """Render unsealed independent Wave 2 screened records, never publication."""
    workspace = Workspace(root)
    if workspace.config().get("independent_second_wave") is not True:
        raise PipelineError("Working draft preview requires the independent Wave 2 workspace")
    if any(workspace.state(stage).get("sealed") for stage in STAGES):
        raise PipelineError("The Wave 2 working-draft preview requires all stages unsealed")
    records = {stage: workspace.records(stage) for stage in STAGES}
    source_ids = set(records["sources"])
    term_ids = set(records["terms"])
    observation_ids = set(records["observations"])
    meaning_ids = set(records["meanings"])
    forms = set()
    for term in records["terms"].values():
        if term["source_id"] not in source_ids:
            raise PipelineError("Working draft term references an unknown source")
    for obs in records["observations"].values():
        if obs["term_id"] not in term_ids or obs["source_id"] not in source_ids:
            raise PipelineError("Working draft observation references an unknown source or term")
    for meaning in records["meanings"].values():
        if any(term not in term_ids for term in meaning["term_ids"]):
            raise PipelineError("Working draft meaning references an unknown term")
        for form in meaning["formulations"]:
            if form["review_state"] != "screened":
                raise PipelineError("Unscreened formulation cannot appear in public draft")
            if not form["evidence_ids"] or any(e not in observation_ids for e in form["evidence_ids"]):
                raise PipelineError("Working draft formulation lacks source evidence")
            if form["id"] in forms:
                raise PipelineError("Working draft has repeated formulation ID")
            forms.add(form["id"])
    for rel in records["relations"].values():
        if (rel["review_state"] != "screened" or rel["from_formulation"] not in forms
                or rel["target_meaning"] not in meaning_ids):
            raise PipelineError("Unscreened or broken relation cannot appear in public draft")
    return {stage: list(records[stage].values()) for stage in STAGES}


def build(workspace, *, draft=False, output=None):
    root = Path(workspace).resolve()
    if draft:
        catalog = read_working_draft(root)
    else:
        source = root / "published/catalog.json"
        if not source.is_file():
            raise PipelineError("Publish the reconstruction catalog first")
        catalog = json.loads(source.read_text(encoding="utf-8"))
    # Page-section IDs are provenance locators, not mathematical term IDs.
    # One section may define unrelated concepts, and one concept can appear
    # in multiple source sections. Group by the complete, normalized title,
    # retaining distinct contextual meanings and all source/formulation IDs.
    # This is a presentation-only identity: sealed Stage 4/5 records remain
    # untouched, and context-sensitive synonym consolidation belongs to Wave 2.
    grouped = defaultdict(list)
    for meaning in catalog["meanings"]:
        normalized_title = " ".join(meaning["display_term"].casefold().split())
        group_id = "preview.term." + digest(normalized_title)[:24]
        grouped[group_id].append(meaning)
    observations = {x["id"]: x for x in catalog["observations"]}
    references = {x["id"]: x for x in catalog["sources"]}
    terms = {x["id"]: x for x in catalog.get("terms", [])}
    out_groups = []
    for gid, meanings in sorted(grouped.items()):
        result_meanings = []
        aliases = set()
        for meaning in meanings:
            form_rows = []
            supporting_ids = set()
            for form in meaning["formulations"]:
                citations = []
                for evidence_id in form["evidence_ids"]:
                    observation = observations[evidence_id]
                    source = references[observation["source_id"]]
                    supporting_ids.add(evidence_id)
                    citations.append({
                        "title": source["title"], "url": source["url"],
                        "locator": observation["locator"], "source_id": source["id"],
                        "evidence_id": evidence_id, "role": "Supporting evidence (screened draft)",
                    })
                form_rows.append({
                    "id": form["id"], "text": form["text"], "sha256": digest(form),
                    "sources": citations, "review_state": form["review_state"],
                })
            other_sources = []
            for obs in observations.values():
                if obs["term_id"] in meaning["term_ids"] and obs["id"] not in supporting_ids:
                    source = references[obs["source_id"]]
                    other_sources.append({
                        "title": source["title"], "url": source["url"], "locator": obs["locator"],
                        "role": "Encountered during research, not approved as supporting evidence",
                    })
            for term_id in meaning["term_ids"]:
                if term_id in terms and (
                    " ".join(terms[term_id]["label"].casefold().split())
                    == " ".join(meaning["display_term"].casefold().split())
                ):
                    # Original Stage 2 page headings must never masquerade as
                    # synonyms for every term defined on that source page.
                    aliases.add(terms[term_id]["label"])
            result_meanings.append({
                "id": meaning["id"], "label": meaning["context"],
                "display_term": meaning["display_term"], "term_group_id": gid,
                "formulations": form_rows, "other_sources": other_sources,
            })
        result_meanings.sort(key=lambda item: (
            item["display_term"].casefold(), item["label"].casefold(), item["id"]
        ))
        out_groups.append({
            "id": gid, "title": meanings[0]["display_term"], "aliases": sorted(aliases),
            "meanings": result_meanings,
        })
    out_groups.sort(key=lambda group: (group["title"].casefold(), group["id"]))
    # Direct mathematical research additions are ordinary website content.
    # No publication stage, dependency graph, global audit, or intake gate.
    added_direct = 0
    if draft:
        added_direct = add_direct_research(
            out_groups, catalog["relations"], root / "direct_research" / "terms.json"
        )
    output = Path(output).resolve() if output is not None else root / "preview"
    output.mkdir(parents=True, exist_ok=True)
    project = json.loads((root / "project.json").read_text(encoding="utf-8"))
    review_file = root / "state/stage5_review.json"
    reviewed = json.loads(review_file.read_text(encoding="utf-8")) if review_file.exists() else None
    status_notice = (
        "Source-screened research draft: %d of %d formulations reviewed; "
        "%d without a supported target and %d held link ambiguities. "
        "Neither complete prerequisite coverage nor human verification is claimed."
        % (reviewed["reviewed"], reviewed["formulations"],
           reviewed["decisions"].get("no_supported_target", 0),
           reviewed["decisions"].get("held_ambiguity", 0))
        if reviewed and not draft else "Source-screened research draft; completeness not verified."
    )
    if draft:
        status_notice = (
            "Unsealed Wave 2 working snapshot: %d contextual meanings, %d screened "
            "relationships. Research remains incomplete, and completeness is not established."
            % (len(catalog["meanings"]) + added_direct, len(catalog["relations"]))
        )
    payload = {
        "groups": out_groups, "relations": catalog["relations"],
        "verification_notice": "Not yet manually verified",
        "github_issues": project.get("github_issues_url", "https://github.com/Zengez/mathDef/issues/new"),
    }
    atomic_json(output / "catalog.json", payload)
    payload_string = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e")
    doc = """<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>___STAGE_TITLE___ — independent mathDef reconstruction</title>
<link rel="stylesheet" href="preview.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="preview.js"></script>
</head><body><header><p><a href="../">← Reconstruction stages</a></p>
<h1>___STAGE_TITLE___</h1>
<p>This independent research reconstruction is not the production mathDef website.</p>
<p><strong>___STAGE_DESC___</strong></p>
<p class="disclaimer">Not yet manually verified. These are screened research drafts, not certified mathematical facts.</p>
<p class="muted">___REVIEW_NOTICE___</p>
<div class="controls">
<label>Search term <input id="term" type="search" placeholder="Names and aliases" aria-label="Search term"></label>
<label>Search definition <input id="definition" type="search" placeholder="Formulation text only" aria-label="Search definition"></label>
<button id="suggest-term" type="button">Suggest a new definition</button>
<label>Explore definitions <select id="mode" aria-label="Definition exploration mode">
<option value="nested">Nested</option><option value="inline">In-Line</option>
<option value="standard">Standard</option></select></label>
</div></header><p class="muted">Each result has View sources and Propose verification actions.</p>
<main id="results"></main>
<dialog id="sources" aria-label="Source evidence"><form method="dialog"><button>Close</button></form>
<h2>Source evidence</h2><div id="sources-content"></div></dialog>
<dialog id="verify" aria-label="Propose a verification"><form method="dialog"><button>Close</button></form>
<h2>Propose verification</h2><div id="verify-content"></div></dialog>
<script id="reconstruction-data" type="application/json">___PAYLOAD___</script>
<footer>Independent experiment • Source references do not imply human verification.</footer>
</body></html>""".replace("___PAYLOAD___", payload_string).replace(
        "___REVIEW_NOTICE___", status_notice).replace(
        "___STAGE_TITLE___", "Wave 2 — evolving research draft" if draft
        else "Wave 1 — frozen baseline").replace(
        "___STAGE_DESC___", "Unsealed and incomplete; regenerated from screened independent records."
        if draft else "Frozen independent first-wave prototype, retained for comparison.")
    (output / "index.html").write_text(doc, encoding="utf-8")
    assets = Path(__file__).resolve().parent
    for asset in ("preview.js", "preview.css"):
        shutil.copy2(assets / asset, output / asset)
    return {"groups": len(out_groups), "meanings": len(catalog["meanings"]) + added_direct,
            "direct_research_meanings": added_direct,
            "path": str(output / "index.html")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--draft", action="store_true",
                        help="Render unsealed independent Wave 2 records without publication")
    parser.add_argument("--output", type=Path,
                        help="Write to an external directory instead of the experiment")
    args = parser.parse_args()
    print(json.dumps(build(args.workspace, draft=args.draft, output=args.output), indent=2))


if __name__ == "__main__":
    main()
