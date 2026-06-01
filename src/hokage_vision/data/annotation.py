from __future__ import annotations

from pathlib import Path

import yaml

from hokage_vision.vision.backends.mock import MockBackend
from hokage_vision.vision.inference import InferenceService

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def assist_annotation(
    images: Path,
    output: Path,
    *,
    confidence_threshold: float = 0.25,
    overwrite: bool = False,
) -> dict[str, object]:
    images = Path(images)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    service = InferenceService(MockBackend())
    generated: list[str] = []
    skipped: list[str] = []

    for image_path in sorted(path for path in images.rglob("*") if path.suffix.lower() in IMAGE_EXTENSIONS):
        result = service.detect_image(image_path)
        label_path = output / f"{image_path.stem}.txt"
        if label_path.exists() and not overwrite:
            skipped.append(str(label_path))
            continue
        lines = []
        for detection in result.detections:
            if detection.confidence < confidence_threshold:
                continue
            cx, cy, width, height = _to_yolo(result.width or 1, result.height or 1, detection.box)
            class_id = ["obito", "naruto", "gaara"].index(detection.label)
            lines.append(f"{class_id} {cx:.6f} {cy:.6f} {width:.6f} {height:.6f}")
        label_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        generated.append(str(label_path))

    review_path = output / "review_required.yaml"
    review_path.write_text(
        yaml.safe_dump({"review_required": True, "labels": generated}, sort_keys=False),
        encoding="utf-8",
    )
    return {"generated": generated, "skipped": skipped, "review_required": True, "review_file": str(review_path)}


def _to_yolo(image_width: int, image_height: int, box) -> tuple[float, float, float, float]:
    width = (box.x2 - box.x1) / image_width
    height = (box.y2 - box.y1) / image_height
    cx = (box.x1 + box.x2) / 2 / image_width
    cy = (box.y1 + box.y2) / 2 / image_height
    return cx, cy, width, height
