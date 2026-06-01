from pathlib import Path

from PIL import Image

from hokage_vision.data.validation import validate_yolo_dataset


def test_validate_yolo_dataset_reports_valid_tiny_dataset(tmp_path: Path) -> None:
    image_dir = tmp_path / "images" / "train"
    label_dir = tmp_path / "labels" / "train"
    image_dir.mkdir(parents=True)
    label_dir.mkdir(parents=True)
    Image.new("RGB", (32, 32), (0, 0, 0)).save(image_dir / "a.jpg")
    (label_dir / "a.txt").write_text("0 0.5 0.5 0.25 0.25\n", encoding="utf-8")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text("dataset:\n  name: tiny\nsources: []\nclasses: [obito]\n", encoding="utf-8")
    dataset_yaml = tmp_path / "dataset.yaml"
    dataset_yaml.write_text(
        "path: .\ntrain: images/train\nval: images/train\nnames:\n  0: obito\nmanifest: manifest.yaml\n",
        encoding="utf-8",
    )

    report = validate_yolo_dataset(dataset_yaml)

    assert report.valid is True
    assert report.image_count == 2
    assert report.box_count == 2
    assert report.class_distribution == {0: 2}


def test_validate_yolo_dataset_reports_missing_labels(tmp_path: Path) -> None:
    image_dir = tmp_path / "images" / "train"
    image_dir.mkdir(parents=True)
    Image.new("RGB", (32, 32), (0, 0, 0)).save(image_dir / "a.jpg")
    dataset_yaml = tmp_path / "dataset.yaml"
    dataset_yaml.write_text("path: .\ntrain: images/train\nval: images/train\nnames: [obito]\n", encoding="utf-8")

    report = validate_yolo_dataset(dataset_yaml)

    assert report.valid is False
    assert report.missing_labels
