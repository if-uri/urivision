# Author: Tom Sapletta · Part of the ifURI solution.
"""VURI / urivision — Visual URI Process Language.

Lekki, szybki model analizy i kontroli obrazu: wskaż OBRAZ + MODEL + ASPEKTY + PYTANIE
DECYZYJNE + SCHEMAT WYNIKU, a proces kompiluje się do wywołania modelu vision i zwraca
DecisionCard (decyzja z dowodami), nie opis. Warstwa wykonawcza: LiteLLM + Gemini.

    from urivision import run_file
    result = run_file("examples/screen-review.vuri")     # dry_run=False → uderza w model
"""
from __future__ import annotations

from pathlib import Path

from .dsl import Model, Process, VuriSyntaxError, parse
from .validators import VuriValidationError, validate

__all__ = ["parse", "validate", "run", "run_file", "run_source",
           "Process", "Model", "VuriSyntaxError", "VuriValidationError"]


def run_source(text: str, *, roots: dict | None = None, dry_run: bool = False) -> dict:
    from .runner_litellm import run as _run
    return _run(validate(parse(text)), roots=roots, dry_run=dry_run)


def run_file(path: str, *, roots: dict | None = None, dry_run: bool = False) -> dict:
    return run_source(Path(path).read_text(encoding="utf-8"), roots=roots, dry_run=dry_run)


# alias zgodny z __all__/API
def run(text: str, *, roots: dict | None = None, dry_run: bool = False) -> dict:
    return run_source(text, roots=roots, dry_run=dry_run)
