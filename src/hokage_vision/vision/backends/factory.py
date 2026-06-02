from __future__ import annotations

from pathlib import Path

from hokage_vision.core.errors import VisionBackendError
from hokage_vision.vision.backends.base import VisionBackend
from hokage_vision.vision.backends.mock import MockBackend
from hokage_vision.vision.backends.ultralytics_backend import UltralyticsBackend
from hokage_vision.vision.backends.yolov5_legacy_backend import YOLOv5LegacyBackend


def create_backend(
    backend: str,
    *,
    model_path: Path | None = None,
    conf_threshold: float = 0.25,
    iou_threshold: float = 0.45,
    device: str = "auto",
    image_size: int = 640,
) -> VisionBackend:
    """Create a project-scoped vision backend from user-facing options."""
    backend_key = backend.strip().lower().replace("-", "_")
    if backend_key == "mock":
        return MockBackend()
    if backend_key in {"ultralytics", "yolo", "yolov8", "yolo11"}:
        return UltralyticsBackend(
            model_path,
            conf_threshold=conf_threshold,
            iou_threshold=iou_threshold,
            device=device,
            image_size=image_size,
        )
    if backend_key in {"yolov5_legacy", "legacy", "yolov5"}:
        return YOLOv5LegacyBackend(model_path)

    supported = "mock, ultralytics, yolov5_legacy"
    raise VisionBackendError(f"Unsupported backend '{backend}'. Supported backends: {supported}.")
