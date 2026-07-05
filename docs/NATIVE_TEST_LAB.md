# Native Test Lab for URI Runtime

## Purpose

The previous Docker layer validates the URI control plane: parser, catalog,
capability discovery, dry-run plans and mock handlers. It does not validate the
native data plane on Windows UIA, macOS AX, Wayland, Android, iOS or hardware KVM.

This native test lab closes that gap by defining runner profiles, host probes,
MethodRouter expectations and confidence gates.

## Principle

Do not ask the LLM to choose OS-specific tricks. Let the LLM issue stable URI
intents and let the runtime choose the method:

```text
intent: type_text
profile: windows-11-uia
route: browser_cdp -> windows_uia/set_value -> SendInput -> RDP/VNC -> HID
```

The model may choose a URI from the catalog, but method selection must be
runtime-owned, observable and testable.

## Layers

```text
LLM / planner
  -> URI capability catalog
  -> MethodRouter
  -> Adapter broker
  -> Native adapter: UIA / AX / AT-SPI / CDP / ADB / XCUITest / VNC / HID
  -> postcondition verifier
  -> event trace store
```

## Required native evidence

Every native runner must produce artifacts:

1. `native-host-probe.json` or profile-specific probe output.
2. Capability catalog.
3. Semantic tree where available: UIA/AX/AT-SPI/CDP/UIAutomator/XCUITest.
4. Screenshot before/after.
5. One safe query: find an element.
6. One safe command: focus/press/type in a demo target.
7. One verified postcondition.
8. Failure classification if any step fails.

## Commands

```bash
PYTHONPATH=src python tools/run_native_lab_matrix.py
PYTHONPATH=src python tools/probe_native_host.py --out artifacts/native-host-probe.json
PYTHONPATH=src python tools/check_confidence_gate.py
```

On native hosts:

```powershell
# Windows
native\windows\run_smoke.ps1
```

```bash
# macOS
native/macos/run_smoke.sh

# Linux
native/linux/run_smoke.sh

# Android
native/android/probe_android.sh

# iOS
native/ios/probe_ios.sh
```

## Confidence gates

- G0: URI contract and MethodRouter pass for all profiles.
- G1: native smoke evidence exists for priority OS families.
- G2: benchmark apps pass with no silent failures.
- G3: reliability thresholds are met.
- G4: policy engine blocks destructive commands unless explicitly approved.

## Failure classes

Use stable failure classes in traces:

```text
capability_unavailable
permission_denied
focus_not_acquired
postcondition_failed
coordinate_transform_failed
adapter_timeout
remote_latency_budget_exceeded
semantic_tree_missing
vision_confidence_low
policy_blocked
requires_human_approval
```
