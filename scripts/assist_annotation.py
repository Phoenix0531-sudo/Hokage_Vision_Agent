from __future__ import annotations

from pathlib import Path

import typer

from hokage_vision.data.annotation import assist_annotation


def main(images: str, output: str) -> None:
    typer.echo(assist_annotation(images=Path(images), output=Path(output)))


if __name__ == "__main__":
    typer.run(main)
