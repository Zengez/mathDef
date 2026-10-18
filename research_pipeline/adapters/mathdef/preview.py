"""Build an isolated mathematical reference preview from an experiment catalog.

Acquisition remains independent of production mathDef. Only experiment files
and the adapter's own static JS/CSS are read. Does not deploy to GitHub Pages.
"""
import argparse
import json
import shutil
from collections import defaultdict
from pathlib import Path

from research_pipeline.engine.core import PipelineError, atomic_json, digest


def build(workspace):
    root = Path(workspace).resolve()
    source = root / "published/catalog.json"
    if not source.is_file():
        raise PipelineError("Publish the reconstruction catalog first")
    catalog = json.loads(source.read_text(encoding="utf-8"))
    grouped = defaultdict(list)
    for meaning in catalog["meanings"]:
        grouped[meaning["term_group_id"]].append(meaning)
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
                if term_id in terms:
                    aliases.add(terms[term_id]["label"])
            result_meanings.append({
                "id": meaning["id"], "label": meaning["context"],
                "display_term": meaning["display_term"], "term_group_id": gid,
                "formulations": form_rows, "other_sources": other_sources,
            })
        out_groups.append({
            "id": gid, "title": meanings[0]["display_term"], "aliases": sorted(aliases),
            "meanings": result_meanings,
        })
    output = root / "preview"
    output.mkdir(parents=True, exist_ok=True)
    project = json.loads((root / "project.json").read_text(encoding="utf-8"))
    payload = {
        "groups": out_groups, "relations": catalog["relations"],
        "verification_notice": "Not yet manually verified",
        "github_issues": project.get("github_issues_url", "https://github.com/Zengez/mathDef/issues/new"),
    }
    atomic_json(output / "catalog.json", payload)
    payload_string = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e")
    doc = """<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Independent reconstruction prototype</title>
<link rel="stylesheet" href="preview.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="preview.js"></script>
</head><body><header><h1>Mathematical definitions — reconstruction prototype</h1>
<p>This independent research reconstruction is not the production mathDef website.</p>
<p class="disclaimer">Not yet manually verified. These are screened research drafts, not certified mathematical facts.</p>
<div class="controls">
<label>Search term <input id="term" type="search" placeholder="Names and aliases" aria-label="Search term"></label>
<label>Search definition <input id="definition" type="search" placeholder="Formulation text only" aria-label="Search definition"></label>
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
</body></html>""".replace("___PAYLOAD___", payload_string)
    (output / "index.html").write_text(doc, encoding="utf-8")
    assets = Path(__file__).resolve().parent
    for asset in ("preview.js", "preview.css"):
        shutil.copy2(assets / asset, output / asset)
    return {"groups": len(out_groups), "meanings": len(catalog["meanings"]),
            "path": str(output / "index.html")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.workspace), indent=2))


if __name__ == "__main__":
    main()
