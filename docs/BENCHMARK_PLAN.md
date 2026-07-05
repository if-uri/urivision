# Benchmark Plan

## Task groups

1. **Navigation**: open app/window/tab, switch focus, close dialog.
2. **Form filling**: text field, checkbox, radio, combo box, submit.
3. **Document UI**: menu, toolbar, save dialog, file picker.
4. **Browser/Electron**: CDP preferred path vs accessibility fallback.
5. **Native toolkit**: Win32/WPF/UWP, Cocoa/SwiftUI, GTK, Qt.
6. **Remote session**: noVNC/VNC/RDP/Citrix-like latency and scaling.
7. **Mobile**: Android UIAutomator and iOS XCUITest.
8. **Hostile UI**: canvas/game-like/custom-rendered screen.
9. **Hardware KVM**: BIOS/UEFI, login screen, OS installer.

## Metrics

```text
success_rate_simple >= 95%
success_rate_multistep >= 85%
silent_failure_rate == 0%
p50_action_without_vision < 1s
p50_action_with_ocr < 3s
p50_action_with_llm_vision < 8s
trace_coverage == 100% for commands
postcondition_coverage == 100% for non-trivial commands
```

## Output

Every benchmark run writes:

- JSON result;
- markdown report;
- screenshots and tree snapshots;
- trace events;
- failure taxonomy.
