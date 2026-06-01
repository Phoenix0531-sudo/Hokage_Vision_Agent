from pathlib import Path

from PIL import Image

from hokage_vision.vision.backends.mock import MockBackend
from hokage_vision.vision.inference import InferenceService


def _image(path: Path) -> Path:
    Image.new("RGB", (100, 100), (20, 30, 40)).save(path)
    return path


def test_detect_image_with_mock_backend(tmp_path: Path) -> None:
    image_path = _image(tmp_path / "input.png")
    service = InferenceService(MockBackend())

    result = service.detect_image(image_path)

    assert result.source.endswith("input.png")
    assert len(result.detections) == 3


def test_detect_folder_filters_images_and_reports_progress(tmp_path: Path) -> None:
    _image(tmp_path / "a.png")
    _image(tmp_path / "b.jpg")
    (tmp_path / "ignore.txt").write_text("not an image", encoding="utf-8")
    progress: list[tuple[int, int]] = []
    service = InferenceService(MockBackend())

    results = service.detect_folder(tmp_path, progress_callback=lambda done, total: progress.append((done, total)))

    assert len(results) == 2
    assert progress == [(1, 2), (2, 2)]
