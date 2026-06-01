from pathlib import Path

from hokage_vision.data.manifest import create_dataset_manifest, load_dataset_manifest


def test_create_and_load_dataset_manifest(tmp_path: Path) -> None:
    output = tmp_path / "manifest.yaml"
    manifest = create_dataset_manifest(tmp_path / "images", output)

    loaded = load_dataset_manifest(output)

    assert manifest.dataset.name == "hokage-vision-local"
    assert loaded.sources[0].license == "unknown"
    assert loaded.dataset.redistribution_allowed is False
