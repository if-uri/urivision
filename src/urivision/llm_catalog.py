# Author: Tom Sapletta · Part of the ifURI solution.
"""LLM-facing catalog compilation."""
from __future__ import annotations

from .runtime import UriRuntime, default_runtime


def compile_runtime_prompt(runtime: UriRuntime | None = None) -> str:
    runtime = runtime or default_runtime()
    return runtime.catalog("prompt")


def compile_runtime_tools(runtime: UriRuntime | None = None) -> list[dict]:
    runtime = runtime or default_runtime()
    return runtime.catalog("tools")
