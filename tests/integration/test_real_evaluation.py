"""Optional real mAP evaluation + FPS benchmark tests.

These exercise evaluate_model(mock=False) against the closed-loop trained
weights and benchmark_fps over the validation images. They skip when the
local artifacts (runs/closed-loop/...) are absent, so CI without the
trained weights stays green.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from hokage_vision.vision.backends.ultralytics_backend import UltralyticsBackend
from hokage_vision.vision.benchmark import benchmark_fps
from hokage_vision.vision.evaluation import evaluate_model

ultralytics = pytest.importorskip("ultralytics")

PT_WEIGHTS = Path("runs/closed-loop/train/run/weights/best.pt")
DATASET_YAML = Path("runs/closed-loop/dataset/dataset.yaml")
VAL_IMAGES_DIR = Path("runs/closed-loop/dataset/images/val")

pytestmark = pytest.mark.integration


def _require_artifacts() -> None:
    if not PT_WEIGHTS.exists() or not DATASET_YAML.exists():
        pytest.skip("no closed-loop artifacts (run scripts/closed_loop_demo.py first)")


def test_real_evaluation_reports_real_map() -> None:
    _require_artifacts()
    payload = evaluate_model(PT_WEIGHTS, DATASET_YAML, mock=False)
    assert payload["mock"] is False
    metrics = payload["metrics"]
    assert 0.0 <= metrics["map50"] <= 1.0
    assert 0.0 <= metrics["map50_95"] <= 1.0
    # the synthetic task is easy; a trained model must exceed random chance
    assert metrics["map50"] > 0.5
    assert metrics["precision"] > 0.5
    assert metrics["recall"] > 0.5


def test_real_evaluation_metrics_consistent_between_runs() -> None:
    _require_artifacts()
    first = evaluate_model(PT_WEIGHTS, DATASET_YAML, mock=False)["metrics"]
    second = evaluate_model(PT_WEIGHTS, DATASET_YAML, mock=False)["metrics"]
    assert first["map50"] == pytest.approx(second["map50"])


def test_real_fps_benchmark_on_validation_images() -> None:
    _require_artifacts()
    images = sorted(VAL_IMAGES_DIR.glob("*.jpg"))[:3]
    assert images, "no validation images found"
    backend = UltralyticsBackend(PT_WEIGHTS, conf_threshold=0.5, image_size=320)
    report = benchmark_fps(backend, images, warmup=2, repeats=3)
    assert report["backend"] == "UltralyticsBackend"
    assert report["fps"] > 0
    assert report["latency_ms_mean"] > 0
    assert len(report["fps_by_image"]) == len(images)
