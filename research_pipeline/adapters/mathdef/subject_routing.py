"""Conservative, inspectable mapping of known mathematical subject evidence.

Never treats research provenance ('Original mathDef', 'Wave 2', Post-Wave2)
as a mathematical Subject. Context-prefix and historical area suggestions
are reviewable classification rules; unknowns remain unassigned.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


def route_subjects(catalog: dict, repo: Path, approved_subjects: set[str]) -> dict:
    routing = json.loads((Path(repo) / "data/math_subject_routing.json").read_text(encoding="utf-8"))
    if routing.get("schema_version") != 1:
        raise ValueError("Unknown mathematical subject routing version")
    original_map = routing["original_area_to_subject"]
    explicit_prefix_map = routing["research_context_prefix_to_subject"]
    for label in [*original_map.values(), *explicit_prefix_map.values()]:
        if label not in approved_subjects:
            raise ValueError("Unregistered subject produced by routing: " + label)
    pending = []
    assignments = Counter()
    needs_attention = []
    for group in catalog["groups"]:
        for meaning in group["meanings"]:
            if meaning.get("subject"):
                continue
            original_id = meaning.get("original_definition_id")
            # Original mathDef area already existed as a curated field in its
            # .tex metadata. It is a classification hint, never a literal
            # subject value, and explicit per-meaning review overrides it.
            if original_id:
                category = original_id.split(".", 1)[0]
                subject = original_map.get(category)
                if subject:
                    meaning["subject"] = subject
                    meaning["subject_assignment_method"] = "curated_original_mathematical_area"
                    assignments["curated_original_mathematical_area"] += 1
                    continue
            label = meaning.get("label", "").strip().casefold()
            label = label.replace("post-wave2", "").replace("wave 2", "").strip(" ·:—-")
            # A mathematical area must stand at the start and be bounded by
            # a true separator. Do not match "algebra" inside a full title.
            candidates = []
            for prefix, subject in explicit_prefix_map.items():
                if label == prefix or any(label.startswith(prefix + delim)
                                          for delim in (":", " ·", " —", " -", " (", ";")):
                    candidates.append((len(prefix), prefix, subject))
            if candidates:
                candidates.sort(key=lambda v: (-v[0], v[1]))
                top = candidates[0]
                if not any(size == top[0] and subj != top[2]
                           for size, _pref, subj in candidates):
                    meaning["subject"] = top[2]
                    meaning["subject_assignment_method"] = "explicit_mathematical_context_prefix"
                    assignments["explicit_mathematical_context_prefix"] += 1
                    continue
            pending.append({"id": meaning["id"], "term": group["title"],
                            "original_definition_id": original_id,
                            "prior_context": meaning.get("label", "")})
            if candidates:
                needs_attention.append({"id": meaning["id"], "matches": candidates})
    return {
        "subject_routing_assignments": dict(assignments),
        "subject_routing_unclassified": len(pending),
        "subject_routing_unclassified_examples": pending[:120],
        "subject_routing_ambiguities": needs_attention[:80],
    }
