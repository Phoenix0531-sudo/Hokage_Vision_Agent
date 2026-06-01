from pathlib import Path

import pytest

from hokage_vision.config import load_settings
from hokage_vision.core.errors import ConfigError


def test_load_default_settings() -> None:
    settings = load_settings()

    assert settings.app.name == "Hokage Vision Agent"
    assert settings.model.backend == "mock"
    assert settings.model.classes == ["obito", "naruto", "gaara"]
    assert settings.agent.shell_access is False
    assert settings.data.allow_web_download is False


def test_load_settings_override(tmp_path: Path) -> None:
    override = tmp_path / "override.yaml"
    override.write_text(
        "model:\n  conf_threshold: 0.6\nui:\n  theme: light\n",
        encoding="utf-8",
    )

    settings = load_settings(override)

    assert settings.model.conf_threshold == 0.6
    assert settings.model.backend == "mock"
    assert settings.ui.theme == "light"


def test_missing_config_raises_readable_error(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="does not exist"):
        load_settings(tmp_path / "missing.yaml")
