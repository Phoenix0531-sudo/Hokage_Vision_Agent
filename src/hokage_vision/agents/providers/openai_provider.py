from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Protocol

from hokage_vision.agents.prompts import PLANNING_SYSTEM_PROMPT, REFUSAL_NOTE
from hokage_vision.agents.registry import ToolRegistry
from hokage_vision.agents.safety import refusal_reason
from hokage_vision.agents.state import AgentResponse, ToolCall
from hokage_vision.agents.tools import create_default_tool_registry


class ChatCompletion(Protocol):
    """Minimal chat-completion interface; the OpenAI SDK client satisfies it."""

    def create(self, **kwargs: Any) -> Any:  # pragma: no cover - protocol marker
        ...


@dataclass(frozen=True)
class ToolDecision:
    """One LLM planning decision: a tool call or a final text answer."""

    tool_name: str | None
    arguments: dict[str, Any] = field(default_factory=dict)
    text: str = ""


class OpenAIProvider:
    """Function-calling agent backed by an allowlisted OpenAI chat model.

    The planning loop is deliberately simple and fully testable offline: any
    object exposing ``chat.completions.create`` can be injected as ``client``,
    which keeps CI free of network access. The provider refuses out-of-scope
    tasks before any LLM call and never executes tools outside the registry.
    """

    def __init__(
        self,
        registry: ToolRegistry | None = None,
        client: ChatCompletion | None = None,
        model: str = "gpt-4o-mini",
        max_steps: int = 8,
    ) -> None:
        self.registry = registry or create_default_tool_registry()
        self.client = client
        self.model = model
        self.max_steps = max_steps

    @property
    def enabled(self) -> bool:
        return self.client is not None

    def _request_tool_calls(self, task: str) -> tuple[list[Any], str]:
        assert self.client is not None
        completion = self.client.create(
            model=self.model,
            messages=[
                {"role": "system", "content": PLANNING_SYSTEM_PROMPT},
                {"role": "user", "content": task},
            ],
            tools=self.registry.list_function_schemas(),
            tool_choice="auto",
        )
        message = completion.choices[0].message
        return list(message.tool_calls or []), str(message.content or "")

    def _request_final_summary(self, task: str, transcript: list[dict[str, Any]]) -> str:
        assert self.client is not None
        completion = self.client.create(
            model=self.model,
            messages=[
                {"role": "system", "content": PLANNING_SYSTEM_PROMPT},
                {"role": "user", "content": task},
                *transcript,
            ],
        )
        return str(completion.choices[0].message.content or "")

    def plan(self, task: str) -> ToolDecision:
        """Ask the LLM for the next single tool call (or a refusal/summary)."""
        if self.client is None:
            msg = "OpenAIProvider is disabled: no client configured."
            raise RuntimeError(msg)
        calls, content = self._request_tool_calls(task)
        if not calls:
            return ToolDecision(
                tool_name=None,
                text=content or "No tool was selected for this task.",
            )
        first = calls[0]
        try:
            arguments = json.loads(first.function.arguments or "{}")
        except json.JSONDecodeError as exc:
            msg = f"LLM returned invalid tool arguments: {exc}"
            raise RuntimeError(msg) from exc
        if not isinstance(arguments, dict):
            msg = "LLM tool arguments must decode to a JSON object."
            raise RuntimeError(msg)
        return ToolDecision(tool_name=first.function.name, arguments=arguments)

    def run(self, user_task: str) -> AgentResponse:
        refused = refusal_reason(user_task)
        if refused:
            return AgentResponse(refused, [], [], [REFUSAL_NOTE])

        if self.client is None:
            return AgentResponse(
                "LLM provider is not configured. Set the provider client before running.",
                [],
                [],
                [],
                ["Install the llm extra and configure an OpenAI-compatible client."],
            )

        tool_calls: list[ToolCall] = []
        errors: list[str] = []
        transcript: list[dict[str, Any]] = []

        for _ in range(self.max_steps):
            try:
                decision = self.plan(user_task)
            except Exception as exc:
                errors.append(f"LLM planning failed: {exc}")
                return AgentResponse(
                    "Agent stopped after an LLM planning error.", tool_calls, [], [], errors
                )

            if decision.tool_name is None:
                return AgentResponse(decision.text or "Task complete.", tool_calls, [], [], errors)

            call = ToolCall(name=decision.tool_name, arguments=decision.arguments, status="pending")
            try:
                call.result = self.registry.call(decision.tool_name, decision.arguments)
                call.status = "success"
                transcript.append(
                    {
                        "role": "assistant",
                        "content": json.dumps(
                            {"tool": decision.tool_name, "result_preview": _preview(call.result)}
                        ),
                    }
                )
            except Exception as exc:
                call.status = "error"
                call.error = str(exc)
                errors.append(f"Tool {decision.tool_name} failed: {exc}")
            tool_calls.append(call)

        summary = ""
        if not errors:
            try:
                summary = self._request_final_summary(user_task, transcript)
            except Exception as exc:
                errors.append(f"Final summary failed: {exc}")
        return AgentResponse(
            summary or "Reached max planning steps without a final summary.",
            tool_calls,
            [],
            [],
            errors,
        )


def _preview(result: dict[str, Any], limit: int = 400) -> dict[str, Any]:
    text = json.dumps(result, ensure_ascii=False, default=str)
    if len(text) <= limit:
        return result
    return {"truncated": True, "preview": text[:limit]}
