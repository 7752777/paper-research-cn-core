from __future__ import annotations

import argparse
import csv
from pathlib import Path


ACTIVE_ARCHIVES = {".zip", ".rar", ".7z"}
CACHE_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "node_modules"}


def classify(path: Path, root: Path) -> str | None:
    parts = set(path.parts)
    if "99_archive" in parts or "08_工作区_旧结构" in parts or "09_压缩包与备份" in parts:
        return None
    if path.name in CACHE_NAMES:
        return "cache/environment outside archive"
    if path.is_file() and path.suffix.casefold() in ACTIVE_ARCHIVES and "09_压缩包与备份" not in parts:
        return "active archive package outside backup folder"
    if path.is_file() and path.name.casefold() in {"desktop.ini", "thumbs.db"}:
        return "system file"
    if path.is_file() and len(path.relative_to(root).parts) > 8 and "08_工作区_旧结构" not in parts:
        return "deeply nested active file"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--csv", type=Path)
    args = parser.parse_args()

    root = args.project_root.resolve()
    rows: list[dict[str, str]] = []
    for path in root.rglob("*"):
        reason = classify(path, root)
        if reason:
            rows.append({"path": path.relative_to(root).as_posix(), "kind": "dir" if path.is_dir() else "file", "reason": reason})
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["path", "kind", "reason"])
            writer.writeheader()
            writer.writerows(rows)
    print(f"structure_findings={len(rows)}")
    for row in rows[:200]:
        print(f"{row['reason']}: {row['path']}")
    return 1 if rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
