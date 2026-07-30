from __future__ import annotations

import argparse
import re
from pathlib import Path


BLOCKERS = {
    "file extension/source residue": re.compile(r"\.(csv|xlsx|qmd|docx|py|log)\b|C:\\|/Users/|scripts?[\\/]|logs?[\\/]", re.I),
    "workflow wording": re.compile(r"交付物|待确认|本轮|旧样本|修订过程|工具调用|模型输出|运行结果|artifact|deliverable|workflow|TODO", re.I),
    "venue placeholder": re.compile(r"\[VENUE RULE UNVERIFIED\]"),
    "broken p-value": re.compile(r"p\s*=\s*<"),
}

OVERCLAIM = re.compile(r"首次|填补空白|证明|显著提升|有效治理|完全解决")
LIMIT_WORDS = re.compile(r"局限|不足|缺陷|无法|仅仅|初步|有待")


def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"[。！？!?]\s*", text) if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manuscript")
    parser.add_argument("--max-long-sentences", type=int, default=8)
    args = parser.parse_args()

    path = Path(args.manuscript)
    text = path.read_text(encoding="utf-8", errors="ignore")
    errors: list[str] = []
    warnings: list[str] = []

    for label, pattern in BLOCKERS.items():
        if pattern.search(text):
            errors.append(label)
    if OVERCLAIM.search(text):
        warnings.append("possible overclaim wording")
    if len(LIMIT_WORDS.findall(text)) > 35:
        warnings.append("possible apology drift / excessive limitation wording")
    long_sentences = [sentence for sentence in split_sentences(text) if len(sentence) > 110]
    if len(long_sentences) > args.max_long_sentences:
        warnings.append(f"many long sentences: {len(long_sentences)}")

    print(f"file={path}")
    print(f"errors={len(errors)} warnings={len(warnings)}")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
