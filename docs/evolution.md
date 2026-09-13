# Project evolution: from vendored YOLO repo to agentic workbench

This page tells the engineering story behind the repo — useful if you are
evaluating the project as a **portfolio piece** and want to know what was
actually rebuilt, measured, and deleted along the way.

All numbers below come from the git history itself (75 commits,
2024-05 → 2026-09), so they can be re-verified with `git log`.

## Phase 0 — the inherited starting point (2024)

The repo began life as a fork of a *yolov5-PySide6* hobby project:

- a full vendored copy of the Ultralytics YOLOv5 toolchain under
  `legacy/old_project/` (177 tracked files, 13.8 MB) carrying GPL-3.0
  obligations and 6 upstream TODOs,
- no tests, no CI, no packaging, and a README with placeholder text.

## Phase 1 — governance first (2026 early commits)

Before writing features, the project paid down license and hygiene debt:

- vendored-code provenance audited and documented
  ([license audit](license-audit.md)),
- Apache-2.0 chosen for new code, GPL/AGPL boundaries documented in
  `THIRD_PARTY_NOTICES.md`,
- hard CI gates, dependabot, docker health checks, bilingual READMEs.

**Why first?** A detection demo is worthless as a portfolio piece if its
legal posture is "unknown GPL blob". Cleaning the license story made
everything after it defensible.

## Phase 2 — rebuild the skeleton (the 17 feature commits)

The new `src/hokage_vision` package was built one vertical slice at a
time, each commit a working product increment:

```
config → detection models → mock backend → inference service → CLI
→ agent tool registry → data/validation → smoke training → model registry
→ ultralytics + legacy backends → PySide6 GUI → FastAPI → packaging → CI
```

Design rule enforced throughout: **the default path needs no weights, no
GPU, no network** (deterministic `MockBackend`), so every layer — CLI,
API, GUI, agent — is testable in CI from a fresh clone.

## Phase 3 — the 13.8 MB deletion (commit `ddc2e3a`)

A read-only dependency audit proved nothing in `src/` imported the
vendored `legacy/old_project` tree: the only linkage was one explicit
boundary class (`YOLOv5LegacyBackend`) loading it through `torch.hub`
behind an opt-in backend name. The deletion removed **177 files /
24,111 lines** in one commit, with docs rewritten to point at git
history for provenance.

Deleting a vendored fork — with a documented audit trail instead of a
silent purge — is the kind of decision portfolio reviewers rarely see,
and it is fully reproducible: `git show ddc2e3a --stat`.

## Phase 4 — closing the "does it actually work" gap

Early 2026 reviews rated the repo *great skeleton, thin proof*. The
response was evidence, not arguments:

| Gap | Fix | Commit |
|---|---|---|
| 39 tests for 2548 LOC | 160+ tests, 93% coverage, 85% CI gate | `dd41ed2`, `60ba0b8` |
| Zero real inference | bundled ONNX model + real mAP (0.995) | `f76769b`, `719da43` |
| No training loop proof | in-repo synthetic-data closed loop | `f76769b` |
| Agent was 4-line placeholder | OpenAI + LangGraph function-calling providers | `74d51f5` |
| Evaluation returned `None` | real ultralytics `val` integration + FPS benchmark | `a1721ad` |

## Phase 5 — shipping (v0.1.1 → v0.1.2)

Release engineering completed the story: GHCR image push, three-OS
desktop packages, changelog-driven release notes, and two tagged
releases with every CI workflow green.

## What this history demonstrates

1. **Audit before delete.** 24k lines removed on the strength of a
   documented dependency audit, not vibes.
2. **Mock-first is a testability strategy**, not laziness — the same
   interfaces run mock in CI and real ONNX locally.
3. **Every feature landed with its test**; coverage went from ~40% to
   93% with the gate raised *behind* the actual level.
4. **Boring, verifiable claims** — every metric in this page maps to a
   commit you can `git show`.
