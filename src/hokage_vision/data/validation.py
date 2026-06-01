from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from hokage_vision.data.yolo_dataset import class_names, load_yolo_dataset_yaml

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


@dataclass
class DatasetValidationReport:
    dataset_yaml: str
    valid: bool
    image_count: int = 0
    box_count: int = 0
    empty_label_count: int = 0
    class_distribution: dict[int, int] = field(default_factory=dict)
    missing_labels: list[str] = field(default_factory=list)
    invalid_labels: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    manifest_exists: bool | None = None
    redistribution_allowed_recorded: bool | None = None


def validate_yolo_dataset(dataset_yaml: Path) -> DatasetValidationReport:
    dataset_yaml = Path(dataset_yaml)
    report = DatasetValidationReport(dataset_yaml=str(dataset_yaml), valid=True)
    if not dataset_yaml.exists():
        report.valid = False
        report.issues.append(f"dataset yaml does not exist: {dataset_yaml}")
        return report

    data = load_yolo_dataset_yaml(dataset_yaml)
    names = class_names(data)
    root = _dataset_root(dataset_yaml, data)
    manifest = data.get("manifest")
    if manifest:
        manifest_path = (
            (dataset_yaml.parent / manifest).resolve()
            if not Path(manifest).is_absolute()
            else Path(manifest)
        )
        report.manifest_exists = manifest_path.exists()
        if not manifest_path.exists():
            report.issues.append(f"manifest does not exist: {manifest}")
    else:
        report.manifest_exists = False
        report.issues.append("manifest is not recorded")
    report.redistribution_allowed_recorded = False

    for split in ("train", "val", "test"):
        split_value = data.get(split)
        if not split_value:
            if split != "test":
                report.issues.append(f"{split} path is not configured")
            continue
        image_dir = _resolve_path(root, split_value)
        if not image_dir.exists():
            report.issues.append(f"{split} path does not exist: {image_dir}")
            continue
        _validate_image_dir(image_dir, names, report)

    report.valid = not report.issues and not report.invalid_labels and not report.missing_labels
    return report


def _dataset_root(dataset_yaml: Path, data: dict[str, Any]) -> Path:
    root = Path(data.get("path", dataset_yaml.parent))
    if not root.is_absolute():
        root = (dataset_yaml.parent / root).resolve()
    return root


def _resolve_path(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _validate_image_dir(image_dir: Path, names: list[str], report: DatasetValidationReport) -> None:
    for image_path in sorted(
        path for path in image_dir.rglob("*") if path.suffix.lower() in IMAGE_EXTENSIONS
    ):
        report.image_count += 1
        label_path = _label_path_for_image(image_path)
        if not label_path.exists():
            report.missing_labels.append(str(label_path))
            continue
        rows = [
            line.strip()
            for line in label_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        if not rows:
            report.empty_label_count += 1
        for line_number, row in enumerate(rows, start=1):
            parts = row.split()
            if len(parts) != 5:
                report.invalid_labels.append(f"{label_path}:{line_number}: expected 5 columns")
                continue
            try:
                values = [float(part) for part in parts]
            except ValueError:
                report.invalid_labels.append(f"{label_path}:{line_number}: non-numeric value")
                continue
            class_id = int(values[0])
            if class_id < 0 or class_id >= len(names):
                report.invalid_labels.append(f"{label_path}:{line_number}: class id out of range")
            if any(value < 0 or value > 1 for value in values[1:]):
                report.invalid_labels.append(
                    f"{label_path}:{line_number}: bbox values must be between 0 and 1"
                )
            report.class_distribution[class_id] = report.class_distribution.get(class_id, 0) + 1
            report.box_count += 1


def _label_path_for_image(image_path: Path) -> Path:
    parts = list(image_path.parts)
    if "images" in parts:
        parts[parts.index("images")] = "labels"
        return Path(*parts).with_suffix(".txt")
    return image_path.with_suffix(".txt")
