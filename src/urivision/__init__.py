# Author: Tom Sapletta · Part of the ifURI solution.
"""VURI / urivision — Visual URI Process Language + URI Runtime.

The original VURI path is kept: image + model + aspects + decision question +
result schema => DecisionCard. The added runtime path exposes reusable functions
as URI-addressable capabilities so an LLM can understand and orchestrate them
without importing Python modules directly.
"""
from __future__ import annotations

from pathlib import Path

from .bindings import register_module_uri_functions, register_uri_function, uri_function
from .capability import Capability, RuntimeContext
from .dsl import Model, Process, VuriSyntaxError, parse
from .orchestrator import PlanRunner, run_plan, run_plan_file
from .platforms import BackendProfile, DEFAULT_MATRIX, get_backend_profile, list_backend_profiles
from .native_profiles import NativeTargetProfile, get_native_target, list_native_targets, coverage_summary, detect_local_host
from .method_router import route_intent, route_matrix
from .registry import CapabilityRegistry, UriDispatchError
from .runtime import UriRuntime, default_runtime
from .validators import VuriValidationError, validate

__all__ = [
    "parse", "validate", "run", "run_file", "run_source",
    "Process", "Model", "VuriSyntaxError", "VuriValidationError",
    "Capability", "RuntimeContext", "CapabilityRegistry", "UriRuntime", "UriDispatchError",
    "default_runtime", "PlanRunner", "run_plan", "run_plan_file",
    "uri_function", "register_uri_function", "register_module_uri_functions",
    "BackendProfile", "DEFAULT_MATRIX", "get_backend_profile", "list_backend_profiles",
    "NativeTargetProfile", "get_native_target", "list_native_targets", "coverage_summary", "detect_local_host",
    "route_intent", "route_matrix",
]


def run_source(text: str, *, roots: dict | None = None, dry_run: bool = False) -> dict:
    from .runner_litellm import run as _run
    return _run(validate(parse(text)), roots=roots, dry_run=dry_run)


def run_file(path: str, *, roots: dict | None = None, dry_run: bool = False) -> dict:
    return run_source(Path(path).read_text(encoding="utf-8"), roots=roots, dry_run=dry_run)


# alias zgodny z __all__/API
def run(text: str, *, roots: dict | None = None, dry_run: bool = False) -> dict:
    return run_source(text, roots=roots, dry_run=dry_run)
