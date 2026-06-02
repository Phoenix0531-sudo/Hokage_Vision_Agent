from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from hokage_vision.ui.main_window import MainWindow
from hokage_vision.ui.theme import apply_application_font


def run_app() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    apply_application_font(app)
    window = MainWindow()
    window.show()
    return app.exec()
