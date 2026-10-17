"""Conservative, reproducible dependency matching for the mathDef definition corpus.

Links are derived from definition bodies, never related metadata alone. Metadata
helps disambiguate terms which actually occur in the body. The override manifest
is a future community-review handoff, not a visitor-editable data store.
"""
import json
import re
import unicodedata
from collections import defaultdict

MATH = re.compile(r"\$\$[\s\S]*?\$\$|\$[^$\n]*\$|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]")
COMMAND = re.compile(r"\\[A-Za-z]+\*?")
WORD = re.compile(r"[\w]+", re.UNICODE)
MAX_MATCHES = 30


def normalize_label(label):
    return " ".join(WORD.findall(unicodedata.normalize("NFKC", label).casefold()))


def _masked_prose(body):
    """Keep offsets unchanged, hiding mathematics and TeX commands."""
    text = list(body)
    for match in MATH.finditer(body):
        for i in range(match.start(), match.end()):
            text[i] = " "
    for match in COMMAND.finditer(body):
        for i in range(match.start(), match.end()):
            text[i] = " "
    for i, char in enumerate(text):
        if char in "{}":
            text[i] = " "
    return "".join(text)


def _forms(label):
    """Only simple morphological variation; no unsafe stemming."""
    label = label.strip()
    if not label or len(normalize_label(label).replace(" ", "")) < 3:
        return []
    forms = [(label, "exact")]
    if "$" in label or "\\" in label:
        return forms
    bits = label.split()
    if not bits:
        return forms
    final = bits[-1]
    if len(final) > 3 and re.fullmatch(r"[A-Za-z]+", final) and not final.lower().endswith("s"):
        if final[-1].lower() == "y" and final[-2].lower() not in "aeiou":
            plural = final[:-1] + "ies"
        elif final.lower().endswith(("ch", "sh", "x", "z")):
            plural = final + "es"
        else:
            plural = final + "s"
        forms.append((" ".join(bits[:-1] + [plural]), "inflection"))
    return forms


def _regex(label):
    pattern = r"\s+".join(re.escape(t) for t in label.split())
    return re.compile(r"(?<!\w)" + pattern + r"(?!\w)", re.I)


def _validate_overrides(entries, overrides):
    ids = {d["id"] for d in entries}
    for src, rule in overrides.items():
        if src not in ids:
            raise ValueError(f"Link override refers to missing definition: {src}")
        if not isinstance(rule, dict) or set(rule) - {"include", "exclude", "resolve"}:
            raise ValueError(f"Invalid link override structure: {src}")
        for target in rule.get("include", []) + rule.get("exclude", []) + list(rule.get("resolve", {}).values()):
            if target not in ids or target == src:
                raise ValueError(f"Invalid dependency target for {src}: {target}")


def populate_dependencies(entries, overrides=None):
    """Return (derived metadata by ID, auditable summary).

    Each match includes source body offsets for inline cues; -1 marks
    an explicit include without a literal occurrence.
    """
    overrides = overrides or {}
    _validate_overrides(entries, overrides)
    patterns = []
    byid = {d["id"]: d for d in entries}
    reverse_related = defaultdict(set)
    for d in entries:
        for target in d["related"]:
            reverse_related[target].add(d["id"])
    for target in entries:
        seen = set()
        for label, kind in [(target["term"], "term")] + [(alias, "alias") for alias in target["aliases"]]:
            for form, variant in _forms(label):
                key = (form.casefold(), variant)
                if key in seen:
                    continue
                seen.add(key)
                patterns.append((target["id"], form, kind, variant, _regex(form)))
    result, ambiguous = {}, []
    matched = 0
    for source in entries:
        src = source["id"]
        rule = overrides.get(src, {})
        blocked = set(rule.get("exclude", [])) | {src}
        resolves = {normalize_label(k): v for k, v in rule.get("resolve", {}).items()}
        prose = _masked_prose(source["body"])
        candidates = defaultdict(list)
        for target_id, form, kind, variant, pattern in patterns:
            if target_id in blocked:
                continue
            text = source["body"] if ("$" in form or "\\" in form) else prose
            for m in pattern.finditer(text):
                score = 100 if variant == "exact" else 75
                score += 10 if kind == "term" else 0
                if target_id in source["related"]:
                    score += 55
                if src in reverse_related[target_id]:
                    score += 20
                if byid[target_id]["path"].split("/")[1] == source["path"].split("/")[1]:
                    score += 25
                forced = resolves.get(normalize_label(m.group()), "")
                if forced and forced != target_id:
                    continue
                if forced == target_id:
                    score += 1000
                candidates[(m.start(), m.end())].append({
                    "id": target_id, "start": m.start(), "end": m.end(),
                    "label": m.group(), "kind": kind, "score": score,
                })
        options = []
        for (start, end), group in candidates.items():
            best_by_id = {}
            for candidate in group:
                if candidate["id"] not in best_by_id or candidate["score"] > best_by_id[candidate["id"]]["score"]:
                    best_by_id[candidate["id"]] = candidate
            ranked = sorted(best_by_id.values(), key=lambda c: (-c["score"], c["id"]))
            if len(ranked) > 1 and ranked[0]["score"] - ranked[1]["score"] < 15:
                ambiguous.append({"source": src, "phrase": ranked[0]["label"],
                                  "candidates": [c["id"] for c in ranked[:6]]})
                continue
            options.append(ranked[0])
        selected, occupied, seen_targets = [], [], set()
        for option in sorted(options, key=lambda c: (-(c["end"] - c["start"]), -c["score"], c["start"], c["id"])):
            if option["id"] in seen_targets or any(option["start"] < b and option["end"] > a for a, b in occupied):
                continue
            seen_targets.add(option["id"])
            occupied.append((option["start"], option["end"]))
            selected.append(option)
        for target in rule.get("include", []):
            if target not in seen_targets and target not in blocked:
                selected.append({"id": target, "start": -1, "end": -1,
                                 "label": byid[target]["term"], "kind": "manual", "score": 2000})
        selected.sort(key=lambda c: (c["start"] < 0, c["start"], c["id"]))
        if len(selected) > MAX_MATCHES:
            selected = selected[:MAX_MATCHES]
        result[src] = [
            {"id": c["id"], "start": c["start"], "end": c["end"], "label": c["label"],
             "reason": "manual" if c["kind"] == "manual" else "text-match"}
            for c in selected
        ]
        matched += len(selected)
    summary = {
        "definitions": len(entries), "links": matched,
        "definitions_with_links": sum(bool(v) for v in result.values()),
        "unresolved_ambiguous_occurrences": len(ambiguous),
        "ambiguous_examples": ambiguous[:150],
        "method": "body-only whole-term/alias matching with conservative inflections and subject/related-context disambiguation",
    }
    return result, summary


def load_overrides(path):
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)
