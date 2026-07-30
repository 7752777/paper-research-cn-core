from __future__ import annotations

import argparse
import csv
from pathlib import Path


def csv_to_markdown(source: Path) -> str:
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return ""
    header = rows[0]
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows[1:])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a CSV data table to a Markdown source suitable for three-line journal table rendering.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(csv_to_markdown(args.source), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
