# Native Adapter Contract

Every native adapter must expose the same runtime shape regardless of platform.

## Required adapter methods

```text
capabilities()
health()
snapshot_tree()
find_element(locator)
focus(element)
press(element)
set_value(element, value)
type_text(text)
hotkey(keys)
click(bounds_or_element)
screenshot()
verify(postcondition)
trace(event)
```

## Required output fields

```json
{
  "ok": true,
  "backend": "windows_uia",
  "duration_ms": 123,
  "confidence": 0.95,
  "evidence": {},
  "limitations": [],
  "trace_id": "..."
}
```

## Non-negotiable rule

A command is not successful merely because the adapter sent input. A command is
successful only when the postcondition is observed or the result is explicitly
classified as unknown/fail.

## Adapter safety

Adapters must declare:

- whether they can act on secure desktops/login screens;
- whether they cross user/session boundaries;
- whether they send external network traffic;
- whether the action can be destructive;
- whether human confirmation is required.
