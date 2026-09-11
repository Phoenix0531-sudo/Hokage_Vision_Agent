"""Unit tests for vision.evaluation."""

from __future__ import annotations

import sys

import pytest

from hokage_vision.core.errors import VisionBackendError
from hokage_vision.vision.evaluation import (
    evaluate_model,
    mock_evaluation_metrics,
)


def test_mock_evaluation_metrics_are_all_none() -> None:
    assert mock_evaluation_metrics() == {
        "map50": None,
        "map50_95": None,
        "precision": None,
        "recall": None,
    }


def test_evaluate_model_mock_path(tmp_path) -> None:
    payload = evaluate_model(tmp_path / "whatever.pt", tmp_path / "data.yaml", mock=True)
    assert payload["mock"] is True
    assert payload["metrics"] == mock_evaluation_metrics()
    # mock path never touches the filesystem
    assert payload["model"].endswith("whatever.pt")


def test_evaluate_model_real_requires_existing_model(tmp_path) -> None:
    with pytest.raises(VisionBackendError, match="Model file does not exist"):
        evaluate_model(tmp_path / "missing.pt", mock=False)


def test_evaluate_model_real_requires_dataset(tmp_path) -> None:
    model = tmp_path / "model.pt"
    model.write_bytes(b"stub")
    with pytest.raises(VisionBackendError, match="requires a YOLO dataset yaml"):
        evaluate_model(model, mock=False)


def test_evaluate_model_real_requires_existing_dataset(tmp_path) -> None:
    model = tmp_path / "model.pt"
    model.write_bytes(b"stub")
    with pytest.raises(VisionBackendError, match="Dataset file does not exist"):
        evaluate_model(model, tmp_path / "missing.yaml", mock=False)


def test_evaluate_model_real_without_ultralytics(tmp_path, monkeypatch) -> None:
    model = tmp_path / "model.pt"
    model.write_bytes(b"stub")
    data = tmp_path / "dataset.yaml"
    data.write_text("path: .\n", encoding="utf-8")
    monkeypatch.setitem(sys.modules, "ultralytics", None)
    with pytest.raises(VisionBackendError, match="train extra"):
        evaluate_model(model, data, mock=False)
