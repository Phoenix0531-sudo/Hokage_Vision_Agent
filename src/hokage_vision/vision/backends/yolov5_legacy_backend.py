from __future__ import annotations

from pathlib import Path
from typing import Any

from hokage_vision.core.errors import VisionBackendError
from hokage_vision.core.types import BoundingBox, Detection, DetectionResult
from hokage_vision.vision.backends.base import VisionBackend


class YOLOv5LegacyBackend(VisionBackend):
    """Compatibility boundary for old YOLOv5 weights.

    This backend intentionally does not import legacy YOLOv5 modules at package import time.
    """

    def __init__(
        self, model_path: Path | None, legacy_root: Path = Path("legacy/old_project")
    ) -> None:
        self.model_path = Path(model_path) if model_path else None
        self.legacy_root = Path(legacy_root)
        self.model: Any | None = None

    def load(self) -> None:
        if self.model_path is None:
            raise VisionBackendError("YOLOv5 legacy backend requires an explicit model path.")
        if not self.model_path.exists():
            raise VisionBackendError(f"Model file does not exist: {self.model_path}")
        if not self.legacy_root.exists():
            raise VisionBackendError(
                f"Legacy YOLOv5 source is not isolated at {self.legacy_root}. Run migration first."
            )
        try:
            import torch  # type: ignore[import-not-found]
        except ImportError as exc:
            msg = "YOLOv5 legacy backend requires torch and the isolated legacy source tree."
            raise VisionBackendError(msg) from exc
        self.model = torch.hub.load(
            str(self.legacy_root),
            "custom",
            path=str(self.model_path),
            source="local",
        )

    def predict_image(self, image_path: Path) -> DetectionResult:
        self._ensure_loaded()
        result = self.model(str(image_path))
        return self._convert_result(str(image_path), result)

    def predict_frame(self, frame: Any) -> DetectionResult:
        self._ensure_loaded()
        result = self.model(frame)
        return self._convert_result("<frame>", result)

    def batch_predict(self, paths) -> list[DetectionResult]:
        return [self.predict_image(Path(path)) for path in paths]

    def close(self) -> None:
        self.model = None

    def _ensure_loaded(self) -> None:
        if self.model is None:
            self.load()

    def _convert_result(self, source: str, result: Any) -> DetectionResult:
        rows = []
        if getattr(result, "xyxy", None):
            rows = result.xyxy[0].detach().cpu().tolist()

        names = getattr(result, "names", None) or getattr(self.model, "names", {}) or {}
        width = height = None
        images = getattr(result, "ims", None)
        if images:
            shape = getattr(images[0], "shape", None)
            if shape is not None and len(shape) >= 2:
                height, width = int(shape[0]), int(shape[1])

        detections: list[Detection] = []
        for row in rows:
            x1, y1, x2, y2, confidence, class_id = row[:6]
            detections.append(
                Detection(
                    label=str(names.get(int(class_id), int(class_id))),
                    confidence=float(confidence),
                    box=BoundingBox(float(x1), float(y1), float(x2), float(y2)),
                )
            )

        return DetectionResult(
            source=source,
            detections=detections,
            width=width,
            height=height,
            metadata={"backend": "yolov5_legacy"},
        )
