from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

ToolHandler = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    handler: ToolHandler


class ToolRegistry:
    def __init__(self, allowed_tools: list[str] | None = None) -> None:
        self._tools: dict[str, Tool] = {}
        self.allowed_tools = set(allowed_tools or [])

    def register(self, name: str, description: str, handler: ToolHandler) -> None:
        self._tools[name] = Tool(name=name, description=description, handler=handler)

    def list_tools(self) -> list[str]:
        return sorted(self._tools)

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            msg = f"Tool is not registered: {name}"
            raise KeyError(msg)
        if self.allowed_tools and name not in self.allowed_tools:
            msg = f"Tool is not allowed: {name}"
            raise PermissionError(msg)
        return self._tools[name]

    def call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        return self.get(name).handler(arguments)
