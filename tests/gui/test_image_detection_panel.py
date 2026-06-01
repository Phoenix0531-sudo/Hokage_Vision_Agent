from pathlib import Path

import pytest

from hokage_vision.ui.widgets.image_detection_panel import ImageDetectionPanel

pytestmark = pytest.mark.gui


def test_image_detection_panel_detects_sample(qtbot) -> None:
    panel = ImageDetectionPanel()
    qtbot.addWidget(panel)

    panel.detect_path(Path("examples/images/sample.jpg"))

    assert panel.table.rowCount() == 3
