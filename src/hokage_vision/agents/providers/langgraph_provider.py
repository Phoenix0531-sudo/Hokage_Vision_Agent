from __future__ import annotations

from typing import Any

from hokage_vision.agents.prompts import REFUSAL_NOTE
from hokage_vision.agents.registry import ToolRegistry
from hokage_vision.agents.safety import refusal_reason
from hokage_vision.agents.state import AgentResponse, ToolCall
from hokage_vision.agents.tools import create_default_tool_registry

_NATIVE_END = "__end__"


class _NativeBuilder:
    """Minimal StateGraph-compatible builder used when langgraph is absent.

    Nodes return the full state dict (single-channel replacement semantics,
    matching ``StateGraph(dict)`` in langgraph), so the native interpreter and
    the real engine behave identically.
    """

    def __init__(self, schema: Any = None) -> None:
        self._nodes: dict[str, Any] = {}
        self._edges: dict[str, str] = {}
        self._conditional: dict[str, tuple[Any, dict[str, str]]] = {}
        self._entry: str | None = None

    def add_node(self, name: str, action: Any) -> _NativeBuilder:
        self._nodes[name] = action
        return self

    def add_edge(self, start: str, end: str) -> _NativeBuilder:
        self._edges[start] = end
        return self

    def add_conditional_edges(
        self, source: str, router: Any, mapping: dict[str, str]
    ) -> _NativeBuilder:
        self._conditional[source] = (router, mapping)
        return self

    def set_entry_point(self, name: str) -> _NativeBuilder:
        self._entry = name
        return self

    def compile(self) -> _NativeCompiled:
        if self._entry is None:
            msg = "Native graph needs an entry point."
            raise ValueError(msg)
        return _NativeCompiled(self._nodes, self._edges, self._conditional, self._entry)


class _NativeCompiled:
    def __init__(
        self,
        nodes: dict[str, Any],
        edges: dict[str, str],
        conditional: dict[str, tuple[Any, dict[str, str]]],
        entry: str,
    ) -> None:
        self._nodes = nodes
        self._edges = edges
        self._conditional = conditional
        self._entry = entry

    def invoke(self, state: dict[str, Any]) -> dict[str, Any]:
        current: str | None = self._entry
        while current is not None and current != _NATIVE_END:
            state = dict(self._nodes[current](state))
            if current in self._conditional:
                router, mapping = self._conditional[current]
                current = mapping[router(state)]
            else:
                current = self._edges.get(current)
        return state


class _NativeEngine:
    """Offline engine with the same surface as the langgraph engine."""

    END = _NATIVE_END
    StateGraph = staticmethod(_NativeBuilder)


class _LangGraphEngine:
    """Engine backed by the real ``langgraph`` package (llm extra)."""

    def __init__(self) -> None:
        from langgraph.graph import END as _END
        from langgraph.graph import StateGraph as _StateGraph

        self.END = _END
        self.StateGraph = _StateGraph


def _default_graph_factory() -> Any:
    try:
        return _LangGraphEngine()
    except ImportError:  # pragma: no cover - depends on the llm extra
        return _NativeEngine()


class LangGraphProvider:
    """Bounded tool-execution loop compiled as a graph state machine.

    The graph topology is ``safety -> plan -> execute -> plan ... END``: the
    safety node refuses out-of-scope tasks before any planning, the plan node
    asks the injected ``planner`` for the next tool call, and the execute node
    runs it through the registry. The loop is bounded by ``max_steps``. When
    the ``llm`` extra is installed the graph compiles on real ``langgraph``;
    otherwise a native interpreter with identical single-channel semantics is
    used, so the provider works offline and in CI without network access.
    """

    def __init__(
        self,
        registry: ToolRegistry | None = None,
        planner: Any = None,
        max_steps: int = 8,
        graph_factory: Any = None,
    ) -> None:
        self.registry = registry or create_default_tool_registry()
        self.planner = planner
        self.max_steps = max_steps
        self._graph_factory = graph_factory or _default_graph_factory

    @property
    def enabled(self) -> bool:
        return self.planner is not None

    def run(self, user_task: str) -> AgentResponse:
        graph = self._build_graph()
        state: dict[str, Any] = {
            "task": user_task,
            "tool_calls": [],
            "errors": [],
            "steps_used": 0,
            "blocked": False,
            "finished": False,
            "pending": None,
        }
        final_state = graph.invoke(state)
        return AgentResponse(
            self._summarize(user_task, final_state),
            list(final_state["tool_calls"]),
            [],
            [],
            list(final_state["errors"]),
        )

    def _build_graph(self) -> Any:
        engine = self._graph_factory()
        builder = engine.StateGraph(dict)
        builder.add_node("safety", self._node_safety)
        builder.add_node("plan", self._node_plan)
        builder.add_node("execute", self._node_execute)
        builder.set_entry_point("safety")
        builder.add_conditional_edges(
            "safety", self._route_safety, {"block": engine.END, "pass": "plan"}
        )
        builder.add_conditional_edges(
            "plan", self._route_plan, {"more": "execute", "done": engine.END}
        )
        builder.add_edge("execute", "plan")
        return builder.compile()

    def _node_safety(self, state: dict[str, Any]) -> dict[str, Any]:
        refused = refusal_reason(state["task"])
        if refused:
            return {
                **state,
                "blocked": True,
                "refusal_message": refused,
                "errors": [REFUSAL_NOTE],
            }
        return {**state, "blocked": False}

    def _route_safety(self, state: dict[str, Any]) -> str:
        return "block" if state.get("blocked") else "pass"

    def _node_plan(self, state: dict[str, Any]) -> dict[str, Any]:
        if state.get("pending") is not None:
            return {**state, "finished": False}
        if int(state.get("steps_used", 0)) >= self.max_steps:
            return {**state, "finished": True, "pending": None}
        if self.planner is None:
            return {**state, "finished": True, "pending": None}
        try:
            decision = self.planner(state["task"], state)
        except Exception as exc:  # planner crash must not loop forever
            errors = [*state["errors"], f"Planner failed: {exc}"]
            return {**state, "finished": True, "pending": None, "errors": errors}
        if decision is None:
            return {**state, "finished": True, "pending": None}
        tool_name, arguments = decision
        return {**state, "finished": False, "pending": {"name": tool_name, "arguments": arguments}}

    def _route_plan(self, state: dict[str, Any]) -> str:
        return "done" if state.get("finished") else "more"

    def _node_execute(self, state: dict[str, Any]) -> dict[str, Any]:
        pending = state.get("pending")
        if not pending:
            return state
        arguments = pending.get("arguments", {})
        call = ToolCall(name=pending["name"], arguments=arguments, status="pending")
        errors = list(state["errors"])
        try:
            call.result = self.registry.call(pending["name"], arguments)
            call.status = "success"
        except Exception as exc:
            call.status = "error"
            call.error = str(exc)
            errors.append(f"Tool {pending['name']} failed: {exc}")
        return {
            **state,
            "tool_calls": [*state["tool_calls"], call],
            "errors": errors,
            "pending": None,
            "steps_used": int(state.get("steps_used", 0)) + 1,
        }

    def _summarize(self, task: str, state: dict[str, Any]) -> str:
        if state.get("blocked"):
            return str(state.get("refusal_message", "Task refused."))
        calls = list(state.get("tool_calls", []))
        if not calls:
            return "I could not map the request to an allowed Hokage Vision Agent tool."
        ok = sum(1 for call in calls if call.status == "success")
        return f"Completed task '{task}' with {ok}/{len(calls)} successful tool calls."
