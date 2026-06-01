# Hokage Vision Agent Refactor Plan

This checklist tracks the staged migration from the legacy YOLOv5 + PySide6 project to the portfolio-ready Hokage Vision Agent project. Each phase must remain reviewable and end with a focused commit.

- [x] Phase 0: Project audit and license audit
- [x] Phase 1: Docker-first project skeleton
- [x] Phase 2: Configuration system and core detection types
- [x] Phase 3: Mock backend, rendering, and inference service
- [x] Phase 4: CLI
- [x] Phase 5: Agent tool registry and rule-based provider
- [x] Phase 6: Dataset manifest, validation, and annotation helpers
- [x] Phase 7: Training skeleton and smoke training
- [x] Phase 8: Model registry, evaluation, and comparison
- [x] Phase 9: Ultralytics and legacy YOLOv5 backends
- [x] Phase 10: Modern PySide6 desktop interface
- [x] Phase 11: FastAPI service
- [x] Phase 12: Python package build workflow
- [x] Phase 13: Desktop executable build workflow
- [x] Phase 14: CI, documentation, release, and governance
- [ ] Phase 15: Final portfolio polish

## Working Rules

- Keep commits small and use Conventional Commits.
- Do not commit model weights, private datasets, API keys, or generated training output.
- Keep the legacy YOLOv5 code isolated from the new `src/hokage_vision` package.
- Use mock backends for CI, GUI smoke tests, API smoke tests, and agent tests.
- Default real training to dry-run unless the user explicitly asks for execution.
- Do not add web scraping or redistribution of copyrighted Naruto/Hokage imagery.

## Review

### Phase 0

- Added migration, license audit, legacy, and third-party notice documents.
- Confirmed the repository currently has upstream-like YOLOv5 code mixed with project-specific PySide6 GUI files.
- Confirmed there is no root `LICENSE` file in the current repository.
- Confirmed hardcoded local Qt plugin and `runs/train/exp/weights/best.pt` paths in the legacy GUI.
- No old code was moved or deleted in this phase.

### Phase 1

- Added `pyproject.toml`, the initial `src/hokage_vision` package, app entrypoint placeholders, tests, Dockerfile, Docker Compose services, Dev Container config, Makefile, `.env.example`, `.editorconfig`, bilingual README placeholders, and MkDocs skeleton.
- Kept legacy YOLOv5 files in place; no old code was moved or deleted.
- Docker build initially exposed local daemon/network instability and heavy dependency cost; the final base image installs Python dev dependencies but avoids apt system packages in the core test image.
- `test` service disables pytest plugin autoload so non-GUI tests do not require Qt bindings. GUI tests will use the separate `gui-test` service.
- Verified `docker compose build` and Docker package import.

### Phase 2

- Added YAML configuration files and a Pydantic settings loader with default config plus override merging.
- Added shared detection dataclasses for boxes, detections, image results, video summaries, and model info.
- Added base project exceptions, logger helper, project root discovery, and a minimal i18n dictionary.
- Added unit tests for config loading and core detection types.
- Verified the Phase 2 test command in Docker.

### Phase 3

- Added the `VisionBackend` interface and deterministic `MockBackend`.
- Added `InferenceService` for image, folder, and video entrypoints, with folder progress callbacks and optional rendered/JSON output.
- Added PIL-based detection rendering.
- Added lightweight vision placeholders for future video, batch, evaluation, and model comparison work.
- Added unit tests for mock prediction, folder inference, and rendering.
- Verified Ruff on the new vision code and the Phase 3 Docker test command.

### Phase 4

- Expanded `hokage-vision` into a Typer CLI with detect, dataset, train, model, agent, GUI, and API command groups.
- Wired mock image and folder detection to `InferenceService`; video command is present and reports missing OpenCV cleanly until video dependencies are introduced.
- Added stable placeholders for dataset validation, manifest creation, smoke training, YOLO training dry-run, model list/register/evaluate/compare, agent run, GUI, and API.
- Added a generated, non-copyright sample image for mock CLI tests.
- Added CLI usage docs and integration tests for help and mock image detection.
- Verified CLI commands, integration tests, and Ruff.

### Phase 5

- Added agent state dataclasses, allowlisted tool registry, default project-scoped tools, safety refusals, and RuleBasedAgent.
- Wired CLI `hokage-vision agent run` to the rule-based provider.
- Registered detect image/folder/video, smoke training, model comparison, project health, reporting, dataset, annotation, training, and model-management tools.
- Kept non-implemented tools as explicit dry-run placeholders.
- Added OpenAI and LangGraph provider placeholders without API key requirements.
- Added tests for tool registration, allowlist enforcement, project-scoped routing, and out-of-scope refusal.
- Verified `hokage-vision agent run "检测 examples/images 里的图片"`, targeted tests, and Ruff.

### Phase 6

- Added dataset manifest schema/load/create helpers with source, license, redistribution, classes, and annotation review fields.
- Added YOLO dataset yaml loading and validation for split paths, labels, class ids, bbox ranges, missing labels, empty labels, class distribution, manifest presence, image count, and box count.
- Added annotation assistance that writes candidate YOLO labels and a `review_required.yaml` file without overwriting existing labels by default.
- Added data directory guidance and `.gitkeep` placeholders for manifests/raw/interim/processed.
- Wired dataset validation, manifest creation, and annotation assistance into CLI and Agent tools.
- Added scripts for dataset manifest creation, preparation, annotation assistance, auto-labeling, review, and splitting.
- Added data governance and annotation docs.
- Verified dataset validation CLI, targeted unit tests, and Ruff.

### Phase 7

- Added training job dataclass, mock smoke training, and YOLO training dry-run planner.
- Real YOLO training validates datasets first, refuses invalid datasets, refuses to overwrite existing output directories, and requires the `train` extra.
- Wired CLI `train smoke` and `train yolo --dry-run` to the training layer.
- Wired Agent `smoke_train` and `train_model` tools to safe training flows.
- Added smoke training script and training docs.
- Verified smoke training command, YOLO dry-run command, and Ruff.

### Phase 8

- Added local model registry support for listing and registering model metadata.
- Added mock evaluation and path-based model comparison with metrics, class list, size, license, and notes fields.
- Wired CLI model list, register, evaluate, and compare commands to actual logic.
- Wired Agent model list, register, evaluate, and compare tools to actual logic.
- Added model README, registry example, model-zoo docs, and model registry/comparison tests.
- Verified `hokage-vision model list`, `hokage-vision model compare --models models/a.pt models/b.pt --mock`, targeted tests, and Ruff.

### Phase 9

- Added `UltralyticsBackend` with explicit model path, conf/iou/device/imgsz settings, lazy import, and clear missing dependency/path errors.
- Added `YOLOv5LegacyBackend` as a compatibility boundary that requires explicit weights and isolated legacy source, with no hardcoded `best.pt` path.
- Added reserved `ONNXBackend` placeholder with clear unsupported errors.
- Added `download_model.py` helper restricted to reviewed GitHub Release URLs.
- Updated model docs with backend guidance and no-hardcoded-weight statement.
- Added lightweight backend tests that do not download weights or require GPU.
- Verified mock flow still passes, missing weight errors are readable, and Ruff passes.

### Phase 10

- Added a PySide6 desktop shell with Overview, Image Detection, Video Detection, Batch Detection, Agent Assistant, Settings, and About pages.
- Added dark/light theme helpers, basic zh-CN/en-US UI text mapping, result table, statistics panel, settings controls, and worker-thread scaffolding.
- Wired image detection and Agent Chat panels to the shared mock-backed inference and rule-based agent layers.
- Added headless pytest-qt GUI smoke tests for the main window, image detection panel, settings panel, and agent chat panel.
- Reworked Docker GUI testing around `python:3.12-slim-bookworm`, separate test/gui dependency stages, BuildKit apt/pip caches, and optional Debian mirror build args.
- Added Docker-specific requirement files without replacing the legacy YOLOv5 `requirements.txt`.
- Verified GUI tests, targeted Ruff checks, and normal Docker package import.

### Phase 11

- Added a FastAPI app package with shared route handlers and request schemas.
- Implemented local JSON endpoints for health, models, image detection, folder detection, agent run, dataset validation, smoke training, and model comparison.
- Kept the API mock-backed by default and left real training out of the exposed API surface.
- Wired `apps/api/main.py`, `hokage-vision api`, and Docker Compose `api` to the same app.
- Added API usage docs and integration tests for `/health` and mock image detection.
- Verified API tests, full unit/integration tests, Ruff checks, and Docker Compose API health response.

### Phase 12

- Added `scripts/build_package.py` as a thin wrapper around `python -m build`.
- Added package build documentation and MkDocs navigation.
- Added a package workflow that builds sdist/wheel, installs the wheel, checks `hokage-vision --help`, and uploads artifacts.
- Added a packaging test that builds sdist/wheel, installs the wheel in a temporary venv, and validates the console script.
- Added package build tooling to the Docker test dependency layer and included packaging tests in the `test` service.
- Verified Docker package build, packaging test, Ruff checks, and full unit/integration/packaging tests.

### Phase 13

- Added a PyInstaller desktop build script that targets the PySide6 desktop entrypoint and excludes large model frameworks from the executable bundle.
- Added a desktop build workflow with Linux as the required target and Windows/macOS as best-effort matrix targets.
- Added desktop executable documentation and clarified that model weights remain external runtime assets.
- Added the `binutils` system dependency to the GUI/desktop Docker layer so PyInstaller can inspect Linux shared libraries.
- Verified Ruff checks, Docker desktop build, and headless GUI smoke tests.

### Phase 14

- Added CI, GUI test, docs deploy, Docker, release, CodeQL, and Dependabot workflows.
- Replaced the legacy YOLOv5 contributing guide with Hokage Vision Agent governance, security, conduct, citation, changelog, PR template, and issue templates.
- Added scoped Apache-2.0 license text plus `LICENSES/README.md`, keeping legacy YOLOv5, datasets, annotations, and weights under separate license boundaries.
- Upgraded English and Chinese README files with badges, Docker-first usage, CLI/GUI/API/Agent examples, data/training workflow, architecture notes, roadmap, and license warnings.
- Added missing MkDocs pages for installation, architecture, dataset format, contributing, roadmap, and changelog.
- Adjusted Docker docs service so `docker compose run --rm docs mkdocs build` works without runtime dependency installation.
- Scoped Ruff away from legacy YOLOv5 files and made default pytest skip GUI tests by test path, while GUI tests run in the dedicated PySide6 image.
- Verified Ruff checks, default pytest, headless GUI tests, MkDocs build, workflow YAML parsing, and docs Docker target build.
