# Event Trace Schema

The trace is required to debug flaky UI automation. Without a trace the system
will fail silently and be impossible to improve.

## Event types

```text
plan.started
plan.step.started
capability.selected
adapter.started
adapter.finished
precondition.checked
postcondition.checked
retry.scheduled
policy.blocked
plan.finished
```

## Minimal event

```json
{
  "ts": "2026-07-05T18:00:00Z",
  "trace_id": "run-001",
  "step": 3,
  "uri": "input://local/keyboard/command/type",
  "backend": "windows_uia",
  "profile": "windows-11-uia",
  "payload_redacted": {"text_len": 12},
  "duration_ms": 140,
  "ok": false,
  "failure_class": "postcondition_failed",
  "screenshots": {
    "before": "artifact://trace/003-before.png",
    "after": "artifact://trace/003-after.png"
  },
  "postcondition": {
    "expected": "text visible in editor",
    "observed": false
  }
}
```

## Rule

Every command URI must have a trace event and either a postcondition result or an
explicit reason why no postcondition was possible.
