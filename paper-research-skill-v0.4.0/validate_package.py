from __future__ import annotations

import py_compile
import re
from pathlib import Path

from install import SKILL_NAMES, discover_skills


REFERENCE_PATTERN = re.compile(r"`((?:references|scripts|agents)/[^`]+)`")


def _frontmatter_value(text: str, key: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    for line in text[4:end].splitlines():
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip().strip('"')
    return None


def validate_package(root: Path) -> list[str]:
    errors: list[str] = []
    installed = set(discover_skills(root))
    expected = set(SKILL_NAMES)
    if installed != expected:
        errors.append(f"SKILL-SET-001 expected {sorted(expected)}, found {sorted(installed)}")

    for name in SKILL_NAMES:
        skill_root = root / "skills" / name
        skill_file = skill_root / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"SKILL-FILE-001 {name} is missing SKILL.md")
            continue
        text = skill_file.read_text(encoding="utf-8")
        if _frontmatter_value(text, "name") != name:
            errors.append(f"SKILL-META-001 {name} frontmatter name does not match directory")
        if not _frontmatter_value(text, "description"):
            errors.append(f"SKILL-META-002 {name} has no description")
        for reference in REFERENCE_PATTERN.findall(text):
            if not (skill_root / reference).is_file():
                errors.append(f"SKILL-LINK-001 {name} references missing {reference}")
        for path in skill_root.rglob("*.py"):
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as error:
                errors.append(f"SKILL-PY-001 {path.relative_to(root)}: {error.msg}")
        for reference in (skill_root / "references").glob("*.md") if (skill_root / "references").exists() else []:
            if len(reference.read_text(encoding="utf-8").strip()) < 120:
                errors.append(f"SKILL-REF-001 {reference.relative_to(root)} is too short to be actionable")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parent
    errors = validate_package(root)
    if errors:
        print("\n".join(errors))
        return 1
    print("package validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
