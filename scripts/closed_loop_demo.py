"""End-to-end closed-loop demo: generate data -> train -> export ONNX -> real inference.

Run from the repository root (requires the train extra: pip install -e ".[train]")):

    python scripts/closed_loop_demo.py

The script proves the full workbench loop with zero external assets:

1. Generate an expanded synthetic YOLO dataset (random colored rectangles, three classes).
2. Fine-tune yolov8n on CPU for a few epochs (``runs/closed-loop/dataset`` is fully
   synthetic and Apache-2.0 redistributable).
3. Validate with a real mAP evaluation and measure CPU FPS.
4. Export the trained weights to ONNX and run them through UltralyticsBackend.
5. Render detections onto the validation image and save a README-ready figure.

Everything is written under ``runs/closed-loop/`` (git-ignored). The rendered
detection figure is committed manually via ``--figure-out`` when updating the README.
"""

from __future__ import annotations

import argparse
import random
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CLASSES = ["obito", "naruto", "gaara"]
COLORS = {"obito": (92, 72, 180), "naruto": (235, 112, 28), "gaara": (184, 52, 48)}

WORK = ROOT / "runs" / "closed-loop"


def generate_split(images_dir: Path, labels_dir: Path, count: int, seed: int) -> None:
    """Synthesize `count` images per class with randomly placed boxes."""
    from PIL import Image, ImageDraw

    rng = random.Random(seed)
    for class_id, label in enumerate(CLASSES):
        for index in range(count):
            image = Image.new("RGB", (320, 240), (19, 22, 31))
            draw = ImageDraw.Draw(image)
            # background noise blocks so the task is not trivially uniform
            for _ in range(rng.randint(2, 5)):
                nx, ny = rng.randint(0, 300), rng.randint(0, 220)
                draw.rectangle((nx, ny, nx + 15, ny + 15), fill=(35, 40, 55))
            box_w, box_h = rng.randint(110, 170), rng.randint(90, 140)
            x1 = rng.randint(5, 320 - box_w - 5)
            y1 = rng.randint(5, 240 - box_h - 5)
            draw.rectangle(
                (x1, y1, x1 + box_w, y1 + box_h),
                fill=COLORS[label],
                outline=(255, 196, 87),
                width=3,
            )
            image.save(images_dir / f"{label}_{index:03d}.jpg", quality=90)
            (labels_dir / f"{label}_{index:03d}.txt").write_text(
                f"{class_id} {(x1 + box_w / 2) / 320:.4f} {(y1 + box_h / 2) / 240:.4f} "
                f"{box_w / 320:.4f} {box_h / 240:.4f}\n",
                encoding="utf-8",
            )


def build_dataset(base: Path, train_count: int, val_count: int) -> Path:
    for split, count, seed in (("train", train_count, 7), ("val", val_count, 11)):
        images_dir = base / "images" / split
        labels_dir = base / "labels" / split
        images_dir.mkdir(parents=True, exist_ok=True)
        labels_dir.mkdir(parents=True, exist_ok=True)
        generate_split(images_dir, labels_dir, count, seed)
    (base / "dataset.yaml").write_text(
        f"path: {base.as_posix()}\n"
        "train: images/train\n"
        "val: images/val\n"
        f"names:\n  0: {CLASSES[0]}\n  1: {CLASSES[1]}\n  2: {CLASSES[2]}\n",
        encoding="utf-8",
    )
    return base / "dataset.yaml"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=40)
    parser.add_argument("--train-count", type=int, default=40, help="images per class")
    parser.add_argument("--val-count", type=int, default=8, help="images per class")
    parser.add_argument(
        "--figure-out",
        type=Path,
        default=None,
        help="Also copy the rendered detection figure to this path (e.g. docs/screenshots).",
    )
    args = parser.parse_args()

    if WORK.exists():
        shutil.rmtree(WORK)
    dataset_yaml = build_dataset(WORK / "dataset", args.train_count, args.val_count)
    print(f"[1/6] synthetic dataset ready: {dataset_yaml}")

    from ultralytics import YOLO

    model = YOLO("models/yolov8n.pt")
    model.train(
        data=str(dataset_yaml),
        epochs=args.epochs,
        imgsz=320,
        batch=16,
        device="cpu",
        project=str(WORK / "train"),
        name="run",
        exist_ok=True,
        verbose=False,
    )
    best_pt = WORK / "train" / "run" / "weights" / "best.pt"
    print(f"[2/6] training done: {best_pt}")

    from hokage_vision.vision.backends.ultralytics_backend import UltralyticsBackend
    from hokage_vision.vision.benchmark import benchmark_fps
    from hokage_vision.vision.evaluation import evaluate_model

    eval_payload = evaluate_model(best_pt, dataset_yaml, mock=False)
    metrics = eval_payload["metrics"]
    print(
        "[3/6] real mAP evaluation: "
        f"mAP50={metrics['map50']:.3f} mAP50-95={metrics['map50_95']:.3f} "
        f"P={metrics['precision']:.3f} R={metrics['recall']:.3f}"
    )

    val_images = sorted((WORK / "dataset" / "images" / "val").glob("*.jpg"))[:5]
    pt_backend = UltralyticsBackend(best_pt, conf_threshold=0.5, image_size=320)
    fps_report = benchmark_fps(pt_backend, val_images, warmup=2, repeats=3)
    print(
        f"[4/6] CPU FPS benchmark: {fps_report['fps']:.1f} fps "
        f"(mean latency {fps_report['latency_ms_mean']:.1f} ms, "
        f"{len(val_images)} val images)"
    )

    onnx_path = Path(model.export(format="onnx", imgsz=320))
    print(f"[5/6] exported: {onnx_path}")

    from hokage_vision.vision.rendering import render_detections

    probe = WORK / "dataset" / "images" / "val" / "naruto_000.jpg"
    backend = UltralyticsBackend(onnx_path, conf_threshold=0.5, image_size=320)
    backend.load()
    result = backend.predict_image(probe)
    print(f"[6/6] real inference on {probe.name}:")
    for detection in result.detections:
        print(
            f"  {detection.label:<7} conf={detection.confidence:.2f} "
            f"box=({detection.box.x1:.0f},{detection.box.y1:.0f},"
            f"{detection.box.x2:.0f},{detection.box.y2:.0f})"
        )

    figure = WORK / "closed-loop-detection.jpg"
    render_detections(probe, result, output_path=figure)
    if args.figure_out:
        args.figure_out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(figure, args.figure_out)
        print(f"figure copied to: {args.figure_out}")
    print("closed loop complete.")


if __name__ == "__main__":
    main()
