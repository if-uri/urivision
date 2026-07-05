#!/usr/bin/env python3
"""Probe the current host for native URI automation readiness.

This script uses only Python stdlib. It does not claim success for Windows UIA,
macOS AX or Wayland input; it reports evidence and missing probes.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Any

JsonDict = dict[str, Any]

COMMANDS = [
    "python", "python3", "powershell", "pwsh", "osascript", "xcrun", "xcodebuild",
    "adb", "docker", "podman", "gdbus", "busctl", "xprop", "xdotool", "wmctrl",
    "swaymsg", "ydotool", "loginctl", "xrandr", "system_profiler",
]


def run_short(cmd: list[str]) -> dict[str, Any]:
    try:
        cp = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
        return {"ok": cp.returncode == 0, "returncode": cp.returncode, "stdout": cp.stdout[:1200], "stderr": cp.stderr[:1200]}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "message": str(exc)}


def read_os_release() -> dict[str, str]:
    path = Path("/etc/os-release")
    if not path.exists():
        return {}
    data: dict[str, str] = {}
    for line in path.read_text(errors="ignore").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            data[k] = v.strip().strip('"')
    return data


def probe() -> JsonDict:
    system = platform.system()
    env_keys = ["CI", "GITHUB_ACTIONS", "RUNNER_OS", "XDG_SESSION_TYPE", "DISPLAY", "WAYLAND_DISPLAY", "DESKTOP_SESSION", "XDG_CURRENT_DESKTOP"]
    found_commands = {cmd: shutil.which(cmd) for cmd in COMMANDS}
    evidence: JsonDict = {
        "schema": "schema://runtime/native-host-probe.v1",
        "platform": {
            "system": system,
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "os_release": read_os_release(),
        },
        "env": {k: os.environ.get(k) for k in env_keys},
        "commands": found_commands,
        "checks": {},
    }

    if system == "Linux":
        evidence["checks"]["session"] = {
            "xdg_session_type": os.environ.get("XDG_SESSION_TYPE"),
            "display": os.environ.get("DISPLAY"),
            "wayland_display": os.environ.get("WAYLAND_DISPLAY"),
        }
        if shutil.which("gdbus"):
            evidence["checks"]["portal"] = run_short(["gdbus", "introspect", "--session", "--dest", "org.freedesktop.portal.Desktop", "--object-path", "/org/freedesktop/portal/desktop"])
        if shutil.which("xprop") and os.environ.get("DISPLAY"):
            evidence["checks"]["x11_root"] = run_short(["xprop", "-root", "_NET_SUPPORTING_WM_CHECK"])
        evidence["checks"]["python_atspi_import"] = run_short(["python3", "-c", "import pyatspi; print('pyatspi-ok')"]) if shutil.which("python3") else {"ok": False, "error": "python3 missing"}

    elif system == "Darwin":
        if shutil.which("sw_vers"):
            evidence["checks"]["sw_vers"] = run_short(["sw_vers"])
        if shutil.which("osascript"):
            evidence["checks"]["osascript_ui_allowed_hint"] = run_short(["osascript", "-e", "tell application \"System Events\" to get UI elements enabled"])
        if shutil.which("xcrun"):
            evidence["checks"]["simctl_list"] = run_short(["xcrun", "simctl", "list", "devices", "available"])

    elif system == "Windows":
        shell = "powershell" if shutil.which("powershell") else "pwsh" if shutil.which("pwsh") else None
        if shell:
            evidence["checks"]["windows_version"] = run_short([shell, "-NoProfile", "-Command", "[Environment]::OSVersion.VersionString"])
            evidence["checks"]["uia_assembly"] = run_short([shell, "-NoProfile", "-Command", "Add-Type -AssemblyName UIAutomationClient; 'uia-assembly-ok'"])
            evidence["checks"]["dpi_hint"] = run_short([shell, "-NoProfile", "-Command", "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::AllScreens | ConvertTo-Json -Depth 3"])

    if shutil.which("adb"):
        evidence["checks"]["adb_devices"] = run_short(["adb", "devices", "-l"])
    return evidence


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    args = ap.parse_args()
    data = probe()
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
