from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve

import typer


def main(url: str, output: Path) -> None:
    if "github.com" not in url:
        raise typer.BadParameter("Only reviewed GitHub Release URLs are supported by this helper.")
    output.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(url, output)
    typer.echo(f"Downloaded model artifact to {output}. Verify its license before use.")


if __name__ == "__main__":
    typer.run(main)
