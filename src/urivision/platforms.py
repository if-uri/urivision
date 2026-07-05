# Author: Tom Sapletta · Part of the ifURI solution.
"""Backend platform profiles for Docker and multi-OS contract testing.

These profiles do not pretend that Linux Docker can become Windows or macOS.
They describe which URI capabilities should exist for a given target family and
what is only a contract/stub until a native adapter is installed on that OS.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

JsonDict = dict[str, Any]


@dataclass(frozen=True)
class BackendProfile:
    name: str
    label: str
    os_family: str
    display_stack: str
    profile_kind: str
    description: str
    observe: list[str] = field(default_factory=list)
    act: list[str] = field(default_factory=list)
    preferred_backends: list[str] = field(default_factory=list)
    unavailable: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    docker_service: str | None = None

    def to_dict(self) -> JsonDict:
        return {
            "name": self.name,
            "label": self.label,
            "os_family": self.os_family,
            "display_stack": self.display_stack,
            "profile_kind": self.profile_kind,
            "description": self.description,
            "observe": list(self.observe),
            "act": list(self.act),
            "preferred_backends": list(self.preferred_backends),
            "unavailable": list(self.unavailable),
            "limitations": list(self.limitations),
            "docker_service": self.docker_service,
        }


PROFILES: dict[str, BackendProfile] = {
    "mock-local": BackendProfile(
        name="mock-local",
        label="Mock local runtime",
        os_family="portable",
        display_stack="mock",
        profile_kind="in-process-mock",
        description="Dependency-free local profile used for unit tests and LLM catalog validation.",
        observe=["mock_accessibility_tree", "mock_screen_text", "mock_screenshot"],
        act=["mock_focus", "mock_press", "mock_keyboard", "mock_pointer", "mock_kvm_batch"],
        preferred_backends=["accessibility", "browser_dom", "keyboard", "pointer"],
        limitations=["Does not control a real OS session", "Used only to validate URI contracts and orchestration"],
    ),
    "linux-x11-novnc": BackendProfile(
        name="linux-x11-novnc",
        label="Linux X11 + noVNC profile",
        os_family="linux",
        display_stack="x11/novnc",
        profile_kind="docker-contract-plus-x11-tools",
        description="Docker profile prepared for Xvfb/x11vnc/noVNC style testing. Current Python handlers remain URI-contract adapters unless real connector is mounted.",
        observe=["accessibility_tree", "screen_text", "screenshot", "vnc_screen"],
        act=["keyboard", "pointer", "kvm_batch", "native_press_if_adapter_available"],
        preferred_backends=["at_spi", "x11", "vnc", "keyboard", "pointer"],
        unavailable=["secure_desktop", "bios", "host_wayland_global_input"],
        limitations=["Coordinate mapping may differ between Xvfb, VNC and client browser scaling", "AT-SPI data quality depends on application toolkit"],
        docker_service="linux-x11-novnc",
    ),
    "linux-wayland-headless": BackendProfile(
        name="linux-wayland-headless",
        label="Linux Wayland headless profile",
        os_family="linux",
        display_stack="wayland/headless",
        profile_kind="docker-contract-plus-wayland-tools",
        description="Headless Wayland profile for validating that URI runtime exposes explicit limitations around surface-relative coordinates and input portals.",
        observe=["accessibility_tree_if_exported", "screenshot_if_compositor_allows", "screen_text"],
        act=["keyboard_if_portal_or_libei_available", "pointer_if_portal_or_libei_available", "kvm_batch_fallback"],
        preferred_backends=["at_spi", "xdg_portal_remote_desktop", "libei", "kvm", "hid"],
        unavailable=["global_x11_coordinates", "unrestricted_global_input"],
        limitations=["Wayland commonly blocks global pointer/keyboard injection", "Coordinates may be surface-relative instead of global"],
        docker_service="linux-wayland-headless",
    ),
    "windows-uia-contract": BackendProfile(
        name="windows-uia-contract",
        label="Windows UI Automation contract profile",
        os_family="windows",
        display_stack="desktop/uia",
        profile_kind="contract-only-in-linux-docker",
        description="Validates URI contracts for a future Windows native adapter. Real UIA execution must run on a Windows host/session, not in Linux Docker.",
        observe=["uia_tree", "active_window", "screenshot"],
        act=["uia_invoke", "uia_set_value", "send_input", "rdp_or_vnc", "hid_fallback"],
        preferred_backends=["windows_uia", "browser_cdp", "send_input", "rdp", "hid"],
        unavailable=["uac_secure_desktop_without_elevation", "different_user_session_without_broker"],
        limitations=["This Docker profile validates schema and orchestration only", "Real UIA requires Windows permissions/session boundary handling"],
        docker_service="windows-uia-contract",
    ),
    "macos-ax-contract": BackendProfile(
        name="macos-ax-contract",
        label="macOS AXUIElement contract profile",
        os_family="macos",
        display_stack="desktop/ax",
        profile_kind="contract-only-in-linux-docker",
        description="Validates URI contracts for a future macOS Accessibility adapter. Real AX execution requires a macOS host with TCC permissions.",
        observe=["ax_tree", "focused_element", "screenshot"],
        act=["ax_press", "ax_set_value", "cg_event", "hid_fallback"],
        preferred_backends=["macos_ax", "browser_cdp", "cg_event", "hid"],
        unavailable=["secure_input", "tcc_denied_screen_recording", "tcc_denied_accessibility"],
        limitations=["This Docker profile validates schema and orchestration only", "Real AX requires Accessibility, Screen Recording and Input Monitoring permissions"],
        docker_service="macos-ax-contract",
    ),
}


DEFAULT_MATRIX = [
    "linux-x11-novnc",
    "linux-wayland-headless",
    "windows-uia-contract",
    "macos-ax-contract",
]


def list_backend_profiles() -> list[BackendProfile]:
    return [PROFILES[name] for name in sorted(PROFILES)]


def get_backend_profile(name: str | None = None) -> BackendProfile:
    selected = name or os.environ.get("URIVISION_BACKEND_PROFILE") or os.environ.get("URIVISION_PROFILE") or "mock-local"
    if selected not in PROFILES:
        known = ", ".join(sorted(PROFILES))
        raise KeyError(f"unknown backend profile: {selected!r}; known: {known}")
    return PROFILES[selected]
