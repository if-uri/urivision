#!/usr/bin/env python3
"""Run the four-profile backend contract matrix without requiring Docker daemon."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from urivision.platforms import DEFAULT_MATRIX
from tools.probe_runtime import run_probe


def to_markdown(matrix: dict) -> str:
    rows = ["# URI Runtime backend matrix", "", "| Profile | OS family | Stack | Kind | Result | Steps | Limitations |", "|---|---:|---|---|---:|---:|---|"]
    for item in matrix["results"]:
        info = item.get("profile_info") or {}
        limitations = "<br>".join(info.get("limitations", [])[:3])
        rows.append(
            f"| `{item['profile']}` | {info.get('os_family')} | {info.get('display_stack')} | {info.get('profile_kind')} | {'OK' if item.get('ok') else 'FAIL'} | {item['summary']['passed_steps']}/{item['summary']['steps']} | {limitations} |"
        )
    rows.append("")
    rows.append("## Important")
    rows.append("")
    rows.append("Linux Docker cannot execute real Windows UIA or macOS AX APIs. Those two rows validate URI contracts, payload schemas and orchestration behavior only. Native adapters must be tested on real Windows/macOS hosts.")
    return "\n".join(rows) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profiles", nargs="*", default=DEFAULT_MATRIX)
    ap.add_argument("--out", default="artifacts/backend-matrix.json")
    ap.add_argument("--markdown", default="artifacts/backend-matrix.md")
    args = ap.parse_args()

    results = [run_probe(profile) for profile in args.profiles]
    matrix = {"ok": all(r.get("ok") for r in results), "profiles": args.profiles, "results": results}

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(matrix, ensure_ascii=False, indent=2), encoding="utf-8")
    md = Path(args.markdown)
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(to_markdown(matrix), encoding="utf-8")
    print(json.dumps(matrix, ensure_ascii=False, indent=2))
    return 0 if matrix["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
