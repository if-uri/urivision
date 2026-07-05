# ChromeOS native profile

ChromeOS is not one backend. Treat it as a mixed runtime:

1. Chrome/PWA: prefer `browser://` through CDP/Chrome remote debugging.
2. Android container: use `android://` / ADB/UIAutomator if developer mode or managed policy allows it.
3. Crostini Linux container: use Linux adapters inside the container, not host-level ChromeOS UI.
4. Hardware fallback: KVM/HID if host UI control is required and policies block software automation.

Evidence to collect:

- Chrome remote debugging target list.
- Android availability and `uiautomator dump` where allowed.
- Crostini session info where enabled.
- Screenshot/input proof and policy limitations.
