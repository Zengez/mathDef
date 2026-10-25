"""Export reproducible reviewed-packet preflight artifacts, without submission.

The workflow wrapper fixes the authorized independent workspace. The reusable
CLI accepts explicit repository-relative inputs and writes only OUTSIDE the
checkout. Each invocation requires a fresh output directory. A successful
report certifies mechanics and unchanged bytes, never contextual correctness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

from .core import PipelineError, digest
from .dependency_global_audit import load_live_snapshot, write_offline_packets
from .dependency_review_preflight import review_preflight


def _input(repo: Path, relative: str, *, base: Path, directory=False) -> Path:
    if (not isinstance(relative, str) or not relative.strip()
            or Path(relative).is_absolute() or ".." in Path(relative).parts):
        raise PipelineError("Input must be a nonempty repository-relative path")
    candidate = (repo / relative).resolve()
    if not candidate.is_relative_to(repo) or not candidate.is_relative_to(base.resolve()):
        raise PipelineError("Input escapes its allowed directory")
    if not (candidate.is_dir() if directory else candidate.is_file()):
        raise PipelineError("Input does not exist or has the wrong type: " + relative)
    if not directory and candidate.suffix != ".json":
        raise PipelineError("Reviewed inputs must be JSON files")
    return candidate


def workspace_files(workspace: Path) -> dict[str, str]:
    """Full byte identity, including ledgers and files absent from STATE.json."""
    hashes = {}
    for path in sorted(workspace.rglob("*")):
        if path.is_symlink():
            raise PipelineError("Workspace symlinks are not supported by the export guard")
        if path.is_file():
            sha = hashlib.sha256()
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    sha.update(block)
            hashes[path.relative_to(workspace).as_posix()] = sha.hexdigest()
    return hashes


def export_review(repo: Path, workspace: str, output_dir: Path, *,
                  manifest: str = "", alias_packet: str = "", commit: str = "") -> dict:
    repo = repo.resolve()
    w = _input(repo, workspace, base=repo, directory=True)
    if not (w / "project.json").is_file():
        raise PipelineError("An initialized explicit workspace is required")
    if not manifest and not alias_packet:
        raise PipelineError("Choose at least one reviewed manifest or alias packet")
    inputs = {}
    for label, relative in (("manifest", manifest), ("alias", alias_packet)):
        if relative:
            path = _input(repo, relative, base=repo / "research_pipeline/reviews")
            raw = path.read_bytes()
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise PipelineError("Reviewed input must be a JSON object")
            if label == "alias" and value.get("mode") != "alias":
                raise PipelineError("Expected an alias packet")
            inputs[label] = (path, raw)
    output = output_dir.resolve()
    if output.is_relative_to(repo):
        raise PipelineError("Artifact output must be outside the repository")
    if output.exists():
        raise PipelineError("Refusing to overwrite an existing artifact directory")
    before = workspace_files(w)
    snapshot = load_live_snapshot(w)
    result = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=False)
    actual_commit = result.stdout.strip() if result.returncode == 0 else ""
    if commit and commit != actual_commit:
        raise PipelineError("Expected commit does not match the checked-out repository")
    commit = actual_commit
    report = {
        "schema_version": 1, "status": "running", "read_only": True,
        "mathematics_certified": False, "automatic_submission_performed": False,
        "authorizes_gate_change": False, "commit": commit or None,
        "workspace": w.relative_to(repo).as_posix(),
        "inventory_sha256": snapshot["inventory"]["source_inventory_sha256"],
        "unresolved_fingerprint": snapshot["state"]["summary"]["unresolved_fingerprint"],
        "workspace_file_count": len(before), "workspace_before_sha256": digest(before),
        "inputs": {label: {"path": path.relative_to(repo).as_posix(),
                            "bytes_sha256": hashlib.sha256(raw).hexdigest()}
                   for label, (path, raw) in inputs.items()},
        "amendment": None, "alias": None,
    }
    # Create exclusively: a failed previous run cannot masquerade as new output.
    output.mkdir(parents=True, exist_ok=False)
    try:
        if "manifest" in inputs:
            report["amendment"] = write_offline_packets(
                w, inputs["manifest"][0], output / "generated-amendments")
        if "alias" in inputs:
            report["alias"] = review_preflight(w, inputs["alias"][0])
        after = workspace_files(w)
        report["workspace_after_sha256"] = digest(after)
        report["workspace_unchanged"] = before == after
        report["reviewed_inputs_unchanged"] = all(
            path.read_bytes() == raw for path, raw in inputs.values())
        if not report["workspace_unchanged"] or not report["reviewed_inputs_unchanged"]:
            raise PipelineError("Workspace or reviewed input changed during read-only preflight")
        for label, (path, raw) in inputs.items():
            destination = output / "reviewed-inputs" / label / path.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw)
        report["artifacts"] = workspace_files(output)
        report["status"] = "mechanically_preflighted_not_applied"
    except Exception as exc:
        # Keep an unambiguously failed report, never reusable half-packets.
        for child in output.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
        report["status"] = "failed_not_applied"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["artifacts"] = {}
        (output / "report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--manifest", default="")
    parser.add_argument("--alias-packet", default="")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--commit", default="")
    args = parser.parse_args()
    try:
        report = export_review(args.repo_root, args.workspace, args.output_dir,
                               manifest=args.manifest, alias_packet=args.alias_packet,
                               commit=args.commit)
    except (PipelineError, OSError, ValueError) as exc:
        parser.exit(1, str(exc) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
