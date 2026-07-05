# Author: Tom Sapletta · Part of the ifURI solution.
"""Native OS coverage profiles for URI Runtime validation.

Docker validates the contract. These profiles describe the native test lab that is
required to validate the data plane on real operating systems and remote sessions.
The goal is to make OS support explicit instead of hiding it inside prompt logic.
"""
from __future__ import annotations

import os
import platform
from dataclasses import dataclass, field
from typing import Any

JsonDict = dict[str, Any]

CORE_URIS = [
    "runtime://local/capabilities/query/list",
    "runtime://local/health/query/check",
    "runtime://local/platform/query/profile",
    "ui://local/tree/query/snapshot",
    "ui://local/element/query/find",
    "ui://local/element/command/focus",
    "ui://local/element/command/press",
    "input://local/keyboard/command/type",
    "view://local/screen/query/text",
    "view://local/screenshot/query/capture",
    "guard://local/batch/command/run",
]

DESTRUCTIVE_URIS = [
    "browser://local/form/command/submit",
    "shell://local/command/run",
    "payment://local/command/confirm",
]


@dataclass(frozen=True)
class NativeTargetProfile:
    id: str
    label: str
    family: str
    versions: list[str]
    runner_kind: str
    runner_labels: list[str]
    display_stack: str
    primary_adapters: list[str]
    fallback_adapters: list[str] = field(default_factory=list)
    required_probes: list[str] = field(default_factory=list)
    representative_apps: list[str] = field(default_factory=list)
    risk_focus: list[str] = field(default_factory=list)
    must_pass_uris: list[str] = field(default_factory=lambda: list(CORE_URIS))
    docker_role: str = "contract-only"
    evidence_required: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> JsonDict:
        return {
            "id": self.id,
            "label": self.label,
            "family": self.family,
            "versions": list(self.versions),
            "runner_kind": self.runner_kind,
            "runner_labels": list(self.runner_labels),
            "display_stack": self.display_stack,
            "primary_adapters": list(self.primary_adapters),
            "fallback_adapters": list(self.fallback_adapters),
            "required_probes": list(self.required_probes),
            "representative_apps": list(self.representative_apps),
            "risk_focus": list(self.risk_focus),
            "must_pass_uris": list(self.must_pass_uris),
            "docker_role": self.docker_role,
            "evidence_required": list(self.evidence_required),
            "notes": self.notes,
        }


NATIVE_TARGETS: dict[str, NativeTargetProfile] = {
    "windows-11-uia": NativeTargetProfile(
        id="windows-11-uia",
        label="Windows 11 native UIA runner",
        family="windows",
        versions=["Windows 11 24H2", "Windows 11 25H2", "Windows 11 current channel"],
        runner_kind="self-hosted-vm-or-physical",
        runner_labels=["self-hosted", "windows", "uia"],
        display_stack="Desktop + UI Automation + optional RDP",
        primary_adapters=["windows_uia", "browser_cdp", "send_input"],
        fallback_adapters=["rdp", "vnc", "hid"],
        required_probes=["powershell", "python", "uia_tree", "sendinput", "screenshot", "dpi"],
        representative_apps=["Notepad", "Settings", "Edge", "Chrome", "VS Code", "Electron app"],
        risk_focus=["UAC secure desktop", "admin/non-admin session boundary", "DPI scaling", "RDP coordinate mapping"],
        evidence_required=["UIA tree snapshot", "focus proof", "set_value or invoke proof", "screenshot before/after"],
        notes="Primary Windows desktop profile. Docker cannot validate UIA; use real Windows runner.",
    ),
    "windows-10-uia-esu": NativeTargetProfile(
        id="windows-10-uia-esu",
        label="Windows 10 UIA/legacy runner",
        family="windows",
        versions=["Windows 10 22H2", "Windows 10 ESU", "Windows 10 Enterprise LTSC/IoT where relevant"],
        runner_kind="self-hosted-vm-or-physical",
        runner_labels=["self-hosted", "windows10", "uia"],
        display_stack="Desktop + UI Automation + optional RDP",
        primary_adapters=["windows_uia", "browser_cdp", "send_input"],
        fallback_adapters=["rdp", "vnc", "hid"],
        required_probes=["powershell", "python", "uia_tree", "sendinput", "screenshot", "dpi"],
        representative_apps=["Notepad", "Control Panel", "Edge/Chrome", "legacy Win32 app", "Office if licensed"],
        risk_focus=["older Win32 controls", "legacy DPI behavior", "unsupported/ESU security posture"],
        evidence_required=["UIA tree snapshot", "legacy app smoke trace", "DPI evidence"],
        notes="Important legacy population. Treat security/update posture separately from automation capability.",
    ),
    "windows-server-rds": NativeTargetProfile(
        id="windows-server-rds",
        label="Windows Server / RDS / enterprise remote desktop",
        family="windows-server",
        versions=["Windows Server 2019", "Windows Server 2022", "Windows Server 2025"],
        runner_kind="self-hosted-enterprise-session",
        runner_labels=["self-hosted", "windows-server", "rds"],
        display_stack="RDS/RDP/Citrix-like remote session + UIA when brokered",
        primary_adapters=["rdp", "windows_uia", "browser_cdp"],
        fallback_adapters=["vnc", "hid"],
        required_probes=["rdp_session", "session_id", "uia_tree", "screenshot", "clipboard", "keyboard"],
        representative_apps=["Line-of-business app", "ERP/CRM web app", "Office", "File Explorer"],
        risk_focus=["session isolation", "clipboard policy", "remote latency", "locked session"],
        evidence_required=["session metadata", "RDP coordinate mapping trace", "locked/unlocked behavior"],
        notes="Critical for enterprise automation; must be tested separately from consumer Windows.",
    ),
    "macos-26-ax-apple-silicon": NativeTargetProfile(
        id="macos-26-ax-apple-silicon",
        label="macOS Tahoe 26 AX runner on Apple silicon",
        family="macos",
        versions=["macOS Tahoe 26", "latest macOS current channel"],
        runner_kind="self-hosted-mac",
        runner_labels=["self-hosted", "macos", "ax", "apple-silicon"],
        display_stack="AXUIElement + CGEvent + TCC permissions",
        primary_adapters=["macos_ax", "browser_cdp", "cg_event"],
        fallback_adapters=["hid"],
        required_probes=["python", "osascript", "accessibility_permission", "screen_recording_permission", "input_monitoring_permission", "retina_scale"],
        representative_apps=["Finder", "System Settings", "Safari", "Chrome", "VS Code", "Electron app"],
        risk_focus=["TCC permission denial", "Secure Input", "Retina scaling", "sandboxed apps"],
        evidence_required=["AX tree snapshot", "TCC checklist", "Retina coordinate transform proof"],
        notes="Primary modern macOS profile. Native Mac runner required; Linux Docker is contract-only.",
    ),
    "macos-14-15-ax": NativeTargetProfile(
        id="macos-14-15-ax",
        label="macOS Sonoma/Sequoia AX compatibility runner",
        family="macos",
        versions=["macOS Sonoma 14", "macOS Sequoia 15"],
        runner_kind="self-hosted-mac-or-github-hosted-smoke",
        runner_labels=["self-hosted", "macos", "ax"],
        display_stack="AXUIElement + CGEvent + TCC permissions",
        primary_adapters=["macos_ax", "browser_cdp", "cg_event"],
        fallback_adapters=["hid"],
        required_probes=["python", "osascript", "accessibility_permission", "screen_recording_permission", "input_monitoring_permission"],
        representative_apps=["Finder", "Safari", "Chrome", "VS Code", "Electron app"],
        risk_focus=["TCC changes between macOS releases", "Secure Input", "window permission prompts"],
        evidence_required=["AX tree snapshot", "permission state", "action postcondition trace"],
    ),
    "ubuntu-24-04-wayland": NativeTargetProfile(
        id="ubuntu-24-04-wayland",
        label="Ubuntu 24.04 LTS GNOME Wayland runner",
        family="linux",
        versions=["Ubuntu 24.04 LTS", "Ubuntu 26.04 LTS preview/current when available"],
        runner_kind="self-hosted-linux-desktop-or-vm",
        runner_labels=["self-hosted", "linux", "ubuntu", "wayland"],
        display_stack="GNOME Wayland + AT-SPI + portals/libei where available",
        primary_adapters=["at_spi", "browser_cdp", "xdg_portal_remote_desktop", "libei"],
        fallback_adapters=["vnc", "hid"],
        required_probes=["xdg_session_type", "dbus", "at_spi", "portal", "screenshot", "keyboard"],
        representative_apps=["GNOME Text Editor", "Files", "Settings", "Firefox", "Chrome", "VS Code"],
        risk_focus=["Wayland input restrictions", "surface-relative coordinates", "portal consent", "AT-SPI quality"],
        evidence_required=["AT-SPI tree", "portal availability", "input method proof", "coordinate mapping proof"],
    ),
    "ubuntu-22-04-x11": NativeTargetProfile(
        id="ubuntu-22-04-x11",
        label="Ubuntu 22.04 LTS X11/noVNC runner",
        family="linux",
        versions=["Ubuntu 22.04 LTS", "Ubuntu 24.04 LTS Xorg session"],
        runner_kind="docker-plus-self-hosted-linux",
        runner_labels=["self-hosted", "linux", "ubuntu", "x11"],
        display_stack="X11 + AT-SPI + xdotool/wmctrl + optional noVNC",
        primary_adapters=["at_spi", "x11", "browser_cdp", "vnc"],
        fallback_adapters=["hid"],
        required_probes=["DISPLAY", "xdotool", "wmctrl", "xprop", "at_spi", "vnc_optional"],
        representative_apps=["gedit", "Files", "Firefox", "Chrome", "LibreOffice", "VS Code"],
        risk_focus=["VNC/browser scaling", "DPI", "toolkit accessibility gaps"],
        evidence_required=["X11 coordinate proof", "AT-SPI tree", "VNC scaling trace"],
        docker_role="contract-plus-linux-x11",
    ),
    "fedora-gnome-wayland": NativeTargetProfile(
        id="fedora-gnome-wayland",
        label="Fedora GNOME Wayland-first runner",
        family="linux",
        versions=["Fedora Workstation 42", "Fedora Workstation 43+"],
        runner_kind="self-hosted-linux-desktop-or-vm",
        runner_labels=["self-hosted", "linux", "fedora", "wayland", "gnome"],
        display_stack="GNOME Wayland + AT-SPI + portals/libei",
        primary_adapters=["at_spi", "xdg_portal_remote_desktop", "libei", "browser_cdp"],
        fallback_adapters=["hid"],
        required_probes=["xdg_session_type", "gnome_shell", "at_spi", "portal", "libei_optional"],
        representative_apps=["GNOME Text Editor", "Files", "Settings", "Firefox", "Flatpak app"],
        risk_focus=["Wayland-only migration", "portal prompts", "Flatpak sandbox accessibility"],
        evidence_required=["Wayland session proof", "AT-SPI tree", "portal/libei probe"],
    ),
    "kde-plasma-wayland": NativeTargetProfile(
        id="kde-plasma-wayland",
        label="KDE Plasma Wayland runner",
        family="linux",
        versions=["KDE Plasma 6 on Fedora/Kubuntu/openSUSE"],
        runner_kind="self-hosted-linux-desktop-or-vm",
        runner_labels=["self-hosted", "linux", "kde", "wayland"],
        display_stack="KWin Wayland + AT-SPI + Appium/Selenium AT-SPI path",
        primary_adapters=["at_spi", "selenium_atspi", "browser_cdp"],
        fallback_adapters=["xdg_portal_remote_desktop", "hid"],
        required_probes=["xdg_session_type", "kwin_wayland", "at_spi", "appium_optional", "portal"],
        representative_apps=["Dolphin", "System Settings", "Kate", "Konsole", "Firefox"],
        risk_focus=["KWin coordinate model", "Qt accessibility", "Appium driver maturity"],
        evidence_required=["Qt/AT-SPI tree", "KWin session proof", "action trace"],
    ),
    "debian-rhel-enterprise": NativeTargetProfile(
        id="debian-rhel-enterprise",
        label="Debian/RHEL/Rocky enterprise Linux runner",
        family="linux-enterprise",
        versions=["Debian 12", "RHEL 9", "Rocky/Alma 9", "RHEL 10 family when adopted"],
        runner_kind="self-hosted-linux-enterprise",
        runner_labels=["self-hosted", "linux", "enterprise"],
        display_stack="GNOME/KDE/X11/Wayland depending on deployment",
        primary_adapters=["at_spi", "browser_cdp", "x11_or_wayland_backend"],
        fallback_adapters=["vnc", "rdp", "hid"],
        required_probes=["os_release", "session_type", "at_spi", "browser_cdp", "remote_session_optional"],
        representative_apps=["terminal", "browser", "file manager", "enterprise app"],
        risk_focus=["old packages", "locked-down enterprise policy", "remote desktop"],
        evidence_required=["os-release", "session proof", "adapter capability list"],
    ),
    "chromeos-chrome-android-linux": NativeTargetProfile(
        id="chromeos-chrome-android-linux",
        label="ChromeOS mixed runtime profile",
        family="chromeos",
        versions=["ChromeOS current stable/LTS channel"],
        runner_kind="device-lab-or-chrome-remote-debugging",
        runner_labels=["self-hosted", "chromeos"],
        display_stack="Chrome DOM/CDP + Android container + Crostini Linux container",
        primary_adapters=["browser_cdp", "android_adb_if_enabled", "linux_container"],
        fallback_adapters=["vnc", "hid"],
        required_probes=["chrome_remote_debugging", "adb_optional", "crostini_optional", "screenshot"],
        representative_apps=["Chrome", "PWA", "Android app", "Linux app in Crostini"],
        risk_focus=["multiple UI stacks", "device management policy", "limited host control"],
        evidence_required=["CDP target list", "Android/Crostini availability", "input path proof"],
    ),
    "android-adb-uiautomator": NativeTargetProfile(
        id="android-adb-uiautomator",
        label="Android ADB/UIAutomator runner",
        family="android",
        versions=["Android 12", "Android 13", "Android 14", "Android 15", "Android 16 current devices"],
        runner_kind="emulator-or-device-lab",
        runner_labels=["self-hosted", "android", "adb"],
        display_stack="ADB + UIAutomator/Appium + screenshot",
        primary_adapters=["adb", "uiautomator", "appium", "browser_cdp_webview"],
        fallback_adapters=["hid", "camera"],
        required_probes=["adb", "device", "uiautomator_dump", "screencap", "input_text", "appium_optional"],
        representative_apps=["Settings", "Chrome", "WebView app", "native demo app"],
        risk_focus=["IME/text escaping", "permissions dialogs", "OEM skins", "WebView vs native"],
        evidence_required=["uiautomator XML", "screencap", "input/action trace"],
    ),
    "ios-xcuitest": NativeTargetProfile(
        id="ios-xcuitest",
        label="iOS/iPadOS XCUITest runner",
        family="ios",
        versions=["iOS 16", "iOS 17", "iOS 18", "iOS 19/26 current naming if applicable"],
        runner_kind="mac-runner-with-simulator-or-device",
        runner_labels=["self-hosted", "macos", "ios", "xcode"],
        display_stack="XCUITest/Appium + simulator/device screenshot",
        primary_adapters=["xcuitest", "appium", "safari_webdriver"],
        fallback_adapters=["camera", "hid_limited"],
        required_probes=["xcodebuild", "xcrun", "simctl", "wda_or_appium_optional", "screenshot"],
        representative_apps=["Settings", "Safari", "native demo app", "PWA"],
        risk_focus=["Apple signing", "device trust", "simulator/device differences", "sandboxing"],
        evidence_required=["XCUITest element tree", "simulator/device trace", "screenshot before/after"],
    ),
    "vnc-novnc-rfb": NativeTargetProfile(
        id="vnc-novnc-rfb",
        label="VNC/noVNC/RFB remote session profile",
        family="remote-session",
        versions=["TigerVNC", "x11vnc", "noVNC/websockify", "real VNC appliance"],
        runner_kind="docker-plus-device-or-remote-host",
        runner_labels=["self-hosted", "vnc"],
        display_stack="RFB pixel stream + keyboard/pointer injection",
        primary_adapters=["vnc_rfb", "ocr", "vision_parser"],
        fallback_adapters=["accessibility_if_inside_guest", "hid"],
        required_probes=["rfb_connect", "screenshot_latency", "keyboard", "pointer", "scaling"],
        representative_apps=["browser", "terminal", "file manager", "custom app"],
        risk_focus=["browser scaling", "latency", "lack of semantic tree", "focus mismatch"],
        evidence_required=["latency benchmark", "coordinate transform proof", "postcondition trace"],
        docker_role="contract-plus-linux-x11",
    ),
    "rdp-citrix-horizon": NativeTargetProfile(
        id="rdp-citrix-horizon",
        label="RDP/Citrix/VMware Horizon profile",
        family="remote-session",
        versions=["Microsoft RDP", "Citrix Workspace", "VMware Horizon", "Azure Virtual Desktop"],
        runner_kind="enterprise-remote-testbed",
        runner_labels=["self-hosted", "remote-desktop"],
        display_stack="remote desktop protocol + guest accessibility where brokered",
        primary_adapters=["rdp", "remote_clipboard", "guest_accessibility_broker"],
        fallback_adapters=["ocr", "vision_parser", "hid"],
        required_probes=["session_metadata", "clipboard_policy", "keyboard", "pointer", "latency"],
        representative_apps=["ERP", "Office", "browser", "file manager"],
        risk_focus=["session locking", "clipboard blocked", "credential prompts", "latency"],
        evidence_required=["session proof", "latency metrics", "security policy proof"],
    ),
    "hid-kvm-rp2040": NativeTargetProfile(
        id="hid-kvm-rp2040",
        label="Hardware HID/KVM/RP2040 fallback profile",
        family="hardware-kvm",
        versions=["USB HID keyboard/mouse", "HDMI capture", "IP-KVM", "RP2040/RP2350 bridge"],
        runner_kind="hardware-lab",
        runner_labels=["self-hosted", "hid", "kvm"],
        display_stack="hardware video capture + USB HID input",
        primary_adapters=["hid_keyboard", "hid_mouse", "hdmi_capture", "camera"],
        fallback_adapters=["ocr", "vision_parser"],
        required_probes=["usb_hid_seen_by_host", "capture_latency", "keyboard_scan_codes", "mouse_relative_absolute", "power_cycle_optional"],
        representative_apps=["BIOS/UEFI", "login screen", "installer", "locked OS", "normal desktop"],
        risk_focus=["no semantic tree", "absolute vs relative mouse", "capture latency", "physical reliability"],
        evidence_required=["HID enumeration", "video capture proof", "BIOS/login task trace"],
        notes="Only practical path for BIOS/login/dead OS. Must be treated as fallback, not default semantic backend.",
    ),
}

REQUIRED_FAMILIES = [
    "windows",
    "windows-server",
    "macos",
    "linux",
    "linux-enterprise",
    "chromeos",
    "android",
    "ios",
    "remote-session",
    "hardware-kvm",
]


def list_native_targets() -> list[NativeTargetProfile]:
    return [NATIVE_TARGETS[k] for k in sorted(NATIVE_TARGETS)]


def get_native_target(target_id: str) -> NativeTargetProfile:
    try:
        return NATIVE_TARGETS[target_id]
    except KeyError as exc:
        known = ", ".join(sorted(NATIVE_TARGETS))
        raise KeyError(f"unknown native target {target_id!r}; known: {known}") from exc


def coverage_summary() -> JsonDict:
    targets = list_native_targets()
    families = sorted({t.family for t in targets})
    missing = [f for f in REQUIRED_FAMILIES if f not in families]
    return {
        "target_count": len(targets),
        "families": families,
        "missing_required_families": missing,
        "native_required_count": sum(1 for t in targets if "self-hosted" in " ".join(t.runner_labels) or t.runner_kind != "docker-plus-self-hosted-linux"),
        "docker_contract_targets": [t.id for t in targets if t.docker_role.startswith("contract")],
    }


def detect_local_host() -> JsonDict:
    system = platform.system().lower() or "unknown"
    release = platform.release()
    machine = platform.machine()
    env = {
        "XDG_SESSION_TYPE": os.environ.get("XDG_SESSION_TYPE"),
        "DISPLAY": os.environ.get("DISPLAY"),
        "WAYLAND_DISPLAY": os.environ.get("WAYLAND_DISPLAY"),
        "CI": os.environ.get("CI"),
        "GITHUB_ACTIONS": os.environ.get("GITHUB_ACTIONS"),
    }
    if system == "windows":
        candidates = ["windows-11-uia", "windows-10-uia-esu", "windows-server-rds"]
    elif system == "darwin":
        candidates = ["macos-26-ax-apple-silicon", "macos-14-15-ax", "ios-xcuitest"]
    elif system == "linux":
        session = (env.get("XDG_SESSION_TYPE") or "").lower()
        if "wayland" in session or env.get("WAYLAND_DISPLAY"):
            candidates = ["ubuntu-24-04-wayland", "fedora-gnome-wayland", "kde-plasma-wayland", "debian-rhel-enterprise"]
        elif env.get("DISPLAY"):
            candidates = ["ubuntu-22-04-x11", "vnc-novnc-rfb", "debian-rhel-enterprise"]
        else:
            candidates = ["debian-rhel-enterprise"]
    else:
        candidates = []
    return {"system": system, "release": release, "machine": machine, "env": env, "candidate_profiles": candidates}


def native_matrix_markdown(targets: list[NativeTargetProfile] | None = None) -> str:
    targets = targets or list_native_targets()
    lines = [
        "# Native OS Test Lab Matrix",
        "",
        "This matrix separates Docker-contract validation from native data-plane validation.",
        "",
        "| Target | Family | Runner | Primary adapters | Risk focus | Evidence required |",
        "|---|---|---|---|---|---|",
    ]
    for t in targets:
        lines.append(
            "| {label} (`{id}`) | {family} | {runner} | {adapters} | {risks} | {evidence} |".format(
                label=t.label,
                id=t.id,
                family=t.family,
                runner=t.runner_kind,
                adapters=", ".join(t.primary_adapters),
                risks="; ".join(t.risk_focus[:3]),
                evidence="; ".join(t.evidence_required[:3]),
            )
        )
    summary = coverage_summary()
    lines.extend([
        "",
        "## Coverage summary",
        "",
        f"- Targets: {summary['target_count']}",
        f"- Families: {', '.join(summary['families'])}",
        f"- Missing required families: {', '.join(summary['missing_required_families']) or 'none'}",
        "",
    ])
    return "\n".join(lines)
