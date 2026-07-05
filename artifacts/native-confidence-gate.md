# Native Lab Confidence Gate

This is the acceptance checklist before claiming broad OS support.

## Current generated state

- Native target profiles: 16
- Core URI contract passed: True
- Contract failures: 0
- Profiles still requiring native evidence: 16

## Gate G0 — architecture contract

PASS when every target profile can resolve the core URI capabilities and MethodRouter has a selected route for the required intents.

## Gate G1 — native smoke

PASS when every priority OS family has at least one real self-hosted run producing: capability list, tree/screenshot evidence, one successful query, one command and one verified postcondition.

## Gate G2 — app benchmark

PASS when the benchmark suite covers browser, Electron, native toolkit, file manager/settings, terminal and one hostile/custom UI with no silent failures.

## Gate G3 — reliability

PASS when simple tasks exceed 95% success, multi-step tasks exceed 85% success, and silent failure rate is 0% on the priority matrix.

## Gate G4 — safety

PASS when command/destructive URI policies are enforced by runtime, not by prompt text, and every command has trace + postcondition or explicit unknown/fail.
