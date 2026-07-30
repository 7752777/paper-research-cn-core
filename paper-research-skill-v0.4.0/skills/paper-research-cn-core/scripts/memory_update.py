from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


DEFAULT_MEMORY = Path.home() / ".codex" / "paper-research-cn-core" / "memory"
FORBIDDEN = ("password", "token", "cookie", "验证码", "账号", "机构账号", "CNKI全文", "论文全文")


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", type=Path, default=DEFAULT_MEMORY)
    parser.add_argument("--candidate")
    parser.add_argument("--category", default="workflow")
    parser.add_argument("--review", action="store_true")
    parser.add_argument("--promote")
    args = parser.parse_args()

    root = args.memory_root.resolve()
    candidates_path = root / "candidates.json"
    accepted_path = root / "accepted.json"
    candidates = load(candidates_path)
    accepted = load(accepted_path)

    if args.candidate:
        text = args.candidate.strip()
        if any(word.casefold() in text.casefold() for word in FORBIDDEN):
            print("ERROR: candidate contains forbidden private/credential wording")
            return 1
        candidates.append({
            "id": f"mem-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "category": args.category,
            "text": text,
            "status": "candidate",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "promotion_rule": "candidate -> reused successfully -> user/audit confirmed",
        })
        save(candidates_path, candidates)
    if args.promote:
        hit = next((item for item in candidates if item.get("id") == args.promote), None)
        if not hit:
            print(f"ERROR: candidate not found: {args.promote}")
            return 1
        hit["status"] = "accepted"
        hit["accepted_at"] = datetime.now().isoformat(timespec="seconds")
        accepted.append(hit)
        candidates = [item for item in candidates if item.get("id") != args.promote]
        save(candidates_path, candidates)
        save(accepted_path, accepted)
    if args.review or not (args.candidate or args.promote):
        print(f"memory_root={root}")
        print(f"candidates={len(candidates)} accepted={len(accepted)}")
        for item in candidates:
            print(f"{item.get('id')} [{item.get('category')}] {item.get('text')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
