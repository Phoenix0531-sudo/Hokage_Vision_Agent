# ADR-002: Backend factory with explicit selection

**Status:** Accepted · **Date:** 2026-06 (commit `b2ac3cc`)

## Context

Three backends with different constructors (mock takes nothing;
Ultralytics takes model path + thresholds; legacy YOLOv5 takes a source
root). Call sites in CLI, API, GUI, and the agent would otherwise each
grow their own `if backend == ...` ladder.

## Decision

One `create_backend(name, **options)` factory in
`vision/backends/factory.py` is the *only* way to construct a backend.
Unknown names and missing model files raise `VisionBackendError` with
actionable messages. The selector accepts a few aliases
(`yolov5_legacy`, `legacy`, `yolov5`) but every real path goes through
the factory.

## Consequences

- ✅ Single place to validate backend names, paths, and thresholds —
  the API layer maps the same errors to HTTP 400 uniformly.
- ✅ Adding a backend (e.g. an RT-DETR adapter) touches one module
  plus one test file.
- ⚠️ Aliases are a small compatibility tax; they exist so early
  configs keep working and are documented in the factory docstring.
