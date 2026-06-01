import pytest

from hokage_vision.ui.main_window import MainWindow

pytestmark = pytest.mark.gui


def test_main_window_smoke(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.windowTitle() == "Hokage Vision Agent"
    assert window.tabs.count() == 7
