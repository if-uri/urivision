# Author: Tom Sapletta · Part of the ifURI solution.
"""Walidacja procesu VURI — blokuj złe procesy ZANIM trafią do modelu (tanio, deterministycznie)."""
from __future__ import annotations

from .dsl import Process

REQUIRED = ("proc", "model", "input_uri", "question", "output_uri", "output_schema")
ALLOWED_SCHEMES = {"view", "llm", "artifact", "aspect", "schema", "policy", "event", "ui", "input", "browser", "vision", "kvm", "hid", "guard", "runtime", "plan", "capability"}


class VuriValidationError(ValueError):
    pass


def _scheme(uri: str) -> str:
    return uri.split("://", 1)[0] if "://" in uri else ""


def validate(p: Process) -> Process:
    missing = [k for k in REQUIRED if not getattr(p, k, None)]
    if "model" in missing or p.model is None:
        missing = [m for m in missing if m != "model"] + ["use(model)"]
    if missing:
        raise VuriValidationError(f"Missing required statements: {', '.join(missing)}")

    # wszystkie adresy muszą używać znanych schematów URI
    for uri in [p.proc, p.input_uri, p.output_uri, p.output_schema, *p.aspects, *p.policies]:
        sch = _scheme(uri)
        if sch and sch not in ALLOWED_SCHEMES:
            raise VuriValidationError(f"Unsupported URI scheme '{sch}' in {uri}")

    if not p.input_mime.startswith("image/"):
        raise VuriValidationError("Only image/* inputs supported")
    if not p.output_schema.startswith("schema://"):
        raise VuriValidationError("emit must target a schema:// contract")
    if not p.aspects:
        raise VuriValidationError("inspect must list at least one aspect://")
    return p
