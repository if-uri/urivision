# Author: Tom Sapletta · Part of the ifURI solution.
"""Registry and dispatcher for URI-addressable capabilities."""
from __future__ import annotations

import inspect
import json
from typing import Any, Callable

from .capability import Capability, CapabilityHandler, RuntimeContext
from .uri import match_uri

JsonDict = dict[str, Any]


class UriDispatchError(RuntimeError):
    pass


class PayloadValidationError(ValueError):
    pass


def _json_type_ok(value: Any, expected: str) -> bool:
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    if expected in ("any", "null"):
        return True
    return True


def validate_payload(schema: JsonDict, payload: JsonDict) -> None:
    if schema.get("type", "object") != "object":
        return
    if not isinstance(payload, dict):
        raise PayloadValidationError("payload must be an object")
    required = schema.get("required", [])
    missing = [name for name in required if name not in payload]
    if missing:
        raise PayloadValidationError(f"missing required payload keys: {', '.join(missing)}")
    props = schema.get("properties", {})
    for name, value in payload.items():
        spec = props.get(name)
        if not spec:
            if schema.get("additionalProperties", True) is False:
                raise PayloadValidationError(f"unknown payload key: {name}")
            continue
        expected = spec.get("type", "any")
        if isinstance(expected, list):
            ok = any(_json_type_ok(value, t) for t in expected)
        else:
            ok = _json_type_ok(value, expected)
        if not ok:
            raise PayloadValidationError(f"payload key {name!r} must be {expected}, got {type(value).__name__}")


class CapabilityRegistry:
    def __init__(self) -> None:
        self._items: list[Capability] = []

    def register(self, capability: Capability, handler: CapabilityHandler | None = None) -> Capability:
        if handler is not None:
            capability.handler = handler
        self._items.append(capability)
        self._items.sort(key=lambda c: c.priority)
        return capability

    def capability(
        self,
        uri_pattern: str,
        *,
        title: str,
        description: str,
        kind: str,
        input_schema: JsonDict | None = None,
        output_schema: JsonDict | None = None,
        **meta: Any,
    ) -> Callable[[CapabilityHandler], CapabilityHandler]:
        def deco(fn: CapabilityHandler) -> CapabilityHandler:
            self.register(
                Capability(
                    uri_pattern=uri_pattern,
                    title=title,
                    description=description,
                    kind=kind,  # type: ignore[arg-type]
                    input_schema=input_schema or schema_from_signature(fn),
                    output_schema=output_schema or {"type": "object", "properties": {}},
                    handler=fn,
                    **meta,
                )
            )
            return fn

        return deco

    def find(self, uri: str) -> tuple[Capability, dict[str, str]]:
        for cap in self._items:
            captures = match_uri(cap.uri_pattern, uri)
            if captures is not None:
                return cap, captures
        raise UriDispatchError(f"No capability registered for URI: {uri}")

    def call(self, uri: str, payload: JsonDict | None = None, *, ctx: RuntimeContext | None = None) -> JsonDict:
        payload = payload or {}
        ctx = ctx or RuntimeContext()
        cap, captures = self.find(uri)
        validate_payload(cap.input_schema, payload)
        event = {"uri": uri, "capability": cap.uri_pattern, "payload": payload, "dry_run": ctx.dry_run}
        ctx.emit({"type": "call.started", **event})
        if ctx.dry_run:
            result = {"ok": True, "dry_run": True, "uri": uri, "would_call": cap.to_dict()}
        else:
            if cap.handler is None:
                raise UriDispatchError(f"Capability has no handler: {cap.uri_pattern}")
            result = cap.handler(ctx, payload, captures)
            if not isinstance(result, dict):
                result = {"ok": True, "result": result}
        ctx.emit({"type": "call.finished", **event, "result": result})
        return result

    def all(self) -> list[Capability]:
        return list(self._items)

    def catalog_json(self) -> JsonDict:
        return {"schema": "schema://runtime/capability-catalog.v1", "capabilities": [c.to_dict() for c in self._items]}

    def catalog_markdown(self) -> str:
        lines = ["# URI Runtime Capability Catalog", "", "Argument wymagany oznaczony jest gwiazdką (`*`).", ""]
        for cap in self._items:
            lines.append(cap.to_llm_card())
        return "\n".join(lines) + "\n"

    def catalog_prompt(self) -> str:
        return (
            "Jesteś orkiestratorem runtime URI. Wybieraj funkcje po URI, nie po nazwach Pythona. "
            "Najpierw preferuj query/DOM/accessibility, potem command natywny, a koordynaty/mysz tylko jako fallback.\n\n"
            + self.catalog_markdown()
        )

    def tools_json(self) -> list[JsonDict]:
        """Return OpenAI-compatible tool descriptions: one generic call plus catalog context.

        A single generic tool is deliberate: the URI itself is the stable function name,
        while the catalog gives the model the deep semantic map of available operations.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "uri_runtime_call",
                    "description": "Execute one URI-addressed runtime capability. Choose URI from the catalog.",
                    "parameters": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["uri", "payload"],
                        "properties": {
                            "uri": {"type": "string", "description": "Capability URI, e.g. input://local/keyboard/command/type"},
                            "payload": {"type": "object", "description": "JSON payload matching selected URI input_schema"},
                        },
                    },
                },
            }
        ]


def schema_from_signature(fn: Callable[..., Any]) -> JsonDict:
    """Infer a minimal JSON schema from a Python handler signature.

    Handler parameters named ctx/captures are ignored. This makes it possible to
    wrap existing functions during refactoring and expose them by URI before the
    implementation is fully cleaned up.
    """
    props: JsonDict = {}
    required: list[str] = []
    sig = inspect.signature(fn)
    for name, param in sig.parameters.items():
        if name in {"ctx", "context", "captures"}:
            continue
        if param.kind in {inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD}:
            continue
        typ = "string"
        ann = param.annotation
        if ann in {int, "int"}:
            typ = "integer"
        elif ann in {float, "float"}:
            typ = "number"
        elif ann in {bool, "bool"}:
            typ = "boolean"
        elif ann in {dict, "dict"}:
            typ = "object"
        elif ann in {list, "list"}:
            typ = "array"
        props[name] = {"type": typ}
        if param.default is inspect._empty:
            required.append(name)
    return {"type": "object", "additionalProperties": True, "required": required, "properties": props}


def pretty_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)
