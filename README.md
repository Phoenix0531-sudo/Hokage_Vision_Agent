# Hokage Vision Agent

**Agentic anime character detection workbench: YOLO, PySide6, Docker, tool workflows.**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Desktop plus API. Config-driven experiments. CI-hardened packaging.

## Preview

![Hokage Vision Agent](docs/screenshots/preview.png)

## Features

- YOLO-family detection pipeline for anime characters
- PySide6 desktop flows under apps/
- Config-driven runs under configs/
- Hatch src/hokage_vision layout with editable install on CI
- Unit + integration tests; GUI suite lives in a dedicated workflow

## Get started

### Install

```bash
git clone https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent.git
cd Hokage_Vision_Agent
python -m pip install -e ".[dev,api]"
```

### Usage

```bash
python -c "import hokage_vision; print('ok')"
pytest -q tests/unit tests/integration
```

## Project layout

```
src/hokage_vision/
apps/  configs/  examples/  models/
tests/{unit,integration,gui,packaging}
```

## Notes

Portfolio CV workbench, not a production moderation system.

## License

Apache-2.0. Free for commercial use with attribution where applicable. See [LICENSE](LICENSE).
