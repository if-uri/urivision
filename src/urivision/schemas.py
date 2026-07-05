# Author: Tom Sapletta · Part of the ifURI solution.
"""Kontrakty wyniku VURI. Model NIE opisuje obrazka — produkuje DECYZJĘ z dowodami."""
from __future__ import annotations

# schema://vision/decision-card.v1 — jeden stabilny kontrakt wyniku analizy obrazu.
DECISION_CARD_V1 = {
    "type": "object",
    "additionalProperties": False,
    "required": ["decision", "confidence", "summary", "findings"],
    "properties": {
        "decision": {"type": "string", "enum": ["ok", "fix", "block", "unknown"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "summary": {"type": "string"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["aspect", "severity", "evidence"],
                "properties": {
                    "aspect": {"type": "string"},                       # np. "ui/cta"
                    "severity": {"type": "string", "enum": ["info", "low", "medium", "high"]},
                    "region": {"type": "object",                          # kotwica, NIE piksele
                               "properties": {"anchor": {"type": "string"}}},
                    "evidence": {"type": "string"},                       # co widać (dowód)
                    "impact": {"type": "string"},
                    "recommendation": {"type": "string"},
                },
            },
        },
        "next_actions": {"type": "array", "items": {"type": "string"}},
    },
}


CAPABILITY_CATALOG_V1 = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schema", "capabilities"],
    "properties": {
        "schema": {"type": "string"},
        "capabilities": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["uri_pattern", "title", "description", "kind", "input_schema"],
                "properties": {
                    "uri_pattern": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "kind": {"type": "string", "enum": ["query", "command", "event"]},
                    "input_schema": {"type": "object"},
                    "output_schema": {"type": "object"},
                    "side_effects": {"type": "array", "items": {"type": "string"}},
                    "preconditions": {"type": "array", "items": {"type": "string"}},
                    "postconditions": {"type": "array", "items": {"type": "string"}},
                    "examples": {"type": "array"},
                    "safety": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
    },
}

URI_PLAN_V1 = {
    "type": "object",
    "additionalProperties": True,
    "required": ["steps"],
    "properties": {
        "schema": {"type": "string"},
        "goal": {"type": "string"},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["call"],
                "properties": {
                    "id": {"type": "string"},
                    "call": {"type": "string"},
                    "with": {"type": "object"},
                    "expect_result": {"type": "object"},
                },
            },
        },
    },
}

SCHEMAS = {
    "schema://vision/decision-card.v1": DECISION_CARD_V1,
    "schema://runtime/capability-catalog.v1": CAPABILITY_CATALOG_V1,
    "schema://runtime/uri-plan.v1": URI_PLAN_V1,
}


def resolve_schema(uri: str) -> dict:
    if uri not in SCHEMAS:
        raise KeyError(f"unknown result schema: {uri}")
    return SCHEMAS[uri]
