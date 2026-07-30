from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


BLOCKING = {"critical", "major"}
VALID_SEVERITIES = {"critical", "major", "minor", "info"}
REQUIRED_FINDING_FIELDS = ("rule_id", "severity", "file", "evidence", "remediation")
REQUIRED_ARTIFACTS = (
    "doc_json",
    "evidence_ledger",
    "render_record",
    "review_matrix",
)
REQUIRED_AUDITS = (
    "number",
    "ai_style",
    "figures",
    "references",
    "ledger",
    "manuscript",
    "structure",
    "review",
    "render",
)


def required_artifacts() -> tuple[str, ...]:
    return REQUIRED_ARTIFACTS


def required_audits() -> tuple[str, ...]:
    return REQUIRED_AUDITS


def finding(rule_id: str, severity: str, file: str, evidence: str, remediation: str) -> dict[str, str]:
    return {
        "rule_id": rule_id,
        "severity": severity,
        "file": file,
        "evidence": evidence,
        "remediation": remediation,
    }


def resolve_input_path(value: object, base_dir: Path) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    path = Path(value)
    return path.resolve() if path.is_absolute() else (base_dir / path).resolve()


def read_findings(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        findings = payload
    elif isinstance(payload, dict) and isinstance(payload.get("findings"), list):
        findings = payload["findings"]
    else:
        raise ValueError("audit report must be a JSON list or an object with a findings list")
    if not all(isinstance(item, dict) for item in findings):
        raise ValueError("every audit finding must be an object")
    return findings


def audit(payload: dict[str, object], base_dir: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, dict):
        findings.append(finding("SUB-PACK-ARTIFACT-001", "critical", "<submission-package>", "missing artifacts object", "Provide the required artifact paths in an artifacts object."))
        artifacts = {}

    for name in REQUIRED_ARTIFACTS:
        path = resolve_input_path(artifacts.get(name), base_dir)
        if path is None or not path.exists() or path.stat().st_size == 0:
            findings.append(finding("SUB-PACK-ARTIFACT-001", "critical", str(path or "<submission-package>"), f"missing or empty artifact: {name}", "Generate the artifact and record its real relative path before final review."))
            continue
        if name == "doc_json":
            try:
                document = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(document, dict) or not isinstance(document.get("blocks"), list):
                    raise ValueError("doc.json lacks blocks")
            except (OSError, ValueError, json.JSONDecodeError) as error:
                findings.append(finding("SUB-PACK-ARTIFACT-002", "critical", str(path), f"invalid doc.json: {error}", "Rebuild doc.json from the manuscript before final review."))

    reports = payload.get("audit_reports")
    if not isinstance(reports, dict):
        findings.append(finding("SUB-PACK-AUDIT-001", "critical", "<submission-package>", "missing audit_reports object", "Persist each audit result as JSON and list every path in audit_reports."))
        reports = {}

    for name in REQUIRED_AUDITS:
        path = resolve_input_path(reports.get(name), base_dir)
        if path is None or not path.is_file() or path.stat().st_size == 0:
            findings.append(finding("SUB-PACK-AUDIT-001", "critical", str(path or "<submission-package>"), f"missing audit report: {name}", "Run the named audit, save its JSON output, and record the real relative path."))
            continue
        try:
            report_findings = read_findings(path)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            findings.append(finding("SUB-PACK-AUDIT-002", "critical", str(path), f"invalid audit report: {error}", "Use an audit script that emits the structured findings interface."))
            continue
        for item in report_findings:
            missing = [field for field in REQUIRED_FINDING_FIELDS if not isinstance(item.get(field), str) or not item[field].strip()]
            severity = str(item.get("severity", "")).lower()
            if missing or severity not in VALID_SEVERITIES:
                findings.append(finding("SUB-PACK-AUDIT-003", "critical", str(path), f"malformed finding in {name}: missing={missing}; severity={severity or '<empty>'}", "Every finding must carry rule_id, severity, file, evidence, and remediation."))
                continue
            if severity in BLOCKING:
                findings.append(finding("SUB-PACK-002", "critical", str(item["file"]), f"unresolved {item['rule_id']} from {name}: {item['evidence']}", "Resolve the upstream Critical or Major finding, regenerate its report, then rerun the final gate."))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Block submission packages with missing artifacts, malformed audit reports, or unresolved major audits.")
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("submission package input must be a JSON object")
        findings = audit(payload, args.input.parent.resolve())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        findings = [finding("SUB-PACK-000", "critical", str(args.input), f"cannot read submission package: {error}", "Fix the package input JSON and rerun the gate.")]
    print(json.dumps({"findings": findings}, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] in BLOCKING for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
