from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("ultralytics", reason="train extra not installed")
pytest.importorskip("onnxruntime", reason="onnx runtime not installed")

from hokage_vision.vision.backends.ultralytics_backend import UltralyticsBackend  # noqa: E402

MODEL_PATH = Path("models/yolo11n.onnx")
SAMPLE_IMAGE = Path("examples/images/sample.jpg")
if not MODEL_PATH.exists():
    pytest.skip(
        f"local ONNX model missing at {MODEL_PATH} (run scripts/closed_loop_demo.py first)",
        allow_module_level=True,
    )

@pytest.fixture(name="backend")
def _backend() -> UltralyticsBackend:
    backend = UltralyticsBackend(MODEL_PATH, conf_threshold=0.25)
    backend.load()
    return backend


@pytest.mark.integration
def test_real_inference_returns_wellformed_result(backend: UltralyticsBackend) -> None:
    result = backend.predict_image(SAMPLE_IMAGE)

    assert result.source.endswith("sample.jpg")
    assert result.width == 160
    assert result.height == 120
    assert result.metadata["backend"] == "ultralytics"
    for detection in result.detections:
        assert 0.0 <= detection.confidence <= 1.0
        assert 0 <= detection.box.x1 < detection.box.x2 <= result.width
        assert 0 <= detection.box.y1 < detection.box.y2 <= result.height
        assert detection.label


@pytest.mark.integration
def test_real_inference_is_deterministic(backend: UltralyticsBackend) -> None:
    first = backend.predict_image(SAMPLE_IMAGE)
    second = backend.predict_image(SAMPLE_IMAGE)

    assert len(first.detections) == len(second.detections)
    for a, b in zip(first.detections, second.detections, strict=False):
        assert a.label == b.label
        assert a.confidence == pytest.approx(b.confidence, abs=1e-6)
        assert a.box.x1 == pytest.approx(b.box.x1, abs=1e-3)


@pytest.mark.integration
def test_real_inference_high_conf_threshold_filters_detections() -> None:
    strict = UltralyticsBackend(MODEL_PATH, conf_threshold=0.99)
    strict.load()

    result = strict.predict_image(SAMPLE_IMAGE)

    assert all(detection.confidence >= 0.99 for detection in result.detections)
    assert len(result.detections) <= 1
