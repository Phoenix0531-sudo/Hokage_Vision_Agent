from __future__ import annotations

from pathlib import Path


def list_images(folder: Path) -> list[Path]:
    return sorted(
        path for path in Path(folder).rglob("*") if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )
