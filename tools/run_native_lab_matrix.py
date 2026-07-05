#!/usr/bin/env python3
"""Generate native OS lab matrix and contract readiness report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from urivision.native_profiles import CORE_URIS, coverage_summary, list_native_targets, native_matrix_markdown
from urivision.method_router import INTENT_METHODS, route_intent
from urivision.runtime import default_runtime

JsonDict = dict[str, Any]


def contract_check() -> dict[str, Any]:
    rt = default_runtime()
    checks = []
    for uri in CORE_URIS:
        try:
            res = rt.explain(uri)
            checks.append({"uri": uri, "ok": bool(res.get("ok")), "capability": res.get("capability", {}).get("uri_pattern")})
        except Exception as exc:
            checks.append({"uri": uri, "ok": False, "error": str(exc)})
    return {"passed": all(c["ok"] for c in checks), "checks": checks}


def build_matrix() -> JsonDict:
    contract = contract_check()
    targets = []
    for target in list_native_targets():
        routes = {intent: route_intent(intent, target).to_dict() for intent in sorted(INTENT_METHODS)}
        target_contract_checks = []
        for uri in target.must_pass_uris:
            item = next((c for c in contract["checks"] if c["uri"] == uri), None)
            target_contract_checks.append(item or {"uri": uri, "ok": False, "error": "not in core contract"})
        targets.append({
            "profile": target.to_dict(),
            "contract": {
                "passed": all(c.get("ok") for c in target_contract_checks),
                "checks": target_contract_checks,
            },
            "routes": routes,
            "native_execution": {
                "status": "requires-native-runner",
                "runner_kind": target.runner_kind,
                "runner_labels": target.runner_labels,
                "evidence_required": target.evidence_required,
            },
        })
    return {
        "schema": "schema://runtime/native-lab-matrix.v1",
        "summary": coverage_summary(),
        "core_contract": contract,
        "targets": targets,
    }


def confidence_gate(matrix: JsonDict) -> str:
    targets = matrix["targets"]
    contract_failures = [t for t in targets if not t["contract"]["passed"]]
    native_required = [t for t in targets if t["native_execution"]["status"] == "requires-native-runner"]
    lines = [
        "# Native Lab Confidence Gate",
        "",
        "This is the acceptance checklist before claiming broad OS support.",
        "",
        "## Current generated state",
        "",
        f"- Native target profiles: {len(targets)}",
        f"- Core URI contract passed: {matrix['core_contract']['passed']}",
        f"- Contract failures: {len(contract_failures)}",
        f"- Profiles still requiring native evidence: {len(native_required)}",
        "",
        "## Gate G0 — architecture contract",
        "",
        "PASS when every target profile can resolve the core URI capabilities and MethodRouter has a selected route for the required intents.",
        "",
        "## Gate G1 — native smoke",
        "",
        "PASS when every priority OS family has at least one real self-hosted run producing: capability list, tree/screenshot evidence, one successful query, one command and one verified postcondition.",
        "",
        "## Gate G2 — app benchmark",
        "",
        "PASS when the benchmark suite covers browser, Electron, native toolkit, file manager/settings, terminal and one hostile/custom UI with no silent failures.",
        "",
        "## Gate G3 — reliability",
        "",
        "PASS when simple tasks exceed 95% success, multi-step tasks exceed 85% success, and silent failure rate is 0% on the priority matrix.",
        "",
        "## Gate G4 — safety",
        "",
        "PASS when command/destructive URI policies are enforced by runtime, not by prompt text, and every command has trace + postcondition or explicit unknown/fail.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="artifacts/native-lab-matrix.json")
    ap.add_argument("--markdown", default="artifacts/native-lab-matrix.md")
    ap.add_argument("--confidence", default="artifacts/native-confidence-gate.md")
    args = ap.parse_args()

    matrix = build_matrix()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    Path(args.markdown).write_text(native_matrix_markdown(), encoding="utf-8")
    Path(args.confidence).write_text(confidence_gate(matrix), encoding="utf-8")
    print(json.dumps({"ok": True, "out": args.out, "markdown": args.markdown, "confidence": args.confidence, "targets": len(matrix["targets"])}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
