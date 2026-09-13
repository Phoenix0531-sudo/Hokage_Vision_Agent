# ADR-004: Agent = tool registry + safety layer, not model output

**Status:** Accepted · **Date:** 2026-06, hardened 2026-09 (commits `5bb1a3f`, `74d51f5`)

## Context

The project is named "…Agent", but an LLM free-generating JSON or text
"results" would be unverifiable and unsafe: it could invent labels,
claim detections that never ran, or touch paths it should not. At the
same time the agent must be useful without any API key.

## Decision

The agent layer is a **`ToolRegistry` of typed, JSON-schema'd tools**
wrapping the *same* services the CLI/API use, plus a **safety layer**
(`agents/safety.py`) that refuses out-of-scope tasks *before any model
call*. An LLM (OpenAI or LangGraph provider) can only *choose and
parameterize* tool calls from `list_function_schemas()`; it never
produces detection content itself. The default provider is a
deterministic rule-based matcher needing no network.

## Consequences

- ✅ "Agent refused the task" is testable and reproducible
  (`tests/unit/test_llm_providers.py`).
- ✅ One implementation of `detect_image` etc. serves CLI, API, GUI,
  and agent — no parallel code paths to drift.
- ✅ `AgentResponse` carries `tool_calls` and `errors`, so every run is
  auditable after the fact.
- ⚠️ The agent is only as capable as its registered tools; adding a
  capability means writing a tool (which is the point, but it is
  work).
