# ADR-007: Bundle a 12 MB ONNX model + synthetic dataset in-repo

**Status:** Accepted · **Date:** 2026-09-12

## Context

After the legacy deletion, a fresh clone could run only the mock
backend: real-inference and real-mAP tests skipped (or failed with
"Model file does not exist"), and every "it actually detects" claim
required the reader to train something first. For a portfolio repo,
"clone → 30 seconds → real detection" is the difference between a claim
and a demo.

## Decision

Ship two copyright-safe assets in `assets/demo/`:

1. `synthetic-shapes-yolov8n.onnx` (12 MB) — the model trained by
   `scripts/closed_loop_demo.py` on synthetic color-block data,
   exported to ONNX so inference needs **no PyTorch**, only
   `onnxruntime`.
2. `synthetic-shapes-dataset.zip` (0.4 MB) — the 144-image synthetic
   dataset with a *portable* `dataset.yaml` (no `path:` key, so
   ultralytics resolves paths relative to wherever it is unzipped).

`.gitignore` gained `!assets/demo/**` **after** the `*.onnx`/`*.pt`
rules (gitignore is last-match-wins — the negation must come last).
The demo README documents the AGPL-3.0 inheritance of the fine-tuned
weights and links the model card.

## Consequences

- ✅ Fresh clones run real detection (`--backend ultralytics`) and
  real mAP evaluation (0.995) with zero downloads.
- ✅ Integration tests can target bundled assets instead of skipping.
- ⚠️ +12.4 MB repo size — accepted trade, the repo is otherwise lean
  (~14 MB pack).
- ⚠️ Weights inherit Ultralytics AGPL-3.0; they are clearly labeled
  as demo artifacts, not Apache-2.0 project code.
- ⚠️ The synthetic dataset's absolute-path `dataset.yaml` was
  rewritten during packing; regenerating the zip must keep the
  portable form (the packing script lives in git history).
