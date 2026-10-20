"""Portable, adapter-driven research resume checkpoints.

This module has no mathDef, definition, theorem, or subject-matter assumptions.
Project policy and domain integrity checks live in a separate adapter.

Examples:
  python -m research_pipeline.engine.resume_checkpoint --config research_pipeline/adapters/mathdef/resume.json --check
  python -m research_pipeline.engine.resume_checkpoint --config research_pipeline/adapters/mathdef/resume.json --write

A checkpoint is a verified snapshot of *local committed files*. It is never
a claim that a queued GitHub Action succeeded, or that subject-matter research
has been independently peer-reviewed. Check remote workflow conclusions
separately. Human-authored next steps are kept outside the generated file.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


class ResumeError(ValueError):
    """A checkpoint must not certify missing or inconsistent input."""


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest_file(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def inside(repo: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ResumeError("A configured path must be nonempty and repository-relative")
    resolved = (repo / relative).resolve()
    if not resolved.is_relative_to(repo.resolve()):
        raise ResumeError("Configured path escapes repository: " + relative)
    return resolved


def read_json(path: Path) -> dict:
    if not path.is_file():
        raise ResumeError("Required JSON file missing: " + str(path))
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ResumeError("Invalid JSON file: " + str(path)) from exc
    if not isinstance(value, dict):
        raise ResumeError("Expected JSON object: " + str(path))
    return value


def scan_jsonl(path: Path, id_field: str | None = None,
               decision_field: str | None = None) -> dict:
    if not path.is_file():
        raise ResumeError("Required JSONL file missing: " + str(path))
    count = 0
    seen = set()
    decisions = Counter()
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ResumeError(f"Invalid JSONL at {path}:{line_number}") from exc
            if not isinstance(row, dict):
                raise ResumeError(f"Non-object row at {path}:{line_number}")
            if id_field:
                key = row.get(id_field)
                if not isinstance(key, str) or not key:
                    raise ResumeError(f"Missing {id_field} at {path}:{line_number}")
                if key in seen:
                    raise ResumeError(f"Duplicate {id_field}={key!r} in {path}")
                seen.add(key)
            if decision_field:
                decision = row.get(decision_field)
                if not isinstance(decision, str) or not decision:
                    raise ResumeError(f"Missing {decision_field} at {path}:{line_number}")
                decisions[decision] += 1
            count += 1
    result = {"rows": count, "sha256": digest_file(path)}
    if decision_field:
        result["decisions"] = dict(sorted(decisions.items()))
    return result


def supporting_inputs(repo: Path, groups: dict) -> dict:
    """Hash whole configurable input groups without bloating the short snapshot.

    Each group includes matching file paths and content hashes in a stable
    digest. Patterns may not escape the repository, including via symlinks.
    An empty or unmatched configured group fails closed.
    """
    if not isinstance(groups, dict):
        raise ResumeError("supporting_groups must be a mapping")
    result = {}
    for name, patterns in sorted(groups.items()):
        if not isinstance(name, str) or not name or not isinstance(patterns, list) or not patterns:
            raise ResumeError("Supporting input groups need names and nonempty pattern lists")
        files = set()
        for pattern in patterns:
            if (not isinstance(pattern, str) or not pattern or
                    Path(pattern).is_absolute() or ".." in Path(pattern).parts):
                raise ResumeError("Unsafe supporting input pattern: " + repr(pattern))
            for candidate in repo.glob(pattern):
                safe = inside(repo, str(candidate.relative_to(repo)))
                if safe.is_file():
                    files.add(safe)
        if not files:
            raise ResumeError("No files in supporting input group: " + name)
        manifests = [(str(file.relative_to(repo)), digest_file(file))
                     for file in sorted(files)]
        result[name] = {
            "files": len(manifests),
            "sha256": hashlib.sha256(canonical(manifests).encode("utf-8")).hexdigest(),
        }
    return result


def active_commit(repo: Path) -> str | None:
    """Git provides provenance only; it does not prove a CI run succeeded."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True, timeout=8,
        )
        head = result.stdout.strip()
        return head if len(head) == 40 else None
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None


def snapshot(config_path: Path, repo_root: Path) -> dict:
    repo = repo_root.resolve()
    config = read_json(config_path.resolve())
    if config.get("schema_version") != 1:
        raise ResumeError("Unsupported resume adapter configuration version")
    project = config.get("project_id")
    if not isinstance(project, str) or not project.strip():
        raise ResumeError("project_id is required")
    manifest = config.get("records")
    if not isinstance(manifest, dict) or not manifest:
        raise ResumeError("Nonempty records map required")
    plan_path = inside(repo, config["plan_path"])
    plan = read_json(plan_path)
    if plan.get("schema_version") != 1 or not plan.get("next_action"):
        raise ResumeError("Human-authored plan must contain schema_version and next_action")
    stats = {}
    for name, spec in sorted(manifest.items()):
        if not isinstance(spec, dict) or "path" not in spec:
            raise ResumeError("Record specifications require a path")
        path = inside(repo, spec["path"])
        format_ = spec.get("format", "jsonl")
        if format_ == "jsonl":
            stats[name] = scan_jsonl(path, spec.get("id_field"),
                                      spec.get("decision_field"))
        elif format_ == "json":
            obj = read_json(path)
            stats[name] = {"sha256": digest_file(path)}
            for key in spec.get("capture", []):
                if key not in obj:
                    raise ResumeError(f"{name}: missing {key}")
                stats[name][key] = obj[key]
        else:
            raise ResumeError("Only json and jsonl record formats are supported")
    inputs = supporting_inputs(repo, config.get("supporting_groups", {}))
    extra = {}
    adapter_module = config.get("validation_adapter")
    if adapter_module:
        if not isinstance(adapter_module, str) or not adapter_module.startswith(
                "research_pipeline.adapters."):
            raise ResumeError("Validation adapter must be a reviewed repository plugin")
        module = importlib.import_module(adapter_module)
        extra = module.inspect(repo, config)
        if not isinstance(extra, dict):
            raise ResumeError("Adapter inspect() must return a dict")
    output = {
        "schema_version": 1,
        "project_id": project,
        "scope": config.get("scope", "project research"),
        "observed_commit": active_commit(repo),
        "record_evidence": stats,
        "configuration_evidence": {
            "adapter_config_sha256": digest_file(config_path.resolve()),
            "resume_plan_sha256": digest_file(plan_path),
        },
        "supporting_input_evidence": inputs,
        "domain_validation": extra,
        "next_action": plan["next_action"],
        "work_budget_minutes_target": plan.get("work_budget_minutes_target", 12),
        "resume_steps": plan.get("resume_steps", []),
        "workflow_runs_to_check_live": plan.get("workflow_runs_to_check_live", []),
        "known_blockers": plan.get("known_blockers", []),
        "verification_limitations": [
            "Local records, hashes, and adapter invariants were checked.",
            "Remote GitHub Actions status must be checked live after a restart.",
            "A source-screened record is not human mathematical peer review.",
            "This snapshot does not authorize sealing or publication.",
        ],
    }
    if not isinstance(output["work_budget_minutes_target"], (int, float)) or not (
            1 <= output["work_budget_minutes_target"] <= 30):
        raise ResumeError("Work budget must be in [1, 30] minutes")
    return output


def run(config: Path, repo: Path, write: bool = False,
        verify: bool = False) -> dict:
    if write and verify:
        raise ResumeError("Choose write or verify, not both")
    config_path = config if config.is_absolute() else (repo / config)
    spec = read_json(config_path)
    output_path = inside(repo.resolve(), spec["output_path"])
    state = snapshot(config_path, repo)
    previous = read_json(output_path) if output_path.exists() else None
    prior_records = previous.get("record_evidence", {}) if previous else {}
    state["changed_record_sets_since_previous_checkpoint"] = sorted(
        k for k, v in state["record_evidence"].items()
        if prior_records.get(k) != v
    )
    prior_groups = previous.get("supporting_input_evidence", {}) if previous else {}
    state["changed_supporting_groups_since_previous_checkpoint"] = sorted(
        k for k, v in state["supporting_input_evidence"].items()
        if prior_groups.get(k) != v
    )

    # Runtime Git HEAD is useful to the caller but is deliberately NOT stored.
    # The checkpoint's own commit changes HEAD without changing research inputs.
    # Including HEAD would make every otherwise-idempotent saved snapshot stale.
    volatile = {
        "observed_commit",
        "changed_record_sets_since_previous_checkpoint",
        "changed_supporting_groups_since_previous_checkpoint",
        "checkpoint_is_current",
    }
    persistent = {k: v for k, v in state.items() if k not in volatile}
    current = previous == persistent
    if verify and not current:
        raise ResumeError("Saved checkpoint is stale or missing; refresh with --write")
    if write and not current:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        body = json.dumps(persistent, indent=2, ensure_ascii=False,
                          sort_keys=True) + "\n"
        tmp = output_path.with_name(output_path.name + ".tmp")
        tmp.write_text(body, encoding="utf-8")
        os.replace(tmp, output_path)
    state["checkpoint_is_current"] = current or write
    return state


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true",
                      help="Read, validate and display state without changing files")
    mode.add_argument("--write", action="store_true",
                      help="Validate and atomically refresh the checkpoint")
    mode.add_argument("--verify", action="store_true",
                      help="Fail if the saved checkpoint is missing or stale")
    args = parser.parse_args()
    try:
        state = run(args.config, args.repo_root, write=args.write,
                    verify=args.verify)
    except (ResumeError, KeyError, ImportError) as exc:
        parser.exit(2, "Checkpoint refused: " + str(exc) + "\n")
    print(json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
