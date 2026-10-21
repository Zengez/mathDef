"""Conservative mathDef-only textual reference proposer.

Suggestions are *not* exhaustive semantic scans. Every automatic snapshot stays
scan_incomplete until a contextual reviewer explicitly checks the full text.
Homonyms remain ambiguous absent reliable disambiguation.
"""
from __future__ import annotations

import re
from collections import defaultdict


def _domain(context):
    return " ".join(re.findall(r"[a-z]+", context.casefold().split(":")[0]))


def propose(formulation, meanings):
    text = formulation["text"]
    fid = formulation["formulation_id"]
    origin_domain = _domain(formulation["context"])
    by_label = defaultdict(list)
    for mid, entry in meanings.items():
        label = " ".join(entry["display_term"].split())
        if len(label) >= 3 and re.search(r"[a-zA-Z]", label):
            by_label[label.casefold()].append((mid, entry))
    candidates = []
    for label, matches in by_label.items():
        # Longest existing names claim overlapping spans. Only exact literal
        # matches: no invented synonym/stem/meaning equivalence.
        pattern = r"(?<!\w)" + re.escape(label).replace(r"\ ", r"\s+") + r"(?!\w)"
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            entries = [(mid, entry) for mid, entry in matches
                       if fid not in entry["formulation_ids"]]
            if not entries:
                continue
            candidates.append((match.start(), match.end(), text[match.start():match.end()],
                               entries))
    candidates.sort(key=lambda x: (x[0], -(x[1] - x[0]), x[2].casefold()))
    selected = []
    end = -1
    for start, stop, phrase, entries in candidates:
        if start < end:
            continue
        end = stop
        targets = sorted(set(mid for mid, _ in entries))
        if len(targets) > 1:
            # Matching a high-level branch label is insufficient evidence
            # to choose between two homonymous contextual meanings.
            same_domain = [mid for mid, m in entries
                           if _domain(m["context"]) == origin_domain and origin_domain]
            if len(same_domain) == 1:
                targets = same_domain
        if len(targets) == 1:
            selected.append({
                "phrase": phrase, "span": [start, stop], "state": "existing",
                "target_meaning_id": targets[0], "origin": "unreviewed_lexical_proposal",
                "matching_note": "Exact display-term string; context/semantics still require inspection",
            })
        else:
            selected.append({
                "phrase": phrase, "span": [start, stop], "state": "ambiguous",
                "candidate_meaning_ids": targets,
                "reason": "Multiple contextual meanings share this display term; requires semantic disambiguation",
                "origin": "unreviewed_lexical_proposal",
            })
    return selected
