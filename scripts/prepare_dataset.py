from __future__ import annotations

import typer


def main() -> None:
    typer.echo("Dataset preparation is project-scoped and requires a reviewed manifest.")


if __name__ == "__main__":
    typer.run(main)
