from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


TEXT_EXTENSIONS = {".md", ".yaml", ".yml", ".json", ".py", ".ps1", ".txt", ".toml", ".ini", ".cfg", ".csv"}
BINARY_PUBLIC_DENY = {".pdf", ".caj", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".zip", ".rar", ".7z"}
PATTERNS = [
    (re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s`]+", re.I), "local user home path"),
    (re.compile(r"ghp_[A-Za-z0-9_]{20,}"), "GitHub classic token"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "GitHub fine-grained token"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "API key"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)(password|token|cookie)\s*=\s*[^\s]+"), "secret assignment"),
]


def iter_files(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            yield path


def read_blocklist(path: Path | None) -> list[str]:
    if not path:
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]


def finding(rule_id: str, severity: str, file: str, evidence: str, remediation: str) -> dict[str, str]:
    return {"rule_id": rule_id, "severity": severity, "file": file, "evidence": evidence, "remediation": remediation}


def scan_tree(root: Path, blocklist: list[str], public: bool) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for path in iter_files(root):
        rel = path.relative_to(root).as_posix()
        if public and path.suffix.casefold() in BINARY_PUBLIC_DENY:
            findings.append(finding("PRIVACY-BINARY-001", "critical", rel, f"forbidden public file type: {path.suffix}", "Remove binary research artifacts from the public release tree."))
        if path.suffix.casefold() not in TEXT_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern, label in PATTERNS:
            if pattern.search(text):
                findings.append(finding("PRIVACY-SCAN-001", "critical", rel, label, "Remove private paths or credentials before public release."))
        for marker in blocklist:
            if marker and marker in text:
                findings.append(finding("PRIVACY-BLOCKLIST-001", "critical", rel, f"blocklist marker: {marker}", "Remove the private marker from the public release tree."))
    return sorted(findings, key=lambda item: (item["file"], item["rule_id"], item["evidence"]))


def scan_history(root: Path, blocklist: list[str]) -> list[dict[str, str]]:
    if not (root / ".git").exists():
        return []
    findings: list[dict[str, str]] = []
    for marker in blocklist:
        proc = subprocess.run(["git", "log", "--all", "--pickaxe-all", f"-S{marker}", "--oneline"], cwd=root, text=True, capture_output=True)
        if proc.stdout.strip():
            findings.append(finding("PRIVACY-HISTORY-001", "critical", "<git-history>", f"history contains marker: {marker}", "Rewrite or isolate the public history before release."))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--public", action="store_true")
    parser.add_argument("--history", action="store_true")
    parser.add_argument("--blocklist-file", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    blocklist = read_blocklist(args.blocklist_file)
    findings = scan_tree(root, blocklist, args.public)
    if args.history:
        findings.extend(scan_history(root, blocklist))
    result = {"summary": {"root": str(root), "finding_count": len(findings)}, "findings": findings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
