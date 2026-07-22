# Hokage Vision Agent

**Agentic anime character detection workbench — YOLO backends, PySide6 desktop, FastAPI, Typer CLI, tool-calling agent.**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-%3E%3D3.12-blue.svg)](pyproject.toml)

Portfolio-grade CV workbench. Detection is performed by a **vision backend** (mock / Ultralytics / legacy YOLOv5). The **agent does not invent labels**; it only chooses safe project tools (detect, validate dataset, smoke train, evaluate, compare, registry updates).

Docs site (MkDocs): <https://phoenix0531-sudo.github.io/Hokage_Vision_Agent/>

## Screenshots / evidence

<table>
  <tr>
    <td width="50%">
      <img src="docs/screenshots/evidence.png" alt="Mock backend detection evidence">
      <br><strong>Mock detection evidence</strong> — deterministic boxes from <code>MockBackend.predict_image</code>
    </td>
    <td width="50%">
      <img src="docs/screenshots/preview.png" alt="Architecture schematic">
      <br><strong>Architecture schematic</strong> — CLI / GUI / API → InferenceService → backends
    </td>
  </tr>
</table>

```bash
# reproducible, no private weights / GPU
PYTHONPATH=src python scripts/generate_evidence.py
# writes docs/screenshots/evidence.png + fixtures/demo_scene.png
```

Default demo classes: `obito`, `naruto`, `gaara` with fixed confidence schedule (`0.91`, `0.84`, `0.77`) and relative boxes — same path CI uses.

## Design boundaries

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
- Default backend is **`mock`**: deterministic boxes so CI and demos need no GPU or private weights
- Destructive / real training paths use careful / dry-run style entrypoints
- Legacy YOLOv5 stays behind a dedicated backend — do not copy legacy package guts into `src/hokage_vision`

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

Console script: `hokage-vision = hokage_vision.cli:main`.

### CLI surface

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

Docker-first path:

```bash
docker compose build
docker compose run --rm test
```

## Quick usage

```bash
python -c "import hokage_vision; print(hokage_vision.__version__)"
hokage-vision --help
hokage-vision detect --help

# CI default paths
pytest -q tests/unit tests/integration

# evidence figure
PYTHONPATH=src python scripts/generate_evidence.py
```

GUI and full training need corresponding extras and (for real weights) local files under `models/` — see `docs/usage.md` and `docs/data-and-models.md`.

## Config

- `configs/app.default.yaml` — mock backend default
- `configs/model.default.yaml`
- `configs/agent.default.yaml`
- `configs/dataset.example.yaml`, `configs/training.example.yaml`

## Tests and CI

| Layer | Location |
|-------|----------|
| Unit | `tests/unit/` — mock backend, inference, registry, agent tools, dataset, rendering, … |
| Integration | `tests/integration/` — API health, CLI detect mock, CLI help |
| GUI | `tests/gui/` — separate workflow |
| Packaging | `tests/packaging/` |

Product `CI` workflow: Python **3.12**, hard editable install `.[dev,api]`, critical ruff, pytest **unit + integration only** (GUI has its own workflow).

## Scope

- **In:** anime-character detection workbench, multi-surface UX (CLI/API/GUI), agent tool layer, dataset/train scaffolding, reproducible mock evidence
- **Out:** production content-moderation SaaS; guaranteed SOTA without your own training data; committing private YOLO weights

## License

Apache-2.0. See [LICENSE](LICENSE) and `THIRD_PARTY_NOTICES.md`.
