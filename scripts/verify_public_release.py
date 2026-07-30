from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_EXTENSIONS = {".pdf", ".caj", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".zip", ".rar", ".7z"}
TEXT_EXTENSIONS = {".md", ".yaml", ".yml", ".json", ".py", ".ps1", ".txt"}
SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)(password|token|cookie)\s*=\s*[^\s]+"),
    re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s`]+"),
]


def main() -> int:
    errors: list[str] = []
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            errors.append(f"forbidden binary/document extension: {rel}")
        if "__pycache__" in path.parts:
            errors.append(f"python cache copied: {rel}")
        if path.stat().st_size > 2_000_000:
            errors.append(f"large file over 2MB: {rel}")
        if path.suffix.lower() in TEXT_EXTENSIONS:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    errors.append(f"secret-like or local-path pattern {pattern.pattern}: {rel}")
    print(f"checked_files={len(files)}")
    print(f"errors={len(errors)}")
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
