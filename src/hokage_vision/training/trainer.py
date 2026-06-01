from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from hokage_vision.core.errors import HokageVisionError
from hokage_vision.data.validation import validate_yolo_dataset
from hokage_vision.training.jobs import TrainingJob


def plan_yolo_training(
    data: Path,
    *,
    base_model: Path | None = None,
    epochs: int = 1,
    batch: int = 1,
    image_size: int = 640,
    device: str = "cpu",
    output_dir: Path = Path("runs/train"),
) -> dict[str, object]:
    report = validate_yolo_dataset(data)
    job = TrainingJob(
        name="hokage-yolo-training-plan",
        status="planned",
        dry_run=True,
        output_dir=output_dir,
        parameters={
            "data": str(data),
            "base_model": str(base_model) if base_model else None,
            "epochs": epochs,
            "batch": batch,
            "image_size": image_size,
            "device": device,
        },
        message="Dry-run training plan generated. Real training requires explicit execution.",
    )
    payload = asdict(job)
    payload["dataset_valid"] = report.valid
    payload["dataset_issues"] = report.issues + report.missing_labels + report.invalid_labels
    return payload


def run_yolo_training(
    data: Path,
    *,
    base_model: Path | None = None,
    epochs: int = 1,
    batch: int = 1,
    image_size: int = 640,
    device: str = "cpu",
    output_dir: Path = Path("runs/train"),
    dry_run: bool = True,
) -> dict[str, object]:
    if dry_run:
        return plan_yolo_training(
            data,
            base_model=base_model,
            epochs=epochs,
            batch=batch,
            image_size=image_size,
            device=device,
            output_dir=output_dir,
        )

    report = validate_yolo_dataset(data)
    if not report.valid:
        msg = "Dataset validation failed; real training will not start."
        raise HokageVisionError(msg)

    try:
        from ultralytics import YOLO  # type: ignore[import-not-found]
    except ImportError as exc:
        msg = "Real YOLO training requires the train extra: pip install -e '.[train]'"
        raise HokageVisionError(msg) from exc

    if output_dir.exists():
        msg = f"Output directory already exists; refusing to overwrite: {output_dir}"
        raise HokageVisionError(msg)

    model = YOLO(str(base_model) if base_model else "yolov8n.pt")
    result = model.train(
        data=str(data),
        epochs=epochs,
        batch=batch,
        imgsz=image_size,
        device=device,
        project=str(output_dir.parent),
        name=output_dir.name,
        exist_ok=False,
    )
    return {"status": "completed", "dry_run": False, "result": str(result), "output_dir": str(output_dir)}
