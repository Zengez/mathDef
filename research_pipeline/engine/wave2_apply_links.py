"""Apply source-screened Wave 2 dependency links without rewriting Wave 1 reviews.

Guards:
* all 440 existing/added formulations have a review entry;
* all prior 445 screened links remain present and linked to their source reviews;
* all 24 incoming links have precise source phrase and source/target provenance;
* old no-target / ambiguity outcomes may be superseded ONLY with individual
  documented, newly supported links and explicit override events;
* no self-links or directed definition-dependency cycles.
"""
from __future__ import annotations
import argparse,json,hashlib
from collections import Counter,defaultdict
from pathlib import Path
from .core import Workspace,PipelineError,canonical,digest,jsonl,atomic_json
from .stage5_review_gate import atomic_jsonl

def locator(meaning,observation_map):
    if isinstance(meaning.get("source_citation"),dict):
        return meaning["source_citation"].get("url")
    form=meaning["formulations"][0]
    ids=form.get("evidence_ids",[])
    return observation_map[ids[0]]["locator"] if ids and ids[0] in observation_map else None

def check_cycles(meanings,rels):
    by_form={f["id"]:m["id"] for m in meanings.values() for f in m["formulations"]}
    graph=defaultdict(set)
    for rel in rels.values():
        if rel["relation_type"]=="definition_uses":
            fr=by_form.get(rel["from_formulation"])
            if fr is None:
                raise PipelineError("Undefined graph source")
            to=rel["target_meaning"]
            if fr==to:
                raise PipelineError("Self-referential definition link")
            graph[fr].add(to)
    color={}
    def visit(u):
        if color.get(u)==1:
            raise PipelineError("Definition dependency cycle introduced: "+u)
        if color.get(u)==2:
            return
        color[u]=1
        for v in graph.get(u,set()):
            visit(v)
        color[u]=2
    for node in list(graph):
        visit(node)

def run(root,batch):
    w=Workspace(root)
    if not (w.root/"state/baseline.json").exists():
        raise PipelineError("Requires independently forked Wave 2")
    if w.state("relations").get("sealed"):
        raise PipelineError("Wave 2 relations already sealed")
    meanings=w.records("meanings")
    observations=w.records("observations")
    forms={f["id"]:(m,f) for m in meanings.values() for f in m["formulations"]}
    if len(meanings)!=428 or len(forms)!=440:
        raise PipelineError("Outdated or altered meaning catalog for curated relationship batch")
    catalog_digest=digest(list(meanings.values()))
    ledger_path=w.root/"state/wave2_formulation_reviews.jsonl"
    reviews=jsonl(ledger_path)
    review_map={r["formulation_id"]:r for r in reviews}
    if len(reviews)!=440 or len(review_map)!=440 or set(review_map)!=set(forms):
        raise PipelineError("Missing or repeated formulation review identity")
    if any(r.get("meaning_catalog_digest")!=catalog_digest for r in reviews):
        raise PipelineError("Wave 2 relation review is stale against meanings")
    previous=w.records("relations")
    if len(previous) not in (445,469,481):
        raise PipelineError("Unexpected relationship ledger size, check earlier batches")
    incoming=jsonl(batch)
    batch_number = "02" if batch.name.endswith("batch_02.jsonl") else "01" if batch.name.endswith("batch_01.jsonl") else None
    if batch_number is None:
        raise PipelineError("Unknown curated relationship batch; explicit scope required")
    expected_count=12 if batch_number=="02" else 24
    if len(incoming)!=expected_count or len({r.get("id") for r in incoming})!=expected_count:
        raise PipelineError(f"Expected {expected_count} distinct curated research relationships")
    before_count=469 if batch_number=="02" else 445
    if len(previous) not in (before_count,before_count+expected_count):
        raise PipelineError(f"Incorrect previous link count for batch {batch_number}: {len(previous)}")
    fromlinks=defaultdict(list)
    for row in incoming:
        fid,mid=row.get("from_formulation"),row.get("target_meaning")
        if fid not in forms or mid not in meanings:
            raise PipelineError("Invalid reviewed relation endpoint: "+str(row.get("id")))
        source,form=forms[fid]
        target=meanings[mid]
        if source["id"]==mid:
            raise PipelineError("Self dependency")
        if form["review_state"]!="screened" or any(
             f["review_state"]!="screened" for f in target["formulations"]):
            raise PipelineError("Unscreened mathematical endpoint")
        if row.get("relation_type")!="definition_uses" or row.get("review_state")!="screened":
            raise PipelineError("Unexpected relationship classification")
        if row.get("human_verified") is not False:
            raise PipelineError("No human peer verification may be invented")
        phrase=row.get("source_phrase")
        if not phrase or phrase.casefold() not in form["text"].casefold():
            raise PipelineError("No exact source formulation anchor for "+row["id"])
        if row.get("source_locator")!=locator(source,observations) or row.get(
                "target_locator")!=locator(target,observations):
            raise PipelineError("Source/target locator diverged from primary evidence")
        if len(row.get("editorial_reason","").strip())<65:
            raise PipelineError("Mathematical rationale too short")
        if row["id"] in previous and previous[row["id"]]!=row:
            raise PipelineError("Previously screened Wave 2 link has changed")
        fromlinks[fid].append(row)
    proposed={**previous,**{r["id"]:r for r in incoming}}
    check_cycles(meanings,proposed)
    for fid,items in fromlinks.items():
        review=review_map[fid]
        if review["decision"] not in (
             "needs_review","linked","no_supported_target","held_ambiguity"):
            raise PipelineError("Unknown old link disposition")
        if review["decision"] in ("no_supported_target","held_ambiguity") and (
               review["relation_ids"] or review.get("original_wave1_disposition") not in
                    ("no_supported_target","held_ambiguity")):
            raise PipelineError("Invalid attempted override of a historical disposition")
        for rel in items:
            if rel["id"] in review["relation_ids"] and rel["id"] not in previous:
                raise PipelineError("Review claims a non-existing relationship")
    # Persist explicit inherited-decision override history before mutation.
    override=[]
    for fid,items in sorted(fromlinks.items()):
        review=review_map[fid]
        if review["original_wave1_disposition"] in ("no_supported_target","held_ambiguity"):
            override.append({
                "formulation_id":fid,
                "old_wave1_disposition":review["original_wave1_disposition"],
                "old_review_digest":review["original_review_digest"],
                "original_editorial_reason":review["editorial_reason"] if not review.get(
                    "wave2_override_reason") else review.get("original_editorial_reason"),
                "new_link_ids":sorted(x["id"] for x in items),
                "override_reason":"Previously missing source-specific mathematical target now has an independently evidenced and screened Wave 2 meaning; compare each new link's exact formulation anchor, hypothesis scope and source locator.",
                "reviewed_by":"assistant_wave2_individual_mathematical_source_comparison_2026_10_19",
                "human_verified":False
            })
    override_path=w.root/f"events/wave2_link_disposition_overrides_batch{batch_number}.jsonl"
    override_path.parent.mkdir(parents=True,exist_ok=True)
    override_payload="".join(canonical(x)+"\n" for x in override)
    if override_path.exists() and override_path.read_text(encoding="utf-8")!=override_payload:
        raise PipelineError("Prior link-disposition override evidence differs; refuse silent revision")
    override_path.write_text(override_payload,encoding="utf-8")

    # Workspace ingest is idempotent for identical link IDs. All mathematical
    # consistency checks above happen before it writes any data.
    result=w.ingest("relations",batch,batch_size=expected_count)
    for fid,links in fromlinks.items():
        review=review_map[fid]
        was=review["decision"]
        if was in ("no_supported_target","held_ambiguity") and not review.get("wave2_override_reason"):
            review["original_editorial_reason"]=review["editorial_reason"]
            review["wave2_override_reason"]="Reassessed after separately sourced and screened Wave 2 foundational meanings became available; the individual mathematical evidence is recorded with each relationship."
        review["decision"]="linked"
        review["relation_ids"]=sorted(set(review["relation_ids"])|{r["id"] for r in links})
        review["editorial_reason"]="Individually checked current mathematical source formulation and new contextual prerequisite meaning against exact source locators; individual reasons are preserved on each relation."
        review["reviewed_by"]="assistant_wave2_individual_mathematical_source_comparison_2026_10_19"
        review["source"]="wave2_explicit_link_review"
    atomic_jsonl(ledger_path,[review_map[k] for k in sorted(review_map)])
    actual=w.records("relations")
    if len(actual)!=before_count+expected_count or len(ledger_path.read_text(encoding="utf-8").splitlines())!=440:
        raise PipelineError("Unexpected post-intake review counts")
    referred={rid for x in review_map.values() for rid in x["relation_ids"]}
    if set(actual)!=referred:
        raise PipelineError("An independent relationship is missing a formulation-specific review")
    check_cycles(meanings,actual)
    counts=dict(Counter(x["decision"] for x in review_map.values()))
    still_pending=sum(r["decision"]=="needs_review" for r in review_map.values())
    report={
      "phase":f"wave2_source_grounded_relationship_batch_{batch_number}_screened",
      "meaning_count":len(meanings),"formulation_count":len(forms),
      "total_screened_links":len(actual),
      "inherited_wave1_links_preserved":445,
      "added_source_grounded_links":expected_count,
      "link_batch_unique_source_formulations":len(fromlinks),
      "review_decisions_after_batch":counts,
      "inherited_missing_or_held_dispositions_revisited":len(override),
      "original_wave1_dispositions_preserved_in_review_fields":True,
      "newly_defined_relations_reviewed_individually":True,
      "dependency_graph_has_cycles":False,
      "pending_wave2_link_reviews":still_pending,
      "wave2_link_stage_sealed":False,
      "original_production_baseline_consulted":False,
      "human_peer_verified":False,
      "next":"Continue source verification, review the remaining new formulations and all unresolved missing-target/ambiguity cases before stage sealing."
    }
    atomic_json(w.root/f"state/wave2_link_review_batch_{batch_number}.json",report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",required=True,type=Path)
    p.add_argument("--batch",required=True,type=Path)
    a=p.parse_args()
    print(json.dumps(run(a.workspace,a.batch),indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
