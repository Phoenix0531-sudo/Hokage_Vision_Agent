from __future__ import annotations

from hokage_vision.core.types import ModelInfo


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
