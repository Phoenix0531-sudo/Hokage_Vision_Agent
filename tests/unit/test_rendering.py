from pathlib import Path

from PIL import Image

from hokage_vision.vision.backends.mock import MockBackend
from hokage_vision.vision.rendering import render_detections


def test_render_detections_saves_output(tmp_path: Path) -> None:
    image_path = tmp_path / "input.png"
    output_path = tmp_path / "rendered.jpg"
    Image.new("RGB", (100, 100), (10, 20, 30)).save(image_path)
    result = MockBackend().predict_image(image_path)

    rendered = render_detections(image_path, result, output_path)

    assert rendered.size == (100, 100)
    assert output_path.exists()
