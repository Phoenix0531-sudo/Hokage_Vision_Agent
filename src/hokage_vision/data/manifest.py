from __future__ import annotations

from pathlib import Path

import yaml

from hokage_vision.data.schema import AnnotationInfo, DatasetInfo, DatasetManifest, DatasetSource


def load_dataset_manifest(path: Path) -> DatasetManifest:
    with Path(path).open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    return DatasetManifest.model_validate(data)


def create_dataset_manifest(
    images: Path,
    output: Path,
    *,
    name: str = "hokage-vision-local",
    classes: list[str] | None = None,
) -> DatasetManifest:
    manifest = DatasetManifest(
        dataset=DatasetInfo(
            name=name,
            description="Local dataset manifest. Raw images are not redistributed by default.",
            redistribution_allowed=False,
        ),
        sources=[
            DatasetSource(
                id="local-001",
                path=images,
                license="unknown",
                redistribution_allowed=False,
                notes="User-provided local images. Do not commit raw images without rights review.",
            )
        ],
        classes=classes or ["obito", "naruto", "gaara"],
        annotations=AnnotationInfo(format="yolo", reviewed=False),
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(manifest.model_dump(mode="json"), sort_keys=False), encoding="utf-8")
    return manifest
