"""Chat-friendly entrypoints: python -m research_pipeline.engine.cli --help."""
import argparse
import json
from pathlib import Path

from .core import EFFORT, PipelineError, Workspace


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True,
                        help="Isolated reconstruction workspace, never the production corpus")
    sub = parser.add_subparsers(dest="action", required=True)
    init = sub.add_parser("init", help="Stage 0 project contract")
    init.add_argument("--config", type=Path, required=True)
    ingest = sub.add_parser("ingest", help="Import one independent, checkpointed research batch")
    ingest.add_argument("stage", choices=("sources", "terms", "observations", "meanings", "relations"))
    ingest.add_argument("--input", type=Path, required=True)
    ingest.add_argument("--batch-size", type=int, default=10)
    ingest.add_argument("--limit", type=int)
    seal = sub.add_parser("seal", help="Freeze a completed stage before the next")
    seal.add_argument("stage", choices=("sources", "terms", "observations", "meanings", "relations"))
    sub.add_parser("status", help="Report current stage counts and handoff")
    sub.add_parser("publish", help="Stage 6 automated gate and private reconstruction catalog")
    sub.add_parser("wave2-plan", help="Generate second-wave source/variant/link queues")
    fork = sub.add_parser("fork-wave2", help="Create a new, separately versioned second-wave workspace")
    fork.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args(argv)
    w = Workspace(args.workspace)
    try:
        if args.action == "init":
            result = w.init(json.loads(args.config.read_text(encoding="utf-8")))
            result = {"initialized": str(w.root)}
        elif args.action == "ingest":
            result = w.ingest(args.stage, args.input, args.batch_size, args.limit)
        elif args.action == "seal":
            result = w.seal(args.stage)
        elif args.action == "status":
            result = w.status()
        elif args.action == "publish":
            result = w.publish()
        elif args.action == "fork-wave2":
            result = w.fork_second_wave(args.destination)
        else:
            result = w.wave2_plan()
    except (PipelineError, OSError, json.JSONDecodeError) as exc:
        parser.exit(2, "Pipeline error: " + str(exc) + "\n")
    print(json.dumps({"action": args.action, "result": result,
                      "recommended_thinking": EFFORT.get(getattr(args, "stage", args.action), "Medium")},
                     ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    main()
