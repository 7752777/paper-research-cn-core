from __future__ import annotations

import argparse
import json
from pathlib import Path


def format_article(item: dict[str, str]) -> str:
    required = ("author", "title", "journal", "year", "volume", "pages")
    missing = [key for key in required if not item.get(key)]
    if missing:
        raise ValueError(f"missing official metadata fields: {', '.join(missing)}")
    issue = f"({item['issue']})" if item.get("issue") else ""
    doi = f". DOI: {item['doi']}" if item.get("doi") else ""
    return f"{item['author']}. {item['title']}[J]. {item['journal']}, {item['year']}, {item['volume']}{issue}: {item['pages']}{doi}."


def main() -> int:
    parser = argparse.ArgumentParser(description="Format verified article metadata as GB/T 7714 candidate references.")
    parser.add_argument("source", type=Path, help="JSON array of verified article metadata")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        values = json.loads(args.source.read_text(encoding="utf-8"))
        lines = [f"[{index}] {format_article(item)}" for index, item in enumerate(values, start=1)]
    except (json.JSONDecodeError, ValueError) as error:
        print(str(error))
        return 1
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
