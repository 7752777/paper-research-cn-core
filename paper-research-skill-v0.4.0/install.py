from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


SKILL_NAMES = (
    "paper-research-cn-core",
    "paper-manuscript-cn-core",
    "paper-figure-cn-core",
    "paper-reference-cn-core",
    "paper-review-cn-core",
    "paper-submission-cn-core",
)


def discover_skills(root: Path) -> list[str]:
    skills_root = root / "skills"
    return sorted(
        path.name for path in skills_root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    )


def default_destination(target: str) -> Path:
    home = Path.home()
    if target == "codex":
        return home / ".codex" / "skills"
    if target == "claude":
        return home / ".claude" / "skills"
    return Path.cwd() / ".agents" / "skills"


def install(root: Path, destination: Path, *, dry_run: bool, force: bool) -> list[dict[str, str]]:
    available = set(discover_skills(root))
    missing = sorted(set(SKILL_NAMES) - available)
    if missing:
        raise ValueError(f"package is incomplete: {', '.join(missing)}")

    actions: list[dict[str, str]] = []
    for name in SKILL_NAMES:
        source = root / "skills" / name
        target = destination / name
        if target.exists() and not force:
            actions.append({"skill": name, "action": "skipped", "target": str(target)})
            continue
        actions.append({"skill": name, "action": "install" if not target.exists() else "replace", "target": str(target)})
        if dry_run:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return actions


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the six Chinese-core-paper skills without touching unrelated skills.")
    parser.add_argument("--target", choices=("codex", "claude", "agents"), default="codex")
    parser.add_argument("--destination", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    destination = args.destination or default_destination(args.target)
    try:
        actions = install(root, destination, dry_run=args.dry_run, force=args.force)
    except ValueError as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"destination": str(destination), "dry_run": args.dry_run, "actions": actions}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
