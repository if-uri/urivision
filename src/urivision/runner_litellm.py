# Author: Tom Sapletta · Part of the ifURI solution.
"""Warstwa wykonawcza VURI na LiteLLM — multimodalne wejście text+image, structured output.
Import litellm jest leniwy: parser/walidacja/kompilacja działają bez zależności (i w testach)."""
from __future__ import annotations

import base64
import json
from pathlib import Path

from .compiler import compile_prompt
from .dsl import Process
from .resolver import artifact_path, model_id
from .schemas import resolve_schema


def _image_data_url(path: str, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode("ascii")


def run(p: Process, *, roots: dict | None = None, dry_run: bool = False) -> dict:
    """Wykonaj proces VURI: obraz+prompt → model → DecisionCard (zwalidowany schematem).
    dry_run zwraca wkompilowane wywołanie bez uderzania w model (do testów/podglądu)."""
    model = model_id(p.model)
    schema = resolve_schema(p.output_schema)
    prompt = compile_prompt(p)
    img = artifact_path(p.input_uri, roots)
    reasoning = (p.model.options or {}).get("reasoning", "low")

    call = {"model": model, "prompt": prompt, "image": img, "mime": p.input_mime,
            "schema": p.output_schema, "reasoning": reasoning}
    if dry_run:
        return {"ok": True, "dryRun": True, "call": call}

    from litellm import completion, supports_vision  # leniwy import
    if not supports_vision(model=model):
        raise RuntimeError(f"Model does not support vision: {model}")

    resp = completion(
        model=model,
        messages=[{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url",
             "image_url": {"url": _image_data_url(img, p.input_mime), "format": p.input_mime}},
        ]}],
        response_format={"type": "json_schema", "json_schema": {
            "name": "decision_card_v1", "schema": schema, "strict": True}},
        reasoning_effort=reasoning,
        num_retries=2,
    )
    card = json.loads(resp.choices[0].message.content)
    out = artifact_path(p.output_uri, roots)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(card, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "decision": card.get("decision"), "output": out, "card": card}
