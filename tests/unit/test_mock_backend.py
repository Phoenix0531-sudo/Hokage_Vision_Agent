from pathlib import Path

from PIL import Image

from hokage_vision.vision.backends.mock import MockBackend


def _image(path: Path, size: tuple[int, int] = (120, 80)) -> Path:
    Image.new("RGB", size, (40, 40, 40)).save(path)
    return path


def test_mock_backend_predicts_deterministic_detections(tmp_path: Path) -> None:
    backend = MockBackend()
    image_path = _image(tmp_path / "sample.png")

    result = backend.predict_image(image_path)

    assert result.source.endswith("sample.png")
    assert result.width == 120
    assert result.height == 80
    assert [item.label for item in result.detections] == ["obito", "naruto", "gaara"]
    assert result.detections[0].confidence == 0.91


def test_mock_backend_batch_predict(tmp_path: Path) -> None:
    backend = MockBackend()
    paths = [_image(tmp_path / "a.png"), _image(tmp_path / "b.png")]

    results = backend.batch_predict(paths)

    assert len(results) == 2
    assert all(result.metadata["backend"] == "mock" for result in results)
