from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from install import SKILL_NAMES


IGNORED_PARTS = {"__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or IGNORED_PARTS.intersection(path.parts) or path.suffix.lower() in IGNORED_SUFFIXES:
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(file_hash(path).encode("ascii"))
    return digest.hexdigest()


def compare_skill_trees(source: Path, installed: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not source.is_dir() or not installed.is_dir():
        return [{"rule_id": "INSTALL-001", "severity": "major", "file": str(installed), "evidence": "source or installed skill directory is missing", "remediation": "run the installer with the verified package root."}]
    if tree_hash(source) != tree_hash(installed):
        findings.append({"rule_id": "INSTALL-002", "severity": "major", "file": str(installed), "evidence": "tree hash differs from package source", "remediation": "rerun installation with --force and inspect local changes."})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare installed 4.0 skill trees against the package source without touching other skills.")
    parser.add_argument("--installed-root", type=Path, default=Path.home() / ".codex" / "skills")
    args = parser.parse_args()
    source_root = Path(__file__).resolve().parent / "skills"
    findings = []
    for name in SKILL_NAMES:
        findings.extend(compare_skill_trees(source_root / name, args.installed_root / name))
    print(json.dumps({"installed_root": str(args.installed_root), "findings": findings}, ensure_ascii=False, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
