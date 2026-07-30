from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DOI_PATTERN = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", re.IGNORECASE)


def finding(rule_id: str, severity: str, file: str, evidence: str, remediation: str, line: int | None = None) -> dict[str, str | int]:
    result: dict[str, str | int] = {"rule_id": rule_id, "severity": severity, "file": file, "evidence": evidence, "remediation": remediation}
    if line is not None:
        result["line"] = line
    return result


def load_metadata(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("references") if isinstance(payload, dict) else payload
    if not isinstance(records, list) or not all(isinstance(record, dict) for record in records):
        raise ValueError("metadata must be a JSON list or an object with a references list")
    return {str(record.get("doi", "")).casefold(): record for record in records}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate DOI syntax and official metadata verification from a UTF-8 DOI list.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    findings: list[dict[str, str | int]] = []
    try:
        metadata = load_metadata(args.metadata)
        values = args.source.read_text(encoding="utf-8").splitlines()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        findings.append(finding("REF-DOI-000", "critical", str(args.source), str(error), "Provide readable DOI and official-metadata files."))
        values = []
        metadata = {}
    for number, value in enumerate(values, start=1):
        doi = value.strip().removeprefix("https://doi.org/").rstrip(".,;")
        if not doi:
            continue
        if not DOI_PATTERN.fullmatch(doi):
            findings.append(finding("REF-DOI-002", "major", str(args.source), value, "Correct the DOI against publisher metadata.", number))
            continue
        record = metadata.get(doi.casefold())
        if not record or record.get("metadata_status") != "official_verified" or not str(record.get("verification_source", "")).strip():
            findings.append(finding("REF-DOI-003", "major", str(args.source), doi, "Record official metadata verification for this DOI before using it in a submission bibliography.", number))
    print(json.dumps(findings, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] in {"critical", "major"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
