from __future__ import annotations


def mock_evaluation_metrics() -> dict[str, float | None]:
    return {"map50": None, "map50_95": None, "precision": None, "recall": None}
