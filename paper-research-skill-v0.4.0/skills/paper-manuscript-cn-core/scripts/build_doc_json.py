from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
TABLE_CAPTION_PATTERN = re.compile(r"^表\s*\d+")
FIGURE_CAPTION_PATTERN = re.compile(r"^图\s*\d+")
BIB_ENTRY_PATTERN = re.compile(r"@(?P<kind>\w+)\s*\{[^,]+,(?P<body>.*?)\n\}", re.DOTALL)
BIB_FIELD_PATTERN = re.compile(r"(?P<key>\w+)\s*=\s*\{(?P<value>[^{}]*)\}")


def _metadata(text: str) -> tuple[dict[str, str], int]:
    if not text.startswith("---"):
        return {}, 0
    closing = text.find("\n---", 3)
    if closing < 0:
        return {}, 0
    values: dict[str, str] = {}
    for line in text[3:closing].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    return values, text[: closing + 5].count("\n")


def _table(markdown: list[str], caption: str) -> dict[str, object]:
    return {"type": "table", "caption": caption, "markdown": markdown}


def _bibliography_entries(path: Path) -> list[str]:
    if not path.is_file():
        return []
    entries: list[str] = []
    for index, match in enumerate(BIB_ENTRY_PATTERN.finditer(path.read_text(encoding="utf-8")), start=1):
        fields = {item.group("key").lower(): item.group("value").strip() for item in BIB_FIELD_PATTERN.finditer(match.group("body"))}
        author = fields.get("author", "").replace(" and ", ", ")
        title = fields.get("title", "")
        journal = fields.get("journal", "")
        year = fields.get("year", "")
        volume = fields.get("volume", "")
        issue = f"({fields['number']})" if fields.get("number") else ""
        pages = fields.get("pages", "").replace("--", "-")
        doi = f" DOI: {fields['doi']}." if fields.get("doi") else ""
        marker = "J" if match.group("kind").lower() == "article" else "M"
        if author and title and journal and year:
            publication = f"{journal}, {year}"
            if volume:
                publication += f", {volume}{issue}"
            if pages:
                publication += f": {pages}"
            entries.append(f"[{index}] {author}. {title}[{marker}]. {publication}.{doi}")
    return entries


def build_document(source: Path) -> dict[str, object]:
    text = source.read_text(encoding="utf-8")
    metadata, content_start = _metadata(text)
    sections: list[dict[str, object]] = []
    tables: list[dict[str, object]] = []
    figures: list[dict[str, str]] = []
    blocks: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    pending_table_caption = ""
    pending_figure_caption = ""
    table_lines: list[str] = []
    has_reference_heading = False
    lines = text.splitlines()

    def flush_table() -> None:
        nonlocal table_lines, pending_table_caption
        if table_lines:
            value = _table(table_lines, pending_table_caption)
            tables.append(value)
            blocks.append(value)
            table_lines = []
            pending_table_caption = ""

    for line in lines[content_start:]:
        stripped = line.strip()
        if line.startswith("|"):
            table_lines.append(line)
            continue
        flush_table()
        if not stripped:
            continue
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            level = len(line) - len(line.lstrip("#"))
            current = {"level": level, "title": title, "paragraphs": []}
            sections.append(current)
            if not (level == 1 and title == metadata.get("title")):
                blocks.append({"type": "heading", "level": level, "text": title})
            has_reference_heading = has_reference_heading or title == "参考文献"
            continue
        if TABLE_CAPTION_PATTERN.match(stripped):
            pending_table_caption = stripped
            continue
        if FIGURE_CAPTION_PATTERN.match(stripped):
            pending_figure_caption = stripped
            continue
        image = IMAGE_PATTERN.search(line)
        if image:
            value = {"type": "figure", "caption": pending_figure_caption or image.group(1), "path": image.group(2), "alt": image.group(1)}
            figures.append(value)
            blocks.append(value)
            pending_figure_caption = ""
            continue
        value = {"type": "paragraph", "text": stripped}
        blocks.append(value)
        if current:
            current["paragraphs"].append(stripped)
    flush_table()
    reference_entries = _bibliography_entries(source.parent / metadata.get("bibliography", "")) if has_reference_heading else []
    blocks.extend({"type": "paragraph", "text": entry} for entry in reference_entries)
    return {
        "title": metadata.get("title", source.stem),
        "source": str(source),
        "sections": sections,
        "blocks": blocks,
        "tables": tables,
        "figures": figures,
        "references": reference_entries,
        "audit_inputs": {},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the shared ordered doc.json contract from a Markdown or Quarto manuscript.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    document = build_document(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
