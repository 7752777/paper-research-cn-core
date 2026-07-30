from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


BLOCKERS = {
    "MANUSCRIPT-RESIDUE-001": re.compile(r"\.(csv|xlsx|qmd|docx|py|log)\b|C:\\|/Users/|scripts?[\\/]|logs?[\\/]", re.I),
    "MANUSCRIPT-WORKFLOW-001": re.compile(r"交付物|待确认|本轮|旧样本|修订过程|工具调用|模型输出|运行结果|artifact|deliverable|workflow|TODO", re.I),
    "MANUSCRIPT-VENUE-001": re.compile(r"\[VENUE RULE UNVERIFIED\]"),
    "MANUSCRIPT-PVALUE-001": re.compile(r"p\s*=\s*<"),
}
OVERCLAIM = re.compile(r"首次|填补空白|证明|显著提升|有效治理|完全解决")
LIMIT_WORDS = re.compile(r"局限|不足|缺陷|无法|仅仅|初步|有待")


def finding(rule_id: str, severity: str, file: str, evidence: str, remediation: str) -> dict[str, str]:
    return {"rule_id": rule_id, "severity": severity, "file": file, "evidence": evidence, "remediation": remediation}


def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"[。！？]\s*", text) if part.strip()]


def audit_text(text: str, file: str = "<memory>", max_long_sentences: int = 8) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for rule_id, pattern in BLOCKERS.items():
        match = pattern.search(text)
        if match:
            findings.append(finding(rule_id, "critical", file, match.group(0), "Remove project-process residue and repair the manuscript before submission."))
    if OVERCLAIM.search(text):
        findings.append(finding("MANUSCRIPT-CLAIM-001", "minor", file, "possible overclaim wording", "Tie the claim to the evidence strength or recast it as a bounded interpretation."))
    if len(LIMIT_WORDS.findall(text)) > 35:
        findings.append(finding("MANUSCRIPT-STYLE-001", "minor", file, "excessive limitation wording", "Separate concrete limitations from the supported contribution and avoid repetitive apology phrasing."))
    long_sentences = [sentence for sentence in split_sentences(text) if len(sentence) > 110]
    if len(long_sentences) > max_long_sentences:
        findings.append(finding("MANUSCRIPT-STYLE-002", "minor", file, f"long_sentences={len(long_sentences)}; threshold={max_long_sentences}", "Split long sentences where this improves the argument and citation traceability."))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a manuscript for process residue, unsupported venue text, and common overclaim patterns.")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--max-long-sentences", type=int, default=8)
    args = parser.parse_args()
    try:
        findings = audit_text(args.manuscript.read_text(encoding="utf-8", errors="ignore"), str(args.manuscript), args.max_long_sentences)
    except OSError as error:
        findings = [finding("MANUSCRIPT-READ-001", "critical", str(args.manuscript), str(error), "Provide a readable manuscript source file.")]
    print(json.dumps({"findings": findings}, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] in {"critical", "major"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
