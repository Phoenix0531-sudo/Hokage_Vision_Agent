<section class="hero">
  <h1>Hokage Vision Agent</h1>
  <div class="tagline">Anime character detection with YOLO, PySide6, Docker, and safe Agent workflows.</div>
  <p>
    A portfolio-grade computer vision workbench: mock-first demos, external model weights,
    dataset license guardrails, and project-scoped Agent tools.
  </p>
  <div class="grid">
    <div class="pill"><strong>Vision</strong>Image, video, and folder detection through shared services.</div>
    <div class="pill"><strong>Agent</strong>Rule-based tool orchestration without API keys by default.</div>
    <div class="pill"><strong>DevOps</strong>Docker-first tests, docs, API, package, and desktop builds.</div>
  </div>
</section>

An agentic computer vision workbench for anime character detection, powered by YOLO, PySide6, Docker, and tool-calling workflows.

This is a fan-made research and portfolio project and is not affiliated with Naruto, Shueisha, Pierrot, or related copyright holders.

## Project Positioning

Hokage Vision Agent is a training-ready and model-ready workbench, not a public redistribution of Naruto/Hokage datasets or weights. The repository demonstrates the production workflow around an anime character detector: controlled data governance, pluggable YOLO backends, desktop/API/CLI surfaces, Docker validation, and Agent-scoped orchestration.

The default demo uses a mock backend and a tiny synthetic YOLO smoke dataset. Any real character data or trained weights are external artifacts that require source, license, redistribution, metrics, and release review before publication.

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

## Portfolio Demo

```bash
docker compose run --rm test hokage-vision dataset validate configs/dataset.example.yaml
docker compose run --rm test hokage-vision detect image examples/images/sample.jpg --backend mock
docker compose run --rm test hokage-vision agent run "训练模型"
docker compose up api
```
