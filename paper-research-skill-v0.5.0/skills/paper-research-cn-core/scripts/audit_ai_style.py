from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


BLOCKING_TERMS = ("投稿", "评审", "审稿意见", "目标期刊", "返修", "专栏契合")
NEGATION_PATTERN = re.compile(r"(?:不是|并非|不在于).{0,24}(?:而是|而在于)")


def finding(rule_id: str, severity: str, evidence: str, remediation: str, file: str = "<memory>") -> dict[str, str]:
    return {"rule_id": rule_id, "severity": severity, "file": file, "evidence": evidence, "remediation": remediation}


def audit_text(text: str, file: str = "<memory>") -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for term in BLOCKING_TERMS:
        if term in text:
            findings.append(finding("AI-STYLE-001", "major", f"正文包含元话语：{term}", "将投稿、评审和修订过程信息移至项目记录，不进入论文正文。", file))
            break
    density = len(NEGATION_PATTERN.findall(text)) * 10_000 / max(len(text), 1)
    if density > 5:
        findings.append(finding("AI-STYLE-002", "major", f"转折否定句密度为 {density:.1f}/万字", "保留必要的辨析句，其余改为直接陈述并检查论证衔接。", file))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Chinese manuscript prose for submission meta-language and repetitive AI-like contrast patterns.")
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    findings = audit_text(args.file.read_text(encoding="utf-8"), str(args.file))
    print(json.dumps(findings, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] in {"critical", "major"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
