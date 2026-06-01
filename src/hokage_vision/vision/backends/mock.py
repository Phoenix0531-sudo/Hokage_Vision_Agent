from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

from PIL import Image

from hokage_vision.core.errors import VisionBackendError
from hokage_vision.core.types import BoundingBox, Detection, DetectionResult
from hokage_vision.vision.backends.base import VisionBackend


class MockBackend(VisionBackend):
    """Deterministic backend used by tests, demos, API smoke tests, and CI."""

    def __init__(self, classes: list[str] | None = None) -> None:
        self.classes = classes or ["obito", "naruto", "gaara"]
        self.loaded = False

    def load(self) -> None:
        self.loaded = True

    def predict_image(self, image_path: Path) -> DetectionResult:
        self._ensure_loaded()
        if not image_path.exists():
            msg = f"Image does not exist: {image_path}"
            raise VisionBackendError(msg)
        with Image.open(image_path) as image:
            width, height = image.size
        return DetectionResult(
            source=str(image_path),
            width=width,
            height=height,
            detections=self._detections(width, height),
            metadata={"backend": "mock"},
        )

    def predict_frame(self, frame: Any) -> DetectionResult:
        self._ensure_loaded()
        width, height = self._frame_size(frame)
        return DetectionResult(
            source="<frame>",
            width=width,
            height=height,
            detections=self._detections(width, height),
            metadata={"backend": "mock"},
        )

    def batch_predict(self, paths: Iterable[Path]) -> list[DetectionResult]:
        return [self.predict_image(Path(path)) for path in paths]

    def close(self) -> None:
        self.loaded = False

    def _ensure_loaded(self) -> None:
        if not self.loaded:
            self.load()

    def _detections(self, width: int | None, height: int | None) -> list[Detection]:
        width = width or 100
        height = height or 100
        boxes = [
            BoundingBox(width * 0.10, height * 0.12, width * 0.42, height * 0.70),
            BoundingBox(width * 0.45, height * 0.18, width * 0.74, height * 0.76),
            BoundingBox(width * 0.66, height * 0.22, width * 0.92, height * 0.80),
        ]
        return [
            Detection(label=label, confidence=round(0.91 - index * 0.07, 2), box=boxes[index])
            for index, label in enumerate(self.classes[:3])
        ]

    def _frame_size(self, frame: Any) -> tuple[int | None, int | None]:
        if hasattr(frame, "size") and isinstance(frame.size, tuple):
            return frame.size
        if hasattr(frame, "shape") and len(frame.shape) >= 2:
            return int(frame.shape[1]), int(frame.shape[0])
        return None, None
