from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from hokage_vision.core.types import DetectionResult


class VisionBackend(ABC):
    @abstractmethod
    def load(self) -> None:
        """Load backend resources."""

    @abstractmethod
    def predict_image(self, image_path: Path) -> DetectionResult:
        """Run detection on an image path."""

    @abstractmethod
    def predict_frame(self, frame: Any) -> DetectionResult:
        """Run detection on an in-memory frame."""

    @abstractmethod
    def batch_predict(self, paths: Iterable[Path]) -> list[DetectionResult]:
        """Run detection on a batch of image paths."""

    @abstractmethod
    def close(self) -> None:
        """Release backend resources."""
