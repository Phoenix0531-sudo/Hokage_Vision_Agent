from __future__ import annotations

from pathlib import Path
from typing import Any

from hokage_vision.agents.registry import ToolRegistry
from hokage_vision.agents.safety import refusal_reason
from hokage_vision.agents.state import AgentResponse, ToolCall
from hokage_vision.agents.tools import create_default_tool_registry


class RuleBasedAgent:
    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self.registry = registry or create_default_tool_registry()

    def run(self, user_task: str) -> AgentResponse:
        refused = refusal_reason(user_task)
        if refused:
            return AgentResponse(refused, [], [], ["Use project-scoped vision or model tasks."])

        tool_name = self._select_tool(user_task)
        if tool_name is None:
            return AgentResponse(
                "I could not map the request to an allowed Hokage Vision Agent tool.",
                [],
                [],
                [
                    "Try asking for image detection, folder detection, dataset checks, training, or model comparison."
                ],
            )

        arguments = self._arguments_for(tool_name, user_task)
        call = ToolCall(name=tool_name, arguments=arguments, status="pending")
        try:
            call.result = self.registry.call(tool_name, arguments)
            call.status = "success"
        except Exception as exc:  # pragma: no cover - tested through safe paths first
            call.status = "error"
            call.error = str(exc)

        return AgentResponse(
            message=self._message(user_task, call),
            tool_calls=[call],
            artifacts=[],
            suggestions=self._suggestions(tool_name),
        )

    def _select_tool(self, task: str) -> str | None:
        if self._has(task, ["生成报告", "report"]):
            return "generate_report"
        if self._has(task, ["批量识别", "文件夹", "folder"]) or (
            self._has(task, ["检测", "识别"]) and self._first_existing_path(task, want_dir=True)
        ):
            return "detect_folder"
        if self._has(task, ["检测图片", "识别图片", "image"]):
            return "detect_image"
        if self._has(task, ["识别视频", "检测视频", "video"]):
            return "detect_video"
        if self._has(task, ["检查数据集", "validate dataset"]):
            return "validate_dataset"
        if self._has(task, ["创建数据集清单", "manifest"]):
            return "create_dataset_manifest"
        if self._has(task, ["辅助标注"]):
            return "assist_annotation"
        if self._has(task, ["自动标注"]):
            return "auto_label_with_model"
        if self._has(task, ["冒烟训练", "smoke train"]):
            return "smoke_train"
        if self._has(task, ["训练模型", "train model"]):
            return "train_model"
        if self._has(task, ["评估模型", "evaluate"]):
            return "evaluate_model"
        if self._has(task, ["比较权重", "compare"]):
            return "compare_models"
        if self._has(task, ["列出模型", "list models"]):
            return "list_models"
        if self._has(task, ["注册模型", "register model"]):
            return "register_model"
        if self._has(task, ["检查项目", "health"]):
            return "project_health_check"
        return None

    def _arguments_for(self, tool_name: str, task: str) -> dict[str, Any]:
        if tool_name == "detect_image":
            return {
                "path": str(
                    self._first_existing_path(task, want_dir=False)
                    or Path("examples/images/sample.jpg")
                )
            }
        if tool_name == "detect_folder":
            return {
                "path": str(
                    self._first_existing_path(task, want_dir=True) or Path("examples/images")
                )
            }
        if tool_name == "detect_video":
            return {
                "path": str(
                    self._first_existing_path(task, want_dir=False)
                    or Path("examples/videos/demo.mp4")
                )
            }
        if tool_name == "generate_report":
            return {"requested": True, "task": task}
        return {"task": task}

    def _first_existing_path(self, task: str, *, want_dir: bool) -> Path | None:
        for raw in task.replace("，", " ").replace(",", " ").split():
            candidate = Path(raw.strip("\"'"))
            if candidate.exists() and candidate.is_dir() == want_dir:
                return candidate
        return None

    def _message(self, user_task: str, call: ToolCall) -> str:
        if call.status == "success":
            return (
                f"Understood task: {user_task}. Called tool: {call.name}. Result status: success."
            )
        return f"Understood task: {user_task}. Called tool: {call.name}. Error: {call.error}"

    def _suggestions(self, tool_name: str) -> list[str]:
        if tool_name.startswith("detect_"):
            return [
                "Review detections in the GUI or run model comparison after real weights are registered."
            ]
        if tool_name == "train_model":
            return ["Validate the dataset before executing real training."]
        return ["Continue with the next project-scoped workflow step."]

    def _has(self, task: str, keywords: list[str]) -> bool:
        lowered = task.lower()
        return any(keyword.lower() in lowered for keyword in keywords)
