"""Hokage Vision Agent — Hugging Face Spaces demo app.

Real object detection in the browser, zero downloads for the visitor. This
Gradio app loads the bundled 12 MB synthetic-shapes YOLOv8n ONNX model and
runs CPU inference through onnxruntime (via ultralytics), so the Space runs
on the free CPU tier.

The model detects three synthetic shape classes (obito / naruto / gaara)
with real metrics: mAP50 0.995, precision 0.994, recall 1.0. The model and
training data are both synthetic and copyright-free; see the main repo for
the full pipeline (synthetic dataset -> CPU training -> ONNX export ->
real mAP evaluation -> FPS benchmark).

Repo: https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent
License note: fine-tuned weights inherit Ultralytics AGPL-3.0.
"""

from __future__ import annotations

import json
from pathlib import Path

import gradio as gr
from ultralytics import YOLO

MODEL_PATH = Path("assets/demo/synthetic-shapes-yolov8n.onnx")
CLASS_COLORS = {"obito": "#e74c3c", "naruto": "#f39c12", "gaara": "#3498db"}

model = YOLO(str(MODEL_PATH))


def detect(image, conf_threshold: float):
    """Run real ONNX detection and return annotated image + JSON table."""
    if image is None:
        return None, "Upload an image to run detection."
    results = model.predict(image, conf=conf_threshold, imgsz=320, verbose=False)
    annotated = results[0].plot() if results else None

    rows = []
    for box in results[0].boxes:
        label = model.names[int(box.cls)]
        rows.append(
            {
                "label": label,
                "confidence": round(float(box.conf), 3),
                "box (x1,y1,x2,y2)": [round(v, 1) for v in box.xyxy[0].tolist()],
            }
        )
    summary = f"Found {len(rows)} object(s) at conf>={conf_threshold}"
    return annotated, f"{summary}\n\n{json.dumps(rows, indent=2)}"


EXAMPLES_DIR = Path("examples")
example_files = (
    sorted(EXAMPLES_DIR.glob("*.jpg")) + sorted(EXAMPLES_DIR.glob("*.png"))
    if EXAMPLES_DIR.exists()
    else []
)

custom_css = """
.gradio-container {max-width: 950px !important; margin: 0 auto !important;}
#hero {text-align: center;}
#hero h1 {
  font-size: 2.2em; margin-bottom: 0.2em;
  background: linear-gradient(90deg, #e74c3c, #f39c12, #3498db);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
#hero p {color: #666; font-size: 1.05em;}
"""

with gr.Blocks(title="Hokage Vision Agent") as demo:
    with gr.Column(elem_id="hero"):
        gr.HTML(
            "<h1>🔥 Hokage Vision Agent</h1>"
            "<p>Real YOLOv8n object detection on synthetic shapes — "
            "ONNX Runtime, CPU-only, mAP50 <b>0.995</b>. "
            "Full pipeline: <a href='https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent'>"
            "GitHub repo</a> (LLM agent, training loop, benchmarks, 93% coverage)</p>"
        )

    with gr.Row():
        with gr.Column():
            input_image = gr.Image(type="pil", label="Input image")
            conf_slider = gr.Slider(
                minimum=0.1,
                maximum=0.9,
                value=0.5,
                step=0.05,
                label="Confidence threshold",
            )
            detect_btn = gr.Button("Detect objects", variant="primary")
            if example_files:
                gr.Examples(
                    examples=[str(p) for p in example_files[:4]],
                    inputs=input_image,
                    label="Try a synthetic example",
                )
        with gr.Column():
            output_image = gr.Image(type="numpy", label="Detections")
            output_json = gr.Textbox(label="Detection details (JSON)", lines=10, max_lines=25)

    detect_btn.click(
        fn=detect,
        inputs=[input_image, conf_slider],
        outputs=[output_image, output_json],
    )

if __name__ == "__main__":
    demo.launch(css=custom_css)
