# Ticket 001: Native governance for connector publication

- **ID**: ticket-001
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-11-06

## Authorization and scope

SESSION_EXECUTION_AUTHORIZATION: user requested continued artifacts and connector publication, testing and merging. Artifacts PLF-017 is the bounded prerequisite of PLF-015/PLF-009. Adopt published new-project v0.20.138 through its supported first bootstrap and allocator. The existing PR2 remains preserved. No product source edits belong to this ticket.

## Acceptance criteria

- [x] AC-01: Published managed closure, canonical relative worktree, writer fencing and governance checks pass.
- [ ] AC-02: Existing application tests and platform contracts remain passing.
- [ ] AC-03: Exact-head OneDev verification and independent Validator publication are read back.

## Local validation

2026-11-06: exact staged adoption passes GOV-PASS (0 errors, 0 warnings). The independently pinned Wellman runtime ran the complete existing product suite: 20 passed and 42 subtests passed. Hosted platform contracts and independent publication remain pending.
