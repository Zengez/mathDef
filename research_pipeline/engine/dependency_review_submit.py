"""Preflight and deliberately stage reviewed graph packets in one local commit.

Never performs semantic review, pushes to GitHub, or triggers a phase gate.
It validates an entire *disjoint* packet collection before any inbox write.
Default action is read-only. Explicit --approved is required to copy packets
into the isolated workspace inbox; --commit additionally creates ONE local
git commit containing ONLY these exact files. Pushing remains a separate,
deliberate user action so concurrent GitHub work can be reconciled.

Usage:
  python -m research_pipeline.engine.dependency_review_submit \
    --workspace research_pipeline/experiments/reconstruction-v2-independent \
    --packet-dir /tmp/wave2-reviewed-packets
  python -m research_pipeline.engine.dependency_review_submit \
    --workspace research_pipeline/experiments/reconstruction-v2-independent \
    --packet-dir /tmp/wave2-reviewed-packets --approved --commit
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from research_pipeline.engine.core import PipelineError
from research_pipeline.engine.dependency_graph import graph_path
from research_pipeline.engine.dependency_review_preflight import review_preflight


def _run_git(root: Path, *args: str) -> str:
    process = subprocess.run(["git", "-C", str(root), *args],
                             capture_output=True, text=True, check=False)
    if process.returncode:
        raise PipelineError("Git command failed: " + process.stderr.strip())
    return process.stdout.strip()


def review_packet_collection(workspace: Path, packet_dir: Path,
                             *, limit: int = 20) -> dict:
    """Read-only preflight for all packets before copying one."""
    packet_dir = packet_dir.resolve()
    graph = graph_path(workspace)
    if not packet_dir.is_dir():
        raise PipelineError("Offline reviewed packet directory does not exist")
    if packet_dir == (graph / "inbox").resolve():
        raise PipelineError("Use a separate offline directory, not graph inbox")
    paths = sorted(packet_dir.glob("*.json"))
    if not paths or len(paths) > limit:
        raise PipelineError("Need between 1 and 20 reviewed packet files")
    fids, event_ids, package_ids = set(), set(), set()
    summaries = []
    inbox = graph / "inbox"
    for file in paths:
        package = json.loads(file.read_text(encoding="utf-8"))
        if package.get("mode") != "amend":
            raise PipelineError("This safe staging helper supports amendments only")
        if package.get("id") != file.stem or file.stem in package_ids:
            raise PipelineError("Duplicate or invalid reviewed package identity")
        package_ids.add(file.stem)
        amendments = package.get("amendments")
        if not isinstance(amendments, list) or not 1 <= len(amendments) <= 5:
            raise PipelineError("Packets must contain 1 to 5 complete amendments")
        for event in amendments:
            fid, eid = event.get("formulation_id"), event.get("amendment_id")
            if fid in fids or eid in event_ids:
                raise PipelineError("Repeated formulation or event across packets")
            fids.add(fid)
            event_ids.add(eid)
        if (inbox / file.name).exists():
            raise PipelineError("Refusing to overwrite a graph inbox package")
        report = review_preflight(workspace, file)
        if report["status"] != "mechanically_valid_not_applied":
            raise PipelineError("Every staged packet must be un-applied and valid")
        summaries.append({
            "packet_id": file.stem,
            "amendments": len(amendments),
            "package_sha256": report["package_sha256"],
        })
    return {"read_only": True, "mathematics_certified": False,
            "packet_count": len(paths), "distinct_formulations": len(fids),
            "packets": summaries, "paths": paths}


def stage_reviewed_packets(workspace: Path, packet_dir: Path, *,
                           approved: bool = False,
                           commit: bool = False) -> dict:
    """Validate before writing; no remote push under any circumstances."""
    workspace = workspace.resolve()
    packet_dir = packet_dir.resolve()
    review = review_packet_collection(workspace, packet_dir)
    paths = review.pop("paths")
    result = {
        **review, "stage_performed": False, "commit_created": False,
        "push_performed": False,
        "next_step": "Mathematically review all proposals; rerun with --approved "
                     "--commit in the intended git checkout, then inspect/push the "
                     "single commit. Verify independent graph CI and exact receipts.",
    }
    if not approved:
        if commit:
            raise PipelineError("--commit requires explicit --approved")
        return result

    inbox = graph_path(workspace) / "inbox"
    relative_paths = []
    root = None
    if commit:
        try:
            root = Path(_run_git(workspace, "rev-parse", "--show-toplevel")).resolve()
        except (OSError, PipelineError) as exc:
            raise PipelineError("Cannot commit without a real git checkout") from exc
        if not inbox.resolve().is_relative_to(root):
            raise PipelineError("Graph inbox must belong to git checkout")
        if _run_git(root, "diff", "--cached", "--name-only"):
            raise PipelineError("Refusing a mixed commit: git index is not empty")
        relative_paths = [
            (inbox / p.name).relative_to(root).as_posix() for p in paths
        ]

    inbox.mkdir(parents=True, exist_ok=True)
    written = []
    try:
        # Re-check after any git inspection. An existing name is a hard error.
        if any((inbox / p.name).exists() for p in paths):
            raise PipelineError("Graph inbox changed after preflight")
        for path in paths:
            target = inbox / path.name
            with tempfile.NamedTemporaryFile(
                    mode="wb", dir=inbox, prefix=".review-stage-",
                    delete=False) as t:
                tmp = Path(t.name)
                try:
                    with path.open("rb") as source:
                        shutil.copyfileobj(source, t)
                except Exception:
                    tmp.unlink(missing_ok=True)
                    raise
            # Hard-link publication is atomic and cannot overwrite another
            # editor's concurrently created inbox packet (unlike os.replace).
            try:
                os.link(tmp, target)
            except FileExistsError as exc:
                raise PipelineError("Concurrent review packet already exists") from exc
            finally:
                tmp.unlink(missing_ok=True)
            written.append(target)
    except Exception:
        for path in written:
            path.unlink(missing_ok=True)
        raise

    result["stage_performed"] = True
    result["staged_files"] = [str(p) for p in written]
    if commit:
        _run_git(root, "add", "--", *relative_paths)
        staged = set(_run_git(root, "diff", "--cached", "--name-only").splitlines())
        if staged != set(relative_paths):
            raise PipelineError("Refusing commit with unrelated staged changes")
        _run_git(root, "commit", "-m",
                 "Stage mathematically reviewed Wave2 dependency amendments",
                 "--only", "--", *relative_paths)
        result["commit_created"] = True
        result["local_commit_sha"] = _run_git(root, "rev-parse", "HEAD")
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", required=True, type=Path)
    p.add_argument("--packet-dir", required=True, type=Path)
    p.add_argument("--approved", action="store_true",
                   help="Explicitly confirm packets have been mathematically reviewed")
    p.add_argument("--commit", action="store_true",
                   help="Create a single local git commit; NEVER push automatically")
    a = p.parse_args()
    result = stage_reviewed_packets(a.workspace, a.packet_dir,
                                  approved=a.approved, commit=a.commit)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
