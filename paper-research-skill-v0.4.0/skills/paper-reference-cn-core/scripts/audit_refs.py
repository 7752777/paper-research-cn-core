from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


JOURNAL_FIELDS = re.compile(r"\b\d{4}\s*,\s*(?:\d+\s*)?(?:\(\d+\))?\s*:\s*\d+(?:\s*[-–]\s*\d+)?")
THESIS_FIELDS = re.compile(r"\[D\].*[，,]\s*[^，,]+[，,]\s*\d{4}")
DOI_PATTERN = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)


def finding(rule_id: str, severity: str, line: int, evidence: str, remediation: str, file: str) -> dict[str, str | int]:
    return {"rule_id": rule_id, "severity": severity, "file": file, "line": line, "evidence": evidence, "remediation": remediation}


def journal_entries(text: str) -> list[tuple[int, str]]:
    return [(number, line.strip()) for number, line in enumerate(text.splitlines(), start=1) if "[J]" in line]


def audit_bibliography(text: str, file: str = "<memory>", metadata_records: list[dict[str, Any]] | None = None) -> list[dict[str, str | int]]:
    findings: list[dict[str, str | int]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if "[J]" in stripped and not JOURNAL_FIELDS.search(stripped):
            findings.append(finding("REF-GBT-001", "major", number, stripped, "Complete year, volume(issue), page range, and official metadata verification before using the journal reference.", file))
        if "[D]" in stripped and not THESIS_FIELDS.search(stripped):
            findings.append(finding("REF-GBT-002", "major", number, stripped, "Complete degree location, awarding institution, and year from official metadata.", file))
        if "doi" in stripped.lower() and not DOI_PATTERN.search(stripped):
            findings.append(finding("REF-DOI-001", "major", number, stripped, "Remove the invalid DOI or correct it against publisher metadata.", file))

    journals = journal_entries(text)
    if journals and metadata_records is None:
        for number, line in journals:
            findings.append(finding("REF-METADATA-001", "major", number, line, "Supply a metadata JSON record confirming official verification for every journal reference.", file))
        return findings
    metadata_records = metadata_records or []
    if journals and len(metadata_records) != len(journals):
        findings.append(finding("REF-METADATA-002", "major", 0, f"journal_entries={len(journals)}; metadata_records={len(metadata_records)}", "Provide one official metadata record for each journal reference in bibliography order.", file))
    for index, (number, line) in enumerate(journals):
        record = metadata_records[index] if index < len(metadata_records) else {}
        if record.get("metadata_status") != "official_verified" or not str(record.get("verification_source", "")).strip():
            findings.append(finding("REF-METADATA-001", "major", number, line, "Verify this entry against a publisher, journal, DOI registry, or other authoritative metadata source and record the status.", file))
            continue
        doi_match = DOI_PATTERN.search(line)
        if doi_match and str(record.get("doi", "")).casefold() != doi_match.group(0).rstrip(".,;").casefold():
            findings.append(finding("REF-METADATA-003", "major", number, line, "Make the metadata DOI match the bibliography DOI exactly before finalizing the reference.", file))
    return findings


def load_metadata(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("references") if isinstance(payload, dict) else payload
    if not isinstance(records, list) or not all(isinstance(record, dict) for record in records):
        raise ValueError("metadata must be a JSON list or an object with a references list")
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit GB/T 7714 bibliography lines, DOI syntax, and official metadata verification.")
    parser.add_argument("file", type=Path)
    parser.add_argument("--metadata", type=Path, help="JSON official-metadata records in bibliography order")
    args = parser.parse_args()
    try:
        records = load_metadata(args.metadata) if args.metadata else None
        findings = audit_bibliography(args.file.read_text(encoding="utf-8"), str(args.file), records)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        findings = [finding("REF-METADATA-000", "critical", 0, str(error), "Provide readable official metadata JSON before reference audit.", str(args.file))]
    print(json.dumps(findings, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] in {"critical", "major"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
