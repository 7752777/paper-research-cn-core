from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_EXTENSIONS = {".pdf", ".caj", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".zip", ".rar", ".7z"}
TEXT_EXTENSIONS = {".md", ".yaml", ".yml", ".json", ".py", ".ps1", ".txt"}
SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)(password|token|cookie)\s*=\s*[^\s]+"),
    re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s`]+"),
]


def finding(rule_id: str, severity: str, file: str, evidence: str, remediation: str) -> dict[str, str]:
    return {"rule_id": rule_id, "severity": severity, "file": file, "evidence": evidence, "remediation": remediation}


def main() -> int:
    findings: list[dict[str, str]] = []
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            findings.append(finding("PUBLIC-VERIFY-001", "critical", rel, "forbidden binary/document extension", "Remove the artifact from the public release."))
        if "__pycache__" in path.parts:
            findings.append(finding("PUBLIC-VERIFY-002", "major", rel, "Python cache copied", "Remove generated cache files and add them to .gitignore."))
        if path.stat().st_size > 2_000_000:
            findings.append(finding("PUBLIC-VERIFY-003", "major", rel, "file exceeds 2 MB", "Keep only compact source, fixtures, and documentation in the public package."))
        if path.suffix.lower() in TEXT_EXTENSIONS:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    findings.append(finding("PUBLIC-VERIFY-004", "critical", rel, f"secret-like or local-path pattern: {pattern.pattern}", "Remove the value or local path before release."))
    findings.sort(key=lambda item: (item["file"], item["rule_id"], item["evidence"]))
    print(json.dumps({"summary": {"rule_set": "public_release", "checked_files": len(files), "finding_count": len(findings)}, "findings": findings}, ensure_ascii=False, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
