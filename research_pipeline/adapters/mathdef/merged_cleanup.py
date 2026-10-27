"""Merged-only semantic cleanup, source registry and mathematical metadata.

This module is deliberately NOT wired into publication yet. It is the staged
pre-link transformation for the approved post-Wave2 cleanup. The final global
linking build must only be enabled AFTER the user's ambiguity review.

Never mutates the original .tex, independently researched records, or the
post-wave historical terms.json research inputs.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from hashlib import sha256

from research_pipeline.adapters.mathdef.conventions import (read_conventions, resolved_source_assessments)
from pathlib import Path
import json


class CleanupError(ValueError):
    """Refuse unclear IDs, context metadata or incorrectly mapped references."""


def _json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _registry(repo: Path, name: str) -> set[str]:
    data = _json(repo / "data" / name)
    if data.get("schema_version") != 1 or not isinstance(data.get("entries"), list):
        raise CleanupError("Invalid registry: " + name)
    labels = [row["name"] for row in data["entries"]]
    if any(not isinstance(s, str) or not s.strip() for s in labels):
        raise CleanupError("Empty label in registry: " + name)
    if len(labels) != len(set(labels)):
        raise CleanupError("Repeated registry label: " + name)
    return set(labels)


def _sid(url: str) -> str:
    """Content-derived stable identity; never strip meaningful tag fragments."""
    return "source.sha256." + sha256(url.strip().encode("utf-8")).hexdigest()[:24]


def _has_external_evidence(citation: dict) -> bool:
    return bool(citation.get("url", "").startswith("https://")) and not (
        "source-file provenance" in str(citation.get("role", "")).lower()
        or "definition provenance" in str(citation.get("role", "")).lower()
        or "github.com/zengez/mathdef/blob/" in citation.get("url", "").lower()
    )


def _source_rank(citation: dict) -> tuple[int, int]:
    """Primary = best available evidence, not a popularity/reliability metric."""
    status = str(citation.get("verification_status") or "")
    role = str(citation.get("role") or "").lower()
    if not _has_external_evidence(citation):
        return (-100, 0)
    if "direct_primary_passage_checked" in status:
        return (6, 0)
    if "direct_source_passage_checked" in status:
        return (5, 0)
    if "source-backed" in role or "supporting evidence (screened" in role:
        return (4, 0)
    if "original_mathdef_editorial" in status:
        return (2, 0)
    if "not_independently_rechecked" in status:
        return (1, 0)
    if "not approved" in role:
        return (-1, 0)
    return (3, 0)


def _add_source(target: list[dict], incoming: dict) -> None:
    """Keep distinct URLs/locators, and evidence on a duplicate source."""
    key = (incoming.get("url", "").strip(), incoming.get("locator", "").strip())
    for item in target:
        if (item.get("url", "").strip(), item.get("locator", "").strip()) == key:
            # Preserve separate citation evidence, not merely the winning title.
            evidence = item.setdefault("additional_evidence", [])
            detail = {k: v for k, v in incoming.items()
                      if k not in ("url", "locator", "additional_evidence")}
            if detail and detail not in evidence and detail != {
                    k: v for k, v in item.items()
                    if k not in ("url", "locator", "additional_evidence")}:
                evidence.append(detail)
            if _source_rank(incoming) > _source_rank(item):
                for field in ("title", "verification_status", "role", "source_id",
                              "evidence_id"):
                    if incoming.get(field):
                        item[field] = incoming[field]
            return
    target.append(deepcopy(incoming))


def _ids(catalog: dict) -> tuple[dict, dict, dict]:
    meanings, forms, groups = {}, {}, {}
    for group in catalog["groups"]:
        gid = group["id"]
        if gid in groups:
            raise CleanupError("Repeated group: " + gid)
        groups[gid] = group
        for meaning in group["meanings"]:
            mid = meaning["id"]
            if mid in meanings:
                raise CleanupError("Repeated meaning: " + mid)
            meanings[mid] = (group, meaning)
            for form in meaning["formulations"]:
                fid = form["id"]
                if fid in forms:
                    raise CleanupError("Repeated formulation: " + fid)
                forms[fid] = (meaning, form)
    return meanings, forms, groups


def prepare_curated_cleanup(catalog: dict, repo: Path,
                            *, require_full_metadata: bool = False) -> tuple[dict, dict, dict]:
    """Apply *only explicit human/mathematically reviewed* pair decisions.

    The relation transformation is safe for stage-local checking. Final
    linking is a separate, user-gated operation, NOT called from here.
    """
    repo = Path(repo)
    decisions = _json(repo / "data" / "merged_cleanup_decisions.json")
    if decisions.get("schema_version") != 1:
        raise CleanupError("Unrecognized cleanup decisions schema")
    allowed_subjects = _registry(repo, "math_subjects.json")
    allowed_contexts = _registry(repo, "math_contexts.json")
    combined = deepcopy(catalog)
    meanings, forms, _ = _ids(combined)
    original_total = (len(meanings), len(forms), len(combined["relations"]))
    meaning_aliases = {}
    form_aliases = {}
    completed = []
    seen = set()
    for row in decisions["merge_meanings"]:
        loser_id, winner_id = row["removed_meaning_id"], row["kept_meaning_id"]
        preferred_fid = row["kept_formulation_id"]
        case = row["case_id"]
        if case in seen or loser_id in meaning_aliases or loser_id == winner_id:
            raise CleanupError("Repeated or self-referential merge decision: " + case)
        seen.add(case)
        if loser_id not in meanings or winner_id not in meanings:
            raise CleanupError("Unknown meaning in merge: " + case)
        losing_group, loser = meanings[loser_id]
        winning_group, winner = meanings[winner_id]
        if losing_group["id"] != winning_group["id"]:
            raise CleanupError("Cross-heading semantic merge requires independent review: " + case)
        targets = [f for f in winner["formulations"] if f["id"] == preferred_fid]
        if len(targets) != 1:
            raise CleanupError("Invalid kept formulation: " + case)
        preferred = targets[0]
        for old_form in loser["formulations"]:
            form_aliases[old_form["id"]] = preferred_fid
            for source in old_form.get("sources", []):
                _add_source(preferred.setdefault("sources", []), source)
        for source in loser.get("other_sources", []):
            _add_source(winner.setdefault("other_sources", []), source)
        winner.setdefault("consolidated_from_meanings", []).append(loser_id)
        if loser.get("original_definition_id"):
            winner.setdefault("legacy_original_definition_ids", []).append(
                loser["original_definition_id"]
            )
        meaning_aliases[loser_id] = winner_id
        losing_group["meanings"].remove(loser)
        del meanings[loser_id]
        for f in loser["formulations"]:
            del forms[f["id"]]
        completed.append(case)

    # Convention-sensitive wording updates belong in this merged-only layer.
    # They must not change the frozen independent source or original .tex files.
    text_override_ids = set()
    translation_audit = []
    for fid, edit in decisions.get("text_overrides", {}).items():
        if fid not in forms:
            raise CleanupError("Text override references missing formulation " + fid)
        meaning, form = forms[fid]
        if form["text"] != edit["original_text"]:
            raise CleanupError("Historical mathematical wording drift: " + fid)
        if not edit.get("source_assessment_id") or not edit.get("convention_id"):
            raise CleanupError("Convention translation requires source evidence: " + fid)
        form["text"] = edit["text"]
        form["editorial_translation"] = deepcopy(edit)
        text_override_ids.add(fid)
        translation_audit.append({"formulation_id": fid, **edit})

    # Repoint incoming targets; safely carry "related" edges from deleted forms.
    # An anchored definition-use relation from removed text is NOT transferable
    # to different text (offsets and phrasing may change). Record it for the
    # user's eventual single full link rebuild, rather than fabricating links.
    rebuilt_relations = []
    needs_relink = []
    dedup = set()
    for rel in combined["relations"]:
        cur = deepcopy(rel)
        old_form = cur["from_formulation"]
        if old_form in text_override_ids and cur.get("relation_type") == "definition_uses":
            # Previously anchored spans are invalidated by modified wording.
            needs_relink.append(cur["id"])
            continue
        if old_form in form_aliases:
            if cur.get("relation_type") == "definition_uses":
                needs_relink.append(cur["id"])
                continue
            cur["from_formulation"] = form_aliases[old_form]
            cur.pop("span_start", None)
            cur.pop("span_end", None)
            cur.pop("source_phrase", None)
        cur["target_meaning"] = meaning_aliases.get(
            cur["target_meaning"], cur["target_meaning"]
        )
        key = (cur["from_formulation"], cur["target_meaning"],
               cur.get("relation_type", "related"))
        if key in dedup:
            continue
        dedup.add(key)
        rebuilt_relations.append(cur)
    combined["relations"] = rebuilt_relations
    metadata = decisions.get("metadata_assignments", {})
    for mid, fields in metadata.items():
        if mid not in meanings:
            raise CleanupError("Metadata references missing/suppressed meaning " + mid)
        if fields.get("subject") not in allowed_subjects:
            raise CleanupError("Unregistered subject for " + mid)
        if fields.get("context") and fields["context"] not in allowed_contexts:
            raise CleanupError("Unregistered context for " + mid)
        meaning = meanings[mid][1]
        meaning["subject"] = fields["subject"]
        if fields.get("context"):
            meaning["context"] = fields["context"]
        else:
            meaning.pop("context", None)
    all_meanings, all_forms, _ = _ids(combined)
    missing_subject = sorted(mid for mid, (g, m) in all_meanings.items()
                             if not m.get("subject"))
    if require_full_metadata and missing_subject:
        raise CleanupError("%d meanings remain without curated mathematical subject"
                           % len(missing_subject))
    combined["consolidated_ids"] = {
        "meaning_aliases": meaning_aliases,
        "formulation_aliases": form_aliases,
    }
    # Resolve registered canonical meanings against the live surviving data.
    # This is deliberately late: nothing is pinned to the pre-cleanup wording.
    canonical, assessments = read_conventions(repo, combined)
    for entry in canonical.values():
        meaning = all_meanings[entry["canonical_meaning_id"]][1]
        notes = meaning.setdefault("convention_notes", [])
        record = {"convention_id": entry["convention_id"], "note": entry["note"]}
        if record not in notes:
            notes.append(record)
    valid_assessment_ids = {a["assessment_id"] for a in assessments}
    for edit in translation_audit:
        if edit["source_assessment_id"] not in valid_assessment_ids:
            raise CleanupError("Missing actual verified convention assessment for translation")
        a = next(a for a in assessments if a["assessment_id"] == edit["source_assessment_id"])
        if a["status"] != "verified_applies" or a["convention_id"] != edit["convention_id"]:
            raise CleanupError("Source wording change lacks a verified applicable restriction")
    register = compile_source_registry(combined, repo=repo)
    subject_counts = Counter(m["subject"] for g, m in all_meanings.values()
                             if m.get("subject"))
    context_counts = Counter(m["context"] for g, m in all_meanings.values()
                             if m.get("context"))
    report = {
        "phase": "stage_only_before_user_review",
        "is_publication_ready": False,
        "source_baseline": decisions.get("source_baseline"),
        "starting_meanings": original_total[0],
        "starting_formulations": original_total[1],
        "starting_relations": original_total[2],
        "surviving_meanings": len(all_meanings),
        "surviving_formulations": len(all_forms),
        "surviving_relations_pre_final_linking": len(combined["relations"]),
        "removed_duplicate_meanings": len(meaning_aliases),
        "removed_duplicate_formulations": original_total[1] - len(all_forms),
        "semantic_decisions_completed": completed,
        "convention_sensitive_text_translations": translation_audit,
        "registered_conventions": sorted(canonical),
        "source_convention_assessments": len(assessments),
        "deleted_source_text_edges_needing_global_relink": needs_relink,
        "subject_coverage": len(all_meanings) - len(missing_subject),
        "subject_missing": len(missing_subject),
        "subjects_assigned_counts": dict(sorted(subject_counts.items())),
        "contexts_assigned_counts": dict(sorted(context_counts.items())),
        "source_registry_count": len(register["sources"]),
        "term_source_registry_groups": len(register["groups"]),
        "metadata_missing_ids_first_50": missing_subject[:50],
        "important": "No full link rebuild, final link audit or publication has run",
    }
    # Source identifiers refer to survivor IDs and safely retain original ID
    # aliases so a future correction ledger can reference either citation ID.
    register["consolidated_ids"] = combined["consolidated_ids"]
    return combined, report, register


def compile_source_registry(catalog: dict, *, repo: Path | None = None) -> dict:
    """Term-level URL registry: locators + support roles + stable source IDs.

    Source metadata is constructed from the *merged* corpus (not historical
    cohort labels). An original Github source file is tracked as provenance
    but is never presented as an independent authoritative source.
    """
    sources: dict[str, dict] = {}
    groups: list[dict] = []
    for group in catalog["groups"]:
        meaning_entries = []
        term_sources = set()
        for meaning in group["meanings"]:
            midsources = set()
            form_primary = {}
            for form in meaning["formulations"]:
                eligible = []
                for citation in form.get("sources", []):
                    url = (citation.get("url") or "").strip()
                    if not url:
                        # This legacy observation should retain a locator, but
                        # cannot be assigned an invented canonical URL.
                        continue
                    sid = _sid(url)
                    provenance = not _has_external_evidence(citation)
                    row = sources.setdefault(sid, {
                        "id": sid, "url": url, "titles": [],
                        "occurrences": [], "visible_in_future_sources_ui": not provenance
                    })
                    if row["url"] != url:
                        raise CleanupError("Source ID hash collision")
                    row["visible_in_future_sources_ui"] |= not provenance
                    if citation.get("title") and citation["title"] not in row["titles"]:
                        row["titles"].append(citation["title"])
                    occurrence = {
                        "group_id": group["id"], "meaning_id": meaning["id"],
                        "formulation_id": form["id"],
                        "locator": citation.get("locator") or url,
                        "verification_status": citation.get("verification_status", "untracked"),
                        "role": citation.get("role", "supporting definition"),
                        "provenance_only": provenance,
                    }
                    if occurrence not in row["occurrences"]:
                        row["occurrences"].append(occurrence)
                    # If two formulations supplied the same URL, preserve each
                    # independently recorded citation evidence after a merge.
                    for extra in citation.get("additional_evidence", []):
                        supplementary = {
                            **occurrence,
                            "verification_status": extra.get("verification_status", "untracked"),
                            "role": extra.get("role", "additional citation evidence"),
                            "evidence_id": extra.get("evidence_id"),
                            "source_id": extra.get("source_id"),
                        }
                        if supplementary not in row["occurrences"]:
                            row["occurrences"].append(supplementary)
                    midsources.add(sid)
                    term_sources.add(sid)
                    if not provenance and _source_rank(citation)[0] >= 0:
                        eligible.append((_source_rank(citation), sid))
                if eligible:
                    # Deterministic primary selection from available evidence;
                    # NOT a source-reliability score or correction statistic.
                    eligible.sort(key=lambda pair: (-pair[0][0], pair[1]))
                    form_primary[form["id"]] = eligible[0][1]
            for citation in meaning.get("other_sources", []):
                url = (citation.get("url") or "").strip()
                if not url:
                    continue
                sid = _sid(url)
                row = sources.setdefault(sid, {
                    "id": sid, "url": url, "titles": [],
                    "occurrences": [], "visible_in_future_sources_ui": _has_external_evidence(citation)
                })
                if citation.get("title") and citation["title"] not in row["titles"]:
                    row["titles"].append(citation["title"])
                occurrence = {
                    "group_id": group["id"], "meaning_id": meaning["id"],
                    "formulation_id": None,
                    "locator": citation.get("locator") or url,
                    "verification_status": citation.get("verification_status", "untracked"),
                    "role": citation.get("role", "supplemental reference"),
                    "provenance_only": not _has_external_evidence(citation),
                }
                if occurrence not in row["occurrences"]:
                    row["occurrences"].append(occurrence)
                midsources.add(sid)
                term_sources.add(sid)
            meaning_entries.append({
                "meaning_id": meaning["id"], "subject": meaning.get("subject"),
                "context": meaning.get("context"),
                "source_ids": sorted(midsources),
                "primary_source_id": next(iter(form_primary.values()), None),
                "primary_source_by_formulation": form_primary,
                "convention_notes": meaning.get("convention_notes", []),
            })
        groups.append({
            "group_id": group["id"], "term": group["title"],
            "source_ids": sorted(term_sources), "meanings": meaning_entries,
        })
    if repo is not None:
        for row in sources.values():
            row["source_convention_assessments"] = resolved_source_assessments(
                repo, catalog, row["url"]
            )
    return {
        "schema_version": 1, "scope": "merged_mathdef_term_sources",
        "primary_policy": "best available citation evidence, subject to future human override",
        "correction_event_history": "not_tracked",
        "source_score_or_correction_count": "not_implemented",
        "sources": dict(sorted(sources.items())),
        "groups": groups,
    }


def write_stage_only(catalog: dict, repo: Path, output: Path) -> dict:
    """Convenient stage-only inspection. Do NOT call the global linker here."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    merged, report, registry = prepare_curated_cleanup(catalog, repo)
    for name, payload in (
        ("catalog.stage-only.json", merged),
        ("cleanup-report.stage-only.json", report),
        ("sources.stage-only.json", registry),
    ):
        (output / name).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return report
