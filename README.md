# Hokage Vision Agent

**Anime character detection workbench (YOLO + PySide6)**

[English](README.md) | [中文](README.zh-CN.md)

![CI](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

Agentic **anime character detection** workbench: YOLO-family models, PySide6 desktop flows, configs under `configs/`, apps under `apps/`.

## Why this exists

Fan / research CV demos need more than a notebook: model configs, desktop labeling / inference UI, and CI for non-GUI pieces.

## Features

- Multi-app layout under `apps/`
- Config-driven experiments in `configs/`
- Assets / examples for demos
- Multiple requirements flavors (api / desktop-build / docker)

## Install

```bash
git clone https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent.git
cd Hokage_Vision_Agent
pip install -r requirements-api.txt   # or desktop-build / docker variants
```

## Usage

Follow `apps/` entry modules and `docs/` for the desktop vs API path you need. Example scripts live under `examples/` when present.

## Project layout

```
apps/ configs/ assets/ examples/ models/ data/
docs/
```

## License

MIT. Free for commercial use with attribution. See [LICENSE](LICENSE).
