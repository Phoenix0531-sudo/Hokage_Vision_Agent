from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from hokage_vision.config.settings import Settings
from hokage_vision.core.errors import ConfigError
from hokage_vision.core.paths import project_root


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        msg = f"Configuration file does not exist: {path}"
        raise ConfigError(msg)
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        msg = f"Configuration file must contain a YAML mapping: {path}"
        raise ConfigError(msg)
    return data


def _merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


def default_config_path() -> Path:
    return project_root() / "configs" / "app.default.yaml"


def load_settings(path: Path | str | None = None) -> Settings:
    base = _read_yaml(default_config_path())
    if path is not None:
        base = _merge_dicts(base, _read_yaml(Path(path)))
    return Settings.model_validate(base)
