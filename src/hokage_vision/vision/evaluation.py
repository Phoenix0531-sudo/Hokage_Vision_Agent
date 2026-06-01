from __future__ import annotations

from pathlib import Path

from hokage_vision.core.errors import VisionBackendError


def mock_evaluation_metrics() -> dict[str, float | None]:
    return {"map50": None, "map50_95": None, "precision": None, "recall": None}


def evaluate_model(
    model_path: Path, data: Path | None = None, *, mock: bool = True
) -> dict[str, object]:
    if mock:
        return {
            "model": str(model_path),
            "data": str(data) if data else None,
            "mock": True,
            "metrics": mock_evaluation_metrics(),
        }
    if not Path(model_path).exists():
        msg = f"Model file does not exist: {model_path}"
        raise VisionBackendError(msg)
    return {
        "model": str(model_path),
        "data": str(data) if data else None,
        "mock": False,
        "metrics": mock_evaluation_metrics(),
    }
