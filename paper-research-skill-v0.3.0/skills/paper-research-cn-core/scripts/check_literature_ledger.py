from __future__ import annotations

import argparse
import csv
from pathlib import Path


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger")
    parser.add_argument("--require-cnki", action="store_true")
    parser.add_argument("--min-downloaded", type=int, default=0)
    args = parser.parse_args()

    path = Path(args.ledger)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        columns = set(reader.fieldnames or [])

    errors: list[str] = []
    missing = sorted(REQUIRED - columns)
    if missing:
        errors.append("missing columns: " + ", ".join(missing))
    statuses = {row.get("fulltext_status", "") for row in rows}
    bad_status = sorted(status for status in statuses if status and status not in ALLOWED_FULLTEXT)
    if bad_status:
        errors.append("bad fulltext_status: " + ", ".join(bad_status))
    downloaded = sum(row.get("fulltext_status") == "downloaded" for row in rows)
    cnki = sum("cnki" in " ".join(row.values()).casefold() or "知网" in " ".join(row.values()) for row in rows)
    if args.require_cnki and cnki == 0:
        errors.append("no CNKI/知网 records found")
    if downloaded < args.min_downloaded:
        errors.append(f"downloaded full text below threshold: {downloaded} < {args.min_downloaded}")

    print(f"rows={len(rows)} cnki={cnki} downloaded={downloaded}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
