"""Offline LLM-agent demo: function calling with a scripted LLM client.

This demo runs the *real* :class:`OpenAIProvider` planning loop end to end —
safety check, tool-schema advertisement, tool execution, result feedback, and
final summarization — without any API key or network access. The "LLM" is a
small scripted client that plays the model, so the terminal shows the full
agent loop exactly as it runs against a live OpenAI-compatible endpoint.

Scenarios
---------
1. Vision task: the scripted model calls ``detect_image`` on the bundled demo
   asset, then summarizes the detection result.
2. Tool error: the model calls a nonexistent tool; the agent records the
   error and keeps the loop safe.
3. Safety refusal: an out-of-scope task is refused before any LLM call.

Run::

    python examples/agent_demo.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hokage_vision.agents.providers.openai_provider import OpenAIProvider  # noqa: E402


class ScriptedToolCall:
    """Mimics ``openai.types.chat.tool_call`` for the scripted demo."""

    def __init__(self, name: str, arguments: str) -> None:
        self.function = type("Function", (), {"name": name, "arguments": arguments})()


class ScriptedChoice:
    """Mimics ``openai.types.chat.chat_completion.Choice``."""

    def __init__(self, message: Any) -> None:
        self.message = message


class ScriptedCompletion:
    """Mimics ``openai.types.chat.ChatCompletion``."""

    def __init__(self, choices: list[Any]) -> None:
        self.choices = choices


def _assistant(tool_calls: list[ScriptedToolCall] | None = None, content: str = "") -> Any:
    return type("Message", (), {"tool_calls": tool_calls, "content": content})()


class ScriptedClient:
    """A scripted chat-completions client: no key, no network, full loop.

    It receives the same kwargs a real OpenAI SDK client would (model,
    messages, tools, tool_choice) and prints them, so the demo shows exactly
    what the agent sends to the LLM and how the loop evolves turn by turn.
    """

    def __init__(self, script: list[dict[str, Any]]) -> None:
        # Each entry: {"tool": (name, args-dict)} or {"text": "..."}
        self.script = script
        self.turn = 0
        self.seen_tools: list[str] = []
        self.saw_tools_kwarg: list[bool] = []

    def create(self, **kwargs: Any) -> ScriptedCompletion:  # noqa: C901
        step = self.script[min(self.turn, len(self.script) - 1)]
        self.turn += 1

        tools = kwargs.get("tools")
        self.saw_tools_kwarg.append(bool(tools))
        if tools:
            self.seen_tools = [t["function"]["name"] for t in tools]

        if "tool" in step:
            name, arguments = step["tool"]
            tool_calls = [ScriptedToolCall(name, json.dumps(arguments))]
            message = _assistant(tool_calls=tool_calls)
        else:
            message = _assistant(content=step["text"])
        return ScriptedCompletion([ScriptedChoice(message)])


def _hr(title: str) -> None:
    print(f"\n{'=' * 62}\n{title}\n{'=' * 62}")


def _describe_call(call: Any) -> str:
    args = json.dumps(call.arguments, ensure_ascii=False)
    return f"  tool={call.name}  arguments={args}"


def run_scenario(title: str, task: str, script: list[dict[str, Any]]) -> OpenAIProvider:
    _hr(title)
    print(f"User task: {task!r}")
    client = ScriptedClient(script)
    agent = OpenAIProvider(client=client, model="demo-scripted-model", max_steps=4)
    print(f"Advertised tool schemas: {len(agent.registry.list_function_schemas())}")

    response = agent.run(task)

    print("\n-- Agent transcript --")
    print(f"LLM turns used: {client.turn}")
    print(
        f"Tools seen by the LLM: {client.seen_tools[:4]}{' ...' if len(client.seen_tools) > 4 else ''}"
    )
    for call in response.tool_calls:
        print(_describe_call(call))
        result = call.result if call.result is not None else {}
        preview = json.dumps(result, ensure_ascii=False, default=str)
        print(f"  -> status={call.status} result={preview[:180]}")
    if response.suggestions:
        print(f"Suggestions: {response.suggestions}")
    if response.errors:
        print(f"Errors: {response.errors}")
    print(f"\nFinal message:\n{response.message}")
    return agent


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    demo_image = repo_root / "assets" / "demo" / "dataset" / "images" / "val" / "naruto_000.jpg"
    if not demo_image.exists():
        # Fall back to the in-repo sample image when demo assets are absent.
        demo_image = repo_root / "examples" / "images" / "sample.jpg"

    run_scenario(
        title="Scenario 1 — vision task: LLM picks detect_image, then summarizes",
        task=f"帮我检测这张图片里的目标: {demo_image}",
        script=[
            {"tool": ("detect_image", {"path": str(demo_image)})},
            {"text": "检测完成: 图片里有一个 obito 目标， 置信度 0.91, 边界框清晰。"},
        ],
    )

    run_scenario(
        title="Scenario 2 — safety: unknown tool is rejected, agent records the error",
        task="检测这张图片并总结",
        script=[
            {"tool": ("shell_exec", {"command": "rm -rf /"})},
            {"tool": ("detect_image", {"path": str(demo_image)})},
            {"text": "检测完成: 图片里有一个 obito 目标， 置信度 0.91。"},
        ],
    )

    run_scenario(
        title="Scenario 3 — refusal: out-of-scope task never reaches the LLM",
        task="帮我写小说， 主角是火影忍者",
        script=[{"text": "should never be reached"}],
    )

    _hr("Demo complete")
    print("The same loop runs against any OpenAI-compatible endpoint by")
    print("installing the llm extra and passing a real client:")
    print("    pip install -e '.[llm]'   # openai + langgraph")
    print("    agent = OpenAIProvider(client=openai.OpenAI(), model='gpt-4o-mini')")


if __name__ == "__main__":
    main()
