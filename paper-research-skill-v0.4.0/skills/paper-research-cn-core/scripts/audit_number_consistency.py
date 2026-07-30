#!/usr/bin/env python3
"""Audit flow totals and multi-coded dimensions in evidence-map data."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any


BLOCKING_SEVERITIES = {"critical", "major"}


def finding(rule_id: str, severity: str, evidence: str, remediation: str, file: str = "<memory>") -> dict[str, str]:
    return {
        "rule_id": rule_id,
        "severity": severity,
        "file": file,
        "evidence": evidence,
        "remediation": remediation,
    }


def as_int(value: Any, label: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be an integer")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be an integer") from exc


def audit_payload(payload: dict[str, Any], file: str = "<memory>") -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    flow = payload.get("flow")
    if isinstance(flow, dict):
        identified = as_int(flow.get("identified"), "flow.identified")
        excluded = flow.get("excluded", {})
        outputs = flow.get("outputs", {})
        if not isinstance(excluded, dict) or not isinstance(outputs, dict):
            raise ValueError("flow.excluded and flow.outputs must be objects")
        excluded_total = sum(as_int(value, f"flow.excluded.{key}") for key, value in excluded.items())
        output_total = sum(as_int(value, f"flow.outputs.{key}") for key, value in outputs.items())
        retained = identified - excluded_total
        if retained != output_total:
            findings.append(
                finding(
                    "NUM-FLOW-001",
                    "critical",
                    f"identified={identified}; excluded={excluded_total}; retained={retained}; outputs={output_total}",
                    "Reconcile every record role so the flow closes before publishing any denominator or figure.",
                    file,
                )
            )

    dimensions = payload.get("dimensions", [])
    if not isinstance(dimensions, list):
        raise ValueError("dimensions must be a list")
    for dimension in dimensions:
        if not isinstance(dimension, dict):
            raise ValueError("each dimension must be an object")
        name = str(dimension.get("name", "unnamed dimension"))
        total = as_int(dimension.get("total"), f"dimensions.{name}.total")
        denominator = as_int(dimension.get("denominator"), f"dimensions.{name}.denominator")
        if total > denominator and not bool(dimension.get("multiple")):
            findings.append(
                finding(
                    "NUM-MULTI-001",
                    "major",
                    f"dimension={name}; total={total}; denominator={denominator}; multiple=false",
                    "Mark the dimension as multi-coded and state this in the method, table note, and figure caption.",
                    file,
                )
            )
    return findings


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="JSON audit payload")
    args = parser.parse_args(list(argv) if argv is not None else None)
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    results = audit_payload(payload, str(args.input))
    print(json.dumps({"findings": results}, ensure_ascii=False, indent=2))
    return 1 if any(item["severity"] in BLOCKING_SEVERITIES for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
