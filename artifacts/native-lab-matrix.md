# Native OS Test Lab Matrix

This matrix separates Docker-contract validation from native data-plane validation.

| Target | Family | Runner | Primary adapters | Risk focus | Evidence required |
|---|---|---|---|---|---|
| Android ADB/UIAutomator runner (`android-adb-uiautomator`) | android | emulator-or-device-lab | adb, uiautomator, appium, browser_cdp_webview | IME/text escaping; permissions dialogs; OEM skins | uiautomator XML; screencap; input/action trace |
| ChromeOS mixed runtime profile (`chromeos-chrome-android-linux`) | chromeos | device-lab-or-chrome-remote-debugging | browser_cdp, android_adb_if_enabled, linux_container | multiple UI stacks; device management policy; limited host control | CDP target list; Android/Crostini availability; input path proof |
| Debian/RHEL/Rocky enterprise Linux runner (`debian-rhel-enterprise`) | linux-enterprise | self-hosted-linux-enterprise | at_spi, browser_cdp, x11_or_wayland_backend | old packages; locked-down enterprise policy; remote desktop | os-release; session proof; adapter capability list |
| Fedora GNOME Wayland-first runner (`fedora-gnome-wayland`) | linux | self-hosted-linux-desktop-or-vm | at_spi, xdg_portal_remote_desktop, libei, browser_cdp | Wayland-only migration; portal prompts; Flatpak sandbox accessibility | Wayland session proof; AT-SPI tree; portal/libei probe |
| Hardware HID/KVM/RP2040 fallback profile (`hid-kvm-rp2040`) | hardware-kvm | hardware-lab | hid_keyboard, hid_mouse, hdmi_capture, camera | no semantic tree; absolute vs relative mouse; capture latency | HID enumeration; video capture proof; BIOS/login task trace |
| iOS/iPadOS XCUITest runner (`ios-xcuitest`) | ios | mac-runner-with-simulator-or-device | xcuitest, appium, safari_webdriver | Apple signing; device trust; simulator/device differences | XCUITest element tree; simulator/device trace; screenshot before/after |
| KDE Plasma Wayland runner (`kde-plasma-wayland`) | linux | self-hosted-linux-desktop-or-vm | at_spi, selenium_atspi, browser_cdp | KWin coordinate model; Qt accessibility; Appium driver maturity | Qt/AT-SPI tree; KWin session proof; action trace |
| macOS Sonoma/Sequoia AX compatibility runner (`macos-14-15-ax`) | macos | self-hosted-mac-or-github-hosted-smoke | macos_ax, browser_cdp, cg_event | TCC changes between macOS releases; Secure Input; window permission prompts | AX tree snapshot; permission state; action postcondition trace |
| macOS Tahoe 26 AX runner on Apple silicon (`macos-26-ax-apple-silicon`) | macos | self-hosted-mac | macos_ax, browser_cdp, cg_event | TCC permission denial; Secure Input; Retina scaling | AX tree snapshot; TCC checklist; Retina coordinate transform proof |
| RDP/Citrix/VMware Horizon profile (`rdp-citrix-horizon`) | remote-session | enterprise-remote-testbed | rdp, remote_clipboard, guest_accessibility_broker | session locking; clipboard blocked; credential prompts | session proof; latency metrics; security policy proof |
| Ubuntu 22.04 LTS X11/noVNC runner (`ubuntu-22-04-x11`) | linux | docker-plus-self-hosted-linux | at_spi, x11, browser_cdp, vnc | VNC/browser scaling; DPI; toolkit accessibility gaps | X11 coordinate proof; AT-SPI tree; VNC scaling trace |
| Ubuntu 24.04 LTS GNOME Wayland runner (`ubuntu-24-04-wayland`) | linux | self-hosted-linux-desktop-or-vm | at_spi, browser_cdp, xdg_portal_remote_desktop, libei | Wayland input restrictions; surface-relative coordinates; portal consent | AT-SPI tree; portal availability; input method proof |
| VNC/noVNC/RFB remote session profile (`vnc-novnc-rfb`) | remote-session | docker-plus-device-or-remote-host | vnc_rfb, ocr, vision_parser | browser scaling; latency; lack of semantic tree | latency benchmark; coordinate transform proof; postcondition trace |
| Windows 10 UIA/legacy runner (`windows-10-uia-esu`) | windows | self-hosted-vm-or-physical | windows_uia, browser_cdp, send_input | older Win32 controls; legacy DPI behavior; unsupported/ESU security posture | UIA tree snapshot; legacy app smoke trace; DPI evidence |
| Windows 11 native UIA runner (`windows-11-uia`) | windows | self-hosted-vm-or-physical | windows_uia, browser_cdp, send_input | UAC secure desktop; admin/non-admin session boundary; DPI scaling | UIA tree snapshot; focus proof; set_value or invoke proof |
| Windows Server / RDS / enterprise remote desktop (`windows-server-rds`) | windows-server | self-hosted-enterprise-session | rdp, windows_uia, browser_cdp | session isolation; clipboard policy; remote latency | session metadata; RDP coordinate mapping trace; locked/unlocked behavior |

## Coverage summary

- Targets: 16
- Families: android, chromeos, hardware-kvm, ios, linux, linux-enterprise, macos, remote-session, windows, windows-server
- Missing required families: none
