# Native Test Lab

Docker validates the URI runtime contract. Native runners validate the data plane.

Use this directory to attach real hosts:

- Windows 10/11/Server: UI Automation, SendInput, RDP session behaviour.
- macOS: AXUIElement, CGEvent, TCC permissions, Retina coordinate transforms.
- Linux X11/Wayland: AT-SPI, portals/libei, X11/noVNC coordinate mapping.
- Android: ADB, UIAutomator/Appium, screencap/input.
- iOS/iPadOS: XCUITest/Appium on a Mac runner.
- ChromeOS: Chrome/CDP, Android container and Crostini Linux container.
- HID/KVM: HDMI capture + USB HID for BIOS/login/dead OS.

Minimum evidence per native run:

1. `artifacts/native-host-probe.json`.
2. capability catalog JSON.
3. one semantic tree or structured UI dump where possible.
4. screenshot before/after.
5. one query, one command and one verified postcondition.
6. trace with timings, backend names and failure classification.

Start locally:

```bash
PYTHONPATH=src python tools/probe_native_host.py --out artifacts/native-host-probe.json
PYTHONPATH=src python tools/run_native_lab_matrix.py
PYTHONPATH=src python tools/check_confidence_gate.py
```
