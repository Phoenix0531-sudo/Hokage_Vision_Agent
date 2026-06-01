# Hokage Vision Agent

An agentic computer vision workbench for anime character detection, powered by YOLO, PySide6, Docker, and tool-calling workflows.

This is a fan-made research and portfolio project and is not affiliated with Naruto, Shueisha, Pierrot, or related copyright holders.

## What This Project Demonstrates

- Modern Python package structure.
- Shared computer vision inference services for CLI, GUI, API, and Agent workflows.
- Safe rule-based Agent orchestration with allowlisted project tools.
- Docker-first testing, docs, package, API, and desktop build workflows.
- Data governance, model registry, evaluation, comparison, and training guardrails.

## Default Demo Mode

The default backend is `mock`. It does not download model weights, use GPU, or require private data. This keeps tests, CI, and demos reproducible.

```bash
docker compose build
docker compose run --rm test
docker compose run --rm gui-test
```
