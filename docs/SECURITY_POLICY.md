# Security Policy for URI Commands

## URI risk classes

```text
query: read-only, no state change
command: state changing
destructive_command: submits, deletes, purchases, sends or persists externally
privileged_command: requires OS permissions/elevation
external_command: sends data outside local runtime
```

## Runtime policy examples

```json
{
  "policy": "default-local-dev",
  "allow": ["query", "safe_command"],
  "confirm": ["destructive_command", "external_command"],
  "deny": ["payment://*", "shell://*/command/run"],
  "dry_run_only": ["admin://*", "secure-desktop://*"]
}
```

## Rule

Safety must be enforced by runtime, not by prompt text. The LLM may propose an
action; the policy engine decides whether it can be executed.
