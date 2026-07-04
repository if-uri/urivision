# Author: Tom Sapletta · Part of the ifURI solution.
"""Resolver URI → konkrety wykonawcze. llm://gemini/x → 'gemini/x' (prefiks LiteLLM);
artifact:// → ścieżka pliku; aspect:///policy:// → czytelne etykiety do promptu."""
from __future__ import annotations

import os

from .dsl import Model


def model_id(model: Model) -> str:
    """llm://gemini/gemini-3.5-flash → 'gemini/gemini-3.5-flash' (forma LiteLLM)."""
    return f"{model.provider}/{model.model}"


def artifact_path(uri: str, roots: dict | None = None) -> str:
    """artifact://screenshots/home.png → ścieżka. ROOTS mapuje pierwszy segment na katalog
    bazowy (domyślnie CWD); pozwala trzymać artefakty poza repo bez zakodowanych ścieżek."""
    body = uri.split("://", 1)[1] if "://" in uri else uri
    top, _, tail = body.partition("/")
    base = (roots or {}).get(top) or os.environ.get(f"URIVISION_ROOT_{top.upper()}") or os.getcwd()
    return os.path.join(base, tail) if tail else os.path.join(base, top)


def label(uri: str) -> str:
    """aspect://ui/cta → 'ui/cta'; policy://vision/no-guessing → 'vision/no-guessing'."""
    return uri.split("://", 1)[1] if "://" in uri else uri
