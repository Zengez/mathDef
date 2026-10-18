"""Apply genuinely source-reviewed Stage 3 batch records in an isolated workspace.

Input is a HUMAN/assistant-authored JSONL of editorial decisions containing
source-grounded independent formulations. A URL/Definition-anchor alone is
never silently promoted to evidence. The existing Stage 3 review gate checks
the full 318-term inventory separately before allowing any seal.

Each record:
  term_id, decision, editorial_reason, reviewed_by,
  definitions: [{key, text, source_section, context_hint, source_locator?}]

Definitions are appended only for decisions of "supported". Decisions of
"no_suitable_definition" must explain which actual section was examined.
Every update is checked against the sealed term/source catalog and the prior
per-term acquisition record. The original production mathDef is never read.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from .core import PipelineError, Workspace, canonical, jsonl
from .source_intake import safe_source_url
from .stage3_attempts import CONTENT_VISITED, require_full_attempt_coverage
from .stage3_review_gate import require_reviewed_term_dispositions
from .core import atomic_json


def apply(workspace, batch_path, *, check_only=False):
    w = Workspace(workspace)
    cfg = w.config()
    if not cfg.get("external_reference_mode") or not cfg.get("require_reviewed_term_dispositions"):
        raise PipelineError("Use the corrected independent Stage 3 workspace")
    if w.state("observations").get("sealed"):
        raise PipelineError("Corrected Stage 3 already sealed; do not amend")
    require_full_attempt_coverage(w.root, w.root/"state/stage3_acquisition_attempts.jsonl")
    terms, sources, existing = w.records("terms"), w.records("sources"), w.records("observations")
    attempts = {r["term_id"]:r for r in jsonl(w.root/"state/stage3_acquisition_attempts.jsonl")}
    reviews_path = w.root/"state/stage3_term_reviews.jsonl"
    reviews = jsonl(reviews_path)
    by_id = {r["term_id"]:r for r in reviews}
    if len(reviews) != len(terms) or len(by_id) != len(terms):
        raise PipelineError("Review inventory is not 1:1 with sealed term catalog")
    incoming = jsonl(batch_path)
    if not incoming:
        raise PipelineError("Empty curated mathematical review batch")
    if len({r.get("term_id") for r in incoming}) != len(incoming):
        raise PipelineError("Duplicate term in curated batch")
    observations = []
    updates = []
    for item in incoming:
        tid = item.get("term_id")
        if tid not in terms:
            raise PipelineError("Review not in sealed Stage 2 inventory: "+str(tid))
        term, attempt = terms[tid], attempts[tid]
        row = by_id[tid]
        if row["decision"] not in ("needs_review",item.get("decision")):
            raise PipelineError("Cannot overwrite a conflicting prior review disposition")
        if attempt["outcome"] not in CONTENT_VISITED:
            raise PipelineError("Cannot review blocked or unread source as if accessed: "+tid)
        decision = item.get("decision")
        if decision not in ("supported", "no_suitable_definition"):
            raise PipelineError("Batch must give a substantive editorial disposition")
        reviewer = item.get("reviewed_by")
        if not isinstance(reviewer,str) or len(reviewer)<8 or reviewer=="automatic_access_check":
            raise PipelineError("Reviewer attribution missing")
        reason = item.get("editorial_reason","")
        if not isinstance(reason,str) or len(reason.strip())<65:
            raise PipelineError("Document the examined source and mathematical rationale (65+ chars)")
        newrow=dict(row)
        newrow.update({"decision":decision,"reviewed_by":reviewer,
                       "editorial_reason":reason,"human_verified":False})
        newrow["source_research_recorded"]=True
        newrow["review_scope"]="source_section_mathematical_content"
        if decision=="no_suitable_definition":
            if item.get("definitions"):
                raise PipelineError("No-definition decision contains candidate definitions")
            newrow.pop("evidence_ids",None)
        else:
            defs = item.get("definitions")
            if not isinstance(defs,list) or not defs:
                raise PipelineError("Supported term must have >=1 independently authored definition")
            ids=[]
            for d in defs:
                key=d.get("key","")
                if not isinstance(key,str) or not re.fullmatch(r"[a-z][a-z0-9_-]{2,64}",key):
                    raise PipelineError("Every definition variant requires a stable key")
                section=d.get("source_section","")
                text=d.get("text","")
                context=d.get("context_hint","")
                if not all(isinstance(x,str) for x in (section,text,context)) or len(section)<6 or len(text)<45 or len(context)<6:
                    raise PipelineError("Incomplete mathematical definition, context or source section")
                # All proof/source references must stay in the reviewed source collection.
                locator=d.get("source_locator",term["locator"])
                safe_source_url(locator,sources[term["source_id"]])
                if locator != term["locator"]:
                    raise PipelineError("Current stage requires term-specific reviewed source URL")
                if term["source_id"]!="src.stacks":
                    raise PipelineError("This source has not been permitted for accessible mathematical review")
                obsid="obs.recovery."+tid.removeprefix("term.")+"."+key.replace("_","-")
                obs={"id":obsid,"term_id":tid,"source_id":term["source_id"],
                     "locator":locator,"record_kind":"paraphrase",
                     "text":text,"source_section":section,"context_hint":context,
                     "review_state":"candidate","confidence":"source_checked",
                     "discovery_method":"independent.source_reading.recovery",
                     "reviewed_by":reviewer,
                     "reproduction_policy":"independently authored paraphrase; no source passage copied",
                     "human_verified":False}
                w.validate("observations",obs)
                if obsid in existing and canonical(existing[obsid])!=canonical(obs):
                    raise PipelineError("Cannot overwrite previously recorded definition: "+obsid)
                if any(v["id"]==obsid for v in observations):
                    raise PipelineError("Duplicate candidate definition stable ID")
                observations.append(obs)
                ids.append(obsid)
            newrow["evidence_ids"]=ids
        updates.append(newrow)
    changed={r["term_id"]:r for r in updates}
    # Idempotent and conflict-checked observation appends; no partial review
    # ledger updates occur until ALL candidate source observations are ingested.
    if check_only:
        return {"terms_in_batch":len(incoming),"authored_formulations":len(observations),
                "existing_reviews":len(reviews),"checked":True}
    temp=w.root/"state/.stage3_review_observation_input.jsonl"
    temp.write_text("".join(canonical(x)+"\n" for x in observations),encoding="utf-8")
    try:
        if observations:
            result=w.ingest("observations",temp,batch_size=10)
        else:
            result={"added":0,"already_present":0}
    finally:
        temp.unlink(missing_ok=True)
    updated=[changed.get(row["term_id"],row) for row in reviews]
    # Current existing rows can still contain needs_review; do not run the final
    # all-terms gate until the entire queue has actually been researched.
    checkpath=w.root/"state/.stage3_review_batch_tmp.jsonl"
    checkpath.write_text("".join(canonical(row)+"\n" for row in updated),encoding="utf-8")
    checkpath.replace(reviews_path)
    tally={}
    for row in updated:tally[row["decision"]]=tally.get(row["decision"],0)+1
    atomic_json(w.root/"state/stage3_review_progress.json",{
        "schema_version":1,"terms_total":len(reviews),"decisions":tally,
        "authored_observation_records":len(w.records("observations")),
        "last_batch":str(batch_path),"stage3_sealed":False,
        "mathematical_research_done":tally.get("needs_review",0)==0,
    })
    return {"terms_reviewed_in_batch":len(incoming),"new_observations":result["added"],
            "observations_already_present":result["already_present"],"progress":tally}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace",type=Path,required=True)
    p.add_argument("--batch",type=Path,required=True)
    p.add_argument("--check-only",action="store_true")
    args=p.parse_args()
    print(json.dumps(apply(args.workspace,args.batch,check_only=args.check_only),indent=2))


if __name__=="__main__":
    main()
