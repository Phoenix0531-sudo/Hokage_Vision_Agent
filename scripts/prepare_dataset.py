from __future__ import annotations

from pathlib import Path

import typer
from PIL import Image, ImageDraw

app = typer.Typer(help="Prepare reviewed local datasets and smoke-test fixtures.")

CLASSES = ["obito", "naruto", "gaara"]
COLORS = {
    "obito": (92, 72, 180),
    "naruto": (235, 112, 28),
    "gaara": (184, 52, 48),
}


@app.callback()
def root() -> None:
    """Prepare project-scoped datasets."""


@app.command("smoke")
def create_smoke_dataset(
    output: Path = typer.Option(
        Path("examples/dataset"),
        "--output",
        help="Synthetic YOLO dataset output directory.",
    ),
    manifest: Path = typer.Option(
        Path("data/manifests/hokage-vision-sample.yaml"),
        "--manifest",
        help="Dataset manifest output path.",
    ),
    overwrite: bool = typer.Option(
        False,
        "--overwrite",
        help="Replace an existing smoke dataset directory.",
    ),
) -> None:
    """Create a tiny synthetic YOLO dataset for validation and dry-run training."""
    if output.exists() and not overwrite:
        msg = f"Refusing to overwrite existing dataset: {output}"
        raise typer.BadParameter(msg)

    _create_dataset(output)
    _write_manifest(manifest)
    typer.echo(f"Created synthetic smoke dataset at {output}")
    typer.echo(f"Wrote manifest at {manifest}")


def _create_dataset(output: Path) -> None:
    for split in ("train", "val", "test"):
        for class_id, label in enumerate(CLASSES):
            image_dir = output / "images" / split
            label_dir = output / "labels" / split
            image_dir.mkdir(parents=True, exist_ok=True)
            label_dir.mkdir(parents=True, exist_ok=True)

            image_path = image_dir / f"{label}_{split}.jpg"
            label_path = label_dir / f"{label}_{split}.txt"
            _write_image(image_path, label, split)
            label_path.write_text(f"{class_id} 0.5000 0.5500 0.5000 0.5667\n", encoding="utf-8")


def _write_image(path: Path, label: str, split: str) -> None:
    image = Image.new("RGB", (160, 120), (19, 22, 31))
    draw = ImageDraw.Draw(image)
    draw.rectangle((40, 28, 120, 96), fill=COLORS[label], outline=(255, 196, 87), width=3)
    draw.text((10, 8), f"{label} / {split}", fill=(245, 245, 245))
    image.save(path, quality=90)


def _write_manifest(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """dataset:
  name: hokage-vision-synthetic-smoke
  version: 0.1.0
  description: Synthetic geometric YOLO dataset for CI, dataset validation, and training dry-runs.
  redistribution_allowed: true

sources:
  - id: synthetic-smoke-001
    type: project_generated
    path: examples/dataset
    license: Apache-2.0
    redistribution_allowed: true
    notes: Synthetic shapes only. These images are not Naruto screenshots and do not represent real character data.

classes:
  - obito
  - naruto
  - gaara

annotations:
  format: yolo
  reviewed: true
  reviewer: project
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    app()
