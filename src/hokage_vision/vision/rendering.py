from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from hokage_vision.core.types import DetectionResult


def render_detections(
    image_path: Path,
    result: DetectionResult,
    output_path: Path | None = None,
) -> Image.Image:
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for detection in result.detections:
        box = detection.box
        xy = [box.x1, box.y1, box.x2, box.y2]
        label = f"{detection.label} {detection.confidence:.2f}"
        draw.rectangle(xy, outline=(255, 80, 80), width=3)
        text_box = draw.textbbox((box.x1, box.y1), label, font=font)
        draw.rectangle(text_box, fill=(255, 80, 80))
        draw.text((box.x1, box.y1), label, fill=(255, 255, 255), font=font)

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path)

    return image
