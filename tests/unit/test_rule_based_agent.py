"""Behavior tests for RuleBasedAgent tool selection and arguments."""

from __future__ import annotations

from pathlib import Path

from hokage_vision.agents.orchestrator import RuleBasedAgent
from hokage_vision.agents.state import AgentResponse


def test_unmapped_task_returns_guidance() -> None:
    response = RuleBasedAgent().run("今天天气怎么样")
    assert isinstance(response, AgentResponse)
    assert not response.tool_calls
    assert "could not map" in response.message


def test_detect_image_with_existing_file_argument() -> None:
    response = RuleBasedAgent().run("检测图片 examples/images/sample.jpg")
    call = response.tool_calls[0]
    assert call.name == "detect_image"
    assert call.status == "success"
    assert call.arguments["path"].endswith("sample.jpg")


def test_detect_folder_keyword_defaults_to_examples() -> None:
    response = RuleBasedAgent().run("批量识别所有目标")
    call = response.tool_calls[0]
    assert call.name == "detect_folder"
    assert call.arguments["path"] == str(Path("examples/images"))


def test_detect_folder_uses_first_existing_dir() -> None:
    response = RuleBasedAgent().run("批量识别 configs 文件夹里的目标")
    assert response.tool_calls[0].arguments["path"] == "configs"


def test_detect_folder_uses_examples_fallback_on_windows_separators(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    response = RuleBasedAgent().run("批量识别所有目标")
    assert response.tool_calls[0].arguments["path"] == str(Path("examples/images"))


def test_detect_video_argument() -> None:
    response = RuleBasedAgent().run("检测视频 examples/videos/demo.mp4")
    call = response.tool_calls[0]
    assert call.name == "detect_video"
    assert call.arguments["path"].endswith("demo.mp4")


def test_generate_report_task() -> None:
    response = RuleBasedAgent().run("生成报告")
    call = response.tool_calls[0]
    assert call.name == "generate_report"
    assert call.arguments == {"requested": True, "task": "生成报告"}


def test_validate_dataset_keyword() -> None:
    response = RuleBasedAgent().run("检查数据集 configs/dataset.example.yaml")
    assert response.tool_calls[0].name == "validate_dataset"
    assert "检查数据集" in response.message


def test_manifest_keyword(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    response = RuleBasedAgent().run("创建数据集清单")
    assert response.tool_calls[0].name == "create_dataset_manifest"


def test_assist_annotation_keyword(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    response = RuleBasedAgent().run("辅助标注 待标注图片")
    assert response.tool_calls[0].name == "assist_annotation"


def test_auto_label_keyword(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    response = RuleBasedAgent().run("自动标注 待标注图片")
    assert response.tool_calls[0].name == "auto_label_with_model"
    assert response.tool_calls[0].status == "success"


def test_smoke_train_keyword() -> None:
    response = RuleBasedAgent().run("冒烟训练")
    assert response.tool_calls[0].name == "smoke_train"
    assert response.tool_calls[0].status == "success"


def test_evaluate_keyword() -> None:
    response = RuleBasedAgent().run("评估模型 mock")
    assert response.tool_calls[0].name == "evaluate_model"
    assert response.tool_calls[0].status == "success"


def test_compare_keyword() -> None:
    response = RuleBasedAgent().run("比较权重")
    assert response.tool_calls[0].name == "compare_models"


def test_list_models_keyword() -> None:
    response = RuleBasedAgent().run("列出模型")
    assert response.tool_calls[0].name == "list_models"
    assert response.tool_calls[0].status == "success"


def test_register_model_keyword() -> None:
    response = RuleBasedAgent().run("注册模型")
    assert response.tool_calls[0].name == "register_model"


def test_health_keyword() -> None:
    response = RuleBasedAgent().run("检查项目 health")
    call = response.tool_calls[0]
    assert call.name == "project_health_check"
    assert call.status == "success"
    assert call.result["status"] == "ok"


def test_detect_suggestions_branch() -> None:
    response = RuleBasedAgent().run("识别图片 examples/images/sample.jpg")
    assert "model comparison" in response.suggestions[0]


def test_error_message_branch() -> None:
    # Directly exercise the error-message branch via a failing injected tool.
    agent = RuleBasedAgent()

    def boom(_args: dict) -> dict:
        raise RuntimeError("boom")

    agent.registry.register("boom", "Exploding tool", boom)
    from hokage_vision.agents.state import ToolCall

    call = ToolCall(name="boom", arguments={}, status="pending")
    try:
        call.result = agent.registry.call("boom", {})
        call.status = "success"
    except Exception as exc:  # noqa: BLE001
        call.status = "error"
        call.error = str(exc)
    message = agent._message("触发 boom", call)
    assert message.startswith("Understood task: 触发 boom.")
    assert "Error" in message and "boom" in message


def test_train_model_suggestion_branch() -> None:
    response = RuleBasedAgent().run("训练模型 train model")
    assert response.tool_calls[0].name == "train_model"
    assert "Validate the dataset" in response.suggestions[0]
