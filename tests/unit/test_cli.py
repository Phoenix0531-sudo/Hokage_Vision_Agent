"""In-process CLI tests using typer's CliRunner.

These complement the subprocess-based tests in tests/integration and give
real coverage for src/hokage_vision/cli.py (subprocess runs are invisible to
coverage measurement).
"""

from __future__ import annotations

import json

import cv2
import numpy as np
import pytest
from PIL import Image
from typer.testing import CliRunner

from hokage_vision.cli import app

runner = CliRunner()


def _make_image(path, size: tuple[int, int] = (64, 48)) -> None:
    Image.new("RGB", size, (120, 30, 200)).save(path)


def _make_video(path, frames: int = 10, size: tuple[int, int] = (64, 48)) -> None:
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), 10, size)
    for i in range(frames):
        frame = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        x = 5 + i
        frame[10:30, x : x + 20] = 255
        writer.write(frame)
    writer.release()


def _parse(result) -> dict | list:
    return json.loads(result.output)


# ------------------------------------------------------------------ basics


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output.strip()


def test_no_args_shows_help() -> None:
    result = runner.invoke(app, [])
    assert "Hokage Vision Agent" in result.output


# ------------------------------------------------------------------ detect


def test_detect_image_mock() -> None:
    result = runner.invoke(
        app, ["detect", "image", "examples/images/sample.jpg", "--backend", "mock"]
    )
    assert result.exit_code == 0, result.output
    payload = _parse(result)
    assert payload["metadata"]["backend"] == "mock"
    assert payload["detections"][0]["label"] == "obito"


def test_detect_image_missing_model_reports_error() -> None:
    result = runner.invoke(
        app,
        [
            "detect",
            "image",
            "examples/images/sample.jpg",
            "--backend",
            "ultralytics",
            "--model-path",
            "models/missing.pt",
        ],
    )
    assert result.exit_code != 0
    assert "Model file does not exist" in result.output


def test_detect_folder_mock(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _make_image(tmp_path / "a.png")
    _make_image(tmp_path / "b.png")
    (tmp_path / "notes.txt").write_text("not an image", encoding="utf-8")
    result = runner.invoke(app, ["detect", "folder", ".", "--backend", "mock"])
    assert result.exit_code == 0, result.output
    payload = _parse(result)
    assert isinstance(payload, list) and len(payload) == 2


def test_detect_video_mock(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _make_video(tmp_path / "clip.mp4", frames=8)
    result = runner.invoke(
        app, ["detect", "video", "clip.mp4", "--backend", "mock", "--frame-stride", "2"]
    )
    assert result.exit_code == 0, result.output
    payload = _parse(result)
    assert payload["processed_frames"] >= 1


# ------------------------------------------------------------------ dataset


def test_dataset_validate_example_config() -> None:
    result = runner.invoke(app, ["dataset", "validate", "configs/dataset.example.yaml"])
    assert result.exit_code == 0, result.output
    payload = _parse(result)
    assert payload["valid"] is True


def test_dataset_validate_missing_yaml_reports_issues(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["dataset", "validate", "missing.yaml"])
    assert result.exit_code == 0
    payload = _parse(result)
    assert payload["valid"] is False
    assert payload["issues"]


def test_dataset_manifest_create(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _make_image(tmp_path / "img.png")
    result = runner.invoke(
        app,
        [
            "dataset",
            "manifest",
            "create",
            "--images",
            ".",
            "--output",
            "manifests/local.yaml",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = _parse(result)
    assert payload["dataset"]["name"]
    assert payload["sources"][0]["path"]


def test_annotation_assist(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _make_image(tmp_path / "img.png")
    result = runner.invoke(app, ["annotation", "assist", "--images", ".", "--output", "labels"])
    assert result.exit_code == 0, result.output
    payload = _parse(result)
    assert payload["review_required"] is True
    assert payload["model"] is None


# ------------------------------------------------------------------ train


def test_train_smoke() -> None:
    result = runner.invoke(app, ["train", "smoke"])
    assert result.exit_code == 0, result.output
    payload = _parse(result)
    assert payload["status"] == "completed"


def test_train_yolo_dry_run_plan(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "dataset.yaml").write_text("train: images/train\nval: images/val\n")
    result = runner.invoke(
        app,
        [
            "train",
            "yolo",
            "--data",
            "dataset.yaml",
            "--epochs",
            "2",
            "--device",
            "cpu",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = _parse(result)
    assert payload["status"] == "planned"
    assert payload["dry_run"] is True


# ------------------------------------------------------------------ model


def test_model_list_empty(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["model", "list"])
    assert result.exit_code == 0, result.output
    assert _parse(result)["models"] == []


def test_model_register_and_list(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "m.pt").write_bytes(b"stub")
    result = runner.invoke(
        app,
        ["model", "register", "--name", "demo", "--path", "m.pt", "--backend", "mock"],
    )
    assert result.exit_code == 0, result.output
    record = _parse(result)
    assert record["name"] == "demo"

    listed = _parse(runner.invoke(app, ["model", "list"]))
    assert listed["models"][0]["name"] == "demo"


def test_model_evaluate_mock() -> None:
    result = runner.invoke(app, ["model", "evaluate", "--model", "models/whatever.pt"])
    assert result.exit_code == 0, result.output
    payload = _parse(result)
    assert payload["mock"] is True
    assert payload["metrics"]


def test_model_evaluate_real_requires_existing_model(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data.yaml").write_text("train: t\nval: v\n")
    result = runner.invoke(
        app,
        [
            "model",
            "evaluate",
            "--model",
            "missing.pt",
            "--data",
            "data.yaml",
            "--real",
        ],
    )
    assert result.exit_code != 0
    assert "Model file does not exist" in result.output


def test_model_benchmark_missing_model(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _make_image(tmp_path / "img.png")
    result = runner.invoke(
        app, ["model", "benchmark", "--model", "missing.onnx", "--image", "img.png"]
    )
    assert result.exit_code != 0
    assert "Model file does not exist" in result.output


def test_model_compare_requires_paths() -> None:
    result = runner.invoke(app, ["model", "compare"])
    assert result.exit_code != 0
    assert "At least one model path is required" in result.output


def test_model_compare_mock(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "a.pt").write_bytes(b"aaaa")
    (tmp_path / "b.pt").write_bytes(b"bbbbbb")
    result = runner.invoke(app, ["model", "compare", "--mock", "a.pt", "b.pt"])
    assert result.exit_code == 0, result.output
    payload = _parse(result)
    assert len(payload["models"]) == 2


# ------------------------------------------------------------------ agent


def test_agent_run_detect_folder(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _make_image(tmp_path / "img.png")
    result = runner.invoke(app, ["agent", "run", "批量识别 . 文件夹里的目标"])
    assert result.exit_code == 0, result.output
    payload = _parse(result)
    assert payload["tool_calls"][0]["name"] == "detect_folder"


def test_agent_run_refuses_out_of_scope() -> None:
    result = runner.invoke(app, ["agent", "run", "帮我写小说"])
    assert result.exit_code == 0, result.output
    assert "Agent refused" in _parse(result)["message"]


# ------------------------------------------------------------------ api


def test_api_command_without_uvicorn(tmp_path, monkeypatch) -> None:
    pytest.importorskip("uvicorn")
    # uvicorn is installed in this env; only assert the command parses.
    result = runner.invoke(app, ["api", "--help"])
    assert result.exit_code == 0
    assert "Launch the FastAPI service" in result.output
