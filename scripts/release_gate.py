from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def finding(rule_id: str, severity: str, file: str, evidence: str, remediation: str) -> dict[str, str]:
    return {"rule_id": rule_id, "severity": severity, "file": file, "evidence": evidence, "remediation": remediation}


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-root", type=Path, default=Path("."))
    parser.add_argument("--blocklist-file", type=Path)
    parser.add_argument("--history", action="store_true")
    args = parser.parse_args()
    root = args.public_root.resolve()
    scripts = root / "scripts"
    findings: list[dict[str, str]] = []
    checks = [
        ("PUBLIC-GATE-001", [sys.executable, str(scripts / "verify_public_release.py")], "Public release verification failed."),
        ("PUBLIC-GATE-002", [sys.executable, str(scripts / "privacy_scan.py"), str(root), "--json"], "Privacy scanning failed."),
    ]
    if args.blocklist_file:
        checks[1][1].extend(["--blocklist-file", str(args.blocklist_file)])
    if args.history:
        checks[1][1].append("--history")
    for rule_id, command, remediation in checks:
        result = run(command, root)
        if result.returncode:
            evidence = (result.stdout + result.stderr).strip()[-1000:] or f"command exited {result.returncode}"
            findings.append(finding(rule_id, "critical", "scripts", evidence, remediation))
    if (root / ".git").exists():
        result = run(["git", "diff", "--check"], root)
        if result.returncode:
            findings.append(finding("PUBLIC-GATE-003", "major", "git diff", result.stdout.strip() or result.stderr.strip(), "Fix whitespace errors before committing."))
    findings.sort(key=lambda item: item["rule_id"])
    print(json.dumps({"summary": {"rule_set": "public_release_gate", "finding_count": len(findings)}, "findings": findings}, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] in {"critical", "major"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
