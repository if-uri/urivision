# Docker/backend matrix for URI Runtime

## Goal

The Docker layer validates that LLM-visible functions are reusable through URI processes before we attach real OS-specific adapters. The test target is the contract:

```text
LLM intent → URI capability → payload validation → runtime dispatch → trace → postcondition
```

It deliberately separates:

- **contract test** — Does the URI runtime expose the capability and execute the plan shape correctly?
- **native adapter test** — Does a real OS backend perform the action in a live session?

## Four profiles

| Profile | Purpose | Reality level |
|---|---|---|
| `linux-x11-novnc` | Linux/X11/noVNC path | Docker harness prepared, current handlers are contract adapters |
| `linux-wayland-headless` | Wayland limitations and future portal/libei path | Docker harness prepared, current handlers are contract adapters |
| `windows-uia-contract` | Windows UI Automation URI contract | Contract-only in Linux Docker |
| `macos-ax-contract` | macOS AXUIElement URI contract | Contract-only in Linux Docker |

## Why this matters

Without this layer you will not know whether a failure comes from:

- bad URI naming,
- missing capability,
- wrong JSON payload,
- orchestration bug,
- backend input problem,
- focus problem,
- visual verification problem,
- OS security boundary.

The matrix first proves the reusable URI surface. Then each native adapter can fail independently without damaging the LLM-facing contract.

## Current limitation

Linux Docker cannot provide true Windows UIA or macOS AX execution. Those must be tested on native runners. This repository now makes that explicit through `profile_kind` and `limitations` in `runtime://local/platform/query/profile`.
