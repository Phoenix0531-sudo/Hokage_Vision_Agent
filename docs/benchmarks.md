# Benchmarks

All numbers on this page are reproducible from a fresh clone using the
**bundled demo assets** (`assets/demo/`) — no downloads, no GPU.

## Real mAP evaluation (ultralytics `val`)

```bash
# unzip the bundled synthetic dataset
python -c "import zipfile; zipfile.ZipFile('assets/demo/synthetic-shapes-dataset.zip').extractall('runs/bundled-demo')"

hokage-vision model evaluate \
  --model assets/demo/synthetic-shapes-yolov8n.onnx \
  --data runs/bundled-demo/dataset/dataset.yaml --real
```

Measured on the 24-image synthetic validation split (3 classes:
`obito`, `naruto`, `gaara`):

| Metric | Value |
|---|---|
| mAP50 | **0.995** |
| mAP50-95 | **0.995** |
| Precision | **0.994** |
| Recall | **1.000** |

Class-level: every class ≥ 0.99 (the dataset is synthetic color blocks —
the point is the *pipeline* being exercised end to end, not SOTA).

## CPU inference latency (ONNX Runtime)

```bash
hokage-vision model benchmark \
  --model assets/demo/synthetic-shapes-yolov8n.onnx \
  --image runs/bundled-demo/dataset/images/val/naruto_000.jpg \
  --warmup 3 --repeats 10 --image-size 320
```

| Environment | FPS | Mean latency | Median | Min / Max |
|---|---|---|---|---|
| AMD Ryzen 5 7500F, Windows, CPUExecutionProvider, imgsz 320 | **92.2** | 10.85 ms | 9.23 ms | 7.26 / 43.49 ms |

- Inference is **ONNX-only** — no PyTorch import at runtime
  (torch appears only for training/export).
- The max-latency outlier (43 ms) is OS scheduling noise, not the
  model; the median is the honest single-shot number.
- Earlier `yolo11n` measurement on the same machine at imgsz 640:
  33.6 FPS / 29.8 ms mean — the 320px synthetic model is ~2.7× faster.

## Reproducibility notes

- `benchmark_fps` (implemented in `src/hokage_vision/vision/benchmark.py`)
  warms up per image first, then times `repeats` full passes over all
  images and reports flattened per-image statistics.
- Ultralytics writes val artifacts to `runs/detect/val*` (gitignored).
- FPS varies with machine; the JSON output of `model benchmark` carries
  the full latency distribution so results can be compared, not just
  averaged.

## Test coverage of these paths

| Path | Tests |
|---|---|
| Real evaluation (missing model / missing yaml / ImportError branches) | `tests/unit/test_evaluation.py` |
| Benchmark statistics and empty-input guard | `tests/unit/test_benchmark.py` |
| Real mAP + FPS on bundled assets (skip if assets absent) | `tests/integration/test_real_evaluation.py` |
