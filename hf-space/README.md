---
title: Hokage Vision Agent
emoji: 🔥
colorFrom: red
colorTo: indigo
sdk: gradio
sdk_version: "6.27.0"
app_file: app.py
pinned: false
license: apache-2.0
---

# Hokage Vision Agent — online demo

Real object detection in your browser. This Space loads the project's bundled
12 MB synthetic-shapes YOLOv8n ONNX model and runs CPU inference via ONNX
Runtime — no GPU, no downloads for the visitor.

**What you're looking at:** a fully local, copyright-free training pipeline
(synthetic dataset → CPU fine-tune → ONNX export → real mAP evaluation → FPS
benchmark) shipped as a working demo. The model detects three synthetic shape
classes (obito / naruto / gaara):

- mAP50 **0.995**, precision 0.994, recall 1.0 on the bundled val split
- ~90 FPS on a single CPU core (320px inputs)

**Main repo:** https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent

The full project adds: LLM agent layer with function calling (OpenAI /
LangGraph providers, offline-testable), FastAPI service, PySide6 GUI,
training pipeline, model registry, evaluation + benchmarking, 93% test
coverage, and a three-OS desktop release pipeline.

## Local run

```bash
pip install -r requirements.txt
python app.py
```

The Space expects `assets/demo/synthetic-shapes-yolov8n.onnx` and an
`examples/` folder of sample images next to `app.py`.

## License notes

- Space code: Apache-2.0 (same as the main repo)
- Fine-tuned ONNX weights inherit Ultralytics AGPL-3.0 (base YOLOv8n)
