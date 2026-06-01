from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class VideoDetectionPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel("Video detection uses local video files; camera input is not supported.")
        )
        layout.addWidget(QPushButton("Select Video"))
        layout.addWidget(QPushButton("Start"))
        layout.addWidget(QPushButton("Pause"))
        layout.addWidget(QPushButton("Stop"))
