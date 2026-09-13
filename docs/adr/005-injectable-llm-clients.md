# ADR-005: Injectable LLM clients for offline-testable providers

**Status:** Accepted · **Date:** 2026-09-11 (commit `74d51f5`)

## Context

Agent providers that talk to OpenAI/LangGraph normally resist unit
testing: tests either hit the network (flaky, costly, key-requiring) or
skip the provider entirely — which is exactly what the placeholder
implementations had done.

## Decision

Both providers take an **injectable client**:

- `OpenAIProvider(client=...)` — any object exposing `.create(...)`
  with chat-completions semantics. The real OpenAI SDK is only built
  lazily when `OPENAI_API_KEY` is set.
- `LangGraphProvider` goes further: the whole StateGraph is built via
  an injectable `graph_factory`, and a native fallback engine
  (`_NativeEngine`) re-implements the tiny graph subset needed, so the
  provider runs and is testable *without the `llm` extra installed*.

Tests script fake clients (see `_FakeClient` in
`tests/unit/test_llm_providers.py`) — 15 tests covering refusal,
missing client, tool-then-summarize loops, invalid JSON, unknown
tools, and `max_steps` bounds, all offline.

## Consequences

- ✅ CI installs the `llm` extra and runs the real-langgraph path via
  `pytest.importorskip`, while the fake-client path works everywhere.
- ✅ Prompt/loop regressions are caught by assertions on the exact
  sequence of `.create(...)` calls.
- ⚠️ The fake must mirror the real client's shape; the contract is
  documented in the provider docstrings (`.create` at the top level,
  not nested under `chat.completions`).
- ⚠️ Real-network behavior (retries, rate limits) remains
  untested by design — that boundary is the SDK's job.
