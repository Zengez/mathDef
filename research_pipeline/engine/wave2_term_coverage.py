"""Validate per-term Wave 2 source/review coverage without rewriting the Wave 1 ledgers.

Inherited Wave 1 decisions remain supported, source-limited, or access-blocked
according to their *sealed* individual records. New Wave 2 terms are only
source-read candidates or unresolved index leads; neither is silently
upgraded into a screened or human-verified meaning.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path

from .core import Workspace, PipelineError, atomic_json, canonical, digest, jsonl

BASELINE_DISPOSITIONS = {"supported", "no_suitable_definition", "access_blocked"}
WAVE2_DISPOSITIONS = {"source_read_candidate", "unverified_source_locator"}


def build(wave1, wave2):
    first = Workspace(wave1)
    second = Workspace(wave2)
    frozen_file = first.root / "state/wave1_freeze.json"
    baseline_file = second.root / "state/baseline.json"
    if not frozen_file.exists() or not baseline_file.exists():
        raise PipelineError("Required frozen independent Wave 1 / forked Wave 2 baseline missing")
    freeze = json.loads(frozen_file.read_text(encoding="utf-8"))
    baseline = json.loads(baseline_file.read_text(encoding="utf-8"))
    if freeze.get("state") != "FROZEN" or baseline.get("mode") != "second_wave":
        raise PipelineError("Wave 2 lineage is invalid")
    if freeze["published_catalog_digest"] != digest(first.publication()):
        raise PipelineError("Wave 1 publication does not match its frozen snapshot")
    if freeze["published_catalog_digest"] != baseline["first_wave_digest"]:
        raise PipelineError("Wave 2 was not forked from the verified frozen publication")

    original_terms, expanded_terms = first.records("terms"), second.records("terms")
    original_observations = first.records("observations")
    new_observations = second.records("observations")
    for tid, record in original_terms.items():
        if expanded_terms.get(tid) != record:
            raise PipelineError("Wave 1 inherited term changed: " + tid)
    for oid, record in original_observations.items():
        if new_observations.get(oid) != record:
            raise PipelineError("Wave 1 inherited observation changed: " + oid)

    original_reviews = jsonl(first.root / "state/stage3_term_reviews.jsonl")
    original_attempts = jsonl(first.root / "state/stage3_acquisition_attempts.jsonl")
    if len(original_reviews) != 318 or len(original_attempts) != 318:
        raise PipelineError("Frozen Wave 1 individual review coverage incomplete")
    from .stage3_review_gate import require_reviewed_term_dispositions
    require_reviewed_term_dispositions(first.root, first.root / "state/stage3_term_reviews.jsonl")
    reviews = {r["term_id"]: r for r in original_reviews}
    attempts = {a["term_id"]: a for a in original_attempts}
    if len(reviews) != len(original_terms) or len(attempts) != len(original_terms):
        raise PipelineError("Inherited review IDs inconsistent with frozen source terms")

    output = []
    for tid, term in sorted(original_terms.items()):
        review, attempt = reviews[tid], attempts[tid]
        if review["decision"] not in BASELINE_DISPOSITIONS:
            raise PipelineError("Unsupported inherited review status: " + tid)
        if (review["label"], review["locator"], review["source_id"]) != (
                term["label"],term["locator"],term["source_id"]):
            raise PipelineError("Inherited source review no longer matches its source term")
        if attempt["term_id"] != tid or attempt["outcome"] != review["attempt_outcome"]:
            raise PipelineError("Original attempt and review diverge: " + tid)
        output.append({
            "term_id":tid,"label":term["label"],"source_id":term["source_id"],
            "locator":term["locator"],"disposition":"inherited_"+review["decision"],
            "provenance":"Wave 1 individual review and acquisition ledgers",
            "original_review_digest":digest(review),
            "original_attempt_digest":digest(attempt),
            "mathematical_observation_ids":review.get("evidence_ids",[]),
            "source_access_verified":attempt["page_fetched"] is True,
            "source_research_complete":review["decision"] != "access_blocked",
            "mathematically_screened_in_wave2":False,
            "human_verified":False
        })

    leads1 = jsonl(second.root / "wave2/foundation_source_discovery_batch_01.jsonl")
    leads2 = jsonl(second.root / "wave2/foundation_source_discovery_batch_02.jsonl")
    leads3 = jsonl(second.root / "wave2/foundation_source_discovery_batch_03.jsonl")
    fourth_path=second.root / "wave2/foundation_source_discovery_batch_04.jsonl"
    leads4=jsonl(fourth_path) if fourth_path.exists() else []
    fifth_path=second.root / "wave2/foundation_source_discovery_batch_05.jsonl"
    leads5=jsonl(fifth_path) if fifth_path.exists() else []
    sixth_path=second.root / "wave2/foundation_source_discovery_batch_06.jsonl"
    leads6=jsonl(sixth_path) if sixth_path.exists() else []
    eighth_path=second.root / "wave2/foundation_source_discovery_batch_08.jsonl"
    leads8=jsonl(eighth_path) if eighth_path.exists() else []
    ninth_path=second.root / "wave2/foundation_source_discovery_batch_09.jsonl"
    leads9=jsonl(ninth_path) if ninth_path.exists() else []
    eleventh_path=second.root / "wave2/foundation_source_discovery_batch_11.jsonl"
    leads11=jsonl(eleventh_path) if eleventh_path.exists() else []
    added={t:record for t,record in expanded_terms.items() if t not in original_terms}
    if (len(added)!=18+len(leads4)+len(leads5)+len(leads6)+len(leads8)+len(leads9)+len(leads11) or len(leads1)!=9 or len(leads2)!=6 or len(leads3)!=3 or len(leads4) not in (0,3) or len(leads5) not in (0,4) or len(leads6) not in (0,4) or len(leads8) not in (0,3) or len(leads9) not in (0,4) or len(leads11) not in (0,2)):
        raise PipelineError("New term/source discovery coverage mismatch")
    in_leads={}
    for lead in leads1+leads2+leads3+leads4+leads5+leads6+leads8+leads9+leads11:
        tid=lead["term_id"]
        if tid in in_leads or tid not in added:
            raise PipelineError("Source lead duplicates/does not name a new term: "+tid)
        in_leads[tid]=lead
    if set(in_leads)!=set(added):
        raise PipelineError("Not every newly added term has an individual source lead")
    for tid,term in sorted(added.items()):
        lead=in_leads[tid]
        url=lead.get("url",lead.get("locator"))
        if (lead["source_id"],url)!=(term["source_id"],term["locator"]):
            raise PipelineError("Wave 2 source lead does not match term: "+tid)
        direct=lead["source_access_outcome"]=="direct_page_read"
        if not direct and lead["source_access_outcome"] not in (
                "indexed_only_not_directly_verified","direct_fetch_failed_502"):
            raise PipelineError("New source access state not recognized")
        candidates=[x["id"] for x in new_observations.values()
                    if x["term_id"]==tid and x["record_kind"]=="paraphrase"]
        if direct and len(candidates)!=1:
            raise PipelineError("Directly reviewed source missing exactly one candidate: "+tid)
        if not direct and candidates:
            raise PipelineError("Unverified source page gained unsupported evidence: "+tid)
        output.append({
            "term_id":tid,"label":term["label"],"source_id":term["source_id"],
            "locator":term["locator"],
            "disposition":"source_read_candidate" if direct else "unverified_source_locator",
            "source_access_outcome":lead["source_access_outcome"],
            "provenance":(
                "wave2/foundation_source_discovery_batch_11.jsonl" if lead in leads11 else
                "wave2/foundation_source_discovery_batch_09.jsonl" if lead in leads9 else
                "wave2/foundation_source_discovery_batch_08.jsonl" if lead in leads8 else
                "wave2/foundation_source_discovery_batch_06.jsonl" if lead in leads6 else
                "wave2/foundation_source_discovery_batch_05.jsonl" if lead in leads5 else
                "wave2/foundation_source_discovery_batch_04.jsonl" if lead in leads4 else
                "wave2/foundation_source_discovery_batch_03.jsonl" if lead in leads3 else
                "wave2/foundation_source_discovery_batch_02.jsonl" if lead in leads2 else
                "wave2/foundation_source_discovery_batch_01.jsonl"),
            "source_research_complete":direct,
            "mathematical_observation_ids":candidates,
            "mathematically_screened_in_wave2":False,
            "human_verified":False
        })
    output.sort(key=lambda x:x["term_id"])
    counter=Counter(x["disposition"] for x in output)
    expected={"inherited_supported":232,"inherited_no_suitable_definition":59,
              "inherited_access_blocked":27,"source_read_candidate":10+len(leads4)+len(leads5)+len(leads6)+len(leads8)+len(leads9)+len(leads11),
              "unverified_source_locator":8}
    if dict(counter)!=expected or len(output)!=len(expanded_terms) or len(output)!=336+len(leads4)+len(leads5)+len(leads6)+len(leads8)+len(leads9)+len(leads11):
        raise PipelineError("Unexpected source coverage; do not seal: "+str(counter))
    existing=second.root/"state/wave2_term_coverage.jsonl"
    content="".join(canonical(row)+"\n" for row in output)
    archival=False
    if existing.exists() and existing.read_text(encoding="utf-8")!=content:
        old_content=existing.read_text(encoding="utf-8")
        old_rows=jsonl(existing)
        old_by_id={r["term_id"]:r for r in old_rows}
        new_by_id={r["term_id"]:r for r in output}
        if len(old_by_id)!=len(old_rows) or not set(old_by_id).issubset(new_by_id):
            raise PipelineError("Previous source review ledger has duplicated/deleted term identity")
        for tid,prior in old_by_id.items():
            if new_by_id[tid]!=prior:
                raise PipelineError("Existing individual source decision changed without revision: "+tid)
        prior_json=second.root/"state/wave2_term_coverage.json"
        if not prior_json.exists():
            raise PipelineError("Previous source ledger has no proof/metadata to archive")
        prior_report=json.loads(prior_json.read_text(encoding="utf-8"))
        if (prior_report.get("term_count")!=len(old_rows) or
                prior_report.get("source_review_ledger_sha256")!=
                   hashlib.sha256(old_content.encode("utf-8")).hexdigest()):
            raise PipelineError("Stale existing Wave 2 source review digest")
        history_file=second.root/f"state/wave2_term_coverage_snapshot_{len(old_rows)}.jsonl"
        history_report=second.root/f"state/wave2_term_coverage_snapshot_{len(old_rows)}.json"
        if len(old_rows) not in (333,336,339,343,347,350,354):
            raise PipelineError("Unexpected review history revision; require explicit versioning")
        if history_file.exists() and history_file.read_text(encoding="utf-8")!=old_content:
            raise PipelineError("Conflicting historical source coverage snapshot")
        if history_report.exists() and json.loads(history_report.read_text())!=prior_report:
            raise PipelineError("Conflicting historical source coverage report")
        history_file.write_text(old_content,encoding="utf-8")
        atomic_json(history_report,prior_report)
        archival=True
    existing.write_text(content,encoding="utf-8")
    summary={
      "phase":"Wave 2 expanded per-term source review coverage",
      "term_count":len(output),
      "inherited_frozen_reviews_checked":318,
      "source_read_new_candidates":10+len(leads4)+len(leads5)+len(leads6)+len(leads8)+len(leads9)+len(leads11),
      "new_source_locators_unverified":8,
      "new_term_review_coverage":18+len(leads4)+len(leads5)+len(leads6)+len(leads8)+len(leads9)+len(leads11),
      "dispositions":dict(counter),
      "pending_new_direct_source_reviews":8,
      "mathematical_candidate_meanings_screened":second.state("meanings").get("screened_new_formulations",0),
      "complete_for_wave2_sealing":False,
      "must_research_all_unverified_source_locators":True,
      "inherited_blocked_sources_remain_unresolved":27,
      "previous_333_term_review_ledger_archived":(second.root/"state/wave2_term_coverage_snapshot_333.jsonl").exists(),
      "previous_336_term_review_ledger_archived":(second.root/"state/wave2_term_coverage_snapshot_336.jsonl").exists(),
      "previous_339_term_review_ledger_archived":(second.root/"state/wave2_term_coverage_snapshot_339.jsonl").exists(),
      "previous_343_term_review_ledger_archived":(second.root/"state/wave2_term_coverage_snapshot_343.jsonl").exists(),
      "previous_347_term_review_ledger_archived":(second.root/"state/wave2_term_coverage_snapshot_347.jsonl").exists(),
      "previous_350_term_review_ledger_archived":(second.root/"state/wave2_term_coverage_snapshot_350.jsonl").exists(),
      "previous_354_term_review_ledger_archived":(second.root/"state/wave2_term_coverage_snapshot_354.jsonl").exists(),
      "source_review_ledger_sha256":hashlib.sha256(content.encode("utf-8")).hexdigest(),
      "frozen_wave1_catalog_digest":freeze["published_catalog_digest"],
      "original_production_mathdef_consulted":False,
      "next":"Finish new-source verification and cross-source evidence, then explicitly screen new meaning variants and relations before any stage can be sealed."
    }
    atomic_json(second.root/"state/wave2_term_coverage.json",summary)
    return summary


def require_wave2_review_complete(root):
    workspace=Workspace(root)
    file=workspace.root/"state/wave2_term_coverage.json"
    if not file.exists():
        raise PipelineError("Wave 2 cannot seal: missing per-term review coverage")
    report=json.loads(file.read_text(encoding="utf-8"))
    current={x["term_id"] for x in jsonl(workspace.root/"state/wave2_term_coverage.jsonl")}
    if current!=set(workspace.records("terms")):
        raise PipelineError("Wave 2 cannot seal: reviewed term IDs do not equal actual term catalog")
    if report["pending_new_direct_source_reviews"] or not report["complete_for_wave2_sealing"]:
        raise PipelineError("Wave 2 cannot seal: unverified source leads or candidate meanings remain")
    return report


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wave1",required=True,type=Path)
    ap.add_argument("--wave2",required=True,type=Path)
    ap.add_argument("--verify-only",action="store_true")
    args=ap.parse_args()
    print(json.dumps(require_wave2_review_complete(args.wave2) if args.verify_only else
         build(args.wave1,args.wave2),indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
