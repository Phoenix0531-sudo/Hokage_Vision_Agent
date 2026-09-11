"""Unit tests for vision.benchmark."""

from __future__ import annotations

from pathlib import Path

import pytest

from hokage_vision.core.types import DetectionResult
from hokage_vision.vision.backends.base import VisionBackend
from hokage_vision.vision.benchmark import benchmark_fps


class _TimingBackend(VisionBackend):
    """Minimal fake backend with a configurable per-prediction sleep."""

    def __init__(self, delay_s: float = 0.001) -> None:
        self.delay_s = delay_s
        self.load_calls = 0
        self.predictions = 0

    def load(self) -> None:
        self.load_calls += 1

    def predict_image(self, image_path: Path) -> DetectionResult:
        import time

        time.sleep(self.delay_s)
        self.predictions += 1
        return DetectionResult(source=str(image_path), detections=[], width=1, height=1)

    def predict_frame(self, frame) -> DetectionResult:
        return DetectionResult(source="<frame>", detections=[], width=1, height=1)

    def batch_predict(self, paths) -> list[DetectionResult]:
        return [self.predict_image(Path(p)) for p in paths]

    def close(self) -> None:
        return None


def test_benchmark_fps_reports_statistics(tmp_path) -> None:
    images = []
    for index in range(2):
        image = tmp_path / f"img_{index}.jpg"
        image.write_bytes(b"stub")
        images.append(image)

    report = benchmark_fps(_TimingBackend(delay_s=0.001), images, warmup=1, repeats=2)

    assert report["backend"] == "_TimingBackend"
    assert report["images"] == 2
    assert report["repeats"] == 2
    assert report["warmup"] == 1
    assert report["fps"] > 0
    assert len(report["fps_by_image"]) == 2
    assert all(fps > 0 for fps in report["fps_by_image"])
    assert 0 < report["latency_ms_mean"] < 5000
    assert report["latency_ms_min"] <= report["latency_ms_mean"] <= report["latency_ms_max"]
    # 2 images x 2 repeats
    assert report["latency_ms_stdev"] >= 0


def test_benchmark_fps_calls_load_once(tmp_path) -> None:
    image = tmp_path / "only.jpg"
    image.write_bytes(b"stub")
    backend = _TimingBackend()
    benchmark_fps(backend, [image], warmup=1, repeats=1)
    assert backend.load_calls == 1
    # warmup(1) + repeats(1)
    assert backend.predictions == 2


def test_benchmark_fps_rejects_empty_paths() -> None:
    with pytest.raises(ValueError, match="at least one image"):
        benchmark_fps(_TimingBackend(), [])


def test_benchmark_fps_with_mock_backend(tmp_path) -> None:
    from PIL import Image

    from hokage_vision.vision.backends.mock import MockBackend

    image = tmp_path / "sample.jpg"
    Image.new("RGB", (64, 48), (10, 20, 30)).save(image)
    report = benchmark_fps(MockBackend(), [image], warmup=1, repeats=3)
    assert report["backend"] == "MockBackend"
    assert report["fps"] > 0
