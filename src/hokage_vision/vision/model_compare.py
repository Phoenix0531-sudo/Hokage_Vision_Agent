from __future__ import annotations

from pathlib import Path

from hokage_vision.core.types import ModelInfo
from hokage_vision.vision.evaluation import mock_evaluation_metrics


def compare_model_info(models: list[ModelInfo]) -> list[dict[str, object]]:
    return [
        {
            "name": model.name,
            "version": model.version,
            "backend": model.backend,
            "classes": model.classes,
            "metrics": model.metrics,
            "notes": model.notes,
        }
        for model in models
    ]


def compare_model_paths(models: list[Path], *, mock: bool = True) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for model_path in models:
        path = Path(model_path)
        rows.append(
            {
                "name": path.stem,
                "path": str(path),
                "backend": "mock" if mock else "ultralytics",
                "classes": ["obito", "naruto", "gaara"],
                "metrics": mock_evaluation_metrics(),
                "size_bytes": path.stat().st_size if path.exists() else None,
                "license": "TBD",
                "notes": "Mock comparison row; real metrics require evaluation.",
            }
        )
    return rows
