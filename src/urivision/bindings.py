# Author: Tom Sapletta · Part of the ifURI solution.
"""Helpers for exposing ordinary Python functions as URI capabilities."""
from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from .capability import Capability, RuntimeContext
from .registry import CapabilityRegistry, schema_from_signature


def uri_function(
    uri_pattern: str,
    *,
    title: str | None = None,
    description: str | None = None,
    kind: str = "command",
    input_schema: dict | None = None,
    output_schema: dict | None = None,
    **meta: Any,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Attach a URI capability contract to a Python function.

    This is the migration bridge from import-based reuse to URI-process reuse.
    Existing functions can keep their implementation, but the runtime/LLM sees a
    stable URI contract.
    """

    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        cap = Capability(
            uri_pattern=uri_pattern,
            title=title or fn.__name__.replace("_", " "),
            description=description or (fn.__doc__ or "").strip() or fn.__name__,
            kind=kind,  # type: ignore[arg-type]
            input_schema=input_schema or schema_from_signature(fn),
            output_schema=output_schema or {"type": "object", "properties": {}},
            **meta,
        )
        setattr(fn, "__uri_capability__", cap)
        return fn

    return deco


def register_uri_function(registry: CapabilityRegistry, fn: Callable[..., Any]) -> Capability:
    cap: Capability | None = getattr(fn, "__uri_capability__", None)
    if cap is None:
        raise ValueError(f"Function {fn.__name__} has no __uri_capability__; decorate it with @uri_function")

    @wraps(fn)
    def handler(ctx: RuntimeContext, payload: dict, captures: dict[str, str]) -> dict:
        try:
            result = fn(**payload)
        except TypeError:
            # Allow advanced functions to accept runtime context/captures.
            result = fn(ctx=ctx, captures=captures, **payload)
        return result if isinstance(result, dict) else {"ok": True, "result": result}

    clone = Capability(**{**cap.to_dict(), "handler": handler})
    return registry.register(clone)


def register_module_uri_functions(registry: CapabilityRegistry, module: Any) -> list[Capability]:
    registered: list[Capability] = []
    for value in vars(module).values():
        if callable(value) and getattr(value, "__uri_capability__", None) is not None:
            registered.append(register_uri_function(registry, value))
    return registered
