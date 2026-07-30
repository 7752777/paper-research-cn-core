from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


SKILL_NAMES = ("paper-research-cn-core",)
LEGACY_SKILL_NAMES = (
    "paper-manuscript-cn-core",
    "paper-figure-cn-core",
    "paper-reference-cn-core",
    "paper-review-cn-core",
    "paper-submission-cn-core",
)


def discover_skills(root: Path) -> list[str]:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return []
    return sorted(path.name for path in skills_root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())


def default_destination(target: str) -> Path:
    home = Path.home()
    if target == "codex":
        return home / ".codex" / "skills"
    if target == "claude":
        return home / ".claude" / "skills"
    return Path.cwd() / ".agents" / "skills"


def prune_legacy(destination: Path, *, dry_run: bool) -> list[dict[str, str]]:
    actions: list[dict[str, str]] = []
    for name in LEGACY_SKILL_NAMES:
        target = destination / name
        if not target.exists():
            continue
        actions.append({"skill": name, "action": "remove", "target": str(target)})
        if not dry_run:
            shutil.rmtree(target)
    return actions


def install(root: Path, destination: Path, *, dry_run: bool, force: bool, prune_legacy_skills: bool) -> list[dict[str, str]]:
    available = set(discover_skills(root))
    if available != set(SKILL_NAMES):
        raise ValueError(f"package must contain only {SKILL_NAMES[0]}, found {sorted(available)}")

    source = root / "skills" / SKILL_NAMES[0]
    target = destination / SKILL_NAMES[0]
    actions: list[dict[str, str]] = []
    if target.exists() and not force:
        actions.append({"skill": SKILL_NAMES[0], "action": "skipped", "target": str(target)})
    else:
        actions.append({"skill": SKILL_NAMES[0], "action": "replace" if target.exists() else "install", "target": str(target)})
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    if prune_legacy_skills:
        actions.extend(prune_legacy(destination, dry_run=dry_run))
    return actions


def main() -> int:
    parser = argparse.ArgumentParser(description="Install one Chinese-core-paper skill and optionally remove only its five retired split skills.")
    parser.add_argument("--target", choices=("codex", "claude", "agents"), default="codex")
    parser.add_argument("--destination", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--prune-legacy", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    destination = args.destination or default_destination(args.target)
    try:
        actions = install(root, destination, dry_run=args.dry_run, force=args.force, prune_legacy_skills=args.prune_legacy)
    except ValueError as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"destination": str(destination), "dry_run": args.dry_run, "actions": actions}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
