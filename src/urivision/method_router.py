# Author: Tom Sapletta · Part of the ifURI solution.
"""Deterministic method router for URI UI automation intents.

LLM should express intent; runtime should choose method. This router ranks adapters
for common UI operations based on the native target profile and returns an explicit
route with fallback candidates and verification URI.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .native_profiles import NativeTargetProfile, get_native_target

JsonDict = dict[str, Any]

INTENT_METHODS: dict[str, list[dict[str, Any]]] = {
    "read_ui_tree": [
        {"adapter": "browser_cdp", "uri": "browser://{target}/tree/query/snapshot", "quality": "semantic"},
        {"adapter": "windows_uia", "uri": "ui://{target}/tree/query/snapshot", "quality": "semantic"},
        {"adapter": "macos_ax", "uri": "ui://{target}/tree/query/snapshot", "quality": "semantic"},
        {"adapter": "at_spi", "uri": "ui://{target}/tree/query/snapshot", "quality": "semantic"},
        {"adapter": "uiautomator", "uri": "mobile://{target}/tree/query/snapshot", "quality": "semantic"},
        {"adapter": "xcuitest", "uri": "mobile://{target}/tree/query/snapshot", "quality": "semantic"},
        {"adapter": "vision_parser", "uri": "vision://{target}/screen/command/parse", "quality": "synthetic"},
    ],
    "find_element": [
        {"adapter": "browser_cdp", "uri": "browser://{target}/element/query/find", "quality": "semantic"},
        {"adapter": "windows_uia", "uri": "ui://{target}/element/query/find", "quality": "semantic"},
        {"adapter": "macos_ax", "uri": "ui://{target}/element/query/find", "quality": "semantic"},
        {"adapter": "at_spi", "uri": "ui://{target}/element/query/find", "quality": "semantic"},
        {"adapter": "uiautomator", "uri": "mobile://{target}/element/query/find", "quality": "semantic"},
        {"adapter": "xcuitest", "uri": "mobile://{target}/element/query/find", "quality": "semantic"},
        {"adapter": "ocr", "uri": "view://{target}/screen/query/text", "quality": "text-only"},
        {"adapter": "vision_parser", "uri": "vision://{target}/screen/command/parse", "quality": "synthetic"},
    ],
    "press_element": [
        {"adapter": "browser_cdp", "uri": "browser://{target}/element/command/press", "quality": "native"},
        {"adapter": "windows_uia", "uri": "ui://{target}/element/command/press", "quality": "native"},
        {"adapter": "macos_ax", "uri": "ui://{target}/element/command/press", "quality": "native"},
        {"adapter": "at_spi", "uri": "ui://{target}/element/command/press", "quality": "native"},
        {"adapter": "uiautomator", "uri": "mobile://{target}/element/command/press", "quality": "native"},
        {"adapter": "xcuitest", "uri": "mobile://{target}/element/command/press", "quality": "native"},
        {"adapter": "pointer", "uri": "input://{target}/pointer/command/click", "quality": "coordinate-fallback"},
        {"adapter": "vnc_rfb", "uri": "kvm://{target}/input/command/task_run", "quality": "remote-coordinate-fallback"},
        {"adapter": "hid_mouse", "uri": "hid://{target}/mouse/command/click", "quality": "hardware-fallback"},
    ],
    "type_text": [
        {"adapter": "browser_cdp", "uri": "browser://{target}/element/command/fill", "quality": "native"},
        {"adapter": "windows_uia", "uri": "ui://{target}/element/command/set-value", "quality": "native"},
        {"adapter": "macos_ax", "uri": "ui://{target}/element/command/set-value", "quality": "native"},
        {"adapter": "at_spi", "uri": "ui://{target}/element/command/set-value", "quality": "native"},
        {"adapter": "uiautomator", "uri": "mobile://{target}/element/command/set-value", "quality": "native"},
        {"adapter": "xcuitest", "uri": "mobile://{target}/element/command/set-value", "quality": "native"},
        {"adapter": "send_input", "uri": "input://{target}/keyboard/command/type", "quality": "focused-keyboard"},
        {"adapter": "cg_event", "uri": "input://{target}/keyboard/command/type", "quality": "focused-keyboard"},
        {"adapter": "vnc_rfb", "uri": "kvm://{target}/input/command/task_run", "quality": "remote-keyboard"},
        {"adapter": "hid_keyboard", "uri": "hid://{target}/keyboard/command/type", "quality": "hardware-keyboard"},
    ],
    "verify_text": [
        {"adapter": "browser_cdp", "uri": "browser://{target}/text/query/find", "quality": "semantic"},
        {"adapter": "windows_uia", "uri": "ui://{target}/tree/query/snapshot", "quality": "semantic"},
        {"adapter": "macos_ax", "uri": "ui://{target}/tree/query/snapshot", "quality": "semantic"},
        {"adapter": "at_spi", "uri": "ui://{target}/tree/query/snapshot", "quality": "semantic"},
        {"adapter": "ocr", "uri": "view://{target}/screen/query/text", "quality": "visual-text"},
        {"adapter": "vision_parser", "uri": "vision://{target}/screen/command/parse", "quality": "synthetic"},
    ],
    "capture_screen": [
        {"adapter": "browser_cdp", "uri": "browser://{target}/screenshot/query/capture", "quality": "app-level"},
        {"adapter": "screenshot", "uri": "view://{target}/screenshot/query/capture", "quality": "host-level"},
        {"adapter": "vnc_rfb", "uri": "kvm://{target}/screen/query/capture", "quality": "remote-pixel"},
        {"adapter": "hdmi_capture", "uri": "hid://{target}/screen/query/capture", "quality": "hardware-pixel"},
    ],
}


@dataclass(frozen=True)
class RouteDecision:
    intent: str
    target_profile: str
    selected: dict[str, Any] | None
    candidates: list[dict[str, Any]]
    verification_uri: str
    reason: str

    def to_dict(self) -> JsonDict:
        return {
            "intent": self.intent,
            "target_profile": self.target_profile,
            "selected": self.selected,
            "candidates": self.candidates,
            "verification_uri": self.verification_uri,
            "reason": self.reason,
        }


def route_intent(intent: str, profile: str | NativeTargetProfile, *, target: str = "local") -> RouteDecision:
    if isinstance(profile, str):
        p = get_native_target(profile)
    else:
        p = profile
    methods = INTENT_METHODS.get(intent)
    if not methods:
        known = ", ".join(sorted(INTENT_METHODS))
        raise KeyError(f"unknown intent {intent!r}; known: {known}")

    ordered_adapters = list(p.primary_adapters) + [a for a in p.fallback_adapters if a not in p.primary_adapters]
    adapter_order = {adapter: i for i, adapter in enumerate(ordered_adapters)}
    available = set(ordered_adapters)
    candidates: list[dict[str, Any]] = []
    for method in methods:
        item = dict(method)
        item["uri"] = item["uri"].format(target=target)
        item["available_in_profile"] = item["adapter"] in available
        item["method_rank"] = len(candidates) + 1
        item["profile_adapter_rank"] = adapter_order.get(item["adapter"], 999)
        candidates.append(item)

    available_candidates = [c for c in candidates if c["available_in_profile"]]
    selected = None
    if available_candidates:
        # Profile order wins over generic global order. This lets Windows choose UIA
        # for desktop work, macOS choose AX, Linux choose AT-SPI, while ChromeOS
        # can still prefer CDP because its profile lists browser_cdp first.
        selected = sorted(available_candidates, key=lambda c: (c["profile_adapter_rank"], c["method_rank"]))[0]

    reason = "selected by profile adapter preference, then generic method rank" if selected else "no compatible adapter listed for profile"
    verification_uri = "view://{target}/screen/query/text".format(target=target)
    if intent in {"press_element", "type_text"}:
        verification_uri = "guard://{target}/batch/command/run".format(target=target)
    return RouteDecision(intent=intent, target_profile=p.id, selected=selected, candidates=candidates, verification_uri=verification_uri, reason=reason)


def route_matrix(*, target: str = "local") -> JsonDict:
    from .native_profiles import list_native_targets

    return {
        "schema": "schema://runtime/method-router-matrix.v1",
        "intents": sorted(INTENT_METHODS),
        "routes": {
            profile.id: {intent: route_intent(intent, profile, target=target).to_dict() for intent in sorted(INTENT_METHODS)}
            for profile in list_native_targets()
        },
    }
