# Hokage Vision Agent

An agentic computer vision workbench for anime character detection, powered by YOLO, PySide6, Docker, and tool-calling workflows.

This is a fan-made research and portfolio project and is not affiliated with Naruto, Shueisha, Pierrot, or related copyright holders.

## Status

This repository is being migrated from a legacy YOLOv5 + PySide6 project into a portfolio-ready open source project.

## Docker-first Quick Start

```bash
docker compose build
docker compose run --rm test
```

## Local Optional Install

```bash
python -m venv .venv
pip install -e ".[dev,gui,api,train]"
```

## Documentation

GitHub Pages documentation will be published from the MkDocs site in `docs/`.

## License

New project source code is planned for Apache-2.0 after legacy code isolation and license audit. Legacy YOLOv5 code remains governed by its upstream license.
