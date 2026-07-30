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
    parser.add_argument("--public-root", type=Path, default=Path("."))
    parser.add_argument("--blocklist-file", type=Path)
    parser.add_argument("--history", action="store_true")
    args = parser.parse_args()

    root = args.public_root.resolve()
    scripts = root / "scripts"
    failures = 0
    failures += run([sys.executable, str(scripts / "verify_public_release.py")], root)
    privacy_cmd = [sys.executable, str(scripts / "privacy_scan.py"), str(root)]
    if args.blocklist_file:
        privacy_cmd += ["--blocklist-file", str(args.blocklist_file)]
    if args.history:
        privacy_cmd += ["--history"]
    failures += run(privacy_cmd, root)
    if (root / ".git").exists():
        failures += run(["git", "diff", "--check"], root)
        failures += run(["git", "status", "--short", "--branch"], root)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
