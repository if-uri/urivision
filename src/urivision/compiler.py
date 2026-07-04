# Author: Tom Sapletta · Part of the ifURI solution.
"""Kompilacja AST procesu → prompt dla modelu vision. Prompt wymusza DECYZJĘ z dowodami
(nie opis), po aspektach, z zasadami polityki — resztę egzekwuje structured output."""
from __future__ import annotations

from .dsl import Process
from .resolver import label

_POLICY_TEXT = {
    "vision/no-guessing": "Nie zgaduj. Jeśli czegoś nie widać jednoznacznie, ustaw decision='unknown'.",
    "vision/evidence-required": "Każde 'finding' MUSI mieć konkretny 'evidence' — co dokładnie widać.",
}


def compile_prompt(p: Process) -> str:
    aspects = "\n".join(f"  - {label(a)}" for a in p.aspects)
    policies = "\n".join(f"  - {_POLICY_TEXT.get(label(x), label(x))}" for x in p.policies)
    return (
        "Jesteś inspektorem obrazu. Nie OPISUJESZ obrazka — wydajesz DECYZJĘ z dowodami.\n"
        f"PYTANIE DECYZYJNE: {p.question}\n\n"
        "Oceń obraz WYŁĄCZNIE pod kątem tych aspektów:\n"
        f"{aspects}\n\n"
        + (f"ZASADY:\n{policies}\n\n" if policies else "")
        + "Zwróć JSON zgodny ze schematem decision-card: decision (ok|fix|block|unknown), "
        "confidence 0..1, summary, findings[] (aspect, severity, region.anchor, evidence, "
        "impact, recommendation), next_actions[]. Region podawaj jako KOTWICĘ opisową "
        "(np. 'prawa część sekcji hero'), nie jako piksele."
    )
