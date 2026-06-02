from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QMainWindow, QTabWidget, QVBoxLayout, QWidget

from hokage_vision.ui.i18n import label
from hokage_vision.ui.theme import stylesheet
from hokage_vision.ui.widgets.agent_chat_panel import AgentChatPanel
from hokage_vision.ui.widgets.batch_detection_panel import BatchDetectionPanel
from hokage_vision.ui.widgets.image_detection_panel import ImageDetectionPanel
from hokage_vision.ui.widgets.settings_panel import SettingsPanel
from hokage_vision.ui.widgets.video_detection_panel import VideoDetectionPanel


class MainWindow(QMainWindow):
    def __init__(self, language: str = "zh-CN", theme: str = "dark") -> None:
        super().__init__()
        self.setWindowTitle("Hokage Vision Agent")
        self.resize(1280, 860)
        self.setStyleSheet(stylesheet(theme))
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.addTab(_overview_panel(), label("home", language))
        self.tabs.addTab(ImageDetectionPanel(), label("image", language))
        self.tabs.addTab(VideoDetectionPanel(), label("video", language))
        self.tabs.addTab(BatchDetectionPanel(), label("batch", language))
        self.tabs.addTab(AgentChatPanel(), label("agent", language))
        self.tabs.addTab(SettingsPanel(), label("settings", language))
        self.tabs.addTab(_about_panel(), label("about", language))


def _overview_panel() -> QWidget:
    panel = QWidget()
    layout = QVBoxLayout(panel)
    layout.setAlignment(Qt.AlignTop)

    card = QFrame()
    card.setObjectName("heroCard")
    card_layout = QVBoxLayout(card)

    title = QLabel("Hokage Vision Agent")
    title.setObjectName("heroTitle")
    subtitle = QLabel("YOLO detection, PySide6 workbench, and safe Agent tool orchestration.")
    subtitle.setObjectName("heroSubtitle")
    body = QLabel(
        "Mock backend is ready for demos and CI. Real weights stay external until "
        "dataset rights, model license, and evaluation metrics are reviewed."
    )
    body.setWordWrap(True)

    card_layout.addWidget(title)
    card_layout.addWidget(subtitle)
    card_layout.addWidget(body)
    layout.addWidget(card)
    return panel


def _about_panel() -> QWidget:
    panel = QWidget()
    layout = QVBoxLayout(panel)
    layout.setAlignment(Qt.AlignTop)

    card = QFrame()
    card.setObjectName("aboutCard")
    card_layout = QVBoxLayout(card)

    title = QLabel("About Hokage Vision Agent")
    title.setObjectName("heroTitle")
    zh = QLabel("这是一个面向学习、研究与作品集展示的火影角色检测 Agent 工作台。")
    en = QLabel("This is a fan-made computer vision and Agent engineering workbench for portfolio demos.")
    note = QLabel(
        "YOLO/CV backends perform detection; the Agent only plans and calls project-scoped tools."
    )
    for item in (zh, en, note):
        item.setWordWrap(True)

    card_layout.addWidget(title)
    card_layout.addWidget(zh)
    card_layout.addWidget(en)
    card_layout.addWidget(note)
    layout.addWidget(card)
    return panel
