from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any]
    status: str
    result: dict[str, Any] | None = None
    error: str | None = None


@dataclass
class AgentState:
    user_task: str
    selected_tools: list[str]
    artifacts: list[Path]
    messages: list[dict[str, str]]
    last_result: dict[str, Any] | None = None
    errors: list[str] = field(default_factory=list)


@dataclass
class AgentResponse:
    message: str
    tool_calls: list[ToolCall]
    artifacts: list[Path]
    suggestions: list[str]
