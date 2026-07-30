from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_ROUNDS = ("第一轮", "第二轮", "第三轮")
REQUIRED_FIELDS = ("严重度", "位置", "证据", "建议", "验证")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("review_file")
    args = parser.parse_args()
    text = Path(args.review_file).read_text(encoding="utf-8", errors="ignore")
    errors = []
    for item in REQUIRED_ROUNDS + REQUIRED_FIELDS:
        if item not in text:
            errors.append(f"missing marker: {item}")
    if len(re.findall(r"局限|不足|缺陷|无法|未能|仅仅", text)) > 40:
        errors.append("possible apology drift")
    for error in errors:
        print(f"ERROR: {error}")
    if not errors:
        print("review output structure OK")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
