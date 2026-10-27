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
from research_pipeline.adapters.mathdef.subject_routing import route_subjects
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



def _apply_reviewed_group_aliases(catalog: dict, repo: Path) -> tuple[dict, list[dict], list[str]]:
    """Move clear duplicate *existing* headings into canonical searchable aliases.

    This is a stage-local deterministic operation, NOT the full link rebuild.
    Every dropped term ID is retained in group_aliases. Never compare or infer
    equivalence from names here: every allowed pair is explicitly adjudicated.
    """
    file = Path(repo) / "data" / "merged_cleanup_cross_heading_review.json"
    ledger = _json(file) if file.is_file() else {
        "schema_version": 1, "clear_duplicate_pending_group_migration": []
    }
    if ledger.get("schema_version") != 1:
        raise CleanupError("Unrecognized cross-heading review ledger")
    groups = {g["id"]: g for g in catalog["groups"]}
    redirected = {}
    rows = []
    used_cases = set()
    for item in ledger.get("clear_duplicate_pending_group_migration", []):
        case = item["case_id"]
        old_gid, new_gid = item["removed_group_id"], item["retained_group_id"]
        old_mid, new_mid = item["removed_meaning_id"], item.get("retained_meaning_id")
        if case in used_cases or old_gid == new_gid or old_gid in redirected:
            raise CleanupError("Repeated cross-heading review decision: " + case)
        used_cases.add(case)
        if old_gid not in groups or new_gid not in groups:
            raise CleanupError("Missing referenced existing heading: " + case)
        old, dest = groups[old_gid], groups[new_gid]
        if (old["title"] != item["removed_title"]
                or dest["title"] != item["retained_title"]):
            raise CleanupError("Cross-heading name drift: " + case)
        if len(old["meanings"]) != 1 or old["meanings"][0]["id"] != old_mid:
            raise CleanupError("Cross-heading source not a single exact meaning: " + case)
        winner = next((m for m in dest["meanings"] if m["id"] == new_mid), None)
        if winner is None or not winner["formulations"]:
            raise CleanupError("Cross-heading canonical meaning missing: " + case)
        for name in [old["title"], *old.get("aliases", [])]:
            if (name.casefold() != dest["title"].casefold()
                    and name.casefold() not in {
                        x.casefold() for x in dest.get("aliases", [])
                    }):
                dest.setdefault("aliases", []).append(name)
        old_meaning = old["meanings"][0]
        old_meaning["term_group_id"] = new_gid
        dest["meanings"].append(old_meaning)
        dest["meanings"].sort(key=lambda m: (m.get("label", "").casefold(), m["id"]))
        dest["aliases"].sort(key=str.casefold)
        catalog["groups"].remove(old)
        del groups[old_gid]
        redirected[old_gid] = new_gid
        rows.append({
            "case_id": case, "removed_meaning_id": old_mid,
            "kept_meaning_id": new_mid,
            "kept_formulation_id": winner["formulations"][0]["id"],
            "reason": item["reason"],
        })
    # A searchable synonym can also refer to a meaningful contextual variant.
    # Move its definitions to the canonical heading WITHOUT deleting any
    # meaning, formulation, source citation or mathematical distinction.
    group_only = []
    for item in ledger.get("group_only_alias_merges", []):
        case = item["case_id"]
        old_gid, new_gid = item["removed_group_id"], item["retained_group_id"]
        if case in used_cases or old_gid == new_gid or old_gid in redirected:
            raise CleanupError("Repeated group-only alias decision: " + case)
        used_cases.add(case)
        if old_gid not in groups or new_gid not in groups:
            raise CleanupError("Group-only alias references missing heading: " + case)
        old, dest = groups[old_gid], groups[new_gid]
        if old["title"] != item["removed_title"] or dest["title"] != item["retained_title"]:
            raise CleanupError("Group-only alias title drift: " + case)
        if not old["meanings"] or not dest["meanings"]:
            raise CleanupError("Empty source/target for group-only alias: " + case)
        for name in [old["title"], *old.get("aliases", [])]:
            if (name.casefold() != dest["title"].casefold()
                    and name.casefold() not in {x.casefold() for x in dest.get("aliases", [])}):
                dest.setdefault("aliases", []).append(name)
        for meaning in old["meanings"]:
            meaning["term_group_id"] = new_gid
            dest["meanings"].append(meaning)
        dest["meanings"].sort(key=lambda m: (m.get("label", "").casefold(), m["id"]))
        dest["aliases"].sort(key=str.casefold)
        catalog["groups"].remove(old)
        del groups[old_gid]
        redirected[old_gid] = new_gid
        group_only.append(case)
    # Reject a small, explicitly reviewed set of misleading historical
    # search aliases while retaining both distinct mathematical definitions.
    # Never infer this from lexical similarity and never touch source records.
    for item in ledger.get("remove_misleading_aliases", []):
        case, gid = item["case_id"], item["group_id"]
        if case in used_cases or gid not in groups:
            raise CleanupError("Unknown/duplicated misleading alias review: " + case)
        used_cases.add(case)
        group = groups[gid]
        if group["title"].casefold() != item["group_title"].casefold():
            raise CleanupError("Alias suppression group title drift: " + case)
        prohibited = item["remove_alias"].casefold()
        if prohibited == group["title"].casefold():
            raise CleanupError("Cannot suppress a canonical mathematical title: " + case)
        found = [x for x in group.get("aliases", []) if x.casefold() == prohibited]
        if not found:
            raise CleanupError("Misleading alias not present for reviewed group: " + case)
        group["aliases"] = [x for x in group["aliases"] if x.casefold() != prohibited]
    return redirected, rows, group_only


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
    original_groups = len(combined["groups"])
    group_aliases, cross_group_merges, group_only_aliases = _apply_reviewed_group_aliases(combined, repo)
    meanings, forms, _ = _ids(combined)
    meaning_aliases = {}
    form_aliases = {}
    completed = []
    seen = set()
    for row in [*decisions["merge_meanings"], *cross_group_merges]:
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
        # In sequential consolidations, the losing meaning may itself be
        # the survivor of a previous reviewed duplicate. Preserve the full
        # provenance chain, not just the immediately discarded ID.
        provenance = winner.setdefault("consolidated_from_meanings", [])
        for previous in [loser_id, *loser.get("consolidated_from_meanings", [])]:
            if previous not in provenance:
                provenance.append(previous)
        original_aliases = winner.setdefault("legacy_original_definition_ids", [])
        for previous in ([loser["original_definition_id"]]
                         if loser.get("original_definition_id") else []) + loser.get(
                             "legacy_original_definition_ids", []):
            if previous not in original_aliases:
                original_aliases.append(previous)
        meaning_aliases[loser_id] = winner_id
        losing_group["meanings"].remove(loser)
        del meanings[loser_id]
        for f in loser["formulations"]:
            del forms[f["id"]]
        completed.append(case)

    # Within one meaning, trivial restatements can also be genuinely
    # redundant. This explicit list is independent of source cohort.
    completed_forms = []
    seen_forms = set()
    for entry in decisions.get("merge_formulations", []):
        case, mid = entry["case_id"], entry["meaning_id"]
        drop_id, keep_id = entry["removed_formulation_id"], entry["kept_formulation_id"]
        if case in seen or drop_id in seen_forms or drop_id == keep_id:
            raise CleanupError("Repeated or self-referential form consolidation: " + case)
        seen.add(case)
        seen_forms.add(drop_id)
        if mid not in meanings or drop_id not in forms or keep_id not in forms:
            raise CleanupError("Unknown meaning/formulation in within-meaning merge: " + case)
        losing_meaning, discarded = forms[drop_id]
        surviving_meaning, selected = forms[keep_id]
        if losing_meaning is not surviving_meaning or surviving_meaning is not meanings[mid][1]:
            raise CleanupError("Cross-meaning formulation merge requires independent review: " + case)
        for citation in discarded.get("sources", []):
            _add_source(selected.setdefault("sources", []), citation)
        selected.setdefault("consolidated_from_formulations", []).append(drop_id)
        surviving_meaning["formulations"].remove(discarded)
        del forms[drop_id]
        form_aliases[drop_id] = keep_id
        completed_forms.append(case)

    # A source-derived meaning may have been folded into another reviewed
    # source-derived meaning before that survivor was itself folded into an
    # original meaning. Historical IDs must resolve directly to LIVE targets,
    # not to intermediate (already removed) IDs. Detect cycles and missing
    # destinations rather than producing broken links or archival aliases.
    def resolve_aliases(mapping: dict[str, str], live: set[str], label: str) -> None:
        for old in mapping:
            destination = mapping[old]
            visited = {old}
            while destination in mapping:
                if destination in visited:
                    raise CleanupError("Cyclic " + label + " redirect: " + old)
                visited.add(destination)
                destination = mapping[destination]
            if destination not in live:
                raise CleanupError("Invalid live " + label + " redirect: " + old)
            mapping[old] = destination

    resolve_aliases(meaning_aliases, set(meanings), "meaning")
    resolve_aliases(form_aliases, set(forms), "formulation")

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
    routing_report = route_subjects(combined, repo, allowed_subjects)
    all_meanings, all_forms, _ = _ids(combined)
    missing_subject = sorted(mid for mid, (g, m) in all_meanings.items()
                             if not m.get("subject"))
    if require_full_metadata and missing_subject:
        raise CleanupError("%d meanings remain without curated mathematical subject"
                           % len(missing_subject))
    combined["consolidated_ids"] = {
        "group_aliases": group_aliases,
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
    retained = _json(repo / "data/merged_cleanup_retained_variants.json")
    if retained.get("schema_version") != 1:
        raise CleanupError("Missing retained-variant review ledger")
    by_name = {g["title"].casefold(): g for g in combined["groups"]}
    retained_count = 0
    for record in retained["entries"]:
        term = record["term"]
        group = by_name.get(term.casefold())
        if not group:
            raise CleanupError("Retained mathematical variant group absent: " + term)
        nforms = sum(len(m["formulations"]) for m in group["meanings"])
        if nforms < 2:
            raise CleanupError("Retained variant lost its independent formulation: " + term)
        retained_count += 1
    subject_counts = Counter(m["subject"] for g, m in all_meanings.values()
                             if m.get("subject"))
    context_counts = Counter(m["context"] for g, m in all_meanings.values()
                             if m.get("context"))
    report = {
        "phase": "stage_only_before_user_review",
        "is_publication_ready": False,
        "source_baseline": decisions.get("source_baseline"),
        "starting_groups": original_groups,
        "surviving_groups": len(combined["groups"]),
        "retired_searchable_heading_aliases": len(group_aliases),
        "cross_heading_cases_applied": [x["case_id"] for x in cross_group_merges],
        "group_only_alias_cases_applied": group_only_aliases,
        "misleading_search_aliases_removed": [r["case_id"] for r in _json(repo / "data/merged_cleanup_cross_heading_review.json").get("remove_misleading_aliases", [])],
        "starting_meanings": original_total[0],
        "starting_formulations": original_total[1],
        "starting_relations": original_total[2],
        "surviving_meanings": len(all_meanings),
        "surviving_formulations": len(all_forms),
        "surviving_relations_pre_final_linking": len(combined["relations"]),
        "removed_duplicate_meanings": len(meaning_aliases),
        "removed_duplicate_formulations": original_total[1] - len(all_forms),
        "semantic_decisions_completed": completed,
        "formulation_decisions_completed": completed_forms,
        "convention_sensitive_text_translations": translation_audit,
        "registered_conventions": sorted(canonical),
        "retained_variant_groups_reviewed": retained_count,
        "source_convention_assessments": len(assessments),
        "deleted_source_text_edges_needing_global_relink": needs_relink,
        "subject_coverage": len(all_meanings) - len(missing_subject),
        **routing_report,
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
                    # Independent records store the work/home URL separately
                    # from a specific section/tag URL. Stable source identity
                    # for correction reports must distinguish Stacks tags.
                    locator = citation.get("locator") or url
                    cited_url = locator if locator.startswith("https://") else url
                    sid = _sid(cited_url)
                    provenance = not _has_external_evidence(citation)
                    row = sources.setdefault(sid, {
                        "id": sid, "url": cited_url, "work_urls": [],
                        "titles": [], "occurrences": [],
                        "visible_in_future_sources_ui": not provenance
                    })
                    if url not in row["work_urls"]:
                        row["work_urls"].append(url)
                    if row["url"] != cited_url:
                        raise CleanupError("Source ID hash collision")
                    row["visible_in_future_sources_ui"] |= not provenance
                    if citation.get("title") and citation["title"] not in row["titles"]:
                        row["titles"].append(citation["title"])
                    occurrence = {
                        "group_id": group["id"], "meaning_id": meaning["id"],
                        "formulation_id": form["id"],
                        "locator": locator,
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
                locator = citation.get("locator") or url
                cited_url = locator if locator.startswith("https://") else url
                sid = _sid(cited_url)
                row = sources.setdefault(sid, {
                    "id": sid, "url": cited_url, "work_urls": [],
                    "titles": [], "occurrences": [],
                    "visible_in_future_sources_ui": _has_external_evidence(citation)
                })
                if url not in row["work_urls"]:
                    row["work_urls"].append(url)
                if citation.get("title") and citation["title"] not in row["titles"]:
                    row["titles"].append(citation["title"])
                occurrence = {
                    "group_id": group["id"], "meaning_id": meaning["id"],
                    "formulation_id": None,
                    "locator": locator,
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
