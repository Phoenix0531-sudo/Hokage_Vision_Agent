from __future__ import annotations

from pathlib import Path

import typer

from hokage_vision.data.manifest import create_dataset_manifest


def main(images: str, output: str) -> None:
    manifest = create_dataset_manifest(images=Path(images), output=Path(output))
    typer.echo(manifest.model_dump_json(indent=2))


if __name__ == "__main__":
    typer.run(main)
