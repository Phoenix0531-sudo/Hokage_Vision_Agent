from __future__ import annotations

import typer


def main() -> None:
    typer.echo("Open review_required.yaml and verify candidate labels before training.")


if __name__ == "__main__":
    typer.run(main)
