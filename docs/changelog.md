# Changelog

## 0.1.2 (2026-09-11)

### Added
- Real LLM agent providers with function calling: `OpenAIProvider` (planner loop over injectable client, refusal-first, max-steps budget) and `LangGraphProvider` (StateGraph plan/execute pipeline with native fallback engine). Factory: `create_agent("openai" | "langgraph")`; `POST /agent/run` gains a `provider` field. Offline-testable via fake clients; `llm` extra installs openai + langgraph.
- Real mAP evaluation: `evaluate_model(mock=False)` runs ultralytics `val` and reports mAP50/mAP50-95/precision/recall; CLI `model evaluate --real` and new `model benchmark` command (warmup/repeats FPS + latency stats) via `vision/benchmark.py`.
- Quality pass: CLI in-process CliRunner tests (22), rule-based agent tests (20), trainer real-path tests, vision re-export tests — coverage 77% → 93% with CI gate at 85%; actions upgraded to checkout@v7 / setup-python@v7 / codeql-action@v4 / artifact actions latest (Node 20 deprecation fix); advisory pip-audit CI job with report artifact; `docs/api.md` endpoint reference with mkdocs nav entry.
- Release engineering: `docker` workflow now pushes the API image to GHCR (master → `latest` + short SHA; tags → `vX.Y.Z`); release workflow builds desktop artifacts for linux, windows, and macos and attaches all available zips to the GitHub Release.

### Changed
- Replaced placeholder default API host with `127.0.0.1` so `hokage-vision api` starts without flags; container CMD uses `0.0.0.0`.
- Fixed dataset-manifest agent test leaking `data/manifests/local.yaml` into the repo root.
- CLI `generate_report` tool now passes keyword arguments (was positional and raised TypeError).

## 0.1.1 (2026-09-10)

### Added
- Closed-loop training demo: `scripts/closed_loop_demo.py` generates a synthetic dataset, fine-tunes yolov8n on CPU, exports ONNX, and runs real inference through `UltralyticsBackend` (24/24 val accuracy; see `models/model-card.synthetic-shapes.md`).
- Quickstart demo: `python examples/quickstart.py` walks detect → validate → smoke-train → agent → report in one command (see `docs/quickstart.md`).
- Real ONNX inference integration tests, video pipeline tests (synthetic MP4), 10 API endpoint tests, GUI interaction tests, and 38 new unit tests (39 → 86+ total).
- Demo video with real trained-model overlay: `examples/videos/demo.mp4`.
- Coverage gate with XML artifact upload in CI.

### Changed
- Removed vendored legacy YOLOv5 toolchain (`legacy/`, 177 files); provenance preserved in git history and documented in `docs/license-audit.md`, `docs/migration.md`, `THIRD_PARTY_NOTICES.md`, and `LICENSES/README.md`.
- Fixed pre-existing lint warnings in `scripts/capture_real_shots.py` and `scripts/generate_evidence.py`; `ruff check` is now clean across the repo.
- Fixed environment-dependent assertion in `tests/unit/test_core_paths.py` that failed in Docker CI.

### Added (previous)
- Added Docker-first project structure and dependency-layer caching.
- Added mock backend, shared inference service, rendering, CLI, API, GUI, Agent tools, dataset validation, annotation assistance, smoke training, model registry, evaluation, and comparison foundations.
- Added package build, desktop build, CI, GUI tests, docs, release, CodeQL, Dependabot, and repository governance files.
- Added license audit, third-party notices, and data/model distribution guardrails.
