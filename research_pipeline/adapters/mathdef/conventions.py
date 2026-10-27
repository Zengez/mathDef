"""Interpret source conventions separately from mathDef's own canonical meanings.

Operational inheritance is dynamic: checked_inconclusive and verified_opposite
resolve against the current merged catalog, never a frozen historic predicate.
No new source searches or correction/reputation scoring occur here.
"""
from __future__ import annotations

import json
from pathlib import Path


VALID_STATUS = frozenset({
    "not_checked", "verified_applies", "verified_opposite",
    "checked_inconclusive", "conflicting_scopes",
})
INHERITING = frozenset({"not_checked", "verified_opposite", "checked_inconclusive"})
SCOPE_PRIORITY = {"work": 1, "chapter": 2, "section": 3, "local": 4}


class ConventionError(ValueError):
    pass


def read_conventions(repo: Path, catalog: dict) -> tuple[dict, list[dict]]:
    """Validate the convention catalog and the separate evidence ledger."""
    root = Path(repo) / "data"
    conventions = json.loads((root / "math_definition_conventions.json").read_text(encoding="utf-8"))
    assessments = json.loads((root / "math_source_convention_assessments.json").read_text(encoding="utf-8"))
    if conventions.get("schema_version") != 1 or assessments.get("schema_version") != 1:
        raise ConventionError("Unsupported convention data schema")
    meanings = {m["id"]: m for g in catalog["groups"] for m in g["meanings"]}
    by_id = {}
    for record in conventions["entries"]:
        cid = record["convention_id"]
        mid = record["canonical_meaning_id"]
        if cid in by_id or mid not in meanings:
            raise ConventionError("Duplicate convention ID or missing current canonical meaning: " + cid)
        if not record.get("concept_id") or not record.get("note"):
            raise ConventionError("Incomplete convention catalog entry: " + cid)
        by_id[cid] = record
    assessments_by_id = set()
    for a in assessments["assessments"]:
        aid, cid, status = a["assessment_id"], a["convention_id"], a["status"]
        if aid in assessments_by_id or cid not in by_id or status not in VALID_STATUS:
            raise ConventionError("Duplicate, unknown or invalid source assessment: " + aid)
        assessments_by_id.add(aid)
        if not a.get("source_url", "").startswith("https://"):
            raise ConventionError("Missing source URL for " + aid)
        scope = a.get("scope") or {}
        if scope.get("kind") not in SCOPE_PRIORITY:
            raise ConventionError("Source assessment requires exact scope: " + aid)
        if status == "verified_applies":
            if not (a.get("explicit_source_restriction") and a.get("evidence_url")
                    and a.get("evidence_locator")):
                raise ConventionError("Positive source restriction requires evidence: " + aid)
        elif status in INHERITING:
            if a.get("explicit_source_restriction"):
                raise ConventionError("Canonical-inheriting status cannot freeze restriction: " + aid)
            if status == "verified_opposite" and not a.get("evidence_url"):
                raise ConventionError("Verified-opposite assessment requires evidence: " + aid)
            if status == "checked_inconclusive" and not a.get("checked_on"):
                raise ConventionError("Inconclusive status requires actual documented check: " + aid)
    return by_id, assessments["assessments"]


def effective_interpretation(
    convention: dict, catalog: dict, assessment: dict | None = None,
) -> dict:
    """Resolve the *latest* canonical meaning; never cache a source reading.

    If no assessment exists, do NOT record an imaginary checked source; return
    not_checked and mathDef editorial default without source attribution.
    """
    cid = convention["convention_id"]
    mid = convention["canonical_meaning_id"]
    current = next((m for g in catalog["groups"] for m in g["meanings"]
                    if m["id"] == mid), None)
    if current is None:
        raise ConventionError("Canonical meaning is missing: " + mid)
    status = assessment["status"] if assessment else "not_checked"
    output = {
        "convention_id": cid,
        "canonical_concept_id": convention["concept_id"],
        "current_canonical_meaning_id": mid,
        "status": status,
        "source_endorses_default": bool(status == "verified_opposite"),
        "assessment_id": assessment["assessment_id"] if assessment else None,
    }
    # A verified rejection of one specific restriction is not proof the author
    # explicitly endorses all future canonical extensions. Keep attribution
    # scoped to the evidence, never claim agreement with all of mathDef.
    output["source_endorses_default"] = False
    if status in INHERITING:
        output["effective_interpretation"] = "inherit_current_mathdef_canonical"
        output["current_formulation_ids"] = [f["id"] for f in current["formulations"]]
        output["author_agreement_verified"] = False
        output["restriction"] = None
    elif status == "verified_applies":
        output["effective_interpretation"] = "verified_source_restriction"
        output["restriction"] = assessment["explicit_source_restriction"]
        output["applicable_scope"] = assessment["scope"]
    else:
        output["effective_interpretation"] = "requires_scoped_review"
        output["restriction"] = None
    return output


def assessments_for_source(url: str, records: list[dict],
                           *, convention_id: str | None = None,
                           applicable_scopes: set[str] | None = None) -> list[dict]:
    """Look up source-specific evidence, not rules inferred from the hostname.

    For conflicting records, the caller may explicitly supply source scope(s);
    otherwise return the collection without pretending a globally valid choice.
    """
    candidates = [x for x in records if x["source_url"] == url
                  and (convention_id is None or x["convention_id"] == convention_id)]
    if applicable_scopes is not None:
        candidates = [a for a in candidates
                      if a["scope"]["kind"] == "work"
                      or a["scope"]["locator"] in applicable_scopes
                      or a["scope"]["name"] in applicable_scopes]
    return sorted(candidates, key=lambda a: (
        -SCOPE_PRIORITY[a["scope"]["kind"]], a["assessment_id"]
    ))


def resolved_source_assessments(repo: Path, catalog: dict,
                                url: str) -> list[dict]:
    conventions, records = read_conventions(repo, catalog)
    return [{
        **{k: v for k, v in a.items() if k != "explicit_source_restriction"},
        **effective_interpretation(conventions[a["convention_id"]], catalog, a)
    } for a in assessments_for_source(url, records)]
