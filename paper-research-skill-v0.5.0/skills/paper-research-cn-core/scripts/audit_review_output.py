from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROUND_NAMES = ("第一轮", "第二轮", "第三轮")
REQUIRED_FIELDS = ("严重度", "位置", "证据", "建议", "验证")
SAMPLE_FIELDS = ("引文抽样", "参考文献抽样", "图表抽样")
ROUND_HEADER = re.compile(r"^##\s*(第一轮|第二轮|第三轮)[^\n]*$", re.MULTILINE)
COUNT_PATTERN = re.compile(r"轮次计数\s*[：:]\s*Critical\s*(\d+)\s*[；;，,]\s*Major\s*(\d+)\s*[；;，,]\s*Minor\s*(\d+)", re.IGNORECASE)
SAMPLE_PATTERN = r"(?:\d+\s*/\s*\d+|全部|不适用)"


def finding(rule_id: str, severity: str, file: str, evidence: str, remediation: str) -> dict[str, str]:
    return {"rule_id": rule_id, "severity": severity, "file": file, "evidence": evidence, "remediation": remediation}


def round_sections(text: str) -> dict[str, str]:
    matches = list(ROUND_HEADER.finditer(text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1)] = text[match.start() : end]
    return sections


def is_chinese_review(text: str) -> bool:
    chinese = len(re.findall(r"[\u4e00-\u9fff]", text))
    letters = len(re.findall(r"[A-Za-z\u4e00-\u9fff]", text))
    return chinese >= 80 and chinese / max(letters, 1) >= 0.35


def audit_review(text: str, file: str = "<memory>") -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not is_chinese_review(text):
        findings.append(finding("REVIEW-LANG-001", "major", file, "review record is not predominantly Chinese", "Write the manuscript review and author-facing evidence in Chinese."))

    sections = round_sections(text)
    for round_name in ROUND_NAMES:
        section = sections.get(round_name)
        if not section:
            findings.append(finding("REVIEW-ROUND-001", "major", file, f"missing section for {round_name}", "Record three independent review rounds with separate evidence."))
            continue
        missing_fields = [field for field in REQUIRED_FIELDS if field not in section]
        if missing_fields:
            findings.append(finding("REVIEW-STRUCT-001", "major", file, f"{round_name} missing fields: {', '.join(missing_fields)}", "Give every review item severity, location, evidence, recommendation, and verification."))
        count_match = COUNT_PATTERN.search(section)
        if not count_match:
            findings.append(finding("REVIEW-ROUND-COUNT-001", "major", file, f"{round_name} lacks Critical/Major/Minor recount", "State the three severity counts separately in every round."))
            critical = major = 0
        else:
            critical, major, _minor = (int(value) for value in count_match.groups())
            if critical:
                findings.append(finding("REVIEW-UNRESOLVED-CRITICAL", "critical", file, f"{round_name} reports Critical={critical}", "Resolve every Critical finding and regenerate the independent review record."))
            if major:
                findings.append(finding("REVIEW-UNRESOLVED-MAJOR", "major", file, f"{round_name} reports Major={major}", "Resolve every Major finding or keep the manuscript out of the submission package."))
        for sample in SAMPLE_FIELDS:
            if not re.search(rf"{sample}\s*[：:][^\n]*{SAMPLE_PATTERN}", section):
                findings.append(finding("REVIEW-SAMPLE-001", "major", file, f"{round_name} lacks verifiable {sample}", "Record a sample size or mark the item not applicable in this review round."))
        if critical + major == 0 and "逐项排除" not in section:
            findings.append(finding("REVIEW-RUBBER-001", "major", file, f"{round_name} reports zero Critical/Major without an exclusion record", "List the checked problem, evidence, method, statistics, claims, figures, references, and style categories."))
        if "限制回写位置" not in section:
            findings.append(finding("REVIEW-REWRITE-001", "major", file, f"{round_name} does not locate limitation write-back in the manuscript", "State where the identified boundary was written back into methods, results, or discussion."))

    if "全部已解决" in text and "逐项排除" not in text:
        findings.append(finding("REVIEW-RUBBER-002", "major", file, "claims all issues are solved without itemized exclusion", "Replace the claim with evidence from the final independent review."))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Chinese review records for independent rounds, evidence fields, and anti-rubber-stamp compliance.")
    parser.add_argument("review_file", type=Path)
    args = parser.parse_args()
    findings = audit_review(args.review_file.read_text(encoding="utf-8"), str(args.review_file))
    print(json.dumps(findings, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] in {"critical", "major"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
