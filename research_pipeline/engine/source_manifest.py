"""Make bounded, rights-aware index-page task manifests from approved sources.

Source metadata may provide index_pages [{url, profile, html_path}], or
index_urls [URL,...]. Otherwise use the canonical source URL. A saved XML
sitemap may be supplied independently; this script never fetches the sitemap.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

from .core import PipelineError, Workspace, canonical
from .source_intake import safe_url


def generate(workspace, *, source_ids=None, sitemap_xml=None, sitemap_source_id=None,
             max_pages=250):
    w = Workspace(workspace)
    w.config()
    if not 1 <= max_pages <= 3000:
        raise PipelineError("max_pages must be between 1 and 3000")
    registry = w.records("sources")
    approved = {}
    for key, source in registry.items():
        if source_ids is not None and key not in source_ids:
            continue
        if (source["authority_reviewed"] and source["access"] == "free"
                and source["rights"] in ("permitted", "locator_only")):
            approved[key] = source
    if sitemap_xml and sitemap_source_id not in approved:
        raise PipelineError("A sitemap must be assigned to a registered, approved source")
    tasks = {}
    for source_id, source in approved.items():
        host = safe_url(source["url"]).hostname
        pages = source.get("index_pages") or [{"url": x} for x in source.get("index_urls", [])]
        if not pages:
            pages = [{"url": source["url"]}]
        if not isinstance(pages, list):
            raise PipelineError("index_pages must be an array")
        for page in pages:
            if not isinstance(page, dict) or not isinstance(page.get("url"), str):
                raise PipelineError("Invalid index_pages entry")
            safe_url(page["url"], host)
            profile = page.get("profile", source.get("index_profile", "headings"))
            if profile not in ("headings", "glossary", "linked-list"):
                raise PipelineError("Unknown index parser profile")
            row = {"source_id": source_id, "url": page["url"], "profile": profile}
            if page.get("html_path"):
                row["html_path"] = page["html_path"]
            row["id"] = "page." + hashlib.sha256(
                (source_id + "|" + row["url"] + "|" + profile).encode("utf-8")
            ).hexdigest()[:16]
            tasks[row["id"]] = row
    if sitemap_xml:
        raw = Path(sitemap_xml).read_bytes()
        if len(raw) > 2_000_000 or b"<!DOCTYPE" in raw or b"<!ENTITY" in raw:
            raise PipelineError("Unsafe or oversized sitemap XML")
        try:
            tree = ET.fromstring(raw)
        except ET.ParseError as exc:
            raise PipelineError("Malformed sitemap") from exc
        host = safe_url(approved[sitemap_source_id]["url"]).hostname
        profile = approved[sitemap_source_id].get("index_profile", "headings")
        for element in tree.iter():
            if element.tag.split("}")[-1] != "loc" or not element.text:
                continue
            url = element.text.strip()
            if urllib.parse.urlparse(url).path.lower().endswith(".xml"):
                continue  # a sitemapindex URL is not itself an HTML article
            try:
                safe_url(url, host)
            except PipelineError:
                continue
            row = {"source_id": sitemap_source_id, "url": url, "profile": profile}
            row["id"] = "page." + hashlib.sha256(
                (sitemap_source_id + "|" + url + "|" + profile).encode("utf-8")
            ).hexdigest()[:16]
            tasks[row["id"]] = row
            if len(tasks) >= max_pages:
                break
    return sorted(tasks.values(), key=lambda x: (x["source_id"], x["url"]))[:max_pages]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--source-ids", nargs="*")
    p.add_argument("--sitemap-xml", type=Path)
    p.add_argument("--sitemap-source-id")
    p.add_argument("--max-pages", type=int, default=250)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    manifest = generate(args.workspace, source_ids=args.source_ids,
                        sitemap_xml=args.sitemap_xml, sitemap_source_id=args.sitemap_source_id,
                        max_pages=args.max_pages)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(canonical(x) + "\n" for x in manifest), encoding="utf-8")
    print(json.dumps({"pages": len(manifest), "output": str(args.output),
                      "next": "Review source list, then run the batch intake reader."}))


if __name__ == "__main__":
    main()
