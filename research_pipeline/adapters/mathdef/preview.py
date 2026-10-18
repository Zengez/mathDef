"""Build an isolated, read-only mathematical definition preview from engine output.

Never reads the production definitions/, variants/, or web/ directories.
Usage: python -m research_pipeline.adapters.mathdef.preview --workspace PATH
"""
import argparse
import html
import json
from collections import defaultdict
from pathlib import Path

from research_pipeline.engine.core import PipelineError, atomic_json


def build(workspace):
    root = Path(workspace).resolve()
    source = root / "published" / "catalog.json"
    if not source.is_file():
        raise PipelineError("Publish the isolated reconstruction catalog first")
    catalog = json.loads(source.read_text(encoding="utf-8"))
    groups = defaultdict(list)
    for meaning in catalog["meanings"]:
        groups[meaning["term_group_id"]].append(meaning)
    observations = {x["id"]: x for x in catalog["observations"]}
    sources = {x["id"]: x for x in catalog["sources"]}
    group_records = []
    for gid, meanings in sorted(groups.items()):
        entries = []
        for meaning in meanings:
            formulations = []
            for form in meaning["formulations"]:
                citations = []
                for evidence_id in form["evidence_ids"]:
                    observation = observations[evidence_id]
                    citation = sources[observation["source_id"]]
                    citations.append({
                        "title": citation["title"], "url": citation["url"],
                        "locator": observation["locator"], "source_id": citation["id"],
                        "evidence_id": evidence_id,
                        "role": "Source evidence (editorially screened, not human-verified)"
                    })
                formulations.append({
                    "id": form["id"], "text": form["text"],
                    "sources": citations, "review_state": form["review_state"]
                })
            entries.append({
                "id": meaning["id"], "label": meaning["context"],
                "display_term": meaning["display_term"],
                "formulations": formulations,
            })
        group_records.append({
            "id": gid, "title": meanings[0]["display_term"], "meanings": entries
        })
    output = root / "preview"
    output.mkdir(parents=True, exist_ok=True)
    atomic_json(output / "catalog.json", {
        "groups": group_records,
        "relations": catalog["relations"],
        "verification_notice": "Not yet manually verified",
    })
    # Raw JSON is encoded for safe insertion into an inline script (avoid HTML end-tags).
    dataset = json.dumps(group_records, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e")
    doc = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Independent reconstruction — prototype</title>
<style>
body{font:16px/1.5 system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem;color:#202329}
header{border-bottom:1px solid #ddd;padding-bottom:1rem} .disclaimer{color:#684800;background:#fff7dc;padding:.65rem;border-radius:.4rem}
input{padding:.5rem;width:min(100%,27rem);font:inherit}label{display:block;margin:.7rem 0}
article{border:1px solid #ccc;border-radius:8px;padding:1rem;margin:1rem 0}
section{border-left:3px solid #777;padding-left:1rem;margin:.8rem 0}
pre{font:inherit;white-space:pre-wrap;overflow-wrap:anywhere}
button{cursor:pointer;padding:.4rem .7rem}dialog{max-width:min(700px,90vw);border:1px solid #777;border-radius:10px}
dialog::backdrop{background:#0008} .muted{color:#666;font-size:.9em}
</style></head><body><header>
<h1>Mathematical definitions — reconstruction prototype</h1>
<p>This experimental site is generated exclusively from an isolated research workspace. It is not the production mathDef website.</p>
<p class="disclaimer">Not yet manually verified. Screened research drafts are not certified mathematical facts.</p>
<label>Search term <input id="term" placeholder="Search names only" aria-label="Search term"></label>
<label>Search definition <input id="definition" placeholder="Search content only" aria-label="Search definition"></label>
</header><main id="results"></main>
<dialog id="sources"><form method="dialog"><button style="float:right">Close</button></form><h2>Source evidence</h2><div id="sources-content"></div></dialog>
<script>const DATA=___DATA___;
const main=document.getElementById("results");
const modal=document.getElementById("sources");
const sourcesView=document.getElementById("sources-content");
function el(tag,text,parent){const x=document.createElement(tag);if(text!==null)x.textContent=text; if(parent)parent.append(x);return x}
function showSources(group){
 sourcesView.replaceChildren();
 group.meanings.forEach(m=>{
  el("h3",m.label,sourcesView);
  m.formulations.forEach(f=>{
   el("h4",f.id,sourcesView);
   const list=el("ul",null,sourcesView);
   f.sources.forEach(s=>{
    const li=el("li",null,list),a=el("a",s.title+" — "+s.locator,li);
    a.href=s.url;a.target="_blank";a.rel="noopener noreferrer";
    el("span"," ("+s.role+")",li);
   });
  });
 });
 modal.showModal();
}
function render(){
 const q=document.getElementById("term").value.toLowerCase().trim();
 const d=document.getElementById("definition").value.toLowerCase().trim();
 main.replaceChildren();
 const hits=DATA.filter(g=>(!q||g.title.toLowerCase().includes(q)) &&
  (!d||g.meanings.some(m=>m.formulations.some(f=>f.text.toLowerCase().includes(d)))));
 hits.forEach(g=>{
  const card=el("article",null,main);el("h2",g.title,card);
  g.meanings.forEach(m=>{
   const section=el("section",null,card);el("h3",m.label,section);
   m.formulations.forEach(f=>{
    el("p","Not yet manually verified",section).className="muted";
    el("pre",f.text,section);
   });
  });
  const btn=el("button","View sources",card);btn.type="button";
  btn.addEventListener("click",()=>showSources(g));
 });
 if(!hits.length)el("p","No matching terms",main);
}
document.getElementById("term").addEventListener("input",render);
document.getElementById("definition").addEventListener("input",render);
render();
</script></body></html>""".replace("___DATA___", dataset)
    (output / "index.html").write_text(doc, encoding="utf-8")
    return {"groups": len(group_records), "meanings": len(catalog["meanings"]),
            "path": str(output / "index.html")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.workspace), indent=2))


if __name__ == "__main__":
    main()
