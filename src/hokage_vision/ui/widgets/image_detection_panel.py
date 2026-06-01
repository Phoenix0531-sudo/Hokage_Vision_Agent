from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QLabel, QPushButton, QSplitter, QVBoxLayout, QWidget

from hokage_vision.ui.widgets.result_table import ResultTable
from hokage_vision.ui.widgets.statistics_panel import StatisticsPanel
from hokage_vision.vision.backends.mock import MockBackend
from hokage_vision.vision.inference import InferenceService
from hokage_vision.vision.rendering import render_detections


class ImageDetectionPanel(QWidget):
    def __init__(self, service: InferenceService | None = None) -> None:
        super().__init__()
        self.setAcceptDrops(True)
        self.service = service or InferenceService(MockBackend())
        self.original = QLabel("Original image")
        self.original.setAlignment(Qt.AlignCenter)
        self.result_image = QLabel("Detection result")
        self.result_image.setAlignment(Qt.AlignCenter)
        self.table = ResultTable()
        self.stats = StatisticsPanel()
        self.button = QPushButton("Select Image")
        self.button.clicked.connect(self.select_image)

        image_split = QSplitter()
        image_split.addWidget(self.original)
        image_split.addWidget(self.result_image)

        layout = QVBoxLayout(self)
        layout.addWidget(self.button)
        layout.addWidget(image_split)
        layout.addWidget(self.table)
        layout.addWidget(self.stats)

    def select_image(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select image", "examples/images", "Images (*.jpg *.jpeg *.png)"
        )
        if path:
            self.detect_path(Path(path))

    def detect_path(self, image_path: Path) -> None:
        result = self.service.detect_image(image_path)
        rendered = render_detections(image_path, result)
        preview_path = Path("runs/gui-preview.jpg")
        preview_path.parent.mkdir(parents=True, exist_ok=True)
        rendered.save(preview_path)
        self.original.setPixmap(QPixmap(str(image_path)).scaled(360, 240, Qt.KeepAspectRatio))
        self.result_image.setPixmap(QPixmap(str(preview_path)).scaled(360, 240, Qt.KeepAspectRatio))
        self.table.set_result(result)
        self.stats.set_result(result)

    def dragEnterEvent(self, event) -> None:  # noqa: N802
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event) -> None:  # noqa: N802
        urls = event.mimeData().urls()
        if urls:
            self.detect_path(Path(urls[0].toLocalFile()))
