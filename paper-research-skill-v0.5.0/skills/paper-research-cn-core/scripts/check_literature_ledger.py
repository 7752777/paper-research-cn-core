from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


REQUIRED = {
    "id",
    "title",
    "authors",
    "year",
    "journal",
    "source_database",
    "journal_tier",
    "search_query",
    "fulltext_status",
    "inclusion_decision",
}
ALLOWED_FULLTEXT = {"downloaded", "metadata-only", "abstract-only", "unavailable", "excluded"}
BLOCKING = {"critical", "major"}


def finding(rule_id: str, severity: str, file: str, evidence: str, remediation: str) -> dict[str, str]:
    return {"rule_id": rule_id, "severity": severity, "file": file, "evidence": evidence, "remediation": remediation}


def audit_ledger(path: Path, require_cnki: bool = False, min_downloaded: int = 0) -> tuple[dict[str, int], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        columns = set(reader.fieldnames or [])

    findings: list[dict[str, str]] = []
    missing = sorted(REQUIRED - columns)
    if missing:
        findings.append(finding("LEDGER-SCHEMA-001", "critical", str(path), f"missing columns: {', '.join(missing)}", "Add all required evidence-ledger fields before using the records in a research sample."))
    statuses = {row.get("fulltext_status", "") for row in rows}
    bad_status = sorted(status for status in statuses if status and status not in ALLOWED_FULLTEXT)
    if bad_status:
        findings.append(finding("LEDGER-FULLTEXT-001", "major", str(path), f"unsupported fulltext_status values: {', '.join(bad_status)}", "Use a declared full-text status and retain the corresponding acquisition evidence."))
    downloaded = sum(row.get("fulltext_status") == "downloaded" for row in rows)
    cnki = sum("cnki" in " ".join(row.values()).casefold() or "知网" in " ".join(row.values()) for row in rows)
    if require_cnki and cnki == 0:
        findings.append(finding("LEDGER-CNKI-001", "major", str(path), "no CNKI records found", "Record an authorized CNKI search or disclose why it is outside the research scope."))
    if downloaded < min_downloaded:
        findings.append(finding("LEDGER-FULLTEXT-002", "major", str(path), f"downloaded={downloaded}; minimum={min_downloaded}", "Acquire the declared minimum number of full texts or lower the claim strength and disclose the limitation."))
    return {"rows": len(rows), "cnki": cnki, "downloaded": downloaded}, findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the evidence-ledger schema, full-text statuses, and Chinese-source coverage.")
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--require-cnki", action="store_true")
    parser.add_argument("--min-downloaded", type=int, default=0)
    args = parser.parse_args()
    try:
        summary, findings = audit_ledger(args.ledger, args.require_cnki, args.min_downloaded)
    except (OSError, csv.Error, UnicodeError) as error:
        summary, findings = {}, [finding("LEDGER-READ-001", "critical", str(args.ledger), str(error), "Provide a readable UTF-8 CSV evidence ledger.")]
    print(json.dumps({"summary": summary, "findings": findings}, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] in BLOCKING for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
