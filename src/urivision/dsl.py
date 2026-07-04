# Author: Tom Sapletta · Part of the ifURI solution.
"""Parser VURI — Visual URI Process Language.

Użytkownik nie pisze długiego promptu; wskazuje OBRAZ, MODEL, ASPEKTY, PYTANIE DECYZYJNE
i SCHEMAT WYNIKU — a to kompiluje się do procesu URI. Każda część to adres URI (reużycie
zdolności przez URI, nie import Pythona).

    proc   view://local/screenshot/query/decision-card
    use    llm://gemini/gemini-3.5-flash as vision(reasoning=low,json=strict)
    read   artifact://screenshots/home.png as image/png
    inspect image for aspect://ui/layout, aspect://ui/cta, aspect://ui/risk
    decide "Czy ekran można pokazać klientowi bez poprawek?"
    emit   artifact://reports/home.decision.json as schema://vision/decision-card.v1
    policy policy://vision/no-guessing, policy://vision/evidence-required
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Model:
    provider: str
    model: str
    options: dict = field(default_factory=dict)


@dataclass
class Process:
    proc: str = ""
    model: Model | None = None
    input_uri: str = ""
    input_mime: str = ""
    aspects: list[str] = field(default_factory=list)
    question: str = ""
    output_uri: str = ""
    output_schema: str = ""
    policies: list[str] = field(default_factory=list)


class VuriSyntaxError(ValueError):
    pass


_OPT = re.compile(r"(\w+)\s*=\s*([^,)]+)")


def _parse_options(blob: str) -> dict:
    return {k: v.strip() for k, v in _OPT.findall(blob or "")}


def parse(text: str) -> Process:
    """Parsuj źródło .vuri → AST procesu. Rzuca VuriSyntaxError na niepoprawnej instrukcji."""
    p = Process()
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()          # komentarze '#'
        if not line:
            continue
        head, _, rest = line.partition(" ")
        rest = rest.strip()
        if head == "proc":
            p.proc = rest
        elif head == "use":
            m = re.match(r"(\S+)\s+as\s+\w+(?:\(([^)]*)\))?", rest)
            if not m:
                raise VuriSyntaxError(f"bad 'use': {rest}")
            uri, opts = m.group(1), m.group(2)
            body = uri.split("://", 1)[1] if "://" in uri else uri   # gemini/gemini-3.5-flash
            provider, _, model = body.partition("/")
            p.model = Model(provider=provider, model=model, options=_parse_options(opts))
        elif head == "read":
            m = re.match(r"(\S+)\s+as\s+(\S+)", rest)
            if not m:
                raise VuriSyntaxError(f"bad 'read': {rest}")
            p.input_uri, p.input_mime = m.group(1), m.group(2)
        elif head == "inspect":
            m = re.match(r"image\s+for\s+(.+)", rest)
            if not m:
                raise VuriSyntaxError(f"bad 'inspect': {rest}")
            p.aspects = [a.strip() for a in m.group(1).split(",") if a.strip()]
        elif head == "decide":
            p.question = rest.strip().strip('"').strip("„”")
        elif head == "emit":
            m = re.match(r"(\S+)\s+as\s+(\S+)", rest)
            if not m:
                raise VuriSyntaxError(f"bad 'emit': {rest}")
            p.output_uri, p.output_schema = m.group(1), m.group(2)
        elif head == "policy":
            p.policies = [a.strip() for a in rest.split(",") if a.strip()]
        else:
            raise VuriSyntaxError(f"unknown statement: {head}")
    return p
