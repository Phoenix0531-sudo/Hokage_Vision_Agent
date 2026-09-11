"""Offline unit tests for the LLM agent providers (no network access)."""

from __future__ import annotations

from typing import Any

import pytest

from hokage_vision.agents.orchestrator import SUPPORTED_AGENT_PROVIDERS, create_agent
from hokage_vision.agents.providers.langgraph_provider import (
    LangGraphProvider,
    _NativeEngine,
)
from hokage_vision.agents.providers.openai_provider import OpenAIProvider

# ---------------------------------------------------------------------------
# Fake OpenAI-compatible client
# ---------------------------------------------------------------------------


class _FakeFunction:
    def __init__(self, name: str, arguments: str) -> None:
        self.name = name
        self.arguments = arguments


class _FakeToolCall:
    def __init__(self, name: str, arguments: str) -> None:
        self.function = _FakeFunction(name, arguments)


class _FakeMessage:
    def __init__(
        self, tool_calls: list[_FakeToolCall] | None = None, content: str | None = None
    ) -> None:
        self.tool_calls = tool_calls
        self.content = content


class _FakeChoice:
    def __init__(self, message: _FakeMessage) -> None:
        self.message = message


class _FakeCompletion:
    def __init__(self, message: _FakeMessage) -> None:
        self.choices = [_FakeChoice(message)]


class _FakeClient:
    """Scripted OpenAI-compatible client exposing top-level create()."""

    def __init__(self, completions: list[_FakeCompletion]) -> None:
        self._completions = list(completions)
        self.requests: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> _FakeCompletion:
        self.requests.append(kwargs)
        return self._completions.pop(0)


# ---------------------------------------------------------------------------
# create_agent factory
# ---------------------------------------------------------------------------


def test_create_agent_builds_rule_based_by_default() -> None:
    from hokage_vision.agents.providers.rule_based import RuleBasedAgent

    agent = create_agent()
    assert isinstance(agent, RuleBasedAgent)


def test_create_agent_rejects_unknown_provider() -> None:
    with pytest.raises(ValueError, match="Unknown agent provider"):
        create_agent("gpt-999")


def test_supported_agent_providers_list() -> None:
    assert SUPPORTED_AGENT_PROVIDERS == ("rule_based", "openai", "langgraph")


# ---------------------------------------------------------------------------
# OpenAIProvider
# ---------------------------------------------------------------------------


def _planned_completion(name: str, arguments: str) -> _FakeCompletion:
    return _FakeCompletion(_FakeMessage(tool_calls=[_FakeToolCall(name, arguments)]))


def _final_completion(text: str) -> _FakeCompletion:
    return _FakeCompletion(_FakeMessage(content=text))


def test_openai_provider_refuses_out_of_scope_before_any_llm_call() -> None:
    completions = _FakeClient([])
    provider = OpenAIProvider(client=completions)

    response = provider.run("帮我写小说")

    assert response.tool_calls == []
    assert "refused" in response.message
    assert completions.requests == []


def test_openai_provider_reports_missing_client() -> None:
    provider = OpenAIProvider()

    response = provider.run("检测这张图片")

    assert response.tool_calls == []
    assert "not configured" in response.message
    assert provider.enabled is False


def test_openai_provider_executes_tool_then_summarizes() -> None:
    completions = _FakeClient(
        [
            _planned_completion("list_models", "{}"),
            _final_completion("You have no registered models yet."),
        ]
    )
    provider = OpenAIProvider(client=completions)

    response = provider.run("列出已注册的模型")

    assert [(call.name, call.status) for call in response.tool_calls] == [
        ("list_models", "success")
    ]
    assert response.message == "You have no registered models yet."
    # Planning requests carry the function schemas for tool calling.
    assert all("tools" in req for req in completions.requests)
    # The first planning turn carried tool calls; the second one was pure text
    # (message.content) which the provider surfaces as the final answer.


def test_openai_provider_invalid_json_arguments_become_planning_error() -> None:
    completions = _FakeClient([_planned_completion("detect_image", "{not json")])
    provider = OpenAIProvider(client=completions)

    response = provider.run("检测一张图片")

    assert response.tool_calls == []
    assert "LLM planning failed" in response.errors[0]


def test_openai_provider_records_unknown_tool_as_failed_call() -> None:
    completions = _FakeClient([_planned_completion("delete_system_files", "{}")])
    provider = OpenAIProvider(client=completions)

    response = provider.run("do something impossible")

    assert len(response.tool_calls) == 1
    assert response.tool_calls[0].status == "error"
    assert response.errors


def test_openai_provider_max_steps_bounds_the_loop() -> None:
    scripted = [_planned_completion("list_models", "{}") for _ in range(2)]
    completions = _FakeClient(scripted)
    provider = OpenAIProvider(client=completions, max_steps=2)

    response = provider.run("keep listing models")

    assert len(response.tool_calls) == 2
    # Two planning turns consumed the scripted tool calls; the third request
    # is the post-loop final summary over the tool transcript.
    assert len(completions.requests) == 3
    assert [m["role"] for m in completions.requests[2]["messages"]][:2] == ["system", "user"]
    assert "max planning steps" in response.message


# ---------------------------------------------------------------------------
# LangGraphProvider
# ---------------------------------------------------------------------------


def test_langgraph_native_engine_runs_planner_loop() -> None:
    def planner(task: str, state: dict[str, Any]) -> tuple[str, dict[str, Any]] | None:
        if state["tool_calls"]:
            return None
        return ("list_models", {})

    provider = LangGraphProvider(planner=planner, graph_factory=_NativeEngine)

    response = provider.run("列出已注册的模型")

    assert [(call.name, call.status) for call in response.tool_calls] == [
        ("list_models", "success")
    ]
    assert "1/1 successful" in response.message


def test_langgraph_native_engine_refuses_out_of_scope_task() -> None:
    provider = LangGraphProvider(
        planner=lambda *_: ("list_models", {}), graph_factory=_NativeEngine
    )

    response = provider.run("帮我查天气")

    assert response.tool_calls == []
    assert "refused" in response.message or "refus" in response.message.lower()


def test_langgraph_planner_crash_terminates_loop_with_error() -> None:
    def broken_planner(task: str, state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        msg = "planner exploded"
        raise RuntimeError(msg)

    provider = LangGraphProvider(planner=broken_planner, graph_factory=_NativeEngine)

    response = provider.run("any task")

    assert response.tool_calls == []
    assert "Planner failed" in response.errors[0]


def test_langgraph_max_steps_bounds_repeated_calls() -> None:
    provider = LangGraphProvider(
        planner=lambda *_: ("list_models", {}), max_steps=3, graph_factory=_NativeEngine
    )

    response = provider.run("keep listing")

    assert len(response.tool_calls) == 3
    assert all(call.status == "success" for call in response.tool_calls)


def test_langgraph_real_engine_matches_native_semantics() -> None:
    pytest.importorskip("langgraph")

    def planner(task: str, state: dict[str, Any]) -> tuple[str, dict[str, Any]] | None:
        if state["tool_calls"]:
            return None
        return ("list_models", {})

    provider = LangGraphProvider(planner=planner)

    response = provider.run("列出已注册的模型")

    assert [(call.name, call.status) for call in response.tool_calls] == [
        ("list_models", "success")
    ]


def test_langgraph_disabled_without_planner() -> None:
    provider = LangGraphProvider(graph_factory=_NativeEngine)

    response = provider.run("detect an image")

    assert response.tool_calls == []
    assert provider.enabled is False
