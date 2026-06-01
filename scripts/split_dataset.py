from __future__ import annotations

import typer


def main() -> None:
    typer.echo("Dataset splitting will preserve manifest and license metadata.")


if __name__ == "__main__":
    typer.run(main)
