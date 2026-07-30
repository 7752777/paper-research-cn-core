from __future__ import annotations

import re
from pathlib import Path

from install import SKILL_NAMES, discover_skills


REFERENCE_PATTERN = re.compile(r"`((?:references|scripts|agents)/[^`]+)`")


def frontmatter_value(text: str, key: str) -> str | None:
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
    if discover_skills(root) != list(SKILL_NAMES):
        errors.append(f"SKILL-SET-001 expected {list(SKILL_NAMES)}, found {discover_skills(root)}")
        return errors
    skill_root = root / "skills" / SKILL_NAMES[0]
    skill_file = skill_root / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    if frontmatter_value(text, "name") != SKILL_NAMES[0]:
        errors.append("SKILL-META-001 frontmatter name does not match the skill directory")
    if not frontmatter_value(text, "description"):
        errors.append("SKILL-META-002 skill has no description")
    for reference in REFERENCE_PATTERN.findall(text):
        if not (skill_root / reference).is_file():
            errors.append(f"SKILL-LINK-001 missing {reference}")
    for path in skill_root.rglob("*.py"):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except (SyntaxError, UnicodeDecodeError, ValueError) as error:
            errors.append(f"SKILL-PY-001 {path.relative_to(root)}: {getattr(error, 'msg', str(error))}")
    return errors


def main() -> int:
    errors = validate_package(Path(__file__).resolve().parent)
    if errors:
        print("\n".join(errors))
        return 1
    print("package validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
