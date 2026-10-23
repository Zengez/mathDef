"""Safe, nonauthoritative audit scoring, notation-aware suggestions and review ledger.

This module never edits source meanings, grants a consolidation gate, or treats
lexical similarity as contextual mathematical equivalence.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import re

from research_pipeline.engine.core import PipelineError, digest
from research_pipeline.engine.dependency_graph import norm


_WORDS = {"the", "with", "and", "for", "from"}
_ARROW = re.compile(r"([A-Za-z][A-Za-z0-9_]*)\s*(→|←|↦|⇒|⇉|->|<-|\\to)\s*([A-Za-z][A-Za-z0-9_]*)")
_SYMBOLS = re.compile(r"[→←↦⇒⇉=∈⊆⊂⊕⊗×∩∪∘≤≥≅≈≠]")
_REVIEW = {"accepted_as_correct", "needs_further_review"}
_FINGERPRINT_FIELDS = (
    "code", "formulation_id", "source_version_sha256",
    "effective_node_sha256", "occurrence_id",
)


def math_signature(phrase: str) -> dict:
    """Conserve typed/directed symbols; a bag of words cannot distinguish arrows."""
    s = str(phrase)
    arrows = [(a, op.replace("->", "→").replace("<-", "←"), b)
              for a, op, b in _ARROW.findall(s)]
    return {"arrows": arrows, "symbols": _SYMBOLS.findall(s),
            "tokens": sorted(set(x for x in re.findall(
                r"[^\W_]+", norm(s), re.UNICODE)
                if len(x) > 2 and x not in _WORDS))}


def notation_aware_leads(candidates: list[dict], limit: int = 40) -> dict:
    """Surface candidate leads, partitioned by the stated mathematical domain.

    This never asserts a correct alias. Equation/arrows disagreement lowers
    queue priority instead of being mistaken for a perfect match.
    """
    canonical = [c for c in candidates if not c.get("alias_of")
                 and not c.get("resolved_target_meaning_id")]
    buckets = defaultdict(list)
    for c in canonical:
        domain = norm(str(c.get("context", "")).split(":", 1)[0])
        buckets[domain].append((c, math_signature(c.get("query", ""))))
    leads = []
    for domain, values in sorted(buckets.items()):
        for (a, sa), (b, sb) in combinations(
                sorted(values, key=lambda x: x[0]["id"]), 2):
            x, y = set(sa["tokens"]), set(sb["tokens"])
            if not x or not y:
                continue
            score = len(x & y) / len(x | y)
            if score < .72:
                continue
            notation_conflict = (
                sa["arrows"] != sb["arrows"]
                or (bool(sa["symbols"]) and bool(sb["symbols"])
                    and sa["symbols"] != sb["symbols"])
            )
            leads.append({
                "domain": domain, "candidate_ids": [a["id"], b["id"]],
                "phrases": [a.get("query", ""), b.get("query", "")],
                "surface_jaccard": round(score, 3),
                "notation_conflict": notation_conflict,
                "arrow_signatures": [sa["arrows"], sb["arrows"]],
                "review_priority": round(score * (.3 if notation_conflict else 1), 3),
                "must_review_full_context": True,
                "established_equivalent": False,
            })
    leads.sort(key=lambda r: (-r["review_priority"],
                             -r["surface_jaccard"], r["domain"],
                             r["candidate_ids"]))
    return {"candidate_count": len(canonical), "possible_pairs": len(leads),
            "notation_conflict_pairs": sum(x["notation_conflict"] for x in leads),
            "leads": leads[:max(0, limit)],
            "warning": "Symbolic disagreement is an explicit REVIEW WARNING; "
                       "matching notation is not proof of equivalence."}


def audit_fingerprint(finding: dict) -> dict:
    """Strictly anchored evidence for an accepted, non-integrity review lead."""
    return {
        "code": finding["code"],
        "formulation_id": finding["formulation_id"],
        "source_version_sha256": finding["version_sha256"],
        "effective_node_sha256": finding["effective_node_sha256"],
        "occurrence_id": finding.get("occurrence_id"),
    }


def validate_review_ledger(rows: list[dict]) -> dict:
    """Ledger is assistant/human-authored, never inferred from a warning."""
    verified = {}
    for row in rows:
        if row.get("disposition") not in _REVIEW:
            raise PipelineError("Unsupported audit-review disposition")
        if not str(row.get("reviewed_by", "")).strip():
            raise PipelineError("Audit review needs a named reviewer")
        if len(str(row.get("rationale", "")).strip()) < 40:
            raise PipelineError("Audit review needs contextual mathematical rationale")
        if any(field not in row for field in _FINGERPRINT_FIELDS):
            raise PipelineError("Audit review missing source or effective node anchor")
        if row.get("code") in ("incomplete_effective_node",
                               "stale_source_anchor", "unknown_existing_target",
                               "unregistered_missing_candidate",
                               "stale_missing_identity", "self_dependency"):
            raise PipelineError("Structural integrity alerts cannot be accepted")
        fingerprint = {k: row[k] for k in _FINGERPRINT_FIELDS}
        key = digest(fingerprint)
        if key in verified:
            raise PipelineError("Duplicate audit review fingerprint")
        verified[key] = row
    return verified


def rank_findings(findings: list[dict], nodes: dict, inventory: dict,
                  ledger: list[dict] | None = None) -> dict:
    """Rank impact across effective links; suppress ONLY exact reviewed leads."""
    reviews = validate_review_ledger(ledger or [])
    fan_in = Counter()
    affected_domains = defaultdict(set)
    for fid, node in nodes.items():
        if not node or fid not in inventory["formulations"]:
            continue
        domain = inventory["formulations"][fid].get("context", "").split(":", 1)[0]
        for r in node.get("references", []):
            if r.get("state") != "existing":
                continue
            target = r.get("target_meaning_id")
            fan_in[target] += 1
            affected_domains[target].add(domain)
    by_code = Counter(f["code"] for f in findings)
    needing_review = []
    accepted = []
    for f in findings:
        target = f.get("reference", {}).get("target_meaning_id")
        severity = f["severity"]
        base = {"integrity": 1000, "high": 700, "review": 300}[severity]
        # Bounded fan-in and recurrence preserve severity ordering.
        score = base + min(90, fan_in[target] * 3) + min(60, by_code[f["code"]] * 2)
        score += min(30, len(affected_domains[target]) * 6)
        item = dict(f, priority_score=score,
                    target_fan_in=fan_in[target] if target else 0,
                    recurring_flag_count=by_code[f["code"]])
        key = digest(audit_fingerprint(f))
        review = reviews.get(key)
        if review and review["disposition"] == "accepted_as_correct":
            if severity != "review":
                raise PipelineError("Cannot suppress high/integrity finding")
            item["review_disposition"] = "accepted_as_correct"
            item["review_rationale"] = review["rationale"]
            accepted.append(item)
        else:
            if review:
                item["review_disposition"] = review["disposition"]
            needing_review.append(item)
    needing_review.sort(key=lambda f: (-f["priority_score"], f["code"],
                                      f["formulation_id"],
                                      f.get("reference_index", -1)))
    accepted.sort(key=lambda f: (-f["priority_score"], f["code"],
                                 f["formulation_id"]))
    return {
        "needing_review": needing_review, "accepted": accepted,
        "accepted_count": len(accepted),
        "stale_review_count": len(reviews) - sum(
            digest(audit_fingerprint(f)) in reviews for f in findings),
        "review_by_code": dict(sorted(Counter(
            x["code"] for x in needing_review).items())),
    }
