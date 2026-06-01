from __future__ import annotations

from pathlib import Path
from typing import Any

from hokage_vision.core.errors import VisionBackendError
from hokage_vision.core.types import BoundingBox, Detection, DetectionResult
from hokage_vision.vision.backends.base import VisionBackend


class UltralyticsBackend(VisionBackend):
    def __init__(
        self,
        model_path: Path | None,
        *,
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.45,
        device: str = "auto",
        image_size: int = 640,
    ) -> None:
        self.model_path = Path(model_path) if model_path else None
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.device = None if device == "auto" else device
        self.image_size = image_size
        self.model: Any | None = None

    def load(self) -> None:
        if self.model_path is None:
            raise VisionBackendError("Ultralytics backend requires an explicit model path.")
        if not self.model_path.exists():
            raise VisionBackendError(f"Model file does not exist: {self.model_path}")
        try:
            from ultralytics import YOLO  # type: ignore[import-not-found]
        except ImportError as exc:
            msg = "Ultralytics backend requires the train extra: pip install -e '.[train]'"
            raise VisionBackendError(msg) from exc
        self.model = YOLO(str(self.model_path))

    def predict_image(self, image_path: Path) -> DetectionResult:
        self._ensure_loaded()
        results = self.model.predict(
            source=str(image_path),
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            imgsz=self.image_size,
            device=self.device,
            verbose=False,
        )
        return self._convert_result(str(image_path), results[0])

    def predict_frame(self, frame: Any) -> DetectionResult:
        self._ensure_loaded()
        results = self.model.predict(
            source=frame,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            imgsz=self.image_size,
            device=self.device,
            verbose=False,
        )
        return self._convert_result("<frame>", results[0])

    def batch_predict(self, paths) -> list[DetectionResult]:
        return [self.predict_image(Path(path)) for path in paths]

    def close(self) -> None:
        self.model = None

    def _ensure_loaded(self) -> None:
        if self.model is None:
            self.load()

    def _convert_result(self, source: str, result: Any) -> DetectionResult:
        names = getattr(result, "names", {}) or {}
        width = height = None
        if getattr(result, "orig_shape", None):
            height, width = int(result.orig_shape[0]), int(result.orig_shape[1])
        detections: list[Detection] = []
        boxes = getattr(result, "boxes", None)
        if boxes is not None:
            for box in boxes:
                xyxy = box.xyxy[0].tolist()
                class_id = int(box.cls[0])
                detections.append(
                    Detection(
                        label=str(names.get(class_id, class_id)),
                        confidence=float(box.conf[0]),
                        box=BoundingBox(*[float(value) for value in xyxy]),
                    )
                )
        return DetectionResult(source=source, detections=detections, width=width, height=height, metadata={"backend": "ultralytics"})
