from __future__ import annotations

from pathlib import Path
from typing import Any

from hokage_vision.core.errors import VisionBackendError
from hokage_vision.core.types import DetectionResult
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
        raise VisionBackendError("YOLOv5 legacy prediction is available after legacy isolation.")

    def predict_frame(self, frame: Any) -> DetectionResult:
        raise VisionBackendError("YOLOv5 legacy prediction is available after legacy isolation.")

    def batch_predict(self, paths) -> list[DetectionResult]:
        return [self.predict_image(Path(path)) for path in paths]

    def close(self) -> None:
        self.model = None
