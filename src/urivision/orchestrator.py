# Author: Tom Sapletta · Part of the ifURI solution.
"""Simple URI process runner.

The plan runner executes JSON plans where each step is a URI command/query.
It is intentionally small and deterministic so it can become the bridge between
LLM planning and real runtime execution.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .runtime import UriRuntime, default_runtime

JsonDict = dict[str, Any]


class PlanError(ValueError):
    pass


def _get_path(data: Any, path: str) -> Any:
    cur = data
    for part in path.split("."):
        if not part:
            continue
        if isinstance(cur, dict):
            cur = cur[part]
        elif isinstance(cur, list):
            cur = cur[int(part)]
        else:
            raise KeyError(path)
    return cur


def _resolve_templates(value: Any, outputs: dict[str, JsonDict]) -> Any:
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        expr = value[2:-1]
        step_id, _, path = expr.partition(".")
        if step_id not in outputs:
            raise PlanError(f"Unknown step reference: {step_id}")
        return _get_path(outputs[step_id], path)
    if isinstance(value, dict):
        return {k: _resolve_templates(v, outputs) for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve_templates(v, outputs) for v in value]
    return value


def _check_expectation(result: JsonDict, expectation: JsonDict | None) -> JsonDict:
    if not expectation:
        return {"ok": True, "checked": False}
    if "ok" in expectation and bool(result.get("ok")) is not bool(expectation["ok"]):
        return {"ok": False, "checked": True, "reason": "ok_mismatch", "expected": expectation["ok"], "got": result.get("ok")}
    if "found" in expectation and bool(result.get("found")) is not bool(expectation["found"]):
        return {"ok": False, "checked": True, "reason": "found_mismatch", "expected": expectation["found"], "got": result.get("found")}
    if "contains" in expectation:
        text = json.dumps(result, ensure_ascii=False)
        if str(expectation["contains"]).lower() not in text.lower():
            return {"ok": False, "checked": True, "reason": "contains_mismatch", "expected": expectation["contains"]}
    return {"ok": True, "checked": True}


class PlanRunner:
    def __init__(self, runtime: UriRuntime | None = None) -> None:
        self.runtime = runtime or default_runtime()

    def run(self, plan: JsonDict, *, dry_run: bool | None = None, stop_on_error: bool = True) -> JsonDict:
        if "steps" not in plan or not isinstance(plan["steps"], list):
            raise PlanError("Plan must contain steps[]")
        outputs: dict[str, JsonDict] = {}
        trace: list[JsonDict] = []
        for index, step in enumerate(plan["steps"]):
            step_id = step.get("id") or f"step_{index + 1}"
            uri = step.get("call") or step.get("uri")
            if not uri:
                raise PlanError(f"Step {step_id} has no call/uri")
            payload = _resolve_templates(step.get("with", step.get("payload", {})), outputs)
            result = self.runtime.call(uri, payload, dry_run=dry_run)
            expectation = _check_expectation(result, step.get("expect_result"))
            item = {"id": step_id, "uri": uri, "payload": payload, "result": result, "expectation": expectation}
            trace.append(item)
            outputs[step_id] = result
            if (not result.get("ok", False) or not expectation.get("ok", False)) and stop_on_error:
                return {"ok": False, "failed_at": step_id, "outputs": outputs, "trace": trace}
        return {"ok": True, "outputs": outputs, "trace": trace, "runtime_trace": self.runtime.trace()}


def run_plan(plan: JsonDict, *, runtime: UriRuntime | None = None, dry_run: bool | None = None) -> JsonDict:
    return PlanRunner(runtime).run(plan, dry_run=dry_run)


def run_plan_file(path: str, *, runtime: UriRuntime | None = None, dry_run: bool | None = None) -> JsonDict:
    return run_plan(json.loads(Path(path).read_text(encoding="utf-8")), runtime=runtime, dry_run=dry_run)
