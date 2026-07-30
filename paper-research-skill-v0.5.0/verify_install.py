from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from install import SKILL_NAMES


IGNORED_PARTS = {"__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or IGNORED_PARTS.intersection(path.parts) or path.suffix.lower() in IGNORED_SUFFIXES:
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(hashlib.sha256(path.read_bytes()).hexdigest().encode("ascii"))
    return digest.hexdigest()


def compare_skill_trees(source: Path, installed: Path) -> list[dict[str, str]]:
    if not source.is_dir() or not installed.is_dir():
        return [{"rule_id": "INSTALL-001", "severity": "major", "file": str(installed), "evidence": "source or installed skill directory is missing", "remediation": "run the verified 5.0 installer with --force."}]
    if tree_hash(source) != tree_hash(installed):
        return [{"rule_id": "INSTALL-002", "severity": "major", "file": str(installed), "evidence": "tree hash differs from package source", "remediation": "rerun installation with --force and inspect local changes."}]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare the one installed 5.0 skill against its package source.")
    parser.add_argument("--installed-root", type=Path, default=Path.home() / ".codex" / "skills")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent / "skills" / SKILL_NAMES[0]
    findings = compare_skill_trees(source, args.installed_root / SKILL_NAMES[0])
    print(json.dumps({"installed_root": str(args.installed_root), "findings": findings}, ensure_ascii=False, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
