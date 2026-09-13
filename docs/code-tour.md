# Code tour

Eight short stops through the codebase — the places a reviewer actually wants
to read. Each stop names the file, the anchor symbol, and why it matters.
All paths are relative to the repo root and permalinked against the latest
release tag where possible; browse them on GitHub at
`src/hokage_vision/...`.

## Stop 1 — The agent planning loop (the heart of the project)

**`src/hokage_vision/agents/providers/openai_provider.py`** — `OpenAIProvider.run`

A complete function-calling loop in ~70 lines: safety check → advertise tool
schemas → execute the chosen tool → feed the result back as a message →
repeat until the model answers in text or `max_steps` is hit. The client is
*injectable*, so the identical loop is unit-tested offline with a scripted
client (`tests/unit/test_llm_providers.py`) and runs against any
OpenAI-compatible endpoint in production. See
[`examples/agent_demo.py`](../examples/agent_demo.py) for a runnable,
no-API-key walkthrough of this loop.

## Stop 2 — Safety before the LLM

**`src/hokage_vision/agents/safety.py`** — `refusal_reason`

Out-of-scope tasks are refused *before any LLM call is made* — no tokens
burned, no prompt-injection surface. `OpenAIProvider.run` and
`LangGraphProvider.run` both start with this gate. The refusal message is
deterministic and testable; the tests assert that the scripted "LLM" sees
zero requests in refused scenarios.

## Stop 3 — Tool registry with real JSON Schemas

**`src/hokage_vision/agents/registry.py`** — `ToolRegistry.list_function_schemas`

Each of the 15 tools carries an explicit OpenAI-style function schema
(`src/hokage_vision/agents/tools.py`), so the LLM sees typed parameters, not
stringly-typed hints. The registry is the single security boundary: tools
are allowlisted at registration, and any name the model invents (say,
`shell_exec`) is rejected with `Tool is not registered`. The
[offline agent demo](../examples/agent_demo.py) demonstrates exactly this
rejection and recovery.

## Stop 4 — The backend factory

**`src/hokage_vision/vision/backends/factory.py`** — `create_backend`

Mock / Ultralytics / legacy YOLOv5 backends are interchangeable behind one
constructor call, which is what lets the whole test suite run without
weights while the integration tests run real ONNX inference. The GUI, CLI,
and API never import a backend class directly — they ask the factory. This
is also the seam that made deleting the 13.8 MB vendored YOLOv5 tree a
one-line change per call site.

## Stop 5 — The graph fallback engine

**`src/hokage_vision/agents/providers/langgraph_provider.py`** — `_NativeEngine`
and `LangGraphProvider`

The LangGraph provider builds a real `StateGraph` when langgraph is
installed, and transparently falls back to a tiny built-in engine with the
same `add_node / add_conditional_edges / compile / invoke` API when it is
not — so the agent layer works in every environment and CI stays
dependency-light. The fallback exists because StateGraph's dict-replacement
semantics bit us once; every node returns the full state for that reason.

## Stop 6 — Real evaluation, not fake numbers

**`src/hokage_vision/vision/evaluation.py`** — `_real_metrics`

`evaluate_model(mock=False)` runs a genuine `ultralytics val` pass and
extracts mAP50 / mAP50-95 / precision / recall from `results.box`; every
failure mode (missing train extra, missing model, missing yaml, missing
data) raises a typed `VisionBackendError` with an install hint. The reported
mAP50 0.995 in [`docs/benchmarks.md`](benchmarks.md) comes from this code
path, and the integration test asserts it.

## Stop 7 — The FPS benchmark

**`src/hokage_vision/vision/benchmark.py`** — `benchmark_fps`

Backend-agnostic CPU benchmark with warmup, per-image FPS, and
mean/median/stdev/min/max latency. Works on any vision backend (ABC
contract: `load / predict_image / predict_frame / batch_predict / close`),
so mock backends are benchmarkable too. Exposed as
`hokage-vision model benchmark`.

## Stop 8 — Training with a guardrail

**`src/hokage_vision/training/trainer.py`** — `run_yolo_training`

The trainer refuses to overwrite an existing output directory (a
`HokageVisionError` before ultralytics is ever imported), validates the
dataset yaml first, and defaults to dry-run planning. Together with
`smoke.py` this gives the agent safe training verbs: the agent can *plan*
training on any machine and only *execute* where the train extra is
installed.

---

## Reading order for reviewers with 10 minutes

1. Stop 1 + 2 (agent loop + safety) — this is the project's thesis.
2. Run `python examples/agent_demo.py` — the loop, live, no key.
3. Run the [30-second fresh-clone demo](../README.md#30-second-demo-works-on-a-fresh-clone) — real ONNX detection.
4. Skim `docs/adr/` for the *why* behind Stop 4 and Stop 5.
