# Hokage Vision Agent

**Agentic anime character detection workbench — YOLO, PySide6, Docker, tool workflows.**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml)
[![License: Apache_2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

Agentic anime character detection workbench — YOLO, PySide6, Docker, tool workflows.

Desktop + API. Config-driven. CI-hardened.


## Screenshots

![Sample image](docs/screenshots/sample-detect.jpg)

## Features

- 🥷 YOLO-family detection for anime characters
- 🖥️ PySide6 desktop flows under `apps/`
- ⚙️ Config-driven experiments in `configs/`
- 🐳 Docker + multi-flavor requirements (api / desktop / docker)
- 🧪 Unit + integration tests; GUI suite in dedicated workflow
- 📦 Hatch `src/hokage_vision` layout, editable install on CI

## Get started

### Install

```bash
git clone https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent.git
cd Hokage_Vision_Agent
python -m pip install -e ".[dev,api]"
# desktop extras / docker: see requirements-*.txt and docs/
```

### Usage

```bash
# API-oriented path (example)
uvicorn ...   # see apps/ and docs for current entrypoints

# package smoke
python -c "import hokage_vision; print('ok')"
pytest -q tests/unit tests/integration
```

## Project layout

```
src/hokage_vision/
apps/  configs/  assets/  examples/  models/
tests/{unit,integration,gui,packaging}
.github/workflows/{ci,gui-tests,docker,...}.yml
```

## Notes

Portfolio CV workbench — not a production content-moderation system.

## License

Apache-2.0. Free for commercial use with attribution where applicable. See [LICENSE](LICENSE).
