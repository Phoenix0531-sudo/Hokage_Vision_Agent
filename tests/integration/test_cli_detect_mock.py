from __future__ import annotations

import json
import subprocess
import sys


def test_cli_detect_image_mock() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hokage_vision",
            "detect",
            "image",
            "examples/images/sample.jpg",
            "--backend",
            "mock",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["detections"][0]["label"] == "obito"
    assert payload["metadata"]["backend"] == "mock"


def test_cli_ultralytics_backend_reports_missing_model() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hokage_vision",
            "detect",
            "image",
            "examples/images/sample.jpg",
            "--backend",
            "ultralytics",
            "--model-path",
            "models/missing.pt",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Model file does not exist" in result.stderr
