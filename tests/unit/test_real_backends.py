from pathlib import Path

import pytest

from hokage_vision.core.errors import VisionBackendError
from hokage_vision.vision.backends.factory import create_backend
from hokage_vision.vision.backends.mock import MockBackend
from hokage_vision.vision.backends.ultralytics_backend import UltralyticsBackend
from hokage_vision.vision.backends.yolov5_legacy_backend import YOLOv5LegacyBackend


def test_ultralytics_backend_reports_missing_model() -> None:
    backend = UltralyticsBackend(Path("models/missing.pt"))

    with pytest.raises(VisionBackendError, match="Model file does not exist"):
        backend.load()


def test_backend_factory_accepts_mock() -> None:
    assert isinstance(create_backend("mock"), MockBackend)


def test_backend_factory_rejects_unknown_backend() -> None:
    with pytest.raises(VisionBackendError, match="Unsupported backend"):
        create_backend("camera")


def test_legacy_backend_reports_missing_model_before_importing_legacy_code() -> None:
    backend = YOLOv5LegacyBackend(Path("models/missing.pt"))

    with pytest.raises(VisionBackendError, match="Model file does not exist"):
        backend.load()


def test_legacy_backend_converts_yolov5_xyxy_rows() -> None:
    class FakeTensor:
        def detach(self):
            return self

        def cpu(self):
            return self

        def tolist(self):
            return [[1, 2, 10, 20, 0.8, 1]]

    class FakeImage:
        shape = (24, 32, 3)

    class FakeResult:
        xyxy = [FakeTensor()]
        ims = [FakeImage()]
        names = {1: "naruto"}

    backend = YOLOv5LegacyBackend(Path("models/fake.pt"))
    backend.model = object()

    result = backend._convert_result("sample.jpg", FakeResult())

    assert result.metadata["backend"] == "yolov5_legacy"
    assert result.width == 32
    assert result.height == 24
    assert result.detections[0].label == "naruto"
    assert result.detections[0].confidence == 0.8
