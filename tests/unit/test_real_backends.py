from pathlib import Path

import pytest

from hokage_vision.core.errors import VisionBackendError
from hokage_vision.vision.backends.ultralytics_backend import UltralyticsBackend
from hokage_vision.vision.backends.yolov5_legacy_backend import YOLOv5LegacyBackend


def test_ultralytics_backend_reports_missing_model() -> None:
    backend = UltralyticsBackend(Path("models/missing.pt"))

    with pytest.raises(VisionBackendError, match="Model file does not exist"):
        backend.load()


def test_legacy_backend_reports_missing_model_before_importing_legacy_code() -> None:
    backend = YOLOv5LegacyBackend(Path("models/missing.pt"))

    with pytest.raises(VisionBackendError, match="Model file does not exist"):
        backend.load()
