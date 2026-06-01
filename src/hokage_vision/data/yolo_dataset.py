from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yolo_dataset_yaml(path: Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        msg = f"YOLO dataset yaml must be a mapping: {path}"
        raise ValueError(msg)
    return data


def class_names(data: dict[str, Any]) -> list[str]:
    names = data.get("names", [])
    if isinstance(names, dict):
        return [str(names[key]) for key in sorted(names)]
    return [str(name) for name in names]
