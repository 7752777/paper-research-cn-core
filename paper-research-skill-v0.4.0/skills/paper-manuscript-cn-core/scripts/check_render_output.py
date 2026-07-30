from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check that rendered DOCX/PDF outputs exist and are non-empty.")
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    findings = []
    for path in args.files:
        if not path.is_file() or path.stat().st_size == 0:
            findings.append({"rule_id": "RENDER-001", "severity": "critical", "file": str(path), "evidence": "missing or empty render", "remediation": "rerun the renderer and inspect its input."})
    print(json.dumps(findings, ensure_ascii=False, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
