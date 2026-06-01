from __future__ import annotations

import typer

from hokage_vision import __version__

app = typer.Typer(
    name="hokage-vision",
    help="Hokage Vision Agent command line interface.",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit


@app.callback()
def root(
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show the installed Hokage Vision Agent version.",
    ),
) -> None:
    """Run Hokage Vision Agent commands."""


def main() -> None:
    app()
