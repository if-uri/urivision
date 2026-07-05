#!/usr/bin/env python3
"""Probe one URI runtime backend profile and write a machine-readable report."""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any

from urivision import default_runtime

JsonDict = dict[str, Any]


def call_step(rt, step_id: str, uri: str, payload: JsonDict) -> JsonDict:
    started = time.perf_counter()
    try:
        result = rt.call(uri, payload)
        ok = bool(result.get("ok", False))
    except Exception as exc:  # pragma: no cover - diagnostic script
        result = {"ok": False, "error": type(exc).__name__, "message": str(exc)}
        ok = False
    return {
        "id": step_id,
        "uri": uri,
        "payload": payload,
        "ok": ok,
        "duration_ms": round((time.perf_counter() - started) * 1000, 3),
        "result": result,
    }


def run_probe(profile: str) -> JsonDict:
    os.environ["URIVISION_BACKEND_PROFILE"] = profile
    rt = default_runtime(state={"backend_profile": profile})
    steps = []
    steps.append(call_step(rt, "profile", "runtime://local/platform/query/profile", {"profile": profile}))
    steps.append(call_step(rt, "health", "runtime://local/health/query/check", {"profile": profile}))
    steps.append(call_step(rt, "catalog", "runtime://local/capabilities/query/list", {"format": "json"}))
    steps.append(call_step(rt, "tree", "ui://local/tree/query/snapshot", {}))
    steps.append(call_step(rt, "find_textbox", "ui://local/element/query/find", {"role": "textbox", "name": "Search"}))
    found = steps[-1]["result"].get("element") or {}
    element_id = found.get("id", "field:search")
    steps.append(call_step(rt, "focus_textbox", "ui://local/element/command/focus", {"element_id": element_id}))
    token = f"probe-{profile}"
    steps.append(call_step(rt, "type_token", "input://local/keyboard/command/type", {"text": token}))
    steps.append(call_step(rt, "verify_token", "view://local/screen/query/text", {"contains": token}))
    steps.append(call_step(rt, "find_save", "ui://local/element/query/find", {"role": "button", "name": "Save"}))
    save = steps[-1]["result"].get("element") or {}
    steps.append(call_step(rt, "press_save", "ui://local/element/command/press", {"element_id": save.get("id", "button:save")}))
    steps.append(call_step(rt, "guarded_batch", "guard://local/batch/command/run", {
        "steps": [{"op": "type", "text": f" guarded-{profile}"}],
        "expect": {"uri": "view://local/screen/query/text", "with": {"contains": f"guarded-{profile}"}},
        "tries": 2,
    }))
    steps.append(call_step(rt, "screenshot", "view://local/screenshot/query/capture", {"emit": f"artifact://reports/{profile}.png", "max_width": 1600}))
    steps.append(call_step(rt, "vision_parse", "vision://local/screen/command/parse", {"image_uri": f"artifact://reports/{profile}.png", "aspects": ["ui/click-targets"]}))
    passed = all(step["ok"] for step in steps) and steps[7]["result"].get("found") is True
    return {
        "ok": passed,
        "profile": profile,
        "profile_info": steps[0]["result"].get("profile"),
        "summary": {
            "steps": len(steps),
            "passed_steps": sum(1 for step in steps if step["ok"]),
            "failed_steps": [step["id"] for step in steps if not step["ok"]],
            "verified_text": steps[7]["result"].get("found"),
        },
        "steps": steps,
        "runtime_trace_events": len(rt.trace()),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default=os.environ.get("URIVISION_BACKEND_PROFILE", "mock-local"))
    ap.add_argument("--out")
    args = ap.parse_args()
    report = run_probe(args.profile)
    data = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding="utf-8")
    print(data)
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
