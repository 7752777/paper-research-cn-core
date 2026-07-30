from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
CAPTION_PATTERN = re.compile(r"^(?:图|表)\s*\d+[^\n]*$", re.MULTILINE)


def finding(rule_id: str, severity: str, evidence: str, remediation: str, file: str) -> dict[str, str]:
    return {"rule_id": rule_id, "severity": severity, "file": file, "evidence": evidence, "remediation": remediation}


def audit_markdown(text: str, root: Path, file: str = "<memory>") -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        caption = line.strip()
        if not CAPTION_PATTERN.fullmatch(caption):
            continue
        end = len(lines)
        for following, candidate in enumerate(lines[index + 1 :], start=index + 1):
            if CAPTION_PATTERN.fullmatch(candidate.strip()):
                end = following
                break
        context = " ".join(lines[index:end])
        if not re.search(r"(?:n\s*=|分母|多重编码|统计口径|非统计图)", context, re.IGNORECASE):
            findings.append(finding("FIG-CAPTION-001", "major", caption, "State the denominator, statistical definition, and multiple-coding limit in the caption note.", file))
    for index, line in enumerate(lines):
        image_match = IMAGE_PATTERN.search(line)
        if not image_match:
            continue
        image = image_match.group(1)
        path = root / image
        if path.suffix.lower() in {".png", ".jpg", ".jpeg"} and not path.with_suffix(".svg").is_file():
            findings.append(finding("FIG-VECTOR-001", "major", image, "Retain a matching SVG or PDF source asset for journal layout and render regression checks.", file))
        if not path.is_file():
            findings.append(finding("FIG-FILE-001", "critical", image, "Correct the image path or regenerate the figure asset.", file))
        nearby = [lines[candidate].strip() for candidate in range(max(0, index - 3), index)]
        if not any(CAPTION_PATTERN.fullmatch(candidate) for candidate in nearby):
            findings.append(finding("FIG-CAPTION-002", "major", image, "Add a numbered figure caption immediately before the image, including denominator and coding notes.", file))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit figure assets and captions in a Markdown or Quarto manuscript.")
    parser.add_argument("file", type=Path)
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()
    root = args.root or args.file.parent
    findings = audit_markdown(args.file.read_text(encoding="utf-8"), root, str(args.file))
    print(json.dumps(findings, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] in {"critical", "major"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
