# Author: Tom Sapletta · Part of the ifURI solution.
"""Capability contracts for URI-addressable functions.

A Capability is the unit the LLM should understand: URI pattern, purpose,
input/output contracts, examples, operational limits and a handler. The handler
can be a real OS adapter, browser adapter, KVM connector, HID bridge or a mock.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Literal

JsonDict = dict[str, Any]
CapabilityKind = Literal["query", "command", "event"]
CapabilityHandler = Callable[["RuntimeContext", JsonDict, dict[str, str]], JsonDict]


@dataclass
class RuntimeContext:
    """Execution context passed to every capability handler."""

    dry_run: bool = False
    state: JsonDict = field(default_factory=dict)
    trace: list[JsonDict] = field(default_factory=list)
    roots: dict[str, str] | None = None

    def emit(self, event: JsonDict) -> None:
        self.trace.append(event)


@dataclass
class Capability:
    uri_pattern: str
    title: str
    description: str
    kind: CapabilityKind
    input_schema: JsonDict = field(default_factory=lambda: {"type": "object", "properties": {}})
    output_schema: JsonDict = field(default_factory=lambda: {"type": "object", "properties": {}})
    handler: CapabilityHandler | None = None
    idempotent: bool = False
    side_effects: list[str] = field(default_factory=list)
    preconditions: list[str] = field(default_factory=list)
    postconditions: list[str] = field(default_factory=list)
    examples: list[JsonDict] = field(default_factory=list)
    priority: int = 100
    tags: list[str] = field(default_factory=list)
    safety: str = "normal"

    def to_dict(self, *, include_handler: bool = False) -> JsonDict:
        data = {
            "uri_pattern": self.uri_pattern,
            "title": self.title,
            "description": self.description,
            "kind": self.kind,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "idempotent": self.idempotent,
            "side_effects": self.side_effects,
            "preconditions": self.preconditions,
            "postconditions": self.postconditions,
            "examples": self.examples,
            "priority": self.priority,
            "tags": self.tags,
            "safety": self.safety,
        }
        if include_handler:
            data["handler"] = getattr(self.handler, "__name__", str(self.handler))
        return data

    def to_llm_card(self) -> str:
        required = self.input_schema.get("required", [])
        props = self.input_schema.get("properties", {})
        args = ", ".join(
            f"{name}:{spec.get('type', 'any')}{'*' if name in required else ''}"
            for name, spec in props.items()
        ) or "brak"
        effects = "; ".join(self.side_effects) if self.side_effects else "brak"
        examples = ""
        if self.examples:
            ex = self.examples[0]
            examples = f"\n    example: call {ex.get('uri', self.uri_pattern)} with {ex.get('with', {})}"
        return (
            f"- {self.uri_pattern}\n"
            f"    kind: {self.kind}; title: {self.title}\n"
            f"    when: {self.description}\n"
            f"    args: {args}\n"
            f"    side_effects: {effects}\n"
            f"    safety: {self.safety}{examples}"
        )
