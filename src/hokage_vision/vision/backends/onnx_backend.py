from __future__ import annotations

from pathlib import Path
from typing import Any

from hokage_vision.core.errors import VisionBackendError
from hokage_vision.core.types import DetectionResult
from hokage_vision.vision.backends.base import VisionBackend


class ONNXBackend(VisionBackend):
    def __init__(self, model_path: Path | None) -> None:
        self.model_path = Path(model_path) if model_path else None

    def load(self) -> None:
        raise VisionBackendError("ONNX backend is reserved for a future release.")

    def predict_image(self, image_path: Path) -> DetectionResult:
        raise VisionBackendError("ONNX backend is reserved for a future release.")

    def predict_frame(self, frame: Any) -> DetectionResult:
        raise VisionBackendError("ONNX backend is reserved for a future release.")

    def batch_predict(self, paths) -> list[DetectionResult]:
        raise VisionBackendError("ONNX backend is reserved for a future release.")

    def close(self) -> None:
        return None
