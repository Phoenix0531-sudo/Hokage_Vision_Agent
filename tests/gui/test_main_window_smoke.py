import pytest
from PySide6.QtWidgets import QLabel

from hokage_vision.ui.main_window import MainWindow

pytestmark = pytest.mark.gui


def test_main_window_smoke(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.windowTitle() == "Hokage Vision Agent"
    assert window.tabs.count() == 7
    about_text = "\n".join(label.text() for label in window.tabs.widget(6).findChildren(QLabel))
    assert "火影风格动漫角色目标检测工作台" in about_text
    assert "YOLO-powered anime character detection workbench" in about_text
