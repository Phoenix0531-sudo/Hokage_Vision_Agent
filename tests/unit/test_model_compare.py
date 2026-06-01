from pathlib import Path

from hokage_vision.vision.model_compare import compare_model_paths


def test_compare_model_paths_returns_rows() -> None:
    rows = compare_model_paths([Path("models/a.pt"), Path("models/b.pt")], mock=True)

    assert [row["name"] for row in rows] == ["a", "b"]
    assert rows[0]["metrics"]["map50"] is None
