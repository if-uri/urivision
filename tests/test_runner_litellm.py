# Author: Tom Sapletta · Part of the ifURI solution.
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from urivision import parse, validate
from urivision.runner_litellm import run

VURI_SNIPPET = (
    "proc   view://local/screenshot/query/decision-card\n"
    "use    llm://openai/custom-vision as vision(reasoning=low,json=strict)\n"
    "read   artifact://screenshots/sample.png as image/png\n"
    "inspect image for aspect://ui/layout\n"
    'decide "Czy ekran wyglada poprawnie?"\n'
    "emit   artifact://reports/sample.decision.json as schema://vision/decision-card.v1\n"
)


def test_runner_litellm_uses_api_base_and_key(monkeypatch, tmp_path):
    img_file = tmp_path / "sample.png"
    img_file.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82")

    monkeypatch.setenv("URIVISION_ROOT_SCREENSHOTS", str(tmp_path))
    monkeypatch.setenv("URIVISION_ROOT_REPORTS", str(tmp_path))
    monkeypatch.setenv("URIVISION_LLM_API_BASE", "http://127.0.0.1:11437/v1")
    monkeypatch.setenv("URIVISION_LLM_API_KEY", "test-token-123")

    mock_resp = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps({
            "decision": "ok",
            "confidence": 0.95,
            "summary": "Layout is fully compliant",
            "findings": []
        })))]
    )

    mock_completion = MagicMock(return_value=mock_resp)
    monkeypatch.setattr("litellm.completion", mock_completion)

    proc = validate(parse(VURI_SNIPPET))
    res = run(proc)

    assert res["ok"] is True
    assert res["decision"] == "ok"
    assert mock_completion.called

    kwargs = mock_completion.call_args.kwargs
    assert kwargs["api_base"] == "http://127.0.0.1:11437/v1"
    assert kwargs["api_key"] == "test-token-123"
    assert kwargs["model"] == "openai/custom-vision"


def test_runner_litellm_strips_markdown_code_fences(monkeypatch, tmp_path):
    img_file = tmp_path / "sample.png"
    img_file.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\x01")

    monkeypatch.setenv("URIVISION_ROOT_SCREENSHOTS", str(tmp_path))
    monkeypatch.setenv("URIVISION_ROOT_REPORTS", str(tmp_path))
    monkeypatch.setenv("URIVISION_LLM_API_BASE", "http://127.0.0.1:11437/v1")

    fenced_json = """```json
{
  "decision": "fix",
  "confidence": 0.8,
  "summary": "Needs minor contrast adjustment",
  "findings": []
}
```"""
    mock_resp = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=fenced_json))]
    )

    monkeypatch.setattr("litellm.completion", MagicMock(return_value=mock_resp))

    proc = validate(parse(VURI_SNIPPET))
    res = run(proc)

    assert res["ok"] is True
    assert res["decision"] == "fix"
    assert res["card"]["summary"] == "Needs minor contrast adjustment"


def test_runner_litellm_oqllm_docker_mock(monkeypatch, tmp_path):
    """Verify connectivity path with custom OQLLM endpoint."""
    img_file = tmp_path / "sample.png"
    img_file.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\x01")

    monkeypatch.setenv("URIVISION_ROOT_SCREENSHOTS", str(tmp_path))
    monkeypatch.setenv("URIVISION_ROOT_REPORTS", str(tmp_path))
    monkeypatch.setenv("URIVISION_LLM_API_BASE", "http://127.0.0.1:11437/v1")
    monkeypatch.setenv("URIVISION_LLM_API_KEY", "oqllm-test-key")

    mock_resp = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps({
            "decision": "ok",
            "confidence": 0.99,
            "summary": "Verified via OQLLM fast path",
            "findings": []
        })))]
    )
    mock_completion = MagicMock(return_value=mock_resp)
    monkeypatch.setattr("litellm.completion", mock_completion)

    vuri = (
        "proc   view://local/screenshot/query/decision-card\n"
        "use    llm://openai/oqlos/system-one-router as vision(reasoning=low,json=strict)\n"
        "read   artifact://screenshots/sample.png as image/png\n"
        "inspect image for aspect://ui/layout\n"
        'decide "Czy ekran wyglada poprawnie?"\n'
        "emit   artifact://reports/sample.decision.json as schema://vision/decision-card.v1\n"
    )

    proc = validate(parse(vuri))
    res = run(proc)
    assert res["ok"] is True
    assert "card" in res
    assert res["decision"] == "ok"
    assert mock_completion.called
    assert mock_completion.call_args.kwargs["api_base"] == "http://127.0.0.1:11437/v1"
