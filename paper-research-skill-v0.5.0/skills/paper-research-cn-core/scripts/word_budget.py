from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def section_counts(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    section = "未分节"
    for line in text.splitlines():
        if line.startswith("#"):
            section = line.lstrip("#").strip()
            counts.setdefault(section, 0)
        elif line.strip() and not line.startswith("---") and ":" not in line[:24]:
            counts[section] = counts.get(section, 0) + len(re.sub(r"\s+", "", line))
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Report section-level character counts for a manuscript budget.")
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    counts = section_counts(args.file.read_text(encoding="utf-8"))
    print(json.dumps({"total": sum(counts.values()), "sections": counts}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
