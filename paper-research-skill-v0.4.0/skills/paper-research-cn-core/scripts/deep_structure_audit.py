from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ACTIVE_ARCHIVES = {".zip", ".rar", ".7z"}
CACHE_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "node_modules"}
BLOCKING = {"critical", "major"}


def finding(rule_id: str, severity: str, file: str, evidence: str, remediation: str) -> dict[str, str]:
    return {"rule_id": rule_id, "severity": severity, "file": file, "evidence": evidence, "remediation": remediation}


def is_archived(relative: Path) -> bool:
    return any(part == "99_archive" or part.startswith("08_") or part.startswith("09_") for part in relative.parts)


def audit_project(root: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if is_archived(relative):
            continue
        if path.name in CACHE_NAMES:
            findings.append(finding("STRUCTURE-CACHE-001", "major", relative.as_posix(), "cache or environment directory in active project tree", "Remove or archive generated environments and caches outside the active research tree."))
        elif path.is_file() and path.suffix.casefold() in ACTIVE_ARCHIVES:
            findings.append(finding("STRUCTURE-ARCHIVE-001", "major", relative.as_posix(), "active archive package outside backup area", "Move the archive to an approved backup directory or unpack only the needed source files."))
        elif path.is_file() and path.name.casefold() in {"desktop.ini", "thumbs.db"}:
            findings.append(finding("STRUCTURE-SYSTEM-001", "minor", relative.as_posix(), "system-generated file", "Exclude the file from the active project tree."))
        elif path.is_file() and len(relative.parts) > 8:
            findings.append(finding("STRUCTURE-DEPTH-001", "minor", relative.as_posix(), "deeply nested active file", "Flatten the active path or document why the nesting is required."))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit active project structure for caches, archives, system files, and excessive nesting.")
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--csv", type=Path)
    args = parser.parse_args()
    try:
        root = args.project_root.resolve()
        findings = audit_project(root)
    except OSError as error:
        findings = [finding("STRUCTURE-READ-001", "critical", str(args.project_root), str(error), "Provide an accessible project root.")]
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["rule_id", "severity", "file", "evidence", "remediation"])
            writer.writeheader()
            writer.writerows(findings)
    print(json.dumps({"findings": findings}, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] in BLOCKING for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
