"""Source-by-source Stage 3 recovery: a real document attempt for EVERY sealed term.

No original mathDef corpus reads, no copied mathematical source passages, and
no false "definition located" claims from a Stage 2 URL alone. A robot-policy
block or failed retrieval has a distinct outcome and still requires follow-up.
The ledger is deliberately independent of the historically sealed Stage 3/4.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

from .core import PipelineError, Workspace, atomic_json, canonical, digest, jsonl
from .source_intake import fetch_index, safe_source_url

TERMINAL = frozenset({
    "definition_markers_found", "page_read_no_definition_marker",
    "page_heading_mismatch", "policy_blocked", "fetch_failed_after_retries"
})
CONTENT_VISITED = frozenset({
    "definition_markers_found", "page_read_no_definition_marker",
    "page_heading_mismatch"
})
FETCH_RETRIES = 2
MAX_BATCH = 60


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class StacksDefinitionIndex(HTMLParser):
    """Inspect structural definition markers in one Stacks section, not prose.

    A tag/reference to a Definition is a *candidate lead*, NOT evidence that
    the definition actually defines the section's title. Human/AI mathematical
    interpretation and independently drafted paraphrases remain separate.
    """
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.in_heading = False
        self.anchor = None
        self.titles = []
        self.headings = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag in ("h1", "h2"):
            self.in_heading = True
        if tag == "a":
            self.anchor = {"href": attrs.get("href", ""), "words": []}

    def handle_data(self, data):
        if self.in_title:
            self.titles.append(data)
        if self.in_heading:
            self.headings.append(data)
        if self.anchor is not None:
            self.anchor["words"].append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag in ("h1", "h2"):
            self.in_heading = False
            self.headings.append(" ")
        if tag == "a" and self.anchor is not None:
            label = " ".join("".join(self.anchor["words"]).split())
            if re.fullmatch(r"Definition\s+\d+(?:\.\d+){2}\.?", label):
                self.links.append((label.rstrip("."), self.anchor["href"]))
            self.anchor = None


def inspect_stacks_page(html_text, term):
    parser = StacksDefinitionIndex()
    parser.feed(html_text)
    title = " ".join("".join(parser.titles).split())
    match = re.search(r"Section\s+(\d+\.\d+)\s+\([0-9A-Z]{4}\):\s*(.*?)\s*[—–-]\s*The Stacks", title)
    if not match:
        return {"status": "page_heading_mismatch", "page_title": title[:180],
                "definition_candidates": [], "reason": "Not a recognized Stacks section title"}
    section, heading = match.groups()
    norm = lambda value: " ".join(re.findall(r"[a-z0-9]+", value.casefold()))
    if norm(heading) != norm(term["label"]):
        return {"status": "page_heading_mismatch",
                "page_title": title[:180], "page_section": section,
                "definition_candidates": [], "reason": "Term label does not match source page heading"}
    prefix = "Definition " + section + "."
    found = {}
    for label, href in parser.links:
        if not label.startswith(prefix):
            continue
        match_id = re.fullmatch(r"Definition\s+(\d+\.\d+\.\d+)", label)
        if match_id:
            found[match_id.group(1)] = {"marker": label, "section_number": match_id.group(1)}
    markers = [found[x] for x in sorted(found, key=lambda s: tuple(map(int,s.split("."))))]
    return {
        "status": "definition_markers_found" if markers else "page_read_no_definition_marker",
        "page_title": title[:180], "page_section": section,
        "definition_candidates": markers[:80],
        "definition_marker_count": len(markers),
        "reason": "Structural definition-marker leads only; precise mathematical contents require review"
    }


def catalog_digest(w):
    return digest(list(w.records("terms").values()))


def validate_ledger(w, ledger):
    """Reject ghost terms, stale source catalogs and counterfeit source attempts."""
    terms = w.records("terms")
    source_map = w.records("sources")
    expected = catalog_digest(w)
    seen = set()
    for row in ledger:
        tid = row.get("term_id")
        if tid in seen or tid not in terms:
            raise PipelineError("Duplicate or unknown Stage 3 attempt term ID: " + str(tid))
        seen.add(tid)
        term = terms[tid]
        if (row.get("source_id"), row.get("locator"), row.get("label")) != (
                term["source_id"], term["locator"], term["label"]):
            raise PipelineError("Attempt does not identify the sealed term: " + tid)
        if row.get("term_catalog_digest") != expected:
            raise PipelineError("Attempt belongs to a different sealed term catalog")
        safe_source_url(row["locator"], source_map[row["source_id"]])
        if row.get("outcome") not in TERMINAL | {"retryable_fetch_error"}:
            raise PipelineError("Unknown attempt outcome")
        attempts = row.get("attempt_count", 0)
        if not isinstance(attempts, int) or attempts < 1 or attempts > FETCH_RETRIES:
            raise PipelineError("Invalid number of acquisition attempts")
        fetched = row.get("page_fetched") is True
        if row["outcome"] in CONTENT_VISITED and not fetched:
            raise PipelineError("Source-read outcome without actual fetched page")
        if row["outcome"] not in CONTENT_VISITED and fetched:
            raise PipelineError("Policy/fetch failure inaccurately marked as fetched")
        if row["outcome"] == "definition_markers_found" and (
                not row.get("definition_candidates") or not row.get("page_content_sha256")):
            raise PipelineError("Definition marker outcome lacks inspected-page evidence")
        if row["outcome"] == "page_read_no_definition_marker" and row.get("definition_candidates"):
            raise PipelineError("No-marker outcome contains markers")
        if row.get("human_verified") is not False:
            raise PipelineError("Automated source acquisition cannot assert human review")
    return {row["term_id"]: row for row in ledger}


def summarize(w, ledger):
    terms = w.records("terms")
    statuses = Counter(row["outcome"] for row in ledger)
    accounted = sum(statuses.get(x,0) for x in TERMINAL)
    content_read = sum(statuses.get(x,0) for x in CONTENT_VISITED)
    not_accounted = sorted(set(terms) - {r["term_id"] for r in ledger if r["outcome"] in TERMINAL})
    restricted = [r["term_id"] for r in ledger if r["outcome"] == "policy_blocked"]
    failed = [r["term_id"] for r in ledger if r["outcome"] == "fetch_failed_after_retries"]
    return {
        "schema_version": 1, "stage": "stage3_recovery_attempt_coverage",
        "term_catalog_digest": catalog_digest(w),
        "source_terms_total": len(terms), "records_in_ledger": len(ledger),
        "attempts_accounted_for": accounted, "source_documents_fetched": content_read,
        "definition_marker_leads": statuses.get("definition_markers_found", 0),
        "no_explicit_definition_marker": statuses.get("page_read_no_definition_marker", 0),
        "heading_mismatch": statuses.get("page_heading_mismatch", 0),
        "policy_blocked": len(restricted),
        "fetch_failed_after_retries": len(failed),
        "retryable_fetch_errors": statuses.get("retryable_fetch_error", 0),
        "pending_term_ids": not_accounted,
        "policy_blocked_term_ids": restricted,
        "failed_term_ids": failed,
        "every_term_attempt_accounted_for": not not_accounted,
        "research_scope_complete": False,
        "reason_research_scope_not_complete": (
            "A completed acquisition attempt is not equivalent to a verified definition. "
            "Policy-blocked, unreachable, mismatch and no-marker terms require follow-up."),
        "no_unlicensed_source_text_stored": True,
    }


def require_full_attempt_coverage(workspace, ledger_path):
    """Gate: every sealed term received a real attempt or explicit access failure.

    Access failure is accounted for, NEVER called successful mathematical research.
    A resumed 'retryable_fetch_error' or missing row prevents advancement.
    """
    w = Workspace(workspace)
    rows = jsonl(ledger_path)
    checked = validate_ledger(w, rows)
    audit = summarize(w, rows)
    if len(checked) != len(w.records("terms")) or not audit["every_term_attempt_accounted_for"]:
        raise PipelineError(
            "Stage 3 cannot advance: only %s/%s terms have terminal attempts" %
            (audit["attempts_accounted_for"], audit["source_terms_total"]))
    if audit["retryable_fetch_errors"]:
        raise PipelineError("Stage 3 has retriable fetch failures")
    return audit


def atomic_jsonl(path, records):
    """Crash-safe replacement after each per-term acquisition event."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as out:
        for key in sorted(records):
            out.write(canonical(records[key]) + "\n")
        out.flush()
        os.fsync(out.fileno())
    os.replace(tmp, path)


def run(workspace, ledger_path, report_path, *, batch_size=40, delay=1.5,
        fetcher=fetch_index):
    if not (1 <= batch_size <= MAX_BATCH):
        raise PipelineError("Batch must be between 1 and " + str(MAX_BATCH))
    if delay < 1.25:
        raise PipelineError("Delay below approved minimum")
    w = Workspace(workspace)
    if not w.config().get("external_reference_mode") or not w.state("terms").get("sealed"):
        raise PipelineError("Only the sealed independent Stage 2 term catalog can be processed")
    if w.state("terms").get("record_digest") != catalog_digest(w):
        raise PipelineError("Sealed term catalog digest mismatch; do not run")
    terms = w.records("terms")
    sources = w.records("sources")
    ledger_path, report_path = Path(ledger_path), Path(report_path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    existing = validate_ledger(w, jsonl(ledger_path))
    cache = {}
    processed = 0
    for tid in sorted(terms):
        prior = existing.get(tid)
        if prior and prior["outcome"] in TERMINAL:
            continue
        if processed >= batch_size:
            break
        term = terms[tid]
        source = sources[term["source_id"]]
        attempts = (prior["attempt_count"] if prior else 0) + 1
        record = {
            "schema_version": 1, "term_catalog_digest": catalog_digest(w),
            "term_id": tid, "label": term["label"], "source_id": term["source_id"],
            "locator": term["locator"], "attempt_count": attempts,
            "attempted_at_utc": utc_now(), "page_fetched": False,
            "definition_candidates": [], "human_verified": False,
        }
        try:
            html = fetcher(term["locator"], source, delay=delay, robots_cache=cache)
            record["page_fetched"] = True
            record["page_content_sha256"] = sha256_text(html)
            if term["source_id"] == "src.stacks":
                record.update(inspect_stacks_page(html, term))
            else:
                # A generic page is not automatically a verified mathematical definition.
                record.update({
                    "status": "page_read_no_definition_marker",
                    "reason": "Generic source page was visited; source-specific mathematical extraction required",
                    "definition_candidates": []})
            record["outcome"] = record.pop("status")
        except (OSError, ValueError, UnicodeError) as exc:
            error = str(exc)[:400]
            record["error"] = error
            if "Robots policy" in error or "Not an approved" in error:
                record["outcome"] = "policy_blocked"
            else:
                record["outcome"] = ("fetch_failed_after_retries" if attempts >= FETCH_RETRIES
                                     else "retryable_fetch_error")
        existing[tid] = record
        processed += 1
        # Each completed source check persists before progressing to the next term.
        atomic_jsonl(ledger_path, existing)
        audit = summarize(w, list(existing.values()))
        atomic_json(report_path, audit)
    audit = summarize(w, list(existing.values()))
    atomic_json(report_path, audit)
    return {"processed_this_batch": processed, **{k:v for k,v in audit.items() if not k.endswith("_ids")}}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--ledger", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--batch-size", type=int, default=40)
    p.add_argument("--delay", type=float, default=1.5)
    args = p.parse_args(argv)
    print(json.dumps(run(args.workspace, args.ledger, args.report,
                         batch_size=args.batch_size, delay=args.delay), indent=2))


if __name__ == "__main__":
    main()
