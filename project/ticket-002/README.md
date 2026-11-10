# Ticket 002: support transport override via URIVISION_LLM_API_BASE and OQLLM

- **ID**: ticket-002
- **Owner**: agent:antigravity
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

Support transport override for LiteLLM via URIVISION_LLM_API_BASE, URIRUN_LLM_API_BASE, and OPENAI_API_BASE.
Support isolated credentials via URIVISION_LLM_API_KEY, OQLLM_API_KEY, and OPENAI_API_KEY.
Provide deterministic unit tests with zero unsafe test skips.

## Acceptance criteria

- [x] AC-01: python3 -m pytest -v tests/test_runner_litellm.py
- [x] AC-02: project/governance-check.sh

## Tracking boundary

This directory contains the minimal reviewed intent. Optional participant prose
and raw command logs are not required delivery output.
