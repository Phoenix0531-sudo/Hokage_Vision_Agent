DARK_STYLE = """
QWidget {
  background: #111111;
  color: #f7f2e8;
  font-size: 13px;
}
QMainWindow {
  background: #111111;
}
QTabWidget::pane {
  border: 1px solid #3b2417;
  border-top: 3px solid #f97316;
}
QTabBar::tab {
  background: #1a1715;
  color: #d6d3d1;
  padding: 9px 14px;
  border: 1px solid #3b2417;
  border-bottom: 0;
}
QTabBar::tab:selected {
  background: #2a160b;
  color: #ffedd5;
  border-top: 3px solid #f97316;
}
QLabel#heroTitle {
  color: #ffedd5;
  font-size: 28px;
  font-weight: 700;
}
QLabel#heroSubtitle {
  color: #fbbf24;
  font-size: 15px;
}
QFrame#heroCard, QFrame#aboutCard {
  background: #1a1715;
  border: 1px solid #7c2d12;
  border-radius: 8px;
}
QPushButton {
  background: #f97316;
  color: #111111;
  border: 0;
  padding: 8px 12px;
  border-radius: 6px;
  font-weight: 600;
}
QPushButton:hover {
  background: #fb923c;
}
QPushButton:disabled {
  background: #57534e;
  color: #d6d3d1;
}
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QDoubleSpinBox, QSpinBox {
  background: #1c1917;
  border: 1px solid #7c2d12;
  color: #fff7ed;
  padding: 6px;
  border-radius: 6px;
}
QTableWidget {
  background: #14110f;
  gridline-color: #3b2417;
  alternate-background-color: #1c1917;
}
QHeaderView::section {
  background: #2a160b;
  color: #ffedd5;
  border: 1px solid #7c2d12;
  padding: 5px;
}
QProgressBar {
  border: 1px solid #7c2d12;
  border-radius: 6px;
  text-align: center;
}
QProgressBar::chunk {
  background: #06b6d4;
  border-radius: 5px;
}
"""

LIGHT_STYLE = """
QWidget {
  background: #fff7ed;
  color: #1c1917;
  font-size: 13px;
}
QTabWidget::pane {
  border: 1px solid #fed7aa;
  border-top: 3px solid #f97316;
}
QTabBar::tab {
  background: #ffedd5;
  padding: 9px 14px;
  border: 1px solid #fed7aa;
  border-bottom: 0;
}
QTabBar::tab:selected {
  background: white;
  color: #9a3412;
  border-top: 3px solid #f97316;
}
QLabel#heroTitle {
  color: #7c2d12;
  font-size: 28px;
  font-weight: 700;
}
QLabel#heroSubtitle {
  color: #0e7490;
  font-size: 15px;
}
QFrame#heroCard, QFrame#aboutCard {
  background: white;
  border: 1px solid #fdba74;
  border-radius: 8px;
}
QPushButton {
  background: #f97316;
  color: #111111;
  border: 0;
  padding: 8px 12px;
  border-radius: 6px;
  font-weight: 600;
}
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QDoubleSpinBox, QSpinBox {
  background: white;
  border: 1px solid #fdba74;
  padding: 6px;
  border-radius: 6px;
}
"""


def stylesheet(theme: str) -> str:
    return LIGHT_STYLE if theme == "light" else DARK_STYLE
