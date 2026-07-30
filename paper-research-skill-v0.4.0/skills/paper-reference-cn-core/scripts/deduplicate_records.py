from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


def key_for(record: dict[str, str]) -> tuple[str, str]:
    doi = re.sub(r"\s+", "", record.get("doi", "").lower())
    title = re.sub(r"[\W_]", "", record.get("title", "").lower())
    return doi, title


def main() -> int:
    parser = argparse.ArgumentParser(description="Report candidate duplicate bibliographic records; it never deletes source records.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.source.open(encoding="utf-8-sig", newline="") as handle:
        records = list(csv.DictReader(handle))
    buckets: dict[tuple[str, str], list[dict[str, str]]] = {}
    for record in records:
        key = key_for(record)
        if key != ("", ""):
            buckets.setdefault(key, []).append(record)
    duplicates = [group for group in buckets.values() if len(group) > 1]
    args.output.write_text(json.dumps(duplicates, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
