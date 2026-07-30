from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(args: list[str], cwd: Path) -> int:
    print("+", " ".join(args))
    return subprocess.run(args, cwd=cwd, text=True).returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-root", type=Path, required=True)
    parser.add_argument("--blocklist-file", type=Path)
    parser.add_argument("--history", action="store_true")
    args = parser.parse_args()

    root = args.public_root.resolve()
    script_dir = Path(__file__).resolve().parent
    cmd = [sys.executable, str(script_dir / "privacy_scan.py"), str(root), "--public"]
    if args.blocklist_file:
        cmd += ["--blocklist-file", str(args.blocklist_file)]
    if args.history:
        cmd += ["--history"]
    failures = run(cmd, root)
    if (root / ".git").exists():
        failures += run(["git", "diff", "--check"], root)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
