"""Apply or recover explicit, auditable second-wave changes."""
import argparse
import json
from pathlib import Path

from .revisions import apply_revision, recover_pending


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", required=True, type=Path)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--proposal", type=Path, help="A single approved revision event JSON")
    g.add_argument("--recover", action="store_true", help="Complete interrupted revision intents")
    args = p.parse_args()
    result = (recover_pending(args.workspace) if args.recover else
              apply_revision(args.workspace, json.loads(args.proposal.read_text(encoding="utf-8"))))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
