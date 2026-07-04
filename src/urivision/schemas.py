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

SCHEMAS = {"schema://vision/decision-card.v1": DECISION_CARD_V1}


def resolve_schema(uri: str) -> dict:
    if uri not in SCHEMAS:
        raise KeyError(f"unknown result schema: {uri}")
    return SCHEMAS[uri]
