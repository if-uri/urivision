# Author: Tom Sapletta · Part of the ifURI solution.
"""Default URI runtime for desktop/browser/KVM/vision orchestration.

The default runtime is intentionally dependency-free. It exposes stable URI
capabilities and mockable state. Real OS-specific implementations should replace
handlers behind the same URI contracts.
"""
from __future__ import annotations

import time
from copy import deepcopy
from typing import Any

from .capability import Capability, RuntimeContext
from .registry import CapabilityRegistry
from .platforms import get_backend_profile, list_backend_profiles

JsonDict = dict[str, Any]


def _schema(props: dict[str, Any], required: list[str] | None = None, *, additional: bool = True) -> JsonDict:
    return {"type": "object", "additionalProperties": additional, "required": required or [], "properties": props}


def _ok(**data: Any) -> JsonDict:
    return {"ok": True, **data}


def _default_tree() -> JsonDict:
    return {
        "id": "desktop:root",
        "role": "desktop",
        "name": "local",
        "children": [
            {
                "id": "window:demo",
                "role": "window",
                "name": "Demo App",
                "bounds": {"x": 0, "y": 0, "width": 1280, "height": 800},
                "children": [
                    {"id": "field:search", "role": "textbox", "name": "Search", "value": "", "actions": ["focus", "set_value"], "bounds": {"x": 40, "y": 40, "width": 440, "height": 32}},
                    {"id": "button:save", "role": "button", "name": "Save", "actions": ["press"], "bounds": {"x": 500, "y": 40, "width": 96, "height": 32}},
                    {"id": "button:cancel", "role": "button", "name": "Cancel", "actions": ["press"], "bounds": {"x": 610, "y": 40, "width": 96, "height": 32}},
                ],
            }
        ],
    }


def _ensure_state(ctx: RuntimeContext) -> None:
    ctx.state.setdefault("tree", _default_tree())
    ctx.state.setdefault("screen_text", "Demo App Search Save Cancel")
    ctx.state.setdefault("focused", None)
    ctx.state.setdefault("typed", "")
    ctx.state.setdefault("pressed", [])
    ctx.state.setdefault("events", [])
    ctx.state.setdefault("backend_profile", None)


def _walk(node: JsonDict) -> list[JsonDict]:
    out = [node]
    for child in node.get("children", []) or []:
        out.extend(_walk(child))
    return out


def _find_element(tree: JsonDict, payload: JsonDict) -> JsonDict | None:
    role = payload.get("role")
    name = payload.get("name")
    text = payload.get("text")
    element_id = payload.get("element_id") or payload.get("id")
    contains = payload.get("contains")
    for el in _walk(tree):
        if element_id and el.get("id") != element_id:
            continue
        if role and el.get("role") != role:
            continue
        if name and str(el.get("name", "")).lower() != str(name).lower():
            continue
        hay = " ".join(str(el.get(k, "")) for k in ("name", "value", "text"))
        if text and str(text).lower() not in hay.lower():
            continue
        if contains and str(contains).lower() not in hay.lower():
            continue
        return deepcopy(el)
    return None


def build_default_registry() -> CapabilityRegistry:
    r = CapabilityRegistry()

    def register(cap: Capability, fn):
        return r.register(cap, fn)

    def runtime_list(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        return _ok(target=captures.get("target"), catalog=r.catalog_json())

    register(Capability(
        uri_pattern="runtime://{target}/capabilities/query/list",
        title="List runtime capabilities",
        description="Zwraca pełny katalog funkcji dostępnych w runtime. Użyj jako pierwszy krok dla LLM.",
        kind="query",
        input_schema=_schema({"format": {"type": "string", "enum": ["json", "markdown", "prompt", "tools"]}}),
        output_schema=_schema({"catalog": {"type": "object"}}, ["catalog"]),
        idempotent=True,
        tags=["introspection", "llm"],
        examples=[{"uri": "runtime://local/capabilities/query/list", "with": {"format": "json"}}],
    ), runtime_list)

    def runtime_explain(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        uri = payload["uri"]
        cap, cap_captures = r.find(uri)
        return _ok(uri=uri, captures=cap_captures, capability=cap.to_dict())

    register(Capability(
        uri_pattern="runtime://{target}/capability/query/explain",
        title="Explain one capability",
        description="Wyjaśnia, która capability obsłuży podany URI oraz jakiego payloadu oczekuje.",
        kind="query",
        input_schema=_schema({"uri": {"type": "string"}}, ["uri"], additional=False),
        output_schema=_schema({"capability": {"type": "object"}}, ["capability"]),
        idempotent=True,
        tags=["introspection", "debug"],
        examples=[{"uri": "runtime://local/capability/query/explain", "with": {"uri": "input://local/keyboard/command/type"}}],
    ), runtime_explain)


    def platform_profile(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        requested = payload.get("profile") or ctx.state.get("backend_profile")
        profile = get_backend_profile(requested)
        ctx.state["backend_profile"] = profile.name
        return _ok(target=captures.get("target"), profile=profile.to_dict())

    register(Capability(
        uri_pattern="runtime://{target}/platform/query/profile",
        title="Read selected backend platform profile",
        description="Zwraca profil backendu: Linux/X11, Linux/Wayland, Windows UIA, macOS AX albo mock. Użyj do świadomego wyboru metody wykonania.",
        kind="query",
        input_schema=_schema({"profile": {"type": "string"}}),
        output_schema=_schema({"profile": {"type": "object"}}, ["profile"]),
        idempotent=True,
        tags=["runtime", "platform", "capability-discovery"],
        examples=[{"uri": "runtime://local/platform/query/profile", "with": {"profile": "linux-x11-novnc"}}],
    ), platform_profile)

    def platform_list(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        return _ok(target=captures.get("target"), profiles=[p.to_dict() for p in list_backend_profiles()])

    register(Capability(
        uri_pattern="runtime://{target}/platform/query/list",
        title="List known backend platform profiles",
        description="Lista profili backendów używanych w Docker/matrix testach i capability discovery.",
        kind="query",
        input_schema=_schema({}),
        output_schema=_schema({"profiles": {"type": "array"}}, ["profiles"]),
        idempotent=True,
        tags=["runtime", "platform", "matrix"],
        examples=[{"uri": "runtime://local/platform/query/list", "with": {}}],
    ), platform_list)

    def runtime_health(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        profile = get_backend_profile(ctx.state.get("backend_profile") or payload.get("profile"))
        required = [
            "runtime://local/capabilities/query/list",
            "runtime://local/platform/query/profile",
            "ui://local/tree/query/snapshot",
            "ui://local/element/query/find",
            "input://local/keyboard/command/type",
            "view://local/screen/query/text",
            "guard://local/batch/command/run",
        ]
        checks = []
        for uri in required:
            try:
                cap, _ = r.find(uri)
                checks.append({"uri": uri, "ok": True, "capability": cap.uri_pattern})
            except Exception as exc:  # pragma: no cover - diagnostic path
                checks.append({"uri": uri, "ok": False, "error": str(exc)})
        return _ok(profile=profile.to_dict(), checks=checks, passed=all(c["ok"] for c in checks))

    register(Capability(
        uri_pattern="runtime://{target}/health/query/check",
        title="Runtime health check",
        description="Sprawdza minimalny zestaw capabilities wymagany przez warstwę Docker i test matrix.",
        kind="query",
        input_schema=_schema({"profile": {"type": "string"}}),
        output_schema=_schema({"passed": {"type": "boolean"}, "checks": {"type": "array"}}, ["passed", "checks"]),
        idempotent=True,
        tags=["runtime", "health", "matrix"],
        examples=[{"uri": "runtime://local/health/query/check", "with": {"profile": "linux-x11-novnc"}}],
    ), runtime_health)

    def tree_snapshot(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        return _ok(target=captures.get("target"), tree=deepcopy(ctx.state["tree"]), source="mock-accessibility-tree")

    register(Capability(
        uri_pattern="ui://{target}/tree/query/snapshot",
        title="Read UI semantic tree",
        description="Czyta znormalizowane drzewo UI. W realnym adapterze: UIA/AX/AT-SPI/CDP; w mocku: przykładowe drzewo.",
        kind="query",
        input_schema=_schema({"max_depth": {"type": "integer"}}),
        output_schema=_schema({"tree": {"type": "object"}, "source": {"type": "string"}}, ["tree"]),
        idempotent=True,
        tags=["ui", "accessibility", "observe"],
        examples=[{"uri": "ui://local/tree/query/snapshot", "with": {}}],
    ), tree_snapshot)

    def element_find(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        el = _find_element(ctx.state["tree"], payload)
        return _ok(found=el is not None, element=el, locator=payload)

    register(Capability(
        uri_pattern="ui://{target}/element/query/find",
        title="Find UI element by semantic locator",
        description="Znajduje element po roli, nazwie, tekście lub id. To odpowiednik prostego locatora jak w Playwright, ale dla desktopowego UI.",
        kind="query",
        input_schema=_schema({
            "role": {"type": "string"},
            "name": {"type": "string"},
            "text": {"type": "string"},
            "contains": {"type": "string"},
            "element_id": {"type": "string"},
        }),
        output_schema=_schema({"found": {"type": "boolean"}, "element": {"type": ["object", "null"]}}, ["found"]),
        idempotent=True,
        tags=["ui", "locator", "observe"],
        examples=[{"uri": "ui://local/element/query/find", "with": {"role": "button", "name": "Save"}}],
    ), element_find)

    def element_focus(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        element_id = payload["element_id"]
        el = _find_element(ctx.state["tree"], {"element_id": element_id})
        if not el:
            return {"ok": False, "error": "element_not_found", "element_id": element_id}
        ctx.state["focused"] = element_id
        return _ok(focused=element_id)

    register(Capability(
        uri_pattern="ui://{target}/element/command/focus",
        title="Focus UI element",
        description="Ustawia fokus na elemencie przez natywne API UI, jeśli adapter to wspiera. Fallback: klik/fokus.",
        kind="command",
        input_schema=_schema({"element_id": {"type": "string"}}, ["element_id"], additional=False),
        output_schema=_schema({"focused": {"type": "string"}}, ["focused"]),
        side_effects=["changes focused element"],
        postconditions=["focused element equals element_id"],
        tags=["ui", "action"],
        examples=[{"uri": "ui://local/element/command/focus", "with": {"element_id": "field:search"}}],
    ), element_focus)

    def element_press(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        element_id = payload["element_id"]
        el = _find_element(ctx.state["tree"], {"element_id": element_id})
        if not el:
            return {"ok": False, "error": "element_not_found", "element_id": element_id}
        ctx.state["pressed"].append(element_id)
        ctx.state["events"].append({"type": "press", "element_id": element_id, "ts": time.time()})
        return _ok(pressed=element_id, element=el)

    register(Capability(
        uri_pattern="ui://{target}/element/command/press",
        title="Press UI element natively",
        description="Wykonuje natywną akcję press/invoke elementu bez używania myszy, jeśli adapter to wspiera.",
        kind="command",
        input_schema=_schema({"element_id": {"type": "string"}}, ["element_id"], additional=False),
        output_schema=_schema({"pressed": {"type": "string"}}, ["pressed"]),
        side_effects=["invokes control action"],
        tags=["ui", "action", "preferred-over-pointer"],
        examples=[{"uri": "ui://local/element/command/press", "with": {"element_id": "button:save"}}],
    ), element_press)

    def keyboard_type(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        text = payload["text"]
        ctx.state["typed"] += text
        focused = ctx.state.get("focused")
        if focused:
            for el in _walk(ctx.state["tree"]):
                if el.get("id") == focused and el.get("role") in {"textbox", "text", "textarea"}:
                    el["value"] = str(el.get("value", "")) + text
        ctx.state["screen_text"] += " " + text
        return _ok(typed=text, focused=focused)

    register(Capability(
        uri_pattern="input://{target}/keyboard/command/type",
        title="Type text through keyboard backend",
        description="Wysyła tekst przez backend klawiatury. Używać po focus/locator i zawsze z postcondition verify.",
        kind="command",
        input_schema=_schema({"text": {"type": "string"}}, ["text"], additional=False),
        output_schema=_schema({"typed": {"type": "string"}}, ["typed"]),
        side_effects=["sends keyboard input", "may type into wrong focused element if focus is stale"],
        preconditions=["target window active", "intended element focused"],
        postconditions=["expected text visible or value changed"],
        safety="needs-verification",
        tags=["input", "keyboard", "fallback"],
        examples=[{"uri": "input://local/keyboard/command/type", "with": {"text": "hello"}}],
    ), keyboard_type)

    def keyboard_hotkey(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        keys = payload["keys"]
        if isinstance(keys, str):
            keys = [p.strip() for p in keys.replace("+", ",").split(",") if p.strip()]
        ctx.state["events"].append({"type": "hotkey", "keys": keys, "ts": time.time()})
        return _ok(keys=keys)

    register(Capability(
        uri_pattern="input://{target}/keyboard/command/hotkey",
        title="Send keyboard shortcut",
        description="Wysyła skrót klawiszowy, np. Ctrl+L. Używać do stabilnych systemowych przejść, nie do semantyki UI.",
        kind="command",
        input_schema=_schema({"keys": {"type": ["array", "string"]}}, ["keys"], additional=False),
        output_schema=_schema({"keys": {"type": "array"}}, ["keys"]),
        side_effects=["sends keyboard shortcut"],
        safety="needs-verification",
        tags=["input", "keyboard"],
        examples=[{"uri": "input://local/keyboard/command/hotkey", "with": {"keys": ["CTRL", "L"]}}],
    ), keyboard_hotkey)

    def pointer_click(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        x, y = payload["x"], payload["y"]
        ctx.state["events"].append({"type": "click", "x": x, "y": y, "button": payload.get("button", "left"), "ts": time.time()})
        return _ok(x=x, y=y, button=payload.get("button", "left"))

    register(Capability(
        uri_pattern="input://{target}/pointer/command/click",
        title="Click pointer coordinates",
        description="Awaryjne kliknięcie we współrzędne. Powinno być wybierane dopiero po niepowodzeniu DOM/accessibility/native action.",
        kind="command",
        input_schema=_schema({"x": {"type": "integer"}, "y": {"type": "integer"}, "button": {"type": "string"}}, ["x", "y"]),
        output_schema=_schema({"x": {"type": "integer"}, "y": {"type": "integer"}}, ["x", "y"]),
        side_effects=["moves/clicks pointer", "fragile under scaling/layout changes"],
        safety="last-resort",
        tags=["input", "pointer", "fallback"],
        examples=[{"uri": "input://local/pointer/command/click", "with": {"x": 500, "y": 40}}],
    ), pointer_click)

    def view_text(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        contains = payload.get("contains")
        text = ctx.state.get("screen_text", "")
        return _ok(text=text, contains=contains, found=(contains.lower() in text.lower()) if contains else None)

    register(Capability(
        uri_pattern="view://{target}/screen/query/text",
        title="Read visible screen text",
        description="Zwraca tekst z aktualnego widoku. W realnym adapterze: OCR/cache/crop; w mocku: tekst ze stanu.",
        kind="query",
        input_schema=_schema({"contains": {"type": "string"}, "region": {"type": "object"}}),
        output_schema=_schema({"text": {"type": "string"}, "found": {"type": ["boolean", "null"]}}, ["text"]),
        idempotent=True,
        tags=["view", "ocr", "verify"],
        examples=[{"uri": "view://local/screen/query/text", "with": {"contains": "Save"}}],
    ), view_text)

    def screenshot_capture(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        return _ok(source="mock-screenshot", artifact_uri=payload.get("emit"), width=1280, height=800)

    register(Capability(
        uri_pattern="view://{target}/screenshot/query/capture",
        title="Capture screenshot",
        description="Pobiera zrzut ekranu jako artefakt. Realne backendy: VNC/RDP/OS API/HDMI capture.",
        kind="query",
        input_schema=_schema({"emit": {"type": "string"}, "max_width": {"type": "integer"}, "region": {"type": "object"}}),
        output_schema=_schema({"artifact_uri": {"type": ["string", "null"]}, "width": {"type": "integer"}, "height": {"type": "integer"}}),
        idempotent=True,
        tags=["view", "screenshot", "observe"],
        examples=[{"uri": "view://local/screenshot/query/capture", "with": {"emit": "artifact://screenshots/current.png", "max_width": 1600}}],
    ), screenshot_capture)

    def browser_fill(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        selector, text = payload["selector"], payload["text"]
        ctx.state["events"].append({"type": "browser.fill", "selector": selector, "text": text, "ts": time.time()})
        ctx.state["screen_text"] += " " + text
        return _ok(selector=selector, filled=text)

    register(Capability(
        uri_pattern="browser://{target}/element/command/fill",
        title="Fill browser DOM element",
        description="Wpisuje tekst przez DOM/CDP/Playwright. Preferowane dla przeglądarki i Electron, bo omija problem fokusu myszy/klawiatury.",
        kind="command",
        input_schema=_schema({"selector": {"type": "string"}, "text": {"type": "string"}}, ["selector", "text"], additional=False),
        output_schema=_schema({"selector": {"type": "string"}, "filled": {"type": "string"}}, ["selector", "filled"]),
        side_effects=["changes DOM input value"],
        postconditions=["DOM value equals text"],
        tags=["browser", "dom", "preferred"],
        examples=[{"uri": "browser://chrome/element/command/fill", "with": {"selector": "textarea[name=q]", "text": "URI runtime"}}],
    ), browser_fill)

    def vision_parse(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        return _ok(
            source="mock-vision-dom",
            elements=[
                {"id": "vision:save", "role": "button", "name": "Save", "bounds": {"x": 500, "y": 40, "width": 96, "height": 32}, "confidence": 0.72}
            ],
        )

    register(Capability(
        uri_pattern="vision://{target}/screen/command/parse",
        title="Parse screenshot into synthetic UI elements",
        description="Fallback perception: screen → synthetic UI elements. Używać gdy accessibility/DOM nie wystarcza.",
        kind="command",
        input_schema=_schema({"image_uri": {"type": "string"}, "aspects": {"type": "array"}}),
        output_schema=_schema({"elements": {"type": "array"}, "source": {"type": "string"}}, ["elements"]),
        side_effects=["may call LLM/vision model"],
        safety="fallback-perception",
        tags=["vision", "fallback", "synthetic-dom"],
        examples=[{"uri": "vision://local/screen/command/parse", "with": {"image_uri": "artifact://screenshots/current.png", "aspects": ["ui/click-targets"]}}],
    ), vision_parse)

    def kvm_task_run(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        _ensure_state(ctx)
        steps = payload.get("steps", [])
        results = []
        for step in steps:
            op = step.get("op")
            if op == "type":
                results.append(r.call(f"input://{captures.get('target', 'local')}/keyboard/command/type", {"text": step.get("text", "")}, ctx=ctx))
            elif op == "hotkey" or op == "key":
                results.append(r.call(f"input://{captures.get('target', 'local')}/keyboard/command/hotkey", {"keys": step.get("keys", [])}, ctx=ctx))
            elif op == "click":
                results.append(r.call(f"input://{captures.get('target', 'local')}/pointer/command/click", {"x": step.get("x", 0), "y": step.get("y", 0)}, ctx=ctx))
            else:
                results.append({"ok": False, "error": "unknown_step", "step": step})
        return _ok(results=results)

    register(Capability(
        uri_pattern="kvm://{target}/input/command/task_run",
        title="Run batched KVM input steps",
        description="Batch input actions over KVM/VNC/HID-like channel. Faster than many round-trips, but must be guarded by postconditions.",
        kind="command",
        input_schema=_schema({"steps": {"type": "array"}}, ["steps"], additional=False),
        output_schema=_schema({"results": {"type": "array"}}, ["results"]),
        side_effects=["sends multiple input events"],
        safety="needs-verification",
        tags=["kvm", "batch", "input"],
        examples=[{"uri": "kvm://local/input/command/task_run", "with": {"steps": [{"op": "type", "text": "hello"}]}}],
    ), kvm_task_run)

    def guard_batch(ctx: RuntimeContext, payload: JsonDict, captures: dict[str, str]) -> JsonDict:
        steps = payload.get("steps", [])
        expect = payload.get("expect") or {}
        tries = int(payload.get("tries", 2))
        target = captures.get("target", "local")
        last_verify: JsonDict = {}
        for i in range(tries):
            r.call(f"kvm://{target}/input/command/task_run", {"steps": steps}, ctx=ctx)
            if expect:
                last_verify = r.call(expect.get("uri", f"view://{target}/screen/query/text"), expect.get("with", {}), ctx=ctx)
                # Convention: found true or ok true with no explicit found means pass.
                if last_verify.get("found") is True or ("found" not in last_verify and last_verify.get("ok")):
                    return _ok(tries=i + 1, verified=True, verify=last_verify)
            else:
                return _ok(tries=i + 1, verified=False)
        return {"ok": False, "tries": tries, "verified": False, "verify": last_verify}

    register(Capability(
        uri_pattern="guard://{target}/batch/command/run",
        title="Guarded batch: actions plus postcondition",
        description="Wykonuje batch i po nim sprawdza postcondition. To wzorzec verify-before-act dla kruchego inputu.",
        kind="command",
        input_schema=_schema({"steps": {"type": "array"}, "expect": {"type": "object"}, "tries": {"type": "integer"}}, ["steps"]),
        output_schema=_schema({"verified": {"type": "boolean"}, "tries": {"type": "integer"}}, ["verified"]),
        side_effects=["sends input events", "may retry"],
        safety="guarded-action",
        tags=["guard", "verify-before-act", "batch"],
        examples=[{"uri": "guard://local/batch/command/run", "with": {"steps": [{"op": "type", "text": "hello"}], "expect": {"uri": "view://local/screen/query/text", "with": {"contains": "hello"}}}}],
    ), guard_batch)

    return r


class UriRuntime:
    def __init__(self, registry: CapabilityRegistry | None = None, *, ctx: RuntimeContext | None = None) -> None:
        self.registry = registry or build_default_registry()
        self.ctx = ctx or RuntimeContext()

    def call(self, uri: str, payload: JsonDict | None = None, *, dry_run: bool | None = None) -> JsonDict:
        old = self.ctx.dry_run
        if dry_run is not None:
            self.ctx.dry_run = dry_run
        try:
            return self.registry.call(uri, payload or {}, ctx=self.ctx)
        finally:
            self.ctx.dry_run = old

    def catalog(self, fmt: str = "json") -> Any:
        if fmt == "markdown":
            return self.registry.catalog_markdown()
        if fmt == "prompt":
            return self.registry.catalog_prompt()
        if fmt == "tools":
            return self.registry.tools_json()
        return self.registry.catalog_json()

    def explain(self, uri: str) -> JsonDict:
        return self.call("runtime://local/capability/query/explain", {"uri": uri})

    def trace(self) -> list[JsonDict]:
        return list(self.ctx.trace)


def default_runtime(*, dry_run: bool = False, state: JsonDict | None = None) -> UriRuntime:
    return UriRuntime(ctx=RuntimeContext(dry_run=dry_run, state=state or {}))
