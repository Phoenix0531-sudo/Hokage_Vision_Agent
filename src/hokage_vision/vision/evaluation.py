"""Model evaluation helpers.

``evaluate_model`` returns mock metrics by default (offline-safe). With
``mock=False`` it runs a real Ultralytics ``val`` pass over a YOLO dataset
yaml and reports mAP50 / mAP50-95 / precision / recall.
"""

from __future__ import annotations

from pathlib import Path

from hokage_vision.core.errors import VisionBackendError


def mock_evaluation_metrics() -> dict[str, float | None]:
    return {"map50": None, "map50_95": None, "precision": None, "recall": None}


def _real_metrics(model_path: Path, data: Path) -> dict[str, float]:
    """Run a real ultralytics val pass and extract headline metrics."""
    try:
        from ultralytics import YOLO  # type: ignore[import-not-found]
    except ImportError as exc:
        msg = "Real evaluation requires the train extra: pip install -e '.[train]'"
        raise VisionBackendError(msg) from exc

    model = YOLO(str(model_path))
    results = model.val(data=str(data), verbose=False)
    box = results.box
    return {
        "map50": float(box.map50),
        "map50_95": float(box.map),
        "precision": float(box.mp),
        "recall": float(box.mr),
    }


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
    model_path = Path(model_path)
    if not model_path.exists():
        msg = f"Model file does not exist: {model_path}"
        raise VisionBackendError(msg)
    if data is None:
        msg = "Real evaluation requires a YOLO dataset yaml path."
        raise VisionBackendError(msg)
    data = Path(data)
    if not data.exists():
        msg = f"Dataset file does not exist: {data}"
        raise VisionBackendError(msg)
    return {
        "model": str(model_path),
        "data": str(data),
        "mock": False,
        "metrics": _real_metrics(model_path, data),
    }
