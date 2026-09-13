# Quickstart

From zero to first detection in under a minute — no GPU, no weights, no network.

## 1. Install

```bash
git clone https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent.git
cd Hokage_Vision_Agent
pip install -e .[dev]
```

## 2. Run the one-command demo

```bash
python examples/quickstart.py
```

This walks the full pipeline with the deterministic mock backend and writes every
artifact under `runs/quickstart/`:

1. Detect one image (with rendered overlay and JSON output)
2. Detect a folder
3. Validate the example YOLO dataset
4. Run a smoke training plan (safe dry-run by default)
5. Ask the rule-based agent to detect a folder
6. Generate a markdown report

Expected output ends with:

```text
=== 5. Ask the rule-based agent ===============================
tool: detect_folder | status: success | count: 1
...
=== Done ======================================================
All artifacts are under: runs\quickstart
```

## 3. Try the CLI

```bash
hokage-vision --help
hokage-vision detect image examples/images/sample.jpg --backend mock
hokage-vision agent run "检测 examples/images 里的图片"
```

The mock backend returns deterministic detections for `obito`, `naruto`, and
`gaara`, so every surface (CLI, API, GUI, agent) works before real model
weights exist.

## 4. Real inference (optional)

Real weights stay external. After placing a reviewed weight file under
`models/` (a YOLO `.pt` or exported `.onnx`), run it explicitly:

```bash
hokage-vision detect image examples/images/sample.jpg --backend ultralytics --model-path models/your-model.onnx --device cpu
```

ONNX Runtime is used automatically for `.onnx` models; both real-inference
paths need the training extra (`pip install -e .[train]`), which is also
required for `.pt` weights.

## 5. Next steps

- [Usage](usage.md) — full CLI, API, GUI, and agent reference
- [Data And Models](data-and-models.md) — dataset governance and license guardrails
- [Architecture](architecture.md) — backend factory and service layer design
