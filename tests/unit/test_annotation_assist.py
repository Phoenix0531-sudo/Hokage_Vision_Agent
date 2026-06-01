from pathlib import Path

from PIL import Image

from hokage_vision.data.annotation import assist_annotation


def test_assist_annotation_writes_candidate_labels_and_review_file(tmp_path: Path) -> None:
    image_dir = tmp_path / "images"
    output_dir = tmp_path / "labels"
    image_dir.mkdir()
    Image.new("RGB", (64, 64), (10, 10, 10)).save(image_dir / "sample.jpg")

    result = assist_annotation(image_dir, output_dir)

    assert result["review_required"] is True
    assert (output_dir / "sample.txt").exists()
    assert (output_dir / "review_required.yaml").exists()
