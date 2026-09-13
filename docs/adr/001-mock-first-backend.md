# ADR-001: Mock-first vision backend

**Status:** Accepted · **Date:** 2026-06 (commit `0442123`)

## Context

Every layer of the workbench (CLI, GUI, API, agent tools) needs
detection results to demo and test. Real YOLO weights are hundreds of
MB, license-encumbered, and machine-dependent — CI and fresh clones
would either skip everything or download weights from the network.

## Decision

Make the **default backend `MockBackend`**: a deterministic stub that
returns fixed boxes (`obito 0.91 / naruto 0.84 / gaara 0.77`) for any
valid image. Real backends (Ultralytics, legacy YOLOv5) are opt-in by
explicit name + model path.

## Consequences

- ✅ CI runs the *same* CLI/API/GUI code paths as production, no
  GPU/weights/network needed; the entire agent loop is testable.
- ✅ Demo output is byte-stable, which made "evidence figures" and
  README examples reproducible.
- ⚠️ Mock boxes are visually fake — mitigated later by the closed-loop
  demo and bundled real ONNX model (ADR-007).
- ⚠️ Requires discipline: every feature must work through the
  `VisionBackend` interface, never by special-casing mock.
