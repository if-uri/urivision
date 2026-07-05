# Implementation notes — urivision 0.2 URI Runtime

## What was implemented

- URI parser and matcher with captured target names: `input://{target}/keyboard/command/type`.
- Capability contract: URI pattern, title, description, kind, schemas, examples, side effects, safety.
- Capability registry and dispatcher.
- LLM catalog export as JSON, Markdown, prompt and tool descriptor.
- Runtime commands:
  - `runtime://.../capabilities/query/list`
  - `runtime://.../capability/query/explain`
  - `ui://.../tree/query/snapshot`
  - `ui://.../element/query/find`
  - `ui://.../element/command/focus`
  - `ui://.../element/command/press`
  - `input://.../keyboard/command/type`
  - `input://.../keyboard/command/hotkey`
  - `input://.../pointer/command/click`
  - `view://.../screen/query/text`
  - `view://.../screenshot/query/capture`
  - `browser://.../element/command/fill`
  - `vision://.../screen/command/parse`
  - `kvm://.../input/command/task_run`
  - `guard://.../batch/command/run`
- JSON plan runner with `${step.path}` references.
- `@uri_function` bridge for exposing existing Python functions as URI capabilities.
- CLI commands: `catalog`, `explain`, `call`, `plan`; old `run FILE.vuri` remains.
- Unit tests for URI matching, catalog, call flow, plan runner and function binding.

## Validation performed

```bash
PYTHONPATH=src:. python3 -m unittest discover -s tests -v   # z katalogu repo (make test)
```

Result:

```txt
Ran 5 tests in 0.003s
OK
```

Manual CLI smoke test:

```bash
PYTHONPATH=src python3 -m urivision.cli catalog --format markdown
PYTHONPATH=src python3 -m urivision.cli plan examples/desktop-control.plan.json
```

The example plan finds a mock textbox, focuses it, types text, verifies visible text and presses Save.

## Intentional limitations

This is not yet a real Windows/macOS/Linux input backend. The default runtime is mock-based so the control plane can be tested without OS permissions. Real adapters should replace handlers while keeping the URI contracts stable.

## Next implementation target

The highest-value next adapter is `browser://` using CDP/Playwright because it solves the flaky focus/contenteditable problem in web portals better than keyboard injection.
