import pytest

from hokage_vision.ui.widgets.settings_panel import SettingsPanel

pytestmark = pytest.mark.gui


def test_settings_panel_defaults(qtbot) -> None:
    panel = SettingsPanel()
    qtbot.addWidget(panel)

    assert panel.backend.currentText() == "mock"
    assert panel.image_size.value() == 640
