# ADR-006: Coverage gate at 85%, raised behind the real level

**Status:** Accepted · **Date:** 2026-09-10 → 2026-09-11 (commits `f76769b`, `70ea60`, `60ba0b8`)

## Context

The suite started at 39 tests / ~40% coverage. Two failure modes were
possible: setting a high gate before the code supported it (red CI
breathing down every PR), or setting no gate (coverage silently
eroding). Additionally, subprocess-based CLI tests were invisible to
coverage, understating reality.

## Decision

Raise the gate in steps, **always below the measured level**:
`60` (when local measured ~77%) → `80` (at ~81%) → `85` (at 93%).
Alongside, convert CLI tests to in-process `CliRunner` so coverage
sees them (cli.py 0% → 88%), and run the gate only on unit +
integration tests where the environment is deterministic.

## Consequences

- ✅ The gate has never been red for reasons unrelated to a change;
  it bites only on real regressions.
- ✅ Step-raising documents intent: each bump commit contains the
  measured level in its message.
- ⚠️ GUI (separate workflow) and packaging tests are outside the
  gate — deliberate, their environments are flakier.
- ⚠️ The 85% number is a floor, not a target; modules like
  `yolov5_legacy_backend` sit at 65% by design (the legacy tree it
  would load no longer exists).
