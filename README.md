# Hokage Vision Agent

**Agentic anime character detection workbench — YOLO backends, PySide6 desktop, FastAPI, Typer CLI, tool-calling agent.**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Portfolio-grade CV workbench. Detection is performed by a **vision backend** (mock / Ultralytics / legacy YOLOv5). The **agent does not invent labels**; it only chooses safe project tools (detect, validate dataset, smoke train, evaluate, compare, registry updates).

Docs site (MkDocs): <https://phoenix0531-sudo.github.io/Hokage_Vision_Agent/>

## Preview

![Hokage Vision Agent](docs/screenshots/preview.png)

## Design boundaries (from project architecture)

```
CLI / PySide6 GUI / FastAPI
        │
        ▼
 InferenceService  ◄── Agent tools (RuleBasedAgent + ToolRegistry)
        │
        ▼
 VisionBackend: MockBackend | UltralyticsBackend | YOLOv5LegacyBackend
        │
        ▼
 Dataset / Training / Model registry
```

- Shared core types and services across CLI, API, GUI, Agent
- Default backend is **`mock`**: deterministic boxes for demo classes (`obito`, `naruto`, `gaara`) so CI and demos need no GPU or private weights
- Destructive / real training paths default to careful / dry-run style entrypoints
- Legacy YOLOv5 stays behind a dedicated backend; do not copy legacy package guts into `src/hokage_vision`

## Package map (`src/hokage_vision`)

| Area | Role |
|------|------|
| `vision/` | Inference service, backends factory, evaluation, compare |
| `agents/` | Orchestrator, tool registry, safety, rule / OpenAI / LangGraph providers |
| `api/` | FastAPI app + routes + schemas |
| `cli.py` | Typer multi-command CLI (`hokage-vision`) |
| `data/` | YOLO dataset helpers, manifest, validation, split, annotation assist |
| `training/` | Trainer, smoke train, model registry |
| `config/` | YAML settings loader (`configs/*.yaml`) |
| `reports/` | Markdown report helpers |

Console script (pyproject): `hokage-vision = hokage_vision.cli:main`.

### CLI surface (real typer groups)

```text
hokage-vision detect ...
hokage-vision dataset ...
hokage-vision dataset manifest ...
hokage-vision annotation ...
hokage-vision train ...
hokage-vision model ...
hokage-vision agent ...
```

## Install

Python **>= 3.12**. Hatchling src layout.

```bash
git clone https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent.git
cd Hokage_Vision_Agent
python -m pip install -e ".[dev,api]"
# optional extras: gui, train (ultralytics), llm, desktop-build, docs, all
```

Docker-first path (recommended in `docs/getting-started.md`):

```bash
docker compose build
docker compose run --rm test
```

## Quick usage

```bash
# package import smoke
python -c "import hokage_vision; print(hokage_vision.__version__)"

# CLI help
hokage-vision --help
hokage-vision detect --help

# unit + integration (CI default paths)
pytest -q tests/unit tests/integration
```

GUI and full training need the corresponding extras and (for real weights) local model files under `models/` — see `docs/usage.md` and `docs/data-and-models.md`.

## Config

Default app config: `configs/app.default.yaml` (mock backend). Also:

- `configs/model.default.yaml`
- `configs/agent.default.yaml`
- `configs/dataset.example.yaml`, `configs/training.example.yaml`

## CI layout

Product `CI` workflow: Python 3.12, editable install `.[dev,api]`, critical ruff on `src` + unit/integration, pytest unit + integration.  
Separate workflows exist for GUI tests, Docker, package, docs, desktop build, CodeQL.

## Scope

- **In:** anime-character detection workbench, multi-surface UX (CLI/API/GUI), agent tool layer, dataset/train scaffolding
- **Out:** production content moderation SaaS, guaranteed SOTA accuracy without your own training data

## License

Apache-2.0. See [LICENSE](LICENSE) and `THIRD_PARTY_NOTICES.md`.
