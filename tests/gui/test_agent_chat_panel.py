import pytest

from hokage_vision.ui.widgets.agent_chat_panel import AgentChatPanel

pytestmark = pytest.mark.gui


def test_agent_chat_panel_runs_task(qtbot) -> None:
    panel = AgentChatPanel()
    qtbot.addWidget(panel)

    panel.input.setText("检测 examples/images 里的图片")
    panel.run_task()

    assert "detect_folder" in panel.history.toPlainText()
