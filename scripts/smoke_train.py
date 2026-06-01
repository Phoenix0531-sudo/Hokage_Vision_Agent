from __future__ import annotations

import json

import typer

from hokage_vision.training.smoke import run_smoke_training


def main() -> None:
    typer.echo(json.dumps(run_smoke_training(), indent=2, default=str))


if __name__ == "__main__":
    typer.run(main)
