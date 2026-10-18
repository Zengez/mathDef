"""Rights-aware source index and definition-locator discovery.

Offline by default. Reads *only* supplied index HTML; optional web access must
be explicitly enabled for a single approved HTTPS source and allowed by robots.
Stage 2 records titles; Stage 3 records definition locators and, only if a
reuse license is documented, short source excerpts. All entries are CANDIDATES.
No mathematical or source-authority judgment is automated here.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import ipaddress
import json
import re
import time
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from pathlib import Path

from .core import PipelineError, Workspace, canonical

AGENT = "mathDef-independent-research/0.1 (+https://github.com/Zengez/mathDef)"
MAX_BYTES = 2_000_000
MAX_ENTRIES = 3000
TITLE_LIMIT = 180


def fingerprint(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def safe_url(url, host=None):
    p = urllib.parse.urlparse(url)
    if p.scheme != "https" or not p.hostname or p.username or p.password or p.port not in (None, 443):
        raise PipelineError("External documents must use public HTTPS without credentials or custom ports")
    try:
        if not ipaddress.ip_address(p.hostname).is_global:
            raise PipelineError("Private/local IP addresses are not allowed")
    except ValueError:
        if p.hostname in ("localhost", "localhost.localdomain") or p.hostname.endswith(".local"):
            raise PipelineError("Local hostnames are not allowed")
    if host and p.hostname.lower() != host.lower():
        raise PipelineError("Index URL must remain on the reviewed source host")
    return p


def fetch_index(url, source, *, delay=1.25, max_bytes=MAX_BYTES):
    """One opt-in request; domain-restricted redirects; robots checked."""
    target = safe_url(url)
    approved = safe_url(source["url"])
    if target.hostname != approved.hostname:
        raise PipelineError("Cannot fetch an unapproved source host")
    if source["access"] != "free" or source["rights"] not in ("permitted", "locator_only") or not source["authority_reviewed"]:
        raise PipelineError("Not an approved, freely accessible source")
    robots_url = "https://" + target.hostname + "/robots.txt"
    robots = urllib.robotparser.RobotFileParser()
    robots.set_url(robots_url)
    # A denied/unreachable robots check is treated conservatively.
    try:
        robots.read()
    except Exception as exc:
        raise PipelineError("Robots policy could not be retrieved; use permitted offline input") from exc
    if not robots.can_fetch(AGENT, url):
        raise PipelineError("Robots policy does not allow this fetch")
    class RestrictedRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            safe_url(newurl, target.hostname)
            return super().redirect_request(req, fp, code, msg, headers, newurl)
    opener = urllib.request.build_opener(RestrictedRedirect)
    time.sleep(max(0.0, delay))
    req = urllib.request.Request(url, headers={
        "User-Agent": AGENT, "Accept": "text/html",
    })
    with opener.open(req, timeout=30) as response:
        if "text/html" not in response.headers.get("Content-Type", "").lower():
            raise PipelineError("Only HTML index pages are supported")
        final = response.geturl()
        safe_url(final, target.hostname)
        raw = response.read(max_bytes + 1)
        if len(raw) > max_bytes:
            raise PipelineError("Index HTML exceeds size cap")
        charset = response.headers.get_content_charset() or "utf-8"
    return raw.decode(charset, errors="replace")


class IndexReader(HTMLParser):
    """Conservative index reader for headings, glossary labels, or linked lists."""

    def __init__(self, base_url, profile="headings"):
        super().__init__(convert_charrefs=True)
        if profile not in ("headings", "glossary", "linked-list"):
            raise PipelineError("Unknown parser profile")
        self.base_url = base_url
        self.profile = profile
        self.depth = 0
        self.ignore = 0
        self.collect = None
        self.parts = []
        self.href = None
        self.entries = []
        self.pending = None
        self.excerpt_parts = []
        self.capture_paragraph = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style", "noscript", "nav", "footer"):
            self.ignore += 1
        if self.ignore:
            return
        if self.collect is None and (
            (self.profile == "headings" and tag in ("h1", "h2", "h3", "h4")) or
            (self.profile == "glossary" and tag == "dt") or
            (self.profile == "linked-list" and tag == "a" and self.depth > 0)
        ):
            self.collect = tag
            self.parts = []
            self.href = attrs.get("href") if tag == "a" else None
            self.anchor_id = attrs.get("id")
        elif self.collect and tag == "a" and attrs.get("href"):
            self.href = attrs["href"]
        if tag in ("ul", "ol") and self.profile == "linked-list":
            self.depth += 1
        if self.pending is not None and tag in ("p", "dd") and not self.capture_paragraph:
            self.capture_paragraph = True
            self.excerpt_parts = []

    def handle_data(self, data):
        if self.ignore:
            return
        if self.collect is not None:
            self.parts.append(data)
        if self.capture_paragraph:
            self.excerpt_parts.append(data)

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "nav", "footer"):
            self.ignore = max(0, self.ignore - 1)
            return
        if self.ignore:
            return
        if self.collect == tag:
            label = re.sub(r"\s+", " ", html.unescape("".join(self.parts))).strip()
            self.collect = None
            if 2 <= len(label) <= TITLE_LIMIT and not label.isnumeric():
                url = urllib.parse.urljoin(self.base_url, self.href or
                    ("#" + self.anchor_id if self.anchor_id else ""))
                if urllib.parse.urlparse(url).scheme == "https":
                    self.entries.append({"label": label, "url": url, "excerpt": ""})
                    self.pending = len(self.entries) - 1
            self.href = None
        if self.capture_paragraph and tag in ("p", "dd"):
            if self.pending is not None:
                excerpt = re.sub(r"\s+", " ", "".join(self.excerpt_parts)).strip()
                self.entries[self.pending]["excerpt"] = excerpt[:2500]
            self.capture_paragraph = False
            self.excerpt_parts = []
        if tag in ("ul", "ol") and self.profile == "linked-list":
            self.depth = max(0, self.depth - 1)

    def candidates(self, limit=MAX_ENTRIES):
        unique = {}
        for row in self.entries:
            key = (row["label"].casefold(), row["url"])
            unique.setdefault(key, row)
            if len(unique) >= limit:
                break
        return list(unique.values())


def extract(workspace, source_id, url, content, *, stage, profile="headings",
            allow_excerpts=False, limit=MAX_ENTRIES):
    w = Workspace(workspace)
    source = w.records("sources").get(source_id)
    if not source:
        raise PipelineError("Unknown source ID")
    safe_url(url, safe_url(source["url"]).hostname)
    if source["access"] != "free" or source["rights"] not in ("permitted", "locator_only") or not source["authority_reviewed"]:
        raise PipelineError("Source is not eligible for index acquisition")
    if stage not in ("terms", "observations"):
        raise PipelineError("Only terms/observations stages are supported")
    if stage == "observations" and allow_excerpts and (
        source["rights"] != "permitted" or
        not str(source.get("license_url", "")).startswith("https://")
    ):
        raise PipelineError("Licensed excerpts require affirmative permitted rights and an HTTPS license URL")
    parser = IndexReader(url, profile)
    parser.feed(content)
    entries = parser.candidates(limit)
    results = []
    if stage == "terms":
        for item in entries:
            results.append({
                "id": "term." + fingerprint(source_id + "|" + item["url"] + "|" + item["label"].casefold()),
                "label": item["label"], "source_id": source_id,
                "locator": item["url"], "discovery_method": "html." + profile,
            })
    else:
        terms = { (t["source_id"], t["locator"], t["label"].casefold()): t for t in w.records("terms").values() }
        for item in entries:
            term = terms.get((source_id, item["url"], item["label"].casefold()))
            if not term:
                continue
            row = {"id": "obs." + fingerprint(term["id"] + "|" + item["url"]),
                   "term_id": term["id"], "source_id": source_id, "locator": item["url"],
                   "record_kind": "locator", "discovery_method": "html." + profile}
            if allow_excerpts and item["excerpt"]:
                row["record_kind"] = "licensed_excerpt"
                row["text"] = item["excerpt"]
                row["license_url"] = source["license_url"]
            results.append(row)
    return results


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--source-id", required=True)
    p.add_argument("--url", required=True, help="Previously approved HTTPS source index URL")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--html", type=Path, help="Local saved HTML; preferred deterministic mode")
    g.add_argument("--allow-network", action="store_true", help="Explicitly fetch one approved URL")
    p.add_argument("--stage", choices=("terms", "observations"), required=True)
    p.add_argument("--profile", choices=("headings", "glossary", "linked-list"), default="headings")
    p.add_argument("--allow-licensed-excerpts", action="store_true")
    p.add_argument("--limit", type=int, default=MAX_ENTRIES)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args(argv)
    w = Workspace(args.workspace)
    src = w.records("sources").get(args.source_id)
    if not src:
        p.error("Source is not registered")
    if not (1 <= args.limit <= MAX_ENTRIES):
        p.error("limit must be between 1 and 3000")
    if args.html:
        text = args.html.read_text(encoding="utf-8")
        if len(text.encode("utf-8")) > MAX_BYTES:
            p.error("HTML exceeds size cap")
    else:
        text = fetch_index(args.url, src)
    rows = extract(w.root, args.source_id, args.url, text, stage=args.stage,
                   profile=args.profile, allow_excerpts=args.allow_licensed_excerpts,
                   limit=args.limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(canonical(r) + "\n" for r in rows), encoding="utf-8")
    print(json.dumps({"stage": args.stage, "candidates": len(rows),
                      "output": str(args.output), "next": "Review before ingesting",
                      "recommended_thinking": "Instant" if args.stage == "terms" else "Medium"}))


if __name__ == "__main__":
    main()
